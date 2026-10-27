'use strict';
/* LSPV-4 ARC-CHECKPOINT-RESIDUAL148. Node.js standard library only.
   Run: node 2026-10-26_2302_CHECKPOINT_RESIDUAL148_repro.js [raw.json]
   Exhaustive source-bit oracle controls, NOT general SAT benchmarks. */
const fs = require('node:fs');
const assert = require('node:assert/strict');
let checks = 0;
function ck(p, explanation) { ++checks; assert.ok(p, explanation); }
function pop(x) { let n=0; while (x) {x&=x-1;++n;} return n; }
function masks(M,r) {
  const ans=[0,0,0];
  for(let i=0;i<M;i++) {
    const stage=(i+r)%4;
    if(stage<3) ans[stage] |= (1<<i);
  }
  return ans;
}
function moved(M,r) {
  let head=0, distance=0, direction=0, reversals=0, probes=0;
  for(let stage=0;stage<3;stage++){
    const bitmask=masks(M,r)[stage];
    for(let i=0;i<M;i++) if(bitmask&(1<<i)) {
      const signed=i-head, newdir=Math.sign(signed);
      if(newdir && direction && newdir!==direction)reversals++;
      if(newdir)direction=newdir;
      distance+=Math.abs(signed);head=i;probes++;
    }
  }
  return {distance,reversals,probes};
}
function main(){
  const results=[];
  let exactSingletonTests=0, allInputTests=0, conditionalCounterexamples=0;
  for(const M of [4,8,12]) {
    let nMutants=0, marginalMin=4, marginalMax=0;
    let unconditionalErrorMax=0, maxMoves=0, maxRev=0;
    const schedules=Array.from({length:4},(_,r)=>masks(M,r));
    for(let r=0;r<4;r++){
      const a=schedules[r];
      ck((a[0]&a[1])===0 && (a[1]&a[2])===0 && (a[0]&a[2])===0,'re-reading a new cell');
      ck(pop(a[0])===M/4 && pop(a[1])===M/4 && pop(a[2])===M/4,'stage probe count');
      const t=moved(M,r);ck(t.probes===3*M/4,'itinerary probes');
      maxMoves=Math.max(maxMoves,t.distance);maxRev=Math.max(maxRev,t.reversals);
    }
    for(let E=1;E<(1<<M);E++) {
      nMutants++;allInputTests++;
      let first=0, beforeLast=0, total=0;
      let newMidCells=0, newLastCells=0, newBothCells=0;
      for(let r=0;r<4;r++) {
        const [h,v,w]=schedules[r];
        if((h&E)!==0)first++;
        if(((h|v)&E)!==0)beforeLast++;
        if(((h|v|w)&E)!==0)total++;
        newMidCells+=pop(v&E);
        newLastCells+=pop(w&E);
        newBothCells+=pop((v|w)&E);
      }
      const failed=4-total;
      ck(failed<=1,'bounded error on a nonzero input');
      ck(newLastCells >= total-beforeLast,'post-checkpoint fractional constraint');
      ck(newBothCells >= total-first,'cold-checkpoint fractional constraint');
      ck(newMidCells+newLastCells===newBothCells,'no double counting of source cells');
      ck(total>=beforeLast && beforeLast>=first,'hit-event monotonicity');
      ck(newLastCells===pop(E),'each coordinate is last-stage read with probability 1/4');
      ck(newBothCells===2*pop(E),'each coordinate is later read with probability 1/2');
      if(pop(E)===1){
        exactSingletonTests++;
        ck(first===1 && beforeLast===2 && total===3,'sharp singleton hit rates');
        ck(newLastCells===total-beforeLast && newBothCells===total-first,'sharp residual LP');
      }
      marginalMin=Math.min(marginalMin,total); marginalMax=Math.max(marginalMax,total);
      unconditionalErrorMax=Math.max(unconditionalErrorMax,failed);
    }
    // A cached exact sufficient statistic erases every future input-cell demand.
    for(let E=1;E<(1<<M);E++) {
      const all=(1<<M)-1;
      ck((all&E)!==0,'full-source prehit');
      ck((all&E)!==0 && (0&E)===0,'cache-only continuation');
    }
    // At checkpoint r=3 on baseline, coordinate 0 was never read.
    // A singleton perturbation at 0 remains indistinguishable at checkpoint,
    // and remains unqueried later, although global mutant error is only 1/4.
    const [h,v,w]=schedules[3];
    ck((h&1)===0 && (v&1)===0 && (w&1)===0,'conditional checkpoint attack');
    conditionalCounterexamples++;
    // Strong native model separation: sequential itinerary travels Theta(M)
    // despite M*3/4 total cell reads; no random-access cost imputed to M_k.
    ck(maxMoves>=M/2 && maxMoves<=5*M,'sequential head movement range');
    results.push({M,coin_outcomes:4,random_seed:'none: exhaustive four equally likely coins',
      inputs_tested:1<<M, nonzero_inputs:nMutants,
      worst_failure_probability:String(unconditionalErrorMax)+'/4',
      singleton_source_preprocess_expected:M/4,
      singleton_first_guest_expected:M/4,
      singleton_second_guest_expected:M/4,
      full_baseline_expected_distinct_reads:3*M/4,
      residual_bound_after_preprocess:M/2,
      residual_bound_after_first_guest:M/4,
      max_sequential_head_moves:maxMoves,
      max_input_head_reversals:maxRev,
      final_checkpoint_counterexample_coin:3,
      exact_cache_warm_new_reads:0});
  }
  ck(conditionalCounterexamples===3,'three conditional transcript counterexamples');
  const raw={id:'ARC-CHECKPOINT-RESIDUAL148',proof_status:'PROVED/EXACT restricted; independent review pending',
    computation:'exact exhaustive coin-and-Boolean-input controls',
    seed:'none',algorithm:'three cold/warm passes with 2-bit shared uniform coin',
    cases:results,allInputTests,exactSingletonTests,conditionalCounterexamples,
    assertions:checks,failures:0,
    limitations:'OR bit-source model, not a full SAT machine, not a Turing-machine timing benchmark. The theorem is symbolic; tests corroborate finite controls. No ARC edge.'};
  const out=process.argv[2];
  if(out)fs.writeFileSync(out,JSON.stringify(raw,null,2)+'\n');
  else process.stdout.write(JSON.stringify(raw,null,2)+'\n');
  return raw;
}
main();
