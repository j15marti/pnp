#!/usr/bin/env node
const fs=require('fs'), crypto=require('crypto'), path=require('path');
const root=path.resolve(__dirname,'../../..');
const p=path.join(root,'results/raw/arc/lspv5_320/finite_audit_firewall_referee320.json');
const raw=fs.readFileSync(p,'utf8'), d=JSON.parse(raw);
let checks=0; function ok(x,m){checks++;if(!x)throw new Error(m)}
ok(d.run==='FINITE-PREFIX-AUDIT-FIREWALL-REFEREE320','run');
ok(d.task_id==='6ad42a2a9a088191ab9042245f3b4393','task');
ok(d.catalog.formulas===255 && d.catalog.sat===254 && d.catalog.unsat===1,'catalog');
ok(d.malformed_count===12,'malformed');
ok(d.audits.length===6,'audits');
let prev=0;
for(const a of d.audits){
  ok(a.bound>prev,'bounds'); prev=a.bound;
  ok(a.exception_bytes>a.bound,'strictly beyond audit');
  ok(a.correct_label==='SAT' && a.forged_label==='UNSAT','false rejection');
  ok(a.witness_all_ones===true,'witness');
  ok(a.symbolic_all_strings_le_bound_agree===true,'symbolic prefix');
  ok(a.malformed_checked===12,'malformed prefix');
  ok(a.forged_work===a.exception_bytes+1,'charged full comparison');
}
ok(d.tseitin_k4.odd_models===0 && d.tseitin_k4.even_models===8,'xor control');
ok(d.both_label_control.sat_exception_family && d.both_label_control.unsat_complete_cube,'labels');
ok(d.all_phase.logical_minimum_claimed===false,'no minimum claim');
for(const k of ['B1','B2','B3','P_vs_NP'])ok(d.status[k]==='OPEN',k);
const sha=crypto.createHash('sha256').update(raw).digest('hex');
console.log(JSON.stringify({status:'PASS',checks,sha256:sha}));
