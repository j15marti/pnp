#!/usr/bin/env node
"use strict";
/* LSPV-3 369 independent finite countercontrols. Node >=18, no imports.
   This does not re-prove Braun 2026 or the earlier complete Cook ER proofs. */
function lit(i,b,h,l){return ((h>>(l-1-b))&1)?i*l+b+1:-(i*l+b+1);}
function source(l) {
  const n=2**l,p=n+1,a=[];
  for(let i=0;i<p;i++)for(let j=i+1;j<p;j++)for(let h=0;h<n;h++){
    const c=[];
    for(let b=0;b<l;b++)c.push(-lit(i,b,h,l));
    for(let b=0;b<l;b++)c.push(-lit(j,b,h,l));
    a.push({i,j,h,c});
  }
  return a;
}
function falsifies(c,x){return c.every(z=>x[Math.abs(z)-1]!==(z>0?1:0));}
function bits(l,h){return Array.from({length:l},(_,b)=>(h>>(l-1-b))&1);}
const results=[];
for(const l of [1,2,3]){
  const n=2**l,p=n+1,arr=source(l);
  if(arr.length!==n*n*(n+1)/2)throw Error("source count");
  let deletions=0,signFlips=0;
  // All sources for l<=2; a deterministic stride-9 sample for l=3.
  const targets=l===3?arr.filter((_,k)=>k%9===0):arr;
  for(const C of targets){
    const hvals=Array(p).fill(null);
    hvals[C.i]=C.h;hvals[C.j]=C.h;
    const available=Array.from({length:n},(_,h)=>h).filter(h=>h!==C.h);
    let k=0;
    for(let i=0;i<p;i++)if(hvals[i]===null)hvals[i]=available[k++];
    const x=hvals.flatMap(h=>bits(l,h));
    const bad=arr.filter(D=>falsifies(D.c,x));
    if(bad.length!==1||bad[0]!==C)throw Error("deletion witness invalid");
    deletions++;
    for(let a=0;a<C.c.length;a++){
      const mutated=C.c.map((z,j)=>a===j?-z:z);
      if(falsifies(mutated,x))throw Error("sign repair invalid");
      signFlips++;
    }
  }
  const matched=Array.from({length:n},(_,h)=>bits(l,h)).flat();
  const matchedFailures=arr.filter(D=>D.i<n&&D.j<n&&falsifies(D.c,matched)).length;
  if(matchedFailures!==0)throw Error("matched satisfiable label failed");
  let fullModels=null;
  if(l<=2){
    fullModels=0;
    for(let a=0;a<2**(p*l);a++){
      const x=Array.from({length:p*l},(_,j)=>(a>>j)&1);
      if(!arr.some(C=>falsifies(C.c,x)))fullModels++;
    }
    if(fullModels!==0)throw Error("unsatisfiable label failed");
  }
  results.push({ell:l,holes:n,clauses:arr.length,originalVariables:p*l,
    occurrences:arr.length*2*l,deletionSATWitnesses:deletions,
    signFlipSATWitnesses:signFlips,matchedSATFailures:matchedFailures,
    exhaustivelyCountedUNSATModels:fullModels});
}
const edges=[];
for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)edges.push([i,j]);
let even=0,odd=0;
for(let x=0;x<64;x++){
  const charges=[0,0,0,0];
  edges.forEach(([i,j],k)=>{charges[i]^=(x>>k)&1;charges[j]^=(x>>k)&1;});
  if(charges.every(z=>z===0))even++;
  if(charges[0]===1&&charges.slice(1).every(z=>z===0))odd++;
}
if(even!==8||odd!==0)throw Error("Tseitin parity control");
console.log(JSON.stringify({name:"LSPV3_369_BRAUN_BACKTRANSLATION",results,
  tseitinK4:{evenModels:even,oddModels:odd},assertions:"deterministic checks passed",
  note:"Finite labels only; not a proof of the Braun preprint or of global ER bounds."},null,2));
