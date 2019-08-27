from polyhedron import polyflag
from vector import vector
from math import sqrt

# helper funcs.
midName = lambda v1, v2: f'{v1}_{v2}' if v1 < v2 else f'{v2}_{v1}'
midpoint = lambda vec1, vec2: ((vector(vec1) + vector(vec2)).mult(0.5)).list()
unit = lambda vec: vec.mult(1. / sqrt(vec.mag2())).list()
tween = lambda vec1, vec2, t: [((1 - t) * vec1[0]) + (t * vec2[0]),
                               ((1 - t) * vec1[1]) + (t * vec2[1]),
                               ((1 - t) * vec1[2]) + (t * vec2[2])]
oneThird = lambda vec1, vec2: tween(vec1, vec2, 1 / 3.0)


class transform():

    # Kis(N)
    # ------------------------------------------------------------------------------------------
    # Kis (abbreviated from triakis) transforms an N-sided face into an N-pyramid rooted at the
    # same base vertices.
    # only kis n-sided faces, but n==0 means kis all.
    @staticmethod
    def kisN(poly, n=0, apexdist=0.1):
        flag = polyflag()
        for i, v in enumerate(poly.vertices):  # each old vertex is a new vertex
            flag.newV(f'v{i}', v)
        normals = [vector(n) for n in poly.normals]
        centers = [vector(c) for c in poly.centers()]
        foundAny = False

        for i in range(len(poly.faces)):
            f = poly.faces[i]
            v1 = f'v{f[len(f) - 1]}'
            for v in f:
                v2 = f'v{v}'
                if len(f) == n or n == 0:
                    foundAny = True
                    apex = f'apex{i}'
                    fname = f'{i}{v1}'
                    # new vertices in centers of n-sided face
                    flag.newV(apex, (centers[i] + normals[i].mult(apexdist)).list())
                    flag.newFlag(fname, v1, v2)  # the old edge of original face
                    flag.newFlag(fname, v2, apex)  # up to apex of pyramid
                    flag.newFlag(fname, apex, v1)  # and back down again
                else:
                    flag.newFlag(f'{i}', v1, v2)  # same old flag, if non-n

                # current becomes previous
                v1 = v2

        if not foundAny:
            pass
            # print(f'No {n} - fold components were found.')

        newpoly = flag.topoly()
        newpoly.name = f'k{"" if n is 0 else n}{poly.name}'
        return newpoly

    #  Ambo
    #  ------------------------------------------------------------------------------------------
    #  The best way to think of the ambo operator is as a topological "tween" between a polyhedron
    #  and its dual polyhedron.  Thus the ambo of a dual polyhedron is the same as the ambo of the
    #  original. Also called "Rectify".
    #
    @staticmethod
    def ambo(poly):
        flag = polyflag()
        for i, f in enumerate(poly.faces):
            v1, v2 = f[-2:]
            for v3 in f:
                if v1 < v2:  # vertices are the midpoints of all edges of original poly
                    flag.newV(midName(v1, v2), midpoint(poly.vertices[v1], poly.vertices[v2]))
                # two new flags: One whose face corresponds to the original f:
                flag.newFlag(f'orig{i}', midName(v1, v2), midName(v2, v3))
                # Another flag whose face  corresponds to (the truncated) v2:
                flag.newFlag(f'dual{v2}', midName(v2, v3), midName(v1, v2))
                # shift over one
                v1, v2 = v2, v3

        newpoly = flag.topoly()
        newpoly.name = f'a{poly.name}'
        return newpoly

    # Gyro
    # ----------------------------------------------------------------------------------------------
    # This is the dual operator to "snub", i.e dual*Gyro = Snub.  It is a bit easier to implement
    # this way.
    # 
    # Snub creates at each vertex a new face, expands and twists it, and adds two new triangles to
    # replace each edge.
    @staticmethod
    def gyro(poly):
        flag = polyflag()
        for i, v in enumerate(poly.vertices):  # each old vertex is a new vertex
            flag.newV(f'v{i}', unit(vector(v)))

        for i, f in enumerate(poly.faces):
            flag.newV(f'center{i}', unit(vector(poly.centersArray[i])))
        for i, f in enumerate(poly.faces):
            v1, v2 = f[-2:]
            for j, v in enumerate(f):
                v3 = v
                flag.newV(f'{v1}~{v2}', oneThird(poly.vertices[v1], poly.vertices[v2]))  # new v in face
                fname = f'{i}f{v1}'
                flag.newFlag(fname, f'center{i}', f'{v1}~{v2}')  # five new flags
                flag.newFlag(fname, f'{v1}~{v2}', f'{v2}~{v1}')
                flag.newFlag(fname, f'{v2}~{v1}', f'v{v2}')
                flag.newFlag(fname, f'v{v2}', f'{v2}~{v3}')
                flag.newFlag(fname, f'{v2}~{v3}', f'center{i}')
                v1, v2 = v2, v3

        newpoly = flag.topoly()
        newpoly.name = f'g{poly.name}'
        return newpoly

    #  Propellor
    # ------------------------------------------------------------------------------------------
    # builds a new 'skew face' by making new points along edges, 1/3rd the distance from v1->v2,
    # then connecting these into a new inset face.  This breaks rotational symmetry about the
    # faces, whirling them into gyres

    @staticmethod
    def propellor(poly):
        flag = polyflag()

        for i, v in enumerate(poly.vertices): # each old vertex is a new vertex
            flag.newV(f'v{i}', unit(vector(v)))

        for i, f in enumerate(poly.faces):
            v1, v2 = f[-2:]
            for v in f:
                v3 = v
                flag.newV(f'{v1}~{v2}',
                          oneThird(poly.vertices[v1], poly.vertices[v2]))  # new v in face, 1/3rd along edge
                fname = f'{i}f{v2}'
                flag.newFlag(f'v{i}', f'{v1}~{v2}', f'{v2}~{v3}')  # five new flags
                flag.newFlag(fname, f'{v1}~{v2}', f'{v2}~{v1}')
                flag.newFlag(fname, f'{v2}~{v1}', f'v{v2}')
                flag.newFlag(fname, f'v{v2}', f'{v2}~{v3}')
                flag.newFlag(fname, f'{v2}~{v3}', f'{v1}~{v2}')

                v1, v2 = v2, v3

        newpoly = flag.topoly()
        newpoly.name = f'p{poly.name}'
        return newpoly


if __name__ == '__main__':
    from seeds import prism, antiprism, tetrahedron, cube, icosahedron, octahedron, dodecahedron, johnson_poly, cupola, \
        anticupola

    pn = transform.propellor(tetrahedron())
