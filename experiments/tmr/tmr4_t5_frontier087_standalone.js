#!/usr/bin/env node
// TMR-4/087 standalone C_n^2 source builder and independent full-color DP.
// Zero dependencies. This does NOT rely on Python's domain-mask OBDD.
'use strict';
const assert = require('assert');
const crypto = require('crypto');
const R = (a,b) => [1,3].includes((b-a+5)%5);
function build(n,unsat=false) {
  assert(n>=10 && n%5===0);
  const und=new Set();
  for(let i=0;i<n;i++) for(let d=1;d<=2;d++) {
    const j=(i+d)%n, u=Math.min(i,j), v=Math.max(i,j);
    und.add(`${u},${v}`);
  }
  const forced={'0,1':false,'0,2':false,'1,2':false,'1,3':false,'2,3':true};
  const arcs=[];
  for(const e of und) {
    const [u,v]=e.split(',').map(Number);
    const forward=unsat && Object.hasOwn(forced,e)?forced[e]:R(u%5,v%5);
    arcs.push(forward?[u,v]:[v,u]);
  }
  arcs.sort((a,b)=>a[0]-b[0] || a[1]-b[1]);
  return {n,arcs};
}
function countSource(src) {
  const {n,arcs}=src;
  const boundary=[],arriving=Array.from({length:n},()=>[]);
  for(let t=0;t<=n;t++) {
    const prior=new Set();
    for(const [u,v] of arcs) {
      if(u<t&&v>=t)prior.add(u);
      if(v<t&&u>=t)prior.add(v);
    }
    boundary.push([...prior].sort((a,b)=>a-b));
  }
  for(const [u,v] of arcs)arriving[Math.max(u,v)].push([u,v]);
  let states=new Map([['',1n]]);
  for(let i=0;i<n;i++) {
    const next=new Map();
    for(const [key,multiplicity] of states) {
      const old=key===''?[]:key.split(',').map(Number);
      const assignment={};
      boundary[i].forEach((v,j)=>assignment[v]=old[j]);
      for(let x=0;x<5;x++) {
        assignment[i]=x;
        if(!arriving[i].every(([u,v])=>R(assignment[u],assignment[v])))continue;
        const to=boundary[i+1].map(v=>assignment[v]).join(',');
        next.set(to,(next.get(to)||0n)+multiplicity);
      }
    }
    states=next;
  }
  return (states.get('')||0n).toString();
}
const lengths=[10,15,20,30,50,100,200];
const outputs=[];
for(const n of lengths)for(const unsat of [false,true]) {
  const original=build(n,unsat), count=countSource(original);
  assert((count==='0')===unsat);
  const sha256=crypto.createHash('sha256').update(JSON.stringify(original)).digest('hex');
  outputs.push({n,unsat,count,sha256});
}
assert.strictEqual(outputs[12].count,'627376149393920708177194198820147825840010');
assert.strictEqual(outputs[13].count,'0');
console.log(JSON.stringify({method:'Independent full-color BigInt DP',cases:outputs.length,outputs},null,2));
