"use strict";
/* LSPV-4/560: reconstruct, compare and replay an authenticated /386
   non-SOURCE-equivalent paid shared lemma. Run from repository root:
   node experiments/arc/lspv4_560_nonsource_shared_lemma.cjs
   It invokes the UNCHANGED archived /386 verifier as a Node OS subprocess,
   including the verifier's eleven built-in negative controls.
   This is not the missing full historical R_mix341 checker. */
const fs = require("node:fs");
const path = require("node:path");
const os = require("node:os");
const crypto = require("node:crypto");
const assert = require("node:assert/strict");
const cp = require("node:child_process");
const root = path.resolve(__dirname, "../..");
const fixture = path.join(root,"results/raw/arc/2026-11-12_0212_LSPV2_571_ACCEPTED_LIVE_JOINT_PORT_ORBIT.json");
const witness = path.join(root,"results/raw/arc/2026-11-12_0436_LSPV4_560_W38_ACCEPTED.json");
const optimized = path.join(root,"results/raw/arc/2026-11-12_0436_LSPV4_560_W38_MINAREA_ACCEPTED.json");
const checker = path.join(root,"experiments/arc/lspv2_386_independent_verify.js");
const clone = x => JSON.parse(JSON.stringify(x));
const input = JSON.parse(fs.readFileSync(fixture,"utf8"));

function make(p) {
  const q=clone(p);
  q.records.splice(29,0,{kind:"RES",c:[-1,-4,-5,-7],parents:[22,23],pivot:8});
  q.records.forEach((r,i)=>{ if(i!==29)r.parents=r.parents.map(v=>v>=29?v+1:v); });
  assert.deepEqual(q.records[31].parents,[7,0]);
  q.records[31].parents[0]=29;
  q.summary.resolution++;
  q.summary.paid_total++;
  q.summary.live_records++;
  return q;
}
function reorder(q) {
  const paid=[32,40,35,44,46,51,23,29,31,43,36,41,47,52,54,
       24,25,26,27,28,33,38,37,45,49,50,30,42,34,39,48,53,55,56,57];
  const permutation=[...Array(23).keys(),...paid];
  const lookup=new Map(permutation.map((old,i)=>[old,i]));
  const out=clone(q);
  out.records=permutation.map(old=>clone(q.records[old]));
  for(const rec of out.records)rec.parents=rec.parents.map(p=>lookup.get(p));
  return out;
}
const q=make(input), r=reorder(q);
const onDisk=JSON.parse(fs.readFileSync(witness,"utf8"));
const reorderedOnDisk=JSON.parse(fs.readFileSync(optimized,"utf8"));
assert.deepEqual(q,onDisk,"published chronological certificate mismatch");
assert.deepEqual(r,reorderedOnDisk,"published reordered certificate mismatch");
assert.equal(q.summary.paid_total,38);
assert.equal(q.records.length,58);
assert.equal(q.records[23].kind,"RES");
assert.ok(!q.records.some(x=>x.kind==="SOURCE"&&JSON.stringify(x.c)===JSON.stringify(q.records[23].c)));
let uses=[];
q.records.forEach((rec,i)=>{if(rec.parents.includes(23))uses.push(i);});
assert.deepEqual(uses,[24,29],"shared non-source paid node must have two consumers");
assert.deepEqual(q.records[31].parents,[29,0]);
assert.deepEqual(q.records[33].parents,[28,3]);
function ancestor(start) {
  const set=new Set(), todo=[start];
  while(todo.length){let id=todo.pop();if(set.has(id))continue;set.add(id);todo.push(...q.records[id].parents);}
  return set;
}
const A=ancestor(24),B=ancestor(29);
assert.deepEqual([...A].filter(i=>B.has(i)&&q.records[i].kind==="RES").sort((x,y)=>x-y),[23]);
assert.deepEqual([...new Set([...A].filter(i=>B.has(i)&&q.records[i].kind==="DEF").map(i=>q.records[i].gate))],[0]);
function reaches(start,target){
 const todo=[start], seen=new Set();
 while(todo.length){const u=todo.pop();if(u===target)return true;if(seen.has(u))continue;seen.add(u);
  q.records.forEach((rec,i)=>{if(rec.parents.includes(u))todo.push(i);});
 }
 return false;
}
assert.ok(reaches(24,57) && reaches(29,57),"both shared branches must reach sink");
function sha(s){return crypto.createHash("sha256").update(s).digest("hex");}
const dir=fs.mkdtempSync(path.join(os.tmpdir(),"lspv4-560-"));
function checkerRun(data,label) {
 const target=path.join(dir,label+".json");
 fs.writeFileSync(target,JSON.stringify(data));
 const proc=cp.spawnSync(process.execPath,[checker,target],{encoding:"utf8",timeout:30000});
 return {status:proc.status,signal:proc.signal,stdout:proc.stdout.trim(),stderr:proc.stderr.trim(),
  bytes:fs.statSync(target).size,sha256:sha(fs.readFileSync(target))};
}
try {
 const positive=[["base",input],["candidate",q],["area-optimal",r]].map(([name,data])=>{
  const out=checkerRun(data,name);
  assert.equal(out.status,0, name+": checker CLI rejected: "+out.stderr);
  const x=JSON.parse(out.stdout);
  assert.equal(x.negativeTests,11);return {name, ...out,checker:x};
 });
 const bad=[
  ["bad-pivot",d=>{d.records[29].pivot=9;}],
  ["bad-resolvent",d=>{d.records[29].c=[1,-4,-5,-7];}],
  ["bad-parent",d=>{d.records[29].parents[1]=7;}],
  ["forward-ref",d=>{d.records[29].parents[1]=57;}],
  ["underpaid",d=>{d.summary.paid_total--;}],
  ["forged-source",d=>{d.records[7].c=[-1,4,5,-7];}],
  ["bad-shared-consumer",d=>{d.records[31].parents[0]=23;}]
 ];
 const negative=bad.map(([name,mutate])=>{
  const d=clone(q);mutate(d);
  const out=checkerRun(d,name);
  assert.notEqual(out.status,0,name+": illegal packet accepted");
  return {name,rejected:true,detail:out.stderr.split("\n").slice(0,2).join(" ")};
 });
 const alternative=clone(q);alternative.records[31].parents[0]=7;
 const control=checkerRun(alternative,"valid-source-bypass");
 assert.equal(control.status,0,"valid cheaper alternative was rejected");
 console.log(JSON.stringify({proof_status:"RESTRICTED /386",work:38,
  sourceEquivalentSharedLemma:false,terminalLiveConsumers:[24,29],
  countedOnceIntersectionPaid:2,positive,negative,
  validShortCircuitSourceBypass:{accepted:true,bytes:control.bytes},
  fullHistoricalMix341:"NOT AUTHENTICATED",osOriginalCheckerReplayed:true},null,2));
} finally {
 fs.rmSync(dir,{recursive:true,force:true});
}
