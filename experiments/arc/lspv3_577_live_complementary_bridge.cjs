#!/usr/bin/env node
'use strict';
// LSPV-3/577. Native OS replay of unchanged archived /386 CLI.
// Run from repository root: node experiments/arc/lspv3_577_live_complementary_bridge.cjs [results.json]
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const os=require('node:os'),cp=require('node:child_process'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checkerPath=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedPath=path.join(root,'results/raw/arc/2026-11-11_0224_LSPV3_566_K4x3_CLI_ACCEPTED_PACKET.json');
const published=path.join(root,'results/raw/arc/2026-11-11_1324_LSPV3_577_LIVE_COMPLEMENTARY_NATIVE386_PACKET.json');
const shaBlob=s=>crypto.createHash('sha1').update(Buffer.from('blob '+Buffer.byteLength(s)+'\0'+s)).digest('hex');
assert.equal(shaBlob(fs.readFileSync(checkerPath,'utf8')),'338305c0ce101704205e57543756b8127074a986');
assert.equal(shaBlob(fs.readFileSync(seedPath,'utf8')),'4656b801feba72b84133bacad5ae18692a83fe03');
const base=JSON.parse(fs.readFileSync(seedPath,'utf8'));
const clone=v=>JSON.parse(JSON.stringify(v));
const key=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function compile(sourceIndex,ell,rewire=true){
 const p=clone(base),at=p.records.findIndex(r=>r.kind==='RES'),old=base.records[sourceIndex];
 const z=21,w=22,n=8,C=old.c;
 assert.equal(at,17);
 assert.equal(old.kind,'SOURCE');
 assert(C.includes(ell)&&Math.abs(ell)<=p.spec.edges.length);
 assert.deepEqual(p.gate_defs,[[0,20,1,4]]);
 const add=[
  {kind:'DEF',c:key([-z,ell]),parents:[],gate:1},
  {kind:'DEF',c:key([-z,-ell]),parents:[],gate:1},
  {kind:'RES',c:[-z],parents:[at,at+1],pivot:ell},
  {kind:'DEF',c:key([w,z,-ell]),parents:[],gate:2},
  {kind:'DEF',c:key([-w,ell]),parents:[],gate:2},
  {kind:'RES',c:key([...C.filter(x=>x!==ell),z,w]),parents:[sourceIndex,at+3],pivot:ell},
  {kind:'RES',c:key([...C.filter(x=>x!==ell),w]),parents:[at+5,at+2],pivot:z},
  {kind:'RES',c:key(C),parents:[at+6,at+4],pivot:w}
 ];
 p.gate_defs.push([1,z,ell,-ell],[2,w,-z,ell]);
 p.records.splice(at,0,...add);
 for(let i=0;i<base.records.length;i++){
  const rec=p.records[i<at?i:i+n];
  rec.parents=rec.parents.map(j=>rewire&&j===sourceIndex&&rec.kind==='RES'?at+n-1:j<at?j:j+n);
 }
 p.summary.def_views+=4;p.summary.resolution+=4;p.summary.paid_gates+=2;
 p.summary.paid_total+=6;p.summary.live_records+=8;
 assert.deepEqual(p.spec,base.spec);
 assert.deepEqual(p.records.filter(r=>r.kind==='SOURCE'),base.records.filter(r=>r.kind==='SOURCE'));
 assert.equal(p.summary.paid_total,35);
 return p;
}
function ancestry(p){
 const seen=new Set(),stack=[p.records.length-1];
 while(stack.length){let i=stack.pop();if(seen.has(i))continue;seen.add(i);
  for(const j of p.records[i].parents)stack.push(j);}
 return {terminal_count:seen.size,inserted_live:Array.from({length:8},(_,i)=>seen.has(17+i))};
}
const plus=compile(0,1),minus=compile(1,-1),dead=compile(0,1,false);
assert.equal(fs.readFileSync(published,'utf8'),JSON.stringify(plus));
assert(ancestry(plus).inserted_live.every(Boolean));
assert(ancestry(minus).inserted_live.every(Boolean));
assert(ancestry(dead).inserted_live.every(x=>!x));
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp577-'));
function run(label,p,expected){
 const serialized=JSON.stringify(p),input=path.join(tmp,label+'.json');
 fs.writeFileSync(input,serialized);
 const result=cp.spawnSync(process.execPath,[checkerPath,input],
  {encoding:'utf8',timeout:30000,maxBuffer:1<<22});
 if(result.error)throw result.error;
 const accepted=result.status===0;
 assert.equal(accepted,expected,label+': '+String(result.stderr||result.stdout).slice(0,240));
 const out={label,accepted,raw_bytes:Buffer.byteLength(serialized),
  sha256:crypto.createHash('sha256').update(serialized).digest('hex'),
  ...ancestry(p)};
 if(accepted){
  const checked=JSON.parse(result.stdout.trim());
  assert.equal(checked.negativeTests,11);
  out.verifier=checked;
 }else out.error=(result.stderr||result.stdout).trim().slice(0,300);
 return out;
}
try{
 const tests=[
  run('baseline',base,true),
  run('terminal_live_positive_pivot',plus,true),
  run('terminal_live_negative_pivot',minus,true),
  run('terminal_dead_control',dead,true)
 ];
 const hostile=[
  ['wrong_facet',p=>p.records[17].c=[1,21]],
  ['wrong_unit',p=>p.records[19].c=[21]],
  ['wrong_signed_pivot',p=>p.records[19].pivot=2],
  ['wrong_parent_pivot',p=>p.records[23].pivot=20],
  ['wrong_owner',p=>p.records[20].gate=8],
  ['future_parent',p=>p.records[22].parents[1]=p.records.length],
  ['underpaid',p=>p.summary.paid_total--],
  ['wire_collision',p=>p.gate_defs[2][1]=21],
  ['future_wire',p=>p.gate_defs[2][2]=-33],
  ['forged_source',p=>p.records[0].source=13],
  ['wrong_rewire',p=>p.records[25].parents[0]=1]
 ];
 for(const [label,change] of hostile){const x=clone(plus);change(x);tests.push(run(label,x,false));}
 const raw={run:'LSPV-3/577',time:'2026-11-11 13:24 PST',
  checker_blob:'338305c0ce101704205e57543756b8127074a986',
  source_seed_blob:'4656b801feba72b84133bacad5ae18692a83fe03',
  checker_execution:'unchanged archived /386 full CLI in OS Node subprocess',
  positives:4,hostile_rejections:11,tests,
  status:'Restricted native /386 demonstration only; full R_mix341, P2-D1, P2-C3, P2-B1/B2/B3 OPEN; P versus NP OPEN'};
 if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(raw,null,2)+'\n');
 console.log(JSON.stringify(raw,null,2));
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
