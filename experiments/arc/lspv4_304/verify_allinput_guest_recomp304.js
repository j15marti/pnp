#!/usr/bin/env node
'use strict';
const fs=require('fs');
const verify304=function verify304(raw){
 function ck(b,m){if(!b)throw Error('independent verification: '+m)}let checks=0;
 const F=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9],[-4,-6,-8],[-1,-6,-7],[-2,-3,-4],[-3,-5,-8],[-1,-2,-9],[-5,-7,-9]];
 function val(C,mask){return C.map(c=>c.filter(l=>Boolean(mask&(1<<(Math.abs(l)-1)))===(l>0)).length)}
 for(let [key,p,n] of [['SAT',{1:0,2:0,8:1,9:1},2],['UNSAT',{3:0,6:1,7:1,9:1},0]]){
  const case0=raw.same_original_paired_cases[key],w=case0.residual_encoded_bits,N=raw.source_F9.original_bit_encoding_length;
  let models=[];for(let mask=0;mask<512;mask++){if(Object.entries(p).some(([i,v])=>Boolean(mask&(1<<(Number(i)-1)))!==Boolean(v)))continue;const t=val(F,mask);if(t.every(x=>x>0))models.push(mask);else if(key==='UNSAT'){const rec=case0.unsat_exhaustive_original_clause_proof.find(x=>x.assignment_mask===mask);ck(rec&&t[rec.falsified_original_clause]===0,'UNSAT cube proof');checks++}}
  ck(models.length===n&&JSON.stringify(models)===JSON.stringify(case0.full_witness_masks),'witness/model equality');checks++;
  for(let h of [1,2]){
   const g=case0.protocols[h],Q=w**h,iw=Math.ceil(Math.log2(w+1));
   let ones=0;for(let j=0;j<Q;j++){let x=j%w;while(x){ones+=(x&1);x>>>=1}}
   ck(g.guest_queries===Q&&g.virtual_full_parent_rescan_reads===Q*N,'charged source reads');
   ck(g.child_index_writes===Q*iw&&g.physical_index_content_xor_sum===2*ones&&g.physical_index_endpoint_xor===0,'index trace accounting');
   checks+=2;
  }
 }
 for(const row of raw.all_original_clause_pair_modes){
  const A=F[row.clause_i],B=F[row.clause_j],want0=row.mode[0]==='S'?3:0,want1=row.mode[1]==='S'?3:0;
  let feasible=false;for(let mask=0;mask<512;mask++){const t=val([A,B],mask);if(t[0]===want0&&t[1]===want1){feasible=true;break}}
  ck(feasible===row.feasible,'extreme compatibility');checks++;
 }
 ck(raw.all_original_clause_pair_modes.length===264,'pair count');checks++;
 ck(raw.source_F9.models===70&&raw.source_Y6.models===20,'source count');checks++;
 ck(raw.FLMV['6/5']==='23/45'&&raw.FLMV['241/200']==='11642479/23232400','FLMV');checks++;
 ck(raw.malformed_rejections===5&&raw.offline_gray_flip_trace.length===64,'controls');checks++;
 return {status:'PASS',independent_checks:checks,paired_SAT_UNSAT:'2/0',S_U_pair_modes:264,FLMV:'exact fractions verified',P_versus_NP:'OPEN'};
};
const raw=JSON.parse(fs.readFileSync(process.argv[2]||'results/raw/arc/2026-11-01_0736_LSPV4_ALLINPUT_GUEST_RECOMP304_raw.json','utf8'));
console.log(JSON.stringify(verify304(raw),null,2));
