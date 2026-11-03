'use strict';
// STRICT3-UP-BACKDOOR354; Node.js stdlib, no external imports.
// Rebuilds every signed source and legal Resolution upper certificate.
const assert=require('assert');
const sort=(a,b)=>Math.abs(a)-Math.abs(b)||Number(a<0)-Number(b<0);
const canon=A=>[...new Set(A)].sort(sort);
function build(n){
  const p=n+1,F=[],edges=[];assert(n>=4);
  for(let i=1;i<=n;i++){
    let j=i%n+1;edges.push([F.length,F.length+1]);
    F.push(canon([-i,j,p]),canon([-i,j,-p]));
  }
  const long=[];
  for(let s of [1,-1]){
    const start=F.length,y=Array.from({length:n-3},(_,j)=>n+2+(s<0?n-3:0)+j);
    const L=Array.from({length:n},(_,j)=>s*(j+1));
    F.push(canon([L[0],L[1],y[0]]));
    for(let j=1;j<n-3;j++)F.push(canon([-y[j-1],L[j+1],y[j]]));
    F.push(canon([-y[y.length-1],L[n-2],L[n-1]]));
    long.push({start,y,length:n-2});
  }
  return {n,p,F,edges,long,variables:3*n-5};
}
function resol(A,B,p){
  assert(A.includes(p)&&B.includes(-p));
  const C=canon([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)]);
  assert(!C.some(l=>C.includes(-l)),'tautological resolvent');
  return C;
}
function makeProof(d){
  const lines=[...d.F],steps=[];
  function step(a,b,p){
    const C=resol(lines[a],lines[b],p);
    steps.push({a,b,p,C});lines.push(C);return lines.length-1;
  }
  const E=d.edges.map(e=>step(e[0],e[1],d.p));
  const L=d.long.map(z=>{
    let cur=z.start;
    for(let k=1;k<z.length;k++)cur=step(cur,z.start+k,z.y[k-1]);
    return cur;
  });
  let plus=L[0];for(let i=2;i<=d.n;i++)plus=step(plus,E[i-1],i);
  let minus=L[1];for(let i=d.n;i>=2;i--)minus=step(E[i-2],minus,i);
  assert.deepStrictEqual(lines[plus],[1]);assert.deepStrictEqual(lines[minus],[-1]);
  const root=step(plus,minus,1);assert.deepStrictEqual(lines[root],[]);
  assert.strictEqual(steps.length,5*d.n-7);
  return {steps,inspections:steps.reduce((v,s)=>v+lines[s.a].length+lines[s.b].length,0)};
}
function up(F,seed){
  const a={...seed};let count=0;
  for(;;){
    let unit=null;
    for(const C of F){
      if(C.some(l=>Object.hasOwn(a,Math.abs(l))&&a[Math.abs(l)]===(l>0)))continue;
      const rest=C.filter(l=>!Object.hasOwn(a,Math.abs(l)));
      if(!rest.length)return {unsat:true,count};
      if(rest.length===1&&unit===null)unit=rest[0];
    }
    if(unit===null)return {unsat:false,count};
    a[Math.abs(unit)]=unit>0;count++;
  }
}
const output=[];
for(const n of [4,5,6,8,12,20,32]){
  const d=build(n),r=makeProof(d);
  assert(d.F.every(C=>C.length===3&&new Set(C.map(Math.abs)).size===3));
  assert.strictEqual(d.F.length,4*n-4);
  for(let j=1;j<=n;j++)for(let t of [false,true])for(let b of [false,true]){
    const seed={};seed[j]=t;seed[d.p]=b;assert(up(d.F,seed).unsat);
  }
  for(let j=1;j<=d.variables;j++)for(let b of [false,true]){
    const seed={};seed[j]=b;assert(!up(d.F,seed).unsat);
  }
  output.push({n,variables:d.variables,clauses:d.F.length,strict3:true,
    backdoor_exact:2,RES_nodes:r.steps.length,RES_parent_literal_scans:r.inspections});
}
console.log(JSON.stringify({status:'PASS',calculus:'Rmix341:ordinary RES subsystem',output,
  B3:'OPEN',P_versus_NP:'OPEN'},null,2));
