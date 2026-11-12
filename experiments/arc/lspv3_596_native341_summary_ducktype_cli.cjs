#!/usr/bin/env node
"use strict";
/*
 * LSPV-3/596: recovered /341 fixture-checker summary shape.
 * This is a test harness. It DOES NOT implement a proof checker.
 * Every verdict comes from a fresh OS Node subprocess running the
 * ORIGINAL, UNMODIFIED experiments/arc/lspv2_341_independent_verify.js.
 *
 * Usage:
 *   node experiments/arc/lspv3_596_native341_summary_ducktype_cli.cjs [raw-output.json]
 *
 * The test verifies exact Git blob identities of the historical checker
 * and source packet, generates 25 exact JSON-byte cases, compares CLI
 * accept/reject outcomes, and writes a machine-readable verdict ledger.
 * This harness is not evidence of a complete R_mix341 grammar.
 */
const fs=require("node:fs");
const path=require("node:path");
const os=require("node:os");
const crypto=require("node:crypto");
const cp=require("node:child_process");
const assert=require("node:assert/strict");
const root=path.resolve(__dirname,"../..");
const checker=path.join(root,"experiments/arc/lspv2_341_independent_verify.js");
const source=path.join(root,"results/raw/arc/2026-11-07_2224_LSPV3_491_BALANCED_341_PACKET.json");
const out=path.resolve(process.argv[2]||path.join(root,"results/raw/arc/2026-11-12_1325_LSPV3_596_SUMMARY_SHAPE_OS_RAW.json"));
const gitBlob=b=>crypto.createHash("sha1").update(Buffer.from("blob "+b.length+"\0")).update(b).digest("hex");
const sha256=b=>crypto.createHash("sha256").update(b).digest("hex");
const checkerBytes=fs.readFileSync(checker),sourceBytes=fs.readFileSync(source);
assert.equal(gitBlob(checkerBytes),"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0","historical checker changed");
assert.equal(gitBlob(sourceBytes),"481423a2f5271ab600bbc2f9a526fe62523239a9","historical fixtures changed");
const fixtures=JSON.parse(sourceBytes.toString("utf8")).fixtures;
assert.equal(fixtures.length,7);
const single=fixtures.slice(0,1),all=fixtures;
const tests=[
 ["single_reference_array",single,[null],true],
 ["single_string_length1",single,"x",true],
 ["single_object_numeric_length1",single,{length:1,untrusted:"would claim SAT",meta:{source:"forged"}},true],
 ["single_object_numeric_length_float1",single,{length:1.0},true],
 ["single_object_extra_array",single,{length:1,values:[null,null,null]},true],
 ["single_array_incorrect_contents",single,[{paid:-1,certified:true}],true],
 ["all_reference_array",all,Array(7).fill(null),true],
 ["all_object_length7",all,{length:7,bogus:"source hash not checked"},true],
 ["all_string_length7",all,"abcdefg",true],
 ["all_array_wrong_payload",all,Array(7).fill({work:0}),true],
 ["single_length_string1",single,{length:"1"},false],
 ["single_length_boolean",single,{length:true},false],
 ["single_length_zero",single,{length:0},false],
 ["single_length_nonint",single,{length:1.5},false],
 ["single_length_negative",single,{length:-1},false],
 ["single_number1",single,1,false],
 ["single_boolean_true",single,true,false],
 ["single_null",single,null,false],
 ["single_missing",single,undefined,false],
 ["single_string_length2",single,"xx",false],
 ["all_object_length6",all,{length:6},false],
 ["all_object_length8",all,{length:8},false],
 ["single_bad_original_source",single.map(f=>({...f,charges:[0,0,0,0]})),{length:1},false],
 ["single_bad_parent",single.map(f=>({...f,proof:[{...f.proof[0],parents:["missing","s1"]},...f.proof.slice(1)]})),{length:1},false],
 ["single_bad_final",single.map(f=>({...f,proof:[...f.proof.slice(0,-1),{...f.proof.at(-1),row:{mask:"0x0",rhs:0}}]})),{length:1},false]
];
const dir=fs.mkdtempSync(path.join(os.tmpdir(),"pnp-lspv3-596-"));
const results=[];
try {
 for(let i=0;i<tests.length;i++){
  const [name,fx,summary,expected]=tests[i];
  const packet={fixtures:fx};if(summary!==undefined)packet.summary=summary;
  const bytes=Buffer.from(JSON.stringify(packet)+"\n","utf8");
  const fname=path.join(dir,String(i).padStart(2,"0")+".json");
  fs.writeFileSync(fname,bytes);
  const proc=cp.spawnSync(process.execPath,[checker,fname],{encoding:"utf8",timeout:15000,maxBuffer:4*1024*1024});
  const accepted=proc.status===0&&!proc.error;
  assert.equal(accepted,expected,name+": unexpected original CLI verdict; "+String(proc.stderr).slice(0,500));
  let checks=null,work=null,fixtureCount=null;
  if(accepted){
   const z=JSON.parse(proc.stdout);checks=z.checks;
   fixtureCount=z.cases.length;
   work=z.cases.reduce((a,c)=>a+c.proofNodes,0);
  }
  results.push({name,expected:expected?"ACCEPT":"REJECT",actual:accepted?"ACCEPT":"REJECT",bytes:bytes.length,sha256:sha256(bytes),...(accepted?{checks,paid_nodes:work,fixtures:fixtureCount}:{error:String(proc.stderr||proc.error||"rejected").slice(0,350)})});
 }
}finally {
 fs.rmSync(dir,{recursive:true,force:true});
}
const raw={id:"LSPV-3/596",date:"2026-11-12 13:25 PST",status:"PROVED/RESTRICTED source inspection and COMPUTATIONAL",authority:"UNCHANGED ORIGINAL /341 CHECKER THROUGH REAL NODE OS CLI SUBPROCESSES",original_checker_path:path.relative(root,checker),original_checker_git_blob:gitBlob(checkerBytes),fixture_path:path.relative(root,source),fixture_git_blob:gitBlob(sourceBytes),candidate:"A JSON summary with strictly numeric length equal to fixture count is accepted irrespective of Array type and member content",scope:"recovered SOURCE/AND3/GF2 fixture checker ONLY, not full historical R_mix341",results,totals:{positive:results.filter(r=>r.actual==="ACCEPT").length,negative:results.filter(r=>r.actual==="REJECT").length,positive_assertions:results.reduce((a,r)=>a+(r.checks||0),0)},open:["P2-D1","P2-C3","P2-B1","P2-B2","P2-B3","P versus NP"]};
fs.mkdirSync(path.dirname(out),{recursive:true});
fs.writeFileSync(out,JSON.stringify(raw,null,2)+"\n");
console.log(JSON.stringify({id:raw.id,totals:raw.totals,original_blob:raw.original_checker_git_blob,raw:out},null,2));
