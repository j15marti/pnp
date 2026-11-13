#!/usr/bin/env node
'use strict';
// LSPV-2/589. Deterministic constructor invoking the UNCHANGED archived /386
// original checker. This runner is not a reconstructed historical R_mix341 checker.
const fs=require('fs'),path=require('path'),os=require('os'),
 cp=require('child_process'),crypto=require('crypto'),assert=require('assert');
const root=path.resolve(__dirname,'../..');
const chk=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const base=path.join(root,'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json');
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const c=fs.readFileSync(chk),b=fs.readFileSync(base);
assert.equal(sha(c),'22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113');
assert.equal(sha(b),'0d8b1894f91d00c554727a92fed35b2bb58f2b1602f2a3cfcb949effda43ceb0');
const seed=JSON.parse(b),src=seed.records.filter(r=>r.kind==='SOURCE'),
 res=seed.records.filter(r=>r.kind==='RES');
assert.equal(src.length,17);assert.equal(res.length,28);
const norm=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
function build(k,j){
 assert(k>=3&&k%2===1&&j>=0&&j<k);
 const E=6*k,g=E+1,z=E+2,edges=[],charge=[];
 for(let t=0;t<k;t++){
  for(const [u,v] of seed.spec.edges)edges.push([u+4*t,v+4*t]);
  charge.push(1,0,0,0);
 }
 const lit=(x,t)=>Math.sign(x)*(Math.abs(x)===7?g:Math.abs(x)+6*t);
 const records=[];
 for(let t=0;t<k;t++)for(let i=0;i<16;i++)
  records.push({kind:'SOURCE',c:norm(src[i].c.map(x=>lit(x,t))),
   parents:[],source:src[i].source+4*t});
 records.push({kind:'SOURCE',c:[g],parents:[],source:-1});
 const baseIndex=records.length;
 const index=p=>p===16?16*k:p<16?16*j+p:baseIndex+p-17;
 for(const r of res)records.push({kind:'RES',
  c:norm(r.c.map(x=>lit(x,j))),parents:r.parents.map(index),pivot:lit(r.pivot,j)});
 return {spec:{h:4*k,edges,charge,guard:g},gate_defs:[[0,z,1,4]],
  records,summary:{source:16*k+1,def_views:0,resolution:28,
   paid_gates:1,paid_total:29,live_records:records.length}};
}
function cone(d){
 const seen=new Set(),q=[d.records.length-1];
 while(q.length){const i=q.pop();if(seen.has(i))continue;seen.add(i);
  q.push(...d.records[i].parents);}
 return [...seen].filter(i=>d.records[i].kind==='SOURCE').sort((a,b)=>a-b);
}
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2-589-')),cases=[];
function check(name,d,want){
 const bytes=Buffer.from(JSON.stringify(d)+'\n'),file=path.join(temp,'c'+cases.length+'.json');
 fs.writeFileSync(file,bytes);
 const p=cp.spawnSync(process.execPath,[chk,file],{encoding:'utf8',timeout:30000,maxBuffer:5e6});
 if(p.error)throw p.error;
 const ok=p.status===0;assert.equal(ok,want,name+': '+p.stderr);
 const a=ok?JSON.parse(p.stdout):null;
 const row={name,accepted:ok,bytes:bytes.length,sha256:sha(bytes),
  assertions:a?.assertions??null,nativeNegatives:a?.negativeTests??null};
 cases.push(row);fs.unlinkSync(file);return row;
}
try {
 const families={};
 for(const k of [3,5]){
  const proofs=[];
  for(let j=0;j<k;j++){
   const d=build(k,j),used=cone(d);
   assert.deepEqual(used,Array.from({length:16},(_,i)=>16*j+i).concat([16*k]));
   const row=check('k'+k+'_component'+j,d,true);
   proofs.push({component:j,used,sha256:row.sha256});
   if(k===3){
    const expected=[4993,5078,5126][j];
    assert.equal(row.bytes,expected);
   }
  }
  const intersection=proofs.reduce((s,x)=>s.filter(a=>x.used.includes(a)),proofs[0].used);
  assert.deepEqual(intersection,[16*k]);
  families[k]={originalSourceCount:16*k+1,smallestUnsatCore:17,
   sharedConeSource:intersection,proofs};
 }
 const negatives=[
  ['forged_SOURCE',d=>{d.records[0].c=[-d.spec.guard]}],
  ['bad_pivot',d=>{d.records.at(-1).pivot=123456}],
  ['cross_component_parent',d=>{d.records.find(r=>r.kind==='RES').parents[0]=16}],
  ['underpaid',d=>{d.summary.paid_total--}],
  ['missing_SOURCE',d=>{d.records.splice(20,1);d.summary.source--;d.summary.live_records--}],
  ['bad_sink',d=>{d.records.at(-1).c=[d.spec.guard]}]
 ];
 for(const [name,change] of negatives){const d=build(3,0);change(d);check(name,d,false);}
 const result={schema:'LSPV2-589-SOURCE-FIXED-OR/v1',
  checker_sha256:sha(c),seed_sha256:sha(b),node:process.version,
  families,cases,totals:{accepted:cases.filter(x=>x.accepted).length,
   rejected:cases.filter(x=>!x.accepted).length,
   assertions:cases.reduce((s,x)=>s+(x.assertions||0),0)}};
 assert.deepEqual(result.totals,{accepted:8,rejected:6,assertions:59000});
 const dest=process.argv[2]||path.join(root,'results/raw/arc/2026-11-12_2035_LSPV2_589_FIXED_SOURCE_OR_CORE_REPLAY.json');
 fs.writeFileSync(dest,JSON.stringify(result,null,2)+'\n');
 console.log(JSON.stringify({status:'PASS',totals:result.totals,output:dest}));
}finally{fs.rmSync(temp,{recursive:true,force:true});}
