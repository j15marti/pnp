#!/usr/bin/env node
// Independently reconstruct signed sources, counts, hashes, parity facets.
// NOT the authoritative historical R_mix341 accepted-byte checker.
import fs from 'node:fs';
import crypto from 'node:crypto';
import assert from 'node:assert/strict';
const fname=process.argv[2]||'results/raw/arc/2026-11-06_LSPV3_460_RANDOM3_SOURCE_COLLISIONS.json';
const original=JSON.parse(fs.readFileSync(fname,'utf8'));
let checks=0;
function eq(a,b){assert.deepEqual(a,b);checks++;}
function ok(a){assert.ok(a);checks++;}
function stream(seed){
 let ctr=0n;const sb=Buffer.alloc(4);sb.writeUInt32BE(seed>>>0,0);
 return function bounded(n){
  let x;const bound=BigInt(n), lim=((1n<<64n)/bound)*bound;
  do{
   const cb=Buffer.alloc(8);cb.writeBigUInt64BE(ctr++);
   x=crypto.createHash('sha256').update(sb).update(cb).digest().readBigUInt64BE(0);
  }while(x>=lim);
  return Number(x%bound);
 };
}
function source(n,seed){
 const rand=stream(seed),cls=[];
 for(let k=0;k<8*n;k++){
  let ids=[];
  while(ids.length<3){
   const v=rand(n)+1;if(!ids.includes(v))ids.push(v);
  }
  ids.sort((a,b)=>a-b);
  const sign=rand(8);
  cls.push(ids.map((v,i)=>((sign>>>i)&1)?-v:v));
 }
 return cls;
}
function counts(cls){
 const h=new Map(),s=new Map();
 for(const c of cls){
  eq(c.length,3);eq(new Set(c.map(Math.abs)).size,3);
  const key=c.map(Math.abs).sort((a,b)=>a-b).join(',');
  h.set(key,(h.get(key)||0)+1);
  const sk=c.join(',');s.set(sk,(s.get(sk)||0)+1);
 }
 const pairs=x=>[...x.values()].reduce((a,k)=>a+k*(k-1)/2,0);
 return {pair_candidates_source_AND3:pairs(h),
  repeated_variable_triples:[...h.values()].filter(k=>k>1).length,
  max_triple_multiplicity:Math.max(0,...h.values()),
  duplicate_signed_source_pairs:pairs(s),distinct_variable_triples:h.size};
}
function hashSource(n,cls){
 let data='p cnf '+n+' '+cls.length+'\n';
 for(const c of cls)data+=c.join(' ')+' 0\n';
 return crypto.createHash('sha256').update(data,'ascii').digest('hex');
}
function checkAll(data){
 eq(data.results.length,16);
 const ns=[256,512,2048,8192],seeds=[11,23,47,89];
 for(const r of data.results){
  eq(r.m,8*r.n);ok(ns.includes(r.n));ok(seeds.includes(r.seed));
  const c=source(r.n,r.seed);
  eq(r.source_sha256,hashSource(r.n,c));
  const cc=counts(c);
  for(const [k,v] of Object.entries(cc))eq(r[k],v);
  const expected=r.m*(r.m-1)/2/(r.n*(r.n-1)*(r.n-2)/6);
  ok(Math.abs(expected-r.expected_collision_pairs_iid)<1e-10);
 }
 const P=data.forced_parity_control;
 eq(P.paid_AND3_nodes,3);eq(P.source_clauses.length,4);
 for(let t=0;t<8;t++){
  const truths=P.source_clauses.map(c=>c.some(l=>(((t>>(Math.abs(l)-1))&1)===(l>0?1:0))));
  const AND=(truths[0]&&truths[1])&&(truths[2]&&truths[3]);
  const ODD=((t&1)+((t>>1)&1)+((t>>2)&1))%2===1;
  eq(AND,ODD);
 }
 const cs=source(256,89),before=counts(cs).pair_candidates_source_AND3;
 const first=cs[0].map(Math.abs).sort((a,b)=>a-b).join(',');
 const occ=cs.filter(c=>c.map(Math.abs).sort((a,b)=>a-b).join(',')===first).length;
 cs.push(cs[0]);eq(counts(cs).pair_candidates_source_AND3-before,occ);
 eq(data.corrupted_control.actual_pair_increase,occ);
}
function immutableAudit(d){
 assert.equal(d.results.length,16);
 for(const row of d.results){
  const c=source(row.n,row.seed);
  assert.equal(row.source_sha256,hashSource(row.n,c));
  assert.equal(row.pair_candidates_source_AND3,counts(c).pair_candidates_source_AND3);
 }
 for(let t=0;t<8;t++){
  const sat=d.forced_parity_control.source_clauses.every(c=>c.some(l=>((t>>(Math.abs(l)-1))&1)==(l>0?1:0)));
  const odd=((t&1)+((t>>1)&1)+((t>>2)&1))%2===1;
  assert.equal(sat,odd);
 }
}
checkAll(original);
const variants=[
 d=>{d.results[0].source_sha256='0'.repeat(64);},
 d=>{d.results[0].pair_candidates_source_AND3++;},
 d=>{d.forced_parity_control.source_clauses[0][0]*=-1;},
 d=>{d.results.pop();}
];
for(const corrupt of variants){
 const d=structuredClone(original);corrupt(d);
 assert.throws(()=>immutableAudit(d));checks++;
}
console.log(JSON.stringify({pass:true,independent_assertion_groups:checks,
  hostile_controls_rejected:4,instances:original.results.length}));
