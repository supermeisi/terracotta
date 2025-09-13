import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import ray
import source
import cylinder

def main(theta_source, phi_source):
    # Display parameters
    n_rays = 100000
    n_rays_disp = 100
    update = 1000
    
    # Start condition of ray
    theta_source = math.radians(theta_source)
    phi_source = math.radians(phi_source)

    #print(theta_source, phi_source)

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

    s.generate(n_rays)

    c1 = cylinder.Cylinder(r=10., height_z=10, center=(0., 0., 10.5)) # Add cylinder to scene
    c2 = cylinder.Cylinder(r=10., height_z=10, center=(0., 0., -10.5)) # Add cylinder to scene

    # Include all cylinders
    cs = [c1, c2]

    hits_y = []
    hits_z = []

    rays = []

    # Main loop over all rays
    for i in range(len(s.rays)):
        if i % update == 0:
            plt.hist2d(hits_y, hits_z, bins=100, cmap ="gray", range=([[-10., 10.], [-10., 10.]]))
            plt.colorbar()
            plt.savefig('hist.png', dpi=300)
            plt.close()

        r = s.rays[i]

        xs = []
        ys = []
        zs = []

        xs.append(r.x)
        ys.append(r.y)
        zs.append(r.z)

        while True:
            is_neg = True
            dlst = []

            for id, c in enumerate(cs):
                d = c.intersection(r)
                dlst.append(d)
                if d > 0:
                    is_neg = False

            #print(idc, dmin)

            if is_neg:
                break

            id = dlst.index(min(filter(lambda x : x > 0, dlst)))
            dmin = dlst[id]

            r.x = r.x + r.dx * dmin
            r.y = r.y + r.dy * dmin
            r.z = r.z + r.dz * dmin
            
            n = cs[id].get_normal(r)
            
            #print(n)
            
            prod = r.dx * n[0] + r.dy * n[1] + r.dz * n[2]
            
            r.dx = r.dx - 2 * prod * n[0]
            r.dy = r.dy - 2 * prod * n[1]
            r.dz = r.dz - 2 * prod * n[2]

            xs.append(r.x)
            ys.append(r.y)
            zs.append(r.z)

        # Interaction with lens

        d = (25 - r.x) / r.dx

        if d < 0:
            continue

        r.x = r.x + d * r.dx
        r.y = r.y + d * r.dy
        r.z = r.z + d * r.dz

        xs.append(r.x)
        ys.append(r.y)
        zs.append(r.z)

        #print(r.dx, r.dy, r.dz)

        r.dx = r.dx
        r.dy = r.dy - 1./12.5 * r.y
        r.dz = r.dz - 1./12.5 * r.z

        #print(r.dx, r.dy, r.dz)

        # Interaction with detector

        d = (50 - r.x) / r.dx

        if d < 0:
            continue

        r.x = r.x + d * r.dx
        r.y = r.y + d * r.dy
        r.z = r.z + d * r.dz

        #r.print()

        if r.y < -50 or r.y > 50 or r.z  < -50 or r.z > 50:
            continue

        xs.append(r.x)
        ys.append(r.y)
        zs.append(r.z)

        hits_z.append(r.z)
        hits_y.append(r.y)

        rays.append([xs, ys, zs])

        

    # Drawing 3D scene
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlim(-50., 50.)
    ax.set_ylim(-50., 50.)
    ax.set_zlim(-50., 50.)

    n = len(rays)

    frac = int(n/n_rays_disp)

    #print(n_rays_disp, n, frac)

    for c in cs:
        xc, yc, zc = c.draw()
        ax.plot_surface(xc, yc, zc, alpha=0.5)

    for id, ray in enumerate(rays):
        if frac != 0 and id % frac == 0:
            ax.plot(ray[0], ray[1], ray[2])

    #plt.show()
    plt.savefig('view.png', dpi=300)

    plt.close()

    #print(hits_y, hits_z)

if __name__ == "__main__":
    theta_source = 90.
    phi_source = 45.

    main(theta_source, phi_source)