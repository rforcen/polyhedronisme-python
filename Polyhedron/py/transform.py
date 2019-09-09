from py.polyhedron import polyflag, polyhedron
from geo import *


class transform():

    # Kis(N)
    # ------------------------------------------------------------------------------------------
    # Kis (abbreviated from triakis) transforms an N-sided face into an N-pyramid rooted at the
    # same base vertices.
    # only kis n-sided faces, but n==0 means kis all.
    @staticmethod
    def kisN(poly: polyhedron, n: int = 0, apexdist=0.1) -> polyhedron:
        flag = polyflag()
        for i, v in enumerate(poly.vertices):  # each old vertex is a new vertex
            flag.newV(f'v{i}', v)
        normals = poly.normals
        centers = poly.calc_centers()
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
                    flag.newV(apex, add(centers[i], mult(apexdist, normals[i])))
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
    def ambo(poly: polyhedron) -> polyhedron:
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
    def gyro(poly: polyhedron) -> polyhedron:
        flag = polyflag()
        for i, v in enumerate(poly.vertices):  # each old vertex is a new vertex
            flag.newV(f'v{i}', unit(v))

        for i, f in enumerate(poly.faces):
            flag.newV(f'center{i}', unit(poly.centersArray[i]))
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
    def propellor(poly: polyhedron) -> polyhedron:
        flag = polyflag()

        for i, v in enumerate(poly.vertices):  # each old vertex is a new vertex
            flag.newV(f'v{i}', unit(v))

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

    #     Reflection
    # ------------------------------------------------------------------------------------------
    # geometric reflection through origin
    @staticmethod
    def reflect(poly: polyhedron) -> polyhedron:
        for i, v in enumerate(poly.vertices):
            poly.vertices[i] = mult(-1, v)
        for i, _ in enumerate(poly.faces):
            poly.faces[i].reverse()
        poly.name = f'r{poly.name}'
        poly.refresh()
        return poly

    # Dual
    # ------------------------------------------------------------------------------------------------
    # The dual of a polyhedron is another mesh wherein:
    # - every face in the original becomes a vertex in the dual
    # - every vertex in the original becomes a face in the dual
    #
    # So N_faces, N_vertices = N_dualfaces, N_dualvertices
    #
    # The new vertex coordinates are convenient to set to the original face centroids.
    @staticmethod
    def dual(poly: polyhedron) -> polyhedron:
        flag = polyflag()

        face = [{} for _ in range(len(poly.vertices))]

        for i, f in enumerate(poly.faces):
            v1 = f[-1]
            for v2 in f:
                face[v1][f'v{v2}'] = f'{i}'
                v1 = v2
        centers = poly.centers
        for i, _ in enumerate(poly.faces):
            flag.newV(f'{i}', centers[i])

        for i, f in enumerate(poly.faces):
            v1 = f[-1]
            for v2 in f:
                flag.newFlag(v1, face[v2][f'v{v1}'], f'{i}')
                v1 = v2

        dpoly = flag.topoly()  # build topological dual from flags

        # match F index ordering to V index ordering on dual
        sortF = [[] for _ in range(len(dpoly.faces))]
        for f in dpoly.faces:
            k = intersect(poly.faces[f[0]], poly.faces[f[1]], poly.faces[f[2]])
            sortF[k] = f
        dpoly.faces = sortF

        if poly.name[0] != 'd':
            dpoly.name = f'd{poly.name}'
        else:
            dpoly.name = poly.name[1:]

        return dpoly

    # Chamfer
    # ----------------------------------------------------------------------------------------
    # A truncation along a polyhedron's edges.
    # Chamfering or edge-truncation is similar to expansion, moving faces apart and outward,
    # but also maintains the original vertices. Adds a new hexagonal face in place of each
    # original edge.
    # A polyhedron with e edges will have a chamfered form containing 2e new vertices,
    # 3e new edges, and e new hexagonal faces. -- Wikipedia
    # See also http://dmccooey.com/polyhedra/Chamfer.html
    #
    # The dist parameter could control how deeply to chamfer.
    # But I'm not sure about implementing that yet.
    #
    # Q: what is the dual operation of chamfering? I.e.
    # if cX = dxdX, and xX = dcdX, what operation is x?
    #
    # We could "almost" do this in terms of already-implemented operations:
    # cC = t4daC = t4jC, cO = t3daO, cD = t5daD, cI = t3daI
    # But it doesn't work for cases like T.
    @staticmethod
    def chamfer(poly: polyhedron, dist=0.5) -> polyhedron:

        normals = poly.normals # [calc_normal([poly.vertices[ic] for ic in f]) for f in poly.faces]

        flag = polyflag()

        for i, f in enumerate(poly.faces):  # For each face f in the original poly
            v1 = f[-1]
            v1new = f'{i}_{v1}'

            for v2 in f:
                flag.newV(v2, mult(1.0 + dist, poly.vertices[v2]))

                v2new = f'{i}_{v2}'
                flag.newV(v2new, add(poly.vertices[v2], mult(dist * 1.5, normals[i])))

                flag.newFlag(f'orig{i}', v1new, v2new)
                facename = f'hex{v1}_{v2}' if v1 < v2 else f'hex{v2}_{v1}'
                flag.newFlag(facename, v2, v2new)
                flag.newFlag(facename, v2new, v1new)
                flag.newFlag(facename, v1new, v1)
                v1 = v2
                v1new = v2new

        newpoly = flag.topoly()
        newpoly.name = f'c{poly.name}'
        return newpoly

    # Whirl
    # ----------------------------------------------------------------------------------------------
    # Gyro followed by truncation of vertices centered on original faces.
    # This create 2 new hexagons for every original edge.
    # (https://en.wikipedia.org/wiki/Conway_polyhedron_notation#Operations_on_polyhedra)
    #
    # Possible extension: take a parameter n that means only whirl n-sided faces.
    # If we do that, the flags marked #* below will need to have their other sides
    # filled in one way or another, depending on whether the adjacent face is
    # whirled or not.
    @staticmethod
    def whirl(poly: polyhedron, n=0) -> polyhedron:
        flag = polyflag()

        for i, v in enumerate(poly.vertices):  # each old vertex is a new vertex
            flag.newV(f'v{i}', unit(v))

        centers = poly.centers

        for i, f in enumerate(poly.faces):
            v1, v2 = f[-2:]
            for j, v in enumerate(f):
                v3 = v
                # New vertex along edge
                v1_2 = oneThird(poly.vertices[v1], poly.vertices[v2])
                flag.newV(f'{v1}~{v2}', v1_2)
                # New vertices near center of face
                cv1name = f'center{i}~{v1}'
                cv2name = f'center{i}~{v2}'
                flag.newV(cv1name, unit(oneThird(centers[i], v1_2)))

                fname = f'{i}f{v1}'
                # New hexagon for each original edge
                flag.newFlag(fname, cv1name, f'{v1}~{v2}')
                flag.newFlag(fname, f'{v1}~{v2}', f'{v2}~{v1}')
                flag.newFlag(fname, f'{v2}~{v1}', f'v{v2}')
                flag.newFlag(fname, f'v{v2}', f'{v2}~{v3}')
                flag.newFlag(fname, f'{v2}~{v3}', cv2name)
                flag.newFlag(fname, cv2name, cv1name)
                # New face in center of each old face
                flag.newFlag(f'c{i}', cv1name, cv2name)

                v1, v2 = v2, v3

        newpoly = flag.topoly()
        newpoly.name = f'w{poly.name}'
        return newpoly

    # Quinto
    # ----------------------------------------------------------------------------------------------
    # This creates a pentagon for every point in the original face, as well as one new inset face.
    @staticmethod
    def quinto(poly: polyhedron) -> polyhedron:
        flag = polyflag()

        for i, f in enumerate(poly.faces):
            lv = list(map(lambda i: poly.vertices[i], f))
            centroid = calc_centroid(lv)
            v1, v2 = f[-2:]
            for v3 in f:
                midpt = midpoint(poly.vertices[v1], poly.vertices[v2])
                innerpt = midpoint(midpt, centroid)
                flag.newV(midName(v1, v2), midpt)
                flag.newV(f'inner_{i}_{midName(v1, v2)}', innerpt)

                flag.newV(f'{v2}', poly.vertices[v2])

                flag.newFlag(f'f{i}_{v2}', f'inner_{i}_{midName(v1, v2)}', midName(v1, v2))
                flag.newFlag(f'f{i}_{v2}', midName(v1, v2), f'{v2}')
                flag.newFlag(f'f{i}_{v2}', f'{v2}', midName(v2, v3))
                flag.newFlag(f'f{i}_{v2}', midName(v2, v3), f'inner_{i}_{midName(v2, v3)}')
                flag.newFlag(f'f{i}_{v2}', f'inner_{i}_{midName(v2, v3)}', f'inner_{i}_{midName(v1, v2)}')

                # inner rotated face of same vertex-number as original
                flag.newFlag(f'f_in_{i}', f'inner_{i}_{midName(v1, v2)}', f'inner_{i}_{midName(v2, v3)}')

                # shift over one
                v1, v2 = v2, v3

        newpoly = flag.topoly()
        newpoly.name = f'q{poly.name}'
        return newpoly

    # inset / extrude / "Loft" operator
    # ------------------------------------------------------------------------------------------
    @staticmethod
    def insetN(poly: polyhedron, n=0, inset_dist=0.5, popout_dist=-0.2) -> polyhedron:
        flag = polyflag()

        for i, p in enumerate(poly.vertices):
            flag.newV(f'v{i}', p)

        normals = poly.normals  # poly.calc_normals()
        centers = poly.centers  # poly.calc_centers()

        for i, f in enumerate(poly.faces):
            if len(f) == n or n == 0:
                for v in f:
                    flag.newV(f'f{i}v{v}', add(tween(poly.vertices[v], centers[i], inset_dist),
                                               mult(popout_dist, normals[i])))
        foundAny = False
        for i, f in enumerate(poly.faces):
            v1 = f'v{f[-1]}'
            for v in f:
                v2 = f'v{v}'
                if len(f) == n or n == 0:
                    foundAny = True
                    fname = f'{i}{v1}'
                    flag.newFlag(fname, v1, v2)
                    flag.newFlag(fname, v2, f'f{i}{v2}')
                    flag.newFlag(fname, f'f{i}{v2}', f'f{i}{v1}')
                    flag.newFlag(fname, f'f{i}{v1}', v1)
                    # new inset, extruded face
                    flag.newFlag(f'ex{i}', f'f{i}{v1}', f'f{i}{v2}')
                else:
                    flag.newFlag(i, v1, v2)  # same old flag, if non-n
                v1 = v2

        if not foundAny:
            print(f'No {n}-fold components were found.')

        newpoly = flag.topoly()
        newpoly.name = f'n{"" if n==0 else n}{poly.name}'
        return newpoly

    # extrudeN
    # ------------------------------------------------------------------------------------------
    # for compatibility with older operator spec
    @staticmethod
    def extrudeN(poly: polyhedron, n: int = 0) -> polyhedron:
        newpoly = transform.insetN(poly, n, 0.0, 0.3)
        newpoly.name = f'x{"" if n==0 else n}{poly.name}'
        return newpoly

    # loft
    # ------------------------------------------------------------------------------------------
    @staticmethod
    def loft(poly: polyhedron, n: int = 0, alpha=0.1) -> polyhedron:
        newpoly = transform.insetN(poly, n, alpha, 0.0)
        newpoly.name = f'l{"" if n==0 else n}{poly.name}'
        return newpoly

    # Hollow (skeletonize)
    #  ------------------------------------------------------------------------------------------
    @staticmethod
    def hollow(poly: polyhedron, inset_dist=0.5, thickness=0.2) -> polyhedron:
        dualnormals = transform.dual(poly).calc_normals()
        normals = poly.normals # poly.calc_normals()
        centers = poly.centers # poly.calc_centers()

        flag = polyflag()

        for i, p in enumerate(poly.vertices):
            flag.newV(f'v{i}', p)
            flag.newV(f'downv{i}', add(p, mult(-1 * thickness, dualnormals[i])))

        for i, f in enumerate(poly.faces):
            for v in f:
                flag.newV(f'fin{i}v{v}', tween(poly.vertices[v], centers[i], inset_dist))
                flag.newV(f'findown{i}v{v}', add(tween(poly.vertices[v], centers[i], inset_dist),
                                                 mult(-1 * thickness, normals[i])))

        for i, f in enumerate(poly.faces):
            v1 = f'v{f[-1]}'
            for v in f:
                v2 = f'v{v}'
                fname = f'{i}{v1}'

                flag.newFlag(fname, v1, v2)
                flag.newFlag(fname, v2, f'fin{i}{v2}')
                flag.newFlag(fname, f'fin{i}{v2}', f'fin{i}{v1}')
                flag.newFlag(fname, f'fin{i}{v1}', v1)

                fname = f'sides{i}{v1}'
                flag.newFlag(fname, f'fin{i}{v1}', f'fin{i}{v2}')
                flag.newFlag(fname, f'fin{i}{v2}', f'findown{i}{v2}')
                flag.newFlag(fname, f'findown{i}{v2}', f'findown{i}{v1}')
                flag.newFlag(fname, f'findown{i}{v1}', f'fin{i}{v1}')

                fname = f'bottom{i}{v1}'
                flag.newFlag(fname, f'down{v2}', f'down{v1}')
                flag.newFlag(fname, f'down{v1}', f'findown{i}{v1}')
                flag.newFlag(fname, f'findown{i}{v1}', f'findown{i}{v2}')
                flag.newFlag(fname, f'findown{i}{v2}', f'down{v2}')

                v1 = v2

        newpoly = flag.topoly()
        newpoly.name = f'H{poly.name}'
        return newpoly

    # scale vertices by factor
    @staticmethod
    def scale(poly: polyhedron, scale=1) -> polyhedron:
        for i, _ in enumerate(poly.vertices):
            poly.vertices[i] = mult(scale, poly.vertices[i])
        poly.refresh()
        return poly

    #  Perspectiva 1
    #  ------------------------------------------------------------------------------------------
    #  an operation reverse-engineered from Perspectiva Corporum Regularium
    @staticmethod
    def perspectiva1(poly: polyhedron) -> polyhedron:
        centers = poly.calc_centers()
        flag = polyflag()

        for i, p in enumerate(poly.vertices):
            flag.newV(f'v{i}', p)

        for i, f in enumerate(poly.faces):
            v1 = f'v{f[-2]}'
            v2 = f'v{f[-1]}'
            vert1 = poly.vertices[f[-2]]
            vert2 = poly.vertices[f[-1]]
            for v in f:
                v3 = f'v{v}'
                vert3 = poly.vertices[v]
                v12 = f'{v1}~{v2}'  # names for "oriented" midpoint
                v21 = f'{v2}~{v1}'
                v23 = f'{v2}~{v3}'

                # on each Nface, N new points inset from edge midpoints towards center = "stellated" points
                flag.newV(v12, midpoint(midpoint(vert1, vert2), centers[i]))

                flag.newFlag(f'in{i}', v12, v23)

                # new tri face constituting the remainder of the stellated Nface
                flag.newFlag(f'f{i}{v2}', v23, v12)
                flag.newFlag(f'f{i}{v2}', v12, v2)
                flag.newFlag(f'f{i}{v2}', v2, v23)

                # one of the two new triangles replacing old edge between v1->v2
                flag.newFlag(f'f{v12}', v1, v21)
                flag.newFlag(f'f{v12}', v21, v12)
                flag.newFlag(f'f{v12}', v12, v1);

                v1, v2 = v2, v3  # current becomes previous
                vert1, vert2 = vert2, vert3

        newpoly = flag.topoly()
        newpoly.name = f'P{poly.name}'
        return newpoly


if __name__ == '__main__':
    from py.seeds import tetrahedron

    pn = transform.perspectiva1(tetrahedron())
