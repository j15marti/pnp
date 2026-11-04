#!/usr/bin/env node
"use strict";
const fs=require("fs");
const d=JSON.parse(fs.readFileSync("results/raw/arc/lspv5_332/selector_profile_cost_nonidentifiability_referee332.json","utf8"));
let checks=0;
function ok(v,m){if(!v)throw new Error(m);checks++;}
ok(d.artifact==="SELECTOR-PROFILE-COST-NONIDENTIFIABILITY-REFEREE332","artifact");
ok(d.rows.length===3,"rows");
for(const r of d.rows){
  const h=r.h,m=(h+1)+h*((h+1)*h/2);
  ok(r.clauses_m===m,"clauses"); ok(r.php_variables===h*(h+1),"PHP vars");
  ok(r.horn_variables===m-1,"Horn vars"); ok(r.php_dimacs_bytes>0&&r.horn_dimacs_bytes>0,"sizes");
  ok(r.selector_truth_table_bits===2**m,"table");
  ok(r.selector_indexed_table_lower_bits===m*2**m,"indexed table");
  ok(r.compact_nand_literal_count===m,"NAND");
  ok(r.horn_exact_resolution_derived_nodes===m-1,"Horn Resolution");
  ok(r.php_resolution_anchor.includes("Haken"),"Haken scope");
}
ok(d.complete_selector_rows_checked===2**3+2**9,"profile enumeration");
ok(d.malformed_rejected===8,"malformed");
ok(d.exact_profile.includes("NOT(AND_i s_i)"),"profile");
ok(d.proof_costs.horn.startsWith("exactly m-1"),"Horn exact");
ok(d.proof_costs.scope.includes("R_mix341"),"scope firewall");
ok(d.charged_ledger.materialized_profile_output.startsWith("2^m"),"materialized");
ok(d.charged_ledger.compact_profile_output.includes("Theta(m"),"compact");
ok(d.charged_ledger.proof_output.includes("separate"),"proof output");
ok(d.classification.proved.length===2,"proved");
ok(d.classification.open.includes("B3_Rmix341")&&d.classification.open.includes("P!=NP"),"open");
console.log(JSON.stringify({artifact:d.artifact,independent_checks:checks,pass:true}));
