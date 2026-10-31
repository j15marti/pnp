// ARC-INDEX-RECHARGE283. Standard Node.js, zero dependencies.
// git root: node experiments/arc/2026-10-31_1400_LSPV1_INDEX_RECHARGE283.js
// Optional fixture: research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt
// Full-state XOR is OFFLINE observation, never an uncharged SAT operation.
"use strict";
function pc(z) { let v=z >>> 0, t=0; while(v){v &= v-1;t++;}return t; }
function target(F){
  if (!Array.isArray(F) || !F.length) return false;
  const n=Math.max(...F.flat().map(x=>Math.abs(x)));
  if(n%3 || F.length*3!==4*n) return false;
  const count=Array.from({length:n+1},()=>[0,0]), keys=new Set();
  for(const c of F){
    if(c.length!==3||new Set(c.map(x=>Math.abs(x))).size!==3||
       !c.every(x=>x>0)&&!c.every(x=>x<0))return false;
    const key=c.slice().sort((x,y)=>x-y).join(",");
    if(keys.has(key))return false;keys.add(key);
    for(const l of c)count[Math.abs(l)][l>0?1:0]++;
  }
  return count.slice(1).every(z=>z[0]===2 && z[1]===2);
}
const P6=[[1,2,3],[1,4,5],[2,4,6],[3,5,6]],
      Q6=[[1,2,4],[1,3,6],[2,3,5],[4,5,6]],
      Y6=P6.concat(Q6.map(c=>c.map(x=>-x)));
const W1=[[-1,3,-14],[2,-8,9],[10,-13,14],[3,7,-13],[-4,-9,-11],
 [5,8,-14],[4,-8,-11],[1,7,13],[1,-7,10],[-5,-6,-15],
 [-2,-6,12],[-4,9,-10],[-2,5,-12],[-3,6,-15],[6,-7,11],
 [2,-9,11],[4,8,-10],[-3,12,15],[-5,-12,15],[-1,13,14]];
function truth(F,a) {
 return F.map(c=>c.reduce((k,l)=>k+Number(!!(a&(1n<<BigInt(Math.abs(l)-1)))===(l>0)),0));
}
function fullEnum(F,n){
 let models=0, witness=null;
 for(let s=0;s<(1<<n);s++){
  if(truth(F,BigInt(s)).every(t=>t>0)){models++; if(witness===null)witness=s;}
 }
 return {model_count:models,example_witness:witness};
}
function clausePairs(F){
 const m=F.length; const masks=[];let counts={"f":0,"9":0,"6":0,"0":0};
 for(let j=0;j<m;j++)for(let k=j+1;k<m;k++){
  let same=false,opp=false;
  for(const a of F[j])for(const b of F[k])if(Math.abs(a)===Math.abs(b)){
   if(Math.sign(a)===Math.sign(b))same=true;else opp=true;
  }
  const mask=(opp?0:9)|(same?0:6);
  counts[mask.toString(16)]=(counts[mask.toString(16)]||0)+1;
  masks.push(mask.toString(16));
 }
 return {ordering:"zero_based_j<k_lexicographic",masks_hex:masks.join(""),counts};
}
function extremes(F){
 return F.map((c,j)=>({j,source_literals:c,
   S_all_literals_true:c.map(l=>[Math.abs(l),Number(l>0)]),
   U_all_literals_false:c.map(l=>[Math.abs(l),Number(l<0)]),
   invert_S_equals_U:true,invert_U_equals_S:true}));
}
function sweep(F,n) {
 let a=0n, before=truth(F,a), totalBin=0,totalGray=0,totalPhysicalAssign=0,rows=[];
 const first=before.reduce((v,t)=>{v[t]++;return v;},[0,0,0,0]);
 for(let i=0;i<n;i++){
  a^=1n<<BigInt(i);
  const after=truth(F,a), changed=[];
  for(let j=0;j<F.length;j++) if(before[j]!==after[j]){
    const old=before[j], neu=after[j];
    if(Math.abs(old-neu)!==1)throw Error("nonunit original source-clause change");
    totalBin+=pc(old^neu);totalGray+=pc((old^(old>>1))^(neu^(neu>>1)));
    changed.push(j);
  }
  if(changed.length!==4)throw Error("strict22 source occurrence violation");
  totalPhysicalAssign++;
  if(rows.length<12||i===n-1) rows.push({flip:i+1,changed_original_clauses:changed});
  before=after;
 }
 const end=before.reduce((v,t)=>{v[t]++;return v;},[0,0,0,0]);
 const m=F.length;
 if(totalBin!==4*m||totalGray!==3*m)throw Error("source sweep closed form violated");
 return {initial_counts:first,final_counts:end,record_changes:4*n,
   logical_status_binary_XOR:totalBin,logical_status_gray_XOR:totalGray,
   logical_including_assignment_binary:totalBin+n,
   logical_including_assignment_gray:totalGray+n,
   lazy_assignment_only_physical_changes:totalPhysicalAssign,
   selected_original_clause_trail:rows};
}
function auditSource(F,label,cert){
 if(!target(F))throw Error("source fails proper duplicate-free monotone exact22");
 const n=Math.max(...F.flat().map(x=>Math.abs(x))),m=F.length;
 const local=extremes(F), pairs=clausePairs(F);
 if(pairs.counts["0"])throw Error("impossible mixed-same/opposite pair in monotone source");
 const sw=sweep(F,n);
 if(sw.initial_counts[0]!==m/2||sw.initial_counts[3]!==m/2)
    throw Error("bad full source endpoints");
 for(const e of local)if(e.S_all_literals_true.some((z,k)=>z[1]===e.U_all_literals_false[k][1]))
     throw Error("local occurrence inverse error");
 return {label,certificate_status:cert,n,m,local_extremes:local,
   extreme_pair_compatibility:pairs,logical_sweep:sw};
}
// Bit-machine abstract primitive: set a single index bit, flip one work bit,
// read without a write, or reset ALL index bits at once. The index begins blank.
// q=1 ordinary changed writable bit per step; reads and unchanged writes cost time.
function enumerateMachine(width,depth) {
 const all=(1<<width)-1,ops=[];
 for(let i=0;i<width;i++)for(const v of [0,1])ops.push({kind:"write-index",i,v});
 ops.push({kind:"indexed-jump-reset"},{kind:"work-flip"},{kind:"read"});
 let leaves=0,stepsChecked=0,maxD=0,nonzeroReset=0;
 function rec(index,work,t,P,E,D){
  if(E>P)throw Error("index erasures exceeded prior 0->1 charge");
  if(D>t+E||D>2*t)throw Error("amortized index-XOR inequality false");
  stepsChecked++;maxD=Math.max(D,maxD);
  if(t===depth){leaves++;return;}
  for(const op of ops){
   let idx=index,w=work,e=0,p=0;
   if(op.kind==="write-index"){
      const bit=1<<op.i;idx=op.v?(index|bit):(index&~bit);
      if(op.v&&!(index&bit))p=1;
   } else if(op.kind==="indexed-jump-reset"){
      e=pc(index);idx=0;if(e)nonzeroReset++;
   } else if(op.kind==="work-flip") w^=1;
   const delta=pc(idx^index)+(w!==work?1:0);
   rec(idx,w,t+1,P+p,E+e,D+delta);
  }
 }
 rec(0,0,0,0,0,0);
 return {width,depth,leaves,states_checked:stepsChecked,max_cumulative_XOR:maxD,
         nonempty_index_resets:nonzeroReset};
}
function machineExample(h) {
 let idx=0,t=0,D=0,E=0,P=0,peak=0;
 for(let i=0;i<h;i++){idx|=1<<i;t++;D++;P++;peak=Math.max(peak,pc(idx));}
 const resetDelta=pc(idx);idx=0;t++;D+=resetDelta;E+=resetDelta;
 if(!(D>t && D<=2*t && E===P))throw Error("reset counterexample failed");
 return {index_bits:h,initially_blank:true,indexed_reset_step_XOR:resetDelta,
         native_reset_steps:1,total_preparation_plus_reset_steps:t,
         cumulative_full_XOR:D,ordinary_0_to_1_writes:P,
         index_bulk_erased_bits:E,maximum_live_index_ones:peak,
         old_unit_step_claim_falsified:true,new_complete_trace_bound_passed:true};
}
function runAudit(rawText){
 const results={claim:"ARC-INDEX-RECHARGE283",time_zone:"America/Los_Angeles",
  status:"EXACT model-specific theorem; COMPUTATIONAL controls; P versus NP OPEN",
  machine:{q:1,initial_index_ones:0,
   checked_enumerations:[[1,7],[2,6],[3,5],[4,5]].map(z=>enumerateMachine(...z)),
   reset16:machineExample(16),
   zero_delta_positive_time:{T:100,data_XOR:0,reads:100},
   restore_example:{T:2,endpoint_XOR:0,cumulative_XOR:2}},
  sources:{Y6:auditSource(Y6,"SAT","INDEPENDENT_EXHAUSTIVE_64_ASSIGNMENTS"),
           W1_comparative_superset:{grammatical_scope:"strict signed (2,2), not canonical monotone",
                   exhaustive:fullEnum(W1,15)}}};
 results.sources.Y6.independent_exhaustive=fullEnum(Y6,6);
 if(results.sources.Y6.independent_exhaustive.model_count!==20)throw Error("Y6 certificate failed");
 if(results.sources.W1_comparative_superset.exhaustive.model_count!==0)throw Error("W1 certificate failed");
 if(rawText){
  const txt=rawText.slice(rawText.indexOf("[["));
  const U=JSON.parse(txt);
  const V=U.map(c=>c.slice());
  if(U[2][2]!==197||U[44][2]!==196)throw Error("U198 source identity mismatch");
  [V[2][2],V[44][2]]=[V[44][2],V[2][2]];
  results.sources.U198=auditSource(U,"UNSAT","PRIOR_VERIFIED_SIX_MODULE_BOUNDARY_CERTIFICATE");
  results.sources.V198=auditSource(V,"SAT","PRIOR_VERIFIED_198_BIT_WITNESS");
  if(results.sources.U198.n!==198||results.sources.U198.m!==264||
     results.sources.V198.n!==198||results.sources.V198.m!==264)
     throw Error("U/V size mismatch");
 }
 results.totals={finite_machine_checks:results.machine.checked_enumerations
   .reduce((x,y)=>x+y.states_checked,0),canonical_sources_audited:rawText?3:1,
   all_canonical_sources_proper:true,
   no_polynomial_SAT_lower_bound_claim:true};
 return results;
}
if(typeof module!=="undefined" && module.exports) module.exports={runAudit};
if(typeof require!=="undefined" && require.main===module){
  const fs=require("fs"),p=require("path");
  const filepath=p.resolve(__dirname,"../../research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt");
  const data=fs.existsSync(filepath)?fs.readFileSync(filepath,"utf8"):null;
  const output=runAudit(data);
  process.stdout.write(JSON.stringify(output,null,2)+"\n");
}
// END_OF_VERIFIED_REPRO::ARC-INDEX-RECHARGE283
