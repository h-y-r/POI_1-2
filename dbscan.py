import numpy as np
import csv
import math
from sklearn.cluster import DBSCAN
from pyransac3d import Plane

def distance(plane, point):
    return abs(plane[0] * point[0] + plane[1] * point[1] + plane[2] * point[2] + plane[3]) / np.sqrt(
        plane[0] ** 2 + plane[1] ** 2 + plane[2] ** 2)


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


points = []
with open("all_points.xyz", 'r') as xyz:
    csv_points = csv.reader(xyz, delimiter=' ')
    for row in csv_points:
        x, y, z = map(float, row)
        points.append([x, y, z])
points = np.array(points)

print("\nZadanie 6 (DBSCAN + pyransac3d):\n")
dbscan = DBSCAN(eps=0.5, min_samples=10).fit(points)
labels = dbscan.labels_
n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

for i in range(n_clusters):
    cluster = points[labels == i]
    if len(cluster) < 3:
        continue

    plane_model = Plane()
    plane, inliers = plane_model.fit(cluster, thresh=1e-5, maxIteration=1000)

    if plane is not None:

        print(f"Klaster {i + 1}: {len(cluster)} punktów.")
        print(f"Płaszczyzna: {plane[0]:.4f}x + {plane[1]:.4f}y + {plane[2]:.4f}z + {plane[3]:.4f} = 0")
        print(f"Inliers: {len(inliers)}")

        if is_plane(cluster, plane):
            print(f"Jest płaszczyzną {plane_orientation(plane[:3])}")
        else:
            print("Nie jest płaszczyzną")
    else:
        print(f"Klaster {i + 1}: Nie udało się dopasować płaszczyzny")

    print()
