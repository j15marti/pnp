#!/usr/bin/env node
"use strict";
/* H22-DANGEROUS-HITSET282: independent compact reproducibility check.
   Full Python source/raw, UNSAT source proof, no-import verifier in ZIP fallback. */
const A=require("node:assert/strict");
const cases=[
 {name:"Y6",P:[[1,2,3],[1,4,5],[2,4,6],[3,5,6]],Q:[[1,2,4],[1,3,6],[2,3,5],[4,5,6]],q:0,hit:[],models:20,safe:3},
 {name:"PRISM9",P:[[1,3,7],[1,2,8],[2,3,9],[4,6,7],[4,5,8],[5,6,9]],Q:[[1,4,6],[3,6,8],[1,2,5],[2,5,7],[3,4,9],[7,8,9]],q:3,hit:[2,8],models:43,safe:1},
 {name:"MOBIUS12",P:[[1,8,9],[1,2,10],[2,3,11],[3,4,12],[4,5,9],[5,6,10],[6,7,11],[7,8,12]],Q:[[7,9,11],[1,6,12],[8,10,11],[4,5,6],[3,4,12],[2,5,8],[2,9,10],[1,3,7]],q:4,hit:[1,8],models:228,safe:5},
 {name:"K33_ALL6",P:[[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9]],Q:[[1,5,9],[1,6,8],[2,4,9],[2,6,7],[3,4,8],[3,5,7]],q:6,hit:null,models:18,safe:0}
];
let check=0,assignments=0;
for(const t of cases){
 const {P,Q}=t,n=Math.max(...P.flat(),...Q.flat()),F=P.concat(Q.map(c=>c.map(x=>-x)));
 A.equal(F.length*3,4*n);
 const plus=Array(n+1).fill(0),minus=Array(n+1).fill(0),seen=new Set();
 for(const C of F){
  A.equal(C.length,3);A.equal(new Set(C.map(Math.abs)).size,3);
  A(C.every(x=>x>0)||C.every(x=>x<0));
  const s=C.slice().sort((a,b)=>a-b).join(",");
  A(!seen.has(s));seen.add(s);
  for(const x of C)(x>0?plus:minus)[Math.abs(x)]++;
 }
 for(let i=1;i<=n;i++)A(plus[i]===2&&minus[i]===2);
 const E=Array.from({length:n+1},()=>[]);
 P.forEach((C,j)=>C.forEach(i=>E[i].push(j)));
 const D=Q.filter(C=>C.every((a,i)=>C.slice(i+1).every(b=>E[a].every(v=>!E[b].includes(v)))));
 A.equal(D.length,t.q);
 let hit=null;
 for(let z=0;z<=2&&hit===null;z++){
  function go(S,next){
   if(hit!==null)return;
   if(S.length===z){if(D.every(C=>C.some(x=>S.includes(x))))hit=S.slice();return;}
   for(let v=next;v<=n;v++)go([...S,v],v+1);
  }go([],1);
 }
 A.deepEqual(hit,t.hit);
 let models=0,safe=0,validHitWitness=false;
 for(let mask=0;mask<(1<<n);mask++){
  assignments++;
  const a=[0,...Array.from({length:n},(_,j)=>(mask>>j)&1)];
  const sat=F.every(C=>C.some(x=>a[Math.abs(x)]===Number(x>0)));
  const pm=P.every(C=>C.reduce((s,x)=>s+a[x],0)===1);
  models+=Number(sat);safe+=Number(sat&&pm);
  if(sat&&pm&&hit!==null&&hit.every(v=>a[v]===0))validHitWitness=true;
 }
 A.equal(models,t.models);A.equal(safe,t.safe);
 if(hit!==null)A(validHitWitness);
 const h=a=>{const x=[0,0,0,0];for(const C of F)x[C.filter(v=>a[Math.abs(v)]===Number(v>0)).length]++;return x;};
 A.deepEqual(h(Array(n+1).fill(0)),[2*n/3,0,0,2*n/3]);
 A.deepEqual(h(Array(n+1).fill(1)),[2*n/3,0,0,2*n/3]);
 for(let v=1;v<=n;v++){const a=Array(n+1).fill(0);a[v]=1;A.deepEqual(h(a),[2*n/3-2,2,2,2*n/3-2]);}
 const modes={6:0,9:0,15:0};
 for(let i=0;i<F.length;i++)for(let j=i+1;j<F.length;j++){
  const a=F[i],b=F[j];
  const same=a.some(x=>b.includes(x)),opp=a.some(x=>b.includes(-x));
  A(!(same&&opp));
  modes[(opp?0:9)|(same?0:6)]++;check+=4;
 }
 for(const C of F)for(const x of C){
  const S=Number(x>0),U=Number(x<0);
  A(S===1-U);check++;
 }
 console.log(JSON.stringify({name:t.name,n,q:t.q,hit,models,safe,modes}));
}
A.equal(assignments,5184);
console.log(JSON.stringify({status:"PASS",complete_assignments:assignments,original_extreme_and_occurrence_checks:check,P_vs_NP:"OPEN"}));
