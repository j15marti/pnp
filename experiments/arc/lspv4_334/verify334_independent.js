#!/usr/bin/env node
// Independent literal-level no-producer-import referee for LSPV4 334.
'use strict';
const assert=require('node:assert/strict');
const Z=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-3],[-1,-4,-5],[-2,-4,-6],[-3,-5,-6]];
const F9=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9],[-4,-6,-8],[-1,-6,-7],[-2,-3,-4],[-3,-5,-8],[-1,-2,-9],[-5,-7,-9]];
let checks=0;const equal=(x,y)=>{checks++;assert.deepEqual(x,y)};
function shift(F,d){return F.map(c=>c.map(v=>Math.sign(v)*(Math.abs(v)+d)))}
function valid(F,n){
 if(!Number.isSafeInteger(n)||n<3||n%3||F.length!==4*n/3)return false;
 const counts=new Map(),seen=new Set();
 for(const c of F){
  if(c.length!==3||c.some(v=>!Number.isSafeInteger(v)||v===0||Math.abs(v)>n)
   ||new Set(c.map(Math.abs)).size!==3||!(c.every(v=>v>0)||c.every(v=>v<0)))return false;
  const k=c.slice().sort((a,b)=>a-b).join(',');
  if(seen.has(k))return false;seen.add(k);
  for(const v of c)counts.set(v,(counts.get(v)||0)+1);
 }
 for(let i=1;i<=n;i++)if(counts.get(i)!==2||counts.get(-i)!==2)return false;
 return true;
}
function sat(F,a){
 for(const c of F){let good=false;
  for(const v of c)if(((a>>>(Math.abs(v)-1))&1)===Number(v>0)){good=true;break}
  if(!good)return false
 }
 return true;
}
function swap(F,i,k,j,l){const H=F.map(c=>c.slice()),v=H[i][k];H[i][k]=H[j][l];H[j][l]=v;return H;}
function connected(F,n){
 const S=new Set([1]);let changed=true;
 while(changed){changed=false;for(const c of F)
  if(c.some(v=>S.has(Math.abs(v))))for(const v of c)
    if(!S.has(Math.abs(v))){S.add(Math.abs(v));changed=true}}
 return S.size===n
}
function main(){
 equal(valid(Z,6),true);equal(valid(F9,9),true);
 const B=[...Z,...shift(Z,6)],pre=new Uint8Array(4096);
 for(let a=0;a<4096;a++)pre[a]=Number(sat(B,a));
 equal(pre.reduce((x,y)=>x+y,0),324);equal(connected(B,12),false);
 let swaps=0,positive=0,negative=0;
 for(let i=0;i<8;i++)for(let k=0;k<3;k++)for(let j=8;j<16;j++)for(let l=0;l<3;l++){
  if((B[i][k]>0)!==(B[j][l]>0))continue;
  const H=swap(B,i,k,j,l);
  equal(valid(H,12),true);equal(connected(H,12),true);
  let after=0,overlap=0,removed=0,added=0;
  for(let a=0;a<4096;a++){
   const q=Number(sat(H,a)),p=pre[a];after+=q;overlap+=q&&p;removed+=p&&!q;added+=q&&!p;
  }
  equal([after,overlap,removed,added],[318,270,54,48]);
  (B[i][k]>0?positive++:negative++);swaps++;
 }
 equal(swaps,288);equal(positive,144);equal(negative,144);
 const H=swap(B,1,1,8,0),mG=new Uint8Array(64),mH=new Uint8Array(4096);
 for(let a=0;a<64;a++)mG[a]=Number(sat(Z,a));
 for(let a=0;a<4096;a++)mH[a]=Number(sat(H,a));
 const triple=[0,0,0,0,0];
 for(let a=0;a<(1<<18);a++){
  const g=Boolean(mG[a&63]),b=a>>>6,p=g&&Boolean(pre[b]),q=g&&Boolean(mH[b]);
  [p,q,p&&q,p&&!q,q&&!p].forEach((v,k)=>triple[k]+=Number(v));
 }
 equal(triple,[5832,5724,4860,972,864]);
 let nF9=0,n0=0,n1=0;
 for(let a=0;a<512;a++)if(sat(F9,a)){
  nF9++;
  if(!((a>>>1)&1)&&!((a>>>2)&1)&&((a>>>5)&1)){if(a&1)n1++;else n0++;}
 }
 equal([nF9,n0,n1],[70,1,0]);
 const bad=[B.concat([B[0]]),B.slice(0,-1),[[-1,2,3],...B.slice(1)],[[1,1,3],...B.slice(1)],[[1,2,13],...B.slice(1)],[[0,2,3],...B.slice(1)]];
 for(const f of bad)equal(valid(f,12),false);
 return {run:'LSPV4_334_INDEPENDENT_NODE',producer_import:false,original_rows_18:262144,
    twelve_variable_swaps:swaps,positive,negative,connected_all_swaps:true,
    twelve_variable_values:[324,318,270,54,48],
    eighteen_variable_values:triple,F9_original_models:nF9,
    F9_SAT_UNSAT_pins:[n0,n1],malformed_rejected:bad.length,
    verified_check_groups:checks,P_vs_NP:'OPEN'};
}
console.log(JSON.stringify(main(),null,2));
