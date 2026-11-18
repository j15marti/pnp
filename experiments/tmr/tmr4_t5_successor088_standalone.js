#!/usr/bin/env node
"use strict";
// TMR-4/088 independent source-graph proof sanity check. Run: node tmr4_t5_successor088_standalone.js
// Exact CSP arcs only: u->v, u->z, z->v. No pre-supplied colors or z-roles to recognizer.
const R=(a,b)=>[1,3].includes((b-a+5)%5);
function source(k,twist){
 const n=2*k+k*k, arcs=[];
 for(let i=0;i<k;i++)for(let j=0;j<k;j++){
  let u=i,v=k+j; if(twist&&i===0&&j===0){const t=u;u=v;v=t}
  const z=2*k+i*k+j;arcs.push([u,v],[u,z],[z,v]);
 }return {n,arcs}
}
function certify(g){
 const {n,arcs}=g, outs=Array.from({length:n},()=>new Set()),ins=Array.from({length:n},()=>new Set()), seen=new Set();
 for(const [u,v] of arcs){if(u===v||u<0||v<0||u>=n||v>=n||seen.has(u+","+v))throw Error("bad arcs");seen.add(u+","+v);outs[u].add(v);ins[v].add(u)}
 const trip=[],zset=new Set();
 for(let z=0;z<n;z++)if(ins[z].size===1&&outs[z].size===1){
  const u=[...ins[z]][0],v=[...outs[z]][0];
  if(u!==v&&outs[u].has(v)){zset.add(z);trip.push([u,v,z])}
 }
 const core=Array.from({length:n},(_,i)=>i).filter(i=>!zset.has(i));
 if(core.some(u=>new Set([...ins[u],...outs[u]]).size<4))throw Error("ambiguous core");
 const covered=new Set(), pairs=new Set();
 for(const [u,v,z] of trip){
  if(zset.has(u)||zset.has(v)||pairs.has(u+","+v))throw Error("invalid expansion");
  pairs.add(u+","+v);for(const [a,b] of [[u,v],[u,z],[z,v]])covered.add(a+","+b)
 }
 if(covered.size!==seen.size||[...seen].some(e=>!covered.has(e)))throw Error("uncovered source arcs");
 const edges=Array.from({length:n},()=>[]);
 for(const [u,v,z] of trip){edges[u].push([v,1]);edges[v].push([u,-1])}
 const pot=Array(n).fill(null);let c=0,valid=true;
 for(const s of core)if(pot[s]===null){
  c++;pot[s]=0;const q=[s];
  for(let i=0;i<q.length;i++)for(const [v,d] of edges[q[i]]){
    const target=(pot[q[i]]+d+5)%5;
    if(pot[v]===null){pot[v]=target;q.push(v)}else if(pot[v]!==target)valid=false
  }
 }
 for(const [u,v,z] of trip)pot[z]=(pot[u]+3)%5;
 return {count:valid?5n**BigInt(c):0n,valid,c};
}
function exhaustive(g){
 let count=0n;
 for(let code=0;code<5**g.n;code++){
  let x=code,a=Array(g.n);
  for(let i=0;i<g.n;i++){a[i]=x%5;x=Math.floor(x/5)}
  if(g.arcs.every(([u,v])=>R(a[u],a[v])))count++;
 }return count
}
let sources=0,assignments=0;
for(const k of [2,3,4,8,20,100])for(const twist of [false,true]){
 const g=source(k,twist), a=certify(g);
 if(a.count!==(twist?0n:5n))throw Error("count mismatch");
 if(k===2){if(exhaustive(g)!==a.count)throw Error("brute mismatch");assignments+=5**g.n}
 sources++;
}
for(let x=0;x<5;x++){
 const fiber=[];for(let y=0;y<5;y++)for(let z=0;z<5;z++)
  if(R(x,y)&&R(x,z)&&R(z,y))fiber.push(y+","+z);
 if(fiber.length!==1||fiber[0]!==((x+1)%5)+","+((x+3)%5))throw Error("nonunique triangle");
}
console.log(JSON.stringify({sources,exhaustive_source_assignments:assignments,exact_triangle_fibers:5,unexpected_failures:0,P_versus_NP:"OPEN"}));
