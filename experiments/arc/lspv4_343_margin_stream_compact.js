// LSPV-4 audit 343: standalone Node.js reproduction, no dependencies.
// Conditional exponent margins are NOT an actual SAT solver or machine-time measurement.
"use strict";
const beta=c=>((c+2)/(c*c)-c)/2;
let left=1.2,right=1.3;
for(let i=0;i<100;i++){let m=(left+right)/2;if(beta(m)>.5)left=m;else right=m}
const crit=(left+right)/2;
function resource(a,b,d,rho,eta){const t=Math.max(d,a/(1-b)),s=Math.max(rho,eta,b);return {t,s,beta:beta(t),strict:s<beta(t)}}
const cases={
 baseline:resource(.6,.5,1.1,.5,.5),
 all_answers_retained:resource(.6,.5,1.1,.5,.6),
 full_source_copy:resource(.6,.5,1.1,1,.5),
 source_reread_each_child:resource(.6,.5,1.6,.5,.5),
 fanout_plus_003:resource(.603,.5,1.1,.5,.5),
 child_plus_003:resource(.6,.503,1.1,.5,.5),
 local_plus_001:resource(.6,.5,1.101,.5,.5)
};
function holds(F,a){return F.every(C=>C.some(l=>(((a>>(Math.abs(l)-1))&1)===Number(l>0))))}
function models(F,n){let count=0;for(let a=0;a<2**n;a++)if(holds(F,a))count++;return count}
const F=[[1],[-1,2],[-2]],G=[[1],[-1,2],[2]];
if(models(F,2)!==0||models(G,2)!==1||F.some((c,i)=>models(F.filter((_,j)=>i!==j),2)!==1))throw Error("core controls");
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function tseitin(q){let F=[];for(let v=0;v<4;v++){let ids=edges.map((e,i)=>e.includes(v)?i+1:null).filter(Boolean);
 for(let a=0;a<8;a++){let p=((a&1)+((a>>1)&1)+((a>>2)&1))&1;
 if(p===q[v])continue;F.push(ids.map((id,j)=>((a>>j)&1)?-id:id));}}return F;}
const odd=tseitin([1,0,0,0]),even=tseitin([0,0,0,0]);
if(models(odd,6)!==0||models(even,6)!==8)throw Error("parity controls");
let schedules=[1e4,1e6,1e8].map(N=>{let q=Math.ceil(N**.6),b=Math.ceil(N**.5);return {N,children:q,child_bits:b,eager_child_storage:q*b,eager_answer_storage:q,reused_buffer:b,stream_OR_answer_bits:1,stream_counter_bits:Math.ceil(Math.log2(q+1)),temp_source_copy:N}});
const out={status:"CONDITIONAL numerical/execution-model audit; P vs NP OPEN",critical_time:crit,beta_6_5:beta(1.2),beta_241_200:beta(241/200),strict_margin:1/90,
 fanout_delta:crit/2-.6,child_delta:.5-.6/crit,local_delta:crit-1.1,accessor_gamma_max:crit-.6,
 scenarios:cases,allocations:schedules,sat_control:{models_UNSAT:models(F,2),models_SAT_neighbor:models(G,2),minimum_binary_premise_nodes:2},tseitin:{odd:models(odd,6),even:models(even,6)}};
process.stdout.write(JSON.stringify(out,null,2)+"\n");
