'use strict';
// Compact independent public reproduction of LSPV1-359 local implicate cost.
// Full paid DAGs and no-import verifier in the companion ZIP.
const assert=require('assert'),V=[1,2,3],A=Array.from({length:8},(_,n)=>({1:n&1,2:(n>>1)&1,3:(n>>2)&1}));
const P=[
[[1],a=>a[1]===1],
[[1,2],a=>!!(a[1]||a[2])],
[[1,2],a=>a[1]===a[2]],
[[2,3],a=>a[2]!==a[3]],
[[1,2],a=>a[1]!==a[2]],
[[1,2,3],a=>!!((a[1]&&a[2])||a[3])]];
const Q=[
[[1],a=>a[1]===0],
[[1,2],a=>a[1]!==a[2]],
[[2],a=>a[2]===0],
[[2,3],a=>!!(a[2]||a[3])],
[[3],a=>a[3]===1],
[[1,3],a=>a[1]===a[3]],
[[1,2,3],a=>(a[1]+a[2]+a[3])%2===1]];
const valid=(c,a)=>c.some(l=>(l>0)===Boolean(a[Math.abs(l)]));
function blockers(s,f) {
 const out=[];
 for(const a of A){if(!f(a))out.push(s.map(v=>a[v]?-v:v));}
 return [...new Map(out.map(c=>[c.join(','),c])).values()];
}
let cases=0,targets=0,sat=0,unsat=0,max=0,checkedBlockers=0;
for(const [ps,p] of P)for(const [qs,q] of Q){
 cases++;
 const sources=[...blockers(ps,p),...blockers(qs,q)];
 if(A.some(a=>p(a)&&q(a)))sat++;else unsat++;
 const opts=[-1,0,1];
 for(const u of opts)for(const v of opts)for(const w of opts){
  const clause=[u,v,w].flatMap((sign,i)=>sign?[sign*(i+1)]:[]);
  const implied=A.every(a=>!(p(a)&&q(a))||valid(clause,a));
  if(!implied)continue;
  targets++;
  const blocked=A.filter(a=>!valid(clause,a));
  assert.strictEqual(blocked.length,2**(3-clause.length));
  let cost=blocked.length-1;
  for(const a of blocked){
   const c=sources.filter(c=>!valid(c,a)).sort((x,y)=>x.length-y.length)[0];
   assert(c,'Source clause required');
   const b=V.map(i=>a[i]?-i:i);
   assert(c.every(l=>b.includes(l)));
   const k=c.length,r=3-k;
   const paid=r===0?0:3*k+2*r-2;
   assert(paid<=6);
   cost+=paid;checkedBlockers++;
  }
  assert(cost<=55,'bound breached: '+cost);
  max=Math.max(max,cost);
 }
}
assert.deepStrictEqual([cases,targets,sat,unsat,max],[42,538,40,2,55]);
console.log(JSON.stringify({status:'PASS',cases,targets,sat,unsat,max_local_paid_bound:max,verified_blocker_rows:checkedBlockers,full_dag_replay:false,interpretation:'symbolic upper compiler; full DAG verifier in companion archive'},null,2));
