#!/usr/bin/env node
"use strict";
// LSPV-1/576: exact 10-vertex bridge source-minimum and native /386 binary cost floor.
// No dependencies beyond Node.js 18+ standard library.
// Run from the repository root:
//   node experiments/arc/lspv1_576_bridge_exact_core_lower.cjs
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const cp = require("node:child_process");
const crypto = require("node:crypto");

const EDGES = [[0,3],[0,4],[1,2],[1,3],[1,4],[2,3],[2,4],
  [5,8],[5,9],[6,7],[6,8],[6,9],[7,8],[7,9],[0,5]];
const CHARGE = [1,0,0,0,0,0,0,0,0,0];
const GUARD = 16;
const occ = Array.from({length:10},()=>[]);
for (let e=0;e<EDGES.length;e++) for(const v of EDGES[e]) occ[v].push(e+1);
assert(occ.every(o=>o.length===3),"cubic incidence");

function canonical(c) { return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b); }
const rows=[];
for(let v=0;v<10;v++) for(let bits=0;bits<8;bits++){
  const parity = ((bits&1)+((bits>>1)&1)+((bits>>2)&1))%2;
  if(parity===CHARGE[v]) continue;
  const clause=canonical([...occ[v].map((e,i)=>((bits>>i)&1)?-e:e),-GUARD]);
  rows.push({vertex:v,pattern:bits,c:clause});
}
assert.equal(rows.length,40);
const source=[...rows.map(r=>r.c),[GUARD]];
function sat(c,mask,guard=true){
  return c.some(l=>{const b=(Math.abs(l)===GUARD)?Number(guard):((mask>>(Math.abs(l)-1))&1);return (l>0)===Boolean(b);});
}
const singleton={};const histogram={};let coreModels=0;
for(let mask=0;mask<(1<<15);mask++){
  const violated=[];
  for(let i=0;i<40;i++) if(!sat(rows[i].c,mask)) violated.push(i);
  histogram[violated.length]=(histogram[violated.length]||0)+1;
  if(violated.length===1 && singleton[violated[0]]===undefined) singleton[violated[0]]=mask;
}
const essential=Object.keys(singleton).map(Number).sort((a,b)=>a-b);
const inessential=Array.from({length:40},(_,i)=>i).filter(i=>singleton[i]===undefined);
assert.equal(essential.length,36);
assert.equal(inessential.length,4);
for(let mask=0;mask<(1<<15);mask++)
  if(essential.every(i=>sat(rows[i].c,mask)))coreModels++;
assert.equal(coreModels,0,"36-clause core must be UNSAT");
for(const i of essential){
  const a=singleton[i];
  assert(!sat(rows[i].c,a));
  assert(rows.every((r,j)=>j===i || sat(r.c,a)),"witness uniquely violates its clause");
}
assert(source.every(c=>sat(c,0,false))===false,"guard unit should fail when guard=false");
assert(rows.every(r=>sat(r.c,0,false)),"all vertex guards must be true when guard=false");

// Symbolic bridge check: left total vertex charge odd; right even.
// For any chosen bridge value, the selected 36 clauses forbid a mismatch on the
// component whose boundary/parity forces a mismatch.
const leftCharge=CHARGE.slice(0,5).reduce((a,b)=>a^b,0);
const rightCharge=CHARGE.slice(5).reduce((a,b)=>a^b,0);
assert.equal(leftCharge,1);assert.equal(rightCharge,0);
assert.equal(EDGES[14].join(","),"0,5");
for (const t of [0,1]){
  const forced = t===0?0:5;
  assert(rows.filter((r,i)=>essential.includes(i)&&r.vertex===forced).length===2);
}
function graphMinusConnected(vertex){
  const seen=new Set(),queue=[];
  let start=0;while(start===vertex)start++;
  queue.push(start);seen.add(start);
  while(queue.length){
    const u=queue.shift();
    for(const [a,b] of EDGES){
      const w=a===u?b:b===u?a:-1;
      if(w>=0&&w!==vertex&&!seen.has(w)){seen.add(w);queue.push(w);}
    }
  }
  return seen.size===9;
}
assert([0,5].every(v=>!graphMinusConnected(v)));
assert([1,2,3,4,6,7,8,9].every(graphMinusConnected));

const packetPath=path.resolve("results/raw/arc/2026-11-11_0900_LSPV1_575_BRIDGE_GUARDED_DP_NATIVE_ACCEPTED.json");
const verifierPath=path.resolve("experiments/arc/lspv2_386_independent_verify.js");
let originalChecker=null;
if(fs.existsSync(packetPath) && fs.existsSync(verifierPath)){
  const p=JSON.parse(fs.readFileSync(packetPath,"utf8"));
  const nativeRows=p.records.filter(r=>r.kind==="SOURCE");
  const key=r=>JSON.stringify(r.c);
  assert.deepEqual(nativeRows.map(key).sort(),source.map(key).sort(),"native source multiset changed");
  const visited=new Set(),todo=[p.records.length-1];
  while(todo.length){const i=todo.pop();if(visited.has(i))continue;visited.add(i);
    for(const k of p.records[i].parents||[])todo.push(k);
  }
  const dead=nativeRows.map(r=>p.records.indexOf(r)).filter(i=>!visited.has(i));
  assert.equal(dead.length,4);
  const deadKeys=dead.map(i=>key(p.records[i])).sort();
  assert.deepEqual(deadKeys,inessential.map(i=>key({c:rows[i].c})).sort(),
    "native dead clause identities differ from mathematical dispensable set");
  const checker=crypto.createHash("sha1").update(fs.readFileSync(verifierPath)).digest("hex");
  assert.equal(checker,"338305c0ce101704205e57543756b8127074a986");
  const run=cp.spawnSync(process.execPath,[verifierPath,packetPath],{
    encoding:"utf8",maxBuffer:1<<20,timeout:20000
  });
  assert.equal(run.status,0,run.stderr);
  const out=JSON.parse(run.stdout.trim().split(/\n/).at(-1));
  assert.equal(out.paid,63);assert.equal(out.res,62);assert.equal(out.def,1);
  assert.equal(out.sources,41);assert.equal(out.negativeTests,11);
  originalChecker={status:"ACCEPT",res:out.res,paid:out.paid,negativeTests:out.negativeTests,
    originalAssertionGroups:out.assertions,deadSourceRecords:dead,
    packet_sha256:out.sha256,checker_git_blob:checker};
}
const evidence={
  id:"LSPV-1/576",status:"PROVED/RESTRICTED plus COMPUTATIONAL",
  scope:"Original archived /386 SOURCE/paid-AND2/DEF/RES checker; not R_mix341",
  graph:EDGES,charge:CHARGE,guard:GUARD,
  enumeration:"At each vertex, local pattern bits 0..7 ascending; retain parity-wrong patterns; clause signed by forbidden assignment.",
  sourceClauseCount:41,
  indispensableSourceOrdinals0Based:essential,
  dispensableSourceOrdinals0Based:inessential,
  indispensableSourceIdentity:essential.map(i=>({vertex:rows[i].vertex,c:rows[i].c})),
  singletonWitnessMasks:singleton,
  histogramAssignmentsByNumberOfViolatedVertexClauses:histogram,
  totalEdgeAssignments:1<<15,coreModels,
  minimumUnsatSourceClausesIncludingGuard:37,
  universalNativeBinaryResLowerBound:36,
  universalNativeCorePaidWorkLowerBound:36,
  universalNativeCLIPaidWorkLowerBound:37,
  publishedNativeCorePaidWorkUpperBound:62,
  publishedNativeCLIPaidWorkUpperBound:63,
  originalChecker,
  limitations:["A finite-instance lower bound only","No optimum proven",
    "No authenticated full historical R_mix341 dispatcher","No SAT machine time lower bound"]
};
const json=JSON.stringify(evidence,null,2)+"\n";
if(process.argv.includes("--write-raw")){
  const out=path.resolve("results/raw/arc/2026-11-11_0957_LSPV1_576_BRIDGE_EXACT_CORE_LOWER_RAW.json");
  fs.mkdirSync(path.dirname(out),{recursive:true});fs.writeFileSync(out,json);
}
console.log(json);
