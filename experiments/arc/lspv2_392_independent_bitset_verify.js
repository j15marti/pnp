/* LSPV-2/392 independent bitset reconstruction, no primary solver imports.
Node: node experiments/arc/lspv2_392_independent_bitset_verify.js */
(function(){
"use strict";
let checks=0;function ok(x,m){checks++;if(!x)throw Error(m)}
function clauseMask(c,n){let a=0;for(let v=0;v<(1<<n);v++){for(let l of c){let q=(v>>>(Math.abs(l)-1))&1;if(q===(l>0?1:0)){a|=(1<<v);break}}}return a}
function cnfMask(C,n){let b=(1<<(1<<n))-1;for(let c of C)b&=clauseMask(c,n);return b}
function essential(C,n){let E=[];for(let i=0;i<C.length;i++){let b=(1<<(1<<n))-1;for(let j=0;j<C.length;j++)if(i!==j)b&=clauseMask(C[j],n);if(b)E.push(i)}return E}
function library(n){let U=[];for(let mask=1;mask<(1<<n);mask++){let vs=[];for(let v=1;v<=n;v++)if(mask&(1<<(v-1)))vs.push(v);for(let signs=0;signs<(1<<vs.length);signs++)U.push(vs.map((v,i)=>signs&(1<<i)?-v:v))}return U}
function sample(U,bits){return U.filter((_,j)=>bits>>>j&1)}
function wrap(H,n){return [[n+1],[-(n+1)],...H.map(c=>[-(n+1),...c])]}
function resolve(p,q,v){if(!p.includes(v)||!q.includes(-v))throw Error("wrong pivot");return [...new Set(p.filter(x=>Math.abs(x)!==v).concat(q.filter(x=>Math.abs(x)!==v)))]}
let counts={two:{sat:0,unsat:0,essential_1:0,essential_2:0},three:{sat:0,unsat:0,essential_1:0,essential_2:0}};
for(let n of [2,3]){let U=library(n),seed=123456789;let runs=n===2?256:1024;for(let k=0;k<runs;k++){
let bits=n===2?k:(seed=(Math.imul(seed,1664525)+1013904223)>>>0);
let H=sample(U,bits),F=wrap(H,n),E=essential(F,n+1),satH=cnfMask(H,n)!==0,stats=counts[n===2?"two":"three"];
ok(cnfMask(F,n+1)===0,"source SAT "+n+" "+k);
ok(resolve(F[0],F[1],n+1).length===0,"RES rule "+n+" "+k);
ok(E.length===1+Number(satH),"E count "+n+" "+k+" got "+E);
ok(E[0]===0,"unit1 "+n+" "+k);
ok(E.includes(1)===satH,"unit2 "+n+" "+k);
ok(E.every(i=>i<2),"guard indispensable "+n+" "+k);
stats[satH?"sat":"unsat"]++;
stats["essential_"+E.length]++;
}}
let data={name:"LSPV2_392 independent bitsets",two_var_exhaustive:256,three_var_sample:1024,counts,assertions:checks,proof_validation:"RES(t,not_t)=empty"};
if(typeof console!=="undefined")console.log(JSON.stringify(data));return data;
})()
