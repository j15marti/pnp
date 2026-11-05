#!/usr/bin/env node
/* LSPV-1/411: independent exhaustive three-original-input semantic-port test.
 * Does not test the unratified original DEF facet serialization or B3.
 * Run: node experiments/arc/lspv1_411_semantic_port_8.js
 */
"use strict";
let checks=0;
function assert(x,msg){checks++;if(!x)throw Error(msg)}
function witness(mask,functions_){
  // outputs are pairs of (truth-table mask, literal polarity)
  let chosen=[];
  for(let a=0;a<8;a++)if((mask>>a)&1){
    let index=functions_.findIndex(([f,pol])=>((f>>a)&1)===pol);
    if(index<0)return null;
    chosen.push(index);
  }
  return [...new Set(chosen)];
}
let rng=411;
function next(){rng^=rng<<13;rng^=rng>>>17;rng^=rng<<5;return rng>>>0;}
let tested=0,notEntailed=0;
for(let mask=0;mask<256;mask++)for(let k=1;k<=24;k++){
  const fs=Array.from({length:k},()=>[next()&255,next()&1]);
  const w=witness(mask,fs);
  if(w===null){notEntailed++;continue;}
  assert(w.length<=Math.min(8,mask.toString(2).split("1").length-1),"row cap");
  for(let a=0;a<8;a++)if((mask>>a)&1)
    assert(w.some(i=>((fs[i][0]>>a)&1)===fs[i][1]),"semantic coverage");
  tested++;
}
// Tightness: outputs whose only true original row is a in S.
let sharp=0;
for(let mask=0;mask<256;mask++){
  const ports=Array.from({length:8},(_,a)=>[1<<a,1]);
  const picked=ports.filter((_,a)=>(mask>>a)&1);
  const selected=witness(mask,picked);
  assert(selected!==null&&selected.length===picked.length,"tight cardinality");
  for(let idx=0;idx<picked.length;idx++){
    let reduced=picked.filter((_,j)=>j!==idx);
    assert(witness(mask,reduced)===null,"each indicator indispensable");
  }
  sharp++;
}
console.log(JSON.stringify({status:"PASS",checks,entailed_cases:tested,nonentailed: notEntailed,sharp_masks:sharp,full_original_Rmix341_B3:"OPEN"},null,2));
