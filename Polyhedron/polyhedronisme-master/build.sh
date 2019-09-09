#!/bin/bash

# just concatenate for now
cat geo.js polyhedron.js johnson_solids.js topo_operators.js \
    geo_operators.js triangulate.js testing.js \
    parser.js canvas_ui.js > polyhedronisme.js

minify polyhedronisme.js -o polyhedronisme.min.js
