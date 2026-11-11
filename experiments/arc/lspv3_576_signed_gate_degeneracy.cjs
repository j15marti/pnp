#!/usr/bin/env node
'use strict';
// LSPV-3/576 reproducible original archived /386 native OS replay.
// Run from the repository root: node experiments/arc/lspv3_576_signed_gate_degeneracy.cjs [output.json]
// No installation or third-party package required.
const assert=require('node:assert/strict');
const cp=require('node:child_process'),fs=require('node:fs'),path=require('node:path');
const os=require('node:os'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seed=path.join(root,'results/raw/arc/2026-11-11_0224_LSPV3_566_K4x3_CLI_ACCEPTED_PACKET.json');
const base=JSON.parse(fs.readFileSync(seed,'utf8'));
const key=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const clone=x=>JSON.parse(JSON.stringify(x));
function variant(mode){
 const p=clone(base),z=20,a=1,b=mode==='constant'?-1:mode==='alias'?1:4;
 assert.deepEqual(p.gate_defs,[[0,20,1,4]]);
 p.gate_defs[0]=[0,z,a,b];
 let facets=[[-z,a],[-z,b],[z,-a,-b]].map(key).filter(c=>!c.some(x=>c.includes(-x)));
 facets=[...new Map(facets.map(c=>[JSON.stringify(c),c])).values()];
 const at=p.records.length-1,added=facets.map(c=>({kind:'DEF',c,parents:[],gate:0}));
 if(mode==='constant'){
  added.push({kind:'RES',c:[-z],parents:[at+facets.findIndex(c=>c.includes(1)),at+facets.findIndex(c=>c.includes(-1))],pivot:1});
 }
 p.records.splice(at,0,...added);
 p.summary.def_views+=facets.length;
 p.summary.resolution+=Number(mode==='constant');
 p.summary.paid_total+=Number(mode==='constant');
 p.summary.live_records+=added.length;
 assert.deepEqual(p.spec,base.spec); // entire original spec stays fixed
 assert.deepEqual(p.records.filter(r=>r.kind==='SOURCE'),base.records.filter(r=>r.kind==='SOURCE'));
 return {p,facets};
}
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp576-'));
function native(label,p,expected){
 const raw=Buffer.from(JSON.stringify(p)),f=path.join(temp,label+'.json');fs.writeFileSync(f,raw);
 const result=cp.spawnSync(process.execPath,[checker,f],{encoding:'utf8',timeout:30000,maxBuffer:1<<20});
 if(result.error)throw result.error;
 const accepted=result.status===0;
 assert.equal(accepted,expected,label+': '+(result.stderr||result.stdout).slice(0,300));
 return {label,accepted,bytes:raw.length,sha256:crypto.createHash('sha256').update(raw).digest('hex'),
  ...(accepted?JSON.parse(result.stdout):{error:result.stderr.trim().slice(0,240)})};
}
try{
 const tests=[native('baseline',base,true)];
 const modes=['constant','alias','ordinary'];
 for(const mode of modes){const v=variant(mode);tests.push({mode,facets:v.facets,...native(mode,v.p,true)});}
 const v=variant('constant').p;
 const mutations=[
  ['underpaid',x=>{x.summary.paid_total--}],
  ['wrong_facet',x=>{x.records[x.records.length-4].c=[2,-20]}],
  ['wrong_pivot',x=>{x.records[x.records.length-2].pivot=4}],
  ['future_parent',x=>{x.records[x.records.length-2].parents[0]=x.records.length+5}],
  ['forged_source',x=>{x.records[0].c=[1,2,3,19]}]
 ];
 for(const [name,f] of mutations){let x=clone(v);f(x);tests.push(native(name,x,false));}
 const output={run:'LSPV-3/576',checker:'experiments/arc/lspv2_386_independent_verify.js',
  scope:'archived /386 grammar, NOT complete R_mix341',tests,positives:4,hostile_rejections:5,
  final_status:'P2-D1/P2-C3/P2-B1/B2/B3 OPEN; P versus NP OPEN'};
 const outputPath=process.argv[2];if(outputPath)fs.writeFileSync(outputPath,JSON.stringify(output,null,2)+'\n');
 console.log(JSON.stringify(output,null,2));
}finally{fs.rmSync(temp,{recursive:true,force:true});}
