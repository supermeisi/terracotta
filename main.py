import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import ray
import source
import cylinder

def main(theta_source, phi_source):
    # Drawing 3D scene
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Start condition of ray
    theta_source = math.radians(theta_source)
    phi_source = math.radians(phi_source)

    print(theta_source, phi_source)

    rot_z = np.array([
        [math.cos(phi_source), -math.sin(phi_source), 0],
        [math.sin(phi_source),  math.cos(phi_source), 0],
        [0,                     0,                    1]
        ])

    rot_x = np.array([
        [1, 0,                       0                     ],
        [0, math.cos(theta_source), -math.sin(theta_source)],
        [0, math.sin(theta_source),  math.cos(theta_source)]
        ])

    s = source.Source()

    s.z = 50.
    s.w = 10.

    v = np.array([s.x, s.y, s.z])
    
    print('Rotation Matrix z:')
    print(rot_z)
    print('Rotation Matrix x:')
    print(rot_x)

    v = rot_z.dot(rot_x.dot(v))

    print('Vector:', v)

    s.x = v[0]
    s.y = v[1]
    s.z = v[2]

    v = np.array([s.nx, s.ny, s.nz])
    
    print('Rotation Matrix z:')
    print(rot_z)
    print('Rotation Matrix x:')
    print(rot_x)

    v = rot_z.dot(rot_x.dot(v))

    print('Vector:', v)

    s.nx = v[0]
    s.ny = v[1]
    s.nz = v[2]

    s.generate(100)

    c = cylinder.Cylinder() # Add cylinder to scene

    xc, yc, zc = c.draw()
    ax.plot_surface(xc, yc, zc, alpha=0.5)

    hits_y = []
    hits_z = []

    # Main loop over all rays
    for i in range(len(s.rays)):
        r = s.rays[i]

        old_x = r.x
        old_y = r.y
        old_z = r.z
        
        d = c.intersection(r)
        
        print(d)
        
        r.x = r.x + r.dx * d
        r.y = r.y + r.dy * d
        r.z = r.z + r.dz * d
        
        n = c.get_normal(r)
        
        print(n)
        
        prod = r.dx * n[0] + r.dy * n[1] + r.dz * n[2]
        
        r.dx = r.dx - 2 * prod * n[0]
        r.dy = r.dy - 2 * prod * n[1]
        r.dz = r.dz - 2 * prod * n[2]

        ax.plot([old_x, r.x], [old_y, r.y], [old_z, r.z])

        old_x = r.x
        old_y = r.y
        old_z = r.z

        l = (50 - r.x) / r.dx

        if l < 0:
            continue

        r.x = r.x + l * r.dx
        r.y = r.y + l * r.dy
        r.z = r.z + l * r.dz

        r.print()

        if r.y < -50 or r.y > 50 or r.z  < -50 or r.z > 50:
            continue

        ax.plot([old_x, r.x], [old_y, r.y], [old_z, r.z])

        hits_z.append(r.z)
        hits_y.append(r.y)
       
    ax.set_xlim(-50., 50.)
    ax.set_ylim(-50., 50.)
    ax.set_zlim(-50., 50.)

    #plt.show()
    plt.savefig('view.png', dpi=300)

    plt.close()

    print(hits_y, hits_z)

    plt.hist2d(hits_y, hits_z, bins=100, cmap ="gray")

    plt.savefig('hist.png', dpi=300)

if __name__ == "__main__":
    theta_source = 90.
    phi_source = 0.

    main(theta_source, phi_source)