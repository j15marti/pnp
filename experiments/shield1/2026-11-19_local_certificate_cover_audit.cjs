#!/usr/bin/env node
// SHIELD1 local-certificate cover and T5 countercontrol audit.
// No dependencies. Run: node experiments/shield1/2026-11-19_local_certificate_cover_audit.cjs
// Exhaustive finite verification, not an asymptotic lower bound.
"use strict";
function audit() {
 const pool=(v)=>[-1,1,-v,v,[-1,-v],[-1,v],[1,-v],[1,v]];
 const pair=(xs)=>xs.flatMap((a,i)=>xs.slice(i+1).map(b=>[a,b]));
 const evalClause=(c,m)=>(Array.isArray(c)?c:[c]).some(l=>(((m[Math.abs(l)]===1)?1:0)===(l>0?1:0)));
 const sat=(clauses,m)=>clauses.every(c=>evalClause(c,m));
 const local=(clauses,z,varId)=>[0,1].some(v=>sat(clauses,{1:z,[varId]:v}));
 const p0=pair(pool(2)),p1=pair(pool(3));
 let cases=0,unsat=0,yes=0,wrong=0,pointRefuteOnSat=0;
 for(const C0 of p0)for(const C1 of p1){
   cases++;
   const global=[0,1].some(z=>local(C0,z,2)&&local(C1,z,3));
   const brute=[0,1].some(z=>[0,1].some(x=>[0,1].some(y=>sat(C0,{1:z,2:x,3:y})&&sat(C1,{1:z,2:x,3:y}))));
   if(global!==brute)throw Error("gluing fail");
   const winners=[0,1].map(z=>[C0,C1].findIndex((c,j)=>!local(c,z,2+j)));
   if(global){yes++;if(winners.some(x=>x>=0))pointRefuteOnSat++;if(winners.every(x=>x>=0))throw Error("false UNSAT cover")}
   else{unsat++;if(winners.some(x=>x<0))throw Error("missing local cover")}
   for(let z=0;z<2;z++)for(let j=0;j<2;j++) {
     const valid=!local(j===0?C0:C1,z,2+j);
     if(!valid){wrong++;if(winners[z]===j)throw Error("accepted wrong block");}
   }
 }
 const E=[[0,1],[0,2],[2,1],[3,0],[3,1]], inc=new Set([1,3]);
 const accepts=(a,e)=>inc.has((a[e[1]]-a[e[0]]+5)%5);
 let full=0,allFailureCovered=0;const deleteCounts=[0,0,0,0,0];
 for(let i=0;i<625;i++){
  let t=i;const a=[];for(let j=0;j<4;j++){a.push(t%5);t=Math.floor(t/5);}
  const satisfied=E.map(e=>accepts(a,e));
  if(satisfied.every(Boolean))full++;
  if(satisfied.some(v=>!v))allFailureCovered++;
  for(let j=0;j<E.length;j++)if(satisfied.every((v,k)=>k===j||v))deleteCounts[j]++;
 }
 if(full!==0||allFailureCovered!==625||deleteCounts.some(x=>x===0))throw Error("T5 control failed");
 return {status:"COMPUTATIONAL",cases,unsat,yes,wrong_selector_rejections:wrong,
 pointwise_refutation_occurs_in_sat_cases:pointRefuteOnSat,
 t5:{arcs:E,original_assignments:625,original_satisfying:full,failed_arc_cover:allFailureCovered,edge_deletion_witness_counts:deleteCounts},
 theorem:"independent exhaustive finite checks; symbolic theorems not inferred"};
}
console.log(JSON.stringify(audit(),null,2));
