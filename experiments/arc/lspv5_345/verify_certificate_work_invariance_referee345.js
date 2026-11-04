#!/usr/bin/env node
const fs=require('fs');
const x=JSON.parse(fs.readFileSync('results/raw/arc/2026-11-04_1352_LSPV5_345_CERTIFICATE_WORK_INVARIANCE.json','utf8'));
let checks=0;const ok=(v,m)=>{checks++;if(!v)throw Error(m)};
ok(x.status==='PASS','status');ok(x.rows.length===16,'rows');ok(x.malformed_rejected===64,'malformed');ok(x.sat_siblings_rejected===32,'SAT');
for(const r of x.rows){ok(r.assignments===2**r.n,'assignments');ok(r.unpacked_paid_nodes===2**r.n,'unpacked nodes');ok(r.packed_paid_nodes===1,'packed node');ok(r.unpacked_proof_bits===r.packed_proof_bits,'proof bits');ok(r.unpacked_certificate_work===r.packed_certificate_work,'work');ok(r.translation_output_bits===r.unpacked_proof_bits,'output');ok(r.dense_parity_table_bits===2**r.n,'dense');ok(r.xor_descriptor_bits===r.n+2,'xor')}
ok(/^[0-9a-f]{64}$/.test(x.digest),'digest');console.log(JSON.stringify({status:'PASS',checks},null,2));
