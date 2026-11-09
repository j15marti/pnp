'use strict';
// LSPV-3/533 independent exact finite verifier. This is NOT an R_mix341 proof checker.
const assert=require('assert');
function onehot(t){return [+(t===0),+(t===1),+(t===2)];}
function merge(A,B){return [0,1,2].map(k=>[0,1,2].reduce((z,i)=>z^(A[i]&B[(k+3-i)%3]),0));}
function evaluate(a){let q=a.map(onehot),depth=0;
 while(q.length>1){let next=[];for(let i=0;i<q.length;i+=2)next.push(i+1<q.length?merge(q[i],q[i+1]):q[i]);
 q=next;depth++;}return [q[0],depth];}
const popcnt=n=>{let w=0;for(;n;n&=n-1)w++;return w;};
let checks=0, inputs=0, cases=0;
for(let b=2;b<=12;b++)for(let c=0;c<3;c++){
 const n=1<<b,f=Array.from({length:n},(_,m)=>+(popcnt(m)%3===c));
 for(let bit=0;bit<b;bit++)for(let m=0;m<n;m++)if(m&(1<<bit))f[m]^=f[m^(1<<bit)];
 let deg=-1;for(let m=0;m<n;m++)if(f[m])deg=Math.max(deg,popcnt(m));
 const expected=b-+((b+c)%3===0);assert.strictEqual(deg,expected);checks++;
 for(let m=0;m<n;m++){const x=Array.from({length:b},(_,i)=>(m>>i)&1),[v,d]=evaluate(x);
 assert.deepStrictEqual(v,onehot(popcnt(m)%3));assert.strictEqual(d,Math.ceil(Math.log2(b)));
 checks+=2;inputs++;}
 cases++;
}
assert.notDeepStrictEqual(merge(onehot(0),onehot(0)),[0,0,0]);checks++;
console.log(JSON.stringify({cases,inputs,checks,description:'COMPUTATIONAL finite consistency only, NOT historical Rmix proof'}));