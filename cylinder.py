import math

class Cylinder():
    def __init__(self):
        self.r = 5 # Radius in mm
    
    def intersection(self, ray):
        A = ray.dx*ray.dx + ray.dy*ray.dy;
        B = 2 * (ray.x*ray.dx + ray.y*ray.dy);
        C = ray.x*ray.x + ray.y*ray.y - self.r*self.r;

        discriminant = B*B - 4*A*C;
        if (discriminant < 0):
            return -1; # No intersection

        sqrtd = math.sqrt(discriminant);
        t1 = (-B - sqrtd) / (2*A);
        t2 = (-B + sqrtd) / (2*A);

        # Choose smallest positive t
        if (t1 > 0):
            return t1;
        if (t2 > 0):
            return t2;
        
        return -1;
