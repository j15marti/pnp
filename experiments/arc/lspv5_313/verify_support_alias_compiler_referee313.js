#!/usr/bin/env node
"use strict";

const fs = require("fs");
const crypto = require("crypto");
const started = process.hrtime.bigint();
const path = "results/raw/arc/lspv5_313/support_alias_compiler_referee313.json";
const payload = fs.readFileSync(path, "utf8");
const data = JSON.parse(payload);
const FULL = 255;

function canon(xs) {
  if (!Array.isArray(xs)) throw new Error("not clause");
  const out = [...new Set(xs)].sort((a,b) => Math.abs(a)-Math.abs(b) || (a<0)-(b<0));
  if (out.some(x => !Number.isInteger(x) || typeof x === "boolean" || x === 0 || out.includes(-x)))
    throw new Error("noncanonical clause");
  return out;
}
function eq(a,b) { return JSON.stringify(a) === JSON.stringify(b); }
function truth(clause, assignment) {
  return clause.some(lit => Boolean((assignment >> (Math.abs(lit)-1)) & 1) === (lit > 0));
}
function models(clauses) {
  return [...Array(8).keys()].filter(a => clauses.every(c => truth(c,a)));
}
function resolve(left, right, pivot) {
  left = canon(left); right = canon(right);
  if (!left.includes(pivot) || !right.includes(-pivot)) throw new Error("bad pivot");
  return canon([...left.filter(x => x !== pivot), ...right.filter(x => x !== -pivot)]);
}
function replay(proof) {
  const lines = proof.sources.map(canon);
  for (const node of proof.nodes) {
    if (!Number.isInteger(node.left_id) || !Number.isInteger(node.right_id) ||
        node.left_id < 0 || node.right_id < 0 || node.left_id >= lines.length || node.right_id >= lines.length)
      throw new Error("parent");
    const out = resolve(lines[node.left_id], lines[node.right_id], node.pivot);
    if (!eq(out, canon(node.out))) throw new Error("resolvent");
    lines.push(out);
  }
  if (proof.cost !== proof.nodes.length || proof.root_id !== lines.length-1) throw new Error("cost/root");
  return lines[proof.root_id];
}

let pairs = 0, checks = 0;
for (let source=0; source<256; source++) for (let output=0; output<256; output++) {
  if ((source & (~output & FULL)) !== 0) continue;
  pairs++;
  for (let continuation=0; continuation<256; continuation++) {
    checks++;
    if (((source & continuation) & (~(output & continuation) & FULL)) !== 0)
      throw new Error("substitution invariant");
  }
}
if (pairs !== 6561 || checks !== 1679616 || data.exhaustive.entailed_pairs !== pairs ||
    data.exhaustive.substitution_checks !== checks) throw new Error("exhaustive counts");

const parity = data.parity;
if (parity.even_mask !== 105 || parity.odd_mask !== 150 ||
    !eq(models(parity.even_cnf), [0,3,5,6]) || !eq(models(parity.odd_cnf), [1,2,4,7]))
  throw new Error("parity labels");

let chainNodes = 0;
for (const control of data.same_support_chain_controls) {
  if (control.nodes.length !== control.semantic_nodes || control.materialized_internal_nodes !== 0 ||
      control.alias_representation_mask !== 1 || control.final_refutation_cost !== 3) throw new Error("chain metadata");
  let representation = control.alias_representation_mask;
  for (const node of control.nodes) {
    if (!eq(node.support,[1,2,3]) || (representation & (~node.output_mask & FULL)) !== 0)
      throw new Error("illegal alias");
  }
  chainNodes += control.semantic_nodes;
}
if (!eq(data.same_support_chain_controls.map(x=>x.semantic_nodes), [1,2,4,8,16,32]) || chainNodes !== 63)
  throw new Error("chain lengths");

const p0 = data.explicit_refutations.singleton_000_vs_odd;
const p1 = data.explicit_refutations.singleton_001_vs_even;
if (replay(p0).length !== 0 || replay(p1).length !== 0 || p0.cost !== 3 || p1.cost !== 3)
  throw new Error("explicit refutation");
if (!eq(models(p0.sources), []) || !eq(models(p1.sources), [])) throw new Error("refutation source label");

const projection = data.projection_exit_control;
if (!eq(replay(projection), [1]) || projection.cost !== 1 ||
    !eq(projection.input_support,[1,2]) || !eq(projection.output_support,[1])) throw new Error("projection");
if (!eq(models(projection.sources), [1,3,5,7])) throw new Error("projection source models");

const sat = data.both_label_sat_controls;
if (!eq(sat.singleton_000_and_even_models,[0]) || !eq(sat.singleton_001_and_odd_models,[1]) ||
    !eq(sat.singleton_000_and_odd_models,[]) || !eq(sat.singleton_001_and_even_models,[]))
  throw new Error("both-label controls");

const exits = Object.fromEntries(data.typed_exit_controls.map(x=>[x.case,x.alias_allowed]));
if (exits.same_support_semantic_consumer !== true || exits.strict_support_drop !== false ||
    exits.native_resolution_consumer !== false || exits.contradiction_output !== false)
  throw new Error("typed exits");

function parseAlias(obj) {
  const keys = ["consumer","input_support","output_mask","output_support","source_mask"];
  if (!obj || typeof obj !== "object" || Array.isArray(obj) || !eq(Object.keys(obj).sort(),keys)) throw new Error("schema");
  for (const k of ["input_support","output_support"]) {
    const s=obj[k];
    if (!Array.isArray(s) || s.length===0 || s.some(x=>!Number.isInteger(x)||typeof x==="boolean"||x<1||x>3) ||
        !eq(s,[...new Set(s)].sort((a,b)=>a-b))) throw new Error("support");
  }
  for (const k of ["source_mask","output_mask"])
    if (!Number.isInteger(obj[k]) || typeof obj[k] === "boolean" || obj[k]<0 || obj[k]>255) throw new Error("mask");
  if ((obj.source_mask & (~obj.output_mask & FULL)) !== 0) throw new Error("not consequence");
  if (!["semantic_same_support","typed_exit"].includes(obj.consumer)) throw new Error("consumer");
}
const valid={input_support:[1,2,3],output_support:[1,2,3],source_mask:1,output_mask:105,consumer:"semantic_same_support"};
parseAlias(valid);
const malformed=[null,{}, {...valid,extra:1}, {...valid,input_support:[]}, {...valid,output_support:[3,2,1]},
  {...valid,input_support:[1,1,2]}, {...valid,input_support:[0,1]}, {...valid,source_mask:-1},
  {...valid,output_mask:256}, {...valid,source_mask:true}, {...valid,consumer:"native_resolution"},
  {...valid,source_mask:150,output_mask:105}];
let malformedRejected=0;
for (const m of malformed) { try { parseAlias(m); } catch (_) { malformedRejected++; } }
if (malformedRejected !== 12 || data.malformed.rejected !== 12) throw new Error("malformed controls");

let corruptRejected=0;
function reject(mutator, kind) {
  const copy=JSON.parse(JSON.stringify(data)); mutator(copy);
  try {
    if (kind === "proof0") replay(copy.explicit_refutations.singleton_000_vs_odd);
    else if (kind === "proof1") replay(copy.explicit_refutations.singleton_001_vs_even);
    else if (kind === "projection") replay(copy.projection_exit_control);
    else if (kind === "chain") {
      const c=copy.same_support_chain_controls[0];
      if ((c.alias_representation_mask & (~c.nodes[0].output_mask & FULL)) !== 0) throw new Error("illegal alias");
    }
  } catch (_) { corruptRejected++; return; }
  throw new Error("corruption accepted");
}
reject(x=>{x.explicit_refutations.singleton_000_vs_odd.nodes[0].pivot*=-1;},"proof0");
reject(x=>{x.explicit_refutations.singleton_001_vs_even.nodes[1].right_id=99;},"proof1");
reject(x=>{x.projection_exit_control.nodes[0].out=[-1];},"projection");
reject(x=>{x.projection_exit_control.nodes[0].pivot=-2;},"projection");
reject(x=>{x.same_support_chain_controls[0].nodes[0].output_mask=0;},"chain");

console.log(JSON.stringify({
  status:"PASS",
  raw_sha256:crypto.createHash("sha256").update(payload).digest("hex"),
  independent_pairs:pairs,
  independent_substitution_checks:checks,
  semantic_chain_nodes_checked:chainNodes,
  replayed_paid_nodes:p0.cost+p1.cost+projection.cost,
  malformed_rejected:malformedRejected,
  corrupt_rejected:corruptRejected,
  verifier_wall_seconds:Number(process.hrtime.bigint()-started)/1e9,
  verifier_peak_rss_kib:process.resourceUsage().maxRSS
}));
