#!/usr/bin/env node
"use strict";
const fs=require("fs");
const d=JSON.parse(fs.readFileSync("results/raw/arc/lspv5_333/conservative_extension_invariant_firewall_referee333.json","utf8"));
let checks=0; function ok(v,m){if(!v)throw new Error(m);checks++;}
ok(d.artifact==="CONSERVATIVE-EXTENSION-INVARIANT-FIREWALL-REFEREE333","artifact");
ok(d.gate_truth_rows.length===8,"gate rows");
for(const r of d.gate_truth_rows){ok(r.output===(r.inputs[0]||(r.inputs[1]&&r.inputs[2])),"gate truth");}
ok(d.php_total_extension_controls.length===3,"PHP rows");
for(const r of d.php_total_extension_controls){
  const h=r.h,m=(h+1)+h*((h+1)*h/2);
  ok(r.original_variables===h*(h+1),"PHP vars"); ok(r.original_clauses===m,"PHP clauses");
  ok(r.definition_clauses===4*r.definition_gates,"gate clauses");
  ok(r.selector_masks_checked===(h<=2?2**m:0),"selector masks");
}
ok(d.alias_controls.length===6,"alias rows");
for(const r of d.alias_controls){
  ok(r.definition_clauses===2*r.alias_edges,"alias clauses");
  ok(r.projected_models===(r.parity==="odd"?0:8),"projected models");
  ok(r.known_base_Rmix341_upper===15&&r.extended_upper_by_ignoring_aliases===15,"proof upper");
}
let fixtures=0;
for(const r of d.rank_one_factor_controls){
  const count=2**(2**r.n); fixtures+=count;
  ok(r.fixtures===count,"factor fixtures"); ok(r.unsat===1&&r.sat===count-1,"factor labels");
}
ok(fixtures===276&&d.factor_fixtures===276,"factor total"); ok(d.malformed_rejected===6,"malformed");
ok(d.asymptotic_theorem.destroyed.includes("O(h^4)"),"Cook/Haken gap");
ok(d.asymptotic_theorem.preserved.includes("unique fibres"),"fibres");
ok(d.transfer.required_direction.startsWith("W_R(F) <="),"reflection direction");
ok(d.transfer.warning.includes("wrong direction"),"direction warning");
ok(d.restricted_survivor.bound.includes("mu(F)-1"),"linear survivor");
ok(d.charged_ledger.factor_certification.includes("coNP-complete"),"certification barrier");
ok(d.charged_ledger.exponential_intermediate.includes("actual L"),"exponential representation");
ok(d.classification.restricted.includes("no machine lower bound"),"scope");
ok(d.classification.open.includes("B3_Rmix341")&&d.classification.open.includes("P!=NP"),"open");
console.log(JSON.stringify({artifact:d.artifact,independent_checks:checks,pass:true}));
