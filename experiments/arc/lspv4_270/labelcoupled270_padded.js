"use strict";
// ARC-LABELCOUPLED-ONEHOT270: length-growing ordinary-SAT guest wrapper control.
function src(m,h){let F=[];for(let i=1;i<=m;i++)F.push(i===h?[-1,(i%2?2:-2),3]:[1,2,3]);
 for(let v of [2,3])for(let a of [-1,1])for(let b of [-1,1])F.push([-v,a*(v===2?4:6),b*(v===2?5:7)]);return F}
function bits(F){let n=0;for(const C of F)for(const l of C)n=Math.max(n,Math.abs(l));
 const w=Math.ceil(Math.log2(n+2));
 return 8*(6+String(F.length).length+F.length*(2+3*(w+2)))}
function pad(F,m,p){const marked=F.slice(0,m).find(c=>c[0]<0),t=marked[1],G=[[t,3,8],[t,3,-8],...F.slice(m)];
 for(let j=0;j<p;j++)G.push([9+3*j,10+3*j,11+3*j]);return G}
function truth(l,a){return ((a>>(Math.abs(l)-1))&1)===(l>0?1:0)}
function sat(F,a){return F.every(C=>C.some(l=>truth(l,a)))}
function run(){
 const rows=[];let checks=0;
 for(const m of [64,256,1024,4096])for(const h of [m-1,m]){
  const F=src(m,h),N=bits(F),p=Math.max(1,Math.floor(Math.sqrt(N)/Math.log2(N+2))),G=pad(F,m,p),M=bits(G);
  const core=G.slice(0,10);
  for(let a=0;a<256;a++){const should=core.every(C=>C.some(l=>truth(l,a)));
   if(should!==(h%2===0&&((a>>1)&1)===0&&((a>>2)&1)===0))throw Error("core projection");checks++}
  const positivePads=G.slice(10);
  if(positivePads.length!==p||positivePads.some(C=>C.length!==3||C.some(l=>l<9)))throw Error("padding");
  const wrapperReads=Math.ceil(Math.pow(M,6/5));
  rows.push({m,h,label:h%2===0?"SAT":"UNSAT",parentBits:N,padClauses:p,ordinaryChildBits:M,
   guestWrapperRepeatedIndexedReads:wrapperReads,
   coldQueryLowerBoundSourceProbes:wrapperReads*Math.floor(m/2),
   cachedSourceProbeCostOnce:Math.floor(m/2),
   certifiedPromiseScanSourceClauses:m+8,
   spaceCachedSourceLabelBits:1,spaceMaterializedChildBits:M,
   nativeTransitionStatus:"NOT measured"});
 }
 return {run:"ARC-LABELCOUPLED-ONEHOT270-PADDED",finiteChecks:checks,rows,
  semantics:"Child equals padded marked x=1 cofactor, plus independent all-positive clauses. Label preserved on canonical one-hot family, both SAT and UNSAT.",
  allInputARC:"OPEN",fixedGuest:"For any correct A, B on child length M performs ceil(M^(6/5)) indexed reads of the same first sign bit before invoking A."};
}
if(typeof module!=="undefined")module.exports={src,pad,bits,run};
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));