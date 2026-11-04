#!/usr/bin/env node
const fs=require('fs');
const x=JSON.parse(fs.readFileSync('results/raw/arc/2026-11-04_1251_LSPV5_344_POPTIMAL_BALANCE.json','utf8'));
let checks=0; function ok(v,m){checks++;if(!v)throw new Error(m)}
ok(x.status==='PASS','status'); ok(x.cnf_cases===256,'cases'); ok(x.sat_cases===95,'SAT'); ok(x.unsat_cases===161,'UNSAT');
ok(x.minimum_target_nodes['1']===112,'q1'); ok(x.minimum_target_nodes['2']===48,'q2'); ok(x.minimum_target_nodes['3']===1,'q3');
for(const k of ['decision','truth_table','resolution'])ok(x.valid_source_translations[k]===161,k);
ok(x.malformed_source_certificates_rejected===644,'malformed'); ok(x.rdagger.length===15,'rows');
for(const r of x.rdagger){ok(r.minimum_paid_nodes===1,'min');ok(r.minimum_proof_bits_excluding_source===1+2**r.N,'long');ok(r.short_nonminimum_paid_nodes===r.N,'cost');ok(r.short_nonminimum_bits_excluding_source===1+r.N,'short');ok(r.truncated_minimum_rejected,'trunc');ok(r.SAT_label_rejected,'SAT reject')}
ok(/^[0-9a-f]{64}$/.test(x.case_digest),'digest'); console.log(JSON.stringify({status:'PASS',checks},null,2));
