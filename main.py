import math

import ray
import cylinder

def main():
    r = ray.Ray()
    
    # Start condition of ray
    r.y = -50
    r.dy = 1
    
    c = cylinder.Cylinder()
    
    intersect = c.intersection(r)

if __name__ == "__main__":
    main()
