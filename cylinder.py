import math
import numpy as np

class Cylinder():
    def __init__(self, r=10, height_z=100, center=(0.0, 0.0, 0.0)):
        self.r = float(r)               # radius (mm)
        self.height_z = float(height_z) # half-height (mm): z ∈ [-height_z, +height_z]
        self.cx, self.cy, self.cz = map(float, center)
        self._eps = 1e-9

    def set_center(self, center):
        self.cx, self.cy, self.cz = map(float, center)

    def _to_local(self, x, y, z):
        return x - self.cx, y - self.cy, z - self.cz

    def intersection(self, ray):
        # Transform ray origin to cylinder-local space (direction unchanged by translation)
        rx, ry, rz = self._to_local(ray.x, ray.y, ray.z)
        rdx, rdy, rdz = ray.dx, ray.dy, ray.dz

        candidates = []

        # 1) Side: x^2 + y^2 = r^2
        A = rdx*rdx + rdy*rdy
        B = 2.0 * (rx*rdx + ry*rdy)
        C = rx*rx + ry*ry - self.r*self.r

        if abs(A) > self._eps:
            disc = B*B - 4.0*A*C
            if disc >= 0.0:
                sqrtd = math.sqrt(disc)
                t1 = (-B - sqrtd) / (2.0*A)
                t2 = (-B + sqrtd) / (2.0*A)
                for t in (t1, t2):
                    if t > self._eps:
                        z_hit_local = rz + t*rdz
                        if -self.height_z - self._eps <= z_hit_local <= self.height_z + self._eps:
                            candidates.append(t)

        # 2) Caps: planes z_local = ±height_z
        if abs(rdz) > self._eps:
            for z_plane in (-self.height_z, self.height_z):
                t = (z_plane - rz) / rdz
                if t > self._eps:
                    xh = rx + t*rdx
                    yh = ry + t*rdy
                    if xh*xh + yh*yh <= self.r*self.r + 1e-9:
                        candidates.append(t)

        return min(candidates) if candidates else -1

    def get_normal(self, ray):
        xw = ray.x
        yw = ray.y
        zw = ray.z
        
        # Convert to local for classification
        x, y, z = self._to_local(xw, yw, zw)

        # Cap normals
        if abs(z - self.height_z) <= 1e-6:
            return [0.0, 0.0, 1.0]
        if abs(z + self.height_z) <= 1e-6:
            return [0.0, 0.0, -1.0]

        # Side normal (radial in x-y)
        denom = math.sqrt(x*x + y*y)
        if denom < 1e-12:
            # Degenerate on axis – pick a stable normal
            return [0.0, 0.0, 1.0]
        return [x/denom, y/denom, 0.0]

    def draw(self, n=50):
        """
        Returns meshgrids (x,y,z) for the side surface, translated to the cylinder center.
        """
        z_local = np.linspace(-self.height_z, self.height_z, n)
        theta = np.linspace(0, 2*np.pi, n)
        theta_grid, z_grid = np.meshgrid(theta, z_local)
        x_grid = self.r * np.cos(theta_grid) + self.cx
        y_grid = self.r * np.sin(theta_grid) + self.cy
        z_grid = z_grid + self.cz
        return x_grid, y_grid, z_grid

    # (Optional) convenience to get cap circle outlines for visualization
    def draw_caps(self, n=100):
        theta = np.linspace(0, 2*np.pi, n)
        x = self.r * np.cos(theta) + self.cx
        y = self.r * np.sin(theta) + self.cy
        z_top = np.full_like(theta, self.cz + self.height_z)
        z_bot = np.full_like(theta, self.cz - self.height_z)
        return (x, y, z_top), (x, y, z_bot)
