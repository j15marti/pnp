'use strict';
// LSPV-4/380: independently reproducible finite PHP vs Horn selector profiles.
const assert=require('node:assert/strict');
let checks=0;
function php(h) {let C=[];const x=(p,j)=>p*h+j+1;
 for(let p=0;p<=h;p++)C.push(Array.from({length:h},(_,j)=>x(p,j)));
 for(let j=0;j<h;j++)for(let p=0;p<=h;p++)for(let q=p+1;q<=h;q++)C.push([-x(p,j),-x(q,j)]);
 return {n:h*(h+1),C};}
function horn(m) {let C=[[1]];for(let i=1;i<m-1;i++)C.push([-i,i+1]);C.push([-(m-1)]);return {n:m-1,C};}
function val(C,a) {return C.every(cl=>cl.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0)));}
function sat(B) {for(let a=0;a<2**B.n;a++)if(val(B.C,a))return true;return false;}
function subs(B,mask) {return {n:B.n,C:B.C.filter((c,j)=>(mask & (1<<j))!==0)};}
const results=[];
for(const h of [1,2,3]) {
 let P=php(h),H=horn(P.C.length),m=P.C.length;
 assert.equal(sat(P),false);assert.equal(sat(H),false);checks+=2;
 for(let j=0;j<m;j++) {
  assert.equal(sat({n:P.n,C:P.C.filter((_,k)=>k!==j)}),true);checks++;
  if(m<=9){assert.equal(sat({n:H.n,C:H.C.filter((_,k)=>k!==j)}),true);checks++;}
 }
 const masks=m<=9?Array.from({length:2**m},(_,i)=>i):[0,(2**m)-1,1,2,3,5,17,131,701,1023];
 for(const mask of masks) {
  const expected=mask!==(2**m)-1;
  assert.equal(sat(subs(P,mask)),expected);checks++;
  if(m<=9){assert.equal(sat(subs(H,mask)),expected);checks++;}
 }
 results.push({h,clauses:m,selector_cases:masks.length,passed:checks});
}
function grammar(n,C){return Number.isInteger(n)&&n>0&&Array.isArray(C)&&C.every(c=>Array.isArray(c)&&c.length>0&&c.every(x=>Number.isInteger(x)&&x!==0&&Math.abs(x)<=n)&&new Set(c).size===c.length&&!c.some(x=>c.includes(-x)));}
for(const bad of [[0,[[1]]],[2,[[0]]],[2,[[3]]],[2,[[1,-1]]],[2,[[]]],[2,[[1,1]]]]) {assert.equal(grammar(...bad),false);checks++;}
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
let parity=[];
for(let charge=0;charge<2;charge++) {let modelcount=0;
 for(let mask=0;mask<64;mask++) {
  let ok=true;for(let v=0;v<4;v++) {let z=0;for(let e=0;e<6;e++)if(edges[e].includes(v))z^=(mask>>e)&1;if(z!==(v===0?charge:0))ok=false;}
  if(ok)modelcount++;
 }
 assert.equal(modelcount,charge?0:8);checks++;parity.push(modelcount);
}
console.log(JSON.stringify({run:'LSPV4_SELECTOR_PHP_HORN_ISOPROFILE380',verifier:'independent Node',checked:checks,results,malformed_rejections:6,even_odd_K4:parity,scope:'COMPUTATIONAL; theorem follows from symbolic proof; no Rmix341 lower bound or B3'},null,2));
