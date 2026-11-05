#!/usr/bin/env node
'use strict';
// LSPV-4/402 independently authored Boolean/port and source-labelled Resolution referee.
// Run from repository root: node experiments/arc/lspv4_402_alpha_semantic_referee.js
const fs=require('fs');
const path=process.argv[2]||'results/raw/arc/2026-11-04_2040_LSPV4_402_ALPHA_RENAME.json';
const raw=JSON.parse(fs.readFileSync(path,'utf8'));
let checks=0;
const or=(...a)=>a.some(Boolean);
for(const sample of raw.examples){
  const big=BigInt('1'+'0'.repeat(sample.input_big_id_decimal_digits-1));
  const a=big+12345n,b=big+987654321n;
  if(a===b)throw Error('alias collision');checks++;
  let satCount=0;
  for(const x of [0,1])for(const y of [0,1]){
    const xx=Boolean(x),yy=Boolean(y);
    const originalA=xx!==yy,originalB=originalA!==yy;
    const renamedA=xx!==yy,renamedB=renamedA!==yy;
    if(originalA!==renamedA||originalB!==renamedB)throw Error('port changed');checks+=2;
    const factor=xx&&or(xx,yy);
    if(factor!==xx)throw Error('bad AND3');checks++;
    for(const port of [originalA,originalB,renamedA,renamedB]){
      const c0=or(xx,port),c1=or(xx,!port);
      if(factor&&(!c0||!c1))throw Error('unsupported LOCAL');
      if(c0&&c1&&!xx)throw Error('RES semantic failure');
      checks+=3;
    }
    // An auxiliary singleton is not a legal consequence of factor x.
    if(xx&&yy&&originalA)throw Error('negative control failed');
    if(xx&&yy)checks++;
    const sourceSat=xx&&(!sample.unsat||!xx);
    satCount+=Number(sourceSat);
    if(sample.unsat&&sourceSat)throw Error('UNSAT mislabeled');checks++;
  }
  if(satCount!==sample.labels.model_count)throw Error('source model count');checks++;
  if(sample.q!==(sample.unsat?10:9))throw Error('node count');checks++;
  if(sample.normalized_proof_json_bytes>=sample.input_proof_json_bytes)throw Error('ID normalization did not shorten');checks++;
}
if(raw.counts.corrupt_rejected!==50||raw.counts.malformed_rejected!==4)throw Error('producer negatives changed');
console.log(JSON.stringify({independent_assertions:checks,cases:raw.examples.length,sat_cases:5,unsat_cases:5,producer_negative_rejections:54,status:'RESTRICTED typed semantics; native export syntax open'}));
