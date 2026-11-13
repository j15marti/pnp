#!/usr/bin/env node
'use strict';
// LSPV-3/610: independent mathematical enumeration of the EXACT SOURCE
// validation predicate extracted from the archived /341 checker.
// This is NOT execution of the unchanged /341 checker and NOT a complete
// R_mix341 proof checker. Run: node lspv3_610_native341_source_fiber.cjs
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const E = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const V=4;
const incidence=Array.from({length:V},(_,v)=>E.map(([a,b],i)=>a===v||b===v?i:-1).filter(x=>x>=0));
const allPatterns=Array.from({length:8},(_,p)=>p);
const parity3=p=> ((p&1)^((p>>1)&1)^((p>>2)&1));
let checks=0;
const ck=(test,msg)=>{checks++;assert.ok(test,msg)};
function choose4(arr){const ret=[];for(let a=0;a<5;a++)for(let b=a+1;b<6;b++)for(let c=b+1;c<7;c++)for(let d=c+1;d<8;d++)ret.push([a,b,c,d]);return ret;}
function clause(v,pattern){return incidence[v].map((e,j)=>((pattern>>j)&1)?-(e+1):e+1);}
function patternOf(clause,inc){return inc.reduce((acc,e,i)=> acc|((clause.find(x=>Math.abs(x)===e+1)<0)?(1<<i):0),0);}
function makeSource(S,charge0=true){const q=[charge0,0,0,0],clauses=[];for(let v=0;v<V;v++){
 const forb=v===0?S:allPatterns.filter(p=>parity3(p)===1);
 for(const p of forb)clauses.push({id:'s'+clauses.length,vertex:v,literals:clause(v,p)});
}return {graph:{n:V,edges:E},charges:q,clauses};}
// Independent reenactment of logical tests appearing in recovered /341 SOURCE
// prefix. Compared by inspection with pinned source blob fcb7d4c....
function sourcePrefix(s){
 if(s.charges.length!==V) return false;
 if(s.charges.reduce((x,y)=>x^y,0)!==1) return false;
 if(s.clauses.length!==4*V)return false;
 const used=new Set(),byV=Array.from({length:V},()=>new Set());
 for(const c of s.clauses){
  if(!Number.isInteger(c.vertex)||c.vertex<0||c.vertex>=V||used.has(c.id)||c.literals.length!==3)return false;
  used.add(c.id);
  const inc=incidence[c.vertex],k=c.literals.map(x=>Math.abs(x)-1).sort((a,b)=>a-b);
  if(k.join(',')!==inc.slice().sort((a,b)=>a-b).join(','))return false;
  const parity=c.literals.map(x=>x<0?1:0).reduce((x,y)=>x^y,0);
  if(!(parity!==s.charges[c.vertex]))return false;
  const pat=patternOf(c.literals,inc),key=Array.from({length:3},(_,j)=>(pat>>j)&1).join('');
  if(byV[c.vertex].has(key))return false;
  byV[c.vertex].add(key);
 }
 return byV.every(s=>s.size===4);
}
function satCount(source){let n=0;const models=[];for(let x=0;x<(1<<E.length);x++){
 let good=source.clauses.every(c=>c.literals.some(l=>((x>>(Math.abs(l)-1))&1)===(l>0?1:0)));
 if(good){n++;models.push(x.toString(2).padStart(E.length,'0'));}
}return {n,models}}
const combos=choose4(allPatterns);
ck(combos.length===70,'choose(8,4)');
const stats={};const sample={};const hashed=[];
for(const S of combos){
 const b=makeSource(S,true),k=S.filter(p=>parity3(p)===0).length;
 ck(sourcePrefix(b),'Boolean-charge SOURCE must accept any four distinct patterns');
 const models=satCount(b);ck(models.n===2*(4-k),'K4 exact source count');
 if(!stats[k])stats[k]={pattern_sets:0,model_count:models.n};
 stats[k].pattern_sets++;
 if(!sample[k])sample[k]={forbidden_patterns:S,first_model:models.models[0]||null,models:models.n};
 hashed.push(JSON.stringify(b.clauses));
 const canonical=makeSource(S,1);
 ck(sourcePrefix(canonical)===(k===4),'numeric charge must admit exactly one parity set');
}
ck(stats[0].pattern_sets===1&&stats[0].model_count===8,'k0');
ck(stats[1].pattern_sets===16&&stats[1].model_count===6,'k1');
ck(stats[2].pattern_sets===36&&stats[2].model_count===4,'k2');
ck(stats[3].pattern_sets===16&&stats[3].model_count===2,'k3');
ck(stats[4].pattern_sets===1&&stats[4].model_count===0,'k4');
ck(Object.values(stats).reduce((a,b)=>a+b.pattern_sets,0)===70,'distribution');
let rejections=0;
const badCases=[
 s=>{s.charges=[false,0,0,0]},
 s=>{s.charges=[2,0,0,0]},
 s=>{s.clauses.pop()},
 s=>{s.clauses[1].literals=s.clauses[0].literals.slice()},
 s=>{s.clauses[0].literals[0]=999},
 s=>{s.clauses[0].vertex=44},
 s=>{s.clauses[0].id=s.clauses[1].id},
];
const valid=makeSource([0,1,2,3],true);
for(const mutate of badCases){const clone=structuredClone(valid);mutate(clone);ck(!sourcePrefix(clone),'hostile near-miss rejected');rejections++}
const output={schema:'LSPV3-610-NATIVE341-SOURCE-PREFIX-FIBER/v1',date_local:'2026-11-13 02:24 PST',
 mode:'independent exact SOURCE-prefix reenactment + exhaustive K4 signed-source models, NOT unchanged original OS checker',
 original_checker_git_blob:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
 fixed_graph:'K4',vertices:V,edge_variables:E.length,source_clause_count:4*V,
 charge_vector:[true,0,0,0],charge_reduction_js32:1,
 alternative_forbidden_sets:combos.length,source_passes_boolean:70,source_passes_canonical_numeric_one:1,
 satisfiable_source_variants:69,unsatisfiable_source_variants:1,
 distribution_by_number_of_even_forbidden_patterns:stats,examples:sample,
 exact_logical_cnf_serializations_sha256:crypto.createHash('sha256').update(hashed.join('\n')).digest('hex'),
 hostile_near_misses_rejected:rejections,assertions:checks,
 scope:'No inference proof produced or replayed. Full /341 terminal acceptance only known from separate previously published sibling evidence. R_mix341 remains unauthenticated.'};
console.log(JSON.stringify(output,null,2));
