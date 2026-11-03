#!/usr/bin/env node
"use strict";
/* LSPV-3 372: independent, self-contained small-support Res(oplus) macro replay.
   Fixed small fixtures, semantic single-line weakenings, strict signed resolution.
   Not a proof of Braun's lower bound or full-calculus transfer. */
const assert=require("assert");
let checks=0, charged=0;
function chk(x,msg){checks++;assert(x,msg)}
function bit(l,a){return a[Math.abs(l)]===(l>0)}
function truth(C,a){return C.some(z=>bit(z,a))}
function sort(C){return [...new Set(C)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}
function assignments(S,work){for(let m=0;m<(1<<S.length);m++){let a={};S.forEach((v,j)=>a[v]=!!(m&(1<<j)));work(a)}}
function local(S,parents,C){
 S=[...S].sort((a,b)=>a-b); const clauses=parents.map(sort);
 chk(S.length<=4&&S.length>0,"scope");
 const fixed={};C.forEach(l=>fixed[Math.abs(l)]=l<0);
 const extras=S.filter(v=>!(v in fixed));
 function branch(a,rest){
  if(!rest.length){
   let B=sort(S.map(v=>a[v]?-v:v));
   let j=clauses.findIndex(P=>!truth(P,a));
   chk(j>=0,"unsound inference");
   if(JSON.stringify(clauses[j])===JSON.stringify(B))return j;
   chk(clauses[j].every(l=>B.includes(l)),"invalid semantic weakening");
   clauses.push(B);charged++;return clauses.length-1;
  }
  let v=rest[0],left=branch({...a,[v]:false},rest.slice(1)),right=branch({...a,[v]:true},rest.slice(1));
  chk(clauses[left].includes(v)&&clauses[right].includes(-v),"signed pivot");
  let D=sort([...clauses[left].filter(l=>l!==v),...clauses[right].filter(l=>l!==-v)]);
  clauses.push(D);charged++;return clauses.length-1;
 }
 const root=branch(fixed,extras);
 chk(JSON.stringify(clauses[root])===JSON.stringify(sort(C)),"wrong derivation conclusion");
 assignments(S,a=>{if(parents.every(p=>truth(p,a)))chk(truth(C,a),"SAT counterexample")});
 return {b:S.length,steps:clauses.length-parents.length};
}
const cases=[
 local([1,2],[[1,2],[-1,2]],[2]),
 local([1,2,3],[[-1,3],[1],[3,2]],[3]),
 local([1,2,3],[[1,2,3],[-1,2,3],[1,-2,3],[-1,-2,3]],[3])
];
let p=[];assignments([1,2,3,4],a=>p.push(sort([1,2,3,4].map(v=>a[v]?-v:v))));
cases.push(local([1,2,3,4],p,[]));
cases.push(local([1,2,3,4],[[1],[-1,4],[4,3]],[3,4]));
cases.push(local([1,2,3,4],[[1],[-1,4],[4,3]],[-3,4]));
function eq(E,a){return E.v? a[E.v]===!!E.eq : E.xor.reduce((x,v)=>x+(a[v]?1:0),0)%2===E.eq}
function lineTrue(C,a){return C.some(l=>eq(l,a))}
function aff(S,sources,E){
 let t=E.xor[E.xor.length-1],other=S.filter(v=>v!==t),lines=sources.map(x=>x.slice());
 function visit(a,k){
  if(k===other.length){
   a={...a};
   let partial=E.xor.filter(v=>v!==t).reduce((s,v)=>s+(a[v]?1:0),0)%2;
   a[t]=!!(1^E.eq^partial);
   chk(!eq(E,a),"affine violating assignment");
   let j=sources.findIndex(line=>!lineTrue(line,a));chk(j>=0,"unsound affine");
   const out=[E,...other.map(v=>({v,eq:a[v]?0:1}))];
   assignments(S,z=>{if(lineTrue(lines[j],z))chk(lineTrue(out,z),"invalid semantic weakening")});
   lines.push(out);charged++;return lines.length-1;
  }
  const v=other[k],L=visit({...a,[v]:false},k+1),R=visit({...a,[v]:true},k+1);
  chk(lines[L].some(x=>x.v===v&&x.eq===1),"affine signed plus pivot");
  chk(lines[R].some(x=>x.v===v&&x.eq===0),"affine signed minus pivot");
  const out=lines[L].filter(x=>x.v!==v);
  chk(JSON.stringify(out)===JSON.stringify(lines[R].filter(x=>x.v!==v)),"wrong affine resolvent");
  lines.push(out);charged++;return lines.length-1;
 }
 const base=lines.length,root=visit({},0);
 chk(JSON.stringify(lines[root])===JSON.stringify([E]),"wrong affine conclusion");
 assignments(S,a=>{if(sources.every(line=>lineTrue(line,a)))chk(lineTrue([E],a),"affine SAT counterexample")});
 return {b:S.length,steps:lines.length-base};
}
let S=[1,2,3],E={xor:S,eq:0},blockers=[];
assignments(S,a=>{if((a[1]+a[2]+a[3])%2)blockers.push(S.map(v=>({v,eq:a[v]?0:1})))});
const affineCases=[
 aff(S,blockers,E),
 aff(S,[[{xor:[1,2],eq:0}],[{v:3,eq:0}]],E)
];
let rejected=0;try{local([1],[[1]],[-1])}catch(e){rejected++}
chk(rejected===1,"invalid SAT entailment should be rejected");
console.log(JSON.stringify({status:"COMPUTATIONAL",ordinary:cases,affine:affineCases,charged,assertions:checks,invalid_entailment_rejected:rejected,
  scope:"Original-name local macros only; does NOT check full Rmix341 or external preprint"}));
