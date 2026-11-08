#!/usr/bin/env node
'use strict';
// LSPV-3/503: distinct R_bridge503 upper-control, NOT native R_mix341.
const graphs=[{name:'K4',n:4,e:[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]},
{name:'K33',n:6,e:Array.from({length:3},(_,i)=>Array.from({length:3},(_,j)=>[i,j+3])).flat()}];
let checks=0;function ok(p,s){checks++;if(!p)throw Error(s)}
const canon=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const eq=(a,b)=>JSON.stringify(canon(a))===JSON.stringify(canon(b));
const sat=(c,a)=>c.some(l=>l>0?a[l-1]===1:a[-l-1]===0);
function count(F,n){let r=0;for(let k=0;k<2**n;k++){const a=Array.from({length:n},(_,j)=>(k>>j)&1);if(F.every(c=>sat(c,a)))r++}return r}
function source(g,b){const v=Array.from({length:g.n},()=>[]);g.e.forEach(([i,j],e)=>{v[i].push(e+1);v[j].push(e+1)});let F=[];
for(let i=0;i<g.n;i++)for(let k=0;k<8;k++){const a=[k&1,(k>>1)&1,(k>>2)&1];if((a[0]^a[1]^a[2])!==b[i])F.push(canon(v[i].map((e,j)=>a[j]?-e:e)))}return F}
function RES(a,b,p){ok(a.includes(p)&&b.includes(-p),'invalid oriented pivot');const out=canon([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);ok(!out.some(x=>out.includes(-x)),'tautological resolvent');return out}
let records=[],bad=0;
for(const g of graphs){const E=g.e.length,F=source(g,Array.from({length:g.n},(_,i)=>i?0:1)),even=source(g,Array(g.n).fill(0));ok(F.length===4*g.n,'original count');ok(count(F,E)===0,'odd UNSAT');ok(count(even,E)===2**(E-g.n+1),'even models');
for(let j=0;j<F.length;j++){const [x,y,z]=F[j],u=E+1,v=E+2;
const A=canon([x,y,u]),B=canon([-u,z,v]),C=canon([-u,z,-v]);
const b2=RES(B,C,v),b3=RES(A,b2,u);ok(eq(b3,F[j]),'source retraction');
const G=[...F.slice(0,j),A,B,C,...F.slice(j+1)];ok(G.length===4*g.n+2,'expanded strict 3-CNF');ok(count(G,E+2)===0,'expanded UNSAT');
for(let i=0;i<G.length;i++)ok(count(G.filter((_,k)=>i!==k),E+2)>0,'every source clause is indispensable');
try{RES(B,C,u);throw Error('bad pivot accepted')}catch(e){if(e.message==='bad pivot accepted')throw e;bad++}
ok(!eq(b2,b3),'wrong intermediate must not be confused with original source');bad++;
records.push({graph:g.name,expandedIndex:j,sourceClauses:G.length,sourceVariables:E+2,RES:2,AND3:3*g.n,XOR:g.n-1,distinctPaidNodes:4*g.n+1})}}
const out={calculus:'distinct R_bridge503 (RES clause views as AND3 inputs)',historicalRmix341:false,cases:records.length,negativeChecks:bad,assertions:checks,records};
console.log(JSON.stringify(out,null,2));