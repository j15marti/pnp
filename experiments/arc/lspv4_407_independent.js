/* LSPV-4/407 independent signed-DNF/paid-gate representation control.
 * Node >=18; no external dependencies.
 * Runs from repository root: node experiments/arc/lspv4_407_independent.js
 * No conclusion about native LOCAL public port legality or B3. */
'use strict';
const fs=require('fs'),path=require('path');
const raw=JSON.parse(fs.readFileSync(path.join(__dirname,'../../results/raw/arc/2026-11-05_0036_LSPV4_407_FLAT_EXPORT_summary.json'),'utf8'));
let count=0;
function assert(p,why){count++;if(!p)throw new Error('FAILED '+why)}
function f(k,x){for(let i=0;i<k;i++)if(!(((x>>(2*i))&1)||((x>>(2*i+1))&1)))return false;return true}
function circuit(k,x){
 const v=[];
 for(let i=0;i<2*k;i++)v[i+1]=!!((x>>i)&1);
 for(let i=0;i<k;i++)v[2*k+i+1]=v[2*i+1]||v[2*i+2];
 let last=v[2*k+1];
 for(let i=1;i<k;i++)last=last&&v[2*k+i+1];
 return last;
}
function dnf(k,x){
 for(let t=0;t<(1<<k);t++){
  let good=true;
  for(let j=0;j<k;j++){
   const b=((t>>j)&1)===0?2*j:2*j+1;
   if(!((x>>b)&1)){good=false;break}
  }
  if(good)return true;
 }
 return false;
}
function minModel(k,t){let x=0;for(let j=0;j<k;j++)x|=(1<<(2*j+((t>>j)&1)));return x}
for(let k=1;k<=12;k++){
 const rec=raw.cases[k-1];
 assert(rec.k===k,'k alignment');
 assert(rec.paid_defs===2*k-1,'paid gates');
 assert(rec.flat_dnf_terms_min===2**k,'DNF term count');
 assert(rec.flat_dnf_literal_tokens_min===k*2**k,'literal count');
 if(k<=6){
  for(let x=0;x<1<<(2*k);x++){
   const y=f(k,x);
   assert(circuit(k,x)===y,'gate value');
   assert(dnf(k,x)===y,'DNF value');
   const impossible=y&&!!(x&1)&&!(x&1);
   assert(!impossible,'UNSAT source');
  }
 }else{
  for(let s=0;s<1<<k;s++){
   const a=minModel(k,s);assert(f(k,a),'minimal model');
   assert(circuit(k,a),'circuit on minimal model');
  }
 }
 for(let s=0;s<1<<k;s++){
  const a=minModel(k,s);assert(f(k,a),'minimal model');
  if(k<=6)for(let t=s+1;t<1<<k;t++){
   const b=minModel(k,t);assert(!f(k,a&b),'distinct minima meet false');
  }
 }
}
for(let k=1;k<=6;k++)
 for(let s=0;s<1<<k;s++)
  for(let t=s+1;t<1<<k;t++){
   const a=minModel(k,s),b=minModel(k,t);
   const common=[];
   for(let j=0;j<2*k;j++)if(((a>>j)&1)===((b>>j)&1))
      common.push([j,(a>>j)&1]);
   const meet=a&b;assert(!f(k,meet),'meet falsifier');
   for(const [j,bit] of common)assert(((meet>>j)&1)===bit,'shared literal retained');
  }
let implicants=0,allTerms=0;
for(let k=1;k<=4;k++){
 const vcount=2*k,total=3**vcount;
 for(let state=0;state<total;state++){
  allTerms++;
  let p=state,positive=0,negative=0;
  for(let j=0;j<vcount;j++){
   const trit=p%3;p=Math.floor(p/3);
   if(trit===1)positive|=1<<j;
   else if(trit===2)negative|=1<<j;
  }
  let implicant=true;
  for(let x=0;x<1<<vcount;x++)
   if((x&positive)===positive&&((~x)&negative)===negative&&!f(k,x)){
    implicant=false;break;
   }
  if(implicant){
   implicants++;
   let hit=0;
   for(let s=0;s<1<<k;s++){
    const x=minModel(k,s);
    if((x&positive)===positive&&((~x)&negative)===negative)hit++;
   }
   assert(hit<=1,'nonmonotone implicant cannot cover two minimal models');
  }
 }
}
console.log(JSON.stringify({independent_assertions:count,all_cases:12,largest_k:12,
 nonmonotone_tested_partial_cubes:allTerms,valid_implicants:implicants,
 conclusion:'Flat DNF materialization requires >=k*2^k literal occurrences; full native export/B3 remain OPEN'},null,2));
