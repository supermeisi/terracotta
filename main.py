import math
import numpy as np

import ray
import cylinder

def main(theta_source, phi_source):
    r = ray.Ray()
    
    # Start condition of ray
    theta_source = math.radians(theta_source)
    phi_source = math.radians(phi_source)
    
    print(theta_source, phi_source)
    
    r.x = 50. * math.sin(theta_source) * math.cos(phi_source)
    r.y = 50. * math.sin(theta_source) * math.sin(phi_source)
    r.z = 50. * math.cos(theta_source)
    
    norm = math.sqrt(r.x*r.x + r.y*r.y + r.z*r.z)
    
    r.dx = -r.x / norm
    r.dy = -r.y / norm
    r.dz = -r.z / norm
    
    r.print()
    
    c = cylinder.Cylinder()
    
    intersect = c.intersection(r)
    
    print(intersect)

if __name__ == "__main__":
    theta_source = 90.
    phi_source = 45.

    main(theta_source, phi_source)
