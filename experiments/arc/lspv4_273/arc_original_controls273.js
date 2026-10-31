"use strict";
const fs=require("fs");
const {source}=require("./arc_bounded_guest273.js");
const input=JSON.parse(fs.readFileSync(process.argv[2]||"results/raw/arc/2026-10-31_0606_LSPV4_ARC_BOUNDED_GUEST273_raw.json","utf8"));
let cases=[],pairsChecked=0,occurrences=0,forbidden=0,resolutions=0;
for(const run of input.cases){
 let b=Array.from({length:run.q},(_,j)=>run.variant==="allzero"?0:run.variant==="lastone"?(j===run.q-1?1:0):j%2);
 const F=source(run.q,b),cl=F.clauses;
 const clauses=cl.map((c,j)=>({j:j+1,literals:c.slice(),
   occurrences:c.map((l,k)=>({variable:Math.abs(l),occurrence:k+1,sign:l>0?"+":"-",S:l>0?1:0,U:l>0?0:1,inverse_S:l>0?0:1,inverse_U:l>0?1:0})),
   forbidden_cube:c.map(l=>[Math.abs(l),l>0?0:1]),proof:{rule:"source_clause",id:j+1}}));
 let pairs=[];
 for(let i=0;i<cl.length;i++)for(let j=i+1;j<cl.length;j++){
   let a=cl[i],b=cl[j],same=a.some(l=>b.includes(l)),opp=a.some(l=>b.includes(-l));
   let predicted=(!opp?9:0)+(!same?6:0);
   let vars=[...new Set(a.concat(b).map(Math.abs))],actual=0;
   for(let mask=0;mask<(1<<vars.length);mask++){
      const z=new Map(vars.map((v,k)=>[v,(mask>>k)&1]));
      const cnt=c=>c.reduce((sum,l)=>sum+(z.get(Math.abs(l))===(l>0?1:0)?1:0),0);
      const ca=cnt(a),cb=cnt(b);
      if(ca===3&&cb===3)actual|=1;
      if(ca===3&&cb===0)actual|=2;
      if(ca===0&&cb===3)actual|=4;
      if(ca===0&&cb===0)actual|=8;
   }
   if(predicted!==actual)throw Error("compatibility "+run.q+"/"+run.variant+"/"+(i+1)+"/"+(j+1));
   pairs.push([i+1,j+1,actual]);pairsChecked++;
 }
 let parent1=cl[0],parent3=cl[2],pivot=parent1[1],resolvent=[...new Set(parent1.concat(parent3).filter(l=>Math.abs(l)!==Math.abs(pivot)))];
 if(parent3[1]!==-pivot||resolvent.some(l=>resolvent.includes(-l)))throw Error("resolution");
 let step={source_clause_ids:[1,3],pivot_literal:pivot,conclusion:resolvent,
    forbidden_cube:resolvent.map(l=>[Math.abs(l),l>0?0:1]),rule:"binary_resolution"};
 resolutions++;occurrences+=clauses.length*3;forbidden+=clauses.length+1;
 cases.push({q:run.q,variant:run.variant,n:F.n,m:cl.length,indexed_original_clauses:clauses,
   all_clause_pair_compatibility_bitmask_SS_SU_US_UU:pairs,derived_prohibited_cube:step,
   complement_endpoints:{zeros:run.sourceDiagnostics.endpoint0,ones:run.sourceDiagnostics.endpoint1},flip_trail:run.sourceDiagnostics.flipTrail});
}
const out={schema:"LSPV4_ARC_ORIGINAL_INDEXED_CONTROLS273",notes:"Each pair [j,k,mask] with SS bit 1, SU bit 2, US bit 4, UU bit 8. Every mask exhaustively checked on union variables. Each local S/U occurrence and inverse retained. Proofs are source axioms and one non-tautological source-indexed resolution.",cases,checks:{cases:cases.length,pairsChecked,occurrences,forbidden,resolutions}};
process.stdout.write(JSON.stringify(out,null,2)+"\n");
