#!/usr/bin/env node
"use strict";
/* LSPV-4/529 paid-live pebbling control. This is a DAG audit,
 * NOT the historical R_mix341 checker or a native physical RAM measurement.
 * Source clauses are read-only; each paid inference requires one fresh slot;
 * after last use a slot may be deleted; recomputation is prohibited. */
function ck(b,s){if(!b)throw Error(s)}
function dag(k){
 ck(Number.isInteger(k)&&k>=0&&k<=16,"bad k");
 let p=[];for(let v=0;v<4;v++)p.push([], [3*v], [3*v+1]);
 p.push([2,5],[12,8],[13,11]);
 for(let j=0;j<k;j++)p.push([j?14+2*j:14,12],[15+2*j,12]);
 for(let j=0;j<p.length;j++)for(const i of p[j])ck(i<j,"invalid ancestry");
 return p;
}
function peakFor(p,order){
 ck(order.length===p.length&&new Set(order).size===p.length,"incomplete permutation");
 const users=p.map((_,j)=>p.map((q,i)=>q.includes(j)?i:-1).filter(i=>i>=0));
 let seen=new Set(),peak=0;
 for(const j of order){
  ck(!seen.has(j)&&j>=0&&j<p.length,"freshness");
  for(const i of p[j])ck(seen.has(i),"parent unavailable");
  let live=0;for(const i of seen)if(users[i].some(v=>!seen.has(v)))live++;
  peak=Math.max(peak,live+1);seen.add(j);
 }
 return peak;
}
function exact(p){
 const n=p.length,full=(1n<<BigInt(n))-1n;
 const req=p.map(a=>a.reduce((x,j)=>x|(1n<<BigInt(j)),0n));
 const uses=p.map((_,i)=>p.reduce((x,a,j)=>a.includes(i)?x|(1n<<BigInt(j)):x,0n));
 let frontier=new Map([[0n,{cost:0,order:[]}]]),states=1;
 for(let depth=0;depth<n;depth++){
  const next=new Map();
  for(const [mask,val] of frontier){
   let live=0;
   for(let i=0;i<n;i++)if((mask&(1n<<BigInt(i)))&&(uses[i]&~mask))live++;
   for(let i=0;i<n;i++){
    const bit=1n<<BigInt(i);
    if(mask&bit||(req[i]&mask)!==req[i])continue;
    const target=mask|bit,cost=Math.max(val.cost,live+1);
    if(!next.has(target)||next.get(target).cost>cost)
      next.set(target,{cost,order:val.order.concat(i)});
   }
  }
  ck(next.size>0,"frontier empty");states+=next.size;frontier=next;
 }
 const v=frontier.get(full);ck(v&&peakFor(p,v.order)===v.cost,"bad optimum witness");
 return {peak:v.cost,states,order:v.order};
}
function explicit(k){
 return [0,1,2,3,4,5,12,6,7,8,...(k===0?[13,9,10,11,14]:[9,10,11,13,14]),
  ...Array.from({length:2*k},(_,i)=>15+i)];
}
function source(odd){
 const edges=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)edges.push([a,b]);
 const clauses=[];
 for(let v=0;v<4;v++){
  const indices=edges.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
  for(let pat=0;pat<8;pat++){
   const parity=((pat&1)^((pat>>1)&1)^((pat>>2)&1));
   if(parity===(odd&&v===0?1:0))continue;
   clauses.push(indices.map((e,j)=>((pat>>j)&1)?-(e+1):e+1));
  }
 }
 let sat=0;for(let a=0;a<64;a++)if(clauses.every(c=>c.some(l=>l>0?((a>>(l-1))&1):!((a>>(-l-1))&1))))sat++;
 return {clauses:clauses.length,satisfyingAssignments:sat};
}
function reject(f){try{f();return false}catch{return true}}
const tests=[0,1,2,3,4,8,16].map(k=>{
 const p=dag(k),opt=exact(p),w=peakFor(p,explicit(k));
 ck(opt.peak===(k?4:3)&&w===opt.peak,"wrong paid-live theorem");
 return {k,paid:p.length,references:p.reduce((s,x)=>s+x.length,0),
   peak:opt.peak,enumeratedStates:opt.states,witness:opt.order};
});
const controls={
 missingParent:reject(()=>{let p=dag(1);p[15][0]=100;peakFor(p,explicit(1))}),
 futureParent:reject(()=>{let p=dag(1);p[12][0]=15;peakFor(p,explicit(1))}),
 missingNode:reject(()=>peakFor(dag(1),explicit(1).slice(1))),
 falseThreeSlot:reject(()=>ck(peakFor(dag(1),explicit(1))<=3,"three paid slots"))
};
ck(Object.values(controls).every(Boolean),"hostile failure");
const odd=source(true),even=source(false);
ck(odd.clauses===16&&odd.satisfyingAssignments===0&&even.satisfyingAssignments===8,"source control");
const result={run:529,status:"PROVED/RESTRICTED + COMPUTATIONAL",
 claim:"fixed source-bound K4 SOURCE/AND3/XOR occurrence DAG: paid-live optimal peak 3 for k=0, 4 for all k>=1, unit work 15+2k",
 model:"source nodes read-only; paid results must use fresh live slots; last-use deletion permitted; no recomputation",
 tests,controls,source:{odd,even},
 limitations:"Not complete R_mix341 byte grammar; no physical peak RAM or proof discovery charge; historical weights unchanged."};
console.log(JSON.stringify(result,null,2));
