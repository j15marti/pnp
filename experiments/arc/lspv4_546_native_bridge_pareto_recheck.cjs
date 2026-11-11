'use strict';
/*
 * LSPV-4/546 restricted native /386 resource dominance audit.
 * Usage: node experiments/arc/lspv4_546_native_bridge_pareto_recheck.cjs [--write]
 * The archival checker is executed unchanged as a real Node subprocess.
 * Deterministic, pinned permutations; no search heuristics are needed to reproduce the witnesses.
 */
const fs=require('fs'),path=require('path'),os=require('os'),crypto=require('crypto');
const cp=require('child_process'),assert=require('assert');
const ROOT=path.resolve(__dirname,'../..');
const BASE='results/raw/arc/2026-11-11_0900_LSPV1_575_BRIDGE_GUARDED_DP_NATIVE_ACCEPTED.json';
const UNFOLD='results/raw/arc/2026-11-11_0836_LSPV4_545_UNFOLDED_BRIDGE_ACCEPTED.json';
const CHECKER='experiments/arc/lspv2_386_independent_verify.js';
const PIN={base:'d5de0f477cd736ec5fd7b01be18350f9cb594fd2',
 unfold:'d8c49d434323c93d621105e664e89a51c9ddad3f',
 checker:'338305c0ce101704205e57543756b8127074a986'};
const AREA_ORDER=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,70,78,79,88,85,71,76,74,86,91,96,82,93,97,73,81,83,80,89,72,77,75,84,90,95,99,87,92,94,98,100,41,53,47,52,58,63,48,50,43,54,59,61,65,67,45,55,42,49,60,64,46,56,44,51,57,62,66,68,69,101,102];
const LITERAL_ORDER=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,72,73,77,87,81,80,89,83,92,75,94,84,90,95,70,79,85,71,76,86,91,96,98,74,82,78,88,93,97,99,100,43,54,41,53,46,56,44,51,57,62,42,49,48,50,59,45,55,60,64,66,61,68,47,52,58,63,65,67,69,101,102];
function sha1Blob(text) {
 const b=Buffer.from(text,'utf8');
 return crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex');
}
function pinned(f,sha) {
 const text=fs.readFileSync(path.join(ROOT,f),'utf8');
 assert.strictEqual(sha1Blob(text),sha,'changed source: '+f);
 return text;
}
function rearrange(base,order) {
 assert.strictEqual(order.length,base.records.length);
 assert.strictEqual(new Set(order).size,order.length);
 assert.deepStrictEqual([...order].sort((a,b)=>a-b),base.records.map((_,i)=>i));
 const pos=new Map(order.map((id,i)=>[id,i]));
 const records=order.map(id=>({...base.records[id],parents:base.records[id].parents.map(j=>pos.get(j))}));
 for(let i=0;i<records.length;i++)
  for(const j of records[i].parents)assert(j<i,'non-topological reference');
 return {...base,records};
}
function audit(p) {
 const R=p.records,n=R.length,remaining=Array(n).fill(0),depth=Array(n).fill(0);
 let refs=0,res=0,src=0;
 function canonical(a){return [...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);}
 for(let i=0;i<n;i++){
  const r=R[i];if(r.kind==='SOURCE')src++;
  if(r.kind==='RES'){
   res++;refs+=2;
   assert.strictEqual(r.parents.length,2);
   const [a,b]=r.parents.map(j=>R[j].c);
   assert(a.includes(r.pivot)&&b.includes(-r.pivot),'signed pivot failure');
   const c=canonical([...a.filter(x=>x!==r.pivot),...b.filter(x=>x!==-r.pivot)]);
   assert.deepStrictEqual(c,r.c,'inexact resolvent');
   depth[i]=1+Math.max(...r.parents.map(j=>depth[j]));
  }
  for(const j of r.parents){assert(j<i);remaining[j]++;}
 }
 let live=new Set(),peak=0,peakLiterals=0,slotSteps=0;
 for(let i=0;i<n;i++){
  const r=R[i];
  if(r.kind==='RES'){
   peak=Math.max(peak,live.size+1);
   peakLiterals=Math.max(peakLiterals,r.c.length+
     [...live].reduce((sum,j)=>sum+R[j].c.length,0));
   if(remaining[i])live.add(i);
  }
  for(const j of r.parents)if(!--remaining[j])live.delete(j);
  slotSteps+=live.size;
 }
 let visited=new Set(),pending=[n-1];
 while(pending.length){
  const i=pending.pop();if(visited.has(i))continue;visited.add(i);
  pending.push(...R[i].parents);
 }
 assert.deepStrictEqual(R[n-1].c,[]);
 assert.strictEqual(src,p.summary.source);
 assert.strictEqual(res,p.summary.resolution);
 assert.strictEqual(p.summary.paid_total,res+p.gate_defs.length);
 return {paidWork:p.summary.paid_total,resolution:res,source:src,owners:p.gate_defs.length,
  records:n,parentReferences:refs,terminalResolutionSpan:depth[n-1],
  peakFreshPaidSlots:peak,peakSignedLiteralSlots:peakLiterals,
  retainedPaidSlotSteps:slotSteps,terminalSourceAncestors:
   [...visited].filter(i=>R[i].kind==='SOURCE').length,
  compactJSONBytes:Buffer.byteLength(JSON.stringify(p),'utf8')};
}
function runOriginal(checker,p,name) {
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv4-546-'));
 try{
  const f=path.join(dir,name+'.json');fs.writeFileSync(f,JSON.stringify(p));
  const out=cp.spawnSync(process.execPath,[checker,f],
   {encoding:'utf8',maxBuffer:10*1024*1024});
  let parsed=null;if(out.status===0){
   parsed=JSON.parse(out.stdout.trim().split('\n').at(-1));
  }
  return {accept:out.status===0,exit:out.status,
   assertions:parsed?.assertions??null,
   bundledNegatives:parsed?.negativeTests??null,
   paid:parsed?.paid??null,
   error:out.status===0?null:out.stderr.trim().slice(0,220)};
 }finally{fs.rmSync(dir,{recursive:true,force:true});}
}
function main(){
 const base=JSON.parse(pinned(BASE,PIN.base));
 const unfold=JSON.parse(pinned(UNFOLD,PIN.unfold));
 const checker=path.join(ROOT,CHECKER);
 pinned(CHECKER,PIN.checker);
 const orderArea=rearrange(base,AREA_ORDER),orderLiteral=rearrange(base,LITERAL_ORDER);
 const specimens={original575:base,area546:orderArea,literal546:orderLiteral,tree545:unfold};
 const positives={};
 const originalSources=JSON.stringify(base.records.filter(r=>r.kind==='SOURCE'));
 for(const [name,p] of Object.entries(specimens)){
  const m=audit(p),test=runOriginal(checker,p,name);
  assert(test.accept,name+': original CLI rejected '+test.error);
  assert.strictEqual(test.bundledNegatives,11);
  assert.strictEqual(JSON.stringify(p.records.filter(r=>r.kind==='SOURCE')),originalSources);
  assert.deepStrictEqual(p.spec,base.spec);
  assert.deepStrictEqual(p.gate_defs,base.gate_defs);
  positives[name]={...m,checker:test};
 }
 assert.strictEqual(positives.original575.paidWork,63);
 assert.deepStrictEqual([positives.original575.peakFreshPaidSlots,
  positives.area546.peakFreshPaidSlots,positives.literal546.peakFreshPaidSlots,
  positives.tree545.peakFreshPaidSlots],[10,7,7,8]);
 assert.deepStrictEqual([positives.area546.retainedPaidSlotSteps,
  positives.literal546.peakSignedLiteralSlots],[199,36]);
 assert.strictEqual(positives.tree545.paidWork,305);
 const mutants={
  wrongPaid:p=>p.summary.paid_total--,
  forgedSource:p=>p.records[0].c[0]*=-1,
  forwardParent:p=>p.records.at(-1).parents[0]=999999,
  badPivot:p=>p.records.at(-1).pivot=1234567,
  removedOwner:p=>p.gate_defs=[],
  removedSource:p=>p.records.shift(),
  wrongParent:p=>p.records[80].parents[0]=41,
  alienOpcode:p=>p.records[88].kind='GF2'
 };
 const negatives={};
 for(const [name,mutate] of Object.entries(mutants)){
  const p=JSON.parse(JSON.stringify(orderLiteral));mutate(p);
  const result=runOriginal(checker,p,name);
  assert(!result.accept,'original checker accepted hostile '+name);
  negatives[name]=result;
 }
 const raw={timestampPST:'2026-11-11 09:36',status:'PROVED/RESTRICTED + COMPUTATIONAL',
  scope:'original archived /386 SOURCE/paid AND2 owner/strict RES, not R_mix341',
  checkerGitBlob:PIN.checker,baseGitBlob:PIN.base,priorTreeGitBlob:PIN.unfold,
  model:'read-only SOURCE; fresh RES result; last-use release; no free recomputation',
  positive:positives,hostile:negatives,notes:[
   'All positives invoke the unchanged archived checker via OS Node subprocess and its eleven native negative controls.',
   'Peak fresh paid-result slots and signed-literal slots are abstract schedule measurements, not process RSS.',
   'Original source, owner, paid DAG nodes, source ancestry and dependency span are unchanged by the two permutations.',
   'The 63/7 schedule beats the previously accepted 305/8 tree on work and paid-result slot peak, but not on literal peak (36 versus 34).',
   'No minimum W or minimum space has been proved; full historical R_mix341 remains unauthenticated.']};
 if(process.argv.includes('--write')){
  const files={
   'results/raw/arc/2026-11-11_0936_LSPV4_546_AREA_SCHEDULE_ACCEPTED.json':orderArea,
   'results/raw/arc/2026-11-11_0936_LSPV4_546_LITERAL_SCHEDULE_ACCEPTED.json':orderLiteral,
   'results/raw/arc/2026-11-11_0936_LSPV4_546_BRIDGE_PARETO_OS_RAW.json':raw};
  for(const [p,obj] of Object.entries(files)){
   const dest=path.join(ROOT,p);
   fs.mkdirSync(path.dirname(dest),{recursive:true});
   fs.writeFileSync(dest,JSON.stringify(obj,null,2)+'\n');
  }
 }
 process.stdout.write(JSON.stringify(raw,null,2)+'\n');
}
main();
