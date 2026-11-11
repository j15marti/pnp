#!/usr/bin/env node
'use strict';
// LSPV-3/571 fixed-source, charge-stabilizing graph automorphism.
// Run from j15marti/pnp root:
// node experiments/arc/lspv3_571_fixed_source_automorphism.cjs [--write]
// This executes the UNCHANGED original archived /386 CLI as an OS subprocess.
// It is a reproducer, not a replacement checker and not a complete R_mix341 parser.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const cp=require('node:child_process'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const originalPath=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedPath=path.join(root,'results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json');
const outPath=path.join(root,'results/raw/arc/2026-11-11_0724_LSPV3_571_SOURCE_FIXED_AUTOMORPHISM_OS_RAW.json');
const witnessPath=path.join(root,'results/raw/arc/2026-11-11_0724_LSPV3_571_FIXED_SOURCE_K4_TRANSPOSITION_PACKET.json');
function blob(s){return crypto.createHash('sha1').update(Buffer.concat([
 Buffer.from('blob '+Buffer.byteLength(s)+'\0'),Buffer.from(s)])).digest('hex');}
const checker=fs.readFileSync(originalPath,'utf8');
const source=fs.readFileSync(seedPath,'utf8');
assert.equal(blob(checker),'338305c0ce101704205e57543756b8127074a986');
assert.equal(blob(source),'08aa169b5db49b2ddd1cb5a9b6890fcc3b790916');
const seed=JSON.parse(source),clone=x=>JSON.parse(JSON.stringify(x));
const canon=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function perms(a){return a.length?a.flatMap((x,i)=>perms(a.filter((_,j)=>i!==j)).map(p=>[x,...p])):[[]];}
function transform(p,mode='all'){
 const q=clone(seed),edges=q.spec.edges,E=edges.length;
 const eperm=edges.map(([u,v])=>edges.findIndex(([a,b])=>a===Math.min(p[u],p[v])&&b===Math.max(p[u],p[v])));
 assert(!eperm.includes(-1),'not an automorphism');
 const lit=x=>Math.abs(x)<=E?Math.sign(x)*(eperm[Math.abs(x)-1]+1):x;
 for(const r of q.records){
  if(mode!=='proof_only'&&r.kind==='SOURCE'){
   r.c=canon(r.c.map(lit));
   if(r.source>=0&&mode!=='literal_only')r.source=p[r.source];
  }
  if(mode!=='source_only'&&r.kind!=='SOURCE'){
   r.c=canon(r.c.map(lit));
   if(r.kind==='RES')r.pivot=lit(r.pivot);
  }
 }
 if(mode!=='source_only')for(const d of q.gate_defs){d[2]=lit(d[2]);d[3]=lit(d[3]);}
 return q;
}
function sourceMultiset(p){return p.records.filter(r=>r.kind==='SOURCE')
 .map(r=>String(r.source)+':'+JSON.stringify(r.c)).sort().join('|');}
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-lspv3-571-'));
function native(o){
 const f=path.join(tmp,'packet.json');fs.writeFileSync(f,JSON.stringify(o));
 const run=cp.spawnSync(process.execPath,[originalPath,f],{encoding:'utf8',timeout:10000,maxBuffer:10000000});
 if(run.error)throw run.error;
 if(run.status===0){const x=JSON.parse(run.stdout);return {accepted:true,assertions:x.assertions,paid:x.paid};}
 return {accepted:false,error:(run.stderr||run.stdout).trim().split('\n').at(-1)};
}
let rows=[],hostiles=[];
try {
 const baseline=native(seed);assert(baseline.accepted&&baseline.paid===53);
 for(const rest of perms([1,2,3])){
  const p=[0,...rest],q=transform(p),r=native(q);
  assert(r.accepted,'original rejected '+p);
  assert.equal(r.assertions,4663);assert.equal(r.paid,53);
  assert.equal(JSON.stringify(q.spec),JSON.stringify(seed.spec));
  assert.equal(sourceMultiset(q),sourceMultiset(seed));
  rows.push({vertex_permutation:p,...r,bytes:Buffer.byteLength(JSON.stringify(q)),
   same_spec:true,same_source_clause_multiset:true});
 }
 const witness=transform([0,3,2,1]);
 assert.equal(fs.readFileSync(witnessPath,'utf8'),JSON.stringify(witness));
 const changes=[
  ['source_only',()=>transform([0,3,2,1],'source_only')],
  ['proof_only',()=>transform([0,3,2,1],'proof_only')],
  ['signed_literals_only',()=>transform([0,3,2,1],'literal_only')],
  ['charge_nonstabilizer',()=>transform([1,0,2,3])],
  ['bad_pivot',()=>{const x=transform([0,3,2,1]);x.records.find(r=>r.kind==='RES').pivot=123;return x;}],
  ['wrong_source',()=>{const x=transform([0,3,2,1]);const r=x.records.find(r=>r.kind==='SOURCE'&&r.source>=0);r.c=canon(r.c.map((v,i)=>i?-v*0+v:-v));return x;}],
  ['underpaid',()=>{const x=transform([0,3,2,1]);x.summary.paid_total--;return x;}],
  ['foreign_LOCAL_CONVERT',()=>{const x=transform([0,3,2,1]);x.records.find(r=>r.kind==='RES').kind='LOCAL-CONVERT';return x;}]
 ];
 for(const [name,make] of changes){const r=native(make());assert(!r.accepted,'accepted hostile '+name);hostiles.push({name,...r});}
} finally {fs.rmSync(tmp,{recursive:true,force:true});}
const raw={run:'LSPV-3/571 OS Node reproducibility',model:'archived /386 original full CLI only',
 source_blob:blob(source),checker_blob:blob(checker),
 positives:rows.length,hostiles_rejected:hostiles.length,paid:53,source_fixed:true,
 proof_context:'unscoped /386 shared DAG, not full historical R_mix341',
 results:rows,hostiles};
if(process.argv.includes('--write'))fs.writeFileSync(outPath,JSON.stringify(raw,null,2)+'\n');
console.log(JSON.stringify(raw,null,2));
