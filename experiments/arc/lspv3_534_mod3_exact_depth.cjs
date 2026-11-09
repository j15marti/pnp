#!/usr/bin/env node
'use strict';
// LSPV-3/534: exact (unrestricted-size) nonlinear AND depth for restricted MOD3.
// This is a deterministic functional-circuit audit, NOT a historical R_mix341 proof.
const assert=require('node:assert/strict');
function pop(x){ let n=0;while(x){x&=x-1;n++;}return n;}
function kCoeff(k,c){return k===0?Number(c===0):Number((k+c)%3!==0);}
function directCoeff(mask,c){
  let ans=0,s=mask;
  do {ans^=Number(pop(s)%3===c);if(s===0)break;s=(s-1)&mask;}while(true);
  return ans;
}
function mobius(a,b){
  const out=a.slice();
  for(let i=0;i<b;i++){const bit=1<<i;
    for(let mask=0;mask<out.length;mask++)if(mask&bit)out[mask]^=out[mask^bit];
  }
  return out;
}
function depth(d){return d<=1?0:Math.ceil(Math.log2(d));}
function main(){
  const rows=[]; let truthInputs=0,coefficientChecks=0,hostile=0;
  for(let b=2;b<=12;b++) for(let c=0;c<3;c++){
    const size=1<<b, coeff=[];
    for(let mask=0;mask<size;mask++){
      const z=directCoeff(mask,c), expected=kCoeff(pop(mask),c);
      assert.equal(z,expected);coeff.push(z);coefficientChecks++;
    }
    const d=Math.max(...coeff.map((a,mask)=>a?pop(mask):0));
    assert.equal(d,b-Number((b+c)%3===0));
    const truth=mobius(coeff,b);
    for(let x=0;x<size;x++){assert.equal(truth[x],Number(pop(x)%3===c));truthInputs++;}
    const firstTop=coeff.findIndex((a,mask)=>a&&pop(mask)===d);
    assert.ok(firstTop>=0);
    const mut=coeff.slice();mut[firstTop]^=1;
    assert.notDeepEqual(mobius(mut,b),truth);hostile++;
    const mono=coeff.reduce((acc,a)=>acc+a,0);
    const andGates=coeff.reduce((acc,a,mask)=>acc+(a?Math.max(0,pop(mask)-1):0),0);
    const exactDepth=depth(d),balancedDepth=depth(b);
    rows.push({b,charge:c,degree:d,exact_min_and_depth:exactDepth,
      balanced_linear_size_depth:balancedDepth,min_depth_anf_monomials:mono,
      min_depth_anf_and_gates:andGates,balanced_and_gates:9*(b-1),
      balanced_xor_gates:6*(b-1),strict_depth_improvement:Number(exactDepth<balancedDepth)});
  }
  assert.deepEqual(rows.filter(r=>r.strict_depth_improvement).map(r=>[r.b,r.charge]),
    [[2,1],[3,0],[5,1],[9,0]]);
  const result={label:'LSPV-3/534 exact nonlinear depth',
    scope:'Free XOR and NOT, arbitrary DAG, binary AND; unbounded circuit size; no historical R_mix341 certificate',
    configurations:rows.length,truth_inputs:truthInputs,coefficient_checks:coefficientChecks,
    hostile_mutations_rejected:hostile,
    strict_improvements:rows.filter(r=>r.strict_depth_improvement).map(r=>[r.b,r.charge]),
    rows,status:'PROVED/RESTRICTED symbolic; COMPUTATIONAL finite checks; P versus NP OPEN'};
  process.stdout.write(JSON.stringify(result,null,2)+'\n');
}
main();
