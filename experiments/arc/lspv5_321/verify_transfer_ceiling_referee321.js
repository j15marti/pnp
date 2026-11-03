#!/usr/bin/env node
'use strict';
const fs=require('fs');
const d=JSON.parse(fs.readFileSync(process.argv[2]||'transfer_ceiling_referee321.json','utf8'));
let checks=0; function ok(x,m){checks++;if(!x)throw new Error(m)}
ok(d.run==='EXPONENTIAL-OVERHEAD-TRANSFER-CEILING-REFEREE321','run');
ok(d.task_id==='6ad42a2a9a088191ab9042245f3b4393','task');
ok(d.status.transfer_ceiling==='PROVED/EXACT' && d.status.B3==='OPEN','status');
for(const r of d.haken_normalized_rows){
  ok(6*r.candidate_q_equals_d>=r.normalized_H_bits,'64^d covers normalized source lower bound');
  ok(r.candidate_q_equals_d<=Math.ceil(r.normalized_H_bits/6),'candidate linear');
  ok(r.rhs_log2_lower>=r.normalized_H_bits,'logged inequality');
}
for(const r of d.braun_rows){
  ok(r.ell>=32,'Braun range');
  ok(BigInt(r.candidate_escape_e)<=BigInt(r.N_scale_proxy_n3_ell2),'escape polynomial in N proxy');
  ok(r.escape_le_N_proxy===true,'producer boolean');
}
for(const r of d.php_controls){
  ok(r.unsat_models===0,'PHP UNSAT');
  ok(r.deletion_sat_models>0 && Array.isArray(r.deletion_witness),'deleted source SAT');
}
ok(d.tseitin_control.odd_models===0,'odd Tseitin');
ok(d.tseitin_control.even_models===8,'even Tseitin');
ok(d.malformed_rejected===8,'malformed');
ok(d.resource_ledger.offline_diagnostic===true && d.resource_ledger.proof_optimizer_work_charged_to_W===false,'cost separation');
console.log(JSON.stringify({verified:true,checks,producer_checks:d.assertion_groups}));
