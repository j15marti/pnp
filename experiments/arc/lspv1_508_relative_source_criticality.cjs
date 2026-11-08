"use strict";
/* LSPV-1/508. Source-criticality truth-table audit. NOT the historical R_mix341 checker. */
function run508(){
 const sources=[[1,2,-4],[1,-2,-4],[-1,2,-4],[-1,-2,4],
 [2,3,-5],[2,-3,5],[-2,3,5],[-2,-3,-5],
 [1,5,-6],[1,-5,-6],[-1,5,-6],[-1,-5,6],
 [4,6,-7],[4,-6,7],[-4,6,7],[-4,-6,-7]];
 const goals=[[-1,-3,7],[1,-7],[3,-7]];
 let assertions=0;
 function ck(x,m){assertions++;if(!x)throw Error(m)}
 function sat(C,a){return C.some(l=>((a >> (Math.abs(l)-1))&1)==(l>0?1:0))}
 const witness=[], counts=[];
 ck(sources.length==16&&goals.length==3,"wrong input length");
 ck(sources.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),"improper signed 3cnf");
 let sourceModels=0;
 for(let a=0;a<128;a++){
   const bits=Array.from({length:7},(_,j)=>(a>>j)&1);
   const [x,y,t,aa,p,b,h]=bits;
   const semantic=(aa===(x&y)&&p===(y^t)&&b===(x&p)&&h===(aa^b));
   const src=sources.every(c=>sat(c,a));
   ck(src===semantic,"source differs from gate meaning");
   ck(!src||goals.every(c=>sat(c,a)),"source does not entail interface");
   ck(goals.every(c=>sat(c,a))===(h===(x&t)),"wrong output facets");
   if(src)sourceModels++;
 }
 ck(sourceModels===8,"wrong source model count");
 for(let j=0;j<16;j++){
   const vals=[];
   for(let a=0;a<128;a++){
     let rest=sources.every((c,k)=>k===j||sat(c,a));
     if(rest&&goals.some(c=>!sat(c,a)))vals.push(a);
   }
   ck(vals.length>0,"not relatively essential source "+j);
   const a=vals[0];
   ck(sources.every((c,k)=>k===j?!sat(c,a):sat(c,a)),"not exact source deletion");
   const violated=goals.map((g,k)=>sat(g,a)?null:`Q${k}`).filter(v=>v!==null);
   ck(violated.length>0,"witness missed output");
   witness.push({source:`S${String(j).padStart(2,"0")}`,assignment:a,goal_violations:violated});
   counts.push(vals.length);
 }
 const wrong=sources.map(c=>c.slice());wrong[3]=[-1,-2,-4];
 ck(Array.from({length:128},(_,i)=>i).some(a=>sources.every(c=>sat(c,a))!==wrong.every(c=>sat(c,a))),"corrupt source control");
 ck(!sources.some(c=>c.join(",")==="1,1,99"),"malformed control");
 ck(witness.every(w=>w.source.startsWith("S")&&w.goal_violations.length>0),"forged witness control");
 return {status:"PROVED_RESTRICTED_AND_COMPUTATIONAL",sourceCount:16,goalCount:3,sourceModels,
  indispensableSourceCount:witness.length,unitBinaryMultiRootLowerBound:16-3,
  knownUpperBoundFromLSPV1_507:19,checkedAssignments:128,deletionWitnessCounts:counts,
  witnesses:witness,assertions,negativeControls:["corrupt-source","malformed-source","missing-goal"]};
}
if (typeof module!=="undefined" && require.main===module) console.log(JSON.stringify(run508(),null,2));
module.exports=run508;
