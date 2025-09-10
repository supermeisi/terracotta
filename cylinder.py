import math
import numpy as np

class Cylinder():
    def __init__(self):
        self.r = 10 # Radius in mm
        self.height_z = 100 # Height in mm
    
    def intersection(self, ray):
        A = ray.dx*ray.dx + ray.dy*ray.dy
        B = 2 * (ray.x*ray.dx + ray.y*ray.dy)
        C = ray.x*ray.x + ray.y*ray.y - self.r*self.r

        discriminant = B*B - 4*A*C
        
        if (discriminant < 0):
            return -1 # No intersection

        sqrtd = math.sqrt(discriminant)
        t1 = (-B - sqrtd) / (2*A)
        t2 = (-B + sqrtd) / (2*A)

        # Choose smallest positive t
        if (t1 > 0):
            return t1
        if (t2 > 0):
            return t2
        
        return -1
    
    def get_normal(self, ray):
        return [ray.x / math.sqrt(ray.x**2 + ray.y**2), ray.y / math.sqrt(ray.x**2 + ray.y**2), 0]
    
    def draw(self):
        z = np.linspace(-self.height_z, self.height_z, 50)
        
        theta = np.linspace(0, 2*np.pi, 50)
        theta_grid, z_grid = np.meshgrid(theta, z)
        
        x_grid = self.r * np.cos(theta_grid)
        y_grid = self.r * np.sin(theta_grid)
        
        return x_grid, y_grid, z_grid
        
