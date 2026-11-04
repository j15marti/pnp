#!/usr/bin/env node
// Independent signed-source and toy-machine checker. Node built-ins only.
'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const raw=JSON.parse(fs.readFileSync(path.join(__dirname,'lspv1_395_profile_raw.json'),'utf8'));
let tests=0;
const eq=(a,b,msg)=>{tests++;assert.deepEqual(a,b,msg)};
const expect=(x,msg)=>{tests++;assert.ok(x,msg)};
const template=(j)=>[[1],[-1],...Array.from({length:j},(_,k)=>[k+2,-k-2])];
const validate=(f)=>Array.isArray(f)&&f.every(row=>Array.isArray(row)&&row.every(x=>Number.isInteger(x)&&x!==0));
const signature=(f)=>JSON.stringify(f);
const next=(n,s)=>(n%3===0&&s>0)?s-1:s;
const checkFast=(n,seq)=>{
 if(!Array.isArray(seq)||seq.length<1||seq[0]!==n%9+1||seq[seq.length-1]!==0)return false;
 return seq.every((x,i)=>Number.isInteger(x)&&x>=0&&(i===0||next(n,seq[i-1])===x));
};
const checkSlow=(n,arr)=>Array.isArray(arr)&&arr.length===n+2&&arr.every((v,i)=>v===i+1);
const checkGeneric=(F,steps)=>{
 if(!validate(F)||!Array.isArray(steps)||steps.length===0)return false;
 const clauses=F.map(x=>new Set(x));
 for(const step of steps){
  if(!Number.isInteger(step.a)||!Number.isInteger(step.b)||!Number.isInteger(step.pivot))return false;
  if(step.pivot===0||step.a<0||step.a>=clauses.length||step.b<0||step.b>=clauses.length)return false;
  const aa=clauses[step.a],bb=clauses[step.b],p=step.pivot;
  if(!aa.has(p)||!bb.has(-p))return false;
  const v=new Set([...aa].filter(x=>x!==p).concat([...bb].filter(x=>x!==-p)));
  if([...v].some(x=>v.has(-x)))return false;
  const out=[...v].sort((a,b)=>a-b);
  if(JSON.stringify(out)!==JSON.stringify(step.out))return false;
  clauses.push(v);
 }
 return clauses.at(-1).size===0;
};
const check=(F,proof)=>{
 if(!validate(F)||typeof proof!=='object'||proof===null)return false;
 let n=F.length-2;
 const special=n>=0&&signature(F)===signature(template(n));
 if(!special)return proof.kind==='PACK'&&checkGeneric(F,proof.steps);
 if(proof.kind==='FAST')return checkFast(n,proof.trace);
 if(proof.kind==='SLOW')return checkSlow(n,proof.stages);
 return false;
};
let prefix=1,fast=0,slow=0;
eq(raw.test_records.length,20,'record count');
for(let idx=0;idx<raw.test_records.length;idx++){
 const r=raw.test_records[idx],n=idx+1;
 eq(r.n,n,'n contiguous');eq(r.source,template(n),'signed source');
 eq(r.source_clause_count,n+2,'source count');
 eq(r.toy_halts,n%3===0,'toy fixed machine');
 expect(check(r.source,{kind:'SLOW',stages:Array.from({length:n+2},(_,k)=>k+1)}),'valid chain');
 expect(!check(r.source,{kind:'SLOW',stages:Array.from({length:n+1},(_,k)=>k+1)}),'no short chain');
 expect(!check(r.source,{kind:'SLOW',stages:Array.from({length:n+2},(_,k)=>k+1).reverse()}),'no permuted chain');
 expect(!check(r.source,{kind:'PACK',steps:[{a:0,b:1,pivot:1,out:[]}]}),'no pack special');
 if(n%3===0){
   fast++;expect(checkFast(n,r.fast_trace),'valid fast');
   expect(check(r.source,{kind:'FAST',trace:r.fast_trace}),'auth fast');
   expect(!check(r.source,{kind:'FAST',trace:r.fast_trace.slice(0,-1).concat([7])}),'bad fast');
   eq(r.min_nodes,1,'fast optimum');
 }else{
   slow++;eq(r.fast_trace,null,'no fast witness');
   expect(!checkFast(n,[n%9+1,0]),'reject no proof');
   eq(r.min_nodes,n+2,'slow optimum');
 }
 prefix=Math.max(prefix,r.min_nodes);
 eq(r.prefix_wbar,prefix,'prefix maximum');
}
expect(check([[1],[-1],[2]],{kind:'PACK',steps:[{a:0,b:1,pivot:1,out:[]}]}),'generic pack proof');
expect(!check([[1]],{kind:'PACK',steps:[{a:0,b:0,pivot:1,out:[]}]}),'SAT blocked');
expect(!check([[0]],{kind:'PACK',steps:[{a:0,b:0,pivot:1,out:[]}]}),'malformed rejected');
expect(!check([[1],[-1],[2]],{kind:'PACK',steps:[{a:0,b:1,pivot:1,out:[1]}]}),'corrupt resolution rejected');
expect(!check(template(5),{kind:'FAST',trace:[6,0]}),'forged semantic fast rejected');
eq(fast,6);eq(slow,14);eq(prefix,22);
console.log(JSON.stringify({checks:tests,records:raw.test_records.length,fast,slow,prefix_wbar:prefix}));
