#!/usr/bin/env node
// LSPV-3/405: independent finite semantic-support oracle and miter controls.
// Not a proof of the mathematical all-size width theorem. Node >=18; no deps.
'use strict';
const assert=require('assert');
const gates={XOR:(a,b)=>a^b,AND:(a,b)=>a&b,OR:(a,b)=>a|b,NAND:(a,b)=>1-(a&b),EQ:(a,b)=>1-(a^b)};
function check(n,G){
 if(!Number.isInteger(n)||n<1||n>12)throw Error('n');
 for(let i=0;i<G.length;i++){
  const [op,a,b]=G[i];
  if(!gates[op]||!Number.isInteger(a)||!Number.isInteger(b)||a<0||b<0||a>=n+i||b>=n+i)throw Error('gate');
 }
}
function evaluate(n,G,x){check(n,G);const w=Array.from({length:n},(_,j)=>(x>>j)&1);for(const [op,a,b] of G)w.push(gates[op](w[a],w[b]));return w[w.length-1]}
function sensitivity(n,G){let result=[];for(let i=0;i<n;i++){let yes=false;for(let x=0;x<(1<<n);x++)if(evaluate(n,G,x)!==evaluate(n,G,x^(1<<i))){yes=true;break}result.push(yes)}return result}
function miter(n,G,i){for(let x=0;x<(1<<n);x++)if(evaluate(n,G,x)!==evaluate(n,G,x^(1<<i)))return true;return false}
let checks=0;
const fixtures=[
 [2,[['XOR',0,0]],[false,false]],
 [2,[['AND',0,1],['OR',0,2]],[true,false]],
 [2,[['XOR',0,1],['XOR',2,2]],[false,false]],
 [3,[['NAND',0,0],['XOR',3,1],['AND',4,2]],[true,true,true]],
 [3,[['AND',0,1],['OR',0,1],['XOR',3,4]],[true,true,false]],
 [4,[['XOR',0,1],['XOR',2,3],['XOR',4,5]],[true,true,true,true]]
];
for(const [n,G,expect] of fixtures){assert.deepStrictEqual(sensitivity(n,G),expect);for(let i=0;i<n;i++){assert.strictEqual(miter(n,G,i),expect[i]);checks++}}
const invalid=[[0,[]],[2,[['BAD',0,1]]],[2,[['AND',0,2]]],[2,[['XOR',-1,0]]],[2,[['AND',1,3]]],[2,[['AND','0',1]]]];
for(const [n,G] of invalid){assert.throws(()=>check(n,G));checks++}
let seed=405;function rand(max){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%max}
const names=Object.keys(gates);
for(let n=2;n<=6;n++)for(let k=1;k<=6;k++)for(let run=0;run<12;run++){
 let G=[];for(let z=0;z<k;z++)G.push([names[rand(names.length)],rand(n+z),rand(n+z)]);
 const a=sensitivity(n,G);for(let i=0;i<n;i++){assert.strictEqual(miter(n,G,i),a[i]);checks++}
}
function parityModels(odd){const e=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];let total=0;
 for(let mask=0;mask<64;mask++){let charge=[0,0,0,0];for(let j=0;j<6;j++){let bit=(mask>>j)&1;charge[e[j][0]]^=bit;charge[e[j][1]]^=bit}
 if(charge.every((v,i)=>v===(odd&&i===0?1:0)))total++}return total}
assert.strictEqual(parityModels(true),0);assert.strictEqual(parityModels(false),8);checks+=2;
console.log(JSON.stringify({checks,fixtureCount:fixtures.length,randomCircuits:5*6*12,malformedRejects:invalid.length,oddK4Models:0,evenK4Models:8,status:'COMPUTATIONAL finite tests only'}));