// CLOCK-GATE-FINITE1. Deterministic exhaustive finite analogue of the
// fixed-clock witness-slice construction. Node 18+, no dependencies.
// 2026-10-18; every 2-variable assignment predicate is enumerated.
// This is a finite semantics check, NOT a complexity lower bound.
"use strict";
const W=4, J=8, m=7, S=2;
function decode(d,w,j,k,z) {
  const x=z&1, y=(z>>1)&1;
  switch(d) {
    case 0:return 0;
    case 1:return 1;
    case 2:return x^((k+w+j)&1);
    case 3:return y^((k+2*j)&1);
    case 4:return x^y^(k&1);
    case 5:return (x&y)^(w&1);
    case 6:return (x|y)^(j&1);
    case 7:return x ? y : ((k>>1)&1);
    default:throw Error("invalid decoder");
  }
}
function word(d,w,j,z){
  let v=0;
  for(let k=0;k<m;k++)v |= decode(d,w,j,k,z)<<k;
  return v;
}
function popcount(x){let s=0;while(x){s+=x&1;x>>=1;}return s;}
function remote(w,j){
  let winner=-1, bestMargin=-1;
  for(let v=0;v<(1<<m);v++){
    let margin=m+1;
    for(let z=0;z<(1<<S);z++)
      margin=Math.min(margin,popcount(v^word(j,w,j,z)));
    if(margin>bestMargin){bestMargin=margin;winner=v;}
  }
  return {v:winner,margin:bestMargin};
}
const H=Array.from({length:W},
  (_,w)=>Array.from({length:J},(_,j)=>remote(w,j)));
let finiteRemotenessChecks=0, satNonmemberChecks=0,
    unsatPositiveRepresentations=0, mistakes=0;
for(let w=0;w<W;w++)for(let j=0;j<J;j++)
  for(let z=0;z<(1<<S);z++){
    finiteRemotenessChecks++;
    if(H[w][j].v===word(j,w,j,z))mistakes++;
  }
for(let mask=0;mask<(1<<W);mask++){
  for(let d=0;d<J;d++)for(let z=0;z<(1<<S);z++){
    let matches=true;
    for(let w=0;w<W&&matches;w++)
      for(let j=0;j<J&&matches;j++)
        if((((mask>>w)&1)?H[w][j].v:0)!==word(d,w,j,z))
          matches=false;
    if(mask===0){
      if(d===0&&matches)unsatPositiveRepresentations++;
    }else{
      satNonmemberChecks++;
      if(matches)mistakes++;
    }
  }
}
const n=4,Q=1<<n,L=6,t=2;
const checkedWitnesses=Array.from({length:L},
  (_,i)=>[(3*i+1)%Q,(5*i+3)%Q]);
const covered=[...new Set(checkedWitnesses.flat())].sort((a,b)=>a-b);
const missed=Array.from({length:Q},(_,i)=>i)
  .filter(i=>!covered.includes(i));
const xorHashFailureMasks=[];
for(let mask=1;mask<(1<<W);mask++){
  const parity=[0,0];
  for(let w=0;w<W;w++)if(mask&(1<<w))parity[w&1]^=1;
  if(parity[0]===0&&parity[1]===0)
    xorHashFailureMasks.push(mask);
}
const output={
  name:"CLOCK-GATE-FINITE1",
  model:"8 two-probe decoder families, 2 seed bits",
  witnesses:W, decoders:J, block_bits:m, seed_bits:S,
  full_output_bits:W*J*m,
  source_predicates_tested:1<<W,
  finite_remoteness_checks:finiteRemotenessChecks,
  sat_nonmember_checks:satNonmemberChecks,
  unsat_constant_zero_representations:unsatPositiveRepresentations,
  minimum_hamming_margin:Math.min(...H.flat().map(x=>x.margin)),
  hamming_margin_histogram:H.flat().reduce((a,x)=>
    (a[x.margin]=(a[x.margin]||0)+1,a),{}),
  failures:mistakes,
  witness_coverage_example:{
    n,possible_witnesses:Q,outputs:L,checks_per_output:t,
    queried_witnesses:checkedWitnesses,covered,missed,
    lower_bound_outputs:Math.ceil(Q/t)},
  xor_hash_failure_masks:xorHashFailureMasks
};
console.log(JSON.stringify(output,null,2));
if(mistakes)process.exitCode=1;
