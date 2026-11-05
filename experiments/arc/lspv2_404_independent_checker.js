#!/usr/bin/env node
'use strict';
// Independent cardinality-layer DP verifies every auxiliary-free basis optimum at k=2,3,4.
const fs=require('fs'),crypto=require('crypto');
const raw=JSON.parse(fs.readFileSync(process.argv[2]||'results/raw/arc/2026-11-04_1712_LSPV2_WEIGHTED_BASIS404_raw.json','utf8'));
function bitcount(i){let n=0;while(i){i&=i-1;n++;}return n;}
function subsetsForClauses(n){
  const cs=[],count=Math.pow(3,n);
  for(let t=1;t<count;t++){
    let q=t,forms=[];for(let j=0;j<n;j++){forms.push(q%3);q=Math.floor(q/3);}
    const width=forms.filter(x=>x!==0).length;
    let falsified=0;
    for(let a=0;a<2**n;a++){
      let falseClause=true;
      for(let j=0;j<n;j++){
        if(forms[j]===1&&((a>>j)&1)===1)falseClause=false;
        if(forms[j]===2&&((a>>j)&1)===0)falseClause=false;
      }
      if(falseClause)falsified|=(1<<a);
    }
    cs.push({mask:falsified,cost:(2**(n-width)-1)+3*(width-1)});
  }
  return cs;
}
function check(n,expected){
  const clauses=subsetsForClauses(n),states=2**(2**n),inf=1e9;
  let dp=new Int32Array(states);dp.fill(inf);dp[0]=0;
  const buckets=Array.from({length:2**n+1},()=>[]);
  for(let i=0;i<states;i++)buckets[bitcount(i)].push(i);
  let checks=0;
  for(let layer of buckets)for(let s of layer){
    if(dp[s]===inf)throw Error('unreachable '+s);
    for(let c of clauses){
      let next=s|c.mask;
      if(next!==s&&dp[next]>dp[s]+c.cost)dp[next]=dp[s]+c.cost;
      checks++;
    }
  }
  let max=0,maximum=0,hist={};
  for(const d of dp){max=Math.max(max,d);hist[d]=(hist[d]||0)+1;}
  maximum=hist[max];
  let even=0,odd=0;
  for(let a=0;a<2**n;a++)if(bitcount(a)%2===0)even|=(1<<a);else odd|=(1<<a);
  let digest=crypto.createHash('sha256').update(Array.from(dp).join(',')).digest('hex');
  if(max!==expected.max_weighted_basis||maximum!==expected.maximizers||
     JSON.stringify([even,odd])!==JSON.stringify(expected.parity_bad_masks)||
     dp[even]!==max||dp[odd]!==max||digest!==expected.distance_sha256||
     JSON.stringify(hist)!==JSON.stringify(expected.histogram))throw Error('independent mismatch n='+n);
  if(((~even)&(states-1))===0||((~odd)&(states-1))===0)throw Error('parity SAT failure');
  if((even|odd)!==states-1||(even&odd)!==0)throw Error('UNSAT union failure');
  return {n,all_relations:states,clauses:clauses.length,checked_transition_candidates:checks,max,
          costs_match_sha256:digest,parity_bad_masks:[even,odd],maximizers:maximum};
}
let out={independent_implementation:true,runs:raw.runs.map(v=>check(v.k,v)),malformed_rejected:0};
for(let obj of [null,{}, {k:5,mask:0},{k:4,mask:65536},{k:-1,mask:0}]){
  try{if(!obj||!Number.isInteger(obj.k)||obj.k<2||obj.k>4||
      !Number.isInteger(obj.mask)||obj.mask<0||obj.mask>=2**(2**obj.k))throw Error('bad');
  }catch(e){out.malformed_rejected++;}
}
if(out.malformed_rejected!==5)throw Error('malformed gate');
process.stdout.write(JSON.stringify(out,null,2)+'\n');
