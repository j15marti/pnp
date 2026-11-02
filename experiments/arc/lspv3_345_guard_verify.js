#!/usr/bin/env node
'use strict';
// Independent source reconstruction and exhaustive both-label verifier.
// NO npm packages. Execute: node experiments/arc/lspv3_345_guard_verify.js
const result=(function run(){
 const cases=[];let checks=0;
 function ok(x,msg){checks++;if(!x)throw Error(msg)}
 function graph(k){
   if(k===0){let es=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)es.push([a,b]);return ["K4",4,es]}
   const es=[];for(let i=0;i<k;i++)es.push([i,(i+1)%k],[i+k,(i+1)%k+k],[i,i+k]);
   return ["prism"+k,2*k,es]
 }
 function generate(h,edges,odd){
  let cs=[];for(let v=0;v<h;v++){let ids=edges.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);ok(ids.length===3,"cubic");
   for(let a=0;a<8;a++){let parity=(a.toString(2).split("1").length-1)%2;
    if(parity!==(odd&&v===0?1:0))cs.push(ids.map((e,j)=>(a>>j&1)?-(e+1):e+1))
   }
  }return cs
 }
 const sat=(c,a)=>c.some(l=>(a>>(Math.abs(l)-1)&1)===(l>0?1:0));
 for(let k of [0,3,4,6]){
  const [name,h,edges]=graph(k),n=edges.length,odd=generate(h,edges,true),even=generate(h,edges,false);
  ok(odd.length===4*h && even.length===4*h,"count");
  let oddModels=0,evenModels=0,deleted=Array(odd.length).fill(-1);
  for(let a=0;a<(1<<n);a++){
   let failure=0,which=-1;
   for(let i=0;i<odd.length;i++)if(!sat(odd[i],a)){failure++;which=i}
   if(failure===0)oddModels++;
   if(failure===1 && deleted[which]<0)deleted[which]=a;
   if(even.every(c=>sat(c,a)))evenModels++
  }
  ok(oddModels===0,"odd UNSAT");
  ok(evenModels===(1<<(n-h+1)),"even SAT rank");
  for(let i=0;i<odd.length;i++){
   let a=deleted[i];ok(a>=0,"deletion witness");
   ok(!sat(odd[i],a)&&odd.every((c,j)=>i===j||sat(c,a)),"deletion validation");
   for(let j=0;j<3;j++){let c=odd[i].slice();c[j]=-c[j];ok(sat(c,a),"sign-flip control")}
  }
  let src=[[n+1],...odd.map(c=>[-(n+1),...c])];
  let dimacs=`p cnf ${n+1} ${src.length}\n`+src.map(c=>c.join(" ")+" 0\n").join("");
  let bits=dimacs.length*8;
  cases.push({graph:name,h,variables:n,sourceClauses:src.length,sourceBits:bits,derivedNodesBinaryMixedUpper:8*h-1,oddPinnedModels:oddModels,evenPinnedModels:evenModels,deletionWitnesses:odd.length,signFlipWitnesses:odd.length*3});
 }
 // Exact elementary pinned guard example (x),(not x), g=(not z or x)&(not z or not x)&z.
 let s=[[1],[-1]], guard=[[-2,1],[-2,-1],[2]];
 for(let i=0;i<guard.length;i++){
  let has=false;for(let a=0;a<4;a++)if(guard.every((c,j)=>i===j||sat(c,a)))has=true;
  ok(has,"mini minimal UNSAT source deletion")
 }
 ok(!Array.from({length:4},(_,a)=>guard.every(c=>sat(c,a))).includes(true),"mini pinned UNSAT");
 // resolution derived [-z], then [] = exactly two derived binary nodes.
 let r1=guard[0].filter(x=>x!==1).concat(guard[1].filter(x=>x!==-1));
 ok(r1.length===2&&r1.every(x=>x===-2),"guard pivot");
 ok(guard[2][0]===2,"pin pivot");
 return {version:"LSPV3-GUARDED-INTERFACE345-COMPACT/v1",status:"COMPUTATIONAL finite both-label and essential-source controls; exact guard law proved separately",checks,cases,mini:{sourceCount:3,provedResolutionOptimum:2,method:"3 indispensable sources and a two-Resolution-node proof"}};
})();
console.log(JSON.stringify(result,null,2));
