from math import sqrt, floor, log10

# helper funcs.
midName = lambda v1, v2: f'{v1}_{v2}' if v1 < v2 else f'{v2}_{v1}'
midpoint = lambda vec1, vec2: mult(0.5, add(vec1, vec2))
unit = lambda v: mult(1. / sqrt(mag2(v)), v)
tween = lambda vec1, vec2, t: [((1 - t) * vec1[0]) + (t * vec2[0]),
                               ((1 - t) * vec1[1]) + (t * vec2[1]),
                               ((1 - t) * vec1[2]) + (t * vec2[2])]
oneThird = lambda vec1, vec2: tween(vec1, vec2, 1 / 3.0)

sub = lambda v1, v2: [v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]]
add = lambda v1, v2: [v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]]
mult = lambda c, v: [v[0] * c, v[1] * c, v[2] * c]

mag2 = lambda v: v[0] * v[0] + v[1] * v[1] + v[2] * v[2]
mag = lambda v: sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
dot = lambda a, b: a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
cross = lambda d1, d2: [(d1[1] * d2[2]) - (d1[2] * d2[1]),
                        (d1[2] * d2[0]) - (d1[0] * d2[2]),
                        (d1[0] * d2[1]) - (d1[1] * d2[0])]

orthogonal = lambda v1, v2, v3: cross(sub(v2, v1), sub(v3, v2))


def intersect(set1, set2, set3):
    for s1 in set1:
        for s2 in set2:
            if s1 == s2:
                for s3 in set3:
                    if s1 == s3:
                        return s1
    return None  # empty intersection


def calc_normal(vertices):
    nv = [0, 0, 0]
    v1, v2 = vertices[-2:]
    for v3 in vertices:
        nv = add(nv, orthogonal(v1, v2, v3))
        v1, v2 = v2, v3
    return unit(nv)


def sigfigs(N, nsigs=2) -> int:  # returns string w. nsigs digits ignoring magnitude
    mantissa = N / pow(10, floor(log10(N)))
    return round(mantissa * pow(10, (nsigs - 1)))


def calc_centroid(vertices):
    # running sum of vertex coords
    centroidV = [0, 0, 0]
    for v in vertices:
        centroidV = add(centroidV, v);
    return mult(1. / len(vertices), centroidV)
