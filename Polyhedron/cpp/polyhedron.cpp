//
//  polygon.cpp
//  test_polygon
//
//  Created by asd on 03/09/2019.
//  Copyright © 2019 voicesync. All rights reserved.
//

#include "polyhedron.hpp"
#include "seeds.hpp"
#include "parser.hpp"

#include <boost/python.hpp>
#include <boost/python/numpy.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>

namespace p = boost::python;
namespace np = boost::python::numpy;

#include "python.h"
#include "poly_operations.hpp"

// polyhedrons
static p::list tetrahedron()  {    return poly2list( Seeds::tetrahedron() );   }
static p::list cube()         {    return poly2list( Seeds::cube() );          }
static p::list octahedron()   {    return poly2list( Seeds::octahedron() );    }
static p::list icosahedron()  {    return poly2list( Seeds::icosahedron() );   }
static p::list dodecahedron() {    return poly2list( Seeds::dodecahedron() );  }

static p::list pyramid(int n)   {    return poly2list( Seeds::pyramid(n) );  }
static p::list prism(int n)     {    return poly2list( Seeds::prism(n) );  }
static p::list antiprism(int n) {    return poly2list( Seeds::antiprism(n) );  }

static p::list cupola(int n=3, float alpha=0, float height=0)      {    return poly2list( Seeds::cupola(n, alpha, height) );  }
static p::list anticupola(int n=3, float alpha=0, float height=0)  {    return poly2list( Seeds::anticupola(n, alpha, height) );  }

static p::list johnson(int j) {    return poly2list( Seeds::johnson(j) );  }

static p::list polyhedron(p::list par_list) {
    if (p::len(par_list)==4) {
        char name=p::extract<char>(par_list[0]);
        int n=p::extract<int>(par_list[1]);
        float   alpha=p::extract<float>(par_list[2]),
                height=p::extract<float>(par_list[3]);

        return poly2list( Seeds::polyhedron(name, n, alpha, height) );
    } else return p::list();
}


// parse string
static p::list parse(string s) {
    auto p=Parser::parse(s);
    return poly2list(p);
}

BOOST_PYTHON_MODULE(polyhedron) {
    def("tetrahedron", tetrahedron);
    def("cube", cube);
    def("octahedron", octahedron);
    def("icosahedron", icosahedron);
    def("dodecahedron", dodecahedron);

    def("pyramid", pyramid, (p::arg("n")=4));
    def("prism", prism, (p::arg("n")=4));
    def("antiprism", antiprism, (p::arg("n")=4));

    def("cupola", cupola, (p::arg("n")=3), (p::arg("alpha")=0), (p::arg("height")=0));
    def("anticupola", anticupola, (p::arg("n")=3), (p::arg("alpha")=0), (p::arg("height")=0));
    def("johnson", johnson, (p::arg("j")=1));

    def("polyhedron", polyhedron); // 4 args not supported

    def("parse", parse, (p::arg("str")));
}
