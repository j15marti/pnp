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

const parseDimacs = text => {
  const lines=text.split(/\n/).map(s=>s.trim()).filter(s=>s && !s.startsWith("c"));
  if(!lines.length) fail("missing header");
  const h=lines[0].split(/\s+/);
  if(h.length!==4 || h[0]!=="p" || h[1]!=="cnf") fail("bad header");
  const n=Number(h[2]), m=Number(h[3]), clauses=[];
  for(const line of lines.slice(1)) {
    const xs=line.split(/\s+/).map(Number);
    if(!xs.length || xs.at(-1)!==0 || xs.slice(0,-1).includes(0)) fail("bad termination");
    const c=xs.slice(0,-1);
    if(c.some(x=>Math.abs(x)<1 || Math.abs(x)>n)) fail("bound");
    clauses.push(c);
  }
  if(clauses.length!==m) fail("count");
  return {n,clauses};
};
const dimacsModels = text => {
  const {n,clauses}=parseDimacs(text), out=[];
  for(let mask=0;mask<(1<<n);mask++) {
    const b=Array.from({length:n},(_,i)=>(mask>>i)&1);
    if(clauses.every(c=>c.some(l=>l>0 ? b[l-1]===1 : b[-l-1]===0))) out.push(b);
  }
  return out;
};

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

// Same-source labels, conservative extension, malformed and freshness controls.
const sm=dimacsModels("p cnf 1 1\n1 0\n");
const um=dimacsModels("p cnf 1 2\n1 0\n-1 0\n");
ok(JSON.stringify(sm)==="[[1]]", "SAT source control wrong");
ok(JSON.stringify(um)==="[]", "UNSAT source control wrong");
ok(sm.every(([x])=>[0,1].filter(z=>sat(xorAliased,{x,y:0,z})).length===1), "not uniquely extending");
for(const bad of ["p cnf 1 1\n1", "p cnf 1 2\n1 0\n", "p cnf 1 1\n2 0\n"]) {
  let rejected=false; try { parseDimacs(bad); } catch { rejected=true; }
  ok(rejected, "accepted malformed DIMACS");
}
ok(new Set(["x","z"]).size===2, "freshness control corrupt");

console.log(JSON.stringify({status:"PASS", run_id:"LSPV5_REFEREE356", checks, alias_bugs:bugs}, null, 2));
