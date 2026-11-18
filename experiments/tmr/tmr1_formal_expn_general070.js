"use strict";
// Independent finite scope test for count-preserving arbitrary-density formal-promise normalization.
const run = function run(seed=20261117){
 let state=seed>>>0, cases=0, assertions=0, assignments=0, failures=0, maxOutput=0, maxOldClauses=0;
 function rnd(){state^=state<<13;state^=state>>>17;state^=state<<5;return state>>>0;}
 function count(n,F){let count=0;for(let a=0;a<2**n;a++){assignments++;if(F.every(C=>C.some(([i,s])=>((a>>>i)&1)===s)))count++;}return count;}
 function check(n,F,expected){const seen=new Set(),uniq=[];for(const C of F){let id=JSON.stringify(C);if(!seen.has(id)){seen.add(id);uniq.push(C)}}let used=new Set(uniq.flatMap(c=>c.map(([i])=>i)));let G=uniq.map(c=>c.map(x=>x.slice()));
 for(let i=0;i<n;i++)if(!used.has(i))G.push([[i,0],[i,1]]);
 for(let j=0;j<4;j++)G.push([[n+j,0]]);
 G.push([[n,0],[n,1]]);
 let m=G.length,np=n+4;cases++;maxOutput=Math.max(maxOutput,m);maxOldClauses=Math.max(maxOldClauses,uniq.length);
 function assert(b){assertions++;if(!b)failures++;}
 assert(np>=4);assert(m>=2);assert(G.every(c=>c.length<=3));assert(new Set(G.map(JSON.stringify)).size===m);
 assert(Array.from({length:np},(_,i)=>G.some(c=>c.some(([v])=>v===i))).every(Boolean));
 let a=count(n,F),b=count(np,G);assert(a===b);if(expected!==undefined)assert(a===expected);assert(uniq.length<=1+(2*n)+(2*n)**2+(2*n)**3);
 return {n,m0:uniq.length,np,m,oldCount:a,newCount:b};
 }
 for(let n=0;n<=5;n++){for(let j=0;j<80;j++){const F=[];const m=rnd()%28;for(let k=0;k<m;k++){if(F.length&&(rnd()%4===0)){F.push(F[rnd()%F.length].map(x=>x.slice()));continue}const C=[];let len=rnd()%4;for(let t=0;t<len;t++)if(n>0)C.push([rnd()%n,rnd()%2]);F.push(C)}check(n,F)}}
 const disj=[];for(let i=0;i<3;i++)disj.push([[2*i,0],[2*i+1,0]]);let disjCheck=check(6,disj,27);
 const dense=[];for(let a=0;a<6;a++)for(let b=0;b<6;b++)for(let c=0;c<6;c++)dense.push([[a>>>1,a%2],[b>>>1,b%2],[c>>>1,c%2]]);
 let denseCheck=check(3,dense,0);
 return {revision:"tmr1-formal-expn-general070-v1",seed,cases,assertions,assignments,failures,maxOutput,maxOldClauses,disjCheck,denseCheck,denseExceeds4n:denseCheck.m>4*denseCheck.np,pinnedSource:"anthropics/formal-math@16a5ce41304fcdaea4e0be7c132e1c361dc26da5",status:"COMPUTATIONAL finite normalizer test only; no Lean kernel run"};
};
console.log(JSON.stringify(run(),null,2));
