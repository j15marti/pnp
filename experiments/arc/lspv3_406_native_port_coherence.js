#!/usr/bin/env node
// LSPV-3/406. Complete independent minimal witness checker, node >= 18.
// Restricted paid signed-AND2 circuit grammar only, NOT full R_mix341 checker.
'use strict';
const assert=require('node:assert/strict'); let tests=0;
function ok(v,name){assert.ok(v,name);tests++;}
function f(x,y,z){return z===(x&y);}
function g(x,y,z){return z===((1-x)&y);}
for(let x=0;x<2;x++)for(let y=0;y<2;y++){
  let nf=0,ng=0;for(let z=0;z<2;z++){if(f(x,y,z))nf++;if(g(x,y,z))ng++;}
  ok(nf===1&&ng===1,"each gate individually a total conservative extension");
}
ok(![0,1].some(z=>f(1,1,z)&&g(1,1,z)),"same exported z has no model");
ok([0,1].some(z=>f(1,1,z))&&[0,1].some(w=>g(1,1,w)),"fresh distinct z,w model");
function evaluate(xs){let acc=xs[0];for(let i=1;i<xs.length;i++)acc&=xs[i];return acc;}
for(let n=2;n<=11;n++){
 for(let mask=0;mask<(1<<n);mask++){
   let xs=Array.from({length:n},(_,i)=>(mask>>i)&1);
   ok(evaluate(xs)===Number(xs.every(Boolean)),"and chain truth table");
 }
 let all=Array(n).fill(1);
 for(let i=0;i<n;i++){let a=all.slice();a[i]=0;ok(evaluate(a)===0,"essential variable");}
}
console.log(JSON.stringify({version:"LSPV3-406-PORT-COHERENCE-MINIMAL/v1",checks:tests,
model_bijection:"checked finite",alias_join_UNSAT:true,fresh_join_SAT:true,
native_export_grammar:"OPEN",B3:"OPEN"},null,2));
