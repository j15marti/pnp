#!/usr/bin/env node
'use strict';
// LSPV-4/541: archived /386 read-only certificate rescan firewall.
// Run from a checkout: node experiments/arc/lspv4_541_archived_386_rescan_firewall.cjs
// Executes the UNMODIFIED original checker as a separate OS Node process.
// A second independent RES/facet auditor indexes the input packet directly
// without retaining or recomputing derived clauses.
// It is NOT a physical logarithmic-space implementation: JSON.parse holds
// the complete read-only certificate in ordinary host memory.
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const cp=require('node:child_process'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const packet=path.join(root,'results/raw/arc/2026-11-11_0336_LSPV4_540_OWNER_FACET_CROSS_CONE_ACCEPTED.json');
const base=JSON.parse(fs.readFileSync(packet,'utf8'));
const clone=x=>JSON.parse(JSON.stringify(x));
const key=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const good=c=>Array.isArray(c)&&c.every(x=>Number.isSafeInteger(x)&&x!==0)
  &&!c.some(x=>c.includes(-x))&&eq(c,key(c));
function prefixFreeFacets(origin,k){
 const d=clone(origin),extra=Array.from({length:k},
   ()=>({kind:'DEF',gate:0,c:[1,-8],parents:[]}));
 d.records=[...extra,...d.records];
 for(const r of d.records.slice(k))
   if(r.kind==='RES')r.parents=r.parents.map(j=>j+k);
 d.summary.def_views+=k;d.summary.live_records+=k;
 return d;
}
function noCacheStepAudit(d){
 let res=0,facets=0,sources=0,refs=0;
 for(let i=0;i<d.records.length;i++){
  const r=d.records[i];
  assert.ok(good(r.c),'noncanonical clause');
  assert.ok(Array.isArray(r.parents)&&r.parents.every(j=>Number.isInteger(j)&&j>=0&&j<i),
    'chronological parents');
  if(r.kind==='SOURCE'){sources++;assert.equal(r.parents.length,0);}
  else if(r.kind==='DEF'){
   facets++;assert.equal(r.parents.length,0);
   const gd=d.gate_defs.find(x=>x[0]===r.gate);
   assert.ok(gd,'missing paid owner');
   const [,z,a,b]=gd;
   assert.ok([[-z,a],[-z,b],[z,-a,-b]].map(key).filter(good)
     .some(c=>eq(c,r.c)),'invalid facet');
  }else if(r.kind==='RES'){
   res++;refs+=2;assert.equal(r.parents.length,2);
   const A=d.records[r.parents[0]].c,B=d.records[r.parents[1]].c,p=r.pivot;
   assert.ok(Number.isInteger(p)&&p!==0&&A.includes(p)&&B.includes(-p),'bad pivot');
   const out=key([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)]);
   assert.ok(good(out)&&eq(out,r.c),'bad resolvent');
  }else throw Error('bad record kind');
 }
 assert.equal(sources,d.summary.source);
 assert.equal(facets,d.summary.def_views);
 assert.equal(res,d.summary.resolution);
 assert.equal(res+d.gate_defs.length,d.summary.paid_total);
 assert.equal(d.records.length,d.summary.live_records);
 assert.deepEqual(d.records.at(-1).c,[]);
 return {source:sources,freeFacets:facets,resolution:res,owners:d.gate_defs.length,
   paid:res+d.gate_defs.length,refs,records:d.records.length};
}
function originalCLI(d,tmp){
 fs.writeFileSync(tmp,JSON.stringify(d));
 const r=cp.spawnSync(process.execPath,[checker,tmp],{encoding:'utf8',maxBuffer:8*1024*1024});
 return {accepted:r.status===0,exit:r.status,
   result:r.status===0?JSON.parse(r.stdout.trim().split('\n').at(-1)):null,
   diagnostic:r.status===0?null:(r.stderr||r.stdout).slice(0,300)};
}
function main(){
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv4-541-'));
 const tmp=path.join(dir,'packet.json'),positive=[],hostile=[];
 try{
  for(const k of [0,1,4,32,128,512]){
   const d=prefixFreeFacets(base,k),payload=JSON.stringify(d);
   const step=noCacheStepAudit(d),native=originalCLI(d,tmp);
   assert.ok(native.accepted,JSON.stringify(native));
   assert.equal(native.result.paid,step.paid);
   assert.equal(native.result.negativeTests,11);
   positive.push({k,bytes:Buffer.byteLength(payload),...step,
     originalCLIAssertions:native.result.assertions});
   const cases=[
    ['bad_pivot',o=>o.records.at(-1).pivot=1000],
    ['bad_facet_owner',o=>o.records.find(r=>r.kind==='DEF').gate=999],
    ['bad_facet_clause',o=>o.records.find(r=>r.kind==='DEF').c=[-1,8]],
    ['forward_parent',o=>o.records.at(-1).parents[0]=99999],
    ['underpaid',o=>o.summary.paid_total++],
    ['changed_source',o=>o.spec.charge[0]=0],
   ];
   for(const [name,mutate] of cases){
    const v=clone(d);mutate(v);let independentRejected=false;
    try{noCacheStepAudit(v);}catch(e){independentRejected=true;}
    const original=originalCLI(v,tmp);
    assert.equal(original.accepted,false,'original accepted '+k+' '+name);
    hostile.push({k,name,originalRejected:true,stepAuditorRejected:independentRejected});
   }
  }
 }finally{fs.rmSync(dir,{recursive:true,force:true});}
 const result={role:'LSPV-4/541',scope:'original /386 OS Node CLI plus no-cache RES/facet step audit',
  accepted:positive.length,originalCLIBuiltInHostiles:positive.length*11,
  externalHostiles:hostile.length,allExternalRejected:hostile.every(x=>x.originalRejected),
  physicalLogspaceMeasured:false,positive,hostile};
 if(process.argv.includes('--write-raw')){
  const dest=path.join(root,'results/raw/arc/LSPV4_541_LOCAL_OS_NODE_REPLAY.json');
  fs.writeFileSync(dest,JSON.stringify(result,null,2)+'\n');
  console.error('WROTE '+dest);
 }
 console.log(JSON.stringify(result,null,2));
}
main();
