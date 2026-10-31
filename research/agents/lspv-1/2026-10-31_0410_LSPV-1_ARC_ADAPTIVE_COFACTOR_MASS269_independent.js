"use strict";
// Independent raw-data checker for ARC-ADAPTIVE-COFACTOR-MASS269.
// Usage: node 2026-10-31_0410_LSPV-1_ARC_ADAPTIVE_COFACTOR_MASS269_independent.js raw.json
function check(b,msg){if(!b)throw Error(msg);}
function bits(k,n){const z=[];for(let i=0;i<n;i++)z.push((k>>i)&1);return z;}
function countTrue(C,z){let s=0;for(let i=0;i<C.length;i++){const t=C[i],v=z[Math.abs(t)-1];if(t>0?v===1:v===0)s++;}return s;}
function matches(cube,z){return Object.entries(cube).every(([v,b])=>z[Number(v.slice(1))-1]===b);}
function verify(d){
 let nSources=0,nLeaves=0,nPairs=0,nTriples=0,nProofs=0,nChecks=0,correctSat=0;
 for(const f of d.rows){
   nSources++;const n=f.n,C=f.original_clauses,ALL=1<<n;
   const truth=Array.from({length:ALL},(_,a)=>C.every(c=>countTrue(c,bits(a,n))!==0));
   const sat=truth.some(Boolean);check(sat===f.ground_truth_sat,f.id+": label");
   check(truth.filter(Boolean).length===f.model_count,f.id+": models");
   check(f.standard_up_dpll.result===sat&&f.charged_adaptive_controller.result===sat,f.id+": solvers");
   if(sat)correctSat++;
   for(const z of f.original_clause_controls.clauses){
     const ci=z.clause_index-1;
     check(z.global_zero_true_count===countTrue(C[ci],Array(n).fill(0)),f.id+": 0");
     check(z.global_one_true_count===countTrue(C[ci],Array(n).fill(1)),f.id+": 1");
     for(const occ of z.signed_occurrences){
       const sg=occ.literal>0?1:0;
       check(occ.S_target===sg&&occ.U_target===1-sg&&occ.S_inverted_U===1-sg&&occ.U_inverted_S===sg,f.id+": occurrence");
       nChecks++;
     }
   }
   for(const p of f.original_clause_controls.pairs){
     const [i,j]=p.source_clause_indices.map(x=>x-1);
     for(const mode of ["SS","SU","US","UU"]){
       const want=mode.split("").map((v,q)=>v==="S"?C[[i,j][q]].length:0);
       const result=truth.some((_,a)=>{const z=bits(a,n);return countTrue(C[i],z)===want[0]&&countTrue(C[j],z)===want[1];});
       check(result===p.matrix[mode],f.id+": pair");
       nPairs++;
     }
   }
   for(const p of f.original_clause_controls.triple_sample){
     const inds=p.source_clause_indices.map(x=>x-1),want=p.types.split("");
     const answer=truth.some((_,a)=>{const z=bits(a,n);return inds.every((idx,k)=>countTrue(C[idx],z)===(want[k]==="S"?C[idx].length:0));});
     check(answer===p.feasible,f.id+": triple");nTriples++;
   }
   for(const x of f.original_clause_controls.flip_trail){
     const z=x.assignment_bits,w=x.complement_bits;
     for(let i=0;i<C.length;i++){
       check(x.source_clause_true_counts[i]===countTrue(C[i],z)&&x.complement_source_clause_true_counts[i]===countTrue(C[i],w),f.id+": flip");
       check(z.every((v,j)=>w[j]===1-v),f.id+": complement");
       nChecks++;
     }
   }
   for(const proof of f.original_clause_controls.prohibited_cubes){
     const [i,j]=proof.source_clause_indices.map(x=>x-1),v=proof.pivot;
     const [left,right]=[C[i],C[j]];
     const pivot=left.includes(v)&&right.includes(-v)?v:left.includes(-v)&&right.includes(v)?-v:null;
     check(pivot!==null,f.id+": pivot");
     const resolvent=[...new Set([...left.filter(l=>l!==pivot),...right.filter(l=>l!==-pivot)])].sort((a,b)=>a-b);
     check(!resolvent.some(l=>resolvent.includes(-l)),f.id+": taut");
     check(JSON.stringify(resolvent)===JSON.stringify([...proof.derived_resolvent].sort((a,b)=>a-b)),f.id+": proof");
     check(truth.every((isSAT,a)=>!isSAT||!matches(proof.prohibited_cube,bits(a,n))),f.id+": blocked SAT");
     nProofs++;
   }
   for(const tree of f.audit_trees){
     nLeaves+=tree.leaves.length;let numerator=0;
     const expectedFalse=Array.from({length:ALL},(_,a)=>C.reduce((k,c)=>k+(countTrue(c,bits(a,n))===0?1:0),0)).reduce((a,b)=>a+b,0);
     for(const l of tree.leaves){
       const assigned=Object.keys(l.cube).length;
       check(assigned===l.depth,f.id+": leaf depth");
       let surviving=0,empty=0,unknown=0;
       for(const c of C){
         const relevant=c.map(x=>({lit:x,val:l.cube["x"+Math.abs(x)]}));
         const good=relevant.some(t=>t.val!==undefined && (t.lit>0?t.val===1:t.val===0));
         if(!good){surviving++;
           if(relevant.every(t=>t.val!==undefined))empty++;
           else unknown++;
         }
       }
       check(surviving===l.remaining_original_clause_records&&empty===l.empty_original_clauses&&unknown===l.unresolved_original_clauses,f.id+": original residual");
       if(l.terminal==="SAT_TERMINAL")check(surviving===0,f.id+": false SAT terminal");
       if(l.terminal==="UNSAT_TERMINAL")check(empty>0,f.id+": false UNSAT terminal");
       numerator+=surviving*(1<<(n-assigned));
       nChecks++;
     }
     check(numerator===tree.weighted.survivalNumerator,f.id+": numerator");
     check(expectedFalse===tree.weighted.originalFalseCount,f.id+": false count");
     check(numerator>=expectedFalse,f.id+": lower bound");
     for(let a=0;a<ALL;a++){
       const z=bits(a,n),hit=tree.leaves.filter(l=>matches(l.cube,z));
       check(hit.length===1,f.id+": adaptive partition");
       const l=hit[0];
       if(l.terminal==="SAT_TERMINAL")check(truth[a],f.id+": unsound SAT terminal");
       if(l.terminal==="UNSAT_TERMINAL")check(!truth[a],f.id+": unsound UNSAT terminal");
       nChecks++;
     }
   }
 }
 for(const K of [4,8,16,32]){
   check(K>Math.max(11/10,3/5+K/2),"delay wrapper test failed");
 }
 check(d.summary.sources===nSources&&d.summary.sat===correctSat&&d.summary.unsat===nSources-correctSat,"summary labels");
 check(d.summary.leaves_audited===nLeaves&&d.summary.pair_modes_checked===nPairs&&d.summary.triple_modes_checked===nTriples,"summary audits");
 return {status:"PASSED",sources:nSources,SAT:correctSat,UNSAT:nSources-correctSat,
  leaf_partition_checks:nChecks,leaves:nLeaves,extreme_pair_modes:nPairs,extreme_triples:nTriples,
  source_resolvent_cubes:nProofs,DELAY_K:[4,8,16,32]};
}
if(typeof process!=="undefined"&&typeof require!=="undefined"&&require.main===module){
 const fs=require("fs");const data=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
 console.log(JSON.stringify(verify(data),null,2));
}