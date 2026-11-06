'use strict';
// Standalone source-authenticated Braun bit-PHP clause-chain ER bridge control.
// NOT a historical R_mix341 accepted-byte checker.
const assert=require('node:assert/strict');
let checks=0;
function eq(a,b){checks++;assert.deepEqual(a,b)}
function norm(a){let s=[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||(x<0)-(y<0));eq(s.some(x=>s.includes(-x)),false);return s}
function res(a,b,p){eq(a.includes(p),true);eq(b.includes(-p),true);return norm([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)])}
function wide(ell,m){let a=[];for(let i=0;i<m;i++)for(let j=i+1;j<m;j++)for(let h=0;h<2**ell;h++){let c=[];for(let p of [i,j])for(let t=0;t<ell;t++){let v=p*ell+t+1;c.push((h>>t)&1?-v:v)}a.push(norm(c))}return a}
function check(ell,m){let F=wide(ell,m),t=2*ell-3,fw=0,bw=0,def=0;
for(let idx=0;idx<F.length;idx++){
 let C=F[idx],base=m*ell+idx*t+1, gates=[];
 for(let j=0;j<t;j++){
  let y=base+j,u=j===0?-C[0]:base+j-1,v=j===0?-C[1]:-C[j+1];
  gates.push([norm([-y,u]),norm([-y,v]),norm([y,-u,-v])]);def++;
 }
 let split=[norm([C[0],C[1],base])];
 for(let j=1;j<t;j++)split.push(norm([-base-j+1,C[j+1],base+j]));
 split.push(norm([-base-t+1,C.at(-2),C.at(-1)]));
 let r=split[0];for(let j=0;j<t;j++){r=res(r,split[j+1],base+j);fw++}eq(r,C);
 eq(split[0],gates[0][2]);for(let j=1;j<t;j++)eq(split[j],gates[j][2]);
 r=C;for(let j=0;j<2;j++){r=res(r,gates[0][j],C[j]);bw++}
 for(let j=1;j<t;j++){r=res(gates[j][0],r,base+j-1);r=res(r,gates[j][1],C[j+1]);bw+=2}
 eq(r,split.at(-1));
 }
 eq(fw,F.length*t);eq(bw,F.length*2*t);eq(def,F.length*t);
 return {ell,m,wide:F.length,strict3:F.length*(t+1),gates:def,forward_resolution:fw,backward_resolution:bw};
}
const cases=[check(2,5),check(2,4),check(3,9)];
assert.throws(()=>res([1,2],[-1,3],-1));
assert.throws(()=>norm([1,-1]));
console.log(JSON.stringify({status:'PASS; restricted ER gate-facet calculus, not native R_mix341',checks,cases},null,2));
