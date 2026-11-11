#!/usr/bin/env node
'use strict';
/*
 * LSPV-4/544: accepted-byte trailing-whitespace query lower-bound audit.
 * Native /386 checker is used without modification, with true OS Node
 * subprocesses when this file is run in a repository checkout.
 *
 * Usage: node experiments/arc/lspv4_544_native_json_whitespace_query_audit.cjs
 */
const fs=require('fs');
const os=require('os');
const path=require('path');
const crypto=require('crypto');
const cp=require('child_process');
const assert=require('assert/strict');
const root=path.resolve(__dirname,'../..');
const checkerPath=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedPath=path.join(root,'results/raw/arc/2026-11-11_0336_LSPV4_540_OWNER_FACET_CROSS_CONE_ACCEPTED.json');
const pin={
  checker:'338305c0ce101704205e57543756b8127074a986',
  seed:'25b5c1f95734f6eae36bdbb4a17c948c00753cff'
};
function gitBlobSHA(bytes){
  return crypto.createHash('sha1').update(Buffer.from('blob '+bytes.length+'\0')).update(bytes).digest('hex');
}
function sha256(bytes){return crypto.createHash('sha256').update(bytes).digest('hex')}
const checker=fs.readFileSync(checkerPath),seed=fs.readFileSync(seedPath);
assert.equal(gitBlobSHA(checker),pin.checker,'original checker provenance mismatch');
assert.equal(gitBlobSHA(seed),pin.seed,'original seed provenance mismatch');
const baseObj=JSON.parse(seed);
const cases=[0,1,16,128,2048,8192],positives=[],negativeOriginal=[],negativeParser=[];
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv4-544-'));
function runOriginal(bytes,label){
  const p=path.join(temp,label+'.json');
  fs.writeFileSync(p,bytes);
  const result=cp.spawnSync(process.execPath,[checkerPath,p],{encoding:'utf8',maxBuffer:4*1024*1024});
  const ok=result.status===0&&!result.error;
  let data=null;
  if(ok){try{data=JSON.parse(result.stdout.trim().split(/\r?\n/).at(-1))}catch(e){throw Error('invalid checker response '+label+': '+e)}}
  return {accepted:ok,status:result.status,stderr:(result.stderr||'').slice(0,450),output:data};
}
try {
  for(const k of cases){
    const bytes=Buffer.concat([seed,Buffer.alloc(k,0x20)]);
    assert.deepEqual(JSON.parse(bytes),baseObj,'JSON parse mismatch for padding '+k);
    const got=runOriginal(bytes,'positive-'+k);
    assert.equal(got.accepted,true,'original rejected whitespace '+k+': '+got.stderr);
    assert.equal(got.output.paid,31);
    assert.equal(got.output.res,30);
    assert.equal(got.output.def,1);
    assert.equal(got.output.records,49);
    assert.equal(got.output.negativeTests,11);
    assert.equal(got.output.assertions,3750);
    assert.equal(got.output.sha256,sha256(bytes));
    positives.push({k,bytes:bytes.length,paid:got.output.paid,
      res:got.output.res,owners:got.output.def,records:got.output.records,
      assertions:got.output.assertions,bundledNegativeTests:got.output.negativeTests,
      sha256:sha256(bytes)});
  }
  const k=128;
  for(let j=0;j<k;j++){
    const bytes=Buffer.concat([seed,Buffer.alloc(j,0x20),Buffer.from('!'),Buffer.alloc(k-j-1,0x20)]);
    let parsed=false;
    try{JSON.parse(bytes);parsed=true}catch(e){}
    assert.equal(parsed,false,'host JSON.parse failed to reject mutated padding '+j);
    negativeParser.push(j);
    if([0,1,63,127].includes(j)){
      const got=runOriginal(bytes,'mutated-space-'+j);
      assert.equal(got.accepted,false,'original accepted corrupted whitespace '+j);
      negativeOriginal.push({index:j,bytes:bytes.length,rejected:true,stderr:got.stderr});
    }
  }
  // Native-source negative guard, independent of JSON syntax.
  const damaged=structuredClone(baseObj);
  damaged.records[0].c=[-damaged.spec.guard];
  const damagedResult=runOriginal(Buffer.from(JSON.stringify(damaged)),'damaged-source');
  assert.equal(damagedResult.accepted,false,'original accepted wrong SOURCE');
  negativeOriginal.push({kind:'source-forgery',rejected:true,stderr:damagedResult.stderr});
  const result={
    run:'LSPV4_544',status:'COMPUTATIONAL',runtime:process.version,
    originalCheckerGitBlob:pin.checker,originalSeedGitBlob:pin.seed,
    baselineBytes:seed.length,originalProof:{sources:17,owners:1,resolutions:30,paid:31,records:49},
    positives,negativeParserPositionsExhaustive:negativeParser.length,
    negativeOriginal,claim:'Every trailing-ASCII-space position in an accepted P_k is decisive for exact-byte membership; deterministic zero-error random-access byte-query verification on this packet needs >= k queries.',
    modelLimitation:'Only /386 original; no R_mix341 mixed dispatcher, SAT decision-time or minimum proof-work lower bound.'
  };
  process.stdout.write(JSON.stringify(result,null,2)+'\n');
}finally{fs.rmSync(temp,{recursive:true,force:true})}
