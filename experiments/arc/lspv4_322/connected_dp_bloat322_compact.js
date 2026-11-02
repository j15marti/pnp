#!/usr/bin/env node
'use strict';
// LSPV-4 CONNECTED-DP-LITERAL-BLOAT322 compact self-contained reproduction.
// Only explicit canonical input and original-clause truth are authoritative.
// Not a native FLMV machine simulator. No external packages.
const assert=require('node:assert/strict');
const p=[[1,2,3],[4,5,6],[7,8,9],[10,11,12],
         [1,4,5],[2,7,10],[3,8,11],[6,9,12]];
const n=[[1,6,7],[2,4,8],[3,5,9],[10,11,12],
         [1,8,9],[2,5,12],[3,6,10],[4,7,11]];
const B=p.concat(n.map(c=>c.map(v=>-v)));
const F9=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9],
          [-4,-6,-8],[-1,-6,-7],[-2,-3,-4],[-3,-5,-8],[-1,-2,-9],[-5,-7,-9]];
const Y6=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],
          [-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]];
const F15=[[1,2,7],[1,3,8],[4,5,9],[4,6,10],[2,3,5],[6,11,12],
           [7,11,13],[8,12,14],[9,13,15],[10,14,15],
           [-1,-2,-11],[-2,-3,-11],[-1,-3,-12],[-4,-5,-13],
           [-5,-6,-14],[-4,-6,-15],[-7,-8,-12],[-8,-9,-13],
           [-9,-10,-14],[-10,-7,-15]];
function family(t){
 const rows=[];
 for(let k=0;k<t;k++)for(const c of B)
  rows.push(c.map(v=>Math.sign(v)*(t>1&&c[0]===10&&c[1]===11&&c[2]===12&&v===10
    ?12*((k+1)%t)+10:12*k+Math.abs(v))));
 return rows;
}
function grammar(rows,N){
 if(rows.length*3!==4*N)return false;
 const cnt=new Map(), seen=new Set();
 for(const c of rows){
  if(c.length!==3||new Set(c.map(Math.abs)).size!==3||
      !(c.every(v=>v>0)||c.every(v=>v<0))||
      c.some(v=>!Number.isInteger(v)||Math.abs(v)<1||Math.abs(v)>N))return false;
  const id=(c[0]>0?'P':'N')+':'+c.map(Math.abs).sort((a,b)=>a-b).join(',');
  if(seen.has(id))return false;
  seen.add(id);
  for(const v of c){
   const id=Math.abs(v)+':'+Math.sign(v);cnt.set(id,(cnt.get(id)||0)+1);
  }
 }
 for(let v=1;v<=N;v++)for(const sign of [-1,1])
  if(cnt.get(v+':'+sign)!==2)return false;
 return true;
}
function connected(rows,N){
 const adj=Array.from({length:N+1},()=>new Set());
 for(const c of rows)for(const a of c)for(const b of c)
  adj[Math.abs(a)].add(Math.abs(b));
 const seen=new Set([1]),queue=[1];
 while(queue.length){
  const v=queue.pop();
  for(const u of adj[v])if(!seen.has(u)){seen.add(u);queue.push(u);}
 }
 return seen.size===N;
}
function eliminate(rows,v){
 const plus=rows.filter(c=>c.includes(v)),minus=rows.filter(c=>c.includes(-v));
 const keep=rows.filter(c=>!c.includes(v)&&!c.includes(-v));
 const added=[],keys=new Set(keep.map(c=>c.slice().sort((a,b)=>a-b).join(',')));
 for(const a of plus)for(const b of minus){
  const c=a.filter(x=>x!==v).concat(b.filter(x=>x!==-v));
  if(c.some(x=>c.includes(-x)))continue;
  const key=c.slice().sort((a,b)=>a-b).join(',');
  if(!keys.has(key)){keys.add(key);added.push(c);}
 }
 return {rows:keep.concat(added),removed:plus.length+minus.length,added};
}
const g=x=>2*Math.floor(Math.log2(x))+1;
const bits=(rows,N)=>g(N)+g(rows.length)+2*rows.length+
    rows.reduce((s,c)=>s+c.length*(1+Math.ceil(Math.log2(N+1))),0);
function truth(v,a){return Boolean(a&(1<<(Math.abs(v)-1)))===(v>0);}
function sat(rows,a){return rows.every(c=>c.some(v=>truth(v,a)));}
function count(rows,N,pin={}){
 let k=0,proof=[];
 for(let a=0;a<2**N;a++){
  if(Object.entries(pin).some(([v,z])=>Number(Boolean(a&(1<<(Number(v)-1))))!==z))continue;
  const falseId=rows.findIndex(c=>!c.some(v=>truth(v,a)));
  if(falseId<0)k++;else proof.push(falseId);
 }
 return {models:k,leafCount:proof.length};
}
const result={family:[],controls:{}};
for(const t of [1,2,3,4,8,16]){
 let rows=family(t),N=12*t;
 assert(grammar(rows,N)&&connected(rows,N));
 const initial=bits(rows,N);
 for(let i=0;i<t;i++){
  const out=eliminate(rows,12*i+1);
  assert.equal(out.removed,4);
  assert.equal(out.added.length,4);
  assert(out.added.every(c=>c.length===4));
  rows=out.rows;
 }
 assert.equal(rows.length,16*t);
 assert.equal(rows.reduce((s,c)=>s+c.length,0),52*t);
 const final=bits(rows,N),delta=4*t*(1+Math.ceil(Math.log2(N+1)));
 assert.equal(final-initial,delta);
 result.family.push({t,inputBits:initial,childBits:final,delta});
}
let child=eliminate(B,1).rows;
for(let a=0;a<2048;a++)assert.equal(sat(child,a*2),sat(B,a*2)||sat(B,a*2+1));
for(const [name,F,N,S,U,expected] of [
 ['B12',B,12,{4:1,5:0,7:1},{4:0,5:0,7:1},[203,35,0]],
 ['F9',F9,9,{1:0,3:0,5:1,6:0,7:0,8:0},{1:1,3:0,5:1,6:0,7:0,8:0},[70,2,0]],
 ['Y6',Y6,6,{1:0,2:0,3:1,4:0},{1:1,2:0,3:1,4:0},[20,1,0]],
 ['F15',F15,15,{7:1,8:0,9:0,10:0,11:1,12:1,13:1,14:1,15:0},
                  {7:0,8:0,9:0,10:0,11:1,12:1,13:1,14:1,15:0},[1032,2,0]]
]){
 assert(grammar(F,N));
 const a=count(F,N),s=count(F,N,S),u=count(F,N,U);
 assert.deepEqual([a.models,s.models,u.models],expected);
 assert(!F.some(c=>c.every(v=>Math.abs(v) in U &&
                     U[Math.abs(v)]===(v>0?0:1))));
 result.controls[name]={root:a.models,S:s.models,U:u.models,U_leaves:u.leafCount};
}
for(const f of [B.concat([[1,2,3]]),B.map((c,i)=>i===0?[1,1,3]:c),
 B.map((c,i)=>i===0?[1,-2,3]:c),B.map((c,i)=>i===0?[-1,2,3]:c),
 B.map((c,i)=>i===0?[0,2,3]:c),B.slice(1)])assert(!grammar(f,12));
console.log(JSON.stringify(result,null,2));
// END_OF_VERIFIED_COMPACT::LSPV4::322::P_VS_NP_OPEN
