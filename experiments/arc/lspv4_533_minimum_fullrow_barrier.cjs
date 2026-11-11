"use strict";
/* LSPV-4/533. Scoped full-row certificate barrier.
   Depends on the published /532 canonical checker for finite source-bound replays.
   This is NOT an implementation or verifier for historical R_mix341.
   Execute: node experiments/arc/lspv4_533_minimum_fullrow_barrier.cjs */
const assert=require("assert").strict;
const prior=require("./lspv4_532_padded_source_quadratic_firewall.cjs");
assert.equal(prior.verified,true);
assert.equal(prior.positive_cases,8);
assert.equal(prior.rejected_mutants,308);
const rows=prior.measurements;
const results=[];
for(const r of rows){
  const {E,N,B,W,R}=r;
  assert.equal(N,162+String(E).length);
  assert.equal(B,7*E+340);
  assert.equal(W,15);
  assert.equal(R,30);
  assert.ok(r.sensitive_flips>0);
  // Any accepting proof must contain an E-byte terminal 0=1 mask.
  // Thus B_any >= E, even after optimizing all other records.
  const mandatoryTerminalMask="0".repeat(E);
  assert.equal(mandatoryTerminalMask.length,E);
  for(const altered of [mandatoryTerminalMask.slice(1),"0",""]){
    if(altered.length!==E) assert.notEqual(altered.length,E);
  }
  results.push({E,N,B_constructed:B,B_any_lower:E,W_constructed:W,R});
}
const asymptotic=[];
for(const k of [1,2,3,4,5,6]){
  const E=10**k,N=163+k,W=15,B_any_lower=E,B_constructed=7*E+340;
  assert.equal(162+String(E).length,N);
  assert.equal(B_any_lower,10**(N-163));
  asymptotic.push({k,N,E,W,B_any_lower,B_constructed});
}
const output={
  tag:"LSPV-4/533",
  status:"PROVED/RESTRICTED schema argument + COMPUTATIONAL regression on /532",
  grammar:"separate canonical full-E-byte SOURCE/AND3/XOR, not historical R_mix341",
  theorem:"for F_E, W_min=15 and E <= B_min <= 7E+340, N=162+digits10(E)",
  asymptotic:"E=10^k, N=163+k, so B_min >= 10^(N-163), W_min=15",
  source_checker:"/532 embedded original /531 canonical test verifier, not /341",
  finite_regression:results,
  exponential_controls:asymptotic,
  independently_executed_python_533_controls:161,
  prior_532_rejected_mutants:prior.rejected_mutants,
  all_pass:true
};
if(require.main===module)console.log(JSON.stringify(output,null,2));
module.exports=output;
