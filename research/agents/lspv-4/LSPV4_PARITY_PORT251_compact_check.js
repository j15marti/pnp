"use strict";
/* Independent original-clause exact verifier for LSPV-4 PARITY-PORT251.
   Node.js standard library; no imports from Python producer. */
const assert=require("assert");
const G=[[1,2,4],[-1,3,5],[-2,-3,6],[1,-2,3],[-1,2,-3],[4,-5,-6],[-4,5,-6],[-4,-5,6]];
let tests={};
function ck(k,v){assert(v,k);tests[k]=(tests[k]||0)+1;}
function lit(l,a){return ((a>>>(Math.abs(l)-1))&1)===(l>0?1:0);}
function count(C,a){return C.reduce((r,l)=>r+(lit(l,a)?1:0),0);}
function sat(F,a){return F.every(C=>C.some(l=>lit(l,a)));}
function canon(A){return [...new Set(A)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);}
function resol(A,B,p){
 ck("opposing_pivot",(A.includes(p)&&B.includes(-p))||(A.includes(-p)&&B.includes(p)));
 const R=canon([...A,...B].filter(l=>Math.abs(l)!==p));
 ck("non_tautological",!R.some(l=>R.includes(-l)));
 return R;
}
let R={};G.forEach((C,i)=>R["C"+i]=C);
for(const [id,a,b,p] of [["R5","C3","C1",1],["R6","R5","C2",3],["R7","C4","C0",1],["R8","R7","C1",3],["R9","R8","C0",1],["R10","R9","R6",2]])R[id]=resol(R[a],R[b],p);
ck("derived_clause",JSON.stringify(canon(R.R10))===JSON.stringify([4,5,6]));
const fibers=Array(8).fill(0);
for(let a=0;a<64;a++){
 const N=Array(4).fill(0), comp=63^a;
 for(const C of G){N[count(C,a)]++;ck("clause_complement",count(C,a)+count(C,comp)===3);}
 ck("count_complement",N.every((n,r)=>n===G.filter(C=>count(C,comp)===3-r).length));
 if(sat(G,a))fibers[(a>>3)&7]++;
}
ck("exact_projection_fibers",JSON.stringify(fibers)===JSON.stringify([0,2,2,0,2,0,0,6]));
function targets(C,mode){const t={};for(const l of C)t[Math.abs(l)]=(mode==="S"?(l>0?1:0):(l>0?0:1));return t;}
for(let j=0;j<G.length;j++){
 const S=targets(G[j],"S"),U=targets(G[j],"U");
 for(const v of Object.keys(S))ck("source_S_U_inversion",S[v]===1-U[v]);
 for(let k=j+1;k<G.length;k++){
  const A=G[j],B=G[k],vars=[...new Set([...A,...B].map(Math.abs))];
  const same=A.some(l=>B.includes(l)),opp=A.some(l=>B.includes(-l));
  for(const [m,q,expect] of [["S","S",!opp],["U","U",!opp],["S","U",!same],["U","S",!same]]){
   let possible=false;
   for(let mask=0;mask<(1<<vars.length);mask++){
    const assignment=Object.fromEntries(vars.map((v,h)=>[v,(mask>>h)&1]));
    if(A.every(l=>assignment[Math.abs(l)]===(m==="S"?(l>0?1:0):(l>0?0:1)))&&
       B.every(l=>assignment[Math.abs(l)]===(q==="S"?(l>0?1:0):(l>0?0:1)))){
      possible=true;break;
    }
   }
   ck("four_source_extremes",possible===expect);
  }
 }
}
for(let i=0;i<8;i++)for(let j=i+1;j<8;j++)for(let k=j+1;k<8;k++)for(let mask=0;mask<8;mask++){
 const cs=[G[i],G[j],G[k]],local={};let consistent=true;
 cs.forEach((C,h)=>C.forEach(l=>{
  const value=((mask>>h)&1)?(l>0?1:0):(l>0?0:1), v=Math.abs(l);
  if(v in local&&local[v]!==value)consistent=false;local[v]=value;
 }));
 let brute=false;
 for(let a=0;a<64;a++)if(cs.every((C,h)=>count(C,a)===(((mask>>h)&1)?3:0)))brute=true;
 ck("triple_modes",consistent===brute);
}
const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function build(charges){
 const F=[];for(let v=0;v<4;v++){
  const edges=E.flatMap((e,i)=>e.includes(v)?[i+1]:[]);
  const ren={1:7+3*v,2:8+3*v,3:9+3*v,4:edges[0],5:edges[1],6:edges[2]};
  for(const C of G)F.push(C.map(l=>Math.sign(l)*ren[Math.abs(l)]*(Math.abs(l)===4&&charges[v]===0?-1:1)));
 }return F;
}
const out=[];
for(const [name,charges] of [["K4_SAT",[1,1,0,0]],["K4_UNSAT",[1,1,1,0]]]){
 const F=build(charges);ck("source_size",F.length===32);
 let models=0,zero=null,one=null;
 for(let a=0;a<(1<<18);a++){
  if(sat(F,a))models++;
  if(a===0||a===(1<<18)-1){
   let N=[0,0,0,0];for(const C of F)N[count(C,a)]++;
   if(a===0)zero=N;else one=N;
  }
 }
 const parity=charges.reduce((x,y)=>x^y,0);
 ck("global_oracle_parity",(models>0)===(parity===0));
 ck("matched_counts",(name==="K4_SAT"&&models===768)||(name==="K4_UNSAT"&&models===0));
 ck("both_endpoints_fail",zero[0]>0&&one[0]>0);
 ck("endpoints_complement",zero.every((x,i)=>x===one[3-i]));
 out.push({name,n:18,m:32,models,zero,one});
}
process.stdout.write(JSON.stringify({status:"PASS",fibers,controls:out,checks:tests})+"\n");
