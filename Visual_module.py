import matplotlib.pyplot as plt
import sys
import json

# Was written by chatGPT
def plot_algorithms(data):
    fig, axs = plt.subplots(1, 3, figsize=(18, 6), dpi=120)  # Create a figure with 3 subplots for each algorithm

    colors = plt.get_cmap("tab20")  # Use a colormap with 20 distinct colors

    for i, (alg_name, alg_data) in enumerate(data.items()):
        clusters = alg_data["clusters"]
        centroids = alg_data["centers"]

        # Select the subplot for the current algorithm
        ax = axs[i]
        ax.set_title(alg_name)  # Set the title to the algorithm's name
        ax.set_aspect('equal', 'box')

        # Plot cluster points for the current algorithm
        for j, cluster in enumerate(clusters):
            x_vals, y_vals = zip(*cluster)
            color = colors(j % 20)  # Apply a unique color for each cluster
            ax.scatter(x_vals, y_vals, color=color, marker='o', s=1, alpha=0.6)

        # Plot centroids for the current algorithm
        centroid_x, centroid_y = zip(*centroids)
        ax.scatter(centroid_x, centroid_y, color='black', marker='o', s=5)

        # Configure axis limits and grid
        ax.set_xlim(-5000, 5000)
        ax.set_ylim(-5000, 5000)
        ax.grid(True)

    plt.suptitle("Comparison of Clustering Algorithms")  # Set the main title for all subplots
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust layout for better spacing
    plt.show()


def plot_clusters(clusters, centroids, alg_name):
    plt.figure(figsize=(10, 10), dpi=120)
    colors = plt.get_cmap("tab20")
    # Drawing clusters with their own colors
    for i, cluster in enumerate(clusters):
        x_vals, y_vals = zip(*cluster)
        plt.scatter(x_vals, y_vals, color=colors(i), marker='o', s=1)
    # Drawing centroids
    centroid_x, centroid_y = zip(*centroids)
    plt.scatter(centroid_x, centroid_y, c='black', marker='o', s=10)
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Result of " + str(alg_name))
    plt.xlim(-5000, 5000)
    plt.ylim(-5000, 5000)
    plt.grid(True)
    plt.show()

def main():
    # Getting the path to the JSON file
    filename = sys.argv[1]
    alg_name = sys.argv[2]
    with open(filename, 'r') as f:
        data = json.load(f)
    if filename == "all_algorithms_data.json":
        plot_algorithms(data)
    else:
        clusters = data["clusters"]
        centroids = data["centers"]
        plot_clusters(clusters, centroids, alg_name)

if __name__ == "__main__":
    main()
