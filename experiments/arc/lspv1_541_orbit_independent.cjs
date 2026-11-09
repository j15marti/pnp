'use strict';
// LSPV-1/541 independent test. Restricted RES plus unused paid DEF only.
// Not an accepted-byte check of historical R_mix341.
const assert = require('node:assert/strict');
const src = [[1],[-1,2],[-2,3],[-3],[-2,4],[-4]];
const proof = (a,b) => [
 {id:6,rule:'DEF',out:a,op:'XOR',inputs:[1,2],ctx:[]},
 {id:7,rule:'DEF',out:b,op:'AND',inputs:[a,3],ctx:[]},
 {id:8,rule:'RES',parents:[0,1],pivot:1,conclusion:[2],ctx:[]},
 {id:9,rule:'RES',parents:[8,2],pivot:2,conclusion:[3],ctx:[]},
 {id:10,rule:'RES',parents:[9,3],pivot:3,conclusion:[],ctx:[]},
 {id:11,rule:'RES',parents:[8,4],pivot:2,conclusion:[4],ctx:[]},
 {id:12,rule:'RES',parents:[11,5],pivot:4,conclusion:[],ctx:[]}
];
const norm = a => [...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||y-x);
const equal = (a,b) => JSON.stringify(a)===JSON.stringify(b);
function verify(p) {
 const known = new Map(src.map((c,i)=>[i,norm(c)]));
 const used = new Set([1,2,3,4]);
 let count=0;
 for (const r of p) {
  assert(!known.has(r.id) && r.id>=src.length);
  assert.deepEqual(r.ctx,[]);
  if (r.rule==='DEF') {
   assert(r.out>4 && !used.has(r.out));
   assert(r.inputs.length===2 && r.inputs.every(x=>used.has(x)));
   used.add(r.out);known.set(r.id,null);
  } else {
   assert.equal(r.rule,'RES');
   const [left,right]=r.parents.map(id=>known.get(id));
   assert(Array.isArray(left) && Array.isArray(right));
   assert(left.includes(r.pivot) && right.includes(-r.pivot));
   const out=norm([...left.filter(x=>x!==r.pivot),...right.filter(x=>x!==-r.pivot)]);
   assert(out.every(x=>!out.includes(-x)));
   assert(equal(out,norm(r.conclusion)));
   known.set(r.id,out);
  }
  count++;
 }
 assert.equal(count,7);
 assert(equal(known.get(10),[]) && equal(known.get(12),[]));
 return true;
}
function canonical(p) {
 const map=new Map();
 return p.map(r=>{
  const x=structuredClone(r);
  if(x.rule==='DEF') {
   x.inputs=x.inputs.map(v=>map.get(v)??v);
   assert(!map.has(x.out) && x.out>4);
   map.set(x.out,5+map.size);x.out=map.get(x.out);
  } else {
   x.pivot=map.get(x.pivot)??x.pivot;
   x.conclusion=x.conclusion.map(v=>Math.sign(v)*(map.get(Math.abs(v))??Math.abs(v)));
  }
  return x;
 });
}
let checks=0,seed=541;
function random() {seed=(Math.imul(seed,1664525)+1013904223)>>>0;return 5+(seed%2147483000)}
const base=canonical(proof(101,50007));
for(let i=0;i<3000;i++) {
 const a=random();let b=random();if(b===a)b++;
 const p=proof(a,b);
 assert(verify(p));assert(equal(canonical(p),base));checks+=2;
}
for(const edit of [
 t=>{t[0].out=3},t=>{t[1].inputs=[999,3]},
 t=>{t[2].pivot=2},t=>{t[3].conclusion=[-3]},
 t=>{t[4].parents=[6,3]},t=>{t[5].id=8},
 t=>{t[3].ctx=[4]}
]) {
 const t=proof(101,102);edit(t);
 assert.throws(()=>verify(t));checks++;
}
console.log(JSON.stringify({status:'PASS',role:'LSPV-1/541',checks,renamed_traces:3000,
  negative_controls:7,paid_nodes:7,source_clauses:6,goals:[10,12],
  native_historical_checker:false}));
