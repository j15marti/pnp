#!/usr/bin/env node
"use strict";
const fs=require("fs");
const d=JSON.parse(fs.readFileSync("results/raw/arc/lspv5_334/node_bit_normalization_firewall_referee334.json","utf8"));
let checks=0; const ok=(v,m)=>{if(!v)throw new Error(m);checks++;};
ok(d.artifact==="NODE-BIT-NORMALIZATION-OPTIMAL-SYSTEM-FIREWALL-REFEREE334","artifact");
ok(d.truth_function_fixtures===276,"fixtures");
ok(d.sat_fixtures===273&&d.unsat_fixtures===3,"labels");
ok(d.corrupt_traces_rejected===6&&d.malformed_rejected===7,"negative controls");
ok(d.horn_wrap_controls.length===12,"Horn controls");
for(let i=0;i<d.horn_wrap_controls.length;i++){
  const r=d.horn_wrap_controls[i];
  ok(r.k===i+1,"k"); ok(r.resolution_nodes===r.k,"Res nodes");
  ok(r.wrap_nodes===1,"Wrap node"); ok(r.wrapped_bytes>=r.payload_bytes,"bytes");
}
ok(d.theorem.counterexample.includes("mutually linear-time"),"p-equivalence firewall");
ok(d.theorem.repair.includes("node-to-bit"),"repair");
ok(d.theorem.optimality_frontier.includes("p-optimal"),"optimality frontier");
ok(d.classification.open.includes("B3_Rmix341")&&d.classification.open.includes("P!=NP"),"open scope");
console.log(JSON.stringify({artifact:d.artifact,independent_checks:checks,pass:true}));
