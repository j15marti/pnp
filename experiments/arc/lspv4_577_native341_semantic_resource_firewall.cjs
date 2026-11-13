#!/usr/bin/env node
"use strict";
// LSPV-4/577: independent semantic cut and original-OS-checker resource ledger.
// Archived /341 SOURCE/AND3/XOR fixture grammar ONLY, not historical R_mix341.
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto"),os=require("node:os"),cp=require("node:child_process"),assert=require("node:assert/strict");
const root=path.resolve(__dirname,"../..");
const artifact="results/raw/arc/2026-11-12_2100_LSPV1_609_BRIDGE_SLICE_SAT_ACCEPTED.json",checker="experiments/arc/lspv2_341_independent_verify.js";
const bytes=fs.readFileSync(path.join(root,artifact)),ck=fs.readFileSync(path.join(root,checker));
const blob=x=>crypto.createHash("sha1").update("blob "+x.length+"\0").update(x).digest("hex");
assert.equal(blob(bytes),"8d6d9bc7f2940a77edf2a07fcb72af111ba5b928");
assert.equal(blob(ck),"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0");
const data=JSON.parse(bytes.toString("utf8")),f=data.fixtures[0],E=f.graph.edges.length,V=f.graph.n;
assert.equal(E,18);assert.equal(V,12);assert.equal(f.clauses.length,48);
const sat=(c,b)=>c.literals.some(l=>l>0?b[l-1]===1:b[-l-1]===0);
const models=[];
for(let x=0;x<(1<<E);x++){
 const b=Array.from({length:E},(_,j)=>(x>>j)&1);
 if(f.clauses.every(c=>sat(c,b)))models.push(b);
}
assert.equal(models.length,64);assert.equal(models[0].join(""),"000000010010000001");
const inc=Array.from({length:V},()=>[]);
f.graph.edges.forEach(([u,v],e)=>{inc[u].push(e);inc[v].push(e);});
function table(v){
 const clauses=f.clauses.filter(c=>c.vertex===v);let out=0;
 assert.equal(clauses.length,4);
 for(let i=0;i<8;i++){
  const b=Array(E).fill(0);
  inc[v].forEach((e,k)=>b[e]=(i>>k)&1);
  if(clauses.every(c=>sat(c,b)))out|=1<<i;
 }
 return out;
}
function rowOK(r,b){
 let lhs=0,mask=BigInt(r.mask);
 for(let e=0;e<E;e++)if((mask>>BigInt(e))&1n)lhs^=b[e];
 return lhs===r.rhs;
}
const vertexRows=Array.from({length:V},(_,v)=>{
 const p=f.proof[3*v+2];let t=table(v),bad=models.filter(b=>!rowOK(p.row,b)).length;
 assert.equal(t,p.table);
 return {vertex:v,table:t,chargeType:typeof f.charges[v],sourceModelsContradictingClaim:bad,claimedRow:p.row};
});
assert.deepEqual(vertexRows.filter(r=>r.sourceModelsContradictingClaim),[vertexRows[5]]);
assert.equal(vertexRows[5].sourceModelsContradictingClaim,64);
assert.equal(vertexRows[5].table,153);
assert.equal(f.proof[17].support,"102");
assert(models.every(b=>b[10]===1&&(b[0]^b[1])===0&&(b[0]^b[1]^b[10])===1));
assert.equal(BigInt(f.proof.at(-1).row.mask),0n);
assert.equal(f.proof.at(-1).row.rhs,1);
const src=new Set(f.clauses.map(c=>c.id)),seen=new Set(src),fan=new Map();
let applications=0,sourceApplications=0,derivedApplications=0,sourceBytes=0,derivedBytes=0;
for(const p of f.proof){
 assert.equal(p.parents.length,2);assert(!seen.has(p.id));
 for(const id of p.parents){
  assert(seen.has(id));applications++;fan.set(id,(fan.get(id)||0)+1);
  if(src.has(id)){sourceApplications++;sourceBytes+=Buffer.byteLength(id);}
  else{derivedApplications++;derivedBytes+=Buffer.byteLength(id);}
 }
 seen.add(p.id);
}
const AND3=f.proof.filter(p=>p.rule==="AND3").length,XOR=f.proof.filter(p=>p.rule==="XOR").length;
assert.equal(AND3,36);assert.equal(XOR,11);assert.equal(applications,94);
assert.equal(sourceApplications,48);assert.equal(derivedApplications,46);
assert.equal(sourceBytes,134);assert.equal(derivedBytes,128);
assert(Math.max(...fan.values())===1);
const cases=[
 ["accepted",null,true],
 ["typed_array",p=>{p.fixtures[0].proof[17].support=[0,1,10];},false],
 ["numeric_charge",p=>{p.fixtures[0].charges[5]=0;},false],
 ["missing_parent",p=>{p.fixtures[0].proof[17].parents[0]="MISSING";},false],
 ["bad_terminal",p=>{p.fixtures[0].proof.at(-1).row.rhs=0;},false]
],folder=fs.mkdtempSync(path.join(os.tmpdir(),"pnp577-")),native=[];
try{
 for(const [name,edit,expected] of cases){
  let p=JSON.parse(bytes.toString("utf8"));if(edit)edit(p);
  const filename=path.join(folder,name+".json");
  fs.writeFileSync(filename,edit?JSON.stringify(p):bytes);
  const r=cp.spawnSync(process.execPath,[path.join(root,checker),filename],
    {encoding:"utf8",timeout:30000,maxBuffer:2000000});
  assert.ifError(r.error);
  assert.equal(r.status===0,expected,name+": "+r.stderr);
  native.push({name,accepted:r.status===0,assertions:r.status===0?JSON.parse(r.stdout).checks:null,
    rejection:r.status===0?null:(r.stderr.match(/Error: [^\r\n]*/)||[])[0]||"rejected"});
 }
}finally{fs.rmSync(folder,{recursive:true,force:true});}
assert.equal(native[0].assertions,5155);
const out={run:"LSPV-4/577",date_pst:"2026-11-12 21:40 PST",scope:"archived /341 fixture, not R_mix341",
 original_checker_git_blob:blob(ck),original_packet_git_blob:blob(bytes),
 source_models:models.length,first_source_model:models[0].join(""),
 forced_edge10_one_on_all_models:true,vertexRows,
 poison_node:"d17",poison_row:{mask:"0x403",rhs:0},source_models_removed_at_d17:64,
 resources:{SOURCE:48,AND3,XOR,paid_work:AND3+XOR,parent_applications:applications,
 source_applications:sourceApplications,derived_applications:derivedApplications,
 parent_reference_ascii_bytes:sourceBytes+derivedBytes,source_reference_bytes:sourceBytes,
 derived_reference_bytes:derivedBytes,shared_parent_records:[...fan.values()].filter(x=>x>1).length,
 compact_packet_bytes:Buffer.byteLength(JSON.stringify(data)),actual_packet_file_bytes:bytes.length,
 checker_assertions:native[0].assertions},native_replays:native,
 limitations:"One actual malformed accepted source, not a valid UNSAT refutation; no full historical grammar; no physical RAM bound."};
process.stdout.write(JSON.stringify(out,null,2)+"\n");
