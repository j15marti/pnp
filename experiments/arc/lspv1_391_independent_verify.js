#!/usr/bin/env node
'use strict';
// Independent finite checker for LSPV-1/391; no packages.
const fs = require('fs');
const raw = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const clauses = [[-1],[-2],[1],[2],[-2,-1],[-2,1],[-1,2],[1,2]];
const key = a => a.join(',');
function input(mask) {
  return clauses.filter((_,i)=>(mask & (1 << i))!==0).map(a=>a.slice());
}
function truth(f) {
  for(let v=0;v<4;v++) {
    if(f.every(c=>c.some(l=>l>0?!!(v&(1<<(l-1))):!(v&(1<<(-l-1)))))) return true;
  }
  return false;
}
function nextClauses(s) {
  const seen=new Set(s.map(key)); let newC=[];
  for(let i=0;i<s.length;i++)for(let j=i+1;j<s.length;j++) {
    for (const l of s[i]) {
      if (!s[j].includes(-l)) continue;
      const c=[...new Set([...s[i].filter(x=>x!==l),...s[j].filter(x=>x!==-l)])].sort((x,y)=>x-y);
      if(c.some(x=>c.includes(-x))) continue;
      if(!seen.has(key(c))) {seen.add(key(c));newC.push(c)}
    }
  }
  return newC;
}
function optimal(f) {
  if (f.some(c=>c.length===0))return 0;
  let frontier=[f],visited=new Set([f.map(key).sort().join('|')]);
  for(let d=1;d<=10;d++){
    const next=[];
    for(const state of frontier){
      for(const c of nextClauses(state)){
        if(!c.length)return d;
        const s=state.concat([c]); const h=s.map(key).sort().join('|');
        if(!visited.has(h)){visited.add(h);next.push(s)}
      }
    }
    frontier=next;
  }
  throw Error('unresolved');
}
let checks=0, nSat=0, nUnsat=0;
for(const r of raw.records){
  const f=input(r.mask);
  if(truth(f)!==r.sat)throw Error('SAT mismatch '+r.mask);
  if(r.sat) nSat++; else {nUnsat++;if(optimal(f)!==r.w)throw Error('W mismatch '+r.mask);}
  checks+=3;
  const sorted=f.map(c=>c.slice()).sort((a,b)=>{for(let i=0;i<Math.min(a.length,b.length);i++){if(a[i]!==b[i])return a[i]-b[i]}return a.length-b.length;});
  const ascii='CNF2|' + sorted.map(c=>c.join(',')).join(';') + '|';
  if(ascii.length!==r.a || 3+2*ascii.length!==r.b)throw Error('length mismatch '+r.mask);
}
if(nSat!==raw.counts.sat||nUnsat!==raw.counts.unsat)throw Error('count mismatch');
console.log(JSON.stringify({checks,nSat,nUnsat,success:true}));
