import ray

class Source:
    def __init__(self):
        self.x = 0.
        self.y = 0.
        self.z = 0.

        self.n = 1
        
        self.rays = []

    def generate(self, n):
        for i in range(n):
            r = ray.Ray()
            r.z = 50
            self.rays.append(r)