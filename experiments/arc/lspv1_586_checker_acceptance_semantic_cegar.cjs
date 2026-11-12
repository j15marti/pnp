#!/usr/bin/env node
"use strict";
/* LSPV-1/586, exact independent semantic firewall for the pinned /341 fixture.
 * Usage: node experiments/arc/lspv1_586_checker_acceptance_semantic_cegar.cjs \
 *   results/raw/arc/2026-11-11_1824_LSPV3_582_STRING_CHARGE_SAT_ACCEPTED_PACKET.json
 * Reads ONLY an existing peer packet; never substitutes a new proof calculus.
 * This audits actual original-source satisfiability and false advertised affine
 * semantics. It does NOT execute or reimplement original checker acceptance. */
const fs = require("node:fs");
const assert = require("node:assert/strict");
const input = process.argv[2];
if (!input) throw Error("missing exact published packet path");
const parsed = JSON.parse(fs.readFileSync(input, "utf8"));
const f0 = parsed.fixtures?.[0];
const witness = "101001000000100000";
const copy = x => JSON.parse(JSON.stringify(x));
function semanticAudit(f, w) {
  assert.equal(f.graph.n, 12);
  assert.equal(f.graph.edges.length, 18);
  assert.equal(f.clauses.length, 48);
  assert.equal(f.proof.length, 47);
  assert.equal(typeof f.charges[0], "string");
  assert.equal(f.charges[0], "1");
  assert.equal(f.charges.reduce((a,b) => a ^ b, 0), 1);
  assert.match(w, /^[01]{18}$/);
  const bits = [...w].map(Number);
  function clauseSat(c) {
    return c.literals.some(lit =>
      bits[Math.abs(lit)-1] === (lit>0 ? 1 : 0));
  }
  assert.equal(f.clauses.filter(clauseSat).length, 48);
  const [d0,d1,d2] = f.proof;
  assert.deepEqual([d0.id,d1.id,d2.id],[48,49,50]);
  assert.deepEqual([d0.rule,d1.rule,d2.rule],["AND3","AND3","AND3"]);
  function factorTrue(d) {
    // Deliberately emulate the recovered checker's character iteration.
    const sup = [...d.support].map(Number);
    const m = sup.reduce((s,e,i) => s + (bits[e]<<i),0);
    return (d.table >> m) & 1;
  }
  assert.equal(factorTrue(d0),1);
  assert.equal(factorTrue(d1),1);
  assert.equal(clauseSat(f.clauses[3]),true);
  assert.deepEqual(d2.parents,[49,3]);
  assert.equal(d2.support,"012");
  assert.equal(d2.table,102);
  assert.equal(d2.row.mask,"0x1003");
  assert.equal(d2.row.rhs,1);
  assert.equal(factorTrue(d2),1);
  let lhs=0, mask=BigInt(d2.row.mask);
  for(let e=0;e<bits.length;e++)
    if((mask>>BigInt(e))&1n)lhs^=bits[e];
  // Advertised original-variable equation is FALSE in a genuine SAT model.
  assert.equal(lhs,0);
  assert.notEqual(lhs,d2.row.rhs);
  return {
    source_clauses_satisfied:48,source_clauses_total:48,
    source_model:w,source_vertices:12,source_edges:18,
    paid_proof_nodes:47,charge_0_type:typeof f.charges[0],
    xor_coerced_charge:f.charges.reduce((a,b)=>a^b,0),
    true_parent_ids:[48,49,3],
    false_original_coordinate_row:{id:50,mask:d2.row.mask,
      lhs,rhs:d2.row.rhs,support_json_type:typeof d2.support}
  };
}
const positive = semanticAudit(f0,witness);
const mutations = [
 ["charge_numeric", f=>{f.charges[0]=1;}],
 ["d2_typed_support", f=>{f.proof[2].support=[0,1,12];}],
 ["d2_row_rhs", f=>{f.proof[2].row.rhs=0;}],
 ["source_witness_failure", f=>{f.clauses[0].literals=[-1,2,-13];}],
 ["d2_false_parent", f=>{f.proof[2].parents[0]=-100;}],
 ["d2_false_table", f=>{f.proof[2].table=0;}]
];
const hostiles = mutations.map(([name,fn])=>{
  const altered=copy(f0);fn(altered);
  let rejected=false;try{semanticAudit(altered,witness)}
  catch(_){rejected=true}
  assert.equal(rejected,true,"hostile mutant escaped: "+name);
  return {name,rejected};
});
console.log(JSON.stringify({
  scope:"independent semantic audit; NOT an original /341 OS acceptance replay",
  input,positive,hostiles,all_passed:true
},null,2));
