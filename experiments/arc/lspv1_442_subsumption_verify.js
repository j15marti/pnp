#!/usr/bin/env node
'use strict';
// LSPV-1/442: independent reconstruction of /440 strict-RES port + missing-facet bypass.
// This compact public replay is NOT the full 17-node certificate checker.
// Full producer/independent checker/raw proof are in the user-facing reproducibility ZIP.
const assert=require('assert');
const lit=(vars,b)=>vars.map((v,i)=>(b>>i&1)?-v:v);
const norm=a=>[...new Set(a)].sort((a,b)=>Math.abs(a)-Math.abs(b)||b-a);
const key=a=>JSON.stringify(norm(a));
const models=clauses=>Array.from({length:32},(_,i)=>i).filter(m=>clauses.every(c=>c.some(l=>Boolean(m>>(Math.abs(l)-1)&1)===(l>0))));
const resolve=(a,b,p)=>{assert(a.includes(p)&&b.includes(-p));return norm([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)])};
let checks=0;const ok=(x)=>{assert(x);checks++};
const U=[];for(let b=0;b<8;b++)if(((b&1)^((b>>1)&1)^((b>>2)&1))===0)U.push(norm([1,...lit([2,3,4],b)]));
for(const i of [2,3,4])U.push(norm([-1,-i]));
const X=[];for(let b=0;b<8;b++)if(((b&1)^((b>>1)&1)^((b>>2)&1))===1)X.push(norm(lit([2,3,5],b)));
const R=[],Q=[];for(let b=0;b<8;b++){const c=norm(lit([1,4,5],b));if(((b&1)^((b>>1)&1)^((b>>2)&1))===0)R.push(c);else Q.push(c)}
const F=[...U,...X];ok(F.length===11);ok(models(F).length===5);ok(models([...F,...Q]).length===0);
const C=new Map(F.map(c=>[key(c),c]));let rounds=0;
while(true){let old=[...C.values()],adds=0;for(let i=0;i<old.length;i++)for(let j=i+1;j<old.length;j++)for(const p of old[i]){
if(!old[j].includes(-p))continue;let r=resolve(old[i],old[j],p);if(r.some(x=>r.includes(-x))||C.has(key(r)))continue;C.set(key(r),r);adds++}
rounds++;if(!adds)break;ok(rounds<8)}
ok(C.size===87);const missing=norm([-1,-4,5]),strong=norm([-1,-4]);
ok(!C.has(key(missing)));ok(F.some(c=>key(c)===key(strong)));ok(R.filter(c=>!C.has(key(c))).length===1);
ok(R.filter(c=>!C.has(key(c))).every(c=>key(c)===key(missing)));
// Explicit strict-RES suffix, one omitted z-pivot due to already stronger clause.
const get=a=>C.get(key(a))||Q.find(c=>key(c)===key(a));
const emit=(a,b,p,expect)=>{let x=resolve(a,b,p);ok(key(x)===key(expect));return x};
const aa=emit(get([1,4,5]),get([1,4,-5]),5,[1,4]);
const ab=emit(get([1,-4,5]),get([1,-4,-5]),5,[1,-4]);
const ba=emit(get([-1,4,5]),get([-1,4,-5]),5,[-1,4]);
const one=emit(aa,ab,4,[1]);
const zero=emit(ba,strong,4,[-1]);
const empty=emit(one,zero,1,[]);
ok(empty.length===0);
const result={id:'LSPV1_442_PORT',closure:87,models_before:5,models_after:0,canonical_join_steps:7,strict_join_steps:6,independent_assertions:checks,verified:true};
console.log(JSON.stringify(result));
