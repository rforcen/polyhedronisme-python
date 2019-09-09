from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor
from parsimonious import exceptions

from py import seeds, polyhedron
from py.transform import transform

base_seeds = {
    'T': seeds.tetrahedron,
    'O': seeds.octahedron,
    'C': seeds.cube,
    'I': seeds.icosahedron,
    'D': seeds.dodecahedron,
    'S': seeds.sphere,
    'P': seeds.prism,  # takes integer arg
    'A': seeds.antiprism,  # takes integer arg
    'Y': seeds.pyramid,  # takes integer arg
    'J': seeds.johnson_solid,  # takes integer arg
    'U': seeds.cupola,  # takes integer arg
    'V': seeds.anticupola,  # takes integer arg
}

takes_arg = 'PAYJUV'

op_trans = {
    'd': transform.dual,
    'a': transform.ambo,
    'k': transform.kisN,
    'g': transform.gyro,
    'p': transform.propellor,
    'r': transform.reflect,
    'c': transform.chamfer,
    'w': transform.whirl,
    'n': transform.insetN,  # -->needle
    'x': transform.extrudeN,
    'l': transform.loft,
    'P': transform.perspectiva1,
    'q': transform.quinto,
    # 'u': transform.trisub,
    # z --> zip
    'H': transform.hollow,
    # 'Z': transform.triangulate,
    # 'C': transform.canonicalize,
    # 'A': transform.adjustXYZ,
}

grammar_conway_polyhedron = Grammar(r'''
    transformation  = trans* seed
    
    trans = ~r"[dakgprcwnxlPquHZ]"
    seed = s_no_param / s_param
    
    s_no_param = ~r"[TOCIDS]"
    s_param = seed_param integer 
    seed_param = ~r"[PAYJUV]"
    integer = ~r"\d"+
'''
                                    )


class ConwayVisitor(NodeVisitor):
    def visit_transformation(self, node, vc):
        output = []
        for child in vc:
            output.append(child)
        return output

    def visit_trans(self, node, vc):
        return node.text

    def visit_s_no_param(selfself, node, vc):
        return node.text

    def visit_s_param(selfself, node, vc):
        key, int_value = vc[0].text, int("".join(map(str, [s.text for s in vc[1]])))

        return {key: int_value}

    def generic_visit(self, node, visited_children):
        return visited_children or node


def parse(poly_def: str) -> polyhedron:
    cv = ConwayVisitor()
    try:
        tree = grammar_conway_polyhedron.parse(poly_def)

        t, s = cv.visit(tree)
        s = s[0]

        # seed
        if type(s) == type(dict()):
            p = base_seeds[next(iter(s))](list(s.values())[0])
        else:
            p = base_seeds[s]()

        # transform
        for _tt in t:
            p = op_trans[_tt](p)

    except exceptions.ParseError:
        p = None

    return p
