import random
import math
import json
import subprocess
import sys

# Function that is used to put all data: centers of clusters and clusters to json file.
# Because PyPy is not compatible to matplotlib we have to put all computed data to file.
def save_clusters_to_json(clusters, centers, filename="clusters_data.json"):
    data = {"clusters": clusters, "centers": centers}
    with open(filename, 'w') as f:
        json.dump(data, f)

# Function to create first random 20 points
def first_points(points):
    # creating set of bods (set will provide us with unique starting bods)
    points_set = set()
    while len(points_set) < 20:
        x = random.randint(-5000, 5000)
        y = random.randint(-5000, 5000)
        points_set.add((x, y))
    points.extend(points_set)

# Function to create all other points
def create_points(number_points, points):
    while len(points) < number_points + 20:
        base_point = random.choice(points)
        # In this part we check the X-axis
        if base_point[0] > 4900:
            #too close to right border
            x = random.randint(base_point[0] - 100, 5000)
        elif base_point[0] < -4900:
            #too close to left border
            x = random.randint(-5000, base_point[0] + 100)
        else:
            x = random.randint(base_point[0] - 100, base_point[0] + 100)

        # In this part we check the Y-axis
        if base_point[1] > 4900:
            # too close to upper border
            y = random.randint(base_point[1] - 100, 5000)
        elif base_point[1] < -4900:
            # too close to lower border
            y = random.randint(-5000, base_point[1] + 100)
        else:
            y = random.randint(base_point[1] - 100, base_point[1] + 100)
        points.append((x, y))



# Function to measure distance from one point to other point
def dist(x1, y1, x2, y2):
    return math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))

# Function to compute a single centroid
def compute_single_centroid(cluster):
    x_coords = [point[0] for point in cluster]
    y_coords = [point[1] for point in cluster]
    x_avg = sum(x_coords) / len(x_coords)
    y_avg = sum(y_coords) / len(y_coords)
    return (x_avg, y_avg)


# Function to compute centroid for cluster
def compute_centroids(centroids, clusters):
    for cluster in clusters:
            centroids.append(compute_single_centroid(cluster))

# Function to compute medoid for cluster
def compute_medoids(medoids, clusters):
    for cluster in clusters:
        distances_min = float('inf')
        medoid = None
        for candidate in cluster:
            distances_sum = sum(dist(candidate[0], candidate[1], bod[0], bod[1]) for bod in cluster)
            if distances_sum < distances_min:
                distances_min = distances_sum
                medoid = candidate
        medoids.append(medoid)


# Function for divisive clustering using custom k-means for splitting
def divisive_clustering_kmeans(points, max_clusters, max_iterations=100):
    clusters = [points]  # Start with all points in one cluster
    centroids = [compute_single_centroid(points)]

    while len(clusters) < max_clusters:

        clusters_average_dist = []
        for centroid, cluster in zip(centroids, clusters):
            total_distance = 0
            for bod in cluster:
                total_distance += dist(bod[0], bod[1], centroid[0], centroid[1])
            average_distance = total_distance / len(cluster)
            clusters_average_dist.append(average_distance)
        split_cluster_idx = clusters_average_dist.index(max(clusters_average_dist))
        split_cluster = clusters[split_cluster_idx]


        # If the largest cluster has less than 2 points, we can't split it further
        if len(split_cluster) < 2:
            break

        # Apply custom k-means with k=2 to split the largest cluster
        cluster_number = 2
        new_clusters, new_centroids = clusterization_k_means(split_cluster, "centroid", cluster_number,
                                                             max_iterations)

        # Replace the largest cluster with the two new clusters
        clusters[split_cluster_idx] = new_clusters[0]
        clusters.append(new_clusters[1])

        # Store the centroids of the two new clusters
        centroids[split_cluster_idx] = new_centroids[0]
        centroids.append(new_centroids[1])

    return clusters, centroids


# Function to evaluate created clusters
def evaluation(clusters, centroids):
    i = 0
    sum = 0
    for centroid, cluster in zip(centroids, clusters):
        i += 1
        total_distance = 0
        for bod in cluster:
            total_distance += dist(bod[0], bod[1], centroid[0], centroid[1])
        average_distance = total_distance / len(cluster)
        bods_num = len(cluster)
        sum += bods_num
        if average_distance <= 500:
            print("Cluster " + str(i) + " success!! With average distance " + str(average_distance) + " and with " + str(bods_num) + " bods")
        else:
            print("Cluster " + str(i) + " failure :( With average distance " + str(average_distance) + " and with " + str(bods_num) + " bods")
    print("Total number of points that were processed: " + str(sum))


def clusterization_k_means(points, mode, cluster_number, max_iterations):
    # Initializing first centers as first points in 'points'
    clusters_centers = points[:cluster_number]
    for _ in range (max_iterations):
        clusters = [[] for _ in range(cluster_number)]
        # appending points into clusters based on centroids
        # (in first iteration based on first bods)
        for point in points:
            distances = []
            # Here we are finding the nearest center to some point so we can attach the point to center of its group
            for cluster_center in clusters_centers:
                distances.append(dist(point[0], point[1], cluster_center[0], cluster_center[1]))
            nearest_cluster_center_index = distances.index(min(distances))
            # cluster_centers has the centers of each cluster on same indexes as cluster in clusters array
            clusters[nearest_cluster_center_index].append(point)
        new_centers = []
        if 'medoid' in mode:
           compute_medoids(new_centers, clusters)
        elif 'centroid' in mode:
           compute_centroids(new_centers, clusters)
        if new_centers == clusters_centers:
            break
        clusters_centers = new_centers
    return clusters, clusters_centers


def main():
    max_clusters = 18
    cluster_number = 19
    max_iterations = 50
    points = []
    first_points(points)
    input_points = 40000
    print("What algorithm you want to use? \n"
          "put 'M' for K-means with medoid \n"
          "put 'C' for K-means with centroid\n"
          "put 'D' for Divisive clustering \n"
          "If you want to use all three then put MCD")
    m = sys.stdin.readline().strip()
    create_points(input_points, points)
    if m == 'M':
        clusters, centers = clusterization_k_means(points, "medoid", cluster_number, max_iterations)
    elif m == 'C':
        clusters, centers = clusterization_k_means(points, "centroid", cluster_number, max_iterations)
    elif m == 'D':
        clusters, centers = divisive_clustering_kmeans(points, max_clusters)
    elif m == "MCD":
        clusters, centers = clusterization_k_means(points, "medoid", cluster_number, max_iterations)
        save_clusters_to_json(clusters, centers, filename="clusters_data.json")
        subprocess.Popen(["python3", "Visual_module.py", "clusters_data.json"])
        evaluation(clusters, centers)

        clusters, centers = clusterization_k_means(points, "centroid", cluster_number, max_iterations)
        save_clusters_to_json(clusters, centers, filename="clusters_data.json")
        subprocess.Popen(["python3", "Visual_module.py", "clusters_data.json"])
        evaluation(clusters, centers)

        clusters, centers = divisive_clustering_kmeans(points, max_clusters)
        save_clusters_to_json(clusters, centers, filename="clusters_data.json")
        subprocess.Popen(["python3", "Visual_module.py", "clusters_data.json"])
        evaluation(clusters, centers)
    else:
        print("Input error")
        exit(1)
    save_clusters_to_json(clusters, centers, filename="clusters_data.json")
    subprocess.Popen(["python3", "Visual_module.py", "clusters_data.json"])
    evaluation(clusters, centers)

if __name__ == "__main__":
    main()
