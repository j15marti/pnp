#!/usr/bin/env node
"use strict";
/* LSPV-1/587 exact zero-charge closure control; NOT historical R_mix341. */
function chk(b,m){if(!b)throw Error(m);}
function graph(n,e,goals){return {n,e,goals:new Set(goals)};}
function close(G,s){
 const got=new Set([s]),todo=[s];
 for(let i=0;i<todo.length;i++)for(const a of G.e)
   if(a.u===todo[i]&&a.w===0&&!got.has(a.v)){got.add(a.v);todo.push(a.v);}
 return got;
}
function dist(G,s){
 const d=Array(G.n).fill(Infinity),used=new Set();d[s]=0;
 for(let k=0;k<G.n;k++){
  let j=-1;for(let i=0;i<G.n;i++)
   if(!used.has(i)&&(j<0||d[i]<d[j]))j=i;
  if(j<0||!Number.isFinite(d[j]))break;
  used.add(j);for(const a of G.e)if(a.u===j)d[a.v]=Math.min(d[a.v],d[j]+a.w);
 }
 return Math.min(...Array.from(G.goals,g=>d[g]));
}
function saturated(G){
 const z=Array.from({length:G.n},(_,i)=>close(G,i)),sets=[],index=[],keys=new Map();
 for(let i=0;i<G.n;i++){
  let k=[...z[i]].sort((a,b)=>a-b).join(",");
  if(!keys.has(k)){keys.set(k,sets.length);sets.push(z[i]);}
  index[i]=keys.get(k);
 }
 const e=[];for(let i=0;i<sets.length;i++)for(const a of G.e)
  if(a.w>0&&sets[i].has(a.u))e.push({u:i,v:index[a.v],w:a.w});
 let ze=0,pe=0;for(const a of G.e){
  chk(Number.isInteger(a.w)&&a.w>=0,"negative/native cost");
  if(a.w===0){ze++;for(const t of z[a.v])chk(z[a.u].has(t),"free closure omitted");}
  else {pe++;chk(e.some(b=>b.u===index[a.u]&&b.v===index[a.v]&&b.w===a.w),"positive edge omitted");}
 }
 const goals=sets.flatMap((ss,i)=>[...G.goals].some(t=>ss.has(t))?[i]:[]);
 return {G:graph(sets.length,e,goals),sets,index,ze,pe};
}
function audit(G){
 const q=saturated(G),values=[];
 for(let i=0;i<G.n;i++){
  const a=dist(G,i),b=dist(q.G,q.index[i]);
  chk(a===b,"normal form not exact at "+i);values.push(a);
 }
 return {q,values,states:G.n};
}
function owned(){
 const e=[];for(let p=0;p<8;p++)for(let h=0;h<4;h++){
  const u=p*4+h;
  if(!(p&1))e.push({u,v:(p|1)*4+h,w:1,rule:"PAY_SHARED_OWNER"});
  for(let bit=1;bit<=2;bit*=2)if(!(h&bit)){
    if(p&1)e.push({u,v:p*4+(h|bit),w:0,rule:"REUSE_FREE_FACET"});
    const id=bit===1?2:4;
    if(!(p&id))e.push({u,v:(p|id)*4+(h|bit),w:2,rule:"PAY_DIRECT_NODE"});
  }
 }
 return graph(32,e,Array.from({length:8},(_,p)=>p*4+3));
}
function main(){
 const G=owned(),a=audit(G);chk(a.values[0]===1&&a.values[4]===0,"owner sharing");
 chk(a.q.sets[a.q.index[4]].size===4,"all two free facets");
 const B=graph(3,[{u:0,v:1,w:0},{u:0,v:2,w:1},{u:1,v:2,w:10}],[2]);
 const b=audit(B);chk(b.values[1]===10&&b.values[0]===1,"one-way witness");
 const C=graph(3,[{u:0,v:1,w:0},{u:1,v:0,w:0},{u:1,v:2,w:2}],[2]);
 const c=audit(C);chk(c.q.index[0]===c.q.index[1]&&c.values[0]===2,"SCC witness");
 const D=graph(G.n,G.e.concat([{u:0,v:3,w:0,rule:"HYPOTHETICAL_UNKNOWN_RULE"}]),[...G.goals]);
 const d=audit(D);chk(d.values[0]===0&&a.values[0]===1,"zero rule omitted");
 let finiteGraphs=0,finiteStateChecks=0;
 const pairs=[[0,1],[0,2],[1,0],[1,2],[2,0],[2,1]];
 for(let encoding=0;encoding<4096;encoding++){
  let bits=encoding,es=[];
  for(const [u,v] of pairs){
   const kind=bits%4;bits=Math.floor(bits/4);
   if(kind!==0)es.push({u,v,w:kind-1});
  }
  for(let goal=0;goal<3;goal++){
   audit(graph(3,es,[goal]));
   finiteGraphs++;finiteStateChecks+=3;
  }
 }
 return {id:"LSPV-1/587",status:"PROVED/RESTRICTED theorem; COMPUTATIONAL finite controls",
  scope:"declared nonnegative weighted full-state graphs, NOT authenticated historical R_mix341",
  allStateExactComparisons:a.states+b.states+c.states+d.states+finiteStateChecks,
  exhaustiveThreeStateGraphs:finiteGraphs,
  paidOwner:{states:a.states,zeroEdges:a.q.ze,positiveEdges:a.q.pe,
    saturatedStates:a.q.G.n,startCost:a.values[0],afterPaidCost:a.values[4],
    facetsInFreeClosure:a.q.sets[a.q.index[4]].size},
  oneWay:{startB:1,exactCost:b.values[1],incorrectLabelMergeCost:1},
  zeroCycle:{sourceCost:c.values[0],saturatedStates:c.q.G.n},
  missingZeroRule:{omittingGives:a.values[0],includingGives:d.values[0]},
  noRandomness:true,hostileChecksPassed:true};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module)
 console.log(JSON.stringify(main(),null,2));