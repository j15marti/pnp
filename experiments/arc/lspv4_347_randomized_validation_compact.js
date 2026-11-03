#!/usr/bin/env node
// LSPV-4 347. Exact SAT/UNSAT source-sign and randomized certificate-query check.
// Self-contained, dependency-free. This is a MODEL-SPECIFIC sensitivity check,
// not an Rmix341 inference rule or an arbitrary SAT-time lower bound.
'use strict';
function horn(m) {
  const c=[[1]];
  for(let i=1;i<m-1;i++) c.push([-i,i+1]);
  c.push([-(m-1)]);
  return [c,m-1];
}
function k4(odd) {
  const edges=[];
  for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)edges.push([a,b]);
  const c=[];
  for(let v=0;v<4;v++){
    const inc=edges.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);
    for(let a=0;a<8;a++){
      const bits=[(a>>2)&1,(a>>1)&1,a&1];
      if((bits[0]^bits[1]^bits[2])!==(odd&&v===0?1:0))
        c.push(inc.map((x,j)=>bits[j]?-x:x));
    }
  }
  return [c,6];
}
function models(c,n) {
  let count=0;
  for(let a=0;a<2**n;a++){
    if(c.every(cl=>cl.some(l=>Boolean(a&(2**(Math.abs(l)-1)))===(l>0))))count++;
  }
  return count;
}
function flip(c,j,k){
  return c.map((cl,i)=>cl.map((l,t)=>(i===j&&t===k)?-l:l));
}
const result=[];
for(let m=2;m<=10;m++){
  const [c,n]=horn(m),L=c.reduce((a,cl)=>a+cl.length,0);
  if(models(c,n)!==0)throw Error('Horn not UNSAT');
  let positive=0;
  for(let j=0;j<c.length;j++)for(let k=0;k<c[j].length;k++)
    if(models(flip(c,j,k),n)>0)positive++;
  if(positive!==L)throw Error('failed sign sensitivity');
  result.push({source:'Horn'+m,n,m,L,sat_sign_flip_neighbors:positive,
    expected_randomized_sign_queries:L/3});
}
let [odd,n]=k4(true),[even]=k4(false);
const L=odd.reduce((a,cl)=>a+cl.length,0);
if(models(odd,n)!==0||models(even,n)!==8)throw Error('parity labels');
let positive=0;
for(let j=0;j<odd.length;j++)for(let k=0;k<odd[j].length;k++)
  if(models(flip(odd,j,k),n)>0)positive++;
if(positive!==L)throw Error('parity sensitivity');
result.push({source:'K4_odd',n,m:odd.length,L,sat_sign_flip_neighbors:positive,
  expected_randomized_sign_queries:L/3});
const total=result.reduce((a,x)=>a+x.L,0);
if(total!==138)throw Error('wrong total');
console.log(JSON.stringify({verified:true,UNSAT_sources:result.length,
  SAT_single_sign_neighbors:total,even_K4_models:8,
  proof_rule_added_to_Rmix341:false,B3:'OPEN',cases:result},null,2));