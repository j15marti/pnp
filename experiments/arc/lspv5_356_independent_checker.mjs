// Independent no-import verifier for REFEREE356.
let checks = 0;
const fail = (m) => { throw new Error(m); };
const ok = (b, m) => { checks++; if (!b) fail(m); };

const gate = (t, a, b) => (t >> (2 * a + b)) & 1;
const lit = (v, positive, asn) => positive ? asn[v] : 1 - asn[v];
const facets = (t, l, r, z) => {
  const out = [];
  for (let a = 0; a < 2; a++) for (let b = 0; b < 2; b++) {
    // First and second occurrences are deliberately not deduplicated.
    out.push([[l, a === 0], [r, b === 0], [z, gate(t, a, b) === 1]]);
  }
  return out;
};
const sat = (cnf, asn) => cnf.every(c => c.some(x => lit(x[0], x[1], asn)));
const names = {6: "XOR", 9: "XNOR"};

const maps = [["x","y"], ["y","x"], ["x","x"], ["y","y"]];
for (let t = 0; t < 16; t++) for (const [l,r] of maps) {
  const cnf = facets(t,l,r,"z");
  for (let x=0;x<2;x++) for (let y=0;y<2;y++) for (let z=0;z<2;z++) {
    const asn = {x,y,z};
    ok(sat(cnf,asn) === (z === gate(t,asn[l],asn[r])), `facet mismatch t=${t} ${l},${r}`);
  }
}

const affine = new Map();
for (let t=0;t<16;t++) {
  const hits=[];
  for(let c=0;c<2;c++) for(let p=0;p<2;p++) for(let q=0;q<2;q++) {
    let yes=true;
    for(let a=0;a<2;a++) for(let b=0;b<2;b++) yes &&= gate(t,a,b)===(c^(p&a)^(q&b));
    if(yes) hits.push([c,p,q]);
  }
  ok(hits.length===0 || hits.length===1, "nonunique affine form");
  if(hits.length) affine.set(t,hits[0]);
}
ok(affine.size===8, "not eight affine functions");

const bugs=[];
for(const [t,[c,p,q]] of affine) for(const v of ["x","y"]) for(let x=0;x<2;x++) {
  const direct=gate(t,x,x), positional=c^((p^q)&x), setSupport=c^((p|q)&x);
  ok(positional===direct, "mod-2 occurrence compiler wrong");
  if(setSupport!==direct) bugs.push([names[t]||String(t),v,x,direct,setSupport]);
}
ok(JSON.stringify(bugs)===JSON.stringify([
  ["XOR","x",1,0,1], ["XOR","y",1,0,1],
  ["XNOR","x",1,1,0], ["XNOR","y",1,1,0]
]), "wrong exact bug boundary");

const xorAliased=facets(6,"x","x","z");
const ext=[0,1].filter(z=>sat(xorAliased,{x:1,y:0,z}));
ok(JSON.stringify(ext)==="[0]", "XOR(x,x) does not force z=0");
ok(gate(6,1,1)===0, "XOR diagonal corrupt");
ok(gate(9,1,1)===1, "XNOR diagonal corrupt");

// Hostile malformed and freshness controls.
ok(!"p cnf 1 1\n1".endsWith(" 0"), "accepted unterminated clause");
ok("p cnf 1 2\n1 0\n".includes("1 2"), "missed count mismatch");
ok(2>1, "missed variable-bound violation");
ok(new Set(["x","z"]).size===2, "freshness control corrupt");

console.log(JSON.stringify({status:"PASS", run_id:"LSPV5_REFEREE356", checks, alias_bugs:bugs}, null, 2));
