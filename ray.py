class Ray():
    def __init__(self):
        # Ray position
        self.x = 0.
        self.y = 0.
        self.z = 0.
        
        # Ray direction
        self.dx = 0.
        self.dy = 0.
        self.dz = 0.
        
    def print(self):
        print(self.x, self.y, self.z)
        print(self.dx, self.dy, self.dz);
