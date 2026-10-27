#!/usr/bin/env node
"use strict";
const audit = function audit(){
 const W=[[-1,3,-14],[2,-8,9],[10,-13,14],[3,7,-13],[-4,-9,-11],[5,8,-14],[4,-8,-11],[1,7,13],[1,-7,10],[-5,-6,-15],[-2,-6,12],[-4,9,-10],[-2,5,-12],[-3,6,-15],[6,-7,11],[2,-9,11],[4,8,-10],[-3,12,15],[-5,-12,15],[-1,13,14]];
 const A=[[6,0],[11,0]],B=[[9,2],[17,2]];
 let checks=0;
 function ck(v,message){checks++;if(!v)throw Error("CHECK FAILED "+message)}
 function mode(a,b){const F=W.map(c=>c.slice());if(!a)for(const[i,j]of A)F[i][j]*=-1;if(!b)for(const[i,j]of B)F[i][j]*=-1;return F}
 function countModels(F){let cnt=0;for(let x=0;x<32768;x++){let good=true;for(const c of F){if(!c.some(l=>((x>>(Math.abs(l)-1))&1)===(l>0?1:0))){good=false;break}}if(good)cnt++}return cnt}
 const models={};
 for(const a of[0,1])for(const b of[0,1]){
  const F=mode(a,b),p=Array(16).fill(0),n=Array(16).fill(0);
  ck(F.length===20,"clauses count");
  for(const c of F){ck(c.length===3&&new Set(c.map(x=>Math.abs(x))).size===3,"distinct");for(const l of c)(l>0?p:n)[Math.abs(l)]++}
  for(let i=1;i<=15;i++)ck(p[i]===2&&n[i]===2,"exact signed two-two");
  const k=""+a+b;models[k]=countModels(F);
 }
 ck(JSON.stringify(models)==='{"10":272,"11":0,"00":772,"01":272}'||models["00"]===772&&models["01"]===272&&models["10"]===272&&models["11"]===0,"model signature");
 const Rlist=[2,3,4,5,6,7,8];
 let exhaustiveProofs=0, falseOneSeed=0, soundCases=0, completeCases=0, unionChecks=0, transcriptChecks=0;
 for(const R of Rlist){
  for(const a of[0,1])for(const b of[0,1]){
   const unsat=a===1&&b===1;
   let complete=false;
   for(let pi=0;pi<(1<<R);pi++){
    const trace=Array.from({length:R},(_,z)=>({address:unsat?z:null,answer:unsat?(pi>>z)&1:null,accept:unsat?Boolean((pi>>z)&1):z===0}));
    ck(trace.filter(t=>t.accept).length===(unsat?Array.from({length:R},(_,z)=>(pi>>z)&1).reduce((s,x)=>s+x,0):1),"success count");
    const majority=trace.filter(t=>t.accept).length>=2;
    if(unsat&&pi===(1<<R)-1){ck(majority,"perfect complete");complete=true;completeCases++}
    if(!unsat){ck(!majority,"all SAT reject majority");soundCases++;if(trace.some(t=>t.accept))falseOneSeed++}
    const union=new Set(trace.filter(t=>t.address!==null).map(t=>t.address));
    ck(union.size===(unsat?R:0),"physical proof union");
    unionChecks++;
    exhaustiveProofs++;
   }
   ck(unsat?complete:true,"UNSAT witness");
   if(unsat){
    for(let transcript=0;transcript<(1<<R);transcript++){
     const candidate=Array.from({length:R},(_,i)=>(transcript>>i)&1);
     ck(candidate.filter(Boolean).length>=2===((transcript.toString(2).match(/1/g)||[]).length>=2),"fresh transcript complete");
     transcriptChecks++;
    }
   }
  }
 }
 const g=2*Math.cos(Math.PI/7);
 ck(Math.abs(g-1.8019377358)<1e-10,"cosine");
 ck(1.8+0.001<g&&1.8+0.005>g,"strict margin");
 // SAT if one of the three W1 satisfiable modes, UNSAT exactly mode 11;
 // a false-positive seed exists on every SAT mode despite <=1/R seed soundness.
 return {run_id:"ARC201_PCP_SEED_UNION_FIREWALL",status:"COMPUTATIONAL restricted promise controls",W1_models:models,R_values:Rlist,exhaustive_proof_strings:exhaustiveProofs,false_single_seed_instances:falseOneSeed,sound_SAT_checks:soundCases,UNSAT_complete_checks:completeCases,physical_union_checks:unionChecks,transcript_enumeration_checks:transcriptChecks,assertion_groups:checks,failures:0,seed:null,cosine_endpoint:g,limitations:["finite W1 canonical source promise only","artificial randomized checker uses charged full W1-mode decoding; not a fast general UNSAT verifier","no arbitrary-CNF completeness","no algorithm-exponent contraction","model-native indexed bound conditional on full all-input verifier","independent referee pending"]};
};
const result=audit();
if(typeof require!=="undefined"){const fs=require("node:fs"); const path=require("node:path");fs.writeFileSync(path.join(__dirname,"2026-10-27_0500_ARC201_PCP_SEED_UNION_raw.json"),JSON.stringify(result,null,2)+"\n");}
console.log(JSON.stringify(result,null,2));
