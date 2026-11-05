#!/usr/bin/env node
// Independent finite verifier for LSPV-1/406. Standard library only.
'use strict';
const fs=require('fs');
const path=process.argv[2]||'results/raw/arc/2026-11-04_1905_LSPV1_FEASIBLE_ANTICHECKER_B3_406.json';
const d=JSON.parse(fs.readFileSync(path,'utf8'));
let checks=0;
function ok(b,msg){if(!b)throw Error(msg);checks++}
const cases=[[[1]],[[-1]],[[1],[-1]],[[1,2]],[[-1,-2]],[[1,2],[-1]],[[1,2],[-1],[-2]],[[1,2],[-1,-2]]];
const truth=cases.map(cs=>[0,1,2,3].some(a=>cs.every(c=>c.some(l=>(Boolean(a&(1<<(Math.abs(l)-1))))===(l>0))))?1:0);
ok(JSON.stringify(truth)===JSON.stringify(d.sat_labels),'SAT labels');
ok(d.source_count===8 && d.all_classifiers===256,'shape');
for(let omit=0;omit<8;omit++){
 const row=d.mutation_records[omit];
 ok(row.omitted_index===omit,'omit');
 ok(row.sample_indices.length===7 && !row.sample_indices.includes(omit),'sample');
 const g=row.flipped_classifier;
 for(let i=0;i<8;i++)ok(g[i]===(i===omit?1-truth[i]:truth[i]),'pointwise flip');
 ok(row.classifiers_agree_on_sample===2,'two compatible');
}
for(let subset=0;subset<256;subset++){
 let candidates=0;
 for(let g=0;g<256;g++){
   let good=true;
   for(let i=0;i<8;i++)if(subset&(1<<i))if(((g>>i)&1)!==truth[i]){good=false;break}
   if(good && Array.from({length:8},(_,i)=>(g>>i)&1).some((v,i)=>v!==truth[i]))candidates++;
 }
 ok((candidates>0)===(subset!==255),'proper subsets fail');
}
ok(d.proper_subset_masks===255 && d.malformed_rejections===9,'controls');
console.log(JSON.stringify({artifact:d.artifact,all_passed:true,independent_checks:checks,labels:truth}));
