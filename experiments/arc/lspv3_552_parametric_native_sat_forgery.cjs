#!/usr/bin/env node
"use strict";
/* LSPV-3/552. Parametric SAT-source packets accepted by the unchanged
 * recovered /341 SOURCE/AND3/XOR *fixture* verifier.
 * Not a full historical R_mix341 checker. Run from repository root:
 *   node experiments/arc/lspv3_552_parametric_native_sat_forgery.cjs [raw.json] [V14-packet.json]
 */
const fs=require("node:fs"), crypto=require("node:crypto"), assert=require("node:assert/strict");
const producerPath="experiments/arc/lspv2_341_mixed_tseitin_min_dag.js";
const checkerPath="experiments/arc/lspv2_341_independent_verify.js";
const oldPacketPath="results/raw/arc/2026-11-10_1224_LSPV3_551_ACCEPTED_SAT_PACKET.json";
function sha1Blob(s){return crypto.createHash("sha1").update("blob "+Buffer.byteLength(s)+"\0"+s).digest("hex");}
const producer=fs.readFileSync(producerPath,"utf8");
const checker=fs.readFileSync(checkerPath,"utf8");
const oldPacket=fs.readFileSync(oldPacketPath,"utf8");
assert.equal(sha1Blob(producer),"4081022e8a3841d79f751a3d3a7a10decbb026da");
assert.equal(sha1Blob(checker),"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0");
assert.equal(sha1Blob(oldPacket),"706947c767361e7c979b8208677eb983d33838f4");
const copy=x=>JSON.parse(JSON.stringify(x));
const baseline=JSON.parse(oldPacket).fixtures[1];
function expand(g){
  const edges=g.edges.map(e=>e.slice()),u=8,a=g.n,z=g.n+1;
  const inc=edges.map((e,i)=>e.includes(u)?i:-1).filter(i=>i>=0);
  assert.equal(inc.length,3);
  edges[inc[1]]=edges[inc[1]].map(x=>x===u?a:x);
  edges[inc[2]]=edges[inc[2]].map(x=>x===u?z:x);
  edges.push([u,a],[a,z],[z,u]);
  return{name:"ATTACK_"+(g.n+2),n:g.n+2,edges};
}
function connected(g,skip=-1){
  const seen=new Set([0]),todo=[0];
  for(let k=0;k<todo.length;k++)
    for(let i=0;i<g.edges.length;i++)if(i!==skip){
      const [a,b]=g.edges[i],v=a===todo[k]?b:b===todo[k]?a:-1;
      if(v>=0&&!seen.has(v)){seen.add(v);todo.push(v);}
    }
  return seen.size===g.n;
}
let graphs=[],g=copy(baseline.graph);
for(let t=0;t<6;t++){g.name="ATTACK_"+g.n;graphs.push(copy(g));g=expand(g);}
const prodI="return all;\n}",prodPatch="for(const g of "+JSON.stringify(graphs)+") all.push(g);\nreturn all;\n}";
assert(producer.includes(prodI));
const prodBody=producer.replace(prodI,prodPatch).replace(
  "if(typeof console!== 'undefined') console.log(JSON.stringify(data,null,2));","return data;");
const made=new Function(prodBody)();
const readI="const fs=require('fs'); const data=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));";
const checkI="console.log(JSON.stringify(verify(data),null,2));";
assert(checker.includes(readI)&&checker.includes(checkI));
const check=new Function("data",checker.replace(readI,"").replace(checkI,"return verify(data);"));
const rows=[];
let v14packet=null;
for(let t=0;t<graphs.length;t++){
  const f=copy(made.fixtures[7+t]);
  for(let j=0;j<4;j++)f.clauses[j].literals=copy(baseline.clauses[j].literals);
  f.charges[0]="1";
  f.proof[0].table=238;f.proof[1].table=230;
  f.proof[2].table=102;f.proof[2].support="012";
  f.deleted=f.clauses.map(c=>({sourceId:c.id,assignment:null}));
  f.properties.essential=0;
  const packet={fixtures:[made.fixtures[0],f],summary:[made.summary[0],made.summary[7+t]]};
  const w=Array(f.graph.edges.length).fill(0);for(const i of [0,2,5,12])w[i]=1;
  assert.equal(f.graph.n,12+2*t);
  assert.equal(f.graph.edges.length,18+3*t);
  assert(connected(f.graph)&&!connected(f.graph,17));
  assert.deepEqual(f.graph.edges.map((e,i)=>e.includes(0)?i:-1).filter(i=>i>=0),[0,1,12]);
  assert(f.graph.edges.every(([a,b])=>a!==b));
  assert.equal(new Set(f.graph.edges.map(e=>e.slice().sort((a,b)=>a-b).join(":"))).size,f.graph.edges.length);
  assert(Array.from({length:f.graph.n},(_,v)=>f.graph.edges.filter(e=>e.includes(v)).length).every(x=>x===3));
  assert(Array.from({length:f.graph.n},(_,v)=>f.graph.edges.reduce((s,e,i)=>s+(e.includes(v)?w[i]:0),0)%2).every(x=>x===0));
  const sat=c=>c.literals.some(x=>w[Math.abs(x)-1]===(x>0?1:0));
  assert.equal(f.clauses.filter(sat).length,4*f.graph.n);
  assert.equal(w[0]^w[1],1);
  assert.equal(w[0]^w[1]^w[12],0);
  function run(q){try{return{accepted:true,checks:check(q).checks};}catch(e){return{accepted:false,reason:String(e.message)};}}
  const positive=run(packet);assert(positive.accepted);
  const negatives={};
  for(const [kind,mut] of [
    ["canonical_charge",q=>q.fixtures[1].charges[0]=1],
    ["typed_support",q=>q.fixtures[1].proof[2].support=[0,1,12]],
    ["wrong_table",q=>q.fixtures[1].proof[2].table^=1],
    ["wrong_sink",q=>q.fixtures[1].proof.at(-1).row.rhs^=1],
    ["bad_source",q=>q.fixtures[1].clauses[0].literals[0]=999]
  ]){const q=copy(packet);mut(q);negatives[kind]=run(q);assert(!negatives[kind].accepted);}
  if(t===1)v14packet=packet;
  rows.push({t,vertices:f.graph.n,variables:f.graph.edges.length,clauses:f.clauses.length,
    paid_records:f.proof.length,satisfying_assignment:w.join(""),satisfied_original_clauses:f.clauses.length,
    native:positive,negative_controls:negatives});
}
const result={role:"LSPV-3/552",date:"2026-11-10 PST",
  model:"pinned recovered SOURCE/AND3/XOR fixture checker, not complete R_mix341",
  sourceGitBlob:{producer:sha1Blob(producer),checker:sha1Blob(checker),basePacket:sha1Blob(oldPacket)},
  theorem:"parametric SAT-source acceptance at V=12+2t,E=18+3t,4V clauses,4V-1 records, subject to JS runtime capacity",
  minimality:"within cubic proper signed numeric source packets the checker exhaustive E<=15 guard rules out SAT; E divisible by 3",
  rows,validation:"six original checker V8 positives, thirty original checker V8 negatives, independently witnessed SAT",
  caveat:"P2-D1/P2-C3/P2-B1/P2-B2 OPEN, no historical full parser"};
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+"\n");
if(process.argv[3])fs.writeFileSync(process.argv[3],JSON.stringify(v14packet,null,2)+"\n");
console.log(JSON.stringify(result,null,2));