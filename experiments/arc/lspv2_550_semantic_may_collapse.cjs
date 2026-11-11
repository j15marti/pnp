"use strict";
/* LSPV-2/550: structural reference replay, NOT native R_mix341 parser.
 Run: node experiments/arc/lspv2_550_semantic_may_collapse.cjs */
function ck(x,m){if(!x)throw Error(m)}
function bits(x){let n=0;for(;x;x&=x-1)n++;return n}
function cube(){return Array.from({length:8},(_,a)=>[0,1,2].map(i=>a&(1<<i)?-(i+1):i+1))}
function models(C,n){let r=[];for(let a=0;a<(1<<n);a++)
 if(C.every(c=>c.some(l=>{let v=!!(a&(1<<(Math.abs(l)-1)));return l>0?v:!v})))r.push(a);return r}
function minimumUnion(m){
 ck(m>=1&&m<=12,"DP bound");const N=1<<m,D=Array(N).fill(Infinity);
 for(let s=1;s<N;s++){
  if(bits(s)===1){D[s]=0;continue}
  for(let a=(s-1)&s;a;a=(a-1)&s){let b=s^a;if(b)D[s]=Math.min(D[s],D[a]+D[b]+1)}
 }
 return D[N-1]
}
function replay(m,steps){
 const known=new Map(Array.from({length:m},(_,i)=>["s"+i,{mask:1<<i,depth:0}]));
 let paid=0;
 for(const p of steps){
  ck(!known.has(p.id),"duplicate identity");
  ck(["RES","AND3","XOR","MAY-BINARY"].includes(p.rule),"unknown reference opcode");
  ck(Array.isArray(p.parents)&&p.parents.length===2,"binary premise restriction");
  ck(p.parents[0]!==p.parents[1],"same parent");
  let a=known.get(p.parents[0]),b=known.get(p.parents[1]);
  ck(a&&b,"missing/forward parent");
  let mask=a.mask|b.mask;
  ck(p.claim===undefined||p.claim===mask,"forged source provenance");
  known.set(p.id,{mask,depth:1+Math.max(a.depth,b.depth)});paid++;
 }
 let z=known.get(steps.at(-1).id);
 return {logical_paid:paid,source_mask:z.mask,ideal_span:z.depth,distinct_paid:paid}
}
function discharge(o){
 ck(o.positive&&o.negative,"branch AND obligation");
 ck(o.positive.assumption===o.var&&o.negative.assumption===-o.var,"bad branch labels");
 ck(o.positive.false===true&&o.negative.false===true,"branch not refuted");return true
}
function run(){
 const F=cube(),ALL=255,del=F.map((_,i)=>models(F.filter((_,j)=>j!==i),3));
 ck(models(F,3).length===0&&del.every(x=>x.length===1),"minimal UNSAT");
 const P=[["d0","RES","s0","s1"],["d1","RES","s2","s3"],
 ["d2","AND3","d0","d1"],["d3","RES","s4","s5"],
 ["d4","RES","s6","s7"],["d5","AND3","d3","d4"],
 ["d6","XOR","d2","d5"]].map(([id,rule,a,b])=>({id,rule,parents:[a,b]}));
 const positive=replay(8,P),DP=minimumUnion(8);
 ck(positive.source_mask===ALL&&positive.logical_paid===7&&DP===7,"reference positive");
 const globalMay={rule:"MAY-GLOBAL-SEMANTIC",parents:[],sources_mask:ALL,
  conclusion:"BOTTOM",paid:1,globally_entailed:models(F,3).length===0};
 let tests={};
 try{replay(8,[{id:"x",rule:"MAY-BINARY",parents:[],claim:ALL}]);tests.global_oracle_blocked=false}catch(e){tests.global_oracle_blocked=true}
 tests.sat_input_blocks_global_bottom=models([[1]],1).length>0;
 try{replay(8,[{...P[0],parents:["s0","missing"]}]);tests.forward_parent_rejected=false}catch(e){tests.forward_parent_rejected=true}
 try{replay(8,[P[0],{...P[1],id:"d0"}]);tests.duplicate_paid_rejected=false}catch(e){tests.duplicate_paid_rejected=true}
 try{replay(8,[{id:"fake",rule:"MAY-BINARY",parents:["s0","s1"],claim:ALL}]);tests.fake_source_support_rejected=false}catch(e){tests.fake_source_support_rejected=true}
 try{discharge({var:1,positive:{assumption:1,false:true}});tests.one_branch_discharge_rejected=false}catch(e){tests.one_branch_discharge_rejected=true}
 tests.two_branch_discharge_accepted=discharge({var:1,positive:{assumption:1,false:true},negative:{assumption:-1,false:true}});
 ck(Object.values(tests).every(Boolean),"hostile control failed");
 return {run:"LSPV-2/550",mode:"independent provenance abstraction",
 source:"full signed 3-CNF cube /547",clauses:F,models:0,
 individual_source_deletion_witnesses:del,reference_paid_DAG:positive,
 exact_union_partition_DP:DP,semantic_global_may:globalMay,
 may_abstraction_min_cost_upper_bound:1,
 binary_provenance_min_cost_lower_bound:7,
 all_hostile_controls_passed:tests,
 statement:"Source-unspecified global semantic entailment MAY admits an UNSAT-to-bottom shortcut costing 1. Requiring exactly two parent identities and exact provenance union excludes that shortcut, without purporting to authenticate missing historical rules.",
 limits:{logical_paid:"exact reference node count",certificate_bits:"not equivalent",
 construction_time:"not measured",physical_peak_space:"not measured",
 historical_checker:"not invoked; native syntax for full R_mix341 unknown"},
 open:["P2-D1","P2-C3","P2-B1","P2-B2/B3","P versus NP"]};
}
if(typeof require==="function"&&typeof module!=="undefined"&&require.main===module)
 console.log(JSON.stringify(run(),null,2));
