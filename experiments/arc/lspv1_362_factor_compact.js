#!/usr/bin/env node
"use strict";
// Standalone dependency-free exact-source XOR4 proof with paid RES+VARDEF.
// Full 7-case Python producer and independent Node verifier archived locally.
function canon(xs){let a=[...new Set(xs)].sort((x,y)=>Math.abs(x)-Math.abs(y)||y-x);if(a.some(x=>a.includes(-x)))throw Error('tautology');return a}
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const S=[1,2,3,4],U=[1,4],P=[1,2,3],Q=[2,3,4];
const enumA=(v)=>{let o=[];for(let mask=0;mask<2**v.length;mask++){let a={};v.forEach((k,j)=>a[k]=(mask>>(v.length-j-1))&1);o.push(a)}return o};
const parity=(a,vs,rhs)=>vs.reduce((acc,k)=>acc+a[k],0)%2===rhs;
const blocker=(a,vs)=>canon(vs.map(v=>a[v]?-v:v));
const src=[];
for(let [name,vs,rhs] of [['left',P,0],['right',Q,1],['opposite',U,0]])for(let a of enumA(vs))if(!parity(a,vs,rhs))src.push({op:'source',name,clause:blocker(a,vs)});
const lines=src.map(x=>({...x}));let next=5;
const clause=i=>lines[i].clause;
function addDef(a,b){if(Math.abs(a)===Math.abs(b))throw Error('equal input variables');let q=next++;let slots=[canon([-q,a]),canon([-q,b]),canon([q,-a,-b])];lines.push({op:'def',q,inputs:[a,b],slots});return lines.length-1}
function slot(i,j){lines.push({op:'slot',def:i,which:j,clause:lines[i].slots[j]});return lines.length-1}
function res(i,j,p){let a=clause(i),b=clause(j);let c;if(a.includes(p)&&b.includes(-p))c=canon(a.filter(x=>x!==p).concat(b.filter(x=>x!==-p)));else if(a.includes(-p)&&b.includes(p))c=canon(a.filter(x=>x!==-p).concat(b.filter(x=>x!==p)));else throw Error('invalid resolution');lines.push({op:'res',parents:[i,j],pivot:p,clause:c});return lines.length-1}
function weaken(i,add){let D=clause(i);let w=-add[0],chain=[];for(let b of add.slice(1)){let j=addDef(w,-b);w=lines[j].q;chain.push(j)}let gs=D.map(x=>addDef(-x,w)),t=i;
for(let j=0;j<D.length;j++)t=res(t,slot(gs[j],0),D[j]);
for(let j=0;j<D.length;j++)t=res(t,slot(gs[j],2),-lines[gs[j]].q);
for(let j of chain.slice().reverse())t=res(t,slot(j,2),-lines[j].q);
if(!eq(clause(t),canon(D.concat(add))))throw Error('weakening result');return t}
const terminal=[];
for(let beta of enumA(U)){if(parity(beta,U,1))continue;let leaves={};for(let rest of enumA([2,3])){
let a={...beta,...rest},name=parity(a,P,0)?'right':'left',vs=name==='left'?P:Q,bl=blocker(a,vs);
let idx=lines.findIndex(x=>x.op==='source'&&x.name===name&&eq(x.clause,bl));
let add=blocker(a,S).filter(x=>!vs.includes(Math.abs(x)));
leaves[''+a[2]+a[3]]=weaken(idx,add);
}
let left0=res(leaves['00'],leaves['01'],3),left1=res(leaves['10'],leaves['11'],3);
let t=res(left0,left1,2);if(!eq(clause(t),blocker(beta,U)))throw Error('factor clause');terminal.push(t)}
function findFrom(ids,cl){return ids.find(i=>eq(clause(i),canon(cl)))}
const opp=src.map((x,i)=>x.name==='opposite'?i:-1).filter(i=>i>=0);
let pos=res(findFrom(terminal,[1,4]),findFrom(opp,[1,-4]),4),neg=res(findFrom(terminal,[-1,-4]),findFrom(opp,[-1,4]),-4);
const final=res(pos,neg,1);if(clause(final).length!==0)throw Error('not refuted');
function verify(){let defs=new Map(),clauses=new Map(),cost=0,gate=4;
for(let i=0;i<lines.length;i++){let x=lines[i];if(x.op==='source'){if(!src.some(y=>y.name===x.name&&eq(y.clause,x.clause)))throw Error('bad source');clauses.set(i,x.clause)}
else if(x.op==='def'){if(x.q!==++gate)throw Error('unfresh gate');let [a,b]=x.inputs;if(Math.abs(a)===Math.abs(b)||Math.abs(a)>=x.q||Math.abs(b)>=x.q)throw Error('illegal gate');let slots=[canon([-x.q,a]),canon([-x.q,b]),canon([x.q,-a,-b])];if(!eq(slots,x.slots))throw Error('bad slots');defs.set(i,x);cost++}
else if(x.op==='slot'){if(!defs.has(x.def)||!eq(defs.get(x.def).slots[x.which],x.clause))throw Error('unauth slot');clauses.set(i,x.clause)}
else if(x.op==='res'){let [a,b]=x.parents;if(a>=i||b>=i||!clauses.has(a)||!clauses.has(b))throw Error('bad parent');let A=clauses.get(a),B=clauses.get(b),p=x.pivot,z;if(A.includes(p)&&B.includes(-p))z=canon(A.filter(y=>y!==p).concat(B.filter(y=>y!==-p)));else if(A.includes(-p)&&B.includes(p))z=canon(A.filter(y=>y!==-p).concat(B.filter(y=>y!==p)));else throw Error('no complementary pivot');if(!eq(z,x.clause))throw Error('bad resolvent');clauses.set(i,z);cost++}
else throw Error('bad op')}
if(!clauses.has(final)||clauses.get(final).length!==0||cost!==81)throw Error('bad proof');
return {status:'PASS',sources:src.length,paid_def:lines.filter(x=>x.op==='def').length,paid_res:lines.filter(x=>x.op==='res').length,paid_total:cost,final_index:final};}
const result=verify();
if(typeof module!=='undefined'&&require.main===module)console.log(JSON.stringify(result,null,2));
