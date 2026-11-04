#!/usr/bin/env node
// LSPV4/372: no-import, deterministic, independently regenerated K4/XOR controls.
// Restricted affine-DAG validator, NOT a general-SAT solver or Rmix341 checker.
"use strict";
const assert=require("assert");
let checks=0, rejected=0;
function ok(cond,msg){assert(cond,msg);checks++}
const edges=[];
for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)edges.push([a,b]);
function parseCharge(s){if(typeof s!=="string"||!/^[01]{4}$/.test(s))throw Error("malformed charge");return s.split("").map(Number)}
function source(z){
  const out=[];
  for(let v=0;v<4;v++){
    const ids=edges.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);
    for(let a=0;a<8;a++){
      const parity=((a&1)+((a>>1)&1)+((a>>2)&1))&1;
      if(parity!==z[v])out.push(ids.map((id,k)=>(a&(1<<k))?-id:id));
    }
  }
  return out;
}
function models(cs){
  let count=0;
  for(let a=0;a<64;a++)if(cs.every(c=>c.some(l=>{
    const b=(a>>(Math.abs(l)-1))&1;
    return l>0?b:!b;
  })))count++;
  return count;
}
function rows(z){return z.map((charge,v)=>{
  let mask=0;
  edges.forEach((e,i)=>{if(e.includes(v))mask|=(1<<i)});
  return [mask,charge];
})}
function xor(x,y){return [x[0]^y[0],x[1]^y[1]]}
function fib(q){let a=1n,b=1n;for(let i=2;i<=q;i++){let c=a+b;a=b;b=c}return q?b:a}
function verify(q,charges){
  let initial=rows(charges),a=initial[0],b=initial[1];
  for(let i=2;i<=q;i++){const n=xor(a,b);a=b;b=n;}
  if(q%3===0)ok(b[0]===initial[0][0]&&b[1]===initial[0][1],"GF2 period");
  for(let v=1;v<4;v++)b=xor(b,initial[v]);
  ok(b[0]===0&&b[1]===charges.reduce((x,y)=>x^y,0),"sum root");
  return {nodes:q+14,walks:fib(q).toString(),xor_bit_work:7*(q+2),root:b};
}
const odd=parseCharge("1000"),even=parseCharge("0000");
const C=source(odd),E=source(even);
ok(C.length===16&&E.length===16,"source cardinality");
ok(models(C)===0&&models(E)===8,"labels");
let outputs=[];
for(let q of [3,6,9,12,18,24,30,36,48,60]){
  let u=verify(q,odd),v=verify(q,even);
  ok(u.root[1]===1&&v.root[1]===0,"opposite label");
  outputs.push({q,nodes:u.nodes,walks:u.walks,xor_bit_work:u.xor_bit_work});
}
for(let i=0;i<16;i++){
  ok(models(C.filter((_,j)=>j!==i))>0,"deletion SAT");
  for(let j=0;j<3;j++){
    let copy=C.map(c=>c.slice());copy[i][j]*=-1;
    ok(models(copy)>0,"single-sign-flip SAT");
  }
}
for(let invalid of ["","0","0X00","00000",4,null,{}]){
  try{parseCharge(invalid);throw Error("accepted malformed");}
  catch(e){if(e.message==="accepted malformed")throw e;rejected++}
}
const evidence={run:"SHARED-XOR-PATH-MULTIPLICITY372",model:"K4 signed parity, explicit binary XOR DAG",checks,rejected,odd_models:models(C),even_models:models(E),cases:outputs};
console.log(JSON.stringify(evidence,null,2));