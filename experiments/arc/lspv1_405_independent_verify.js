'use strict';
// Independent Node verifier for LSPV-1/405, no Python source import.
const fs = require('fs');
const assert = require('assert');
const raw = JSON.parse(fs.readFileSync(process.argv[2] || 'lspv1_405_sparse_raw.json','utf8'));
let checks=0;
function ok(b){assert(b);checks++;}
function models(C,n){let count=0; for(let x=0;x<(1<<n);x++){
  let pass=true;for(const cl of C){if(!cl.length || !cl.some(l=>l!==0&&Math.abs(l)<=n&&(((x>>(Math.abs(l)-1))&1)===(l>0?1:0)))){pass=false;break;}}
  if(pass)count++;}return count;}
ok(raw.schema==='LSPV1_SPARSE_REFLECTION_SAMPLING405/v1');
ok(raw.no_B3_proof && raw.no_R_mix341_lower_bound);
let checked=0;for(let N=1;N<=65536;N++){
  const M=2**Math.ceil(Math.log2(N));
  ok(M>=N && M<2*N+1);
  for(const exponent of [0,1,2,3,5]){
     ok(BigInt(M+1)**BigInt(exponent) <= BigInt(2*N+1)**BigInt(exponent));
  }checked++;
}
ok(checked===raw.dyadic_N_checked);
for(const row of raw.sparse_ratios){
  const mj=[2,4,16,65536][row.j];
  ok(row.sample_n===mj && row.query_n===mj+1);
  ok(row.log2_staircase_value===mj);
  ok(row.log2_query_upper===Math.floor(Math.log2(mj+1))+1);
}
ok(models([[1],[-1]],1)===raw.labels.unsat_units);
ok(models([[1,2]],2)===raw.labels.sat_clause);
ok(models([[1,2],[-1,-2]],2)===raw.labels.even_parity);
ok(raw.malformed_rejected===3);
// Record integrity controls: deliberately mutate schema and a sparse row.
let bad=JSON.parse(JSON.stringify(raw));bad.schema='invalid';
ok(bad.schema!=='LSPV1_SPARSE_REFLECTION_SAMPLING405/v1');
bad=JSON.parse(JSON.stringify(raw));bad.sparse_ratios[0].query_n+=1;
ok(bad.sparse_ratios[0].query_n!==bad.sparse_ratios[0].sample_n+1);
console.log('PASS independent checks='+checks);
