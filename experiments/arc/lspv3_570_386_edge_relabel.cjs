#!/usr/bin/env node
'use strict';
// LSPV-3/570 exact original /386 checker external-process differential.
// From repo root: node experiments/arc/lspv3_570_386_edge_relabel.cjs [--write]
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),cp=require('node:child_process');
const crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedPath=path.join(root,'results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json');
const witnessPath=path.join(root,'results/raw/arc/2026-11-11_0624_LSPV3_570_REVERSE_EDGE_NATIVE_PACKET.json');
const outputPath=path.join(root,'results/raw/arc/2026-11-11_0624_LSPV3_570_386_EDGE_PERMUTATION_OS_NODE_RAW.json');
function blob(s){return crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+Buffer.byteLength(s)+'\0'),Buffer.from(s)])).digest('hex')}
const checkerText=fs.readFileSync(checker,'utf8'),seedText=fs.readFileSync(seedPath,'utf8');
assert.equal(blob(checkerText),'338305c0ce101704205e57543756b8127074a986');
assert.equal(blob(seedText),'08aa169b5db49b2ddd1cb5a9b6890fcc3b790916');
const seed=JSON.parse(seedText),E=seed.spec.edges.length;
const key=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function rename(o,p){
 assert.equal(p.length,E);assert.equal(new Set(p).size,E);
 const z=JSON.parse(JSON.stringify(o)),edges=z.spec.edges.slice();
 for(let i=0;i<E;i++)z.spec.edges[p[i]]=edges[i];
 const lit=x=>Math.abs(x)<=E?Math.sign(x)*(p[Math.abs(x)-1]+1):x;
 for(const d of z.gate_defs){d[2]=lit(d[2]);d[3]=lit(d[3]);}
 for(const r of z.records){r.c=key(r.c.map(lit));if(r.kind==='RES')r.pivot=lit(r.pivot);}
 return z;
}
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-570-'));
function native(o){
 const fn=path.join(tmp,'packet.json');fs.writeFileSync(fn,JSON.stringify(o));
 const v=cp.spawnSync(process.execPath,[checker,fn],{encoding:'utf8',timeout:10000,maxBuffer:10000000});
 if(v.error)throw v.error;
 if(v.status===0){const a=JSON.parse(v.stdout);return {accepted:true,checks:a.assertions,work:a.paid};}
 return {accepted:false,error:(v.stderr||v.stdout).trim().split('\n').at(-1)};
}
let perms=[[...Array(E).keys()],Array.from({length:E},(_,i)=>E-1-i)],state=0x5700611;
function rand(){state^=state<<13;state^=state>>>17;state^=state<<5;return state>>>0;}
for(let t=0;t<30;t++){let p=[...Array(E).keys()];for(let i=E-1;i>0;i--){let j=rand()%(i+1);[p[i],p[j]]=[p[j],p[i]];}perms.push(p);}
let good=[],failures=[];
try{
 for(let i=0;i<perms.length;i++){
  const p=perms[i],q=rename(seed,p),inv=p.map((_,j)=>p.indexOf(j)),r=native(q);
  assert(r.accepted);assert.equal(r.work,53);assert.equal(r.checks,4663);
  assert.equal(JSON.stringify(rename(q,inv)),JSON.stringify(seed));
  good.push({i,p,ok:true,assertions:r.checks,paid:r.work,roundtrip:true,bytes:Buffer.byteLength(JSON.stringify(q))});
 }
 const reversed=rename(seed,perms[1]);assert.equal(fs.readFileSync(witnessPath,'utf8'),JSON.stringify(reversed));
 const cases=[
  ['edges_only',q=>q.spec.edges=reversed.spec.edges],
  ['records_only',q=>{q.records=reversed.records;q.gate_defs=reversed.gate_defs;}],
  ['charge',q=>{q.spec.charge[0]=0;q.spec.charge[1]=1;}],
  ['source_sign',q=>{q.records[0].c[0]*=-1;q.records[0].c=key(q.records[0].c);}],
  ['facet',q=>q.records.find(r=>r.kind==='DEF').c[0]*=-1],
  ['pivot',q=>q.records.find(r=>r.kind==='RES').pivot=99],
  ['underpay',q=>q.summary.paid_total--],
  ['fake_LOCAL_CONVERT',q=>q.records.find(r=>r.kind==='RES').kind='LOCAL-CONVERT']
 ];
 for(const [name,change] of cases){let q=JSON.parse(JSON.stringify(seed));change(q);
  const r=native(q);assert(!r.accepted,'corrupted accepted: '+name);failures.push({name,...r});}
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
const result={run:'LSPV3-570 real Node OS process',node:process.version,checker_blob:blob(checkerText),seed_blob:blob(seedText),
 positive:good.length,unique_perms:new Set(perms.map(p=>p.join(','))).size,inverse_roundtrips:good.length,
 hostiles_rejected:failures.length,work:53,positive_cases:good,hostile_cases:failures};
if(process.argv.includes('--write'))fs.writeFileSync(outputPath,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
