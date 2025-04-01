import numpy as np

def generate_flat_horizontal_surface(width, length, num_points):

    x = np.random.uniform(-width / 2, width / 2, num_points)
    y = np.random.uniform(-length / 2, length / 2, num_points)
    z = np.zeros(num_points)
    return np.column_stack((x, y, z))

def generate_flat_vertical_surface(width, height, num_points):

    x = np.random.uniform(-width / 2, width / 2, num_points)
    z = np.random.uniform(0, height, num_points)
    y = np.zeros(num_points)
    return np.column_stack((x, y, z))

def generate_cylindrical_surface(radius, height, num_points):

    theta = np.random.uniform(0, 2 * np.pi, num_points)
    z = np.random.uniform(0, height, num_points)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    return np.column_stack((x, y, z))

def save_to_xyz_file(points, filename):

    with open(filename, 'w') as f:
        for point in points:
            f.write(f"{point[0]} {point[1]} {point[2]}\n")


num_points = 10000

horizontal_surface = generate_flat_horizontal_surface(10, 5, num_points)
save_to_xyz_file(horizontal_surface, "horizontal_surface.xyz")

vertical_surface = generate_flat_vertical_surface(8, 6, num_points)
save_to_xyz_file(vertical_surface, "vertical_surface.xyz")

cylindrical_surface = generate_cylindrical_surface(4, 7, num_points)
save_to_xyz_file(cylindrical_surface, "cylindrical_surface.xyz")
