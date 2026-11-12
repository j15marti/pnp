#!/usr/bin/env node
'use strict';
// LSPV-4/559: executable native /386 paid-fanout and exact schedule audit.
// Run from any directory: node experiments/arc/lspv4_559_shared_native_paid_fanout_audit.cjs
const fs=require('fs'),path=require('path'),os=require('os'),cp=require('child_process');
const crypto=require('crypto'),assert=require('assert');
const root=path.resolve(__dirname,'../..');
const input=path.join(root,'results/raw/arc/2026-11-12_0212_LSPV2_571_ACCEPTED_LIVE_JOINT_PORT_ORBIT.json');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const clone=x=>JSON.parse(JSON.stringify(x));
const serialize=x=>JSON.stringify(x)+'\n';
const base=JSON.parse(fs.readFileSync(input,'utf8'));
assert.equal(serialize(base),fs.readFileSync(input,'utf8'));
assert.deepEqual(base.records[28].c,base.records[7].c);
assert.deepEqual(base.records[30].parents,[7,0]);
const shared=clone(base);
shared.records[30].parents[0]=28; // Paid node 28 now consumed by nodes 30 and 32.
function graph(p){
  const ids=p.records.map((r,i)=>r.kind==='RES'?i:-1).filter(i=>i>=0);
  const ix=new Map(ids.map((v,i)=>[v,i]));
  const deps=[],pr=[],cs=Array(ids.length).fill(0n),len=[];
  for(let i=0;i<ids.length;i++){
    const d=p.records[ids[i]].parents.filter(j=>ix.has(j)).map(j=>ix.get(j));
    deps.push(d);pr.push(d.reduce((s,j)=>s|(1n<<BigInt(j)),0n));
    len.push(JSON.stringify(p.records[ids[i]].c).length);
    for(const j of d)cs[j]|=1n<<BigInt(i);
  }
  return {ids,deps,pr,cs,len};
}
function optimize(g,cap,mode){
  const n=g.ids.length,bits=Array.from({length:n},(_,i)=>1n<<BigInt(i));
  const layers=[new Map([[0n,{area:0,bytes:0,order:[]}]]),...Array.from({length:n},()=>new Map())];
  let states=0,arcs=0;
  for(let level=0;level<n;level++)for(const [s,past] of layers[level]){
    states++;let area=0,bytes=0;
    for(let i=0;i<n;i++)if((s&bits[i])&&(g.cs[i]&~s)){area++;bytes+=g.len[i]}
    for(let v=0;v<n;v++){
      const bit=bits[v];if((s&bit)||(s&g.pr[v])!==g.pr[v])continue;
      const reuse=mode!=='fresh'&&g.deps[v].some(u=>
        (g.cs[u]&~s)===bit&&(mode!=='nonexpand'||g.len[u]>=g.len[v]));
      if(area+1-Number(reuse)>cap)continue;
      const next=s|bit,old=layers[level+1].get(next);
      const x={area:past.area+area,bytes:past.bytes+bytes,order:[...past.order,g.ids[v]]};
      arcs++;
      if(!old||x.area<old.area||(x.area===old.area&&x.bytes<old.bytes))
        layers[level+1].set(next,x);
    }
  }
  const winner=layers[n].get((1n<<BigInt(n))-1n);
  return {cap,mode,states,arcs,feasible:!!winner,...(winner||{})};
}
function permute(p,order){
  const perm=[...Array(23).keys(),...order],ix=new Map(perm.map((v,i)=>[v,i]));
  assert.deepEqual([...perm].sort((a,b)=>a-b),[...Array(57).keys()]);
  const q=clone(p);q.records=perm.map(i=>{
    const r=clone(p.records[i]);r.parents=r.parents.map(j=>ix.get(j));return r;
  });return q;
}
function replay(p){
  for(let i=0;i<p.records.length;i++){
    const r=p.records[i];assert(r.parents.every(j=>j>=0&&j<i));
    if(r.kind!=='RES')continue;
    const [A,B]=r.parents.map(j=>p.records[j].c),pv=r.pivot;
    assert(A.includes(pv)&&B.includes(-pv));
    const C=[...new Set([...A.filter(x=>x!==pv),...B.filter(x=>x!==-pv)])]
      .sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
    assert(!C.some(x=>C.includes(-x)));
    assert.deepEqual(r.c,C);
  }
  assert.deepEqual(p.records.at(-1).c,[]);
}
function native(p){
  const d=fs.mkdtempSync(path.join(os.tmpdir(),'lspv4-559-'));
  try{
    const filename=path.join(d,'certificate.json');
    const data=serialize(p);fs.writeFileSync(filename,data);
    const r=cp.spawnSync(process.execPath,[checker,filename],{encoding:'utf8',timeout:30000});
    return {accept:r.status===0,exit:r.status,bytes:Buffer.byteLength(data),
      sha256:crypto.createHash('sha256').update(data).digest('hex'),
      stdout:r.stdout.trim(),stderr:(r.stderr||'').slice(-200)};
  }finally{fs.rmSync(d,{recursive:true,force:true})}
}
const prior=optimize(graph(base),4,'nonexpand');
const sharedModes=[['fresh',4],['fresh',5],['inplace',3],['inplace',4],
  ['nonexpand',3],['nonexpand',4],['nonexpand',5]]
  .map(([m,c])=>optimize(graph(shared),c,m));
const all=optimize(graph(shared),34,'fresh');
assert.deepEqual([prior.area,prior.bytes],[66,700]);
assert.deepEqual(sharedModes.map(x=>x.feasible),[false,true,false,true,false,true,true]);
assert.deepEqual([sharedModes[5].area,sharedModes[5].bytes],[79,839]);
assert.deepEqual([all.area,all.bytes],[79,837]);
const optimized=permute(shared,sharedModes[5].order);
[base,shared,optimized].forEach(replay);
const positives=[native(base),native(shared),native(optimized)];
assert(positives.every(x=>x.accept));
const bad={
  underpayment:q=>{q.summary.paid_total--},
  forged_source:q=>{q.records[0].c=[-q.spec.guard]},
  invalid_terminal_pivot:q=>{q.records.at(-1).pivot=999999},
  future_reference:q=>{q.records[30].parents[0]=56},
  invalid_alias:q=>{q.records[30].parents[0]=27}
};
const negatives={};
for(const [name,mut] of Object.entries(bad)){
  const q=clone(shared);mut(q);negatives[name]=!native(q).accept;
  assert(negatives[name],name);
}
const fan=Array(57).fill(0);
for(const r of shared.records)for(const j of r.parents)fan[j]++;
assert.equal(fan[28],2);
assert.equal(Buffer.byteLength(serialize(shared)),3579);
console.log(JSON.stringify({status:'PASS',
  checker_blob:'338305c0ce101704205e57543756b8127074a986',
  original_blob:'ae515a483bf7ec5a32232266adb17ef664ba7e9a',
  native_rule_fragment:'SOURCE, paid AND2 owner, DEF facet, signed RES',
  substitution:{record:30,parent_before:7,parent_after:28,paid_fanout_28:fan[28]},
  logical_W:37,paid_RES:34,paid_owners:3,
  prior_nonexpand4:prior,shared_modes:sharedModes,
  shared_unconstrained:all,native_positive:positives,native_hostile_rejected:negatives,
  p_np:'OPEN'},null,2));
