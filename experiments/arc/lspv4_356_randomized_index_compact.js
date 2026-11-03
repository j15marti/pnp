#!/usr/bin/env node
/* LSPV-4 RANDOMIZED-SOURCE-FIRST-FANO356 compact independent reproducer.
 * Pure Node.js 18+, no external packages. Execute:
 * node experiments/arc/lspv4_356_randomized_index_compact.js
 * This is a finite verification, not a SAT runtime lower bound.
 */
"use strict";
const pop=x=>{let z=0;for(;x;x&=x-1)z++;return z};
const make=(x,L)=>{
  const f=Array.from({length:L},(_,i)=>[((x>>>i)&1)?i+1:-i-1]);
  f.push(Array.from({length:L},(_,i)=>((x>>>i)&1)?-i-1:i+1));
  return f;
};
const sat=(f,a)=>f.every(c=>c.some(l=>((a>>>(Math.abs(l)-1))&1)===Number(l>0)));
const allsat=(f,L)=>Array.from({length:1<<L},(_,a)=>a).filter(a=>sat(f,a));
let counts={unsat:0,source_deletion_SAT:0,sign_flip_SAT:0,valid_resolution_DAG:0};
for(let L=1;L<=8;L++)for(let x=0;x<(1<<L);x++){
  const f=make(x,L);if(allsat(f,L).length)throw Error("UNSAT control failed");
  counts.unsat++;
  for(let i=0;i<=L;i++){
    if(!allsat(f.filter((_,j)=>i!==j),L).length)throw Error("deletion SAT control");
    counts.source_deletion_SAT++;
  }
  for(let j=0;j<f.length;j++)for(let k=0;k<f[j].length;k++){
    const g=f.map(c=>c.slice());g[j][k]=-g[j][k];
    if(!allsat(g,L).length)throw Error("sign flip SAT control");
    counts.sign_flip_SAT++;
  }
  let c=f[L].slice();
  for(let i=0;i<L;i++){
    const u=f[i][0];
    if(!c.includes(-u)||c.includes(u))throw Error("bad pivot");
    c=c.filter(l=>l!==-u);
  }
  if(c.length)throw Error("proof does not end empty");
  counts.valid_resolution_DAG++;
}
function optimum(L,s){
  const n=1<<L,k=1<<s,selection=[];
  let best=Infinity,codebook=null,examined=0;
  function rec(start){
    if(selection.length===k){
      examined++;let sum=0;
      for(let x=0;x<n;x++){
        let m=L+1;
        for(let y of selection)m=Math.min(m,pop(x^y));
        sum+=m;
      }
      if(sum<best){best=sum;codebook=selection.slice();}
      return;
    }
    for(let y=start;y<n;y++){selection.push(y);rec(y+1);selection.pop();}
  }
  rec(0);
  const epsilon=best/(n*L);
  const H=epsilon===0?0:-epsilon*Math.log2(epsilon)-(1-epsilon)*Math.log2(1-epsilon);
  if(s+1e-10<L*(1-H))throw Error("Fano violation");
  return {L,retained_bits:s,possible_messages:k,codebooks_examined:examined,
          hamming_loss:best,error:epsilon,fano_lb:L*(1-H),best_codebook:codebook};
}
const codebooks=[];
for(let L=1;L<=5;L++)for(let s=0;s<=Math.min(2,L);s++)codebooks.push(optimum(L,s));
if(counts.unsat!==510||counts.source_deletion_SAT!==4096||
   counts.sign_flip_SAT!==7172||counts.valid_resolution_DAG!==510)throw Error("wrong census");
function k4(charges){const e=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  let models=0;for(let a=0;a<64;a++){
    let p=[0,0,0,0];
    e.forEach(([u,v],i)=>{p[u]^=(a>>>i)&1;p[v]^=(a>>>i)&1});
    if(p.every((z,i)=>z===charges[i]))models++;
  }return models;
}
if(k4([1,0,0,0])!==0||k4([0,0,0,0])!==8)throw Error("parity control");
const result={status:"PASS",counts,codebooks,
                 odd_k4_models:0,even_k4_models:8,
                 note:"Finite exact codebook optimum; randomized Fano bound is analytic; not B3."};
process.stdout.write(JSON.stringify(result,null,2)+"\n");
