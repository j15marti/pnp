#!/usr/bin/env node
/* LSPV-2/382. Self-contained semantic and size-ledger reproducer.
 * Full source-authenticated producer and independent trace checker are in the
 * companion reproducibility ZIP. This script does NOT prove that auxiliary-
 * named AND3 steps are legal in original-only R_mix341.
 */
'use strict';
const assert=require('node:assert/strict');
let checks=0;function ok(x,msg){assert.ok(x,msg);checks++;}
const K4=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)K4.push([i,j]);
const K33=[];for(let i=0;i<3;i++)for(let j=3;j<6;j++)K33.push([i,j]);
const Cube=[];for(let i=0;i<8;i++)for(let b=0;b<3;b++){const j=i^(1<<b);if(i<j)Cube.push([i,j]);}
const Petersen=[];for(let i=0;i<5;i++)Petersen.push([i,(i+1)%5],[i+5,5+(i+2)%5],[i,i+5]);
const graphs=[['K4',4,K4,[1,0,0,0]],['K33',6,K33,[1,0,0,0,0,0]],['CUBE',8,Cube,[1,0,0,0,0,0,0,0]],['PETERSEN',10,Petersen,[1,0,0,0,0,0,0,0,0,0]],['K4_CHARGE3',4,K4,[1,1,1,0]]];
function checkLocal(c){for(let t=0;t<2;t++)for(let mask=0;mask<8;mask++){
 const x=[mask&1,(mask>>1)&1,(mask>>2)&1],y=x.map(v=>t&v),p=y[0]^y[1];
 let guarded=true;
 for(let pat=0;pat<8;pat++){const a=[pat&1,(pat>>1)&1,(pat>>2)&1];
  if((a[0]^a[1]^a[2])!==c&&t===1&&x.every((v,i)=>v===a[i]))guarded=false;}
 if(guarded)ok((p^y[2]^(c&t))===0,'guarded port row');
 ok((p^y[0]^y[1])===0,'gate identity');
}}
function fixture([name,h,edges,charges]){
 const inc=Array.from({length:h},()=>[]);
 for(let e=0;e<edges.length;e++){const[a,b]=edges[e];ok(a!==b&&a>=0&&b>=0&&a<h&&b<h,'edge');inc[a].push(e);inc[b].push(e);}
 ok(inc.every(x=>x.length===3),'cubic');ok(2*edges.length===3*h,'edge count');
 const r=charges.reduce((a,b)=>a+b,0);ok(r%2===1,'odd');
 checkLocal(0);checkLocal(1);
 const even=charges.slice();even[0]^=1;let oddSat=0,evenSat=0;
 for(let bits=0;bits<2**edges.length;bits++){
  const x=e=>(bits>>e)&1;
  let odd=true,evenModel=true,sOdd=0,sEven=0;
  for(let v=0;v<h;v++){
    const[a,b,c]=inc[v],par=x(a)^x(b)^x(c);
    if(par!==charges[v])odd=false;if(par!==even[v])evenModel=false;
    const ya=x(a),yb=x(b),yc=x(c),p=ya^yb;
    sOdd^=p^yc^charges[v];sOdd^=p^ya^yb;
    sEven^=p^yc^even[v];sEven^=p^ya^yb;
  }
  ok(sOdd===1,'odd signed summation');ok(sEven===0,'even signed summation');
  if(odd)oddSat++;if(evenModel)evenSat++;
 }
 ok(oddSat===0,'odd unguarded must be UNSAT');
 ok(evenSat>0,'even unguarded must be SAT');
 const cost={SOURCE:4*h,DEF:5*h/2,RES:23*h-2*r,CONVERT:1+2*r,AND3:4*h+2*r,XOR:2*h-1};
 const q=Object.entries(cost).filter(([k])=>k!=='SOURCE').reduce((s,[,v])=>s+v,0);
 ok(q===63*h/2+2*r,'count of all paid nodes');
 return {name,vertices:h,edges:edges.length,positiveCharges:r,paidNodes:q,cost,guard0SAT:true,guard1UNSAT:true,evenGuard1SAT:true};
}
const results=graphs.map(fixture);
console.log(JSON.stringify({schema:'LSPV2/382-public/v1',scope:'auxiliary-named-wire X3 only, full literal R_mix341 translation remains open',checks,results},null,2));