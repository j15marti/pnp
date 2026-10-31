'use strict';
// Independently reproduce the quantified guard entailment and hostile controls.
// Node >=18, standard library only. Does not import the producer's Python.
const assert=require('node:assert/strict');
const vals=n=>Array.from({length:2**n},(_,m)=>Array.from({length:n},(_,i)=>(m>>i)&1));
const lit=(a,l)=>a[Math.abs(l)-1]===Number(l>0);
const holds=(a,C)=>C.some(l=>lit(a,l));
const source=(a,F)=>F.every(C=>holds(a,C));
const C=Array.from({length:8},(_,m)=>[1,2,3].map(v=>(m>>(v-1)&1)?v:-v));
const cubes=Array.from({length:27},(_,m)=>{let o={};for(let i=1;i<=3;i++){let z=m%3;m=Math.floor(m/3);if(z)o[i]=z-1;}return o;});
const Ds=Array.from({length:27},(_,m)=>{let d=[];for(let i=1;i<=3;i++){let z=m%3;m=Math.floor(m/3);if(z)d.push(i*(z===1?-1:1));}return d;});
const extendsCube=(a,r)=>Object.entries(r).every(([i,b])=>a[Number(i)-1]===b);
const block=r=>Object.entries(r).map(([i,b])=>b?-Number(i):Number(i));
let tested=0,truth=0;
for(let mask=0;mask<256;mask++){
 let F=C.filter((_,i)=>(mask>>i)&1);
 for(let rho of cubes)for(let D of Ds){
  let left=true,right=true;
  for(let a of vals(3)){
   let f=source(a,F);
   if(f&&extendsCube(a,rho)&&!holds(a,D))left=false;
   if(f&&!holds(a,block(rho).concat(D)))right=false;
   truth++;
  }
  assert.equal(left,right);
  tested++;
 }
}
assert.equal(tested,186624);
assert.equal(truth,1492992);
const leak=[[1,2],[1,-2]];
assert.equal(vals(2).filter(a=>source(a,leak)).length,2);
assert.equal(vals(2).filter(a=>source(a,leak.concat([[2],[-2]]))).length,0);
assert.equal(vals(2).filter(a=>source(a,leak.concat([[1]]))).length,2);
const t=(C,a)=>C.filter(l=>lit(a,l)).length;
let pairs=0,modes=0;
for(let F of [leak,C]){
 const n=F===leak?2:3;
 for(let j=0;j<F.length;j++)for(let k=j+1;k<F.length;k++){
   const A=F[j],B=F[k],shared=A.filter(l=>B.some(r=>Math.abs(r)===Math.abs(l)));
   const same=shared.some(l=>B.some(r=>Math.abs(l)===Math.abs(r)&&(l>0)===(r>0)));
   const opp=shared.some(l=>B.some(r=>Math.abs(l)===Math.abs(r)&&(l>0)!==(r>0)));
   for(let m of ['SS','SU','US','UU']){
     let expected=(m[0]===m[1])?!opp:!same;
     let observed=vals(n).some(a=>t(A,a)===(m[0]==='S'?A.length:0)&&t(B,a)===(m[1]==='S'?B.length:0));
     assert.equal(expected,observed);modes++;
   }
   pairs++;
 }
 for(let a of vals(n))for(let clause of F)assert.equal(t(clause,a)+t(clause,a.map(x=>1-x)),clause.length);
}
const up=(F,rho)=>{let a={...rho};while(true){let progress=false;
 for(let cl of F){
  if(cl.some(l=>Math.abs(l) in a&&a[Math.abs(l)]===Number(l>0)))continue;
  const rem=cl.filter(l=>!(Math.abs(l) in a));
  if(!rem.length)return true;
  if(rem.length===1){let l=rem[0],v=Math.abs(l),b=Number(l>0);
   if(v in a&&a[v]!==b)return true;
   if(!(v in a)){a[v]=b;progress=true;}
  }
 }
 if(!progress)return false;
}};
const refutes=(F,n,rho,depth)=>up(F,rho)||(depth>0&&
  Array.from({length:n},(_,i)=>i+1).filter(v=>!(v in rho)).some(v=>
    refutes(F,n,{...rho,[v]:0},depth-1)&&refutes(F,n,{...rho,[v]:1},depth-1)));
assert.equal(refutes(C,3,{},0),false);
assert.equal(refutes(C,3,{},1),false);
assert.equal(refutes(C,3,{},2),true);
console.log(JSON.stringify({pass:true,source_subsets:256,entailment_cases:tested,assignment_checks:truth,source_pairs:pairs,pair_modes:modes,full8_minimal_UP_split_depth:2,hostile_unguarded_false_UNSAT:true}));
