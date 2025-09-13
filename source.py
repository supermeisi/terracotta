import numpy as np
import random

import ray

class Source:
    def __init__(self):
        # Source position
        self.x = 0.
        self.y = 0.
        self.z = 0.

        # Source normal vector
        self.nx = 0.
        self.ny = 0.
        self.nz = -1.

        self.w = 0 # Source width
        
        self.rays = []

    def plane(self):
        n = np.array([self.nx, self.ny, self.nz])
        norm_n = np.linalg.norm(n)
        if norm_n == 0:
            raise ValueError("Normal vector must be non-zero.")
        n_hat = n / norm_n

        # Pick a vector least aligned with n_hat for numerical stability
        i = np.argmin(np.abs(n_hat))
        a = np.zeros(3)
        a[i] = 1.0

        u = np.cross(a, n_hat)
        u /= np.linalg.norm(u)
        v = np.cross(n_hat, u)
        
        return u, v, n_hat

    def generate(self, n):
        # Create ray plane
        u, v, n_hat = self.plane()

        self.nx = n_hat[0]
        self.ny = n_hat[1]
        self.nz = n_hat[2]

        for i in range(n):
            r = ray.Ray()

            theta = 2 * np.pi * random.random()
            R = np.sqrt(random.random()) * self.w
            a = R * np.cos(theta)
            b = R * np.sin(theta)

            r.x = self.x + a * u[0] + b * v[0]
            r.y = self.y + a * u[1] + b * v[1]
            r.z = self.z + a * u[2] + b * v[2]

            r.dx = self.nx
            r.dy = self.ny
            r.dz = self.nz

            #r.print()

            self.rays.append(r)