#!/usr/bin/env node
'use strict';
// LSPV-1/564: deterministic local normal-form witness; Node >= 18.
// Run: node experiments/arc/lspv1_564_gate_bridge_elimination.cjs
// No internet or external dependencies. Checks original /386 checker unmodified.
// Not a replay of the missing historical full R_mix341 checker.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const os=require('node:os');
const path=require('node:path');
const crypto=require('node:crypto');
const cp=require('node:child_process');
const repo=path.resolve(__dirname,'../..');
const source=path.join(repo,'results/raw/arc/2026-11-10_2124_LSPV3_561_ARCHIVED_386_NATIVE_PACKET.json');
const verifier=path.join(repo,'experiments/arc/lspv2_386_independent_verify.js');
const published=path.join(repo,'results/raw/arc/2026-11-10_2200_LSPV1_564_GATE_BRIDGE_ELIMINATED_PACKET.json');
function blobsha(b){return crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex');}
assert.equal(blobsha(fs.readFileSync(source)),'d0fa96a155672f8f6a6a3428eacafa15e79b9e88','input certificate changed');
assert.equal(blobsha(fs.readFileSync(verifier)),'338305c0ce101704205e57543756b8127074a986','original checker changed');
const original=JSON.parse(fs.readFileSync(source,'utf8'));
const clone=x=>JSON.parse(JSON.stringify(x));
const eq=(a,b)=>assert.deepEqual(a,b);
function eliminate(p){
  eq(p.summary,{source:17,def_views:3,resolution:49,paid_gates:1,paid_total:50,live_records:69});
  eq(p.gate_defs,[[0,8,1,2]]);
  const rr=p.records;
  assert.equal(rr.length,69);
  eq(rr[1],{kind:'SOURCE',c:[-1,-2,3,-7],parents:[],source:0});
  eq(rr[17],{kind:'DEF',c:[1,-8],parents:[],gate:0});
  eq(rr[18],{kind:'DEF',c:[2,-8],parents:[],gate:0});
  eq(rr[19],{kind:'DEF',c:[-1,-2,8],parents:[],gate:0});
  eq(rr[20],{kind:'RES',c:[-2,3,-7,-8],parents:[17,1],pivot:1});
  eq(rr[21],{kind:'RES',c:[-1,-2,3,-7],parents:[19,20],pivot:8});
  for(let i=22;i<rr.length;i++){
    assert(!rr[i].c.includes(8)&&!rr[i].c.includes(-8),'gate variable escapes bridge');
    assert(rr[i].parents.every(j=>![17,18,19,20].includes(j)),'other surviving bridge user');
  }
  const removed=new Set([17,18,19,20,21]),oldToNew=new Map(),out=[];
  for(let i=0;i<rr.length;i++)if(!removed.has(i)){oldToNew.set(i,out.length);out.push(clone(rr[i]));}
  for(const r of out)r.parents=r.parents.map(i=>{
    const j=(i===21?oldToNew.get(1):oldToNew.get(i));
    assert.notEqual(j,undefined,'unmapped proof parent');return j;
  });
  const result={spec:clone(p.spec),gate_defs:[],records:out,
    summary:{source:17,def_views:0,resolution:47,paid_gates:0,paid_total:47,live_records:64}};
  return result;
}
function ancestry(p){
  const seen=new Set();
  function visit(i){if(seen.has(i))return;seen.add(i);for(const j of p.records[i].parents)visit(j);}
  visit(p.records.length-1);
  return {all:[...seen].length,source:[...seen].filter(i=>p.records[i].kind==='SOURCE').length,
    paidRes:[...seen].filter(i=>p.records[i].kind==='RES').length,dead:p.records.length-seen.size};
}
const optimized=eliminate(original);
eq(ancestry(original),{all:68,source:17,paidRes:49,dead:1});
eq(ancestry(optimized),{all:64,source:17,paidRes:47,dead:0});
assert(fs.readFileSync(published,'utf8')===JSON.stringify(optimized)+'\n','published packet differs');
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-lspv1-564-'));
function run(packet,accept,name){
  const file=path.join(dir,name+'.json');
  fs.writeFileSync(file,JSON.stringify(packet)+'\n');
  try {
    const stdout=cp.execFileSync(process.execPath,[verifier,file],{encoding:'utf8',stdio:['ignore','pipe','pipe'],timeout:30000});
    assert.equal(accept,true,'unexpected native acceptance of '+name);
    return {name,accepted:true,native:JSON.parse(stdout)};
  }catch(e){
    if(e instanceof assert.AssertionError)throw e;
    assert.equal(accept,false,'unexpected native rejection of '+name+': '+String(e.stderr));
    return {name,accepted:false,error:String(e.stderr||e.message).split('\n').slice(0,3).join(' ')};
  }
}
try{
  const tests=[run(original,true,'original'),run(optimized,true,'optimized')];
  let c=clone(optimized);c.summary.paid_total=50;tests.push(run(c,false,'wrong_charge'));
  c=clone(optimized);c.records[18].parents[1]=21;tests.push(run(c,false,'unmapped_parent'));
  c=clone(optimized);c.records[17].pivot=1;tests.push(run(c,false,'bad_pivot'));
  c=clone(optimized);c.records[1].c[0]=1;tests.push(run(c,false,'bad_source'));
  c=clone(optimized);c.records[18].c=[1];tests.push(run(c,false,'bad_resolvent'));
  console.log(JSON.stringify({result:'PASS',old_paid:50,new_paid:47,removed_paid:3,
    old_ancestry:ancestry(original),new_ancestry:ancestry(optimized),
    archived_checker_blob:blobsha(fs.readFileSync(verifier)),
    original_packet_blob:blobsha(fs.readFileSync(source)),
    new_packet_blob:blobsha(fs.readFileSync(published)),
    new_packet_sha256:crypto.createHash('sha256').update(fs.readFileSync(published)).digest('hex'),
    negative_controls:5,tests},null,2));
}finally{fs.rmSync(dir,{recursive:true,force:true});}
