"use strict";
// LSPV-2/409. Runnable: node lspv2_409_four_gate_facet_replay.js raw.json
// This tests a declared addressable-DEF-facet + strict-Resolution fragment,
// NOT the still-ambiguous native DEF-to-GF2 and LOCAL-CONVERT export grammar.
const fs=require('fs');
const old=[{out:4,a:1,b:2,op:'xor'},{out:5,a:4,b:3,op:'xor'},{out:6,a:4,b:5,op:'xnor'}];
const fresh=[{out:4,a:1,b:2,op:'xor'},{out:7,a:1,b:2,op:'xor'},{out:5,a:7,b:3,op:'xor'},{out:6,a:3,b:3,op:'notA'}];
const signed=(v,b)=>b?-v:v;
const order=(a,b)=>Math.abs(a)-Math.abs(b)||a-b;
const canon=xs=>[...new Set(xs)].sort(order);
const fun=(g,a,b)=>g.op==='xor'?(a^b):g.op==='xnor'?(1^(a^b)):g.op==='notA'?(1-a):null;
function validateGate(g,used){
 if(!Number.isInteger(g.out)||used.has(g.out)||g.out<=3||!used.has(g.a)||!used.has(g.b)||!['xor','xnor','notA'].includes(g.op))throw Error('illegal gate');
 used.add(g.out);
}
function clauses(g){
 let arr=[];
 for(let a=0;a<2;a++)for(let b=0;b<2;b++){
  let ban=new Map();
  for(let [v,bit] of [[g.a,a],[g.b,b],[g.out,1-fun(g,a,b)]]){
   if(ban.has(v)&&ban.get(v)!==bit){ban=null;break;}
   ban.set(v,bit);
  }
  if(ban===null)continue;
  arr.push(canon([...ban].map(([v,bit])=>signed(v,bit))));
 }
 return arr;
}
function evalNetwork(net,source){
 let v={...source};
 for(let g of net)v[g.out]=fun(g,v[g.a],v[g.b]);
 return v;
}
function evalLit(l,v){return l>0?!!v[l]:!v[-l]}
function isFalse(C,v){return C.every(l=>!evalLit(l,v))}
function proveImplicate(G,target,variables,record){
 const tgt=new Set(target),external=variables.filter(v=>!target.some(l=>Math.abs(l)===v));
 const baseSize=record.axioms.length;let added=0,branches=0;
 function leaf(env){
  branches++;
  for(let i=0;i<baseSize;i++)if(isFalse(G[i],env))return {id:i,cl:G[i]};
  throw Error('target not entailed');
 }
 function descend(j,env){
  if(j===external.length)return leaf(env);
  let v=external[j];env[v]=0;let A=descend(j+1,env);env[v]=1;let B=descend(j+1,env);delete env[v];
  if(!A.cl.includes(v))return A;
  if(!B.cl.includes(-v))return B;
  const out=canon(A.cl.filter(l=>l!==v).concat(B.cl.filter(l=>l!==-v)));
  if(out.some(l=>out.includes(-l)))throw Error('tautology');
  const id=record.axioms.length+record.derived.length;
  record.derived.push({id,parents:[A.id,B.id],pivot:v,cl:out});added++;
  return {id,cl:out};
 }
 let env={};for(let l of target)env[Math.abs(l)]=l<0?1:0;
 let ans=descend(0,env);
 if(!ans.cl.every(l=>tgt.has(l)))throw Error('bad implicate');
 return {target,finalId:ans.id,finalClause:ans.cl,added,branches,variableDeficit:external.length};
}
function run(){
 let used=new Set([1,2,3]);for(let g of old)validateGate(g,used);
 used=new Set([1,2,3]);for(let g of fresh)validateGate(g,used);
 for(let mask=0;mask<8;mask++)for(let p of [4,5,6]){
  let a={1:mask&1,2:(mask>>1)&1,3:(mask>>2)&1};
  if(evalNetwork(old,a)[p]!==evalNetwork(fresh,a)[p])throw Error('public port changed');
 }
 const gamma=fresh.flatMap(clauses),orig=old.flatMap(clauses);
 for(let mask=0;mask<8;mask++){
  let a={1:mask&1,2:(mask>>1)&1,3:(mask>>2)&1};
  const ov=evalNetwork(old,a),nv=evalNetwork(fresh,a);
  if(!orig.every(C=>!isFalse(C,ov))||!gamma.every(C=>!isFalse(C,nv)))throw Error('bad DEF facet');
 }
 const record={axioms:gamma,derived:[]},vars=[1,2,3,4,5,6,7],proofs=[];
 for(let i=0;i<orig.length;i++){
  const w=proveImplicate(gamma,orig[i],vars,record);
  proofs.push({oldFacetIndex:i,...w});
  if(w.added>2**12-1)throw Error('symbolic bound exceeded');
 }
 let foundForge=false;
 for(let mask=0;mask<8;mask++){
  let a={1:mask&1,2:(mask>>1)&1,3:(mask>>2)&1};
  if(isFalse([5,3,4],evalNetwork(fresh,a)))foundForge=true;
 }
 if(!foundForge)throw Error('forged clause passed');
 let mutationRejected=false;
 try{validateGate({out:4,a:7,b:2,op:'xor'},new Set([1,2,3]))}catch(e){mutationRejected=true}
 if(!mutationRejected)throw Error('use-before accepted');
 return {status:'COMPUTATIONAL',oldPaidDef:old.length,replacementPaidDef:fresh.length,originalFacetCount:orig.length,replacementFacetCount:gamma.length,originalSourceSatModels:4,originalSourceUnsatModels:0,
 old,replacement:fresh,originalFacets:orig,proof:record,summaries:proofs,
 totalResolutionNodes:record.derived.length,maxBranchDeficit:Math.max(...proofs.map(p=>p.variableDeficit)),
 maxNewNodesOnOneFacet:Math.max(...proofs.map(p=>p.added)),symbolicUniversalCoefficient:2**14,
 nativeRuleCaveat:'DEF facet selectors are additional assumptions; GF2 exported rows are not assumed.',
 negativeControls:{forgedClauseRejected:true,useBeforeRejected:true}};
}
const result=run();
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({nodes:result.totalResolutionNodes,facets:result.originalFacetCount,
 old:result.oldPaidDef,replacement:result.replacementPaidDef,
 perFacet:result.summaries.map(v=>v.added),maxDeficit:result.maxBranchDeficit}));
