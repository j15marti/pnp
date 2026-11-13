#!/usr/bin/env node
'use strict';
/* LSPV-2/588. REFERENCE constructor and native CLI replayer, not an authoritative
 * R_mix341 checker. The unchanged pinned /386 executable makes every verdict.
 * From repo root: node experiments/arc/lspv2_588_native386_live_guard_ports.cjs
 * For independent evidence archive: node SCRIPT CHECKER SEED SOURCE OUTDIR.
 * The pinned /341 K4 source is matched to the explicitly provided canonical
 * clauses after authenticated GitHub readback; /341 checker is never merged.
 */
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const crypto=require('node:crypto'),cp=require('node:child_process'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checker=process.argv[2]||path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedFile=process.argv[3]||path.join(root,'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json');
const sourceFile=process.argv[4]||path.join(root,'results/raw/arc/574_k01_SIGNED_SOURCE.cnf');
const outDir=process.argv[5]||path.join(root,'results/raw/arc');
const fixtureFile=process.argv[6]||path.join(root,'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const gitblob=b=>crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');
const pins={checker:['338305c0ce101704205e57543756b8127074a986','22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113'],
 seed:['318c52d99977ea4e91bc8554051138a700c1dc94','0d8b1894f91d00c554727a92fed35b2bb58f2b1602f2a3cfcb949effda43ceb0'],
 source:[null,'3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c']};
function read(file,key){const b=fs.readFileSync(file);assert.equal(sha(b),pins[key][1],key+' SHA256 drift');if(pins[key][0])assert.equal(gitblob(b),pins[key][0],key+' Git blob drift');return b}
const checkerBytes=read(checker,'checker'), seedBytes=read(seedFile,'seed'), sourceBytes=read(sourceFile,'source');
const seed=JSON.parse(seedBytes),clone=x=>JSON.parse(JSON.stringify(x));
const canon=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const signedSource=sourceBytes.toString('utf8').trim().split(/\n/).filter(x=>x&&!x.startsWith('p ')).map(x=>x.trim().split(/\s+/).map(Number).slice(0,-1));
assert.deepEqual(seed.records.filter(r=>r.kind==='SOURCE').map(r=>r.c),signedSource,'external signed SOURCE not matched');
assert.equal(seed.records.length,45);assert.equal(seed.summary.paid_total,29);
assert.equal(seed.spec.h,4);assert.equal(seed.spec.guard,7);
assert.deepEqual(seed.gate_defs,[[0,8,1,4]]);
const g=seed.spec.guard;
const unguarded=signedSource.filter(c=>c.includes(-g)).map(c=>c.filter(x=>x!==-g));
const original341K4=[[1,2,3],[-1,-2,3],[-1,2,-3],[1,-2,-3],[-1,4,5],[1,-4,5],[1,4,-5],[-1,-4,-5],[-2,4,6],[2,-4,6],[2,4,-6],[-2,-4,-6],[-3,5,6],[3,-5,6],[3,5,-6],[-3,-5,-6]];
assert.deepEqual(unguarded,original341K4,'original /341 K4 source signature discrepancy');
let original341Verified=false;
if(fs.existsSync(fixtureFile)){
 const fixtureBytes=fs.readFileSync(fixtureFile);
 assert.equal(gitblob(fixtureBytes),'fe27fe1011d0021e721ccaeb747ed58da65d7464','original /341 fixture Git blob drift');
 const clauses=JSON.parse(fixtureBytes).fixtures[0].clauses.map(c=>c.literals);
 assert.deepEqual(clauses,unguarded,'live ports do not match original /341 K4 source');
 original341Verified=true;
}
const allTruths=Array.from({length:1<<6},(_,m)=>m);
function sat(C,m){return C.some(x=>x>0?!!(m&(1<<(x-1))):!(m&(1<<(-x-1))))}
assert.equal(allTruths.filter(m=>unguarded.every(c=>sat(c,m))).length,0,'K4 source not UNSAT');
for(let skip=0;skip<16;skip++)assert(allTruths.filter(m=>unguarded.every((c,i)=>i===skip||sat(c,m))).length>0,'source nonessential');
const originalUnitIndex=seed.records.findIndex(r=>r.kind==='SOURCE'&&r.source===-1);
assert.equal(originalUnitIndex,16);assert.deepEqual(seed.records[16].c,[g]);
function construct(order){
 const p=clone(seed),records=p.records.slice(0,17);
 // Every one of the sixteen signed native source occurrences is converted
 // into a CHARGED, actual native RES node, before any unguarded use.
 let ids=new Map(),active=new Set(),nodeClauses=new Map(),sourcePortIds=[];
 for(let i=0;i<16;i++){
  const D=seed.records[i];assert(D.c.includes(-g));
  const id=records.length;
  records.push({kind:'RES',c:unguarded[i],parents:[originalUnitIndex,i],pivot:g});
  assert.deepEqual(canon([...seed.records[16].c.filter(x=>x!==g),...D.c.filter(x=>x!==-g)]),unguarded[i]);
  ids.set(JSON.stringify(unguarded[i]),id);nodeClauses.set(id,unguarded[i]);active.add(id);sourcePortIds.push(id);
 }
 const allDP=[];
 for(const x of order){
  const pos=[...active].filter(id=>nodeClauses.get(id).includes(x));
  const neg=[...active].filter(id=>nodeClauses.get(id).includes(-x));
  for(const ai of pos)for(const bi of neg){
   const A=nodeClauses.get(ai),B=nodeClauses.get(bi);
   const c=canon([...A.filter(a=>a!==x),...B.filter(b=>b!==-x)]);
   if(c.some(a=>c.includes(-a)))continue;
   const key=JSON.stringify(c);
   if(!ids.has(key)){
    const j=records.length;
    records.push({kind:'RES',c,parents:[ai,bi],pivot:x});
    nodeClauses.set(j,c);ids.set(key,j);active.add(j);allDP.push(j);
   }
  }
  for(const v of [...pos,...neg])active.delete(v);
 }
 const sink=ids.get('[]');assert(sink!==undefined,'DP must reach empty clause');
 const live=new Set(),stack=[sink];
 while(stack.length){const v=stack.pop();if(live.has(v))continue;live.add(v);stack.push(...records[v].parents)}
 assert(sourcePortIds.every(v=>live.has(v)),'every guard-discharge port must be terminal-live');
 assert(allDP.every(v=>live.has(v)),'every paid DP node must be terminal-live');
 assert([...Array(17).keys()].every(i=>live.has(i)),'all originals and guard terminal-live');
 assert.equal(sink,records.length-1);
 p.records=records;p.summary={source:17,resolution:sourcePortIds.length+allDP.length,def_views:0,paid_gates:1,
   paid_total:sourcePortIds.length+allDP.length+1,live_records:records.length};
 const depth=Array(records.length).fill(0);
 for(let i=0;i<records.length;i++)if(records[i].parents.length)depth[i]=1+Math.max(...records[i].parents.map(x=>depth[x]));
 return {packet:p,meta:{order,sourcePorts:sourcePortIds.length,sourcePortIds,sourcePortsInTerminalCone:sourcePortIds.filter(i=>live.has(i)).length,
   true341SignedClauses:original341K4.length,pureResolutionNodes:allDP.length,allPaidProofRecordsLive:allDP.every(x=>live.has(x)),
   proofDepth:depth[sink],paidWork:p.summary.paid_total,sourceSha256:sha(sourceBytes)}};
}
const orders=[[6,5,4,3,2,1],[1,4,2,5,3,6],[1,2,3,4,5,6]];
const cases=[],results=[];const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2-588-'));
function run(label,p,want,write=false){
 const bytes=Buffer.from(JSON.stringify(p)+'\n');const file=path.join(tmp,label+'.json');fs.writeFileSync(file,bytes);
 const t0=process.hrtime.bigint(),r=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',timeout:30000,maxBuffer:1024*1024});
 const actual=r.status===0&&!r.error;assert.equal(actual,want,label+' '+r.stderr.slice(0,400));
 const output=actual?JSON.parse(r.stdout):null;
 if(actual){assert.equal(output.paid,p.summary.paid_total);assert.equal(output.negativeTests,11)}
 const result={label,expected:want?'ACCEPT':'REJECT',actual:actual?'ACCEPT':'REJECT',bytes:bytes.length,
   sha256:sha(bytes),gitBlob:gitblob(bytes),paidWork:p.summary.paid_total,records:p.records.length,
   elapsedMs:Number(process.hrtime.bigint()-t0)/1e6,
   originalAssertions:output?.assertions??null,originalBuiltInNegatives:output?.negativeTests??null,
   error:actual?null:(r.stderr.match(/Error: [^\n]+/)||[])[0]??r.stderr.slice(0,200)};
 cases.push(result);
 if(write){const outputFile='2026-11-12_2012_LSPV2_588_LIVE_PORTS_'+label+'.json';
 fs.mkdirSync(outDir,{recursive:true});fs.writeFileSync(path.join(outDir,outputFile),bytes);result.saved=outputFile;}
 return result;
}
try{
 run('original_W29',seed,true);
 for(const order of orders){const z=construct(order);const name='DP'+order.join('');
  results.push({label:name,...z.meta,verdict:run(name,z.packet,true,true)});
 }
 const base=construct(orders[0]);
 const edits={
  bad_signed_pivot:p=>p.records[17].pivot=-g,
  wrong_parent_order:p=>p.records[17].parents.reverse(),
  forged_source_clause:p=>p.records[0].c[0]*=-1,
  invalid_unguarded_resolvent:p=>p.records[17].c[0]*=-1,
  undercharge_one:p=>p.summary.paid_total--,
  missing_paid_owner:p=>p.gate_defs.pop(),
  future_parent:p=>p.records[17].parents[0]=p.records.length,
  unknown_AND3_consumer:p=>p.records.at(-1).kind='AND3',
  invalid_terminal:p=>p.records.at(-1).c=[1]
 };
 for(const [name,edit] of Object.entries(edits)){const p=clone(base.packet);edit(p);run('hostile_'+name,p,false)}
 const total=cases.length;
 const manifest={schema:'LSPV2-588-NATIVE386-LIVE-GUARD-TO-341-PORTS/v1',status:'PROVED/RESTRICTED construction + COMPUTATIONAL OS original checker',
  fact:'Every one of 16 /386 native RES unguarded source ports is a true ancestor of the final empty clause, unlike /593A unused port records.',
  original:{checker_sha256:sha(checkerBytes),checker_git_blob:gitblob(checkerBytes),seed_sha256:sha(seedBytes),seed_git_blob:gitblob(seedBytes),
   external_signed_source_sha256:sha(sourceBytes),source_bytes:sourceBytes.length},
  k4_original341_source_clause_count:16,original341_fixture_git_blob:'fe27fe1011d0021e721ccaeb747ed58da65d7464',original341_fixture_git_blob_checked_in_this_local_run:original341Verified,claimed_cross_calculus_bridge:'NOT AUTHENTICATED; no original single dispatcher for mixed RES-to-AND3',
  counters:{testCount:total,accepts:cases.filter(c=>c.actual==='ACCEPT').length,rejects:cases.filter(c=>c.actual==='REJECT').length,
   originalAcceptedAssertions:cases.reduce((n,c)=>n+(c.originalAssertions||0),0)},
  originalW29Paid:29,variants:results,allCases:cases,
  distinctResources:'logical W; certificate bytes; local construction/verification time; structural span; physical peak memory (not bounded)',
  open:['P2-D1','P2-C3','P2-B1','P2-B2','P2-B3','P1-01','P1-03','P1-04']};
 fs.mkdirSync(outDir,{recursive:true});const basename='2026-11-12_2012_LSPV2_588_LIVE_GUARD_PORTS_OS_RAW.json';
 fs.writeFileSync(path.join(outDir,basename),JSON.stringify(manifest,null,2)+'\n');
 console.log(JSON.stringify({status:'PASS',count:manifest.counters,variants:results.map(x=>({label:x.label,ports:x.sourcePortsInTerminalCone,dp:x.pureResolutionNodes,work:x.paidWork,span:x.proofDepth,bytes:x.verdict.bytes})),
   checker:sha(checkerBytes),sourceSha256:sha(sourceBytes),manifest:basename},null,2));
}finally{fs.rmSync(tmp,{recursive:true,force:true})}
