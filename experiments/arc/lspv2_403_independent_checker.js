#!/usr/bin/env node
'use strict';
// Independently tests the strict source-Resolution clause-target compiler and hypercube tightness.
const fs=require('fs');
function fail(s){throw new Error(s)}
function canonical(a){let z=[...new Set(a)].sort((x,y)=>x-y);for(let v of z){if(z.includes(-v))fail('tautology')}return z}
function eq(a,b){return JSON.stringify(a)===JSON.stringify(b)}
function evalClause(c,bits){return c.some(t=>t>0 ? !!(bits&(1<<(t-1))) : !(bits&(1<<(-t-1))))}
function semantics(src,bits){return src.every(c=>evalClause(c,bits))}
function compile(src,target,n){
 const C=canonical(target),st=src.map(c=>canonical(c)),fixed={},vC=new Set(C.map(Math.abs)),other=[];
 for(let a of C)fixed[Math.abs(a)]=a<0?1:0;
 for(let v=1;v<=n;v++)if(!vC.has(v))other.push(v);
 const cert=st.map(c=>({typ:'src',c}));
 function solve(depth,bits){
  if(depth===other.length){
   let w=cert.findIndex((record,i)=>i<st.length&&!evalClause(record.c,bits));
   if(w<0)fail('not entailed');return w;
  }
  const v=other[depth],bit=(1<<(v-1));
  let lo=solve(depth+1,bits&~bit),hi=solve(depth+1,bits|bit);
  const a=cert[lo].c,b=cert[hi].c;
  if(!a.includes(v))return lo;
  if(!b.includes(-v))return hi;
  let resolvent=canonical([...a.filter(x=>x!==v),...b.filter(x=>x!==-v)]);
  cert.push({typ:'res',a:lo,b:hi,v,c:resolvent});return cert.length-1;
 }
 let bits=0;for(let [key,value]of Object.entries(fixed)){if(value)bits|=1<<(Number(key)-1)}
 const root=solve(0,bits),num=cert.length-st.length,ub=(1<<other.length)-1;
 if(num>ub)fail('upper bound failed');if(!cert[root].c.every(x=>C.includes(x)))fail('root not subclause');
 for(let i=st.length;i<cert.length;i++){
  const rec=cert[i];if(rec.typ!=='res'||rec.a>=i||rec.b>=i)fail('bad index');
  const a=cert[rec.a].c,b=cert[rec.b].c;
  if(!a.includes(rec.v)||!b.includes(-rec.v))fail('bad pivot');
  if(!eq(rec.c,canonical([...a.filter(x=>x!==rec.v),...b.filter(x=>x!==-rec.v)])))fail('bad resolvent');
 }
 return {num,ub,root,cert};
}
const universe=[[-2],[-1],[1],[2],[-2,-1],[-2,1],[-1,2],[1,2]];
const targets=[[],[-1],[1],[-2],[2],[-1,-2],[-1,2],[1,-2],[1,2]];
let checked=0,derived=0;
for(let mask=0;mask<256;mask++){
 const source=universe.filter((c,i)=>!!(mask&(1<<i)));
 for(let goal of targets){
  const entails=[0,1,2,3].every(bits=>!semantics(source,bits)||evalClause(goal,bits));
  if(!entails)continue;
  let r=compile(source,goal,2);checked++;derived+=r.num;
 }
}
let hyper=[];
for(let d=1;d<=6;d++){
 let source=[];
 for(let x=0;x<(1<<d);x++){
  let clause=[1];for(let j=0;j<d;j++)clause.push((x&(1<<j))?-(j+2):(j+2));
  source.push(clause);
 }
 let r=compile(source,[1],d+1);
 if(r.num!==(1<<d)-1)fail('non-tight')
 const F=[...source,[-1]];
 if(Array.from({length:1<<(d+1)},(_,bits)=>semantics(F,bits)).some(Boolean))fail('UNSAT failed');
 for(let omitted=0;omitted<F.length;omitted++){
  let sub=F.filter((_,i)=>i!==omitted);
  if(!Array.from({length:1<<(d+1)},(_,bits)=>semantics(sub,bits)).some(Boolean))fail('essentiality failed');
 }
 hyper.push({d,paidMin:1<<d,proofNodes:r.num});
}
const report={status:'COMPUTATIONAL',checkedEntailmentCases:checked,derivedResolutionNodes:derived,hypercube:hyper};
fs.writeFileSync('lspv2_403_independent_raw.json',JSON.stringify(report,null,2));
console.log(JSON.stringify(report,null,2));
