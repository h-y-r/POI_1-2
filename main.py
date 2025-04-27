import numpy as np

# generowane punkty są oddalone od siebie dla róźnych powierzchni, ponieważ inaczej nie byłem w stanie uzyskać poprawnego podziału za pomocą dbscan i metody k-średnich

def generate_flat_horizontal_surface(width, length, num_points):

    x = np.random.uniform(-width / 2 + 2, width / 2 + 2, num_points)
    y = np.random.uniform(-length / 2 + 3, length / 2+ 3, num_points)
    z = np.zeros(num_points)
    return np.column_stack((x, y, z))

def generate_flat_vertical_surface(width, height, num_points):

    x = np.random.uniform(-width / 2, width / 2, num_points)
    z = np.random.uniform(-height/2 - 3, height/2 - 3, num_points)
    y = np.zeros(num_points)
    return np.column_stack((x, y, z))

def generate_cylindrical_surface(radius, height, num_points):

    theta = np.random.uniform(0, 2 * np.pi, num_points)
    z = np.random.uniform(-height/2 + 5, height/2 + 5, num_points)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    return np.column_stack((x, y, z))

def save_to_xyz_file(points_list, filename):
    with open(filename, 'w') as f:
        for points in points_list:
            for point in points:
                f.write(f"{point[0]} {point[1]} {point[2]}\n")


num_points = 1000

horizontal_surface = generate_flat_horizontal_surface(5, 5, num_points)
vertical_surface = generate_flat_vertical_surface(5, 5, num_points)
cylindrical_surface = generate_cylindrical_surface(2, 5, num_points)

save_to_xyz_file([cylindrical_surface, vertical_surface, horizontal_surface], "all_points.xyz")

