"use strict";
/* GENERATORBYPASS1: small exact logical controls, no hard RS5 instance is constructed.
 * Run: node experiments/review/lspv2_generatorbypass_audit.js
 * No packages, timeouts or stochastic seeds.
 */
function canonical(t) {
  const clauses = [];
  for (let a = 0; a < 8; a++)
    clauses.push([0,1,2].map(i => ((a >> i) & 1) ? -(i+1) : i+1));
  for (let j = 0; j < t; j++)
    clauses.push([4+3*j, 5+3*j, 6+3*j]);
  return {n: Math.max(3, 3+3*t), clauses};
}
function encode(F) {
  return `p cnf ${F.n} ${F.clauses.length}\n` +
    F.clauses.map(c => c.join(" ") + " 0").join("\n") + "\n";
}
function sat(F) {
  if (F.n > 14) throw new Error("exhaustive cap");
  for(let bits = 0; bits < (1 << F.n); bits++)
    if(F.clauses.every(c => c.some(l =>
      ((bits >> (Math.abs(l)-1)) & 1) === (l > 0 ? 1 : 0)))) return true;
  return false;
}
function recognized(s) {
  for(let t=0; t<=s.length; t++) {
    const candidate = encode(canonical(t));
    if(candidate === s) return t;
    if(candidate.length > s.length) break;
  }
  return null;
}
function failUnless(x,msg) { if(!x) throw new Error(msg); }
const family=[], mutations=[];
for(let t=0;t<=6;t++) {
  const F=canonical(t), s=encode(F), r=recognized(s);
  failUnless(r===t,"recognition failed t="+t);
  if(t<=3) failUnless(sat(F)===false,"canonical not UNSAT t="+t);
  family.push({t,bytes:s.length,clauses:F.clauses.length,recognized:true,
    bruteUnsat:t<=3?true:"not_exhausted"});
  if(t<=3) {
    const mutated=canonical(t);
    mutated.clauses.splice(0,1);
    const mutatedString=encode(mutated);
    failUnless(recognized(mutatedString)===null,"false generator positive");
    failUnless(sat(mutated)===true,"mutated formula should be SAT");
    mutations.push({t,not_recognized:true,bruteSAT:true});
  }
}
let checks=0, fail=0;
for(let H=1;H<=7;H++)
 for(let B=1;B<=7;B++)
  for(let R=1;R<=B;R++)
   for(let S0=1;S0<=R;S0++)
    for(let D0=0;D0<S0;D0++){
      if(D0<H) continue;
      for(let S=1;S<=10;S++)
       for(let D=0;D<S;D++){
        if(S<=B && D<H) continue;
        checks++;
        if(S<H) fail++;
       }
    }
failUnless(fail===0 && checks===11286,"cap-removal brute check failed");
const k=400000,c=164000,a=500,delta=1/200;
const q=4*a+c+1, u=a*(k+4)+k,z=a*(1-delta)*(k+c);
failUnless(q===166001 && u===200402000 && z===280590000,"RS5 ledger mismatch");
function variableRow(t){
 const k=Math.floor(t/(4*Math.log(t))), c=Math.floor(Math.sqrt(k)),
       a=Math.ceil(12*Math.sqrt(k)), delta=1/(4*Math.sqrt(k)), w=k+c;
 const log2nu=Math.log2(40)+2*Math.log2(k)+(c+1)*Math.log2(2*t);
 const ell=Math.ceil(1+log2nu),h=Math.ceil(1+a*Math.log2(t)+log2nu);
 const logLHS=a*delta*Math.log(t),
       logRHS_C1=Math.log(64)+Math.log(w+1)+Math.log(ell)+Math.log(h);
 const logUpperProofT=a*(k+4)+k+Math.log(4)/Math.log(t)*k+2*Math.log(k)/Math.log(t);
 const logCapT=a*(1-delta)*w;
 const logInputTUpper=4*a+c+1+
   ((c+1)*Math.log(2)+2*Math.log(k)+Math.log(80))/Math.log(t)+3;
 return {t,k,c,a,delta,spread_slack_ln_C1:logLHS-logRHS_C1,
   cap_margin_logt:logCapT-logUpperProofT,
   depth_exponent_over_input_upper:k/logInputTUpper};
}
const rows=[1e3,1e4,1e5,1e6,1e7].map(variableRow);
console.log(JSON.stringify({protocol:"deterministic bounded toy/exponent sanity",
 family, mutations, cap_removal:{admissible_checks:checks,failures:fail,
 without_incap_witness_counterexample:{B:1,H:3,minimal_proof_size:2}},
 RS5:{q,u,z,depth_margin:"7988/5",cap_margin:"135993/5"},
 variable_parameters:rows,
 limitations:"No hard formula instantiated. C=1 in spread logarithm only illustrates growth and is not an external constant bound."},null,2));
