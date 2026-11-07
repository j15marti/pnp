'use strict';
// LSPV-3/476 compact source-only Resolution / shared-DAG control.
// Historical mixed R_mix341 byte grammar is NOT assumed or checked.
const assert=require('node:assert/strict');
const sort=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const valid=c=>c.every(x=>Number.isSafeInteger(x)&&x!==0&&!c.includes(-x));
let checks=0;const ck=x=>{checks++;assert.ok(x)};
function res(A,B,p){ck(A.includes(p)&&B.includes(-p));let C=sort([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)]);ck(valid(C));return C}
function replay(F,steps){const P=[];for(const t of steps){let c;if(t[0]==='s'){ck(t[1]>=0&&t[1]<F.length);c=sort(F[t[1]])}else{ck(t[0]==='r'&&t[1]<P.length&&t[2]<P.length&&t[1]>=0&&t[2]>=0);c=res(P[t[1]],P[t[2]],t[3])}P.push(c)}return P}
function models(F,n){let count=0;for(let mask=0;mask<(1<<n);mask++)if(F.every(C=>C.some(l=>Boolean(mask&(1<<(Math.abs(l)-1)))===(l>0))))count++;return count}
const F=[[1,2],[-1,2],[-2,3],[-2,-3]];
const trace=[['s',0],['s',1],['s',2],['s',3],['r',0,1,1],['r',4,2,2],['r',4,3,2],['r',5,6,3]];
const P=replay(F,trace);ck(JSON.stringify(P.slice(4))===JSON.stringify([[2],[3],[-3],[]]));ck(models(F,3)===0);
// Shared lemma [2] is referenced by both branch-derived opposing literals; paid once.
ck(trace.filter(t=>t[0]==='r').length===4&&trace[5][1]===4&&trace[6][1]===4);
function k4(odd){const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],F=[];for(let v=0;v<4;v++){
 const I=E.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);for(let t=0;t<8;t++){
 let q=((t&1)+((t>>1)&1)+((t>>2)&1))&1;if(q===((v===0&&odd)?1:0))continue;
 F.push(I.map((id,j)=>(t>>j)&1?-id:id));}}
return F}
const odd=k4(true),even=k4(false);ck(odd.length===16&&even.length===16);
ck(models(odd,6)===0&&models(even,6)===8);
// Build a source-indexed strict Resolution DAG by closure, then slice to ancestors.
function refute(F){let nodes=F.map((C,i)=>({step:['s',i],C:sort(C)})),seen=new Set(nodes.map(t=>t.C.join(',')));
 for(let i=0;i<nodes.length;i++)for(let j=0;j<i;j++)for(let p of nodes[i].C){
 if(!nodes[j].C.includes(-p))continue;let C=sort([...nodes[i].C.filter(x=>x!==p),...nodes[j].C.filter(x=>x!==-p)]);
 if(!valid(C)||seen.has(C.join(',')))continue;seen.add(C.join(','));nodes.push({step:['r',i,j,p],C});if(C.length===0){
 let live=new Set(),stack=[nodes.length-1];while(stack.length){let v=stack.pop();if(live.has(v))continue;live.add(v);if(nodes[v].step[0]==='r')stack.push(nodes[v].step[1],nodes[v].step[2])}
 let ids=[...live].sort((a,b)=>a-b),map=new Map(ids.map((v,k)=>[v,k]));let steps=ids.map(v=>nodes[v].step[0]==='s'?nodes[v].step:['r',map.get(nodes[v].step[1]),map.get(nodes[v].step[2]),nodes[v].step[3]]);
 const last=replay(F,steps).at(-1);ck(last.length===0);return {paid:steps.filter(t=>t[0]==='r').length,steps:steps.length};}}
 throw Error('unexpected SAT source')}
const r=refute(odd);ck(r.paid===31);
function reject(f){let bad=false;try{f()}catch(_){bad=true}ck(bad)}
reject(()=>replay(F,[['s',1000]]));reject(()=>replay(F,[['s',0],['s',1],['r',0,1,3]]));reject(()=>replay(F,[['a',1]]));
console.log(JSON.stringify({run:'LSPV-3/476',strict_source_only_resolution:true,shared_paid_lemma:1,shared_example_paid:4,k4_original_clauses:16,k4_resolution_paid:r.paid,odd_models:0,even_models:8,assertions:checks,hostile_rejections:3,historical_native_checker:false,status:'COMPUTATIONAL; P versus NP OPEN'}));
