// LSPV-3/466 independent compact affine-substitution self-check.
// Full authenticated source generator and independent Python checker are in the reproducibility archive.
'use strict';
const assert=require('node:assert/strict');
const sx=(a,b)=>[...new Set([...a,...b])].filter(v=>a.includes(v)!==b.includes(v)).sort((x,y)=>x-y);
const add=(a,b)=>({v:sx(a.v,b.v),rhs:a.rhs^b.rhs});
function replay(edges,h){
 const incident=Array.from({length:h},(_,v)=>edges.flatMap((e,i)=>e.includes(v)?[i+1]:[]));
 assert(incident.every(x=>x.length===3));
 const n=edges.length,rows=incident.map((v,i)=>({v,rhs:i===0?1:0}));
 const d1={v:sx([n+1],[1,2]),rhs:0},d2={v:sx([n+2],[n+1,3]),rhs:0};
 let p=rows[0],q=0;const proof=[];
 for(let b of [d1,d2,...rows.slice(1),d1,d2]){p=add(p,b);proof.push(p);q++}
 assert.deepEqual(p,{v:[],rhs:1});
 const phi={};for(let i=1;i<=n;i++)phi[i]=[i];
 phi[n+1]=sx(phi[1],phi[2]);phi[n+2]=sx(phi[n+1],phi[3]);
 function project(r){let v=[];for(let i of r.v)v=sx(v,phi[i]);return {v,rhs:r.rhs};}
 assert.deepEqual(project(d1),{v:[],rhs:0});assert.deepEqual(project(d2),{v:[],rhs:0});
 let z=rows[0];for(let r of rows.slice(1))z=add(z,r);
 assert.deepEqual(z,{v:[],rhs:1});assert.deepEqual(project(p),z);
 for(let r of proof)assert(r.v.every(i=>i<=n+2));
 return {h,sourceClauses:4*h,augXor:q,projectedXor:h-1};
}
function complete(h){let e=[];for(let i=0;i<h;i++)for(let j=i+1;j<h;j++)e.push([i,j]);return e}
function bip(){let e=[];for(let i=0;i<3;i++)for(let j=3;j<6;j++)e.push([i,j]);return e}
function cube(){let e=[];for(let i=0;i<8;i++)for(let b=0;b<3;b++)if(!(i&(1<<b)))e.push([i,i^(1<<b)]);return e}
console.log(JSON.stringify([replay(complete(4),4),replay(bip(),6),replay(cube(),8)]));
