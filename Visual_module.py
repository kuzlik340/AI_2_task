import matplotlib.pyplot as plt
import sys
import json

def plot_clusters(clusters, centroids):
    plt.figure(figsize=(10, 10), dpi=120)  # Увеличиваем размер и разрешение графика
    colors = plt.get_cmap("tab20", len(clusters))  # палитра для 20 кластеров

    for i, cluster in enumerate(clusters):
        if cluster:
            x_vals, y_vals = zip(*cluster)
            plt.scatter(x_vals, y_vals, color=colors(i), label=f"Cluster {i + 1}", marker='o', s=1)
        else:
            continue

    # Рисуем центроиды
    centroid_x, centroid_y = zip(*centroids)
    plt.scatter(centroid_x, centroid_y, c='black', marker='o', s=10, label="Centroids")  # увеличиваем центроиды

    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("K-means Medoids")
    plt.xlim(-5000, 5000)
    plt.ylim(-5000, 5000)
    plt.grid(True)
    plt.show()

def main():
    # Получаем путь к JSON-файлу из аргументов командной строки
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        data = json.load(f)

    clusters = data["clusters"]
    centroids = data["centers"]

    plot_clusters(clusters, centroids)

if __name__ == "__main__":
    main()
