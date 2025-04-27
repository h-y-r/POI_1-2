import numpy as np
import random
import csv
import math

def fitplane(points):
    p0, p1, p2 = [np.array(p) for p in points]
    v1 = p1 - p0
    v2 = p2 - p0

    normal = np.cross(v1, v2)
    normal = normal / np.linalg.norm(normal)

    a, b, c = normal
    d = -np.dot(normal, points[1])

    return [a,b,c,d]

def distance(plane, point):
    return abs(plane[0]*point[0] + plane[1]*point[1] + plane[2]*point[2] + plane[3])/np.sqrt(plane[0]**2 + plane[1]**2 + plane[2]**2)

def ransac(points, max_iterations, threshold):
    best_plane = []
    best_inliers = []
    for i in range(max_iterations):
        sample = random.sample(points, 3)
        plane = fitplane(sample)
        inliers = []
        for x in points:
            if distance(plane, x) < threshold:
                inliers.append(x)

        if len(inliers) > len(best_inliers):
            best_inliers = inliers
            best_plane = plane

    return best_inliers, best_plane


def assign_clusters(points, centroids):
    clusters = [[] for _ in range(len(centroids))]

    for point in points:
        distances = [np.linalg.norm(np.array(point) - np.array(centroid)) for centroid in centroids]
        closest = np.argmin(distances)
        clusters[closest].append(point)

    return clusters


def update_centroids(clusters):
    new_centroids = []
    for cluster in clusters:
        if cluster:
            new_centroid = np.mean(cluster, axis=0)
            new_centroids.append(new_centroid)
        else:
            new_centroids.append(random.choice(sum(clusters, [])))

    return new_centroids


def kmeans(points, k, max_iterations=1000):
    centroids = random.sample(points, k)

    for _ in range(max_iterations):
        clusters = assign_clusters(points, centroids)
        new_centroids = update_centroids(clusters)

        if np.allclose(np.array(centroids), np.array(new_centroids)):
            break

        centroids = new_centroids

    return clusters


def is_plane(points, plane, threshold=1e-2):
    distances = [distance(plane, point) for point in points]
    avg = np.mean(distances)
    return avg < threshold


def plane_orientation(plane_normal):
    normal = plane_normal / np.linalg.norm(plane_normal)

    angle_with_z = math.degrees(math.acos(abs(normal[2])))

    if angle_with_z < 15:
        return "poziomą"
    elif angle_with_z > 75:
        return "pionową"
    else:
        return "ukośną"



def save_to_xyz_file(points_list, filename):
    with open(filename, 'w') as f:
        for points in points_list:
            f.write(f"{points[0]} {points[1]} {points[2]}\n")

points = []
with open("all_points.xyz", 'r') as xyz:
    csv_points = csv.reader(xyz, delimiter = ' ')
    for row in csv_points:
        x, y, z = map(float, row)
        points.append([x, y, z])

clusters = kmeans(points, k=3)
print("Zadania 1-4 (własna implementacja):\n")
i=1
for cluster in clusters:
    inliers, plane = ransac(cluster, 1000, 1e-5)
    print(f"Klaster {i}: {len(cluster)} punktów.\nPłaszczyzna: {plane[0]}x + {plane[1]}y + {plane[2]}z + {plane[3]} = 0; {len(inliers)} inlierów")
    if(is_plane(cluster,plane)):
        print(f"Jest płaszczyzną {plane_orientation(plane[:3])}")
    else:
        print("Nie jest płaszczyzną")
    save_to_xyz_file(cluster, f"cluster{i}.xyz")
    i=i+1