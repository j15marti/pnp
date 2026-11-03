#!/usr/bin/env node
'use strict';
// Public compact end-to-end authentic strict-Resolution certificate builder.
// For all 2^k assignment blocker clauses, proves global exact mixed min 2^k-1
// using indispensable-source arity plus an independently checked Resolution DAG.
const assert=require('assert');
const litSort=(a,b)=>Math.abs(a)-Math.abs(b)||b-a;
const cn=a=>[...new Set(a)].sort(litSort);
const rs=(p,q,v)=>{
 assert(p.includes(v)&&q.includes(-v),'bad pivot');
 const a=cn([...p.filter(x=>x!==v),...q.filter(x=>x!==-v)]);
 assert(!a.some(x=>a.includes(-x)),'tautological');return a;
};
const test=k=>{
 let source=[];
 for(let mask=0;mask<(1<<k);mask++){
   source.push(cn(Array.from({length:k},(_,i)=>(mask&(1<<i))?-(i+1):(i+1))));
 }
 // Source 0/1 are contiguous in bit order; each adjacent pair opposite x1.
 let nodes=source.map(clause=>({clause})), active=source.map((_,i)=>i);
 for(let v=1;v<=k;v++){
   let nxt=[];
   for(let j=0;j<active.length;j+=2){
     let a=active[j],b=active[j+1];
     assert(nodes[a].clause.includes(v)&&nodes[b].clause.includes(-v));
     let clause=rs(nodes[a].clause,nodes[b].clause,v);
     nodes.push({p:a,q:b,v,clause});nxt.push(nodes.length-1);
   }
   active=nxt;
 }
 assert.strictEqual(active.length,1);
 for(let i=source.length;i<nodes.length;i++){
   const x=nodes[i];assert.deepStrictEqual(x.clause,rs(nodes[x.p].clause,nodes[x.q].clause,x.v));
 }
 assert.deepStrictEqual(nodes[active[0]].clause,[]);
 // Each deleted source has its own unique model.
 for(let mask=0;mask<(1<<k);mask++){
   let bits=Array.from({length:k},(_,i)=>!!(mask&(1<<i)));
   const truth=c=>c.some(x=>bits[Math.abs(x)-1]===(x>0));
   assert.strictEqual(source.filter((c,j)=>j!==mask).every(truth),true);
   assert.strictEqual(truth(source[mask]),false);
 }
 let bad=JSON.parse(JSON.stringify(nodes));if(k>0){bad[source.length].v=k+1;
   assert.throws(()=>rs(bad[bad[source.length].p].clause,bad[bad[source.length].q].clause,bad[source.length].v));}
 return {k,variables:k,sources:source.length,inferences:nodes.length-source.length,certified_minimum:source.length-1,source_delete_sat_witnesses:source.length};
};
const out={claim:'BLOCKER-SHARP-CONTROL357',results:Array.from({length:7},(_,i)=>test(i+1)),label:'exact source-arity-plus-Resolution minima, no decision-time lower bound'};
console.log(JSON.stringify(out,null,2));
