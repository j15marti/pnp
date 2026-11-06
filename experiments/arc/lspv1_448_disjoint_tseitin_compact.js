#!/usr/bin/env node
'use strict';
/* LSPV-1/448 independent compact control, declared /341 semantics, not authoritative byte checker */
const assert=require('assert');
let checks=0;const ok=x=>{assert(x);checks++};
function graph(name){
 if(name==='K4')return [4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]];
 if(name==='K33')return [6,Array.from({length:9},(_,i)=>[Math.floor(i/3),3+i%3])];
 throw Error('unknown graph');
}
function source(name,odd){
 let [h,edges]=graph(name),clauses=[],V=[];
 for(let v=0;v<h;v++){
  let inc=edges.flatMap((edge,i)=>edge.includes(v)?[i+1]:[]);
  ok(inc.length===3);
  let ids=[];
  for(let b=0;b<8;b++)if(((b&1)^((b>>1)&1)^((b>>2)&1))!==((v===0&&odd)?1:0)){
   ids.push(clauses.length);clauses.push(inc.map((x,i)=>((b>>i)&1)?-x:x));
  }
  ok(ids.length===4);V.push({inc,ids,charge:v===0&&odd?1:0});
 }
 return {h,edges,odd,clauses,V};
}
function sat(clauses,n){
 for(let mask=0;mask<2**n;mask++)
 if(clauses.every(c=>c.some(l=>(((mask>>(Math.abs(l)-1))&1)===(l>0?1:0)))))return mask;
 return null;
}
function checkSource(c){
 ok(c.clauses.length===4*c.h);ok(c.edges.length===3*c.h/2);
 ok((sat(c.clauses,c.edges.length)===null)===Boolean(c.odd));
 if(c.odd)for(let j=0;j<c.clauses.length;j++)
 ok(sat(c.clauses.filter((_,i)=>i!==j),c.edges.length)!==null);
}
function proofUpper(c){
 let rows=[],paid=0;
 for(let v of c.V){
  for(let bits=0;bits<8;bits++){
   const model=v.ids.every(j=>c.clauses[j].some(l=>(((bits>>v.inc.indexOf(Math.abs(l)))&1)===(l>0?1:0))));
   const parity=((bits&1)^((bits>>1)&1)^((bits>>2)&1))===v.charge;
   ok(model===parity);
  }
  rows.push({m:new Set(v.inc),b:v.charge});paid+=3;
 }
 while(rows.length>1){
  const next=[];
  for(let i=0;i<rows.length;i+=2){
   if(i+1===rows.length){next.push(rows[i]);continue;}
   const mask=new Set(rows[i].m);
   for(let x of rows[i+1].m){if(mask.has(x))mask.delete(x);else mask.add(x)}
   next.push({m:mask,b:rows[i].b^rows[i+1].b});paid++;
  }
  rows=next;
 }
 ok(rows[0].m.size===0&&rows[0].b===1);ok(paid===4*c.h-1);
 return paid;
}
const cases=[[['K4',0]],[['K4',1]],[['K33',0]],[['K33',1]],
 [['K4',1],['K33',0]],[['K4',0],['K33',1]],
 [['K4',1],['K33',1]],[['K4',0],['K33',0]]];
let costs=[];
for(let cs of cases){
 const parts=cs.map(([name,odd])=>source(name,odd));
 parts.forEach(checkSource);
 const odd=parts.filter(c=>c.odd);
 costs.push(odd.length?Math.min(...odd.map(proofUpper)):null);
}
ok(JSON.stringify(costs)===JSON.stringify([null,15,null,23,15,23,15,null]));
console.log(JSON.stringify({status:'PASS',cases:cases.length,computed_minimums:costs,
 assertions:checks,scope:'historical declared AND3/XOR semantics only'}));
