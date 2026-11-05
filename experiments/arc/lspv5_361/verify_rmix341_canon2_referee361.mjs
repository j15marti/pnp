#!/usr/bin/env node
// Independent semantic audit of REFEREE361; imports no producer code.
import fs from "node:fs";
const raw = JSON.parse(fs.readFileSync("results/raw/arc/2026-11-05_0448_LSPV5_REFEREE361_raw.json", "utf8"));
let checks = 0;
function ok(x, m) { if (!x) throw new Error(m); checks++; }
const sortClause = a => [...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y) || +(x<0)-+(y<0));
const sat = (c,e) => c.some(l => e[Math.abs(l)] === +(l>0));
function facets(mask) {
  const out=[];
  for (const av of [0,1]) for (const bv of [0,1]) {
    const t=(mask>>(av|(bv<<1)))&1, zv=1-t;
    out.push(sortClause([av?-1:1,bv?-1:1,zv?-2:2]));
  }
  return out;
}
function oriented(a,b,p) {
  const ans=[];
  if(a.includes(p)&&b.includes(-p)) ans.push(sortClause([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]));
  if(a.includes(-p)&&b.includes(p)) ans.push(sortClause([...a.filter(x=>x!==-p),...b.filter(x=>x!==p)]));
  return ans;
}

let vulnerable=0;
for(let mask=0;mask<16;mask++) {
  const f=facets(mask); ok(f.length===4,`facets ${mask}`);
  // Every possible x extends uniquely to z=f(x,x) and satisfies all facets.
  for(const x of [0,1]) {
    const z=(mask>>(x|(x<<1)))&1, e={1:x,2:z};
    for(let j=0;j<4;j++) ok(sat(f[j],e),`definition ${mask}/${x}/${j}`);
  }
  ok(f[1].includes(1)&&f[1].includes(-1),`facet1 taut ${mask}`);
  ok(f[2].includes(1)&&f[2].includes(-1),`facet2 taut ${mask}`);
  const old1=f[1].filter(l=>Math.abs(l)!==1), old2=f[2].filter(l=>Math.abs(l)!==1);
  if(old1.length===1&&old2.length===1&&old1[0]===-old2[0]) vulnerable++;
  const n1=oriented(f[1],[1],1), n2=oriented(f[2],[1],1);
  ok(n1.length===1&&n1[0].includes(1),`oriented keeps x facet1 ${mask}`);
  ok(n2.length===1&&n2[0].includes(1),`oriented keeps x facet2 ${mask}`);
}
ok(vulnerable===8,"eight vulnerable truth tables");

// Exact LSPV-2/415 witness: old checker accepted a false unit on model x=z=1.
const witnessFacets=facets(0b1010);
ok(JSON.stringify(witnessFacets[1])===JSON.stringify([1,-1,-2]),"witness facet1");
ok(JSON.stringify(witnessFacets[2])===JSON.stringify([1,-1,2]),"witness facet2");
ok(!sat([-2],{1:1,2:1}),"old false unit");
ok(JSON.stringify(oriented(witnessFacets[1],[1],1)[0])===JSON.stringify([1,-2]),"new resolvent1");
ok(JSON.stringify(oriented(witnessFacets[2],[1],1)[0])===JSON.stringify([1,2]),"new resolvent2");

// LSPV-4/412 distinct-parent affine-subsupport source.
const clauses=[[1,2],[1,-2],[-1],[-1,2]];
const t0=[],t1=[];
for(let z=0;z<4;z++) {
  const e={1:z&1,2:(z>>1)&1};
  t0.push(+(sat(clauses[0],e)&&sat(clauses[1],e)));
  t1.push(+(sat(clauses[2],e)&&sat(clauses[3],e)));
  ok(t0[z]===e[1],`factor x ${z}`); ok(t1[z]===1-e[1],`factor !x ${z}`);
}
ok(JSON.stringify(t0)===JSON.stringify([0,1,0,1]),"x table");
ok(JSON.stringify(t1)===JSON.stringify([1,0,1,0]),"!x table");
ok(raw.legal_affine_subsupport.accepted&&raw.legal_affine_subsupport.paid_nodes===3,"coverage accepted");

ok(raw.old_checker_unsound_attack.old_accept.accepted,"old exploit accepted");
ok(raw.old_checker_unsound_attack.paid_nodes===4&&raw.old_checker_unsound_attack.bytes===615,"old exploit ledger");
ok(raw.old_checker_unsound_attack.new_reject.includes("oriented resolvent"),"new exploit rejection");
ok(raw.external_source_replacement_reject.includes("externally supplied"),"external source rejection");
ok(raw.huge_sparse_header.accepted&&raw.huge_sparse_header.header_decimal_digits===81,"sparse huge header");
ok(raw.huge_sparse_header.active_original_ids===1,"active coordinate count");
ok(raw.odd_k4.accepted&&raw.odd_k4.paid_nodes===15,"odd K4 replay");
ok(raw.status.REFEREE360_soundness==="FALSIFIED_RETIRED", "retirement status");
ok(raw.status.same_R_B3==="OPEN"&&raw.status.P_vs_NP==="OPEN","open status");
console.log(JSON.stringify({status:"PASS",checks,vulnerable_alias_truth_tables:vulnerable,
  oriented_witness:[oriented(witnessFacets[1],[1],1)[0],oriented(witnessFacets[2],[1],1)[0]]}));
