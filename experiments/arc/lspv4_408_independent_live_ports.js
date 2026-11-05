#!/usr/bin/env node
/* LSPV-4/408 independent semantic live-port verifier.
   Runs against archived original/normalized JSON fixtures.
   This tests a declared fragment, NOT native R_mix341.
*/
'use strict';
const fs=require('fs'),assert=require('assert');
const [a,b]=process.argv.slice(2);
if(!a||!b)throw Error('usage: node script.js old.json normalized.json');
const old=JSON.parse(fs.readFileSync(a,'utf8'));
const neo=JSON.parse(fs.readFileSync(b,'utf8'));
const original=new Map(old.ports.map((p,i)=>[p.name,{gate:p.gate,id:i}]));
const indexed=new Map(neo.ports.map((p,i)=>[p.name,i]));
let checks=0;
function compute(net,input){
 const v=input.slice();
 for(const rec of net){
  if(!Array.isArray(rec)||rec.length!==3)throw Error('bad gate tuple');
  const [m,x,y]=rec;
  if(!Number.isInteger(m)||m<0||m>15||![x,y].every(j=>Number.isInteger(j)&&j>=0&&j<v.length))throw Error('malformed or forward gate');
  v.push((m>>((v[x]<<1)|v[y]))&1);
 }
 return v;
}
function cnf(C,x){return C.every(c=>c.some(lit=>lit>0?x[lit-1]:!x[-lit-1]));}
for(let k=0;k<8;k++){
 const x=[k&1,(k>>1)&1,(k>>2)&1], o=compute(old.net,x);
 const n=neo.ports.map(p=>compute(p.circuit,x).at(-1));
 old.ports.forEach((p,i)=>{assert.strictEqual(o[p.gate],n[i]);checks++});
 old.consumers.forEach((rec,i)=>{
  const r=neo.consumers[i];assert.strictEqual(rec.rule,r.rule);checks++;
  for(let j=0;j<2;j++){
   assert.strictEqual(o[original.get(rec.refs[j]).gate]^rec.neg[j],n[indexed.get(r.refs[j])]^r.neg[j]);checks++;
  }
 });
 assert.strictEqual(cnf(old.source.sat,x),cnf(neo.source.sat,x));checks++;
 assert.strictEqual(cnf(old.source.unsat,x),false);checks++;
}
for(const bad of [[[16,0,0]],[[-1,0,0]],[[8,3,0]],[[4,0,4]]]){assert.throws(()=>compute(bad,[0,0,0]));checks++}
assert.strictEqual(old.ports.length,32);checks++;
assert.strictEqual(neo.ports.length,32);checks++;
assert.ok(old.ports.some(p=>p.name.length>700));checks++;
assert.ok(neo.ports.every((p,i)=>p.name==='p'+(i+1)));checks++;
assert.strictEqual(new Set(neo.ports.map(p=>p.name)).size,neo.ports.length);checks++;
console.log(JSON.stringify({status:'PASS',assertions:checks,port_count:32,consumer_count:16,rows:8,native_calculus_claim:false}));
