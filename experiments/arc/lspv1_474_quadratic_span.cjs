// LSPV-1/474: finite independent GF(2) evaluation-matrix verifier.
// Checks proper signed 3-CNF; DOES NOT run historical R_mix341.
// Execute: node lspv1_474_quadratic_span.cjs
'use strict';
let checks=0, all=0, good=0, bad=0;
function yes(x,label){if(!x)throw Error(label);checks++;}
function clauses(n){
 const A=[];for(let a=1;a<=n;a++)for(let b=a+1;b<=n;b++)for(let c=b+1;c<=n;c++)
 for(let s=0;s<8;s++)A.push([s&1?-a:a,s&2?-b:b,s&4?-c:c]);return A;
}
function peel(F){
 let A=F.map(C=>C.map(Math.abs));
 while(A.length){
  let counts={};for(const C of A)for(const v of C)counts[v]=(counts[v]||0)+1;
  let i=A.findIndex(C=>C.some(v=>counts[v]===1));
  if(i<0)return false;A.splice(i,1);
 }return true;
}
function models(F,n){
 let A=[];for(let x=0;x<1<<n;x++)
 if(F.every(C=>C.some(v=>Boolean(x&(1<<(Math.abs(v)-1)))===(v>0))))A.push(x);
 return A;
}
function degree2Rank(V,n){
 const mono=[0];for(let i=0;i<n;i++)mono.push(1<<i);
 for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)mono.push((1<<i)|(1<<j));
 const pivot=new Map();
 for(const x of V){
  let row=0;for(let i=0;i<mono.length;i++)if((x&mono[i])===mono[i])row|=1<<i;
  while(row){let b=31-Math.clz32(row);if(pivot.has(b))row^=pivot.get(b);
   else{pivot.set(b,row);break;}}
 }return [pivot.size,mono.length];
}
function check(F,n){
 all++;if(!peel(F)){bad++;return;}
 good++;const v=models(F,n),[r,t]=degree2Rank(v,n);
 yes(v.length>0,'peelable SAT');yes(r===t,'quadratic independence');
}
function select(A,k,fn){
 const chosen=[];function rec(start){
  if(chosen.length===k){fn(chosen.map(i=>A[i]));return;}
  for(let i=start;i<=A.length-(k-chosen.length);i++){
   chosen.push(i);rec(i+1);chosen.pop();}}
 rec(0);
}
for(const [n,K] of [[4,2],[5,3]]){
 const A=clauses(n);for(let k=1;k<=K;k++)select(A,k,F=>check(F,n));
}
const two=[[1,2,3],[1,2,-3]],single=[[1,2,3]];
yes(!peel(two),'2-core');yes(degree2Rank(models(two,3),3)[0]<7,'quadratic resolvent');
const m=models(single,3);
yes(peel(single),'one clause peelable');yes(m.length===7,'7 models');
yes(m.some(x=>(x&4)===0),'z not globally fixed');
yes(m.filter(x=>(x&3)===0).every(x=>(x&4)!==0),'branch z fixed');
const out={schema:'LSPV1_474_STANDALONE/v1',status:'COMPUTATIONAL',tested:all,peelable:good,nonpeelable:bad,checks,quadratic_control:true,branch_scope_control:true,full_mixed_hardness:false,actual_native_checker:false,P_vs_NP:'OPEN'};
console.log(JSON.stringify(out));