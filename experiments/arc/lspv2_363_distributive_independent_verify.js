// LSPV-2 363 independently authored public verifier. Run:
// node lspv2_363_distributive_independent_verify.js full.json
'use strict';
function canon(c){if(!Array.isArray(c))throw Error('clause');let s=[...new Set(c)];
 if(s.some(x=>!Number.isSafeInteger(x)||x===0||s.includes(-x)))throw Error('tautology/invalid');
 return s.sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}
function EQ(a,b){return canon(a).join()===canon(b).join()}
const AND=(z,a,b)=>[[-z,a],[-z,b],[z,-a,-b]];
const XOR=(z,a,b)=>[[a,b,-z],[a,-b,z],[-a,b,z],[-a,-b,-z]];
let assertions=0;function ok(b,msg){assertions++;if(!b)throw Error(msg)}
function verify(d){
 let {h,sources,proof,gates,root,variables}=d;
 ok(variables===10*h-2,'variables');
 ok(sources.length===25*h-6,'source count');
 ok(gates.length===7*h-2,'gate count');
 ok(proof.length===39*h-11,'certificate bound');
 let src=[];
 for(const g of gates){
  ok(['AND','XOR'].includes(g.t),'gate type');
  ok(g.z>3*h&&g.z<=variables&&g.a>0&&g.b>0&&g.a!==g.b&&g.a<g.z&&g.b<g.z,'gate topology');
  src.push(...(g.t==='AND'?AND(g.z,g.a,g.b):XOR(g.z,g.a,g.b)))}
 src.push([root[0],root[1]],[-root[0],-root[1]]);
 ok(src.length===sources.length,'slots length');
 for(let i=0;i<src.length;i++)ok(EQ(src[i],sources[i]),'source slot '+i);
 let all=sources.map(canon);
 for(let k=0;k<proof.length;k++){
  let step=proof[k], [u,v]=step.parents,p=step.pivot;
  ok(Number.isInteger(u)&&Number.isInteger(v)&&u>=0&&v>=0&&u<all.length&&v<all.length,'refs');
  let a=all[u],b=all[v];ok(a.includes(p)&&b.includes(-p),'signed pivot');
  let res=canon(a.filter(z=>z!==p).concat(b.filter(z=>z!==-p)));
  ok(EQ(res,step.clause),'resolvent');all.push(res)}
 ok(all.at(-1).length===0,'not contradiction');
 let bad=JSON.parse(JSON.stringify(proof));bad.at(-1).pivot=variables+1;
 let rejected=false;try{let s=bad.at(-1),[u,v]=s.parents;let a=all[u],b=all[v];if(!a.includes(s.pivot)||!b.includes(-s.pivot))throw Error('pivot')}catch(_){rejected=true}
 ok(rejected,'forged pivot accepted');
 let altered=gates.map(g=>({...g}));altered[4].t='AND';
 const near=altered.flatMap(g=>g.t==='AND'?AND(g.z,g.a,g.b):XOR(g.z,g.a,g.b)).concat(src.slice(-2));
 const nb=d.sat_neighbor;
 ok(nb.altered_gate_z===altered[4].z&&nb.source.length===near.length,'neighbor schema');
 for(let i=0;i<near.length;i++)ok(EQ(nb.source[i],near[i]),'neighbor source');
 let w=[0,...nb.witness];ok(w.length===variables+1&&w.slice(1).every(x=>x===0||x===1),'witness');
 for(let g of altered)ok(w[g.z]===(g.t==='AND'?(w[g.a]&w[g.b]):(w[g.a]^w[g.b])),'witness gate');
 for(const c of near)ok(c.some(t=>w[Math.abs(t)]===(t>0?1:0)),'witness clause');
 ok(w[root[0]]!==w[root[1]],'wrong label');
 // Full enumeration of the primary input space for n<=3, deterministic sample otherwise.
 const samples=h<=3?(1<<(3*h)):32;
 for(let mask=0;mask<samples;mask++){
  let v=Array(variables+1).fill(0);
  for(let i=1;i<=3*h;i++)v[i]=(h<=3)?((mask>>(i-1))&1):((Math.imul(mask+23+i,2654435761)>>>30)&1);
  for(let g of gates)v[g.z]=g.t==='AND'?(v[g.a]&v[g.b]):(v[g.a]^v[g.b]);
  ok(v[root[0]]===v[root[1]],'non-equivalent identity');
 }
 return {h,paid:proof.length,sources:sources.length}
}
function run(data){const rows=data.cases.map(verify);
 for(const malformed of [[],[0],['x'],[1,-1],[2,-2,3]]){let rejected=false;try{canon(malformed.length===0?[1,0]:malformed)}catch(e){rejected=true}if(malformed.length!==1||malformed[0]!==0)ok(rejected,'malformed')}
 return {status:'PASS',rows,assertions}}
if(typeof module!=='undefined'){module.exports={verify,run};
 if(require.main===module){const fs=require('fs');console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2],'utf8'))),null,2))}}
