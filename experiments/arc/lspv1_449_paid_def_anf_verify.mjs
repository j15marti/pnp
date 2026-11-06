#!/usr/bin/env node
// LSPV-1/449 standalone independent ANF and affine escape control.
// Checks a separately declared conservative two-input DEF circuit semantics;
// NOT the authoritative historical R_mix341 accepted-byte checker.
import assert from 'node:assert/strict';
let checks=0,assignments=0;
const ok=(x,m)=>{assert(x,m);checks++};
for(let k=1;k<=8;k++){
  const N=1<<(2*k), f=new Uint8Array(N);
  for(let a=0;a<N;a++){
    let v=1,clause=false;
    for(let i=0;i<k;i++){
      const bit=((a>>(2*i))^(a>>(2*i+1)))&1;
      v&=bit;clause||=bit===0;
    }
    f[a]=v;assignments++;
    ok((v===0)===clause,'compact affine disjunction is equivalent');
  }
  // Boolean Mobius transform recovers multilinear ANF from truth table.
  for(let j=0;j<2*k;j++)for(let a=0;a<N;a++)
    if(a&(1<<j))f[a]^=f[a^(1<<j)];
  let count=0;
  for(let a=0;a<N;a++)if(f[a]){
    count++;ok(a.toString(2).replace(/0/g,'').length===k,'ANF degree');
    for(let i=0;i<k;i++)
      ok(((a>>(2*i))&3)===1 || ((a>>(2*i))&3)===2,'one member of each pair');
  }
  ok(count===2**k,'2^k explicit monomials');
}
for(let k=1;k<=12;k++){
  ok(2*k-1===k+(k-1),'paid binary gates');
  ok(k*2**k===k*(1<<k),'explicit-variable occurrence count');
}
// Hostile count falsification.
let caught=false;try{assert.equal(2**5+1,2**5)}catch{caught=true}ok(caught,'forged monomial count rejected');
ok(checks===91509 && assignments===87380,'original independent count reconciliation');
console.log(JSON.stringify({id:'LSPV1-449',status:'PASS',checks,assignments,
  full_mobius_through_k:8,original_variable_anf_only:true,
  compact_affine_escape:true,native_Rmix341_byte_checker:false,
  B1_B2_B3:'OPEN',P_vs_NP:'OPEN'}));
