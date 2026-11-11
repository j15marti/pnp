#!/usr/bin/env node
"use strict";
/*
 * LSPV-1/563 native-fixture surrogate-ID collision reproducer.
 * Run from the repository root:
 *   node experiments/arc/lspv1_563_surrogate_id_collision.cjs
 * Node >=18, builtins only. Executes the PINNED original producer and verifier
 * unchanged as separate OS Node processes. Not a full historical R_mix341 checker.
 */
const fs=require("node:fs");
const path=require("node:path");
const os=require("node:os");
const crypto=require("node:crypto");
const cp=require("node:child_process");
const assert=require("node:assert/strict");
const root=path.resolve(__dirname,"../..");
const producer=path.join(root,"experiments/arc/lspv2_341_mixed_tseitin_min_dag.js");
const verifier=path.join(root,"experiments/arc/lspv2_341_independent_verify.js");
const pins={
  producer:"4081022e8a3841d79f751a3d3a7a10decbb026da",
  checker:"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0"
};
function gitBlob(file){
  const bytes=fs.readFileSync(file);
  const header=Buffer.from("blob "+bytes.length+"\0");
  return crypto.createHash("sha1").update(header).update(bytes).digest("hex");
}
assert.equal(gitBlob(producer),pins.producer,"original producer blob changed");
assert.equal(gitBlob(verifier),pins.checker,"original checker blob changed");
const original=JSON.parse(cp.execFileSync(process.execPath,[producer],
   {encoding:"utf8",maxBuffer:16*1024*1024}));
const fixture=original.fixtures[0];
assert.equal(fixture.graph.name,"K4");
const baseline={version:original.version,definition:original.definition,
  fixtures:[fixture],summary:[original.summary[0]]};
const clone=x=>JSON.parse(JSON.stringify(x));
function rename(packet,mapping){
  const x=clone(packet);
  const relabel=id=>Object.prototype.hasOwnProperty.call(mapping,id)?mapping[id]:id;
  for(const f of x.fixtures){
    for(const c of f.clauses)c.id=relabel(c.id);
    for(const n of f.proof){
      n.id=relabel(n.id);
      n.parents=n.parents.map(relabel);
    }
    for(const d of f.deleted)d.sourceId=relabel(d.sourceId);
  }
  return x;
}
function loseSurrogates(id){return id.replace(/[\uD800-\uDFFF]/g,"\uFFFD");}
function lossy(packet){
  const x=clone(packet);
  for(const f of x.fixtures){
    for(const c of f.clauses)c.id=loseSurrogates(c.id);
    for(const n of f.proof){
      n.id=loseSurrogates(n.id);
      n.parents=n.parents.map(loseSurrogates);
    }
    for(const d of f.deleted)d.sourceId=loseSurrogates(d.sourceId);
  }
  return x;
}
const allIds={};
for(let i=0;i<16;i++)allIds["s"+i]=String.fromCharCode(0xD800+i);
for(let i=0;i<15;i++)allIds["d"+i]=String.fromCharCode(0xDC00+i);
const srcPair=rename(baseline,{s0:"\uD800",s1:"\uD801"});
const paidPair=rename(baseline,{d0:"\uD800",d1:"\uD801"});
const all31=rename(baseline,allIds);
const utf8One=s=>Buffer.from(s,"utf8").toString("utf8");
let codecChecks=0;
for(let code=0xD800;code<=0xDFFF;code++){
  const s=String.fromCharCode(code);
  assert.equal(Buffer.from(s,"utf8").toString("hex"),"efbfbd");
  assert.equal(utf8One(s),"\uFFFD");
  assert.equal(JSON.parse(JSON.stringify(s)),s);
  codecChecks+=3;
}
assert.notEqual("\uD800","\uD801");
assert.equal(utf8One("\uD800"),utf8One("\uD801"));
assert.notEqual(utf8One("\u03B1"),utf8One("\u03B2"));
assert.equal(JSON.stringify("\uD800"),'"\\ud800"');
assert.equal(JSON.stringify("\uD801"),'"\\ud801"');
codecChecks+=5;
const dir=fs.mkdtempSync(path.join(os.tmpdir(),"pnp-lspv1-563-"));
const results=[];
let acceptedOriginalChecks=0;
function checkCase(label,packet,expected,diagnostic){
  const b=Buffer.from(JSON.stringify(packet),"utf8");
  const file=path.join(dir,label+".json");
  fs.writeFileSync(file,b);
  let accept=false,checks=null,error=null;
  try{
    const stdout=cp.execFileSync(process.execPath,[verifier,file],
      {encoding:"utf8",maxBuffer:16*1024*1024,stdio:["ignore","pipe","pipe"]});
    const answer=JSON.parse(stdout);
    checks=answer.checks;
    accept=true;
  }catch(e){
    error=String(e.stderr?e.stderr.toString("utf8"):e.message).trim();
  }
  assert.equal(accept,expected,label+" wrong original-checker verdict: "+error);
  if(diagnostic)assert.ok(error&&error.includes(diagnostic),label+" bad failure diagnostic");
  if(accept)acceptedOriginalChecks+=checks;
  results.push({label,accepted:accept,assertion_groups:checks,
     byte_length:b.length,paid_nodes:packet.fixtures.length===1?
      packet.fixtures[0].proof.length:null,
     failure:error?error.slice(0,200):null,
     sha256:crypto.createHash("sha256").update(b).digest("hex")});
}
try{
  checkCase("seven_original",original,true);
  checkCase("k4_baseline",baseline,true);
  checkCase("source_pair_lone_surrogates",srcPair,true);
  checkCase("paid_pair_lone_surrogates",paidPair,true);
  checkCase("all_31_ids_lone_surrogates",all31,true);
  checkCase("json_stringify_roundtrip_all31",clone(all31),true);
  checkCase("lossy_utf8_source_pair",lossy(srcPair),false,"unique source id");
  checkCase("lossy_utf8_paid_pair",lossy(paidPair),false,"fresh inference ID");
  checkCase("lossy_utf8_all31",lossy(all31),false,"unique source id");
  checkCase("scalar_utf8_id_controls",
    rename(baseline,{s0:"\u03B1",s1:"\u03B2"}),true);
  const badParent=clone(srcPair);
  badParent.fixtures[0].proof[0].parents[0]="unbound";
  checkCase("bad_parent",badParent,false,"missing antecedent");
  const duplicatePaid=clone(baseline);
  duplicatePaid.fixtures[0].proof[1].id=duplicatePaid.fixtures[0].proof[0].id;
  checkCase("duplicate_paid",duplicatePaid,false,"fresh inference ID");
  const badSource=clone(baseline);
  badSource.fixtures[0].clauses[0].literals[0]=999;
  checkCase("invalid_signed_source",badSource,false,"signed incidence mismatch");
  const badOpcode=clone(baseline);
  badOpcode.fixtures[0].proof[0].rule="RES";
  checkCase("unsupported_historical_opcode",badOpcode,false,"unknown rule");
}finally{
  fs.rmSync(dir,{recursive:true,force:true});
}
const output={
  role:"LSPV-1",result:563,date_pst:"2026-11-10 20:56 PST",
  status:"PROVED/RESTRICTED + COMPUTATIONAL",p_vs_np:"OPEN",
  pinned_original_git_blobs:pins,
  theorem:"Raw JSON escaped lone-surrogate identifiers remain distinct native Map keys, but separate UTF8 encode/decode of parsed IDs conflates them; full JSON stringify/parse preserves them.",
  native_scope:"Recovered SOURCE/AND3/XOR fixture verifier, not complete R_mix341",
  codec_checks:codecChecks,
  original_checker_accepted_assertion_groups:acceptedOriginalChecks,
  tests:results,
  limitations:["No full mixed native checker","No external source binding in recovered verifier",
     "Logical paid work != certificate bytes, verification time, discovery, span or peak space"]
};
const raw=path.join(root,"results/raw/arc/2026-11-10_2056_LSPV1_563_SURROGATE_ID_COLLISION_RAW.json");
fs.mkdirSync(path.dirname(raw),{recursive:true});
fs.writeFileSync(raw,JSON.stringify(output,null,2)+"\n");
console.log(JSON.stringify({raw,tests:results.length,
  positives:results.filter(x=>x.accepted).length,
  negatives:results.filter(x=>!x.accepted).length,
  codec_checks:codecChecks,original_assertions:acceptedOriginalChecks},null,2));
