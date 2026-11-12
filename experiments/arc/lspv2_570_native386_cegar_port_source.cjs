#!/usr/bin/env node
'use strict';
/* LSPV-2/570. Bounded-corpus executable CEGAR for archived /386 only.
 * This program executes the UNMODIFIED pinned original checker in actual Node OS
 * subprocesses. The abstract stage filters are REFERENCE code, NOT historical.
 * Run at repo root: node experiments/arc/lspv2_570_native386_cegar_port_source.cjs
 * Requires Node >=18, no dependencies.
 */
const fs=require('node:fs'),cp=require('node:child_process'),path=require('node:path'),os=require('node:os'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=process.cwd();
const checkerRel='experiments/arc/lspv2_386_independent_verify.js';
const seedRel='results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json';
const checkerPath=path.join(root,checkerRel),seedPath=path.join(root,seedRel);
function sha256(x){return crypto.createHash('sha256').update(x).digest('hex')}
function blob(x){const b=Buffer.isBuffer(x)?x:Buffer.from(x);return crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex')}
assert.equal(blob(fs.readFileSync(checkerPath)),'338305c0ce101704205e57543756b8127074a986','original checker drift');
assert.equal(blob(fs.readFileSync(seedPath)),'318c52d99977ea4e91bc8554051138a700c1dc94','source-bound seed drift');
const seed=JSON.parse(fs.readFileSync(seedPath,'utf8'));
const externalRel='results/raw/arc/2026-11-11_0812_LSPV2_559_EXTERNAL_K4_SIGNED_SOURCE.cnf';
const external=fs.readFileSync(path.join(root,externalRel));
assert.equal(blob(external),'e8bc4300f1f4518cb447edaf3f699bcee4839803','external source drift');
const sourceLines=external.toString('utf8').trim().split(/\n/);
assert.equal(sourceLines.shift(),'p cnf 7 17');
const externalClauses=sourceLines.map(l=>{
  const lits=l.split(/\s+/).map(Number);assert.equal(lits.pop(),0);return lits;
});
assert.equal(externalClauses.length,17);
assert.deepEqual(seed.records.filter(r=>r.kind==='SOURCE').map(r=>r.c),externalClauses,'actual external source clauses must match seed exactly');
assert.equal(seed.summary.paid_total,29);
const copy=x=>JSON.parse(JSON.stringify(x));
const canon=c=>[...new Set(c)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const bsource=seed.records.filter(x=>x.kind==='SOURCE');
const sourceKey=x=>JSON.stringify([x.source,x.c]);
const sourceHash=sha256(Buffer.from(bsource.map(sourceKey).sort().join('\n')+'\n'));
const externalBytesSHA256=sha256(external);
const externalSpecHash=sha256(Buffer.from(JSON.stringify(seed.spec)));
function variant(name,mutate){const x=copy(seed);mutate(x);return {name,data:x}}
const cases=[
 variant('VALID_W29_ORIGINAL',()=>{}),
 variant('VALID_W29_PAIRED_ORIENTATION',x=>{const r=x.records.at(-1);r.parents.reverse();r.pivot=-r.pivot}),
 variant('VALID_W30_LIVE_DUPLICATE',x=>{
   const prior=x.records.at(-2),last=x.records.at(-1);
   const duplicate=copy(prior);x.records.splice(-1,0,duplicate);last.parents=[last.parents[0],x.records.length-2];
   x.summary.resolution++;x.summary.paid_total++;x.summary.live_records++;
 }),
 variant('INVALID_FORGED_SOURCE_SIGN',x=>{x.records[0].c=[-1,2,3,-7]}),
 variant('INVALID_WRONG_SIGNED_PIVOT',x=>{x.records.at(-1).pivot=-7}),
 variant('INVALID_WRONG_PARENT_ORDER',x=>{x.records.at(-1).parents.reverse()}),
 variant('INVALID_UNDERPAID_RESOLUTION',x=>{x.summary.paid_total--}),
 variant('INVALID_FRESH_OWNER_COLLISION',x=>{x.gate_defs[0][1]=x.spec.guard}),
 variant('INVALID_FORWARD_PARENT',x=>{x.records.at(-1).parents[0]=x.records.length+10})
];
// Each stage is a NECESSARY condition for /386 acceptance at this pinned source.
// Unknown operations of R_mix341 are not modeled or rejected by this program.
function stage(x){
 const ret={A0_MAY:true,A1_SOURCE:false,A2_SIGNED_PORT:false,A3_ACCOUNT_FRESH:false};
 if(!x || !x.spec || !Array.isArray(x.records) || !Array.isArray(x.gate_defs)||!x.summary)return ret;
 const src=x.records.filter(r=>r&&r.kind==='SOURCE');
 const specOK=sha256(Buffer.from(JSON.stringify(x.spec)))===externalSpecHash;
 const sameSrc=src.length===bsource.length && eq(src.map(sourceKey).sort(),bsource.map(sourceKey).sort());
 if(!(specOK&&sameSrc))return ret;ret.A1_SOURCE=true;
 const known=[];
 for(let i=0;i<x.records.length;i++){
  const r=x.records[i];if(!r||!Array.isArray(r.c)||r.c.some(v=>!Number.isSafeInteger(v)||v===0))return ret;
  const cl=canon(r.c);if(!eq(cl,r.c)||cl.some(v=>cl.includes(-v)))return ret;
  if(r.kind==='RES'){
   if(!Array.isArray(r.parents)||r.parents.length!==2||r.parents.some(j=>!Number.isInteger(j)||j<0||j>=i))return ret;
   const [A,B]=r.parents.map(j=>known[j]),p=r.pivot;
   if(!Number.isInteger(p)||p===0||!A.includes(p)||!B.includes(-p))return ret;
   const c=canon([...A.filter(v=>v!==p),...B.filter(v=>v!==-p)]);
   if(c.some(v=>c.includes(-v))||!eq(c,r.c))return ret;
  }
  known.push(r.c);
 }
 ret.A2_SIGNED_PORT=true;
 const {h,edges,charge,guard}=x.spec;
 if(!Number.isInteger(h)||!Array.isArray(edges)||!Array.isArray(charge)||!Number.isSafeInteger(guard))return ret;
 const defs=new Map(),ids=new Set();
 for(const d of x.gate_defs){
  if(!Array.isArray(d)||d.length!==4||!d.every(Number.isSafeInteger))return ret;
  const [id,z,a,b]=d;
  if(id<0||ids.has(id)||z<=edges.length||z===guard||defs.has(z))return ret;
  if([a,b].some(v=>v===0||Math.abs(v)===guard||!(Math.abs(v)<=edges.length||defs.has(Math.abs(v)))))return ret;
  ids.add(id);defs.set(z,id);
 }
 let ns=0,nr=0,nd=0;
 for(let i=0;i<x.records.length;i++){
  const r=x.records[i];
  if(!Array.isArray(r.parents)||r.parents.some(j=>!Number.isInteger(j)||j<0||j>=i))return ret;
  if(r.kind==='SOURCE'){ns++;if(r.parents.length!==0)return ret}
  else if(r.kind==='RES')nr++;
  else if(r.kind==='DEF'){nd++;if(r.parents.length!==0||!ids.has(r.gate))return ret}
  else return ret;
  if(r.c.some(v=>Math.abs(v)>edges.length&&Math.abs(v)!==guard&&!defs.has(Math.abs(v))))return ret;
 }
 if(!eq(x.records.at(-1).c,[]))return ret;
 if(ns!==x.summary.source||nr!==x.summary.resolution||nd!==x.summary.def_views||defs.size!==x.summary.paid_gates||nr+defs.size!==x.summary.paid_total||x.records.length!==x.summary.live_records)return ret;
 ret.A3_ACCOUNT_FRESH=true;return ret;
}
function abstractWork(x){
 const paidGates=new Set();let cost=0;const seen=new Set();
 for(const g of x.gate_defs){if(Array.isArray(g)&&!paidGates.has(g[0])){paidGates.add(g[0]);cost++}}
 for(const r of x.records){if(!r||!Array.isArray(r.c))continue;
  if(r.kind==='RES'){const key=JSON.stringify(r.c);if(!seen.has(key))cost++}
  seen.add(JSON.stringify(r.c));
 }
 return cost;
}
function originalCLI(x,tmp,name){const p=path.join(tmp,name+'.json');const content=JSON.stringify(x)+'\n';fs.writeFileSync(p,content);
 const started=process.hrtime.bigint();const r=cp.spawnSync(process.execPath,[checkerPath,p],{encoding:'utf8',timeout:30000});
 const ms=Number(process.hrtime.bigint()-started)/1e6;
 return {accept:r.status===0,exit:r.status,reason:(r.stderr||'').match(/Error: ([^\n]+)/)?.[1]||(r.status===0?'ACCEPT':'UNKNOWN'),stdout:(r.stdout||'').trim(),bytes:Buffer.byteLength(content),sha256:sha256(Buffer.from(content)),duration_ms:Math.round(ms*1000)/1000};
}
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp570-'));
let results=[];
try{for(const {name,data} of cases){const native=originalCLI(data,tmp,name),abstract=stage(data);const aw=abstractWork(data);const expected=name.startsWith('VALID');
  assert.equal(native.accept,expected,'unexpected exact original-checker result: '+name);
  if(expected){assert(abstract.A3_ACCOUNT_FRESH,'overrestrictive reference stage '+name);assert(aw<=data.summary.paid_total,'cost soundness finite control '+name)}
  results.push({name,expected_accept:expected,concrete_work:data.summary.paid_total,abstract_work:aw,abstract,native});
 }
} finally {fs.rmSync(tmp,{recursive:true,force:true})}
const states=['A0_MAY','A1_SOURCE','A2_SIGNED_PORT','A3_ACCOUNT_FRESH'];
const progression=states.map(stageName=>{
 const feasible=results.filter(r=>r.abstract[stageName]);const spurious=feasible.filter(r=>!r.native.accept);const truePos=feasible.filter(r=>r.native.accept);
 return {stage:stageName,candidates:feasible.length,accepted_native_retained:truePos.length,spurious_witnesses:spurious.map(r=>r.name),min_abstract_work:Math.min(...feasible.map(r=>r.abstract_work))};
});
assert.equal(results.filter(r=>r.native.accept).length,3);
assert.equal(progression[0].candidates,9);
assert.equal(progression.at(-1).candidates,3);
assert(progression.every(p=>p.accepted_native_retained===3));
assert.equal(results.find(r=>r.name==='VALID_W30_LIVE_DUPLICATE').abstract_work,29);
assert.equal(results.find(r=>r.name==='VALID_W30_LIVE_DUPLICATE').concrete_work,30);
const out={run:'LSPV-2/570',scope:'restricted archived /386 SOURCE/DEF/RES only; native CLI executed as independent Node OS subprocess',original_checker_git_blob:'338305c0ce101704205e57543756b8127074a986',seed_git_blob:'318c52d99977ea4e91bc8554051138a700c1dc94',source_multiset_sha256:sourceHash,external_source_git_blob:'e8bc4300f1f4518cb447edaf3f699bcee4839803',external_source_sha256:externalBytesSHA256,source_spec_sha256:externalSpecHash,stage_order:states,progression,cases:results,limitations:['A3 is a necessary-condition filter, not complete historical checker','native operational acceptance is not independent source semantic soundness','missing full R_mix341 operations overapproximated MAY','logical work differs from certificate bytes, construction time, span and peak space']};
const resultRel='results/raw/arc/2026-11-11_1912_LSPV2_570_NATIVE386_CEGAR_OS_RAW.json';const dest=path.join(root,resultRel);fs.mkdirSync(path.dirname(dest),{recursive:true});fs.writeFileSync(dest,JSON.stringify(out,null,2)+'\n');
for(const name of ['VALID_W30_LIVE_DUPLICATE','INVALID_WRONG_SIGNED_PIVOT']){const o=cases.find(x=>x.name===name);const filename='results/raw/arc/2026-11-11_1912_LSPV2_570_'+name+'.json';fs.writeFileSync(path.join(root,filename),JSON.stringify(o.data)+'\n')}
console.log(JSON.stringify({out:resultRel,sourceHash,progression,results:results.map(x=>({name:x.name,native:x.native.accept,work:x.concrete_work,abstract:x.abstract_work,at:x.abstract}))},null,2));
