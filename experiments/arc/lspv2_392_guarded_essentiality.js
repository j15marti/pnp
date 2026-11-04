/* LSPV-2/392 primary: exhaustive source-clause deletion on a one-RES-step UNSAT wrapper.
   Run: node experiments/arc/lspv2_392_guarded_essentiality.js
   All inputs are nonempty, non-tautological labelled source clauses. */
(function(){
"use strict";
let checks=0;function must(b,s){checks++;if(!b)throw Error(s)}
function sat(clauses,n){for(let a=0;a<2**n;a++){let ok=clauses.every(cl=>cl.some(l=>((a>>(Math.abs(l)-1))&1)==(l>0?1:0)));if(ok)return true}return false}
function Hfrom(U,k){return U.filter((_,i)=>((k>>>i)&1)!==0).map(c=>c.slice())}
function wrap(H,n){let t=n+1;return [[t],[-t],...H.map(c=>[-t,...c])]}
function essential(F,n){let out=[];for(let i=0;i<F.length;i++)if(sat(F.filter((_,j)=>i!==j),n))out.push(i);return out}
function validClause(c,n){return Array.isArray(c)&&c.length>0&&c.every(x=>Number.isInteger(x)&&x!==0&&Math.abs(x)<=n)&&new Set(c).size===c.length&&!c.some(x=>c.includes(-x))}
function verify(F,n){if(!Array.isArray(F)||F.length<2||!F.every(c=>validClause(c,n)))return false;return F[0].length===1&&F[1].length===1&&F[0][0]===-F[1][0]}
// Two-original-variable universe, exhaustive all 2^8 nonempty clause subsets.
const U2=[[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]];
let u2={sat:0,unsat:0,one:0,two:0};
for(let k=0;k<256;k++){let H=Hfrom(U2,k),b=sat(H,2),F=wrap(H,2),E=essential(F,3);must(!sat(F,3),"wrapper unexpectedly SAT "+k);must(verify(F,3),"invalid units "+k);must(E.length===1+Number(b),"essential count "+k);must(E[0]===0,"first unit "+k);must(E.includes(1)===b,"second unit "+k);must(E.every(i=>i<2),"guard essential "+k);u2[b?"sat":"unsat"]++;u2[E.length===1?"one":"two"]++}
const U3=[];for(let mask=1;mask<8;mask++){let vars=[1,2,3].filter((v,i)=>mask&(1<<i));for(let signs=0;signs<(1<<vars.length);signs++)U3.push(vars.map((v,j)=>(signs&(1<<j))?-v:v))}
let seed=123456789,u3={sat:0,unsat:0};
for(let k=0;k<1024;k++){seed=(Math.imul(seed,1664525)+1013904223)>>>0;let H=Hfrom(U3,seed),b=sat(H,3),F=wrap(H,3),E=essential(F,4);must(!sat(F,4),"3var wrapper SAT "+k);must(E.length===1+Number(b),"3var essential count "+k);must(E[0]===0,"3var unit 0 "+k);must(E.includes(1)===b,"3var unit 1 "+k);must(E.every(i=>i<2),"3var guard essential "+k);u3[b?"sat":"unsat"]++}
// Both labels and syntactic/malformed/corrupt-parent fixtures.
must(essential(wrap([[1]],1),2).length===2,"SAT control");
must(essential(wrap([[1],[-1]],1),2).length===1,"UNSAT control");
must(!sat([[1],[-1]],1),"one-step proof source control");
for(const bad of [[],[[1]],[[1],[-2]],[[1],[-1],[0]],[[1],[-1],[2,-2]],[[1],[-1],[]],[[1],[-1],[1,1]],[[1],[-1],["x"]]])must(!verify(bad,2),"invalid input accepted");
const data={label:"LSPV2_392",model:"strict RES subcalculus of unchanged R_mix341",exact_formula:"E(F_H)=1+[SAT(H)], W_Rmix341(F_H)=1 under unit-paid inference convention",two_var_exhaustive:256,two_var:u2,three_var_sample:1024,three_var:u3,seed_init:123456789,assertions:checks,malformed_rejected:8};
if(typeof console!=="undefined")console.log(JSON.stringify(data));return data;
})()
