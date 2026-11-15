#!/usr/bin/env node
'use strict';
// TMR-4/051, source exactly re-executed in hosted V8. Exhaustive, no randomness.
const runTMR4051 = function runTMR4051(){
 const assert=(b,msg)=>{if(!b)throw Error(msg)};
 const permutations=a=>{if(!a.length)return [[]];return a.flatMap((v,i)=>permutations(a.slice(0,i).concat(a.slice(i+1))).map(q=>[v,...q]))};
 function matrixRows(n,order,p,fn){
  const out=[];
  for(let u=0;u<(1<<p);u++){
    let base=0;for(let j=0;j<p;j++)if((u>>j)&1)base|=1<<order[j];
    let row=0n;
    for(let v=0;v<(1<<(n-p));v++){
      let full=base;for(let j=p;j<n;j++)if((v>>(j-p))&1)full|=1<<order[j];
      if(fn(full))row|=1n<<BigInt(v);
    }out.push(row)
  }return out
 }
 function rankGF2(rows){let basis=new Map(),r=0;for(let v of rows){while(v!==0n){let p=v.toString(2).length-1;if(basis.has(p))v^=basis.get(p);else{basis.set(p,v);r++;break}}}return r}
 function reducedNodes(n,order,fn){
  const unique=new Map();let next=2;
  function rec(p,assignment){if(p===n)return fn(assignment)?1:0;
    const lo=rec(p+1,assignment),hi=rec(p+1,assignment|(1<<order[p]));
    if(lo===hi)return lo;
    const key=p+","+lo+","+hi;
    if(!unique.has(key))unique.set(key,next++);
    return unique.get(key);
  }
  const root=rec(0,0);assert(root===0||root===1||root>=2,"valid BDD");return unique.size
 }
 function audit(n,order,fn){
  let ranks=[],residuals=[],frontal=[];
  for(let p=0;p<=n;p++){
   const rows=matrixRows(n,order,p,fn),rank=rankGF2(rows),distinct=new Set(rows.map(String)).size;
   assert(rank<=distinct,"rank bound");ranks.push(rank);residuals.push(distinct);
   frontal.push({prefix:p,rankGF2:rank,distinctResiduals:distinct});
  }
  const nodes=reducedNodes(n,order,fn),peakRank=Math.max(...ranks);
  assert(nodes+2>=peakRank,"rank-to-size guard");
  return {order:order.map(x=>x+1),nodes,peakRankGF2:peakRank,rankAtBalanced:ranks[n/2],peakResiduals:Math.max(...residuals),ranks,frontal}
 }
 const k=3,n=2*k, bad=Array.from({length:n},(_,j)=>j),good=Array.from({length:k},(_,j)=>[j,k+j]).flat();
 const disj=mask=>{for(let i=0;i<k;i++)if(((mask>>i)&1)&&((mask>>(k+i))&1))return 0;return 1};
 const all=permutations(bad),allResults=all.map(o=>audit(n,o,disj));
 const minNodes=Math.min(...allResults.map(z=>z.nodes)),maxNodes=Math.max(...allResults.map(z=>z.nodes));
 const minPeakRank=Math.min(...allResults.map(z=>z.peakRankGF2)),maxPeakRank=Math.max(...allResults.map(z=>z.peakRankGF2));
 const badResult=audit(n,bad,disj),goodResult=audit(n,good,disj);
 assert(badResult.rankAtBalanced===8,"DISJ_3 rank=8");assert(minNodes<=goodResult.nodes&&goodResult.nodes<badResult.nodes,"good order shortcut");
 assert(maxPeakRank===8,"max rank DISJ_3");
 const disj4=n4=>{for(let i=0;i<4;i++)if(((n4>>i)&1)&&((n4>>(i+4))&1))return 0;return 1};
 const bad4=audit(8,[0,1,2,3,4,5,6,7],disj4),good4=audit(8,[0,4,1,5,2,6,3,7],disj4);
 assert(bad4.rankAtBalanced===16,"DISJ_4 16");
 const unique4=audit(8,[0,1,2,3,4,5,6,7],v=>v===0);
 assert(unique4.peakRankGF2===1&&unique4.nodes<=8,"unique solution rank 1");
 const edges=[[0,1],[1,2],[2,3],[3,4],[4,5],[5,0]];
 const horn=mask=>edges.every(([a,b])=>!(((mask>>a)&1)&&((mask>>b)&1)))?1:0;
 const hOrder=[0,1,2,3,4,5],hall=permutations(hOrder).map(o=>audit(6,o,horn));
 const hornResults={orders:hall.length,minNodes:Math.min(...hall.map(x=>x.nodes)),maxNodes:Math.max(...hall.map(x=>x.nodes)),minPeakRank:Math.min(...hall.map(x=>x.peakRankGF2)),maxPeakRank:Math.max(...hall.map(x=>x.peakRankGF2)),canonical:audit(6,hOrder,horn)};
 return {revision:"tmr4_fixed_order_obdd_rank051.v1",seed:"none exhaustive deterministic",model:"fixed-order read-once BDD with arbitrary DAG sharing, early terminals, skipped tests",exact_arithmetic:"GF(2) BigInt row xor; generic integer truth table; nonprobabilistic",disj3:{orders:all.length,bad:badResult,good:goodResult,minNodes,maxNodes,minPeakRank,maxPeakRank,optimalNodeOrderCount:allResults.filter(x=>x.nodes===minNodes).length},disj4:{bad:bad4,good:good4},unique4,hornC6:hornResults,errors:0};
};
const out=runTMR4051();
console.log(JSON.stringify(out,null,2));
