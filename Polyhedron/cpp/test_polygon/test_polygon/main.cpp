//
//  main.cpp
//  test_polygon
//
//  Created by asd on 08/09/2019.
//  Copyright © 2019 voicesync. All rights reserved.
//

#include "common.hpp"
#include "seeds.hpp"
#include "poly_operations.hpp"
#include "parser.hpp"

void test02() {
    auto p=Parser::parse("qD");
    p.recalc();
    p.print_stat();
}

void test01() {
    puts("start...");
    Polyhedron p=Seeds::tetrahedron();
    for (int i=0; i<4; i++) p=PolyOperations::trisub(p);
    p=PolyOperations::quinto(p);
    p.print_stat();
}

int main(int argc, const char * argv[]) {
    test02();
    return 0;
}
