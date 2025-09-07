import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import ray
import cylinder

def main(theta_source, phi_source):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    r = ray.Ray()
    
    # Start condition of ray
    theta_source = math.radians(theta_source)
    phi_source = math.radians(phi_source)
    
    print(theta_source, phi_source)
    
    r.x = 50. * math.sin(theta_source) * math.cos(phi_source)
    r.y = 50. * math.sin(theta_source) * math.sin(phi_source)
    r.z = 50. * math.cos(theta_source)
    
    norm = math.sqrt(r.x**2 + r.y**2 + r.z**2)
    
    r.dx = -r.x / norm
    r.dy = -r.y / norm
    r.dz = -r.z / norm
    
    r.print()
    
    c = cylinder.Cylinder()
    
    d = c.intersection(r)
    
    print(d)
    
    r.x = r.x + r.dx * d
    r.y = r.y + r.dy * d
    r.z = r.z + r.dz * d
    
    n = c.get_normal(r)
    
    print(n)
    
    prod = r.dx * n[0] + r.dy * n[1] + r.dz * n[2]
    
    r.dx = r.dx - 2 * prod * n[0]
    r.dy = r.dy - 2 * prod * n[1]
    r.dz = r.dz - 2 * prod * n[2]
    
    r.print()
    
    xc, yc, zc = c.draw()
    ax.plot_surface(xc, yc, zc, alpha=0.5)
    
    plt.show()

if __name__ == "__main__":
    theta_source = 90.
    phi_source = 45.

    main(theta_source, phi_source)
