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
def compute_centroid(centroids_old, centroids, clusters):
    for cluster in clusters:
        # Check if cluster exists
        if cluster:
            centroids.append(compute_single_centroid(cluster))
        else:
            # If cluster does not exist then we just append old centroid
            centroids.append(centroids_old[clusters.index(cluster)])

# Function to compute medoid for cluster
def compute_medoid(medoids_old, medoids, clusters):
    for cluster in clusters:
        distances_min = float('inf')
        medoid = None
        if cluster:
            for candidate in cluster:
                distances_sum = sum(dist(candidate[0], candidate[1], bod[0], bod[1]) for bod in cluster)
                if distances_sum < distances_min:
                    distances_min = distances_sum
                    medoid = candidate
            medoids.append(medoid)
        else:
            medoids.append(medoids_old[clusters.index(cluster)])


# Function to compute single centroid
def compute_single_centroid(cluster):
    x_coords = [point[0] for point in cluster]
    y_coords = [point[1] for point in cluster]
    x_mean = sum(x_coords) / len(x_coords)
    y_mean = sum(y_coords) / len(y_coords)
    return (x_mean, y_mean)

# Function for divisive clustering
def divisive_clustering(points, max_clusters):
    distance_border = 400 #maybe 500????
    clusters = [points]
    centroids = []

    while len(clusters) < max_clusters:
        new_clusters = []
        new_centroids = []

        for cluster in clusters:
            if len(cluster) < 1:
                # Cluster is too small, just one point
                new_clusters.append(cluster)
                centroids.append(compute_single_centroid(cluster))  # Добавляем его центроид
                continue
            # Find the centroid cluster
            centroid = compute_single_centroid(cluster)
            total_distance = sum(dist(point[0], point[1], centroid[0], centroid[1]) for point in cluster)
            average_distance = total_distance / len(cluster)

            # if average_distance <= distance_border:
            #     # Cluster is too dense
            #     new_clusters.append(cluster)
            #     new_centroids.append(centroid)  # Сохраняем центроид кластера
            #     continue

            # Creating two small clusters to split main cluster
            child_cluster1 = []
            child_cluster2 = []

            for point in cluster:
                if dist(point[0], point[1], centroid[0], centroid[1]) < average_distance:
                    child_cluster1.append(point)
                else:
                    child_cluster2.append(point)

            # Appending the clusters if there are some points inside
            if child_cluster1:
                new_clusters.append(child_cluster1)
                new_centroids.append(compute_single_centroid(child_cluster1))  # Сохраняем центроид
            if child_cluster2:
                new_clusters.append(child_cluster2)
                new_centroids.append(compute_single_centroid(child_cluster2))  # Сохраняем центроид

        if len(new_clusters) == len(clusters):
            # If there is a situation when after last iteration there was no changing to the clusters
            break

        clusters = new_clusters
        centroids = new_centroids  # Updating an array of centroids

    return clusters, centroids

# Function to evaluate created clusters
def evaluation(clusters, centroids):
    i = 0
    sum = 0
    for centroid, cluster in zip(centroids, clusters):
        i += 1
        total_distance = 0
        if cluster:
            for bod in cluster:
                total_distance += dist(bod[0], bod[1], centroid[0], centroid[1])
            average_distance = total_distance / len(cluster)
            bods_num = len(cluster)
            sum += bods_num
            if average_distance <= 500:
                print("Cluster " + str(i) + " success!! with average distance " + str(average_distance) + " and with " + str(bods_num) + " bods")
            else:
                print("Cluster " + str(i) + " failure!! with average distance " + str(average_distance) + " and with " + str(bods_num) + " bods")
        else:
            print("Cluster " + str(i) + " does not exist...")
    print(sum)



# todo K means how many clusters?
# todo May we use first 20 points
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
           compute_medoid(clusters_centers, new_centers, clusters)
        elif 'centroid' in mode:
           compute_centroid(clusters_centers, new_centers, clusters)
        if new_centers == clusters_centers:
            break
        clusters_centers = new_centers
    return clusters, clusters_centers

def main():
    max_clusters = 20
    cluster_number = 20
    max_iterations = 50
    points = []
    first_points(points)
    print("How many points do you want?")
    input_points = int(input())
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
        clusters, centers = divisive_clustering(points, max_clusters)
    elif m == "MCD":
        clusters, centers = clusterization_k_means(points, "medoid", cluster_number, max_iterations)
        save_clusters_to_json(clusters, centers, filename="clusters_data.json")
        subprocess.Popen(["python3", "Visual_module.py", "clusters_data.json"])
        evaluation(clusters, centers)

        clusters, centers = clusterization_k_means(points, "centroid", cluster_number, max_iterations)
        save_clusters_to_json(clusters, centers, filename="clusters_data.json")
        subprocess.Popen(["python3", "Visual_module.py", "clusters_data.json"])
        evaluation(clusters, centers)

        clusters, centers = divisive_clustering(points, max_clusters)
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
