#!/usr/bin/env node
"use strict";
const fs=require("fs");
const d=JSON.parse(fs.readFileSync("results/raw/arc/lspv5_330/guarded_task_separation_referee330.json","utf8"));
let checks=0; function ok(v,m){if(!v)throw new Error(m);checks++;}
ok(d.artifact==="GUARDED-TASK-SEPARATION-REFEREE330","artifact");
ok(d.guarded_php_fixtures.length===3,"fixtures");
for(const f of d.guarded_php_fixtures){
  ok(f.source_variables===f.h*(f.h+1),"variables");
  ok(f.source_clauses===(f.h+1)+f.h*f.h*(f.h+1)/2,"clauses");
  ok(f.guarded_variables===f.source_variables+1,"guard");
  ok(f.guarded_clauses===f.source_clauses,"guarded clauses");
  ok(JSON.stringify(f.guard_relation)==="[0]","relation");
  ok(f.decider_branch==="guarded-php","branch");
  ok(f.source_bytes_read===f.guarded_dimacs_bytes,"scan");
  ok(f.witness_output_bits===f.guarded_variables,"output");
}
ok(JSON.stringify(d.boundary_relation_controls.SAT_source)==="[0,1]","SAT relation");
ok(JSON.stringify(d.boundary_relation_controls.UNSAT_source)==="[0]","UNSAT relation");
ok(JSON.stringify(d.manual_resolution_transport_steps)==="[1,2]","transport");
ok(d.control_results.some(x=>x.label==="SAT"),"SAT control");
ok(d.control_results.some(x=>x.label==="UNSAT"),"UNSAT control");
ok(d.control_results.every(x=>x.branch==="exact-fallback"),"fallback");
ok(d.malformed_rejected===8,"malformed");
ok(d.uniform_decider.one_program_all_lengths===true,"uniform");
ok(d.uniform_decider.fallback_worst_case==="exponential","worst case");
ok(d.classification.open.includes("B3")&&d.classification.open.includes("P!=NP"),"open");
console.log(JSON.stringify({artifact:d.artifact,independent_checks:checks,pass:true}));
