#!/usr/bin/env node
'use strict';
// LSPV-3/572: execute ORIGINAL archived /386 CLI as an OS subprocess.
// The original checker is unmodified; this file is an independent driver.
// It is not an implementation of full historical R_mix341.
const fs=require('fs'),path=require('path'),os=require('os'),cp=require('child_process');
const crypto=require('crypto'),assert=require('assert').strict;
const ROOT=path.resolve(__dirname,'../..');
const CHECK='experiments/arc/lspv2_386_independent_verify.js';
const SEED='results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json';
const TARGET='results/raw/arc/2026-11-11_0824_LSPV3_572_CYCLE_SPACE_NATIVE_OS_RAW.json';
const SHA={checker:'338305c0ce101704205e57543756b8127074a986',
           seed:'08aa169b5db49b2ddd1cb5a9b6890fcc3b790916'};
function bytes(rel){
  const buf=fs.readFileSync(path.join(ROOT,rel));
  const got=crypto.createHash('sha1').update(Buffer.concat([
    Buffer.from('blob '+buf.length+'\0'),buf])).digest('hex');
  assert.equal(got,rel===CHECK?SHA.checker:SHA.seed,'pinned Git blob mismatch '+rel);
  return buf;
}
const source=bytes(CHECK);const seed=JSON.parse(bytes(SEED).toString('utf8'));
const E=seed.spec.edges.length, V=seed.spec.h;
assert.equal(E,6);assert.equal(V,4);assert.equal(seed.records.length,74);
const clone=x=>JSON.parse(JSON.stringify(x));
const canonical=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function flip(x,mask){
  return Math.abs(x)<=E && (mask&(1<<(Math.abs(x)-1))) ? -x : x;
}
function transport(mask){
  const q=clone(seed);
  for(const r of q.records){
    r.c=canonical(r.c.map(x=>flip(x,mask)));
    if(r.kind==='RES')r.pivot=flip(r.pivot,mask);
  }
  for(const owner of q.gate_defs){
    owner[2]=flip(owner[2],mask);owner[3]=flip(owner[3],mask);
  }
  return q;
}
function boundary(mask){
  const out=[];
  for(let v=0;v<V;v++){
    let s=0;
    seed.spec.edges.forEach(([a,b],e)=>{if(mask&(1<<e))s^=Number(a===v||b===v)});
    if(s)out.push(v);
  }
  return out;
}
function sources(q){
  return q.records.filter(r=>r.kind==='SOURCE')
    .map(r=>JSON.stringify([r.source,r.c])).sort();
}
const s0=JSON.stringify(sources(seed));
const originalSpec=JSON.stringify(seed.spec);
const originalOwners=JSON.stringify(seed.gate_defs.map(g=>g.slice(0,2)));
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-lspv3-572-'));
let counter=0;
function replay(q){
  const filename=path.join(temp,'certificate_'+(counter++)+'.json');
  const data=Buffer.from(JSON.stringify(q)+'\n');
  fs.writeFileSync(filename,data);
  const result=cp.spawnSync(process.execPath,[path.join(ROOT,CHECK),filename],
    {encoding:'utf8',timeout:30000,maxBuffer:16*1024*1024});
  if(result.error)throw result.error;
  if(result.status===0){
    const r=JSON.parse(result.stdout);
    return {accepted:true,paid:r.paid,assertions:r.assertions,
      negativeTests:r.negativeTests,sha256:r.sha256,bytes:data.length};
  }
  return {accepted:false,reason:(result.stderr||'').split('\n').slice(0,4).join(' | '),
    bytes:data.length};
}
try{
  const cases=[];
  for(let mask=0;mask<(1<<E);mask++){
    const q=transport(mask),odd=boundary(mask);
    assert.equal(JSON.stringify(q.spec),originalSpec,'source spec unchanged');
    assert.equal(JSON.stringify(q.gate_defs.map(g=>g.slice(0,2))),originalOwners,
                 'paid gate owners changed');
    const sameSources=JSON.stringify(sources(q))===s0;
    assert.equal(sameSources,odd.length===0,'source multiset/cycle equivalence');
    const result=replay(q);
    assert.equal(result.accepted,odd.length===0,'original checker mismatch '+mask);
    if(result.accepted){
      assert.equal(result.paid,53);assert.equal(result.assertions,4663);
      assert.equal(result.negativeTests,11);
    }
    cases.push({mask,bitmask:mask.toString(2).padStart(E,'0'),
      boundary:odd,sourceFixed:sameSources,...result});
  }
  const positive=cases.filter(x=>x.accepted).map(x=>x.mask);
  assert.deepEqual(positive,[0,11,21,30,38,45,51,56]);
  const hostiles=[];
  const reject=(name,change)=>{
    const p=transport(11);change(p);const r=replay(p);
    assert.equal(r.accepted,false,'accepted hostile '+name);
    hostiles.push({name,accepted:r.accepted,reason:r.reason});
  };
  reject('single_source_literal_corruption',p=>{p.records.find(x=>x.kind==='SOURCE').c[0]*=-1});
  reject('source_provenance_corruption',p=>{p.records.find(x=>x.kind==='SOURCE').source=3});
  reject('gate_input_incomplete_transport',p=>{p.gate_defs[0][2]*=-1});
  reject('resolution_pivot_incomplete_transport',p=>{p.records.find(x=>x.kind==='RES').pivot*=-1});
  reject('duplicate_paid_output_wire',p=>{p.gate_defs[1][1]=p.gate_defs[0][1]});
  reject('undercharge',p=>{p.summary.paid_total--});
  const out={
    id:'LSPV3_572',status:'PROVED_RESTRICTED_PLUS_COMPUTATIONAL_OS_REPLAY',
    checker_sha:SHA.checker,seed_sha:SHA.seed,
    exact_scope:'archived /386 SOURCE/DEF/RES checker, NOT R_mix341',
    originalGraph:seed.spec,cycleDimension:E-V+1,
    sourceFixedGroupSize:positive.length,allMasks:cases.length,
    accepted:positive.length,rejected:cases.length-positive.length,
    masks:positive,workEachAccepted:53,recordsEachAccepted:74,
    assertionsEachAccepted:4663,originalCLINegativeControlsEachAccepted:11,
    hostiles, cases,
    evidenceNotes:'Actual OS Node subprocess replays original archived checker. Time/peak-space not inferred from logical work.'
  };
  if(process.argv.includes('--write-raw')){
    fs.writeFileSync(path.join(ROOT,TARGET),JSON.stringify(out,null,2)+'\n');
  }
  process.stdout.write(JSON.stringify(out,null,2)+'\n');
}finally{fs.rmSync(temp,{recursive:true,force:true})}
