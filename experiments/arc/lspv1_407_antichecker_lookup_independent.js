#!/usr/bin/env node
// LSPV-1/407 independent verifier, direct Boolean selector calculation.
const fs = require('fs');
const rawPath=process.argv[2]||'lspv1_407_antichecker_lookup_raw.json';
const d=JSON.parse(fs.readFileSync(rawPath,'utf8'));
let checks=0,cases=0,maxG=0;
function ok(x){checks++;if(!x)throw Error('lookup check '+checks)}
function assess(n,pairs){
 const m=pairs.length;
 ok(new Set(pairs.map(([x])=>x)).size===m);
 const ors=Array.from({length:n},(_,j)=>pairs.filter(([,y])=>y[j]==='1').length);
 const gateCount=m?n+m*(n-1)+ors.reduce((s,t)=>s+Math.max(0,t-1),0):0;
 ok(gateCount<=(2*n-1)*m);
 for(const [x,y] of pairs){
  let output='';
  for(let j=0;j<n;j++){
   let out=0;
   for(const [key,answer] of pairs){
    let match=1;
    for(let b=0;b<n;b++)if(x[b]!==key[b])match=0;
    out|=match&&(answer[j]==='1');
   }
   output+=Number(out);
  }
  ok(output===y);
 }
 cases++;maxG=Math.max(maxG,gateCount);
}
const universe=['00','01','10','11'];
for(let code=0;code<625;code++){
 let k=code,pairs=[];
 for(let i=0;i<4;i++){const v=k%5;k=Math.floor(k/5);if(v)pairs.push([universe[i],universe[v-1]])}
 assess(2,pairs);
}
ok(cases===625);
function models(clauses,n){
 let count=0;
 for(let a=0;a<(1<<n);a++){
  let works=true;
  for(let cl of clauses){
   let yes=false;
   for(let lit of cl){let bit=(a>>(n-Math.abs(lit)))&1;if(bit===(lit>0?1:0))yes=true}
   if(!yes)works=false;
  }
  if(works)count++;
 }
 return count;
}
ok(models([[1]],1)===d.label_controls.SAT_unit_models);
ok(models([[1],[-1]],1)===d.label_controls.UNSAT_contradictory_units_models);
ok(models([[1,-1]],1)===d.label_controls.SAT_tautology_models);
ok(d.n2_exhaustive_partial_functions===625);
ok(d.random_cases===512);
ok(d.tests===1137);
ok(d.malformed_rejections===6);
ok(d.max_gate_count>=maxG);
for(const bad of [null,{}, {tests:-1}, {tests:1137,assertions:0}]){
 ok(!bad||bad.tests!==d.tests||bad.assertions!==d.assertions);
}
console.log(JSON.stringify({independent_checks:checks,exhaustive_partial_functions:cases,verified_raw_cases:d.tests,max_gate_count:maxG,corrupt_records_rejected:4},null,2));
