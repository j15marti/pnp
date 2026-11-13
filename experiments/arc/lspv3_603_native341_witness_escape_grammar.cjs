#!/usr/bin/env node
"use strict";
// LSPV-3/603. Original archived /341 checker executed as OS Node subprocess.
// node experiments/arc/lspv3_603_native341_witness_escape_grammar.cjs [ledger.json]
const fs=require("fs"),path=require("path"),cp=require("child_process"),os=require("os"),crypto=require("crypto"),assert=require("assert/strict");
const root=path.resolve(__dirname,"../.."),checker=path.join(root,"experiments/arc/lspv2_341_independent_verify.js"),seed=path.join(root,"results/raw/arc/2026-11-12_1725_LSPV3_600_NATIVE341_K4_EDGE_SUFFIX_ACCEPTED.json");
const blob=b=>crypto.createHash("sha1").update("blob "+b.length+"\0").update(b).digest("hex");
const cb=fs.readFileSync(checker),sb=fs.readFileSync(seed),raw=sb.toString("utf8");
assert.equal(blob(cb),"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0");
assert.equal(blob(sb),"393d13265192b4e43073c6f6559bc22b6a71ece5");
const baseline=JSON.parse(raw),copy=x=>JSON.parse(JSON.stringify(x));
const originalSources=JSON.stringify(baseline.fixtures[0].clauses);
assert.equal(baseline.fixtures[0].evenWitness,"000000");
assert.equal(baseline.fixtures[0].deleted[0].assignment,"000000");
const dir=fs.mkdtempSync(path.join(os.tmpdir(),"lspv3-603-")),cases=[],slash=String.fromCharCode(92);
function edit(field,token){
 const pat=field==="even"?/("evenWitness":\s*")000000(")/:/("assignment":\s*")000000(")/;
 assert(pat.test(raw));return raw.replace(pat,(_,a,b)=>a+"00000"+token+b);
}
function test(name,packet,expected){
 const d=JSON.parse(packet);if(name!=="hostile_source")assert.equal(JSON.stringify(d.fixtures[0].clauses),originalSources);
 const f=path.join(dir,cases.length+".json");fs.writeFileSync(f,packet);
 const r=cp.spawnSync(process.execPath,[checker,f],{encoding:"utf8",timeout:30000,maxBuffer:4000000});
 let o=null;try{o=JSON.parse(r.stdout)}catch{}
 const accepted=r.status===0;assert.equal(accepted,expected,name);
 cases.push({name,accepted,expected,bytes:Buffer.byteLength(packet),checks:o?.checks??null,
 error:(r.stderr||"").split("\n").find(x=>x.includes("Error:"))||"",
 sha256:crypto.createHash("sha256").update(packet).digest("hex")});
}
try{
 test("baseline",raw,true);
 for(const field of ["even","deleted"]){
   test(field+"_escaped_ascii0",edit(field,slash+"u0030"),true);
   test(field+"_literal0",edit(field,"0"),true);
   for(const t of ["n","r","u2028","u2029","t","u0020","u0078"]){
     test(field+"_bad_"+t,edit(field,slash+t),false);
   }
   test(field+"_wrongbit1",edit(field,"1"),false);
 }
 test("both_escaped_ascii0",edit("deleted",slash+"u0030",edit("even",slash+"u0030")),true);
 for(const [name,fn] of [
   ["source",d=>d.fixtures[0].clauses[0].literals[0]=999],
   ["parent",d=>d.fixtures[0].proof[0].parents[0]="MISSING"],
   ["sink",d=>d.fixtures[0].proof.at(-1).row.rhs^=1]]){
   const d=copy(baseline);fn(d);test("hostile_"+name,JSON.stringify(d),false);
 }
 const out={schema:"LSPV3-603-archived341-witness-escape-grammar",
 checkerBlob:blob(cb),seedBlob:blob(sb),sources:16,paid:15,
 runs:cases.length,accepts:cases.filter(x=>x.accepted).length,
 rejects:cases.filter(x=>!x.accepted).length,
 originalAssertionGroups:cases.filter(x=>x.accepted).reduce((s,x)=>s+x.checks,0),
 scope:"Recovered /341 fixture only, not complete historical R_mix341",cases};
 const text=JSON.stringify(out,null,2)+"\n";
 if(process.argv[2])fs.writeFileSync(process.argv[2],text);process.stdout.write(text);
}finally{fs.rmSync(dir,{recursive:true,force:true});}
