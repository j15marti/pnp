#!/usr/bin/env node
'use strict';
// Independent structural checker for LSPV2/397 raw certificate. No imports except fs.
const fs=require('fs');let checked=0;
function key(c){return [...new Set(c)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y)}
function eq(a,b){return JSON.stringify(a)===JSON.stringify(b)}
function taut(c){return c.some(x=>c.includes(-x))}
function resolve(a,b,p){if(!a.includes(p)||!b.includes(-p)) throw Error('bad pivot');return key([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)])}
function verify(src,lines){let seen=src.map(key);for(let [a,b,p,c] of lines){if(a>=seen.length||b>=seen.length||a<0||b<0)throw Error('parent');if(taut(c)||!eq(resolve(seen[a],seen[b],p),key(c))) throw Error('resolution invalid');seen.push(key(c));checked++}if(!eq(seen[seen.length-1],[])) throw Error('not a refutation');return true}
function satisfiable(cs,n){for(let z=0;z<(1<<n);z++){if(cs.every(c=>c.some(l=>l>0? Boolean(z&(1<<(l-1))) : !Boolean(z&(1<<(-l-1))))))return true}return false}
let d=JSON.parse(fs.readFileSync(process.argv[2] || 'lspv2_397_raw.json','utf8'));
const source=d.sample_original_sources,original=d.sample_original_steps,lifted=d.sample_lifted_strict_resolution_steps;
verify(source,original);verify(source.slice(0,3),lifted);
if(satisfiable(source,3)||satisfiable(source.slice(0,3),2))throw Error('UNSAT control');
if(!satisfiable(source.slice(0,3).filter((_,i)=>i!==2),2))throw Error('SAT control');
for(let x=0;x<2;x++)for(let w=0;w<2;w++){
 let gateClause=source.slice(3);
 let y=x&&w;
 if(!gateClause.every(c=>c.some(l=>{let bits={1:x,2:w,3:Number(y)};return l>0?bits[l]:!bits[-l]})))throw Error('not conservative');checked++;
}
if(d.sample_lifted_cost!==lifted.length||d.sample_lifted_cost>2*(d.sample_cost+1)-1)throw Error('cost');
let rejected=0;for(const mutate of [a=>{a.sample_lifted_strict_resolution_steps[0][2]=3},a=>{a.sample_original_steps[0][2]=2},a=>{a.sample_lifted_strict_resolution_steps.pop()}]){
 let clone=JSON.parse(JSON.stringify(d));mutate(clone);
 try{verify(clone.sample_original_sources,clone.sample_original_steps);verify(clone.sample_original_sources.slice(0,3),clone.sample_lifted_strict_resolution_steps)}catch(_){rejected++}
}
if(rejected!==3)throw Error('mutations not rejected');
console.log(JSON.stringify({status:'PASS',strict_inferences_checked:checked,negative_controls_rejected:rejected,source_clause_count:source.length,lifted_cost:lifted.length,satisfiable_control:true},null,2));
