# Task

The primary objective of this task is to implement clustering of points
in a 2D space. Initially, 20 random points are generated, serving as
central points, around which an additional 40,000 points are
created(These 40,000 points will be created also around each other).
Using clustering algorithms, the goal is to organize all points into
clusters, adhering to a single rule: the average distance from points to
the cluster center must be less than 500.

The 2D space has to have dimensions X and Y, ranging from -5000 to
+5000.

# Algorithms

In this task, we implement three clustering algorithms:

1.  K-means clustering with centroids as cluster centers

2.  K-means clustering with medoids as cluster centers

3.  Divisive clustering with centroids as cluster centers

# K-means algorithm description

The K-means algorithm begins by defining K --- the number of clusters
--- and initializing the centroids. Here is a step-by-step breakdown of
the algorithm:

1.  **Initialization**: Start by defining K - number of clusters, and
    initialize the centroids or medoids.

2.  **Assign Points to Clusters**: In this step, each point is assigned
    to the nearest centroid/medoid. In the first iteration, points are
    assigned to the initial centroids/medoids.

3.  **Recompute Centroids**: For each cluster, calculate the new
    centroids/medoids based on the points assigned in the previous step.
    This step redefines the centers of the clusters.

4.  **Update Centroids and Repeat**: Set the newly computed centroids as
    the current centroids and return to step two. The process repeats
    until the centroids/medoids no longer change.

## K-means with centroids

A centroid is a point that is equidistant from all points in a cluster.
That means that in code centroid will be represented as two float
variables. Here is the graphic for the K-means algorithm with centroids
based on the elbow method. We can see here that the optimal number is 17
but after many tests, the best number was found and it is 18 clusters.
If the number of clusters equals 18 then the chance of creating a
cluster with average distances larger than 500 is near 0. The first
centroids are initialized as the first points in the points array.

Here is the picture that contains all 40020 points and the result of
K-means with centroids clusterization.

<figure>
<img width="736" alt="centroel" src="https://github.com/user-attachments/assets/4625e6d8-c14d-448b-a5bf-2509d1db284c">
<img width="539" alt="Screenshot 2024-11-04 at 02 21 21" src="https://github.com/user-attachments/assets/01ab5641-773a-4f13-bbe5-5c0ee9bfe0e6">

</figure>

## K-means with medoids

K-means with medoids functions similarly to K-means with centroids, but
with a key difference: each cluster's center is an actual point within
the cluster. While a centroid can be any point in 2D space representing
the center, a medoid is an existing point within the cluster that is
approximately equidistant from all other points. Based on testing, 18
was selected as the optimal number of clusters.

<figure>
<img width="721" alt="medoel" src="https://github.com/user-attachments/assets/82306745-7a7c-442e-916f-c9a24bbdd044">
<img width="852" alt="Screenshot 2024-11-02 at 20 21 21" src="https://github.com/user-attachments/assets/d2f92616-c8a3-447b-9131-0f2eb3fa9441">
</figure>

# Divisive clustering

Divisive clustering is a hierarchical algorithm that is used for
clusterization. Step-by-step analysis of the divisive algorithm:

1.  At this step we initialize the clusters array with just one cluster
    with all points.

2.  Here we have to choose a cluster that will be split in two. It
    depends on the task, in this code, there will be chosen the cluster
    with the largest average distance from all points to centroid.

3.  Creation of two smaller clusters is done by calling the K-means with
    centroids for 2 clusters.

4.  K-means will return two new clusters and we are appending them to
    the clusters in divisive clustering algorithm. Then we go to the
    second step until the desired cluster number is reached.

## Optimizations for divisive algorithm

The first optimization focuses on selecting the cluster to split. In
this approach, we choose the cluster with the largest average distance
between all its points and the centroid. Since we have to evaluate our
clusters based on the average distance from points to the center the
cluster with the biggest distance will be chosen, for other tasks the
cluster that will be chosen could be the largest one or with the
smallest density.
```cython
for centroid, cluster in zip(centroids, clusters):
    total_distance = 0
    for point in cluster:
        total_distance += dist(point[0], point[1], centroid[0], centroid[1])
    average_distance = total_distance / len(cluster)
    clusters_average_dist.append(average_distance)
split_cluster_idx = clusters_average_dist.index(max(clusters_average_dist))
split_cluster = clusters[split_cluster_idx]
```

Also, divisive algorithm in this code is done by calling the K-means
algorithm for splitting the cluster. It means that when we choose the
best cluster to split code will call the K-means algorithm to make 2
clusters out of one.
```cython
new_clusters, new_centroids = clusterization_k_means(split_cluster, "centroid", 2)
```

# Start the code

Please put both codes AI_project.py and Visual_module.py in one folder
and start the code by this command:

    pypy AI_project.py

# Final overview

The clustering maps demonstrate that each algorithm---K-means with
medoids, K-means with centroids, and divisive clustering with centroids
effectively organizes the generated points into clusters. The
implementation seems solid, as each clustering method produces clear and
tightly grouped clusters that meet the set criteria. In particular, the
average distance from all points to their cluster centers is below 500,
showing that the clustering results fit the task requirements well.

The execution time for running all three algorithms sequentially is
under 30 seconds on my laptop, which is a good result for clustering
40,000 points. Overall, this implementation is efficient and performs
well in terms of both speed and accuracy.

The fastest clustering method is divisive clustering with centroids,
while the slowest is K-means with medoids, as it requires checking all
points in each cluster during every iteration. Comparing the quality of
the clustering methods isn't necessary here, as each method as a result
has organized clusters in a very similar way.

<img width="1440" alt="ALL" src="https://github.com/user-attachments/assets/5fabc92c-3c80-425f-acfe-7524d72205d1">


