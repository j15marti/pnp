// LSPV-2 DPLL-IMPLICATE-PRUNE358: deterministic finite producer and cost checker.
// Node: node experiments/arc/lspv2_358_dpll_implicate_producer.js
"use strict";
function canon(xs) {
  const z=[...new Set(xs)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
  if(z.some(x=>!Number.isInteger(x)||x===0||z.includes(-x)))throw Error("bad clause");
  return z;
}
function same(a,b){return a.length===b.length&&a.every((x,i)=>x===b[i]);}
function clauseTrue(c,m){return c.some(x=>((m>>(Math.abs(x)-1))&1)===(x>0?1:0));}
function sat(F,m){return F.every(c=>clauseTrue(c,m));}
function entails(F,C,n){for(let m=0;m<2**n;m++)if(sat(F,m)&&!clauseTrue(C,m))return false;return true;}
function resolve(a,b,p) {
  if(!a.includes(p)||!b.includes(-p))throw Error("invalid pivot");
  return canon(a.filter(x=>x!==p).concat(b.filter(x=>x!==-p)));
}
function targets(n) {
  const out=[];
  for(let h=0;h<3**n;h++){let r=h,c=[];for(let i=1;i<=n;i++){const z=r%3;r=Math.floor(r/3);if(z===1)c.push(i);if(z===2)c.push(-i);}out.push(canon(c));}
  return out;
}
function compile(Fraw,Craw,n) {
  if(!Number.isInteger(n)||n<1||n>10)throw Error("n cutoff");
  const F=Fraw.map(canon),C=canon(Craw);
  if(F.flat().concat(C).some(x=>Math.abs(x)>n))throw Error("bad source var");
  if(!entails(F,C,n))throw Error("not entailed");
  const proof=F.map((c,i)=>({op:"src",source:i,clause:c}));let cost=0, next=n+1;
  function add(o){proof.push(o);if(o.op==="res"||o.op==="def")cost++;return proof.length-1;}
  if(F.some(c=>c.length===0))return {F,C,n,proof,root:F.findIndex(c=>c.length===0),cost,cutoff:2**n};
  const fixed={};for(const x of C)fixed[Math.abs(x)]=x>0?0:1;
  const free=Array.from({length:n},(_,i)=>i+1).filter(x=>fixed[x]===undefined);
  function branch(depth,assign) {
    if(depth===free.length){
      const m=Object.entries(assign).reduce((m,[x,v])=>m|(v<<(Number(x)-1)),0);
      const j=F.findIndex(c=>!clauseTrue(c,m));
      if(j<0)throw Error("missing falsified authentic source");
      return j;
    }
    const v=free[depth], a0={...assign,[v]:0},a1={...assign,[v]:1};
    const left=branch(depth+1,a0),right=branch(depth+1,a1);
    const L=proof[left].clause,R=proof[right].clause;
    if(!L.includes(v))return left;
    if(!R.includes(-v))return right;
    const clause=resolve(L,R,v);
    return add({op:"res",parents:[left,right],pivot:v,clause});
  }
  let root=branch(0,fixed);
  if(proof[root].clause.length>0){
    const missing=C.filter(x=>!proof[root].clause.includes(x));
    for(const l of missing){
      const D=proof[root].clause,u=D[0],y=next++;
      const d=add({op:"def",y,a:u,b:-l,clause:[]});
      const c0=add({op:"dc",def:d,slot:0,clause:canon([-y,u])});
      add({op:"dc",def:d,slot:1,clause:canon([-y,-l])});
      const c2=add({op:"dc",def:d,slot:2,clause:canon([y,-u,l])});
      const r1=add({op:"res",parents:[root,c2],pivot:u,clause:resolve(D,proof[c2].clause,u)});
      root=add({op:"res",parents:[r1,c0],pivot:y,clause:resolve(proof[r1].clause,proof[c0].clause,y)});
    }
  }
  if(!same(proof[root].clause,C)&&proof[root].clause.length!==0)throw Error("not exact output");
  const t=n-C.length,bound=2**t-1+3*Math.max(C.length-1,0);
  if(cost>bound)throw Error("bound violated "+cost+" "+bound);
  return {F,C,n,proof,root,cost,bound,free:t,early:proof[root].clause.length===0};
}
function seedRng(seed){let x=seed|0;return ()=>{x^=x<<13;x^=x>>>17;x^=x<<5;return (x>>>0)/4294967296;};}
function run() {
  const r=seedRng(3582026),cases=[],counts={twoVarSources:0,threeVarSources:0,claims:0,early:0,exact:0,logicalNodes:0,defNodes:0,resNodes:0,satSources:0,unsatSources:0};
  function trySource(F,n,group){
    if(F.every(c=>c.length>0)&&(F.some(c=>!c.length)))throw Error("unreachable");
    const N=2**n;
    if(Array.from({length:N},(_,m)=>m).some(m=>sat(F,m)))counts.satSources++;else counts.unsatSources++;
    counts[group]++;
    for(const C of targets(n))if(entails(F,C,n)){
      const item=compile(F,C,n);cases.push(item);counts.claims++;
      counts.early+=item.early?1:0;counts.exact+=item.early?0:1;counts.logicalNodes+=item.cost;
      for(const v of item.proof){counts.defNodes+=(v.op==="def");counts.resNodes+=(v.op==="res");}
    }
  }
  const two=targets(2).filter(x=>x.length>0);
  for(let mask=0;mask<2**two.length;mask++)trySource(two.filter((_,i)=>mask&(1<<i)),2,"twoVarSources");
  const three=targets(3).filter(x=>x.length>0);
  for(let j=0;j<100;j++){const p=.13+.72*r(),F=three.filter(()=>r()<p);trySource(F,3,"threeVarSources");}
  const five=[
    [1,2],[3,4],[-1,-3],[-2,-4],[1,-2,-3,4],[-1,2,3,-4]
  ];trySource(five,4,"threeVarSources");
  const horn=[[1],[-1,2],[-2,3],[-3]];trySource(horn,3,"threeVarSources");
  const oddK4=[[1,2,3],[1,-2,-3],[-1,2,-3],[-1,-2,3]];
  trySource(oddK4,3,"threeVarSources"); // local parity row: four clauses SAT; control only.
  return {run_id:"LSPV-2_DPLL_IMPLICATE_PRUNE358",seed:3582026,grammar:"canonical nonempty nontautological source clauses; signed literals 1..n",status:"COMPUTATIONAL",counts,cases};
}
function selfTest() {
  let bad=0;for(const q of [[1,-1],[0],[1,1,-1]])try{canon(q);}catch(e){bad++;}
  if(bad!==2)throw Error("malformed check mismatch");
  if(entails([[1]],[-1],1))throw Error("opposite-label SAT should be non-entailed");
  if(!entails([[1],[-1]],[],1))throw Error("UNSAT empty consequence absent");
  const x=compile([[1],[-1]],[],1);if(x.cost!==1)throw Error("one-pivot contradiction");
  return {malformedRejected:bad,oppositeLabelChecked:true,tinyUnsatCost:x.cost};
}
function main(){const out=run();out.selfTest=selfTest();return out;}
if(typeof module!=="undefined"&&module&&module.exports)module.exports={main,run,compile,entails,canon,selfTest};
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
 const x=main();console.log(JSON.stringify({run_id:x.run_id,counts:x.counts,selfTest:x.selfTest,full_cases:x.cases.length}));
}
