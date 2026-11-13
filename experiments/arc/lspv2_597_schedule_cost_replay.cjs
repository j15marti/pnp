#!/usr/bin/env node
'use strict';
/* LSPV-2/597. Replays byte-exact /386 certificates with unchanged archived
 * checker. This is a TEST DRIVER, not an authoritative native R_mix341 parser.
 * Usage: node lspv2_597_schedule_cost_replay.cjs [output_directory]
 */
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const crypto=require('node:crypto'),cp=require('node:child_process');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..'),out=path.resolve(process.argv[2]||path.join(root,'results/raw/arc'));
const chk=path.join(root,'experiments/arc/lspv2_386_independent_verify.js'),base=path.join(root,'results/raw/arc/2026-11-13_0308_LSPV2_596_NATIVE386_W81_ACCEPTED.json');
const src=path.join(root,'results/raw/arc/2026-11-13_0212_LSPV2_595_TRIPLEX_SOURCE.cnf');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const chkb=fs.readFileSync(chk),baseb=fs.readFileSync(base),srcb=fs.readFileSync(src);
assert.equal(hash(chkb),'22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113');
assert.equal(hash(baseb),'85d353148d9e4ddc6f39f1d9666158665439fdab41f9e72ade6ae7ca56990562');
assert.equal(hash(srcb),'096666b94d8865aba487c331abe9b899d04c4e1251b90ea0565b370218537c5c');
const seed=JSON.parse(baseb),R=seed.records;
assert.equal(R.length,129);assert.equal(seed.summary.paid_total,81);
const sources=R.filter(r=>r.kind==='SOURCE');assert.equal(sources.length,49);
// The external signed CNF is an independent input, not a native checker field.
const lines=srcb.toString('utf8').trim().split(/\r?\n/);
assert.equal(lines.shift(),'p cnf 19 49');
const external=lines.map(x=>x.trim().split(/\s+/).map(Number));
assert.equal(external.length,49);
assert(external.every(x=>x.at(-1)===0));
assert.deepEqual(external.map(x=>x.slice(0,-1)),sources.map(s=>s.c));
const B=[[...Array(27)].map((_,j)=>j+49),[...Array(26)].map((_,j)=>j+76),[...Array(26)].map((_,j)=>j+102)];
const terminal=128;
assert(B.every(b=>b.every(i=>R[i].kind==='RES')));
for(let c=0;c<B.length;c++) for(const i of B[c]) for(const p of R[i].parents){
 assert(p<49||B[c].includes(p),`cross-block paid dependency ${p}->${i}`);
}
const last=R[terminal];assert.equal(last.kind,'RES');
assert(last.parents.every(p=>p<49||B[0].includes(p)));
const cache=structuredClone(seed);
function permute(order){
 let oldOrder=[...Array(49)].map((_,i)=>i);
 for(const c of order)oldOrder.push(...B[c]);oldOrder.push(terminal);
 assert.equal(new Set(oldOrder).size,129);
 const relocated=new Map(oldOrder.map((old,idx)=>[old,idx]));
 const out=structuredClone(cache);
 out.records=oldOrder.map(i=>{const r=structuredClone(R[i]);r.parents=r.parents.map(j=>relocated.get(j));return r;});
 assert(out.records.every((r,i)=>r.parents.every(j=>j<i)));
 assert.equal(JSON.stringify(out.records.slice(0,49)),JSON.stringify(R.slice(0,49)));
 assert.deepEqual(out.gate_defs,seed.gate_defs);assert.deepEqual(out.spec,seed.spec);assert.deepEqual(out.summary,seed.summary);
 return {out,oldOrder};
}
function ancestry(packet){let R=packet.records,all=[];
 for(let i=0;i<R.length;i++){
  if(R[i].kind==='SOURCE')all[i]=new Set([i]);
  else if(R[i].kind==='RES'){const s=new Set();for(const p of R[i].parents)for(const x of all[p])s.add(x);all[i]=s;}
  else all[i]=new Set();
 }
 return [...all.at(-1)].sort((a,b)=>a-b);
}
function resources(packet){
 const R=packet.records,lastUse=new Map(),useCount=new Map();
 for(let i=0;i<R.length;i++)if(R[i].kind==='RES'){lastUse.set(i,i);useCount.set(i,0)}
 for(let i=0;i<R.length;i++)for(const p of R[i].parents)if(R[p].kind==='RES'){
  lastUse.set(p,i);useCount.set(p,useCount.get(p)+1);
 }
 const live=new Map();let peak=0,peakAfter=0,area=0,byteArea=0,maxPayload=0;
 const originalIndexOf=new Map();
 const depth=[];
 let span=0;
 for(let i=0;i<R.length;i++){
  if(R[i].kind!=='RES'){depth[i]=0;continue}
  depth[i]=1+Math.max(...R[i].parents.map(p=>depth[p]||0));span=Math.max(span,depth[i]);
  live.set(i,JSON.stringify(R[i].c).length);
  peak=Math.max(peak,live.size);
  for(const p of R[i].parents) if(R[p].kind==='RES'&&lastUse.get(p)===i)live.delete(p);
  if(lastUse.get(i)===i && i!==R.length-1)live.delete(i);
  peakAfter=Math.max(peakAfter,live.size);
  area+=live.size;
  let payload=[...live.values()].reduce((s,v)=>s+v,0);
  byteArea+=payload;maxPayload=Math.max(maxPayload,payload);
 }
 return {paid:packet.summary.paid_total,res:packet.summary.resolution,source:packet.summary.source,
  peak_fresh_clause_slots:peak,peak_retained_after_step:peakAfter,live_paid_slot_steps:area,
  retained_clause_json_byte_steps:byteArea,peak_retained_clause_json_bytes:maxPayload,
  res_span:span,zero_consumer_res:[...useCount].filter(([,n])=>n===0).length};
}
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2-597-'));
const cases=[];
function run(label,obj,expect){
 const body=Buffer.from(JSON.stringify(obj)+'\n');const p=path.join(tmp,'packet.json');fs.writeFileSync(p,body);
 const r=cp.spawnSync(process.execPath,[chk,p],{encoding:'utf8',timeout:30000,maxBuffer:1<<20});
 const accept=r.status===0&&!r.error;
 assert.equal(accept,expect,`${label}: native checker mismatch: ${r.stderr||r.error}`);
 let result=accept?JSON.parse(r.stdout.trim()):null;
 if(accept){assert.equal(result.paid,81);assert.equal(result.sources,49);assert.equal(result.negativeTests,11)}
 const rec={name:label,verdict:accept?'ACCEPT':'REJECT',sha256:hash(body),bytes:body.length,
  paid:accept?result.paid:null,assertions:result?.assertions||null,
  negative_controls:result?.negativeTests||null,
  error:accept?null:(r.stderr.trim().split('\n').find(x=>x.includes('Error:'))||r.stderr.trim()).slice(0,200)};
 cases.push(rec);if(!expect)fs.writeFileSync(path.join(out,`LSPV2_597_${label}.json`),body);return {rec,body};
}
const orders=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
const rows=[];let minPeak=Infinity,maxPeak=-Infinity;
try{
 for(const order of orders){
  const {out:p,oldOrder}=permute(order);
  const label=order.join('');const {rec,body}=run('order_'+label,p,true);
  assert.deepEqual(ancestry(p),[...Array(16)].map((_,i)=>i).concat([48]));
  const m=resources(p);
  rows.push({...rec,order:label,terminal_parent_original:[48,75],metrics:m});
  minPeak=Math.min(minPeak,m.peak_fresh_clause_slots);maxPeak=Math.max(maxPeak,m.peak_fresh_clause_slots);
  fs.writeFileSync(path.join(out,`LSPV2_597_NATIVE386_ORDER_${label}_W81.json`),body);
 }
 assert(minPeak<maxPeak,'space must vary across validated schedules');
 const sample=permute([1,2,0]).out;
 for(const [name,mutate] of [
  ['wrong_pivot',d=>{d.records.at(-1).pivot=987654}],
  ['forged_source',d=>{d.records[0].c=[-1,2,3,-19]}],
  ['paid_undercharge',d=>{d.summary.paid_total--}],
  ['future_parent',d=>{d.records.at(-1).parents[1]=d.records.length}],
  ['unsupported_and3',d=>{d.records.at(-1).kind='AND3'}],
  ['invalid_owner',d=>{d.gate_defs[0][1]=1}],
 ]){const q=structuredClone(sample);mutate(q);run('reject_'+name,q,false)}
 const baseline=resources(seed);
 const manifest={id:'LSPV-2/597',date:'2026-11-13 04:12 PST',
  scope:'Original /386 SOURCE/DEF/RES checker only; not historical complete R_mix341; source-bound signed CNF',
  status:'PROVED/RESTRICTED scheduling theorem; COMPUTATIONAL original CLI',
  pins:{checker_sha256:hash(chkb),input_W81_sha256:hash(baseb),external_CNf_sha256:hash(srcb)},
  source:{variables:19,clauses:49,terminal_ancestry:[...Array(16)].map((_,i)=>i).concat([48])},
  ordered_blocks_original_indices:B.map(x=>[x[0],x.at(-1)]),
  target:'Permute 3 independent paid-RES cones with terminal contradiction last',
  baseline_metrics:baseline,permutations:rows,
  totals:{accepts:cases.filter(x=>x.verdict==='ACCEPT').length,rejects:cases.filter(x=>x.verdict==='REJECT').length,
   assertions:cases.reduce((s,x)=>s+(x.assertions||0),0),
   peak_fresh_range:[minPeak,maxPeak]},
  cases,guards:['No cross-block RES dependencies','all SOURCE objects unchanged in original order','native terminal still last','all signed parent indices rewritten', 'one paid gate owner unchanged'],
  limitations:['Fixed source-first presentation','metrics only retained RES clause values, no source/heap/OS RAM','no claim of globally optimal peak','verification time separate from paid logical work','full mixed grammar absent']};
 const raw=JSON.stringify(manifest,null,2)+'\n';fs.writeFileSync(path.join(out,'LSPV2_597_SCHEDULE_OS_RAW.json'),raw);
 console.log(JSON.stringify({status:'PASS',totals:manifest.totals,baseline,results:rows.map(x=>({order:x.order,bytes:x.bytes,...x.metrics}))},null,2));
}finally{fs.rmSync(tmp,{recursive:true,force:true})}