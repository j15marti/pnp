#!/usr/bin/env node
/* LSPV-3 360: standalone width-independent signed-gate weakening replay. */
'use strict';
const assert=require('assert');
const canon=a=>{const s=new Set(a);for(const x of s)if(!Number.isInteger(x)||!x||s.has(-x))throw Error('bad clause');return [...s].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)};
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function generate(C,B){
 C=canon(C);B=canon(B);if(!C.length)throw Error('empty parent');
 canon(C.concat(B));let k=Math.max(...C.concat(B).map(Math.abs));
 const entries=new Map([['S0',C]]),defs=[],steps=[];let ref='S0';
 function step(left,right,p){const a=entries.get(left),b=entries.get(right);if(!a.includes(p)||!b.includes(-p))throw Error('pivot');const result=canon(a.filter(x=>x!==p).concat(b.filter(x=>x!==-p)));const id='R'+steps.length;steps.push({id,left,right,pivot:p,clause:result});entries.set(id,result);return id}
 for(const l of B){if(entries.get(ref).includes(l))continue;const u=entries.get(ref)[0];const y=++k, id='D'+defs.length;
  const slots=[canon([-y,u]),canon([-y,-l]),canon([y,-u,l])];defs.push({id,y,a:u,b:-l,slots});
  slots.forEach((s,i)=>entries.set(id+'.'+i,s));
  ref=step(ref,id+'.2',u);ref=step(ref,id+'.0',y);
 }
 const goal=canon(C.concat(B));if(!same(entries.get(ref),goal))throw Error('bad output');
 return {source:C,extra:B,goal,defs,steps,final:ref};
}
function check(p){const ent=new Map([['S0',canon(p.source)]]);if(!p.source.length)throw Error('empty source');
 let largest=Math.max(...p.source.concat(p.extra).map(Math.abs)),ref='S0';
 for(let i=0;i<p.defs.length;i++){const d=p.defs[i];if(d.id!=='D'+i||d.y<=largest||Math.abs(d.a)>=d.y||Math.abs(d.b)>=d.y)throw Error('invalid definition');
  const want=[canon([-d.y,d.a]),canon([-d.y,d.b]),canon([d.y,-d.a,-d.b])];if(!same(d.slots.map(canon),want))throw Error('forged signed slot');
  for(let j=0;j<3;j++)ent.set(d.id+'.'+j,want[j]);largest=d.y;
 }
 for(let i=0;i<p.steps.length;i++){const s=p.steps[i];if(s.id!=='R'+i||!ent.has(s.left)||!ent.has(s.right))throw Error('unknown parent');
  const a=ent.get(s.left),b=ent.get(s.right);if(!a.includes(s.pivot)||!b.includes(-s.pivot))throw Error('unsigned pivot');
  const c=canon(a.filter(x=>x!==s.pivot).concat(b.filter(x=>x!==-s.pivot)));if(!same(c,canon(s.clause)))throw Error('false resolvent');ent.set(s.id,c);
 }
 if(!ent.has(p.final)||!same(ent.get(p.final),canon(p.goal))||!same(canon(p.source.concat(p.extra)),canon(p.goal)))throw Error('incorrect conclusion');
 if(p.steps.length!==2*p.defs.length)throw Error('incorrect ledger');
 return p.steps.length+p.defs.length;
}
let cases=0,charged=0;
for(let k=2;k<=9;k++)for(let width=1;width<k;width++){
 const C=Array.from({length:width},(_,j)=>(j%2?-(j+1):j+1));
 const B=Array.from({length:k-width},(_,j)=>width+j+1);
 const p=generate(C,B),actual=check(p);
 assert.strictEqual(actual,3*(k-width));cases++;charged+=actual;
}
let rejected=0;const p=generate([-1,2,-3,4],[5,6,7,8]);
for(const change of [q=>q.defs[0].slots[0][0]*=-1,q=>q.steps[0].pivot*=-1,q=>q.steps[0].left='S88',q=>q.steps[0].clause.push(123),q=>q.final='S0']){
 const q=JSON.parse(JSON.stringify(p));change(q);try{check(q)}catch(e){rejected++}
}
assert.strictEqual(rejected,5);
console.log(JSON.stringify({status:'PASS',cases,charged_nodes:charged,corrupted_rejected:rejected,example_width4_add4:check(p)},null,2));
