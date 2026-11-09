'use strict';
// Independently checks Fourier orbit support separation and explicit XOR witness.
// This is not an R_mix341 proof checker.
const assert = require('assert').strict;
const fs = require('fs');
function* vectors(q,b,arr=[]) {
  if(arr.length===b) {yield arr;return;}
  for(let a=0;a<q;a++)yield* vectors(q,b,[...arr,a]);
}
function weight(v){return v.filter(x=>x!==0).length;}
let results=[], checks=0;
for(const [q,b] of [[3,2],[3,3],[3,4],[3,5],[3,6],[3,7],[5,3],[5,4],[5,5],[7,3]]){
  const d=Math.ceil(b/2), c=(b+1)%q;
  const sign=Array.from({length:b},(_,i)=>i%2===0?1:-1);
  let witnessed=0, legal=0, wrong=0;
  for(const x of vectors(q,b)){
    for(let t=1;t<q;t++) {
      const shifted=x.map(z=>(z+t)%q);
      assert(weight(x)+weight(shifted)>=b);checks++;
      assert(!(weight(x)<=d-1&&weight(shifted)<=d-1));checks++;
    }
    const a=Math.floor(b/2);
    const left=x.slice(0,a).reduce((s,v,i)=>s+sign[i]*v,0);
    const right=x.slice(a).reduce((s,v,i)=>s+sign[a+i]*v,0);
    const total=((left+right)%q+q)%q;
    const f=(Number(((left%q)+q)%q===0)^Number(((right%q)+q)%q===c));
    if(total===c){assert(f===0);legal++}else{wrong++;if(f)witnessed++}
    checks++;
  }
  assert(legal===q**(b-1));checks++;
  assert(wrong===(q-1)*q**(b-1));checks++;
  assert(witnessed>0);checks++;
  results.push({q,b,minimal_degree:d,charge:c,legal,wrong,wrong_detected:witnessed,
    monomials_in_explicit_witness:q**(Math.floor(b/2)-1)+q**(Math.ceil(b/2)-1)});
}
// q=2 deliberately violates odd-modulus lower bound: linear parity determines charge.
for(let b=4;b<=7;b++){
  for(const x of vectors(2,b)){
    const linear=x.reduce((a,z)=>a^z,0);const charge=x.reduce((a,z)=>a+z,0)%2;
    assert(linear===charge);checks++;
  }
}
const output={status:'PASS',checks,configurations:results.length,results,
  scope:'odd q; original one-hot indicators only; no auxiliaries; no historical mixed-rule claim'};
fs.writeFileSync('/mnt/data/lspv1_532_js_results.json',JSON.stringify(output,null,2));
console.log('PASS JS',checks,'checks',results.length,'configurations');
