'''
simulate_drone_flight.py

Generates a simulation of historic drone flight paths using the graph generalized in reconstruct_flight_path.py
'''

# import script(s)
import reconstruct_flight_path

# Import data structures
import pandas as pd

# Import visualizations
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Import graphical structure
import networkx as nx

#---------------------------------------------------------------------------------------------------------------------

# Function used to simulate historic drone flights, bringing in context
def simulate_flight(input,
                    error_log=None,
                    save_path=None,
                    interval=300,
                    export_gif=False):

    # Get the graph
    G, _ = reconstruct_flight_path.construct_flight_path(input)

    # Add error entities, if available
    if error_log:
        error_log_df = pd.read_csv(error_log)
        error_log_df["timestamp"] = pd.to_datetime(
            error_log_df["timestamp"],
            format="%Y-%m-%d %H:%M:%S",  # <-- or %f if milliseconds are included
            errors='coerce'
        )
    else:
        error_log_df = pd.DataFrame(columns=["timestamp", "log_message"])

    # Normalize both timestamps to be tz-naive (no timezone awareness)
    error_log_df["timestamp"] = pd.to_datetime(
        error_log_df["timestamp"], errors='coerce'
    ).dt.tz_localize(None)

    # Get IMU-calculated coordinates
    pos = nx.get_node_attributes(G, "pos")

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    plt.subplots_adjust(top=0.85)

    # Set axis limits to give space around the path
    x_vals, y_vals = zip(*pos.values())
    padding = 0.0005
    ax.set_xlim(min(x_vals) - padding, max(x_vals) + padding)
    ax.set_ylim(min(y_vals) - padding, max(y_vals) + padding)

    # Draw all edges in the background
    nx.draw(G,
            pos,
            edge_color="whitesmoke",
            node_color="none",
            ax=ax,
            alpha=0.1)

    # Scatter frame by frame
    node_scatter = ax.scatter([],
                              [],
                              s=100,
                              edgecolors='black',
                              zorder=3)

    # Initialize the trail
    trail_x, trail_y = [], []

    trail_line, = ax.plot([],
                         [],
                         color="teal",
                         linewidth=3,
                         alpha=0.4)

    # Set visualization's title
    title = ax.set_title("", fontsize=10)

    # Get list of positions
    coords = [pos[n] for n in G.nodes]

    # Get list of nodes
    nodes = list(G.nodes)

    # Only include every 10th normal frame, but keep all anomalies
    filtered_frames = [i for i, n in enumerate(nodes)
                       if G.nodes[n]["activity"] == -1 or i % 25 == 0]

    # Get total number of frames
    total_frames = len(filtered_frames)

    # Update visual
    def update(frame_idx):
        node_id = nodes[frame_idx]
        node = G.nodes[node_id]
        coord = pos[node_id]   # and its coordinate

        # Apply color logic used to visually describe events
        color = "red" if node["activity"] == -1 else "green"
        node_scatter.set_offsets([coord])   # Sets position
        node_scatter.set_color(color)       # Set color

        # Append current node to trail
        trail_x.append(coord[0])
        trail_y.append(coord[1])
        trail_line.set_data(trail_x, trail_y)

        # Context of activity
        if node["activity"] == -1:
            title.set_text(
                f"SUSPICIOUS BEHAVIOR DETECTED!\n"
                f"Time: {node['timestamp']}\n"
                f"Score: {node['anomaly_score']}\n"
                f"Velocity: {node['velocity']}\n"
                f"distance: {node['distance']}\n"
            )

            # Show error log message if timestamp matches
            if not error_log_df.empty:
                current_time = pd.to_datetime(node['timestamp'], errors='coerce')

                # Get all logs within ±1 second of current timestamp
                nearby_logs = error_log_df[
                    error_log_df["timestamp"].between(current_time - pd.Timedelta(seconds=3),
                                                      current_time + pd.Timedelta(seconds=3))
                ]

                if not nearby_logs.empty:
                    combined_logs = "\n".join(nearby_logs["log_message"].astype(str).tolist())

                    ax.text(0.5, -0.1, f"📝 Log: {combined_logs}",
                            fontsize=9,
                            transform=ax.transAxes,
                            ha='center',
                            va='top',
                            bbox=dict(facecolor='lightyellow', edgecolor='black', boxstyle='round,pad=0.3'))

            for txt in ax.texts:
                txt.remove()

        else:
            title.set_text(
                f"Behavior: Normal\n"
                f"Time: {node['timestamp']}\n"
                f"Score: {node['anomaly_score']}\n"
                f"Velocity: {node['velocity']}\n"
                f"distance: {node['distance']}\n"
            )

            for txt in ax.texts:
                txt.remove()

        return node_scatter, trail_line, title

    # Create animation
    ani = animation.FuncAnimation(fig,
                                  update,
                                  frames=filtered_frames,
                                  interval=interval,
                                  blit=False,
                                  repeat=False)

    # Save visual if desired
    if save_path:
        writer = "pillow" if export_gif else "ffmpeg"
        ext = ".gif" if export_gif else ".mp4"

        ani.save(save_path + ext,
                 writer=writer,
                 fps=1000 // interval)

    else:
        plt.show()

log = pd.read_csv("/Users/ladylo/PycharmProjects/FlightForensics/data/processed/logs/flight/DF061/anomaly_detection/model_ready/flight_anomaly_dataset.csv")
log = log[log["flight_sequence"] == "flight04"].reset_index(drop=True)
simulate_flight(log,
                error_log="/Users/ladylo/PycharmProjects/FlightForensics/data/processed/logs/error/DF061/cleaned_19-06-2018-11VKF5500202NZ_error_log.csv",
                save_path="/Users/ladylo/PycharmProjects/FlightForensics/src/visualization")