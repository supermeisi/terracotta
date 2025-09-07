import math

import ray
import cylinder

def main():
    r = ray.Ray()
    c = cylinder.Cylinder()
    
    intersect = c.intersection(r)

if __name__ == "__main__":
    main()
