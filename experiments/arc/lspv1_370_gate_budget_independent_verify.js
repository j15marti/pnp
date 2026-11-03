#!/usr/bin/env node
'use strict';
// Independently written finite source/proof verifier for LSPV1 result 370.
// No library beyond Node stdlib, no solver, no claim to verify asymptotic Braun theorem.
const fs=require('fs');
const raw=JSON.parse(fs.readFileSync(process.argv[2]||'gate_budget_controls_raw.json','utf8'));
let assertions=0;
function ok(v,msg){assertions++;if(!v)throw Error(msg)}
function normalize(c){let a=[...new Set(c)].sort((x,y)=>Math.abs(x)-Math.abs(y)||y-x);if(a.some(x=>a.includes(-x)))throw Error('tautology');return a}
function same(a,b){return JSON.stringify(normalize(a))===JSON.stringify(normalize(b))}
function resolve(a,b,p){if(!(a.includes(p)&&b.includes(-p)||a.includes(-p)&&b.includes(p)))throw Error('bad pivot '+p);let aa=a.includes(p)?a.filter(x=>x!==p):a.filter(x=>x!==-p);let bb=a.includes(p)?b.filter(x=>x!==-p):b.filter(x=>x!==p);return normalize(aa.concat(bb))}
function satisfied(C,vals){return C.some(v=>v>0?Boolean(vals[Math.abs(v)]):!Boolean(vals[Math.abs(v)]))}
const sources=[[1],[2],[-1,-2]];
const slots=[[-3,1],[-3,2],[3,-1,-2]];
ok(raw.tiny_paid_mixed_proof.paid_definition_nodes===1,'one charged definition');
ok(raw.tiny_paid_mixed_proof.strict_RES_nodes===5,'five charged RES');
ok(raw.tiny_paid_mixed_proof.total_paid_nodes===6,'one plus five');
const nodes=[];
nodes.push(resolve(slots[2],sources[0],-1));
nodes.push(resolve(nodes[0],sources[1],-2));
nodes.push(resolve(sources[2],slots[0],-1));
nodes.push(resolve(nodes[2],slots[1],-2));
nodes.push(resolve(nodes[1],nodes[3],3));
for(let i=0;i<nodes.length;i++)ok(same(nodes[i],raw.tiny_paid_mixed_proof.derived_clauses[i]),'signed proof line '+i);
ok(nodes[nodes.length-1].length===0,'empty proof root');
for(const a of [0,1])for(const b of [0,1]){
 const vals={1:a,2:b,3:a&b};
 for(const C of slots)ok(satisfied(C,vals),'AND slot must be true');
 const B=normalize([a?-1:1,b?-2:2]);
 let key='('+a+', '+b+')';
 ok(same(B,raw.same_source_guard_lift.blockers[key]),'guard identity '+key);
 ok(sources.some(C=>C.every(l=>!satisfied([l],vals))&&C.every(l=>B.includes(l))),'falsified source is weaker than blocker');
}
const b=raw.same_source_guard_lift.blockers;
ok(same(resolve(b['(0, 0)'],b['(0, 1)'],2),[1]),'left guard merge');
ok(same(resolve(b['(1, 0)'],b['(1, 1)'],2),[-1]),'right guard merge');
ok(same(resolve([1],[-1],1),[]),'guard root');
ok(raw.same_source_guard_lift.derived_ordinary_RES_merges===3,'three guarded merges');
// Each source deletion and one occurrence sign change must allow a model.
for(let removed=0;removed<3;removed++){
 const sub=sources.filter((_,i)=>i!==removed);
 ok([0,1].some(a=>[0,1].some(b=>sub.every(C=>satisfied(C,{1:a,2:b})))),'source deletion SAT');
 for(const lit of sources[removed]){
  const F=sources.map((C,i)=>i===removed?C.map(x=>x===lit?-x:x):C);
  ok([0,1].some(a=>[0,1].some(b=>F.every(C=>satisfied(C,{1:a,2:b})))),'signed flip SAT');
 }
}
ok(![0,1].some(a=>[0,1].some(b=>sources.every(C=>satisfied(C,{1:a,2:b})))),'original UNSAT');
const edges=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)edges.push([a,b]);
function k4(odd){let out=[];for(let v=0;v<4;v++){
 let vars=edges.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);
 for(let b=0;b<8;b++){
 let x=[b&1,(b>>1)&1,(b>>2)&1];
 if((x[0]^x[1]^x[2])!==(odd&&v===0?1:0))out.push(vars.map((id,j)=>x[j]?-id:id));
 }}return out}
for(let odd of [false,true]){
 const C=k4(odd);
 let models=0;for(let mask=0;mask<64;mask++){
 let vals={};for(let i=1;i<=6;i++)vals[i]=(mask>>(i-1))&1;
 if(C.every(c=>satisfied(c,vals)))models++;
 }
 const expected=odd?raw.k4_controls.odd.models:raw.k4_controls.even.models;
 ok(models===expected,'K4 model counts');
 ok(C.length===16,'K4 clause count');
}
for(const bad of [{a:[1],b:[2],p:3},{a:slots[0],b:slots[1],p:3}]){
 try{resolve(bad.a,bad.b,bad.p);throw Error('invalid accepted')}catch(e){ok(e.message.includes('bad pivot'),'bad pivots rejected')}
}
try{normalize([1,-1]);throw Error('tautological proof accepted')}catch(e){ok(e.message==='tautology','tautology rejected')}
ok(raw.assertions>=20000,'producer diagnostic count');
console.log(JSON.stringify({PASS:true,independent_assertions:assertions,original_producer_assertions:raw.assertions,odd_K4_models:raw.k4_controls.odd.models,even_K4_models:raw.k4_controls.even.models}));