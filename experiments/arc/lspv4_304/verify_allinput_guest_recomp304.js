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

// Independently re-evaluate source grammar, 5 malformed controls, original S/U and Gray trail.
const verifyExtra=function verifyExtra(raw){
 let checks=0;const ok=(v,s)=>{if(!v)throw Error("extra verifier "+s);checks++};
 const F=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9],[-4,-6,-8],[-1,-6,-7],[-2,-3,-4],[-3,-5,-8],[-1,-2,-9],[-5,-7,-9]];
 const Y=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]];
 function grammar(C,n){if(n%3||3*C.length!==4*n)return false;let degree=Array.from({length:n+1},()=>[0,0]),keys=new Set();for(const c of C){if(c.length!==3||new Set(c.map(Math.abs)).size!==3||c.some(l=>!Number.isInteger(l)||l===0||Math.abs(l)>n||Math.sign(l)!==Math.sign(c[0])))return false;let k=c.slice().sort((a,b)=>a-b).join('|');if(keys.has(k))return false;keys.add(k);for(const l of c)degree[Math.abs(l)][l<0?0:1]++}return degree.slice(1).every(d=>d[0]===2&&d[1]===2)}
 function count(C,a){return C.map(c=>c.filter(l=>(((a>>(Math.abs(l)-1))&1)===(l>0?1:0))).length)}
 ok(grammar(F,9)&&grammar(Y,6),"source grammar");
 let y=0,f=0;for(let m=0;m<64;m++)if(count(Y,m).every(v=>v))y++;for(let m=0;m<512;m++)if(count(F,m).every(v=>v))f++;
 ok(y===20&&f===70,"source model enumeration");
 const malformed=[F.concat([F[0]]),F.map((c,i)=>i===0?[c[0],-c[1],c[2]]:c),F.map((c,i)=>i===0?[c[0],c[0],c[2]]:c),F.slice(1),F.map((c,i)=>i===0?[c[0],c[1],999]:c)];
 for(let i=0;i<malformed.length;i++)ok(!grammar(malformed[i],9),"malformed "+i);
 for(let j=0;j<F.length;j++){const obj=raw.S_U_original_clause_targets[j];ok(obj.clause_id===j,"clause id");for(let k=0;k<3;k++){let l=F[j][k];let want=l>0?1:0;ok(obj.S[k].value===want&&obj.U[k].value===1-want&&obj.invert_S_to_U[k].value===1-want&&obj.invert_U_to_S[k].value===want,"original occurrence S/U")}}
 let last=count(F,0),D=0;for(let k=0;k<64;k++){let m=k^(k>>1),t=count(F,m),row=raw.offline_gray_flip_trace[k];ok(row.assignment_mask===m&&row.N0toN3.every((v,r)=>v===t.filter(y=>y===r).length),"Gray trace "+k);if(k>0){let x=0;for(let j=0;j<12;j++){let z=t[j]^last[j];x+=((z&1)?1:0)+((z&2)?1:0)}ok(row.logical_two_bit_xor===x,"XOR "+k);D+=x}last=t}ok(D===raw.offline_gray_sum_dlogic,"offline XOR total");
 return {extra_independent_checks:checks,grammar:true,malformed_rejections:5,source_counts:{F9:f,Y6:y},original_occurrence_targets:36,gray_steps:64,raw_match:true};
};
const extra=verifyExtra(raw);
console.log(JSON.stringify(extra,null,2));
