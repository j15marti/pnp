// LSPV2 XOR-DISTRIBUTIVE-TREE363. Fixed Rmix341, strict binary Resolution only.
// Usage: node lspv2_363_distributive_public.js 5
'use strict';
function canon(xs){const a=[...new Set(xs)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
 if(a.some(x=>!Number.isInteger(x)||x===0||a.includes(-x)))return null;return a}
const AND=(z,a,b)=>[[-z,a],[-z,b],[z,-a,-b]].map(canon);
const XOR=(z,a,b)=>[[a,b,-z],[a,-b,z],[-a,b,z],[-a,-b,-z]].map(canon);
const equiv=(a,b)=>[[-a,b],[a,-b]].map(canon);
function build(h){
 if(!Number.isInteger(h)||h<1||h>20000)throw Error('size');
 let nv=3*h,src=[],gates=[],groups=[],proof=[],root;
 function gate(t,a,b){let z=++nv;gates.push({t,a,b,z});src.push(...(t==='AND'?AND(z,a,b):XOR(z,a,b)));return z}
 for(let i=0;i<h;i++){let a=3*i+1,b=a+1,c=a+2,s=src.length;
   let t=gate('XOR',b,c),p=gate('AND',a,t),u=gate('AND',a,b),v=gate('AND',a,c),q=gate('XOR',u,v);
   groups.push({a,b,c,t,p,u,v,q,sources:Array.from({length:src.length-s},(_,j)=>s+j)})}
 function tree(l,r){if(r-l===1){const g=groups[l];return {p:g.p,q:g.q,block:l}}
   let m=(l+r)>>1,A=tree(l,m),B=tree(m,r),s=src.length;
   let p=gate('XOR',A.p,B.p),q=gate('XOR',A.q,B.q);
   return {p,q,children:[A,B],sources:Array.from({length:src.length-s},(_,j)=>s+j)}}
 root=tree(0,h);src.push(canon([root.p,root.q]),canon([-root.p,-root.q]));
 const M=src.length;
 function cl(id){return id<M?src[id]:proof[id-M].clause}
 function res(i,j,p){let a=cl(i),b=cl(j);if(!a.includes(p)||!b.includes(-p))throw Error('bad pivot');
   let c=canon(a.filter(x=>x!==p).concat(b.filter(x=>x!==-p)));
   if(!c)throw Error('tautological pivot');let id=M+proof.length;proof.push({parents:[i,j],pivot:p,clause:c});return id}
 function deriv(inputs,order,targets){
   const ids=new Map(inputs.map(i=>[cl(i).join(','),i]));let active=new Set(inputs);
   for(let x of order){const pos=[...active].filter(i=>cl(i).includes(x)).sort((a,b)=>a-b),
      neg=[...active].filter(i=>cl(i).includes(-x)).sort((a,b)=>a-b),fresh=[];
     for(let i of pos)for(let j of neg){
       let c=canon(cl(i).filter(t=>t!==x).concat(cl(j).filter(t=>t!==-x)));if(!c)continue;
       let key=c.join(',');if(!ids.has(key))ids.set(key,res(i,j,x));fresh.push(ids.get(key))}
     for(let i of pos.concat(neg))active.delete(i);for(let i of fresh)active.add(i)}
   return targets.map(t=>{let v=ids.get(t.join(','));if(v===undefined)throw Error('no target');return v})}
 function rec(t){
   if(t.block!==undefined){let g=groups[t.block];return deriv(g.sources,[g.t,g.u,g.v,g.a,g.b,g.c],equiv(g.p,g.q))}
   let A=t.children[0],B=t.children[1],e1=rec(A),e2=rec(B);
   return deriv(t.sources.concat(e1,e2),[A.p,A.q,B.p,B.q],equiv(t.p,t.q))}
 const [e0,e1]=rec(root);let u=res(M-2,e1,root.q),v=res(e0,M-1,root.q),last=res(u,v,root.p);
 if(cl(last).length)throw Error('not false');const raw=proof.length,seen=new Set();
 function visit(i){if(seen.has(i))return;seen.add(i);if(i>=M)proof[i-M].parents.forEach(visit)}
 visit(last);const kept=[...seen].filter(i=>i>=M).sort((a,b)=>a-b);
 const ren=new Map(kept.map((id,i)=>[id,M+i]));
 const pr=kept.map(id=>{const s=proof[id-M];return {...s,parents:s.parents.map(p=>ren.get(p)??p)}});
 if(pr.length>39*h-11||raw>47*h-15)throw Error('cap exceeded');
 return {h,variables:nv,sources:src,proof:pr,paid:pr.length,raw,cap:39*h-11,gates,root:[root.p,root.q]}
}
function check(d){const all=d.sources.map(canon),M=all.length;
 for(const s of d.proof){let [i,j]=s.parents,p=s.pivot;
  if(i>=all.length||j>=all.length||!all[i].includes(p)||!all[j].includes(-p))throw Error('forged pivot');
  let c=canon(all[i].filter(x=>x!==p).concat(all[j].filter(x=>x!==-p)));
  if(!c||c.join()!=canon(s.clause).join())throw Error('forged output');all.push(c)}
 if(all.at(-1).length)throw Error('no contradiction');return true
}
if(typeof module!=='undefined'){module.exports={build,check};
 if(require.main===module){let d=build(Number(process.argv[2]||5));check(d);console.log(JSON.stringify({h:d.h,variables:d.variables,sources:d.sources.length,paid:d.paid,raw:d.raw,cap:d.cap}))}}
