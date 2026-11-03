#!/usr/bin/env node
// LSPV-2 352: self-contained Rmix341 paid weakening compiler and RES/VARDEF checker.
'use strict';
const canonical=a=>{if(!Array.isArray(a)||!a.length||a.some(x=>!Number.isInteger(x)||x===0))throw Error('malformed');let s=new Set(a);if(s.size!==a.length||a.some(x=>s.has(-x)))throw Error('tautological/duplicate');return [...s].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y)};
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function build(C,B){C=canonical(C);B=canonical(B);if(B.some(x=>C.includes(x)||C.includes(-x)))throw Error('overlap/complement');
let high=Math.max(...C.concat(B).map(Math.abs)),nodes=[{type:'source',clause:C}],defs=[];
function gate(a,b){let q=++high,slots=[[-q,a],[-q,b],[q,-a,-b]].map(canonical);nodes.push({type:'DEF',var:q,inputs:[a,b],slots});defs.push({q,slots});return q;}
let ws={};let w=-B[0];if(B.length>1){for(let i=1;i<B.length;i++){w=gate(i===1?-B[0]:w,-B[i]);ws[i+1]=w;}}
let qs=C.map(l=>gate(-l,w)),curr=C;
function resolve(other,p,label){if(!curr.includes(p)||!other.includes(-p))throw Error('bad pivot');let clause=canonical([...new Set([...curr.filter(x=>x!==p),...other.filter(x=>x!==-p)])]);nodes.push({type:'RES',pivot:p,left:curr,right:other,clause,label});curr=clause;}
for(let i=0;i<C.length;i++)resolve([-qs[i],-C[i]],C[i],'C_to_not_q');
for(let i=0;i<C.length;i++)resolve([qs[i],C[i],-w],-qs[i],'not_q_to_l_or_not_w');
for(let j=B.length;j>=2;j--)resolve(j===2?[ws[2],B[0],B[1]]:[ws[j],-ws[j-1],B[j-1]],-ws[j],'unfold_or_B');
const target=canonical(C.concat(B)),k=C.length,r=B.length,charge=3*k+2*r-2;
if(!eq(curr,target)||nodes.length!==charge+1)throw Error('bad compile');return {C,B,nodes,target,logical_cost:charge,definition_nodes:k+r-1,resolution_nodes:2*k+r-1};}
function verify(p){let allowed=new Set([JSON.stringify(p.C)]),slots=new Set(),max=Math.max(...p.C.concat(p.B).map(Math.abs));
for(let nd of p.nodes.slice(1)){if(nd.type==='DEF'){if(nd.var<=max||nd.inputs.some(x=>Math.abs(x)>max))throw Error('not fresh');let [a,b]=nd.inputs;let exp=[[-nd.var,a],[-nd.var,b],[nd.var,-a,-b]].map(canonical);if(!eq(nd.slots,exp))throw Error('bad DEF');for(let c of exp)slots.add(JSON.stringify(c));max=nd.var;}else if(nd.type==='RES'){let L=canonical(nd.left),R=canonical(nd.right),q=nd.pivot;if(!allowed.has(JSON.stringify(L))||!(allowed.has(JSON.stringify(R))||slots.has(JSON.stringify(R)))||!L.includes(q)||!R.includes(-q))throw Error('bad RES');let output=canonical([...new Set([...L.filter(x=>x!==q),...R.filter(x=>x!==-q)])]);if(!eq(output,nd.clause))throw Error('invalid resolvent');allowed.add(JSON.stringify(output));}else throw Error('unknown step');}
if(!eq(p.target,p.nodes.at(-1).clause)||p.logical_cost!==p.nodes.length-1)throw Error('wrong end');return true;}
const sizes=[[1,1],[1,4],[2,1],[2,3],[4,5],[6,2],[8,8]];const cases=sizes.map(([k,r])=>build([...Array(k)].map((_,i)=>i+1),[...Array(r)].map((_,i)=>k+i+1)));
cases.push(build([1,-2,3],[-4,5]),build([-1,-3],[-2,-4,-5]));for(let p of cases)verify(p);
let rejection=0;for(let p of cases){let c=JSON.parse(JSON.stringify(p));c.nodes.find(n=>n.type==='DEF').slots[0][0]*=-1;try{verify(c)}catch(e){rejection++;}}
if(rejection!==cases.length)throw Error('bad corruption rejection');
const out={run:'LSPV2-PAID-WEAKENING352',status:'PASS',fixed_calculus:'Rmix341 source-independent signed VARDEF plus strict binary RES',cases,costs:cases.map(x=>x.logical_cost),corrupt_rejections:rejection};
if(process.argv.includes('--raw'))console.log(JSON.stringify(out));else console.log(JSON.stringify({status:out.status,cases:cases.length,costs:out.costs,corrupt_rejections:rejection}));
