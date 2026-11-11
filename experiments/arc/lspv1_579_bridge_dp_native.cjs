#!/usr/bin/env node
'use strict';
/* LSPV-1/579, deterministic same-source guarded-bridge /386 refutation.
 * Run at repository root:
 *   node experiments/arc/lspv1_579_bridge_dp_native.cjs
 * The source and original historical sibling checker are pinned by Git blob/SHA256.
 * This DOES NOT authenticate the full R_mix341 mixed calculus.
 */
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const cp=require('child_process'),assert=require('assert/strict'),os=require('os');
const root=process.cwd();
const seedFile=path.join(root,'results/raw/arc/2026-11-11_0900_LSPV1_575_BRIDGE_GUARDED_DP_NATIVE_ACCEPTED.json');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const target=process.argv[2]||path.join(root,'results/raw/arc/2026-11-11_1200_LSPV1_579_BRIDGE_DP_W61.json');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const gitsha=b=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex');
assert.equal(gitsha(fs.readFileSync(seedFile)),'d5de0f477cd736ec5fd7b01be18350f9cb594fd2');
assert.equal(gitsha(fs.readFileSync(checker)),'338305c0ce101704205e57543756b8127074a986');
assert.equal(sha(fs.readFileSync(checker)),'22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113');
const old=JSON.parse(fs.readFileSync(seedFile,'utf8'));
const source=old.records.filter(x=>x.kind==='SOURCE');
assert.equal(source.length,41);
const canon=x=>[...new Set(x)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const key=x=>JSON.stringify(x);
const lex=(a,b)=>{for(let i=0;i<Math.min(a.length,b.length);i++)if(a[i]!==b[i])return a[i]-b[i];return a.length-b.length};
const records=source.map(r=>({...r,parents:[]}));
const by=new Map(records.map((r,i)=>[key(r.c),i]));
let active=new Set(by.keys());
const order=[12,10,14,13,11,8,9,4,6,3,5,7,1,2,15,16];
for(const pivot of order){
 const pos=[...active].map(k=>JSON.parse(k)).filter(c=>c.includes(pivot)).sort(lex);
 const neg=[...active].map(k=>JSON.parse(k)).filter(c=>c.includes(-pivot)).sort(lex);
 const nxt=new Set([...active].filter(k=>{let c=JSON.parse(k);return !c.includes(pivot)&&!c.includes(-pivot)}));
 for(const A of pos)for(const B of neg){
  const tmp=new Set([...A,...B]);tmp.delete(pivot);tmp.delete(-pivot);
  if([...tmp].some(x=>tmp.has(-x)))continue;
  const C=canon([...tmp]),k=key(C);
  if(!by.has(k)){by.set(k,records.length);records.push({kind:'RES',c:C,parents:[by.get(key(A)),by.get(key(B))],pivot})}
  nxt.add(k);
 }
 active=nxt;
 if(active.has('[]'))break;
}
assert(by.has('[]'));
const seen=new Set,stack=[by.get('[]')];
while(stack.length){
 const x=stack.pop();if(seen.has(x))continue;
 seen.add(x);stack.push(...records[x].parents);
}
const kept=[...new Set([...Array(source.length).keys(),...seen])].sort((a,b)=>a-b);
const id=new Map(kept.map((j,i)=>[j,i]));
const pr=kept.map(j=>({...records[j],parents:records[j].parents.map(p=>id.get(p))}));
const nres=pr.filter(r=>r.kind==='RES').length;
assert.equal(nres,60);assert.equal(pr.length,101);assert.deepEqual(pr.slice(0,41),source);
assert.deepEqual(pr.at(-1).c,[]);
const packet={spec:old.spec,gate_defs:[[0,17,1,2]],records:pr,
 summary:{source:41,resolution:nres,def_views:0,paid_gates:1,paid_total:61,live_records:pr.length}};
const bytes=Buffer.from(JSON.stringify(packet)+'\n');
assert.equal(bytes.length,6523);
assert.equal(sha(bytes),'56934e9b2cd910615fc99dfcacf6411cf2a65a1ea9d46bfc5de1549a837cc6d8');
assert.equal(gitsha(bytes),'807aaf7b7cf5e4a4feb29c2599f9e582ea140e30');
fs.mkdirSync(path.dirname(target),{recursive:true});
fs.writeFileSync(target,bytes);
const run=p=>cp.spawnSync(process.execPath,[checker,p],{encoding:'utf8',timeout:10000});
const valid=run(target);
assert.equal(valid.status,0,'original verifier failed: '+valid.stderr);
const output=JSON.parse(valid.stdout.trim().split('\n').at(-1));
assert.equal(output.paid,61);assert.equal(output.res,60);assert.equal(output.def,1);
assert.equal(output.sources,41);assert.equal(output.records,101);
assert.equal(output.negativeTests,11);
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv1-579-'));
const controls={
 wrong_source:q=>q.records[0].c[0]=-q.records[0].c[0],
 wrong_pivot:q=>q.records.at(-1).pivot=999999,
 underpayment:q=>q.summary.paid_total=60,
 future_parent:q=>q.records.at(-1).parents[0]=102,
 wrong_terminal:q=>q.records.at(-1).c=[16]
};
const negatives={};
try{
 for(const [name,edit] of Object.entries(controls)){
  const q=JSON.parse(bytes.toString());edit(q);
  const f=path.join(temp,name+'.json');fs.writeFileSync(f,JSON.stringify(q)+'\n');
  const r=run(f);negatives[name]=r.status!==0;
  assert.equal(negatives[name],true,'hostile variant accepted: '+name);
 }
}finally{fs.rmSync(temp,{force:true,recursive:true})}
console.log(JSON.stringify({status:'PASS',id:'LSPV-1/579',scope:'archived /386 only',
 old_paid:63,new_paid:61,new_resolution:60,original_source_clauses:41,records:101,
 target_sha256:sha(bytes),original_checker_git_blob:gitsha(fs.readFileSync(checker)),
 original_checker_sha256:sha(fs.readFileSync(checker)),original_verifier:output,
 five_hostile_controls:negatives,order},null,2));
