#!/usr/bin/env node
// LSPV-3 355. Standalone deterministic feedback-rank / mixed parity reproducer.
// node experiments/arc/lspv3_355_feedback_compact.js
'use strict';
const assert=require('assert');let assertions=0;
function yes(p,s){assert.ok(p,s);assertions++}
function graph(tag) {
 if(tag==='K4'){let es=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)es.push([i,j]);return [4,es]}
 let r=Number(tag.slice(5)),u=new Set();
 for(let i=0;i<r;i++)for(let [a,b] of [[i,(i+1)%r],[i+r,r+(i+1)%r],[i,i+r]])u.add([a,b].sort((x,y)=>x-y).join(','));
 return [2*r,[...u].map(s=>s.split(',').map(Number)).sort((a,b)=>a[0]-b[0]||a[1]-b[1])];
}
function source(h,edges,sigma){
 let F=[],owner=[];
 for(let v=0;v<h;v++){
  let inc=edges.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);yes(inc.length===3,'cubic');
  for(let a=0;a<8;a++){
   let b=[(a>>2)&1,(a>>1)&1,a&1];if((b[0]^b[1]^b[2])===sigma[v])continue;
   F.push(inc.map((i,j)=>b[j]?-(i+1):(i+1)));owner.push(v)
  }
 }
 return {F,owner};
}
function sat(C,a){return C.some(l=>Boolean((a>>(Math.abs(l)-1))&1)===(l>0))}
function unit(F,B,a){
 let v=new Map(B.map((id,i)=>[id,(a>>i)&1]));
 for(;;){let changed=false;
  for(let C of F){let hit=false,unknown=[];
   for(let l of C){let id=Math.abs(l)-1;
    if(!v.has(id))unknown.push(l);else if(v.get(id)===Number(l>0)){hit=true;break}
   }
   if(hit)continue;if(!unknown.length)return true;
   if(unknown.length===1){let l=unknown[0],id=Math.abs(l)-1;
    if(!v.has(id)){v.set(id,Number(l>0));changed=true}
    else if(v.get(id)!==Number(l>0))return true
   }
  }
  if(!changed)return false
 }
}
function pop(x){let k=0;for(;x;x>>=1)k+=x&1;return k}
function forestComplement(h,edges){
 let seen=new Set([0]),stack=[0],tree=new Set();
 while(stack.length){let v=stack.pop();edges.forEach(([a,b],i)=>{
  let w=a===v?b:b===v?a:-1;
  if(w>=0&&!seen.has(w)){seen.add(w);stack.push(w);tree.add(i)}
 })}
 yes(seen.size===h);
 return edges.map((_,i)=>i).filter(i=>!tree.has(i))
}
function run(tag){
 const [h,edges]=graph(tag),m=edges.length,k=m-h+1,sigma=Array(h).fill(0);sigma[0]=1;
 const {F,owner}=source(h,edges,sigma),even=source(h,edges,Array(h).fill(0)).F;
 yes(F.length===4*h);
 let oddCount=0,evenCount=0,witness=Array(F.length).fill(-1);
 for(let a=0;a<(1<<m);a++){
  let bad=[];F.forEach((C,i)=>{if(!sat(C,a))bad.push(i)});
  if(!bad.length)oddCount++;
  if(bad.length===1&&witness[bad[0]]<0)witness[bad[0]]=a;
  if(even.every(C=>sat(C,a)))evenCount++;
 }
 yes(oddCount===0&&evenCount===(1<<k));
 yes(witness.every(a=>a>=0));
 let signs=0;
 witness.forEach((a,i)=>{
  F.forEach((C,j)=>yes(sat(C,a)===(j!==i)));
  for(let l of F[i]){yes(((a>>(Math.abs(l)-1))&1)!==Number(l>0));signs++}
 });
 let subsets=0,probes=0;
 for(let mask=0;mask<(1<<m);mask++){
  let size=pop(mask);if(size>=k)continue;
  let B=[];for(let i=0;i<m;i++)if(mask&(1<<i))B.push(i);
  let found=false;
  for(let a=0;a<(1<<size);a++){probes++;if(!unit(F,B,a)){found=true;break}}
  yes(found,'nonbackdoor witness');subsets++;
 }
 let B=forestComplement(h,edges);yes(B.length===k);
 for(let a=0;a<(1<<k);a++){yes(unit(F,B,a));probes++}
 // Independent local truth-table checks for 4-clause AND3-to-parity aliases.
 for(let v=0;v<h;v++){
  let local=F.filter((_,i)=>owner[i]===v);
  let inc=edges.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
  yes(local.length===4);
  for(let a=0;a<(1<<m);a++){
   let parity=inc.reduce((x,i)=>x^((a>>i)&1),0);
   yes(local.every(C=>sat(C,a))===(parity===sigma[v]))
  }
 }
 let xorMask=0,rhs=0;for(let v=0;v<h;v++){
  edges.forEach((e,i)=>{if(e.includes(v))xorMask^=1<<i});rhs^=sigma[v]
 }
 yes(xorMask===0&&rhs===1);
 let input='p cnf '+m+' '+F.length+'\n'+F.map(C=>C.join(' ')+' 0').join('\n')+'\n';
 return {graph:tag,vertices:h,edgeVariables:m,clauses:F.length,feedbackRank:k,UPMinimum:k,
  mixedMinimum:4*h-1,smallerSetsRefutedAsBackdoors:subsets,UPCalls:probes,
  deletionSAT:witness.length,signFlipSAT:signs,oddModels:oddCount,evenModels:evenCount,
  DIMACSbits:8*Buffer.byteLength(input),backdoorEdgeIDs:B.map(i=>i+1)};
}
let cases=['K4','prism3','prism4'].map(run);
console.log(JSON.stringify({status:'PASS',assertions,cases},null,2));