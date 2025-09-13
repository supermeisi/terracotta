import math
import numpy as np

class Cylinder():
    def __init__(self):
        self.r = 10 # Radius in mm
        self.height_z = 1 # Height in mm
        self._eps = 1e-9 # Precision in mm
    
    def intersection(self, ray):
        
        candidates = []

        # Intersection with curved sides
        A = ray.dx*ray.dx + ray.dy*ray.dy
        B = 2.0 * (ray.x*ray.dx + ray.y*ray.dy)
        C = ray.x*ray.x + ray.y*ray.y - self.r*self.r

        if abs(A) > self._eps:
            disc = B*B - 4.0*A*C
            if disc >= 0.0:
                sqrtd = math.sqrt(disc)
                t1 = (-B - sqrtd) / (2.0*A)
                t2 = (-B + sqrtd) / (2.0*A)

                # check both ts for positivity and z-range
                for t in (t1, t2):
                    if t > self._eps:
                        z_hit = ray.z + t*ray.dz
                        if -self.height_z - self._eps <= z_hit <= self.height_z + self._eps:
                            candidates.append(t)

        # Intersection with caps
        if abs(ray.dz) > self._eps:
            for z_plane in (-self.height_z, self.height_z):
                t = (z_plane - ray.z) / ray.dz
                if t > self._eps:
                    x_hit = ray.x + t*ray.dx
                    y_hit = ray.y + t*ray.dy
                    if x_hit*x_hit + y_hit*y_hit <= self.r*self.r + 1e-9:
                        candidates.append(t)

        if not candidates:
            return -1

        return min(candidates)
    
    def get_normal(self, ray):
        x = ray.x
        y = ray.y
        z = ray.z

        # If on a cap, normal is ±z
        if abs(z - self.height_z) <= 1e-6:
            return [0.0, 0.0, 1.0]
        if abs(z + self.height_z) <= 1e-6:
            return [0.0, 0.0, -1.0]

        # Otherwise side: radial normal in x-y
        denom = math.sqrt(x*x + y*y)
        if denom < 1e-12:
            # Degenerate case at the axis to avoid NaN
            return [0.0, 0.0, 1.0]
        return [x/denom, y/denom, 0.0]

    def draw(self):
        z = np.linspace(-self.height_z, self.height_z, 50)
        
        theta = np.linspace(0, 2*np.pi, 50)
        theta_grid, z_grid = np.meshgrid(theta, z)
        
        x_grid = self.r * np.cos(theta_grid)
        y_grid = self.r * np.sin(theta_grid)
        
        return x_grid, y_grid, z_grid
        
