#!/usr/bin/env node
"use strict";
// LSPV-3/615: source hash binds bytes, not the logical soundness of native inference.
// Execute from a full repository checkout:
// node experiments/arc/lspv3_615_external_source_hash_not_sufficient.cjs [output.json]
const assert=require("node:assert/strict");
const fs=require("node:fs");
const os=require("node:os");
const path=require("node:path");
const cp=require("node:child_process");
const crypto=require("node:crypto");
const root=path.resolve(__dirname,"../..");
const loc={
 checker:"experiments/arc/lspv2_341_independent_verify.js",
 sat:"results/raw/arc/2026-11-12_2219_LSPV3_606_X10_NATIVE341_ACCEPTED.json",
 unsat:"results/raw/arc/2026-11-13_0624_LSPV3_614_K4_TYPED_CHARGE_ACCEPTED.json",
 cnf:"results/raw/arc/2026-11-13_0124_LSPV3_609_SAT_SIGNED_SOURCE.cnf"
};
const expectedBlobs={
 checker:"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0",
 sat:"1e19a9d2b84daa1fc8c29468873ad62e0d67e105",
 unsat:"70e9c764326e682f28363d11d8303bb27fdf0df5",
 cnf:"fe1fbde1c74ec1caf052fe009bf96c14ab229303"
};
function blob(bytes) {
 return crypto.createHash("sha1").update(Buffer.concat([
  Buffer.from("blob "+bytes.length+"\0"),bytes])).digest("hex");
}
const bytes={};
for(const k of Object.keys(loc)){
 bytes[k]=fs.readFileSync(path.join(root,loc[k]));
 assert.equal(blob(bytes[k]),expectedBlobs[k],"historical blob mismatch: "+k);
}
const sat=JSON.parse(bytes.sat.toString("utf8"));
const unsat=JSON.parse(bytes.unsat.toString("utf8"));
const externalSat=bytes.cnf.toString("utf8");
function signedSource(packet){
 const f=packet.fixtures[0];
 return "p cnf "+f.graph.edges.length+" "+f.clauses.length+"\n"
      +f.clauses.map(c=>c.literals.join(" ")+" 0").join("\n")+"\n";
}
function parseCNF(text) {
 const lines=text.trim().split(/\r?\n/),header=lines.shift().trim().split(/\s+/);
 assert.deepEqual(header.slice(0,2),["p","cnf"]);
 const n=Number(header[2]),m=Number(header[3]);
 assert(Number.isInteger(n)&&n>=0&&n<=24,"exhaustive test n guard");
 assert.equal(lines.length,m);
 const clauses=lines.map(line=>{
  const a=line.trim().split(/\s+/).map(Number);
  assert.equal(a.pop(),0);
  assert(a.every(l=>Number.isInteger(l)&&l!==0&&Math.abs(l)<=n));
  return a;
 });
 return {n,clauses};
}
function enumerate(text) {
 const {n,clauses}=parseCNF(text);let count=0,first=null;
 for(let x=0;x<(1<<n);x++) {
  const ok=clauses.every(c=>c.some(l=>l>0 ?
   ((x >>> (l-1))&1)===1 : ((x >>> (-l-1))&1)===0));
  if(ok){count++;if(first===null)first=Array.from({length:n},(_,i)=>(x>>>i)&1).join("");}
 }
 return {variables:n,source_clauses:clauses.length,assignments_checked:1<<n,
   models:count,first_model:first};
}
const externalUnsat=signedSource(unsat);
assert.equal(signedSource(sat),externalSat,"trusted CNF differs from signed packet source");
const dir=fs.mkdtempSync(path.join(os.tmpdir(),"pnp-l3-615-"));
const pathname=path.join(dir,"native.json");
const rows=[];
function nativeVerify(packet) {
 fs.writeFileSync(pathname,JSON.stringify(packet)+"\n");
 const r=cp.spawnSync(process.execPath,[path.join(root,loc.checker),pathname],
   {encoding:"utf8",timeout:25000,maxBuffer:8*1024*1024});
 if(r.error)throw r.error;
 return {accept:r.status===0,checks:r.status===0?JSON.parse(r.stdout).checks:null,
   error:r.status===0?null:r.stderr.slice(0,220)};
}
function trial(name,packet,source,expectedHash,expectedNative,expectedBind) {
 const native=nativeVerify(packet);
 const exact=signedSource(packet)===source;
 const hash=crypto.createHash("sha256").update(Buffer.from(source,"utf8")).digest("hex");
 const bound=exact && hash===expectedHash;
 assert.equal(native.accept,expectedNative,name+" native verdict");
 assert.equal(bound,expectedBind,name+" source binding");
 rows.push({name,native,source_equal:exact,source_sha256:hash,
   expected_source_sha256:expectedHash,source_bound:bound,
   accepted_by_both:native.accept&&bound});
}
const hSat=crypto.createHash("sha256").update(bytes.cnf).digest("hex");
const hUnsat=crypto.createHash("sha256").update(Buffer.from(externalUnsat)).digest("hex");
try {
 trial("SAT_source_exactly_bound_but_false_refutation",sat,externalSat,hSat,true,true);
 trial("UNSAT_control_source_exactly_bound",unsat,externalUnsat,hUnsat,true,true);
 trial("SAT_source_wrong_hash",sat,externalSat,"0".repeat(64),true,false);
 trial("SAT_source_swapped_to_K4",sat,externalUnsat,hUnsat,true,false);
 trial("SAT_source_single_signed_token_changed",sat,
  externalSat.replace("3 4 8 0","-3 4 8 0"),
  crypto.createHash("sha256").update(externalSat.replace("3 4 8 0","-3 4 8 0")).digest("hex"),
  true,false);
 const typed=structuredClone(sat);typed.fixtures[0].charges[5]=0;
 trial("native_numeric_charge_rejection",typed,externalSat,hSat,false,true);
 const support=structuredClone(sat);support.fixtures[0].proof.find(p=>p.id==="d17").support=[0,1,10];
 trial("native_numeric_support_rejection",support,externalSat,hSat,false,true);
 const sink=structuredClone(sat);sink.fixtures[0].proof.at(-1).row.rhs=0;
 trial("native_GF2_terminal_corruption",sink,externalSat,hSat,false,true);
 const satModels=enumerate(externalSat),unsatModels=enumerate(externalUnsat);
 assert.equal(satModels.models,64);assert.equal(unsatModels.models,0);
 assert.equal(rows[0].native.checks,5155);assert.equal(rows[1].native.checks,1401);
 const result={
  schema:"PNP_LSPV3_615_SOURCE_HASH_NOT_SOUNDNESS/v1",
  source:"unchanged original checker in independent Node OS processes",
  authority:expectedBlobs,
  source_sha256:{sat:hSat,unsat_control:hUnsat},
  novelty:"exact external signed-CNF byte equality and even ideal collision-free source binding cannot repair native inference unsoundness",
  sat:satModels,unsat_control:unsatModels,
  verdicts:{tests:rows.length,native_accept:rows.filter(r=>r.native.accept).length,
    native_reject:rows.filter(r=>!r.native.accept).length,
    bound_accept:rows.filter(r=>r.source_bound).length,
    joint_accept:rows.filter(r=>r.accepted_by_both).length},
  rows,scope:"recovered /341 SOURCE/AND3/XOR only; not historical full R_mix341"
 };
 if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+"\n");
 process.stdout.write(JSON.stringify(result,null,2)+"\n");
}finally{fs.rmSync(dir,{recursive:true,force:true});}
