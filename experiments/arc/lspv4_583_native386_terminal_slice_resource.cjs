#!/usr/bin/env node
'use strict';
/* LSPV-4/583, historical Route A. Executable audit of the actual recovered
   /386 SOURCE/DEF/RES sibling only, NOT the historical unified R_mix341. */
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const cp=require('node:child_process'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const file85=path.join(root,'results/raw/arc/2026-11-13_0212_LSPV2_595_TRIPLEX_W85_ACCEPTED.json');
const file81=path.join(root,'results/raw/arc/2026-11-13_0308_LSPV2_596_NATIVE386_W81_ACCEPTED.json');
const file29=path.join(root,'results/raw/arc/2026-11-13_0332_LSPV4_583_NATIVE386_TERMINAL_SLICE_W29.json');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const hash=x=>crypto.createHash('sha256').update(x).digest('hex');
function read(p,want){const b=fs.readFileSync(p);if(want)assert.equal(hash(b),want,p+' digest');return b;}
const checkerHash='22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113';
read(checker,checkerHash);
const A=JSON.parse(read(file85,'4bd50ef54044187a5b9811d87b19c640e55bd4f70d024d057ff5fb57226e5d46'));
const B=JSON.parse(read(file81,'85d353148d9e4ddc6f39f1d9666158665439fdab41f9e72ade6ae7ca56990562'));
const same=(x,y)=>JSON.stringify(x)===JSON.stringify(y);
const sort=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const copy=x=>JSON.parse(JSON.stringify(x));
function strictVerify(d){
  assert.deepEqual(d.spec,A.spec);assert.deepEqual(d.gate_defs,A.gate_defs);
  const {h,edges,charge,guard}=d.spec,occ=Array.from({length:h},()=>[]);
  edges.forEach(([a,b],i)=>{occ[a].push(i+1);occ[b].push(i+1);});
  const expected=[];
  for(let v=0;v<h;v++){
    assert.equal(occ[v].length,3);
    for(let t=0;t<8;t++){
      const bits=[t&1,(t>>1)&1,(t>>2)&1];
      if((bits[0]^bits[1]^bits[2])!==charge[v]){
        const c=sort(occ[v].map((x,k)=>bits[k]?-x:x).concat([-guard]));
        expected.push(v+':'+JSON.stringify(c));
      }
    }
  }
  expected.push('-1:'+JSON.stringify([guard]));
  let source=0,res=0,def=0,span=Array(d.records.length).fill(0);
  const actual=[];
  d.records.forEach((r,i)=>{
    assert.ok(['SOURCE','DEF','RES'].includes(r.kind),'opcode');
    assert.deepEqual(r.c,sort(r.c),'clause sort');
    assert.ok(!r.c.some(x=>r.c.includes(-x)),'no tautology');
    assert.ok(r.parents.every(j=>Number.isSafeInteger(j)&&j>=0&&j<i),'chronological parent');
    if(r.kind==='SOURCE'){source++;assert.equal(r.parents.length,0);actual.push(r.source+':'+JSON.stringify(r.c));}
    else if(r.kind==='DEF'){def++;assert.equal(r.parents.length,0);}
    else{
      res++;assert.equal(r.parents.length,2);
      const [left,right]=r.parents.map(j=>d.records[j].c);
      assert.ok(left.includes(r.pivot)&&right.includes(-r.pivot),'signed pivot');
      const result=sort(left.filter(x=>x!==r.pivot).concat(right.filter(x=>x!==-r.pivot)));
      assert.ok(!result.some(x=>result.includes(-x)),'taut resolvent');
      assert.deepEqual(r.c,result,'authentic resolvent');
      span[i]=1+Math.max(...r.parents.map(j=>span[j]));
    }
  });
  assert.deepEqual(actual.sort(),expected.sort(),'exact signed 49-clause source');
  assert.equal(d.records.at(-1).c.length,0,'terminal empty');
  assert.deepEqual(d.summary,{source,def_views:def,resolution:res,
    paid_gates:d.gate_defs.length,paid_total:res+d.gate_defs.length,
    live_records:d.records.length},'complete counters');
  return{source,res,def,span:Math.max(...span)};
}
function slice(d){
  const rows=d.records,wanted=new Set([rows.length-1]),stack=[rows.length-1];
  while(stack.length)for(const p of rows[stack.pop()].parents||[]){
    if(!wanted.has(p)){wanted.add(p);stack.push(p);}
  }
  const kept=rows.flatMap((r,i)=>r.kind==='SOURCE'||r.kind==='DEF'||wanted.has(i)?[{r,i}]:[]);
  const link=new Map(kept.map(({i},j)=>[i,j]));
  const records=kept.map(({r})=>({...copy(r),parents:r.parents.map(j=>link.get(j))}));
  const nres=records.filter(r=>r.kind==='RES').length;
  const packet={spec:copy(d.spec),gate_defs:copy(d.gate_defs),records,
    summary:{source:records.filter(r=>r.kind==='SOURCE').length,
      def_views:records.filter(r=>r.kind==='DEF').length,resolution:nres,
      paid_gates:d.gate_defs.length,paid_total:nres+d.gate_defs.length,
      live_records:records.length}};
  return{packet,removed:rows.length-kept.length,ancestors:[...wanted].sort((a,b)=>a-b)};
}
const sliced=slice(B),C=sliced.packet;
assert.deepEqual(C,JSON.parse(read(file29)),'published W29 full-content readback');
assert.equal(sliced.removed,52);
[A,B,C].forEach(strictVerify);
assert.deepEqual(B.records.filter(r=>r.kind==='SOURCE'),C.records.filter(r=>r.kind==='SOURCE'));
function cost(d){
  const rows=d.records,ids=rows.flatMap((r,i)=>r.kind==='RES'?[i]:[]);
  const last=Array(rows.length).fill(-1),use=Array(rows.length).fill(0);
  let parentApplications=0,parentIDDigits=0;
  rows.forEach((r,i)=>(r.parents||[]).forEach(j=>{
    last[j]=i;use[j]++;
    if(r.kind==='RES'){parentApplications++;parentIDDigits+=String(j).length;}
  }));
  let fresh=0,inplace=0,nonexpanding=0,retention=0,retentionBytes=0,livePeak=0,payloadPeak=0;
  ids.forEach((i,k)=>{
    const before=ids.slice(0,k).filter(j=>last[j]>=i);
    const after=ids.slice(0,k+1).filter(j=>last[j]>i||(i===ids.at(-1)&&i===j));
    const reusable=rows[i].parents.filter(j=>rows[j].kind==='RES'&&last[j]===i);
    fresh=Math.max(fresh,before.length+1);
    inplace=Math.max(inplace,before.length+1-(reusable.length?1:0));
    nonexpanding=Math.max(nonexpanding,before.length+1-
      (reusable.some(j=>JSON.stringify(rows[j].c).length>=JSON.stringify(rows[i].c).length)?1:0));
    retention+=after.length;livePeak=Math.max(livePeak,after.length);
    const payload=after.reduce((s,j)=>s+JSON.stringify(rows[j].c).length,0);
    retentionBytes+=payload;payloadPeak=Math.max(payloadPeak,payload);
  });
  return{paid:d.summary.paid_total,records:rows.length,
    parentApplications,parentIDDigits,
    freshPeak:fresh,inplacePeak:inplace,nonexpandingPeak:nonexpanding,
    livePeak,retentionSlotSteps:retention,
    retainedClauseJSONByteSteps:retentionBytes,retainedClauseJSONPeak:payloadPeak};
}
const costs={W85:cost(A),W81:cost(B),W29:cost(C)};
assert.deepEqual([costs.W85.paid,costs.W81.paid,costs.W29.paid],[85,81,29]);
assert.deepEqual([costs.W85.parentApplications,costs.W81.parentApplications,costs.W29.parentApplications],[168,160,56]);
assert.deepEqual([costs.W85.freshPeak,costs.W81.freshPeak,costs.W29.freshPeak],[9,10,9]);
assert.deepEqual([costs.W85.retentionSlotSteps,costs.W81.retentionSlotSteps,costs.W29.retentionSlotSteps],[433,477,145]);
assert.deepEqual([costs.W85.retainedClauseJSONByteSteps,costs.W81.retainedClauseJSONByteSteps,costs.W29.retainedClauseJSONByteSteps],[6880,7078,2010]);
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv4-583-'));const cases=[];
function run(name,obj,accept){
  const p=path.join(tmp,name+'.json');fs.writeFileSync(p,JSON.stringify(obj)+'\n');
  const x=cp.spawnSync(process.execPath,[checker,p],
    {encoding:'utf8',timeout:25000,maxBuffer:3000000});
  const outcome=x.status===0;
  assert.equal(outcome,accept,name+': '+String(x.stderr).slice(0,300));
  cases.push({name,accepted:outcome,assertions:outcome?JSON.parse(x.stdout).assertions:null,
    sha256:hash(fs.readFileSync(p)),bytes:fs.statSync(p).size});
}
try{
  run('original_W85',A,true);run('original_W81',B,true);run('new_W29',C,true);
  const negatives=[
    ['source_forgery',d=>d.records[0].c=[-d.spec.guard]],
    ['pivot_forgery',d=>d.records.at(-1).pivot=99999],
    ['future_parent',d=>d.records.at(-1).parents[1]=d.records.length],
    ['cost_underpayment',d=>d.summary.paid_total--],
    ['unsupported_GF2_rule',d=>d.records.at(-1).kind='XOR'],
    ['paid_owner_removal',d=>d.gate_defs.shift()]
  ];
  negatives.forEach(([name,fn])=>{const d=copy(C);fn(d);run(name,d,false);});
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
const result={status:'PASS: original /386 CLI, not complete historical R_mix341',
  checkerSHA256:checkerHash,node:process.version,
  packetSHA256:{W85:hash(read(file85)),W81:hash(read(file81)),W29:hash(read(file29))},
  costs,sliced:{removed:sliced.removed,ancestors:sliced.ancestors.length},cases};
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({status:result.status,costs,positive:3,negative:6},null,2));
