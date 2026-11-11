#!/usr/bin/env node
'use strict';
// LSPV-5/497 Independent Proof Red Team.
// Native multi-consumer paid-Resolution audit on the exact LSPV-4/551 W61 source.
// Run from a full checkout: node experiments/review/lspv5_497_native_shared_paid_dp_audit.cjs
// Deterministic (seeded LCG); designed to finish well under 30 s.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),cp=require('node:child_process'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const seedFile=path.join(root,'results/raw/arc/2026-11-11_1436_LSPV4_551_W61_MIN_SLOT_THEN_BYTE_AREA_ACCEPTED.json');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const outRaw=path.join(root,'results/raw/review/2026-11-11_1548_LSPV5_497_NATIVE_SHARED_PAID_DP_RAW.json');
const outPacket=path.join(root,'results/raw/review/2026-11-11_1548_LSPV5_497_NATIVE_SHARED_PAID_DP_ACCEPTED.json');
const seedBytes=fs.readFileSync(seedFile);const seed=JSON.parse(seedBytes);
const key=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const K=c=>JSON.stringify(c);
const sources=seed.records.filter(r=>r.kind==='SOURCE');
assert.equal(sources.length,41);
const E=seed.spec.edges.length,G=seed.spec.guard;
// ---------- DP elimination with clause-level sharing ----------
function dp(order){
 const recs=sources.map(r=>({kind:'SOURCE',c:r.c,parents:[],source:r.source}));
 const index=new Map();recs.forEach((r,i)=>index.set(K(r.c),i));
 let active=new Set(recs.map((_,i)=>i).filter(i=>recs[i].c.length===0||!recs[i].c.includes(G)?true:true));
 const guardIdx=recs.findIndex(r=>r.source===-1);active.delete(guardIdx);
 const subsumed=(c,set)=>{for(const j of set){const d=recs[j].c;if(d.length<c.length&&d.every(x=>c.includes(x)))return true}return false};
 for(const v of order){
  const P=[...active].filter(i=>recs[i].c.includes(v)),N=[...active].filter(i=>recs[i].c.includes(-v));
  const rest=new Set([...active].filter(i=>!recs[i].c.includes(v)&&!recs[i].c.includes(-v)));
  const fresh=[];
  for(const a of P)for(const b of N){
   const c=key([...recs[a].c.filter(x=>x!==v),...recs[b].c.filter(x=>x!==-v)]);
   if(c.some(x=>c.includes(-x)))continue;
   const k=K(c);
   if(index.has(k)){rest.add(index.get(k));continue}   // shared: reuse the earlier distinct node
   if(subsumed(c,rest))continue;
   recs.push({kind:'RES',c,parents:[a,b],pivot:v});index.set(k,recs.length-1);rest.add(recs.length-1);fresh.push(recs.length-1);
  }
  active=rest;
 }
 const neg=index.get(K([-G]));if(neg===undefined)return null;
 recs.push({kind:'RES',c:[],parents:[guardIdx,neg],pivot:G});
 return prune(recs);
}
function prune(recs){
 const live=new Set();const st=[recs.length-1];
 while(st.length){const i=st.pop();if(live.has(i))continue;live.add(i);recs[i].parents.forEach(p=>st.push(p))}
 const keep=recs.map((r,i)=>i).filter(i=>recs[i].kind==='SOURCE'||live.has(i));
 const map=new Map();keep.forEach((i,j)=>map.set(i,j));
 return keep.map(i=>{const r=recs[i];const o={kind:r.kind,c:r.c,parents:r.parents.map(p=>map.get(p))};if(r.kind==='SOURCE')o.source=r.source;else o.pivot=r.pivot;return o});
}
function packet(records,gateDefs){
 const nres=records.filter(r=>r.kind==='RES').length;
 return {spec:seed.spec,gate_defs:gateDefs,records,summary:{source:41,resolution:nres,def_views:0,paid_gates:gateDefs.length,paid_total:nres+gateDefs.length,live_records:records.length}};
}
let s=0x497497;const rnd=()=>(s=(Math.imul(s,1103515245)+12345)>>>0)/2**32;
const shuffle=a=>{a=a.slice();for(let i=a.length-1;i>0;i--){const j=Math.floor(rnd()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};
const vars=[...Array(E)].map((_,i)=>i+1);
let best=null,bestOrder=null,tried=0,hist={};const t0=Date.now();
const candidates=[vars,vars.slice().reverse(),[7,5,3,6,4,1,2,8,11,10,13,9,14,12,15]];
while(Date.now()-t0<12000&&tried<6000){
 const ord=tried<candidates.length?candidates[tried]:shuffle(vars);tried++;
 const r=dp(ord);if(!r)continue;const w=r.filter(x=>x.kind==='RES').length;hist[w]=(hist[w]||0)+1;
 if(!best||w<best.filter(x=>x.kind==='RES').length){best=r;bestOrder=ord}
}
// ---------- fanout ----------
function fanout(recs){const f=Array(recs.length).fill(0);recs.forEach(r=>r.parents.forEach(p=>f[p]++));
 const h={};recs.forEach((r,i)=>{if(r.kind==='RES'&&i<recs.length-1){h[f[i]]=(h[f[i]]||0)+1}});return {hist:h,f}}
function refDigits(recs){return recs.reduce((a,r)=>a+r.parents.reduce((b,p)=>b+String(p).length,0),0)}
function native(obj,tag){const f=path.join(os.tmpdir(),`lspv5_497_${tag}_${process.pid}.json`);const bytes=Buffer.from(JSON.stringify(obj));fs.writeFileSync(f,bytes);
 const r=cp.spawnSync(process.execPath,[checker,f],{encoding:'utf8'});fs.unlinkSync(f);
 let out=null;try{out=JSON.parse(r.stdout.trim().split('\n').pop())}catch(e){}
 return {tag,status:r.status,accept:r.status===0&&!!out,bytes:bytes.length,sha256:crypto.createHash('sha256').update(bytes).digest('hex'),paid:out&&out.paid,res:out&&out.res,assertions:out&&out.assertions,negativeTests:out&&out.negativeTests,stderrHead:(r.stderr||'').split('\n')[0].slice(0,160)}}
// Reorder: a different legal topological order of the same DAG (sources fixed first, derived nodes by reverse-DFS from sink).
function reorder(recs){
 const S=recs.filter(r=>r.kind==='SOURCE').length;const order=[];const seen=new Set();
 const visit=i=>{if(seen.has(i))return;seen.add(i);const ps=recs[i].parents.slice().reverse();ps.forEach(visit);if(i>=S)order.push(i)};
 visit(recs.length-1);
 const map=new Map();for(let i=0;i<S;i++)map.set(i,i);order.forEach((i,j)=>map.set(i,S+j));
 const out=recs.slice(0,S).map(r=>({...r}));order.forEach(i=>{const r=recs[i];out.push({kind:'RES',c:r.c,parents:r.parents.map(p=>map.get(p)),pivot:r.pivot})});return out}
// Tree expansion: duplicate every multi-consumer paid node per consumer (legal, costlier).
function treeExpand(recs){
 const S=recs.filter(r=>r.kind==='SOURCE').length;const out=recs.slice(0,S).map(r=>({...r}));
 const emit=i=>{if(i<S)return i;const r=recs[i];const ps=r.parents.map(emit);out.push({kind:'RES',c:r.c,parents:ps,pivot:r.pivot});return out.length-1};
 emit(recs.length-1);return out}
const gate=seed.gate_defs; // identical inert owner, for like-for-like CLI paid comparison with W61
assert.ok(best,'no DP refutation');
const P0=packet(best,gate),P0g=packet(best,[]);
const R1=reorder(best),P1=packet(R1,gate);
const T=treeExpand(best),PT=packet(T,gate);
const fan0=fanout(best),fan1=fanout(R1),fanT=fanout(T);
const ownerFloor=native(P0g,'shared_dp_nogate_expected_reject_by_owner_floor');
const runs=[native(P0,'shared_dp'),native(P1,'shared_dp_reordered'),native(PT,'tree_expanded'),native(seed,'seed_w61')];
// hostile controls: each must reject
const multi=best.findIndex((r,i)=>r.kind==='RES'&&fan0.f[i]>=2);
const consumers=best.map((r,i)=>r.parents.includes(multi)?i:-1).filter(i=>i>=0);
const hostile=[];
{const o=structuredClone(P0);o.summary.resolution+=fan0.f[multi]-1;o.summary.paid_total+=fan0.f[multi]-1;hostile.push(native(o,'h_charge_per_consumer'))}
{const o=structuredClone(P0);o.summary.resolution-=1;o.summary.paid_total-=1;hostile.push(native(o,'h_undercharge_one'))}
{const o=structuredClone(P0);o.records[consumers[1]].parents=o.records[consumers[1]].parents.map(p=>p===multi?o.records.length+3:p);hostile.push(native(o,'h_dangling_second_consumer'))}
{const o=structuredClone(P0);o.records[consumers[1]].pivot=-o.records[consumers[1]].pivot;hostile.push(native(o,'h_flip_consumer_pivot'))}
{const o=structuredClone(P0);o.records[multi].c=o.records[multi].c.slice(1);hostile.push(native(o,'h_weaken_shared_clause'))}

// ---------- random legal topological orders of the SAME shared DAG ----------
function randomTopo(recs){
 const S=recs.filter(r=>r.kind==='SOURCE').length,n=recs.length;
 const indeg=Array(n).fill(0),kids=[...Array(n)].map(()=>[]);
 for(let i=S;i<n;i++)for(const p of new Set(recs[i].parents))if(p>=S){indeg[i]++;kids[p].push(i)}
 let ready=[];for(let i=S;i<n-1;i++)if(indeg[i]===0)ready.push(i);
 const order=[];
 while(ready.length){const j=Math.floor(rnd()*ready.length);const i=ready.splice(j,1)[0];order.push(i);for(const k of kids[i])if(--indeg[k]===0&&k!==n-1)ready.push(k)}
 order.push(n-1);assert.equal(order.length,n-S);
 const map=new Map();for(let i=0;i<S;i++)map.set(i,i);order.forEach((i,j)=>map.set(i,S+j));
 const out=recs.slice(0,S).map(r=>({...r}));order.forEach(i=>{const r=recs[i];out.push({kind:'RES',c:r.c,parents:r.parents.map(p=>map.get(p)),pivot:r.pivot})});return out}
let lo=null,hi=null;const digitHist={};
for(let t=0;t<3000;t++){const o=randomTopo(best);const d=refDigits(o);digitHist[d]=(digitHist[d]||0)+1;if(!lo||d<refDigits(lo))lo=o;if(!hi||d>refDigits(hi))hi=o}
const topoRuns=[native(packet(lo,gate),'shared_topo_min_digits'),native(packet(hi,gate),'shared_topo_max_digits')];
const p575File=path.join(root,'results/raw/arc/2026-11-11_0900_LSPV1_575_BRIDGE_GUARDED_DP_NATIVE_ACCEPTED.json');
const p575=JSON.parse(fs.readFileSync(p575File));const fan575=fanout(p575.records);
const sameAs575=K(p575.records.map(r=>K(r.c)).sort())===K(best.map(r=>K(r.c)).sort());
const run575=native(p575,'lspv1_575_historical_packet');

// ---------- exact band-rigidity criterion (poset position ranges) ----------
function bands(recs){
 const S=recs.filter(r=>r.kind==='SOURCE').length,n=recs.length,f=fanout(recs).f;
 const anc=[...Array(n)].map(()=>new Set()),desc=[...Array(n)].map(()=>new Set());
 for(let i=S;i<n;i++)for(const p of recs[i].parents)if(p>=S){anc[i].add(p);anc[p].forEach(x=>anc[i].add(x))}
 for(let i=n-1;i>=S;i--)for(const p of recs[i].parents)if(p>=S){desc[p].add(i);desc[i].forEach(x=>desc[p].add(x))}
 const out=[];
 for(let k=1;10**k<=n-2;k++){const b=10**k;if(b<S)continue;
  const flex=[];for(let j=S;j<n-1;j++){const lo=S+anc[j].size,hi=n-2-(desc[j].size-1);if(lo<b&&hi>=b)flex.push(j)}
  out.push({boundary:b,flexible_nodes:flex.length,flexible_nonunit_fanout:flex.filter(j=>f[j]!==1).length,max_fanout_node_hi_position:Math.max(...[...Array(n).keys()].filter(j=>j>=S&&j<n-1&&f[j]>=2).map(j=>n-2-(desc[j].size-1)))})}
 return out}
const bandShared=bands(best);
const W=n=>n.filter(r=>r.kind==='RES').length;
const raw={run:'LSPV-5/497',timestamp:'2026-11-11T15:48:00-08:00',seed_file:path.relative(root,seedFile),seed_sha256:crypto.createHash('sha256').update(seedBytes).digest('hex'),
 search:{orders_tried:tried,res_count_histogram:hist,best_order:bestOrder,wall_ms:Date.now()-t0,scope:'DP variable elimination with clause-level dedup (sharing) and strict-subsumption skipping; NOT an exhaustive minimum'},
 shared_dp:{res:W(best),paid_with_owner:W(best)+gate.length,records:best.length,fanout_hist:fan0.hist,ref_digits:refDigits(best),multi_node:multi,multi_node_clause:best[multi].c,consumers},
 reordered:{res:W(R1),fanout_hist:fan1.hist,ref_digits:refDigits(R1),same_clause_multiset:K(best.map(r=>K(r.c)).sort())===K(R1.map(r=>K(r.c)).sort())},
 tree_expanded:{res:W(T),fanout_hist:fanT.hist,ref_digits:refDigits(T),extra_paid:W(T)-W(best)},
 seed_w61:{res:W(seed.records)},band_rigidity:bandShared,topo:{samples:3000,ref_digit_hist:digitHist,min:refDigits(lo),max:refDigits(hi),runs:topoRuns},lspv1_575:{file:path.relative(root,p575File),res:W(p575.records),fanout_hist:fan575.hist,same_clause_multiset_as_independent_dp:sameAs575,native:run575},native_runs:runs,owner_floor_control:ownerFloor,hostile_controls:hostile,node:process.version,platform:process.platform};
assert.ok(runs.every(r=>r.accept),'a positive native run rejected: '+JSON.stringify(runs));
assert.ok(topoRuns.every(r=>r.accept)&&run575.accept,'topo/575 native reject');
assert.ok(bandShared.every(x=>x.flexible_nonunit_fanout===0),'band criterion fails');
assert.ok(!ownerFloor.accept,'zero-owner packet unexpectedly accepted');
assert.ok(hostile.every(r=>!r.accept),'a hostile control was accepted');
assert.ok(Object.keys(fan0.hist).some(k=>+k>=2),'no multi-consumer paid node');
fs.writeFileSync(outPacket,JSON.stringify(P0));
fs.writeFileSync(outRaw,JSON.stringify(raw,null,1)+'\n');
console.log(JSON.stringify({bands:bandShared,topo:[raw.topo.min,raw.topo.max,topoRuns.map(r=>r.bytes)],p575:[raw.lspv1_575.res,fan575.hist,sameAs575],shared_res:raw.shared_dp.res,fan:fan0.hist,refDigits:[raw.shared_dp.ref_digits,raw.reordered.ref_digits],bytes:[runs[0].bytes,runs[2].bytes],tree:raw.tree_expanded.res,tried,accepts:runs.map(r=>r.accept),hostileRejects:hostile.map(r=>!r.accept)}));
