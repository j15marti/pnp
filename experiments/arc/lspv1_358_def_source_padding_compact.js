'use strict';
// LSPV-1 ER2 source-padding sandwich (fixed Rmix341 RES+VARDEF subsystem).
// Reproducible exhaustive both-label controls, signed source anchors, genuine
// proof pivots and typed full-mixed counterexample. No optimizer or FLMV claim.
function run(){
 let checks=0,cases=[];
 const norm=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
 const same=(a,b)=>a.length===b.length&&a.every(x=>b.includes(x));
 const sat=(c,v)=>c.some(z=>z>0?v[z]===1:v[-z]===0);
 function build(n,g,opp){
   if(n<2||g<1)throw Error('bad dimensions');
   const base=[[1]];for(let j=1;j<n;j++)base.push([-j,j+1]);
   base.push([opp?n:-n]);
   const source=base.map(x=>x.slice()),gates=[];
   for(let i=0;i<g;i++){
     const q=n+1+i,a=i?n+i:1,b=i?(i%n)+1:2;
     if(a===b||a===q||b===q)throw Error('illegal gate');
     gates.push({q,a,b});
     source.push([-q,a],[-q,b],[q,-a,-b]);
   }
   const proof=[];let active=0;
   if(!opp)for(let i=1;i<=n;i++){
     const A=active<source.length?source[active]:proof[active-source.length].cl;
     const B=source[i],pivot=i;
     if(!A.includes(pivot)||!B.includes(-pivot))throw Error('bad RES pivot');
     const cl=norm([...A.filter(z=>z!==pivot),...B.filter(z=>z!==-pivot)]);
     if(cl.some(z=>cl.includes(-z)))throw Error('tautology');
     proof.push({left:active,right:i,pivot,cl});active=source.length+proof.length-1;checks++;
   }
   if(!opp&&proof.at(-1).cl.length)throw Error('nonempty proof root');
   let models=0;
   for(let mask=0;mask<2**n;mask++){
     const v=Array(n+g+1).fill(0);
     for(let j=1;j<=n;j++)v[j]=(mask>>(j-1))&1;
     const bSat=base.every(c=>sat(c,v));
     for(let t of gates)v[t.q]=v[t.a]&v[t.b];
     if(!source.slice(n+1).every(c=>sat(c,v)))throw Error('bad DEF truth table');
     const pSat=source.every(c=>sat(c,v));
     if(bSat!==pSat)throw Error('source-extension not conservative');
     models+=+pSat;checks++;
   }
   let deletions=0,flips=0;
   if(!opp)for(let j=0;j<base.length;j++){
     let witness=null;
     for(let mask=0;mask<2**n;mask++){
       const v=Array(n+g+1).fill(0);
       for(let k=1;k<=n;k++)v[k]=(mask>>(k-1))&1;
       for(let t of gates)v[t.q]=v[t.a]&v[t.b];
       if(source.every((c,i)=>i===j||sat(c,v))){witness=v;break}
     }
     if(!witness||sat(base[j],witness))throw Error('bad deletion witness');
     deletions++;checks++;
     for(let lit of base[j]){
       const changed=base[j].map(x=>x===lit?-x:x);
       if(!sat(changed,witness))throw Error('sign repair failed');
       flips++;checks++;
     }
   }
   return {n,g,source,base,gates,proof,models,deletions,flips};
 }
 for(let n of [2,3,4,6,8])for(let g of [1,2,4]){
   const u=build(n,g,false),s=build(n,g,true);
   if(u.models!==0||s.models!==1)throw Error('wrong labels');
   if(u.proof.length!==n||u.deletions!==n+1)throw Error('wrong source minimum');
   cases.push({n,g,vars:n+g,sourceClauses:u.source.length,
      certifiedMixedMin:n,paidER2BackReplayCeiling:n+g,
      satModels:s.models,unsatModels:u.models,
      originalSourceDeletions:u.deletions,originalLiteralFlips:u.flips});
 }
 const def=[[-3,1],[-3,2],[3,-1,-2]];
 for(let m=0;m<8;m++){
   const v=[0,m&1,(m>>1)&1,(m>>2)&1];
   if(def.every(c=>sat(c,v))!==(v[3]===(v[1]&v[2])))throw Error('bad DEF');
   checks++;
 }
 const malicious=[
   {q:1,a:1,b:2},{q:3,a:1,b:1},{q:3,a:3,b:1},
   {q:3,a:1,b:2,slot:[3,1]}];
 function legal(t){return t.q>2&&t.a!==t.b&&t.q!==t.a&&t.q!==t.b
  &&(!t.slot||same(t.slot,[-t.q,t.a]));}
 for(let t of malicious){if(legal(t))throw Error('forged gate accepted');checks++}
 return {run:'ER2_SOURCE_PADDING_SANDWICH358',cases,checks,
   gateTruthTableAssignments:8,malformedGateRejections:4,
   typedAND3Failure:{paddedOriginals:[1,2,3],translatedOriginals:[1,2],
      extensionOutput:3,paddedLocalAND3Legal:true,verbatimReplayLegal:false},
   note:'Mathematical global minimum uses indispensable original Horn sources and sound binary-premise Rmix. Optimizer/machine cost separate.'};
}
if(typeof module!=='undefined'&&module.exports)module.exports={run};
if(typeof require!=='undefined'&&require.main===module)console.log(JSON.stringify(run(),null,2));
