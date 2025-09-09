import random

import ray

class Source:
    def __init__(self):
        self.x = 0.
        self.y = 0.
        self.z = 0.

        self.w = 0 # Source width
        
        self.rays = []

    def generate(self, n):
        for i in range(n):
            r = ray.Ray()
            r.x = self.w * random.random()
            r.z = self.w * random.random()
            self.rays.append(r)