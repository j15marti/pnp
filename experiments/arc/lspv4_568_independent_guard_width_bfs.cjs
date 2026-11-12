#!/usr/bin/env node
'use strict';
// LSPV-4/568 independent reachability check, restricted archived /386 fixed DAG.
// Requires checked-in exact ORIGINAL 560 W38 packet. Does not execute original checker.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const file=path.join(root,'results/raw/arc/2026-11-12_0436_LSPV4_560_W38_ACCEPTED.json');
const obj=JSON.parse(fs.readFileSync(file,'utf8'));
assert.equal(obj.spec.guard,7);
const rows=obj.records, R=rows.filter(r=>r.kind==='RES');
assert.equal(R.length,35);
const bit=Array.from({length:35},(_,j)=>1n<<BigInt(j));
const parents=R.map(r=>r.parents.filter(i=>i>=23).map(i=>i-23));
const req=parents.map(p=>p.reduce((m,i)=>m|bit[i],0n));
const renamed=c=>c.map(v=>Math.abs(v)===7?Math.sign(v)*Number.MAX_SAFE_INTEGER:v).sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const sizes=R.map(r=>JSON.stringify(renamed(r.c)).length);
const ids=mask=>{const out=[];for(let j=0;j<35;j++)if(mask&bit[j])out.push(j);return out;};
const size=mask=>ids(mask).reduce((s,j)=>s+sizes[j],0);
function search(cap){
  const seen=new Set(['0']),q=[0n];let head=0,transitions=0,solved=false;
  while(head<q.length&&!solved){
    const liveMask=q[head++],live=ids(liveMask);
    for(let j=0;j<35&&!solved;j++){
      if(liveMask&bit[j]||(liveMask&req[j])!==req[j])continue;
      const extras=live.filter(i=>!parents[j].includes(i));
      for(let selector=0;selector<(1<<extras.length)&&!solved;selector++){
        let before=req[j];
        for(let k=0;k<extras.length;k++)if(selector&(1<<k))before|=bit[extras[k]];
        const count=ids(before).length,bytes=size(before);
        const options=[];
        if(count<4&&bytes+sizes[j]<=cap)options.push(before);
        if(count<=4&&bytes<=cap)for(const p of parents[j])
          if(sizes[p]>=sizes[j])options.push(before&~bit[p]);
        for(const retained of options){
          const keep=ids(retained);
          for(let t=0;t<(1<<keep.length);t++){
            let after=bit[j];
            for(let k=0;k<keep.length;k++)if(t&(1<<k))after|=bit[keep[k]];
            transitions++;
            if(after&bit[34]){solved=true;break;}
            const key=after.toString();
            if(!seen.has(key)){seen.add(key);q.push(after);}
          }
          if(solved)break;
        }
      }
    }
  }
  return {cap,feasible:solved,reachable_states:seen.size,expanded_states:head,
          legal_transition_candidates:transitions};
}
const A=search(100),B=search(101);
assert.deepEqual(A,{cap:100,feasible:false,reachable_states:5579,
  expanded_states:5579,legal_transition_candidates:819306});
assert.equal(B.feasible,true);
console.log(JSON.stringify({run:'LSPV-4/568 independent Node reachability',
  model:'four derived registers; source+facet read-only; paid recomputation; nonexpanding overwrite',
  validation:'NO full historical R_mix341 inference grammar',
  results:[A,B]},null,2));
