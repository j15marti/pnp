#!/usr/bin/env node
'use strict';
// Original-source paired SAT/UNSAT, S/U, Gray and restricted guest read tariffs.
const run304=function run304(){
 const pos=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9]],neg=[[4,6,8],[1,6,7],[2,3,4],[3,5,8],[1,2,9],[5,7,9]];
 const F=pos.concat(neg.map(c=>c.map(v=>-v))),Y=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]];
 function valid(C,n){if(n%3||3*C.length!==4*n)return false;let cnt=Array.from({length:n+1},()=>[0,0]),ids=new Set();for(let c of C){if(c.length!==3||new Set(c.map(Math.abs)).size!==3||c.some(x=>!Number.isInteger(x)||!x||Math.abs(x)>n||Math.sign(x)!==Math.sign(c[0])))return false;let k=c.slice().sort((a,b)=>a-b).join(',');if(ids.has(k))return false;ids.add(k);for(let x of c)cnt[Math.abs(x)][x>0?1:0]++;}return cnt.slice(1).every(z=>z[0]===2&&z[1]===2)}
 function counts(C,m){return C.map(c=>c.reduce((s,l)=>s+(((m>>(Math.abs(l)-1))&1)===(l>0?1:0)?1:0),0))}
 function ismodel(C,m){return counts(C,m).every(t=>t>0)}
 function allmodels(C,n,p={}){let out=[];for(let m=0;m<(1<<n);m++){if(Object.entries(p).some(([v,b])=>((m>>(Number(v)-1))&1)!==b))continue;if(ismodel(C,m))out.push(m)}return out}
 function residual(C,p){return C.filter(c=>!c.some(x=>p[Math.abs(x)]!==undefined&&p[Math.abs(x)]===(x>0?1:0))).map(c=>c.filter(x=>p[Math.abs(x)]===undefined))}
 function encode(C,n){let w=Math.ceil(Math.log2(n+1)),z=(v,k)=>v.toString(2).padStart(k,'0');return z(n,8)+z(C.length,8)+C.map(c=>z(c.length,2)+c.map(l=>(l<0?'1':'0')+z(Math.abs(l),w)).join('')).join('')}
 function pop(n){let c=0;while(n){c+=n&1;n>>=1}return c}
 if(!valid(F,9)||!valid(Y,6))throw Error('canonical grammar');
 const Fmodels=allmodels(F,9),Ymodels=allmodels(Y,6);
 if(Fmodels.length!==70||Ymodels.length!==20)throw Error('root models');
 const malformed=[F.concat([F[0]]),F.map((c,i)=>i===0?[c[0],-c[1],c[2]]:c),F.map((c,i)=>i===0?[c[0],c[0],c[2]]:c),F.slice(1),F.map((c,i)=>i===0?[c[0],c[1],999]:c)];
 if(malformed.some(C=>valid(C,9)))throw Error('malformed accepted');
 const originalTarget=F.map((c,j)=>({clause_id:j,polarity:c[0]>0?'+':'-',S:c.map(l=>({variable:Math.abs(l),value:l>0?1:0})),invert_S_to_U:c.map(l=>({variable:Math.abs(l),value:l>0?0:1})),U:c.map(l=>({variable:Math.abs(l),value:l>0?0:1})),invert_U_to_S:c.map(l=>({variable:Math.abs(l),value:l>0?1:0}))}));
 let compatibility=[];
 for(let i=0;i<F.length;i++)for(let j=i+1;j<F.length;j++){
  let same=F[i].some(l=>F[j].includes(l)),opposite=F[i].some(l=>F[j].includes(-l));
  for(let [k,types] of ['SS','SU','US','UU'].entries()){
   let possible=(types==='SS'||types==='UU')?!opposite:!same,observed=false;
   for(let m=0;m<512;m++){let ts=counts([F[i],F[j]],m);if(ts[0]===(types[0]==='S'?3:0)&&ts[1]===(types[1]==='S'?3:0)){observed=true;break}}
   if(possible!==observed)throw Error('compat mismatch');
   compatibility.push({clause_i:i,clause_j:j,mode:types,feasible:possible});
  }
 }
 let gray=[],sumXor=0,prev=counts(F,0),changed=new Set();
 for(let k=0;k<64;k++){let mask=k^(k>>1),next=counts(F,mask),ids=[],dx=0;for(let j=0;j<F.length;j++)if(next[j]!==prev[j]){ids.push(j);changed.add(j);dx+=pop(next[j]^prev[j])}if(k>0)sumXor+=dx;gray.push({step:k,assignment_mask:mask,changed_clause_ids:ids,logical_two_bit_xor:dx,N0toN3:[0,1,2,3].map(r=>next.filter(x=>x===r).length)});prev=next}
 const S=encode(F,9),N=S.length;
 function analyze(p,label){
  const R=residual(F,p),M=encode(R,9).length,models=allmodels(F,9,p);
  if((models.length>0)!==(label==='SAT'))throw Error('bad paired label');
  let proofs=[];
  if(label==='UNSAT'){for(let mask=0;mask<512;mask++){if(Object.entries(p).some(([v,b])=>((mask>>(v-1))&1)!==b))continue;const misses=counts(F,mask).flatMap((x,j)=>x===0?[j]:[]);if(!misses.length)throw Error('unsat proof missing');proofs.push({assignment_mask:mask,falsified_original_clause:misses[0]})}}
  let modes={};
  for(let h of [1,2]){
   const Q=M**h,w=Math.ceil(Math.log2(M+1));let bitOnes=0;
   for(let i=0;i<Q;i++)bitOnes+=pop(i%M);
   modes[h]={guest_queries:Q,virtual_full_parent_rescan_reads:Q*N,child_index_writes:Q*w,child_index_jumps:Q,child_index_head_moves:2*Q*(w-1),physical_index_content_xor_sum:2*bitOnes,physical_index_endpoint_xor:0,cached_child_materialization_writes:M,cached_child_plus_index_peak_bits:M+w};
  }
  return {label,pins:p,models:models.length,full_witness_masks:models,unsat_exhaustive_original_clause_proof:proofs,child_noncanonical_clause_widths:R.map(c=>c.length),residual_encoded_bits:M,protocols:modes};
 }
 const a=analyze({1:0,2:0,8:1,9:1},'SAT'),b=analyze({3:0,6:1,7:1,9:1},'UNSAT');
 function d2(p,q){let a=BigInt(p),b=BigInt(q),num=((a+2n*b)*b*b-a*a*a),den=2n*a*a*b;function gcd(x,y){return y?gcd(y,x%y):x};let g=gcd(num,den);return [num/g,den/g]}
 const first=d2(6,5),second=d2(241,200);
 if(first[0]!==23n||first[1]!==45n||second[0]!==11642479n||second[1]!==23232400n)throw Error('FLMV rational');
 function deltas(C){return [0,(1<<9)-1].map(mask=>[0,1,2,3].map(t=>counts(C,mask).filter(z=>z===t).length))}
 return {run:'LSPV-4_ALLINPUT_GUEST_RECOMP304',status:'COMPUTATIONAL; restricted theorem proved in report',source_F9:{variables:9,clauses:12,models:Fmodels.length,original_bit_encoding_length:N},source_Y6:{variables:6,clauses:8,models:Ymodels.length},malformed_rejections:malformed.length,S_U_original_clause_targets:originalTarget,all_original_clause_pair_modes:compatibility,allzero_allone_histograms:deltas(F),offline_gray_flip_trace:gray,offline_gray_sum_dlogic:sumXor,offline_gray_changed_record_ids:[...changed].sort((x,y)=>x-y),same_original_paired_cases:{SAT:a,UNSAT:b},FLMV:{'6/5':`${first[0]}/${first[1]}`,'241/200':`${second[0]}/${second[1]}`},declared_interface:'Faithful uncached guest reads. Each virtual child bit query deliberately rescans the entire 220-bit read-only source; physical index subtape writes/erasure counted for a fixed-width protocol. Source-address arithmetic, policy, proof production, guest decision, work/index head movement and peak live state outside the displayed subtapes remain unpaid.',status_P_versus_NP:'OPEN'};
};
console.log(JSON.stringify(run304(),null,2));
