'use strict';
const assert=require('node:assert/strict');
const graphs={K4:[4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]],
 cube:[8,Array.from({length:8},(_,a)=>Array.from({length:7-a},(_,k)=>[a,a+k+1]).filter(([u,v])=>((u^v).toString(2).match(/1/g)||[]).length===1)).flat()],
 Petersen:[10,[...Array.from({length:5},(_,i)=>[i,(i+1)%5]),...Array.from({length:5},(_,i)=>[i,i+5]),...Array.from({length:5},(_,i)=>[i+5,5+(i+2)%5])]]};
let projections=0,minorEdges=0;
for(const [name,[n,edges]] of Object.entries(graphs))for(let charge=0;charge<=1;charge++){
 const src=[],inc=Array.from({length:n},()=>[]);
 edges.forEach(([a,b],j)=>{inc[a].push(j+1);inc[b].push(j+1)});
 for(let v=0;v<n;v++)for(let bits=0;bits<8;bits++){
  const p=[bits&1,(bits>>1)&1,(bits>>2)&1];
  if((p[0]^p[1]^p[2])!==(v===0?charge:0))src.push(inc[v].map((x,i)=>p[i]?-x:x));
 }
 assert.equal(src.length,4*n);
 let uid=1;const owner=new Map(),occ=Array.from({length:edges.length+1},()=>[]);
 const cl=src.map(c=>c.map(l=>{const id=uid++;const o=Math.abs(l);owner.set(id,o);occ[o].push(id);return l>0?id:-id}));
 const branch=Array.from({length:edges.length+1},(_,i)=>new Set(occ[i]));
 for(let o=1;o<occ.length;o++)for(let k=1;k<occ[o].length;k++){
  const a=occ[o][k-1],b=occ[o][k];
  for(const two of [[-a,b],[a,-b]]){const z=uid++;owner.set(z,o);branch[o].add(z);cl.push([...two,z],[...two,-z]);}
 }
 const pair=x=>x.map(Math.abs).flatMap((v,i,a)=>a.slice(i+1).map(w=>Math.min(v,w)+','+Math.max(v,w)));
 const es=new Set(cl.flatMap(pair)),old=new Set(src.flatMap(pair));
 const contracted=new Set([...es].map(s=>s.split(',').map(Number)).filter(([a,b])=>owner.get(a)!==owner.get(b)).map(([a,b])=>Math.min(owner.get(a),owner.get(b))+','+Math.max(owner.get(a),owner.get(b))));
 for(const e of old){assert(contracted.has(e));minorEdges++}
 for(let o=1;o<branch.length;o++){
  const b=branch[o],q=[...b].slice(0,1),seen=new Set(q);
  while(q.length){const x=q.pop();for(const y of b){const e=Math.min(x,y)+','+Math.max(x,y);if(es.has(e)&&!seen.has(y)){seen.add(y);q.push(y)}}}
  assert.equal(seen.size,b.size);
 }
 assert(cl.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3));
 const evalf=(cs,asgn)=>cs.every(c=>c.some(l=>asgn[Math.abs(l)]===(l>0?1:0)));
 let count=0;
 for(let mask=0;mask<(1<<edges.length);mask++){
  const x=[0,...Array.from({length:edges.length},(_,i)=>(mask>>i)&1)];
  const lifted=Array.from({length:uid},(_,i)=>i?x[owner.get(i)]:0);
  assert.equal(evalf(src,x),evalf(cl,lifted));
  if(evalf(src,x))count++;
  projections++;
 }
 assert.equal(count>0,charge===0);
 console.log(name,charge?'UNSAT':'SAT','original-models',count,'lifted-clauses',cl.length);
}
console.log(JSON.stringify({status:'PASS',original_sources:6,projection_checks:projections,minor_edges:minorEdges}));
