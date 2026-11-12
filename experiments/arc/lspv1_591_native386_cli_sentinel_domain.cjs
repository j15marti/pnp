#!/usr/bin/env node
'use strict';
// LSPV-1/591. Run: node experiments/arc/lspv1_591_native386_cli_sentinel_domain.cjs [output.json]
// Uses unmodified historical /386 checker in actual Node OS subprocesses.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),
  crypto=require('node:crypto'),assert=require('node:assert/strict'),
  cp=require('node:child_process'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedFile=path.join(root,'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json');
const rootFile=path.join(root,'results/raw/arc/2026-11-11_0812_LSPV2_559_EXTERNAL_K4_SIGNED_SOURCE.cnf');
const checkerText=fs.readFileSync(checker,'utf8'),seedText=fs.readFileSync(seedFile,'utf8');
function blob(s){return crypto.createHash('sha1').update('blob '+Buffer.byteLength(s)+'\0').update(s).digest('hex')}
assert.equal(blob(checkerText),'338305c0ce101704205e57543756b8127074a986');
assert.equal(blob(seedText),'318c52d99977ea4e91bc8554051138a700c1dc94');
const seed=JSON.parse(seedText),clone=x=>JSON.parse(JSON.stringify(x));
const lines=fs.readFileSync(rootFile,'utf8').trim().split(/\r?\n/);
assert.equal(lines.shift(),'p cnf 7 17');
const extRoot=lines.map(line=>{const a=line.split(/\s+/).map(Number);assert.equal(a.pop(),0);return a});
assert.deepEqual(seed.records.filter(r=>r.kind==='SOURCE').map(r=>r.c),extRoot);
function rebased(d,newGuard){
 const q=clone(d),old=q.spec.guard;
 assert(Number.isSafeInteger(newGuard)&&newGuard>q.spec.edges.length&&newGuard!==8);
 const f=x=>Math.abs(x)===old?Math.sign(x)*newGuard:x;
 q.spec.guard=newGuard;
 for(const r of q.records){
   r.c=r.c.map(f).sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
   if(r.kind==='RES')r.pivot=f(r.pivot);
 }
 const caller=extRoot.map(c=>c.map(f).sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b));
 assert.deepEqual(q.records.filter(r=>r.kind==='SOURCE').map(r=>r.c),caller);
 return q;
}
// Expose ONLY the unmodified checkProof function; skip the OS CLI loop in VM.
const sandbox={require,process:{argv:[process.execPath,checker]},console,structuredClone};
vm.runInNewContext(checkerText+'\n;globalThis.nativeCore=checkProof;',sandbox,{filename:checker});
const core=d=>{try{return {accept:true,paid:sandbox.nativeCore(d,{control:true}).paid}}catch(e){return {accept:false,error:String(e)}}};
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv1_591_'));
function cli(d,name){
 const p=path.join(temp,name+'.json');fs.writeFileSync(p,JSON.stringify(d));
 const r=cp.spawnSync(process.execPath,[checker,p],{encoding:'utf8',timeout:15000});
 if(r.error)throw r.error;
 const accepted=r.status===0,output=accepted?JSON.parse(r.stdout.trim().split('\n').at(-1)):null;
 return {accept:accepted,assertions:output?.assertions||null,
   error:accepted?null:(r.stderr.match(/accepted a corrupted proof|[A-Za-z]+ mismatch|bad pivot|wrong source|paid cost/)||[])[0]||r.stderr.slice(0,160)};
}
const guards=[7,9,13,17,61,97,127,257,997,10007,123456,999994,999995,999996,
  999997,999998,999999,1000000,1000001,1000002,2000003,1000000000,Number.MAX_SAFE_INTEGER];
const rows=[],hostiles=[];
try{
 for(const g of guards){
   const d=rebased(seed,g),a=core(d),b=cli(d,'guard_'+g);
   assert.equal(a.accept,true);assert.equal(a.paid,29);
   assert.equal(b.accept,g!==999999);
   assert.equal(d.records.at(-1).pivot,g);
   rows.push({guard:g,core:a.accept,cli:b.accept,paid:a.paid,assertions:b.assertions,error:b.error});
 }
 const noOwner=clone(seed);noOwner.gate_defs=[];noOwner.summary.paid_gates=0;noOwner.summary.paid_total=28;
 assert.equal(core(noOwner).accept,true);assert.equal(cli(noOwner,'no_owner').accept,false);
 hostiles.push({name:'ownerless',core:core(noOwner),cli:cli(noOwner,'no_owner_again')});
 for(const [name,change] of [
  ['wrong_source',d=>{d.records[0].c[0]*=-1}],
  ['wrong_payment',d=>{d.summary.paid_total--}],
  ['unbound_guard',d=>{d.spec.guard=97}]
 ]){
  const d=clone(seed);change(d);const a=core(d),b=cli(d,name);
  assert.equal(a.accept,false);assert.equal(b.accept,false);
  hostiles.push({name,core:a,cli:b});
 }
}finally{fs.rmSync(temp,{recursive:true,force:true})}
const out={id:'LSPV-1/591',original_checker_blob:blob(checkerText),seed_blob:blob(seedText),
  external_root_blob:blob(fs.readFileSync(rootFile,'utf8')),
  mode:'Node OS CLI + unchanged mathematical checker exposed via VM',
  guard_tests:rows.length,cli_accepts:rows.filter(x=>x.cli).length,
  cli_rejects:rows.filter(x=>!x.cli).length,all_core_accept:rows.every(x=>x.core),
  rows,hostiles,
  scope:'Only parsed JSON historical /386 SOURCE/DEF/RES checker; not unified R_mix341.'};
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify(out,null,2));
