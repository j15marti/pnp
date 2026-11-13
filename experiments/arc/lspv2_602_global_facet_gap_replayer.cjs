#!/usr/bin/env node
'use strict';
/* LSPV-2/602. Native archived /386 SOURCE/DEF/RES ONLY.
   Uses the *unchanged* original checker as a separate Node process.
   Input: extracted LSPV2_601 evidence601 folder; output: packet and manifest folder.
   This is a replayer and optimizer, NOT the historical R_mix341 checker. */
const fs=require('node:fs'), path=require('node:path'), cp=require('node:child_process');
const crypto=require('node:crypto'), assert=require('node:assert/strict');
const root=path.resolve(process.argv[2]||path.join(__dirname,'evidence601'));
const out=path.resolve(process.argv[3]||path.join(__dirname,'raw602'));
fs.mkdirSync(out,{recursive:true});
const chk=path.join(root,'native/checker386.js');
const src=fs.readFileSync(path.join(root,'native/SOURCE.cnf'));
const base=JSON.parse(fs.readFileSync(path.join(root,'generated/M8_shared_facets.json'),'utf8'));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
assert.equal(sha(fs.readFileSync(chk)),'22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113');
assert.equal(sha(src),'3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c');
const cpobj=x=>JSON.parse(JSON.stringify(x));
const defs=base.records.map((r,i)=>r.kind==='DEF'?i:-1).filter(x=>x>=0);
assert.equal(defs.length,2);
assert.equal(base.summary.paid_total,249);
assert.equal(base.records.length,267);
// A separate byte-for-byte signed SOURCE stream must match the in-band SOURCE occurrences.
const tokens=src.toString().trim().split(/\s+/);assert.deepEqual(tokens.slice(0,4),['p','cnf','7','17']);
const cnf=[];let row=[];for(const t of tokens.slice(4)){const k=Number(t);assert(Number.isSafeInteger(k));if(k===0){cnf.push(row);row=[];}else row.push(k);}
assert.equal(row.length,0);assert.equal(cnf.length,17);
const keys=x=>x.map(a=>JSON.stringify(a)).sort();
assert.deepEqual(keys(cnf),keys(base.records.filter(r=>r.kind==='SOURCE').map(r=>r.c)));
// Introduce nonuniform paid-step spacing using valid, redundant original RES inferences.
// No original inference or parent is erased. Added RES work is explicitly paid.
function nonuniformNative(original){
  const d=cpobj(original);d.records=[];const map=new Map();let step=0,first=null,added=0;
  const padding=new Map([[31,2],[93,5],[186,11]]);
  for(let i=0;i<original.records.length;i++){
    const r=cpobj(original.records[i]);
    if(r.kind==='RES'){
      r.parents=r.parents.map(j=>{assert(map.has(j));return map.get(j)});
      if(first===null)first=cpobj(r);
    }
    const next=d.records.length;d.records.push(r);map.set(i,next);
    if(r.kind==='RES'){
      step++;
      if(padding.has(step)){
        for(let n=0;n<padding.get(step);n++){d.records.push(cpobj(first));added++;}
      }
    }
  }
  assert.equal(step,248);assert.equal(added,18);
  d.summary.resolution=248+added;
  d.summary.paid_total=d.summary.resolution+d.summary.paid_gates;
  d.summary.live_records=d.records.length;
  return d;
}
const padded=nonuniformNative(base);
const ids=padded.records.map((r,i)=>r.kind==='DEF'?i:-1).filter(i=>i>=0);
assert.equal(ids.length,2);
const useTimes=()=>{
  const uses=ids.map(()=>[]);let t=0;
  for(const r of padded.records){if(r.kind!=='RES')continue;t++;
    r.parents.forEach(p=>{const f=ids.indexOf(p);if(f>=0)uses[f].push(t)});
  }
  uses.forEach(a=>assert.equal(a.length,8));return uses;
};
const uses=useTimes();
function gapsFor(times,f){return Array.from({length:times.length-1},(_,i)=>({f,i,gap:times[i+1]-times[i]-1}));}
const gaps=uses.flatMap((t,f)=>gapsFor(t,f));
assert.equal(gaps.length,14);
const highest=gaps.slice().sort((a,b)=>b.gap-a.gap||a.f-b.f||a.i-b.i);
const lowest=gaps.slice().sort((a,b)=>a.gap-b.gap||a.f-b.f||a.i-b.i);
function chosenSets(k,policy){assert(Number.isInteger(k)&&k>=2&&k<=16);
 const chosen=(policy==='top'?highest:lowest).slice(0,k-2),sets=[new Set(),new Set()];
 for(const {f,i} of chosen)sets[f].add(i);
 return sets;
}
function groups(sets){return sets.map((cuts,f)=>{
  let g=0;return uses[f].map((_,i)=>{if(i>0&&cuts.has(i-1))g++;return g});
});}
function instantiate(sets){
 const group=groups(sets),d=cpobj(padded);d.records=[];const oldToNew=new Map();
 const newDefs=ids.map(()=>new Map());const used=ids.map(()=>0);
 for(let old=0;old<padded.records.length;old++){
  const r=padded.records[old];if(r.kind==='DEF')continue;
  const row=cpobj(r);
  if(r.kind==='RES'){
   row.parents=row.parents.map(p=>{
    const f=ids.indexOf(p);
    if(f<0){assert(oldToNew.has(p));return oldToNew.get(p);}
    const n=used[f]++,g=group[f][n];
    if(!newDefs[f].has(g)){
      const idx=d.records.length;d.records.push(cpobj(padded.records[ids[f]]));newDefs[f].set(g,idx);
    }
    return newDefs[f].get(g);
   });
  }
  const at=d.records.length;d.records.push(row);oldToNew.set(old,at);
 }
 used.forEach((n,f)=>assert.equal(n,uses[f].length));
 const count=newDefs.reduce((sum,x)=>sum+x.size,0);
 d.summary.def_views=count;d.summary.live_records=d.records.length;
 assert.equal(d.summary.resolution,266);
 assert.equal(d.summary.paid_total,267);
 assert.equal(d.records.at(-1).c.length,0);
 return d;
}
function areaFromTimes(useArrays,sets){let A=0;for(let f=0;f<useArrays.length;f++){
  const t=useArrays[f],g=groups(sets)[f];
  const map=new Map();for(let i=0;i<t.length;i++){
    if(!map.has(g[i]))map.set(g[i],[t[i],t[i]]);else map.get(g[i])[1]=t[i];
  }
  for(const [lo,hi] of map.values())A+=hi-lo+1;
 }return A;
}
function areaFromNative(pkt){const views=new Map();let t=0;
 for(let i=0;i<pkt.records.length;i++){
  const r=pkt.records[i];if(r.kind==='DEF')views.set(i,[]);
  else if(r.kind==='RES'){t++;for(const p of r.parents)if(views.has(p))views.get(p).push(t);}
 }
 let area=0,peak=0;const life=[];for(const u of views.values()){
  assert(u.length>0,'unused DEF copy');area+=u.at(-1)-u[0]+1;life.push([u[0],u.at(-1)]);
 }
 for(let j=1;j<=t;j++)peak=Math.max(peak,life.filter(([a,b])=>a<=j&&j<=b).length);
 return {area,peak,views:views.size,resolution:t};
}
function minArea(uses,k){const gs=uses.flatMap((t,f)=>gapsFor(t,f)).sort((a,b)=>b.gap-a.gap),base=uses.reduce((s,t)=>s+t.at(-1)-t[0]+1,0);return base-gs.slice(0,k-uses.length).reduce((s,z)=>s+z.gap,0);}
function brute(t,k){const gaps=t.length-1;let best=Infinity;
 for(let mask=0;mask<2**gaps;mask++){
  let cuts=0,save=0;for(let i=0;i<gaps;i++)if(mask&(1<<i)){cuts++;save+=t[i+1]-t[i]-1;}
  if(cuts===k-1)best=Math.min(best,t.at(-1)-t[0]+1-save);
 }return best;
}
// Exhaustively falsify greedy in 200 small deterministic nonuniform instances.
let bruteCases=0;for(let n=2;n<=8;n++)for(let s=0;s<20;s++){
 const t=[1+s%3];for(let j=1;j<n;j++)t.push(t.at(-1)+1+((s*11+j*7+j*j)%9));
 for(let k=1;k<=n;k++){
  const ours=t.at(-1)-t[0]+1-gapsFor(t,0).map(g=>g.gap).sort((a,b)=>b-a).slice(0,k-1).reduce((a,b)=>a+b,0);
  assert.equal(ours,brute(t,k));bruteCases++;
 }
}
const rows=[];let checks=0;
function test(name,obj,accepted){const bytes=Buffer.from(JSON.stringify(obj)+'\n');
 const f=path.join(out,name+'.json');fs.writeFileSync(f,bytes);
 const r=cp.spawnSync(process.execPath,[chk,f],{encoding:'utf8',timeout:45000,maxBuffer:4e6});
 assert.equal(r.status===0,accepted,`${name}: ${r.stderr.slice(0,300)}`);
 const assertions=accepted?JSON.parse(r.stdout.trim()).assertions:0;checks+=assertions;
 const item={name,verdict:accepted?'ACCEPT':'REJECT',bytes:bytes.length,sha256:sha(bytes),
  native_assertions:assertions,error:accepted?null:(r.stderr.match(/Error: ([^\n]+)/)||[])[1]||r.stderr.slice(0,160)};
 rows.push(item);return item;
}
test('base_original_W249',base,true);
test('padded_nonuniform_W267',padded,true);
const frontier=[];for(let k=2;k<=16;k++){
 const cuts=chosenSets(k,'top'),obj=instantiate(cuts),p=areaFromNative(obj);
 assert.equal(p.views,k);assert.equal(p.area,areaFromTimes(uses,cuts));assert.equal(p.area,minArea(uses,k));
 const result=test(`optimal_views_${String(k).padStart(2,'0')}`,obj,true);
 frontier.push({views:k,area:p.area,peak:p.peak,bytes:result.bytes,sha256:result.sha256,
  saving_relative_to_2:minArea(uses,2)-p.area});
}
const k=8,worstObj=instantiate(chosenSets(k,'low')),
 worst=areaFromNative(worstObj),best=frontier.find(x=>x.views===k);
assert(worst.area>best.area);const wr=test('suboptimal_same_view_count_08',worstObj,true);
const seed=instantiate(chosenSets(8,'top'));
for(const [n,mut] of [
 ['wrong_signed_SOURCE',d=>{d.records.find(r=>r.kind==='SOURCE').c=[-d.spec.guard]}],
 ['wrong_DEF_facet',d=>{d.records.find(r=>r.kind==='DEF').c=[99999999]}],
 ['wrong_RES_pivot',d=>{d.records.at(-1).pivot=100} ],
 ['future_RES_parent',d=>{d.records.at(-1).parents[0]=d.records.length+3}],
 ['underpaid',d=>{d.summary.paid_total--}],
 ['unknown_LOCAL_CONVERT',d=>{d.records.find(r=>r.kind==='DEF').kind='LOCAL-CONVERT'}]
]){const d=cpobj(seed);mut(d);test(n,d,false)}
const output={schema:'LSPV2-602-NATIVE386-GLOBAL-DEF-GAP-OPT/v1',status:'PROVED/RESTRICTED; original /386 OS-Node checked; complete R_mix341 OPEN',
 model:'Fixed paid RES chronology and true DEF facet values. Facet view intervals assessed at paid RES checkpoints. A newly emitted view is inserted at its first consumer, no deletions; output measures retention slots, not RAM or verifier time.',
 independent_external_source_sha256:sha(src),checker_sha256:sha(fs.readFileSync(chk)),
 baseline_packet_sha256:sha(fs.readFileSync(path.join(root,'generated/M8_shared_facets.json'))),
 paid_work_original:249,paid_work_padded:267,padding_after_paid_steps:{31:2,93:5,186:11},
 original_source_count:17,facet_classes:2,uses,
 gaps_descending:highest,min_area_formula:'sum_f(t_last-t_first+1) - sum of globally K-2 largest nonnegative consecutive-use gaps',
 brute_force_finite_cases:bruteCases,frontier,
 same_count_adversary:{views:8,optimal_area:best.area,suboptimal_area:worst.area,suboptimal_peak:worst.peak,suboptimal_bytes:wr.bytes,
 suboptimal_sha256:wr.sha256},
 cases:rows,totals:{accepted:rows.filter(r=>r.verdict==='ACCEPT').length,rejected:rows.filter(r=>r.verdict==='REJECT').length,original_checker_assertions:checks}};
fs.writeFileSync(path.join(out,'LSPV2_602_GLOBAL_GAP_RAW.json'),JSON.stringify(output,null,2)+'\n');
console.log(JSON.stringify({pass:true,uses,top_gaps:highest.slice(0,9),bruteCases,frontier,adversary:output.same_count_adversary,totals:output.totals},null,2));
