#!/usr/bin/env node
/* TMR-4/091 standalone zero-dependency audit.
 * Exact five-symbol R(y-x in {1,3} mod 5), parsed source graph,
 * source-only halfgraph recognition, complete-query OBDD with dead
 * state, BigInt exact counts and direct pointwise source tests.
 * Run: node experiments/tmr/tmr4_t5_chain091_standalone.js
 */
"use strict";
const K=[1,2,3,4,5,10,20,40,100,200,400];
const out=Array.from({length:5},(_,a)=>(1<<((a+1)%5))|(1<<((a+3)%5)));
function beats(a,b){return ((b-a+5)%5===1)||((b-a+5)%5===3);}
function source(k){
  const arcs=[];
  for(let i=0;i<k;i++)for(let j=i;j<k;j++)arcs.push([i,k+j]);
  return {n:2*k,arcs};
}
function discover(g){
  const dIn=new Int32Array(g.n),dOut=new Int32Array(g.n),edges=new Set();
  for(const [u,v] of g.arcs){
    if(u===v||u<0||v<0||u>=g.n||v>=g.n)return null;
    dOut[u]++;dIn[v]++;edges.add(u+","+v);
  }
  const k=g.n/2;
  if(!Number.isInteger(k)||g.arcs.length!==k*(k+1)/2)return null;
  const U=[],V=[];
  for(let x=0;x<g.n;x++){
    if(dIn[x]===0&&dOut[x]>0)U.push(x);
    else if(dOut[x]===0&&dIn[x]>0)V.push(x);
    else return null;
  }
  U.sort((a,b)=>dOut[b]-dOut[a]);V.sort((a,b)=>dIn[a]-dIn[b]);
  if(U.length!==k||V.length!==k)return null;
  for(let i=0;i<k;i++){
    if(dOut[U[i]]!==k-i||dIn[V[i]]!==i+1)return null;
    for(let j=i;j<k;j++)if(!edges.has(U[i]+","+V[j]))return null;
  }
  return U.flatMap((u,i)=>[u,V[i]]);
}
function direct(g,colors){
  return g.arcs.every(([u,v])=>beats(colors[u],colors[v]));
}
function node(state,layer,color){
  if(!state)return 0;
  return layer%2===0 ? (state&out[color])
    : ((state&(1<<color))?state:0);
}
function evaluate(order,colors){
  let mask=31;
  for(let level=0;level<order.length;level++)
    mask=node(mask,level,colors[order[level]]);
  return mask!==0;
}
function count(n){
  let states=new Map([[31,1n]]),width=0,nodes=0;
  for(let level=0;level<n;level++){
    width=Math.max(width,states.size);nodes+=states.size;
    const next=new Map();
    for(const [state,num] of states.entries())
      for(let color=0;color<5;color++){
        const t=node(state,level,color);
        next.set(t,(next.get(t)||0n)+num);
      }
    states=next;
    let total=0n;for(const value of states.values())total+=value;
    if(total!==5n**BigInt(level+1))throw Error("lost multiplicity");
  }
  let accepted=0n,rejected=states.get(0)||0n;
  for(const [state,num] of states.entries())if(state)accepted+=num;
  if(accepted+rejected!==5n**BigInt(n))throw Error("terminal loss");
  return {accepted,rejected,width,nodes};
}
function exhaustive(g,order){
  const colors=new Int8Array(g.n);let checked=0,accepted=0;
  function go(level){
    if(level===g.n){
      const d=direct(g,colors),p=evaluate(order,colors);
      if(d!==p)throw Error("OBDD mismatch");
      checked++;accepted+=d?1:0;return;
    }
    for(let c=0;c<5;c++){colors[level]=c;go(level+1);}
  }
  go(0);return {checked,accepted};
}
let checks=0;const cases=[];
for(const k of K){
  const g=source(k),order=discover(g);
  if(!order)throw Error("source recognition "+k);
  const x=count(g.n),formula=5n*BigInt(k)*2n**BigInt(k);
  if(x.accepted!==formula||x.width>11)throw Error("formula or width "+k);
  if(k>=2&&(x.nodes!==22*k-21||x.width!==11))
    throw Error("exact OBDD count "+k);
  if(k<=4){
    const p=exhaustive(g,order);checks+=p.checked;
    if(BigInt(p.accepted)!==formula)throw Error("pointwise count");
  }
  cases.push({k,n:g.n,m:g.arcs.length,minimum_frontier_at_least:Math.floor(k/2),
    width:x.width,nodes:x.nodes,count:x.accepted.toString()});
}
const bad=source(4);bad.arcs.pop();
if(discover(bad))throw Error("missing-arc negative failed");
console.log(JSON.stringify({cases,pointwise_checks:checks,
  failed_representations:0,source_nonmembers_declined:1,
  status:"RESTRICTED COMPUTATIONAL audit; P versus NP OPEN"},null,2));
