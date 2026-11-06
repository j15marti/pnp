#!/usr/bin/env node
'use strict';
// LSPV-1/454 independent, stdlib-only exact integer and existential chain verifier.
// Applies Braun only to ORIGINAL BPHP, not the different strict-3 source.
// This is NOT the authoritative historical R_mix341 checker.
const assert=require('node:assert/strict');
let checks=0; const ck=(v,msg)=>{assert.ok(v,msg);checks++};
function counts(ell){
  const n=1n<<BigInt(ell),m=n+1n,L=BigInt(ell);
  const A=n*m*(m-1n)/2n;
  const S=A*(2n*L-2n),V=m*L+A*(2n*L-3n);
  const base=A*(4n*L-3n)+m*(2n*n*L-9n);
  const num=n*m*(27n*n*n+11n*n-14n);
  ck(num%24n===0n,'Cook exact node count must be integral');
  const Q=base+num/24n;
  ck(Q>0n);
  return {n,m,A,S,V,Q};
}
function chain(ell){
  const L=2*ell,K=L-3;
  const lits=Array.from({length:L},(_,i)=>i%2===0?i+1:-(i+1));
  const clauses=[[lits[0],lits[1],L+1]];
  for(let i=1;i<=K-1;i++)clauses.push([-(L+i),lits[i+1],L+i+1]);
  clauses.push([-(L+K),lits[L-2],lits[L-1]]);
  ck(clauses.length===L-2);
  ck(clauses.every(c=>c.length===3&&new Set(c.map(x=>Math.abs(x))).size===3));
  for(let x=0;x<2**L;x++){
    const orig=lits.some(l=>Boolean((x>>(Math.abs(l)-1))&1)===(l>0));
    let exists=false;
    for(let y=0;y<2**K;y++){
      const val=v=>v<=L?Boolean((x>>(v-1))&1):Boolean((y>>(v-L-1))&1);
      if(clauses.every(c=>c.some(l=>val(Math.abs(l))===(l>0)))){exists=true;break}
    }
    ck(orig===exists,'equisatisfiability for original bit assignment '+x);
  }
}
for(let ell=2;ell<=4;ell++)chain(ell);
ck(counts(2).S===80n);
ck(counts(3).S===1152n);
ck(counts(2).Q===620n);
ck(counts(3).Q===8349n);
ck(counts(2).Q!==495n); // a different finite FACET proof, do not conflate
for(const ell of [32,33,34,40,50]){
  const {n,Q,S}=counts(ell);
  ck(Q<=2n*n**4n);
  ck(Q+S<=3n*n**4n);
  // Count the output lines, NOT the cost of discovering them.
  const logBraun=Number(n)/(32768*ell*ell);
  ck(logBraun>Math.log(Number(Q+S)));
}
console.log(JSON.stringify({tag:'LSPV1_454',assertions:checks,passed:true,
 braun_model:'original bit PHP Res(XOR), ell>=32',
 upper_model:'separate FACET-A, not historic R_mix341',
 accepted_native_bytes:false}));
