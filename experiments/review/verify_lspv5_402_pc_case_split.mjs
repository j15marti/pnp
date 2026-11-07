#!/usr/bin/env node
import fs from "node:fs";

const path = process.argv[2];
if (!path) throw new Error("usage: node verify_lspv5_402_pc_case_split.mjs result.json");
const data = JSON.parse(fs.readFileSync(path, "utf8"));
let checks = 0;
const ok = (v, m) => { checks++; if (!v) throw new Error(m); };
const key = p => JSON.stringify(p);
const asMap = p => new Map(p.map(([m,n,d]) => [JSON.stringify(m), n/d]));
const normalize = m => [...m.entries()].filter(([,c]) => c !== 0).sort(([a],[b]) => a.localeCompare(b));
const add = (p,q,a=1,b=1) => {
  const out = new Map();
  for (const [m,c] of asMap(p)) out.set(m,(out.get(m)||0)+a*c);
  for (const [m,c] of asMap(q)) out.set(m,(out.get(m)||0)+b*c);
  return normalize(out);
};
const mul = (p,v) => {
  const out = new Map();
  for (const [m,c] of asMap(p)) {
    const mm=JSON.stringify([...JSON.parse(m),v].sort());
    out.set(mm,(out.get(mm)||0)+c);
  }
  return normalize(out);
};
const canonical = p => normalize(asMap(p));
const lines = data.compiled_trace;
const seen = new Map();
for (const line of lines) {
  ok(!seen.has(line.id), "duplicate id");
  for (const p of line.parents) ok(seen.has(p), "missing/forward parent");
  if (line.kind === "lin") {
    const a=line.alpha[0]/line.alpha[1], b=line.beta[0]/line.beta[1];
    ok(JSON.stringify(canonical(line.poly))===JSON.stringify(add(seen.get(line.parents[0]),seen.get(line.parents[1]),a,b)),"bad lin");
  } else if (line.kind === "mul") {
    ok(JSON.stringify(canonical(line.poly))===JSON.stringify(mul(seen.get(line.parents[0]),line.var)),"bad mul");
  } else {
    ok(["source","bool"].includes(line.kind), "assumption leaked");
  }
  seen.set(line.id,line.poly);
}
ok(key(lines.at(-1).poly)===key([[[],1,1]]),"last line not one");
ok(data.example.left_guard.some(x=>x[0].length===0),"left guard lacks constant");
ok(data.example.right_guard.length===1 && data.example.right_guard[0][0][0]==="x", "right guard");
ok(data.example.compiled.lines===lines.length,"line count");
ok(data.example.compiled.maximum_degree===3,"degree control");
ok(data.example.compiled.monomial_occurrences <= 4*(data.example.left_branch.monomial_occurrences+data.example.right_branch.monomial_occurrences)+2,"size bound");
ok(lines.length <= 3*(data.example.left_branch.lines+data.example.right_branch.lines)+1,"length bound");
for (const value of Object.values(data.corruptions_rejected)) ok(value===true,"corruption not rejected");
for (const row of data.pcr_tree_controls) {
  ok(row.leaves===2**row.depth,"PCR leaf count");
  ok(row.pcr_guard_monomials_per_leaf===1,"PCR guard not monomial");
  ok(row.pc_worst_expanded_guard_monomials===2**row.depth,"PC expansion control");
  ok(row.omitted_leaf_witness_rejected===true,"omitted leaf accepted");
}
ok(data.disclaimer.includes("not an authoritative"),"disclaimer");
console.log(JSON.stringify({status:"PASS",checks,lines:lines.length}));
