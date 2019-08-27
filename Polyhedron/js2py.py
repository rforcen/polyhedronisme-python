import jiphy

js_code = '''
// Kis(N)
// ------------------------------------------------------------------------------------------
// Kis (abbreviated from triakis) transforms an N-sided face into an N-pyramid rooted at the
// same base vertices.
// only kis n-sided faces, but n==0 means kis all.
//
const kisN = function(poly, n, apexdist){
  let i;
  if (!n) { n = 0; }
  if (apexdist===undefined) { apexdist = 0.1; }
  console.log(`Taking kis of ${n===0 ? "" : n}-sided faces of ${poly.name}...`);

  const flag = new polyflag();
  for (i = 0; i < poly.vertices.length; i++) {
    // each old vertex is a new vertex
    const p = poly.vertices[i];
    flag.newV(`v${i}`, p);
  }

  const normals = poly.normals();
  const centers = poly.centers();
  let foundAny = false;
  for (i = 0; i < poly.faces.length; i++) {
    const f = poly.faces[i];
    let v1 = `v${f[f.length-1]}`;
    for (let v of f) {
      const v2 = `v${v}`;
      if ((f.length === n) || (n === 0)) {
        foundAny = true;
        const apex = `apex${i}`;
        const fname = `${i}${v1}`;
        // new vertices in centers of n-sided face
        flag.newV(apex, add(centers[i], mult(apexdist, normals[i])));
        flag.newFlag(fname,   v1,   v2); // the old edge of original face
        flag.newFlag(fname,   v2, apex); // up to apex of pyramid
        flag.newFlag(fname, apex,   v1); // and back down again
      } else {
        flag.newFlag(`${i}`, v1, v2);  // same old flag, if non-n
      }
      // current becomes previous
      v1 = v2;
    }
  }

  if (!foundAny) {
    console.log(`No ${n}-fold components were found.`);
  }

  const newpoly = flag.topoly();
  newpoly.name = `k${n === 0 ? "" : n}${poly.name}`;
  return newpoly;
};

'''


print(jiphy.to.python(code=js_code))

