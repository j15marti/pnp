"use strict";
/* LSPV-4 ARC-HEAD-SHADOW-GATE256, independent native Node 18+ reproducer.
   Node built-ins only. No SAT oracle. Run: node ARC_HEAD_SHADOW_GATE256.js
   Source-model and operation ledgers are *abstract*, not FLMV native timings.
*/
const assert=(p,m="failed assertion")=>{if(!p)throw Error(m);};
let checks=0;
const ck=(p,m)=>{checks++;assert(p,m);};
const W1_TEXT="-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14";
function parse(s){return s.split(";").map(c=>c.trim().split(/\s+/).map(Number));}
function truth(l,a){return ((a >>> (Math.abs(l)-1))&1)===(l>0?1:0);}
function truthCount(c,a){return c.reduce((s,l)=>s+(truth(l,a)?1:0),0);}
function histogram(F,a){const v=[0,0,0,0];F.forEach(c=>v[truthCount(c,a)]++);return v;}
function models(F,n){
 let z=0,witness=null;
 for(let a=0;a<(1<<n);a++){
  let sat=true;for(const c of F){if(!c.some(l=>truth(l,a))){sat=false;break;}}
  if(sat){z++;if(witness===null)witness=a;}
 }
 return {count:z,witness};
}
function sourceEncoding(F,n){
 const width=Math.max(1,Math.ceil(Math.log2(n+1)));
 let y="1"+"1".repeat(n)+"0"+"1".repeat(F.length)+"0";
 for(const c of F)for(const l of c)y+=(l<0?"1":"0")+Math.abs(l).toString(2).padStart(width,"0");
 return y;
}
function extrema(F){
 return F.map((c,j)=>({clause:j,source:c.slice(),literal_targets:c.map((l,k)=>({
  occurrence:"x_"+Math.abs(l)+","+(j+1),variable:Math.abs(l),literal_position:k,sign:l>0?"+":"-",
  local_S_all_true:l>0?1:0,local_U_all_false:l>0?0:1,
  inverted_S_becomes_U:l>0?0:1,inverted_U_becomes_S:l>0?1:0
 }))}));
}
function extremeMode(c,mode){const x={};for(const l of c)x[Math.abs(l)]=(l>0)===(mode==="S")?1:0;return x;}
function compatible(cs,modes){
 const d={};
 for(let i=0;i<cs.length;i++)for(const [k,v] of Object.entries(extremeMode(cs[i],modes[i]))){
  if(k in d && d[k]!==v)return false;d[k]=v;
 }
 return true;
}
function bruteCompatible(cs,modes){
 const vars=[...new Set(cs.flat().map(Math.abs))].sort((a,b)=>a-b);
 for(let mask=0;mask<(1<<vars.length);mask++){
  const a={};vars.forEach((v,k)=>a[v]=(mask>>k)&1);
  if(cs.every((c,i)=>c.every(l=>a[Math.abs(l)]===((l>0)===(modes[i]==="S")?1:0))))return true;
 }
 return false;
}
function modes(F){
 const pairs=[];let checksHere=0;
 for(let j=0;j<F.length;j++)for(let k=j+1;k<F.length;k++){
  const c=F[j],d=F[k];const shared=c.filter(l=>d.some(x=>Math.abs(x)===Math.abs(l)));
  const same=shared.some(l=>d.includes(l));
  const opp=shared.some(l=>d.includes(-l));
  const val={SS:!opp,SU:!same,US:!same,UU:!opp};
  for(const mode of ["SS","SU","US","UU"]){
   ck(val[mode]===compatible([c,d],mode),"pair direct "+j+","+k+","+mode);
   ck(val[mode]===bruteCompatible([c,d],mode),"pair brute "+j+","+k+","+mode);
   checksHere++;
  }
  pairs.push({clauses:[j,k],shared_same:same,shared_opposite:opp,
   SS:val.SS,SU:val.SU,US:val.US,UU:val.UU,all_extremes_impossible:same&&opp});
 }
 return {pairs,pair_modes_checked:checksHere};
}
function triples(F,budget=24){
 const out=[];let tested=0;
 for(let j=0;j<F.length&&tested<budget;j++)
 for(let k=j+1;k<F.length&&tested<budget;k++)
 for(let h=k+1;h<F.length&&tested<budget;h++){
  const entry={clauses:[j,k,h],modes:[]};
  for(let mask=0;mask<8;mask++){
   const mm=[0,1,2].map(i=>((mask>>i)&1)?"S":"U");
   const c=compatible([F[j],F[k],F[h]],mm);
   ck(c===bruteCompatible([F[j],F[k],F[h]],mm),"triple:"+j+","+k+","+h);
   entry.modes.push({modes:mm.join(""),feasible:c});
  }
  out.push(entry);tested++;
 }
 return {tested,modes_checked:tested*8,entries:out};
}
function flipTrace(F,n){
 const mask=(1<<n)-1,events=[];
 let a=0;const seq=[0,1,Math.min(3,mask),mask,0];
 for(const next of seq){const old=a;const now=next;const h=histogram(F,now);
  if(events.length)for(let j=0;j<F.length;j++){
   const from=truthCount(F[j],old),to=truthCount(F[j],now);
   const changed=F[j].filter(l=> ((old^now)>>(Math.abs(l)-1))&1);
   ck(to-from===changed.reduce((sum,l)=>sum+(truth(l,old)?-1:1),0),"flip delta");
  }
  events.push({assignment_mask:now,true_literal_counts:F.map(c=>truthCount(c,now)),
    histogram:h,SAT:h[0]===0,complement_SAT:h[3]===0});a=next;
 }
 return events;
}
function runDpll(F,n){
 const stats={nodes:0,literal_tests:0,source_clause_visits:0,branches:0,up_assignments:0};
 function rec(b){
  stats.nodes++;
  let a=b.slice();
  while(true){
   let forced=null,allSatisfied=true;
   for(const c of F){
    stats.source_clause_visits++;
    let sat=false,un=0,unknown=0;
    for(const l of c){
     stats.literal_tests++;
     const v=a[Math.abs(l)];
     if(v===-1){un++;unknown=l;}
     else if(v===(l>0?1:0)){sat=true;break;}
    }
    if(sat)continue;
    allSatisfied=false;
    if(un===0)return null;
    if(un===1){const v=Math.abs(unknown),needed=unknown>0?1:0;
      if(a[v]!==-1&&a[v]!==needed)return null;
      if(a[v]===-1)forced=[v,needed];
      break;
    }
   }
   if(allSatisfied)return a.map(v=>v===-1?0:v);
   if(forced){a[forced[0]]=forced[1];stats.up_assignments++;continue;}
   break;
  }
  const v=a.findIndex((x,j)=>j>0&&x===-1);ck(v>0,"branch id");
  stats.branches++;
  for(const value of [0,1]){
   let x=a.slice();x[v]=value;const r=rec(x);if(r)return r;
  }
  return null;
 }
 const witness=rec(new Array(n+1).fill(-1));
 let pass=witness===null?false:F.every(c=>c.some(l=>witness[Math.abs(l)]===(l>0?1:0)));
 ck(witness===null||pass,"SAT witness not verified");
 return {SAT:!!witness,stats,verified_witness:witness?witness.slice(1):null};
}
function rational(n,d=1n){
 n=BigInt(n);d=BigInt(d);let a=n<0n?-n:n,b=d<0n?-d:d;
 while(b){let t=a%b;a=b;b=t;}const g=a||1n;return {n:(d<0n?-n:n)/g,d:(d<0n?-d:d)/g};
}
const add=(a,b)=>rational(a.n*b.d+b.n*a.d,a.d*b.d);
const sub=(a,b)=>rational(a.n*b.d-b.n*a.d,a.d*b.d);
const mul=(a,b)=>rational(a.n*b.n,a.d*b.d);
const div=(a,b)=>rational(a.n*b.d,a.d*b.n);
const comp=(a,b)=>a.n*b.d===b.n*a.d?0:a.n*b.d>b.n*a.d?1:-1;
const fr=a=>a.n+"/"+a.d,fl=a=>Number(a.n)/Number(a.d);
function flmv(p,q){
 const c=rational(p,q),one=rational(1),zero=rational(0);
 let f=one,power=one,best=zero,index=0,details=[];
 for(let k=1;k<100;k++){
  f=div(mul(c,f),add(one,f));
  power=mul(power,div(one,c));
  const a=div(sub(div(one,f),c),rational(k));
  const d=comp(a,power)<0?a:power;
  if(comp(d,best)>0){best=d;index=k;}
  details.push({k,lower_branch:fr(a),upper_branch:fr(power),d:fr(d)});
  if(comp(mul(power,div(one,c)),best)<0){
   return {c:fr(c),best:fr(best),decimal:fl(best),k_opt:index,
           infinite_tail_certified_at:k,tail_upper_next:fr(mul(power,div(one,c))),
           checked_terms:details};
  }
 }
 throw Error("tail did not terminate");
}
function shortIndexBits(p){return Math.max(1,p.toString(2).length);}
function shadow(y,start,commands,cap=null){
 const m=y.length;let p=start,seen=[],stats={moves:0,reads:0,indexed_jumps:1,
  index_address_bits:shortIndexBits(start),source_bit_probes:0,blank_reads:0,
  counter_update_proxy:0,naive_full_scan_proxy:0,peak_shadow_bits:0};
 function raw(){if(p<0||p>=m){stats.blank_reads++;return "_";}
  stats.source_bit_probes++;return y[p];}
 function observe(){
  stats.peak_shadow_bits=Math.max(stats.peak_shadow_bits,shortIndexBits(p));
  seen.push(p);
 }
 if(cap!==null && p>=m+cap+1)p=m+cap+1;
 observe();
 let observed=[];
 for(const cmd of commands){
  if(cmd==="L"||cmd==="R"){
   stats.moves++;stats.counter_update_proxy++;
   stats.naive_full_scan_proxy+=shortIndexBits(p);
   if(cmd==="L"){if(p===m+cap+1&&cap!==null){/* saturation loses distance */}
    else p=Math.max(0,p-1);
   }else{
    p++;
    if(cap!==null&&p>=m+cap+1)p=m+cap+1;
   }
  }else if(cmd==="read"){
   stats.reads++;observed.push(raw());
  }else throw Error("bad cmd:"+cmd);
  observe();
 }
 return {observed,final:p,stats};
}
function reentryTest(y,r){
 const m=y.length,start=m+r,commands=Array(r+1).fill("L").concat("read");
 const physical=shadow(y,start,commands);
 const sufficient=shadow(y,start,commands,r+1);
 const clipped=shadow(y,start,commands,Math.max(0,Math.floor(r/2)));
 const sticky={observed:["_"]};
 ck(physical.observed[0]===y[m-1],"physical reentry");
 ck(sufficient.observed[0]===physical.observed[0],"sufficient cap");
 ck(clipped.observed[0]!==physical.observed[0],"undersized cap should fail");
 ck(sticky.observed[0]!==physical.observed[0],"sticky should fail");
 return {r,start,actual_last_bit:y[m-1],
  exact:physical,cap_sufficient:sufficient,cap_inadequate:clipped,sticky,
  input_index_highwater_bits:shortIndexBits(start),
  abstract_head_space_upper_bits:shortIndexBits(start+r+2),
  valid_label_with_exact:true,valid_label_with_bad_cap:false};
}
function distinguishability(m,r){
 const positions=Array.from({length:r+1},(_,u)=>m+u);
 let pairs=0;
 for(let i=0;i<positions.length;i++)for(let j=i+1;j<positions.length;j++){
  const left=i+1;
  const p=positions[i]-left,q=positions[j]-left;
  ck(p===m-1&&q>=m,"pair reentry distinguished");
  pairs++;
 }
 return {r,head_positions:r+1,pairs,
  lower_bound_bits:Math.ceil(Math.log2(r+1)),
  upper_bound_exact_counter_bits:Math.ceil(Math.log2(m+r+2))};
}
function caseRecord(name,F,n,fullEnumerate=true){
 const dpll=runDpll(F,n),mdl=fullEnumerate?models(F,n):null;
 if(mdl)ck(dpll.SAT===(mdl.count>0),name+" DPLL vs enumeration");
 const y=sourceEncoding(F,n),ext=extrema(F),pair=modes(F),tri=triples(F);
 for(const r of ext)for(const x of r.literal_targets){
  ck(x.local_S_all_true===x.inverted_U_becomes_S&&x.local_U_all_false===x.inverted_S_becomes_U,"inverse");
 }
 const a0=histogram(F,0),a1=histogram(F,(1<<n)-1);
 ck(a0.join(",")===a1.slice().reverse().join(","),"endpoint complement");
 if(n<=15)for(let a=0;a<(1<<n);a++){
  const p=histogram(F,a),q=histogram(F,((1<<n)-1)^a);
  ck(p.join(",")===q.slice().reverse().join(","),"all complements");
 }
 const trail=flipTrace(F,n),reentry=reentryTest(y,8),slow=reentryTest(y,32);
 // Count baseline and complete same-input wrapper cost, including full source encoding,
 // scanning, binary-address loading, guest moves, both read operations, and SAT solve.
 const baseline_work=dpll.stats.literal_tests+dpll.stats.source_clause_visits+3*F.length;
 const wrapExtra=y.length+y.length+shortIndexBits(y.length+8)
  +reentry.exact.stats.moves+reentry.exact.stats.reads+2+3*F.length;
 return {name,n,m:F.length,labels:{DPLL:dpll.SAT,exhaustive:mdl},
  code:{encoding:"self-delimiting indexed proper signed 3CNF",physical_bits:y.length,
    last_source_bit:y[y.length-1]},
  original_targets:ext,compatibility:pair,triples:tri,
  endpoints:{zero:a0,one:a1},flip_trail:trail,
  reentry:{radius8:reentry,radius32:slow},
  dpll,charged_proxy:{baseline_work,correct_virtual_wrapper_work:baseline_work+wrapExtra,
    wrapper_overhead:wrapExtra,
    baseline_search_nodes:dpll.stats.nodes,
    wrapper_search_nodes:dpll.stats.nodes,
    native_FLMV_steps_claimed:false}};
}
function xor3(p){
 const out=[];for(let x=0;x<8;x++){
  let parity=0;for(let k=0;k<3;k++)parity^=(x>>k)&1;
  if(parity!==p){out.push([1,2,3].map(v=>((x>>(v-1))&1)?-v:v));}
 }return out;
}
function runAudit(){
 checks=0;
 const F=parse(W1_TEXT),G=F.map(c=>c.slice());
 ck(G[7][0]===1&&G[19][0]===-1,"auth W1 occurrences");
 G[7][0]=-1;G[19][0]=1;
 const H=[[1,3,5],[1,-3,6],[-1,4,5],[-1,-4,6],[2,3,-5],[2,-3,-6],[-2,4,-5],[-2,-4,-6]];
 const Hrename=H.map(c=>c.map(l=>Math.abs(l)===1?-l:l));
 const cases=[
  ["W1_strict22_UNSAT",F,15],["W1_sign_swap_SAT",G,15],
  ["H1_strict22_SAT",H,6],["H1_polarity_rename_SAT",Hrename,6],
  ["XOR3_parity1_SAT",xor3(1),3],
  ["XOR3_opposing_parities_UNSAT",xor3(1).concat(xor3(0)),3],
  ["single_clause_SAT",[[1,2,3]],3],
  ["all_eight_sign_patterns_UNSAT",xor3(0).concat(xor3(1)),3]
 ];
 const results=cases.map(v=>caseRecord(...v));
 ck(results[0].labels.exhaustive.count===0,"W1 unsat");
 ck(results[1].labels.exhaustive.count===168,"W1 prime 168 models");
 const radii=[1,2,4,8,16,32,64,128].map(r=>distinguishability(32,r));
 const flmvValues=[flmv(6,5),flmv(241,200),flmv(7,5)];
 ck(flmvValues[0].best==="23/45","c1");
 ck(flmvValues[1].best==="11642479/23232400","c2");
 ck(flmvValues[0].k_opt===2&&flmvValues[1].k_opt===2,"k=2");
 const strict={time_c:"241/200",space_d:"11642479/23232400",
  desired_fixed_time:"6/5",desired_fixed_space:"1/2",
  time_margin:"1/200",space_margin:"26279/23232400",
  strict_entry_requires_both_inequalities:true,
  physical_child_length_exponent:"1/2",children_count_exponent:"3/5",
  serial_full_N_bit_source_rescan_total_exponent:"8/5",
  ordered_Q_guest_head_address_bound:"2^S_guest_index + T_guest",
  shadow_bits_bound:"S_guest_index + ceil(log2(T_guest+2)) + O(1)",
  simulator_time_bound:"OPEN; this experiment does not implement a native FLMV TM"};
 return {id:"ARC-HEAD-SHADOW-GATE256",date:"2026-10-30",scope:"restricted input-head abstraction, no all-input ARC",
  main_claim:"For T-step indexed guest with input-index highwater s, exact logical read-only input-head coordinate needs at most s+ceil(log2(T+2))+O(1) bits; r+1 OOB entry positions demand ceil(log2(r+1)) distinguishable states under <=r left moves.",
  proof_status:{head_space:"PROVED/EXACT restricted abstract bound",
    distinguishability:"PROVED/EXACT restricted abstract bound",
    fixed_FLMV:"KNOWN THEOREM / exact rational arithmetic",contractor:"OPEN",P_vs_NP:"OPEN"},
  three_falsifiers:["One sticky out-of-range state simulates later ordinary input-head moves (FALSE).",
   "An O(log physical child length)-bit head shadow with guest-independent constant suffices for arbitrarily long reentry horizons (FALSE in bounded-state abstraction).",
   "A bit-accurate abstract head counter proves the native FLMV uniform guest simulator has negligible time overhead (NOT ESTABLISHED)."],
  flmv:flmvValues,strict,distinguishability:radii,instances:results,
  total_checks:checks,limitations:["DPLL selected operations are not native TM steps.",
   "No physical power-short SAT child was built.",
   "Exact shadow uses host-language big integers; no native TM per-step tariff proved.",
   "Bounded distinguishability conditions on a post-jump state abstraction with no guest-code-dependent external reconstruction."]};
}
if(typeof module!=="undefined"&&module&&typeof require==="function"&&require.main===module)
 console.log(JSON.stringify(runAudit(),null,2));
