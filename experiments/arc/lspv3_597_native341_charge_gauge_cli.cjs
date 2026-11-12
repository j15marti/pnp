#!/usr/bin/env node
"use strict";
/*
 * LSPV-3/597: original /341 native edge-sign/charge gauge replay.
 * Node >=18; no dependencies.
 * Run from checkout:
 *   node experiments/arc/lspv3_597_native341_charge_gauge_cli.cjs [raw-results.json]
 *
 * This transforms certificates, not the checker. All 118 acceptance decisions
 * come from OS subprocesses running the byte-identical archived /341 checker.
 * Historical unified R_mix341 dispatcher and cross-rule ports remain UNKNOWN.
 */
const fs=require("node:fs");
const path=require("node:path");
const os=require("node:os");
const cp=require("node:child_process");
const crypto=require("node:crypto");
const assert=require("node:assert/strict");
const root=path.resolve(__dirname,"../..");
const checker=path.join(root,"experiments/arc/lspv2_341_independent_verify.js");
const seedPath=path.join(root,"results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json");
const checkerBlob="fcb7d4ced8f922de14c0bda16263a8cc7853e8e0";
const seedBlob="fe27fe1011d0021e721ccaeb747ed58da65d7464";
const sha256=b=>crypto.createHash("sha256").update(b).digest("hex");
const gitBlob=b=>crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+b.length+"\0"),b])).digest("hex");
const checkerBytes=fs.readFileSync(checker),seedBytes=fs.readFileSync(seedPath);
assert.equal(gitBlob(checkerBytes),checkerBlob,"checker Git blob drift");
assert.equal(gitBlob(seedBytes),seedBlob,"original fixture Git blob drift");
const fixtures=JSON.parse(seedBytes).fixtures;
const clone=x=>JSON.parse(JSON.stringify(x));
function gauge(original,indices){
 const f=clone(original),E=f.graph.edges.length,flip=new Set(indices);
 for(const e of flip){
  assert(Number.isSafeInteger(e)&&e>=0&&e<E,"edge mask bounds");
  const [u,v]=f.graph.edges[e];
  f.charges[u]^=1; f.charges[v]^=1;
 }
 for(const c of f.clauses){
  c.literals=c.literals.map(l=>flip.has(Math.abs(l)-1)?-l:l);
  c.pattern=c.literals.reduce((a,l,i)=>a+(l<0?2**i:0),0);
 }
 for(const p of f.proof){
  if(p.rule==="AND3"){
   let table=0;
   for(let m=0;m<2**p.support.length;m++){
    let old=m;
    for(let j=0;j<p.support.length;j++)
      if(flip.has(p.support[j]))old^=2**j;
    if(((p.table>>old)&1)!==0)table|=2**m;
   }
   p.table=table;
  }
  if(p.row){
   const mask=BigInt(p.row.mask);
   let delta=0;
   for(const e of flip)if(((mask>>BigInt(e))&1n)!==0n)delta^=1;
   p.row.rhs^=delta;
  }
 }
 for(const d of f.deleted){
  if(d.assignment!==null)d.assignment=d.assignment.split("")
    .map((bit,e)=>flip.has(e)?String(1-Number(bit)):bit).join("");
 }
 // The fixture's evenWitness tests the independent all-zero even-charge
 // system, not the odd-charge source. Keep it unchanged.
 return f;
}
function sampleSets(E){
 const a=[[],[0],[E-1],Array.from({length:E},(_,i)=>i)];
 for(let e=0;e<Math.min(5,E);e++)a.push([e]);
 const used=new Set();
 return a.filter(s=>{const k=s.join(",");if(used.has(k))return false;used.add(k);return true;});
}
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),"lspv3-597-"));
let count=0;
function native(f,label){
 const packet=JSON.stringify({fixtures:[f],summary:[null]});
 const file=path.join(tmp,"packet-"+count+++".json");
 fs.writeFileSync(file,packet);
 const result=cp.spawnSync(process.execPath,[checker,file],{encoding:"utf8",maxBuffer:16*1024*1024,timeout:120000});
 let checks=null;
 if(result.status===0){
  const o=JSON.parse(result.stdout);
  checks=o.checks;
 }
 return {label,accepted:result.status===0,checks,
  error:result.status===0?null:String(result.stderr||result.error||"unknown").trim().slice(-450),
  packet_sha256:sha256(Buffer.from(packet)),
  packet_bytes:Buffer.byteLength(packet)};
}
try {
 const cases=[],seen=new Set();
 for(let i=0;i<fixtures.length;i++){
  const f=fixtures[i],E=f.graph.edges.length;
  const ss=sampleSets(E);
  if(i===0)for(let m=0;m<2**E;m++)
   ss.push(Array.from({length:E},(_,j)=>j).filter(j=>((m>>j)&1)!==0));
  for(const indices of ss){
   const tag=f.graph.name+":"+indices.join(",");
   if(seen.has(tag))continue;
   seen.add(tag);
   const out=gauge(f,indices);
   assert.deepEqual(out.proof.map(r=>[r.id,r.rule,r.kind,r.parents]),
     f.proof.map(r=>[r.id,r.rule,r.kind,r.parents]));
   assert.equal(out.clauses.length,f.clauses.length);
   assert.equal(out.proof.length,f.proof.length);
   const v=native(out,tag);
   assert(v.accepted,"original /341 checker rejected "+tag+": "+v.error);
   cases.push({graph:f.graph.name,edges:E,mask:indices,paid:out.proof.length,
      charges:out.charges,...v});
  }
 }
 const p=gauge(fixtures[0],[0]);
 const attacks=[
  ["wrong_charge",d=>{d.charges[0]^=1}],
  ["wrong_table",d=>{d.proof[0].table^=1}],
  ["wrong_sink",d=>{d.proof.at(-1).row.rhs^=1}],
  ["wrong_deleted",d=>{d.deleted[0].assignment="000000"}],
  ["wrong_parent",d=>{d.proof[0].parents[0]="unknown-source"}],
  ["source_charge_uncoupled",d=>{d.charges=fixtures[0].charges.slice()}]
 ];
 const hostiles=attacks.map(([name,fn])=>{const f=clone(p);fn(f);
  const v=native(f,name);assert(!v.accepted,"original checker accepted hostile "+name);return v;});
 const orbit={group:"F2^E",K4_total_masks:64,
  K4_distinct_charge_vectors:new Set(cases.filter(x=>x.graph==="K4").map(x=>x.charges.join(""))).size,
  K4_same_charge_fiber_size:8};
 const raw={run:"LSPV-3/597",date:"2026-11-12 America/Los_Angeles",
  authority:"unchanged original archived /341 checker in fresh Node OS subprocesses",
  checker_git_blob:checkerBlob,seed_git_blob:seedBlob,
  scope:"SOURCE/AND3/XOR, NOT complete historical R_mix341",
  orbit,positives:cases.length,hostile_rejects:hostiles.length,
  original_positive_assertions:cases.reduce((a,c)=>a+c.checks,0),
  fixture_counts:fixtures.map(f=>({name:f.graph.name,edges:f.graph.edges.length,
    vertices:f.graph.n,paid:f.proof.length,accepted:cases.filter(c=>c.graph===f.graph.name).length})),
  cases,hostiles,limitations:[
   "native full R_mix341, RES-to-AND3, LOCAL-CONVERT, DEF, branching and discharge remain unauthenticated",
   "K4 mask space exhaustive; other fixtures have eight deterministic masks each",
   "OS runtime/RSS and certificate acquisition are not logical work"]
 };
 const output=JSON.stringify(raw,null,2)+"\n";
 if(process.argv[2])fs.writeFileSync(path.resolve(process.argv[2]),output);
 console.log(JSON.stringify({run:raw.run,positives:raw.positives,
 hostile_rejects:raw.hostile_rejects,original_positive_assertions:raw.original_positive_assertions,
 orbit,fixture_counts:raw.fixture_counts}));
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
