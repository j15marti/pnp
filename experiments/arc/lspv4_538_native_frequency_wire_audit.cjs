#!/usr/bin/env node
"use strict";
/* LSPV-4/538: original /386 checker, fixed SOURCE and guard, exact wire-label compression.
   Run from repository checkout:
   node experiments/arc/lspv4_538_native_frequency_wire_audit.cjs [output.json]
   Every positive check launches the UNCHANGED original /386 CLI including its
   eleven built-in negative controls. No historical mixed-rule parser is inferred.
*/
const fs = require("fs");
const cp = require("child_process");
const path = require("path");
const os = require("os");
const crypto = require("crypto");
const assert = require("assert/strict");
const root = path.resolve(__dirname, "../..");
const checker = path.join(root, "experiments/arc/lspv2_386_independent_verify.js");
const seedpath = path.join(root, "results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json");
function gitBlob(file) {
  const bytes=fs.readFileSync(file);
  return crypto.createHash("sha1").update("blob "+bytes.length+"\0").update(bytes).digest("hex");
}
assert.equal(gitBlob(checker),"338305c0ce101704205e57543756b8127074a986");
assert.equal(gitBlob(seedpath),"08aa169b5db49b2ddd1cb5a9b6890fcc3b790916");
const seed=JSON.parse(fs.readFileSync(seedpath,"utf8"));
const clone=o=>JSON.parse(JSON.stringify(o));
const key=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function make(k) {
  const d=clone(seed);
  assert.equal(d.spec.guard,7);
  assert.equal(d.gate_defs.length,2);
  d.gate_defs.push([2,10,1,2],[3,11,1,3]);
  d.summary.paid_gates=4;
  d.summary.paid_total=55;
  for(let i=0;i<k;i++) {
    d.records.splice(d.records.length-1,0,{kind:"DEF",c:key([-11,1]),parents:[],gate:3});
  }
  d.summary.def_views+=k;
  d.summary.live_records+=k;
  return d;
}
function rename(d,labels) {
  const o=clone(d), map=new Map(d.gate_defs.map((t,i)=>[t[1],labels[i]]));
  const lit=x=>{const t=map.get(Math.abs(x));return t===undefined?x:(x<0?-t:t);};
  o.gate_defs=d.gate_defs.map(([id,z,a,b])=>[id,lit(z),lit(a),lit(b)]);
  o.records=d.records.map(r=>Object.assign({},r,{c:key(r.c.map(lit))},
    r.kind==="RES"?{pivot:lit(r.pivot)}:{}));
  return o;
}
function permutations(a) {
  if(!a.length)return [[]];
  return a.flatMap((v,i)=>permutations(a.filter((_,j)=>j!==i)).map(b=>[v,...b]));
}
function frequencies(d) {
  return d.gate_defs.map(([,z])=>{
    let f=0;
    for(const t of d.gate_defs)for(const x of t.slice(1))f+=Number(Math.abs(x)===z);
    for(const r of d.records){
      for(const x of r.c)f+=Number(Math.abs(x)===z);
      if(r.kind==="RES")f+=Number(Math.abs(r.pivot)===z);
    }
    return f;
  });
}
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),"lspv4_538_"));
const packet=path.join(tmp,"packet.json");
function originalCLI(d) {
  fs.writeFileSync(packet,JSON.stringify(d));
  const p=cp.spawnSync(process.execPath,[checker,packet],{encoding:"utf8",maxBuffer:1048576});
  if(p.status!==0)throw new Error("Original checker REJECT: "+(p.stderr||p.stdout).slice(0,500));
  const result=JSON.parse(p.stdout.trim().split(/\r?\n/).at(-1));
  return result;
}
function originalRejects(d) {
  fs.writeFileSync(packet,JSON.stringify(d));
  const p=cp.spawnSync(process.execPath,[checker,packet],{encoding:"utf8",maxBuffer:1048576});
  return p.status!==0;
}
let rows=[], negatives=[];
try {
  for(const k of [0,1,16,64,120]){
    const base=make(k),baseStr=JSON.stringify(base),freq=frequencies(base);
    const accepted=[];
    for(const labels of permutations([8,9,10,11])) {
      const p=rename(base,labels);
      assert.equal(JSON.stringify(p.records.filter(r=>r.kind==="SOURCE")),JSON.stringify(base.records.filter(r=>r.kind==="SOURCE")));
      assert.equal(JSON.stringify(p.spec),JSON.stringify(base.spec));
      const r=originalCLI(p);
      assert.equal(r.paid,55);
      assert.equal(r.res,51);
      assert.equal(r.def,4);
      accepted.push({labels,bytes:Buffer.byteLength(JSON.stringify(p),"utf8")});
    }
    assert.equal(accepted.length,24);
    const min=Math.min(...accepted.map(x=>x.bytes));
    const optimal=accepted.filter(x=>x.bytes===min);
    const oldWireCost=freq.reduce((s,f,i)=>s+f*String([8,9,10,11][i]).length,0);
    const theoretical=freq.slice().sort((a,b)=>b-a).reduce((s,f,i)=>s+f*String([8,9,10,11][i]).length,0);
    assert.equal(min,Buffer.byteLength(baseStr,"utf8")-oldWireCost+theoretical);
    rows.push({k,base_bytes:Buffer.byteLength(baseStr,"utf8"),minimum_bytes:min,
      saved_bytes:Buffer.byteLength(baseStr,"utf8")-min,gate_wire_frequencies:freq,
      one_optimal_assignment:optimal[0].labels,number_of_optimal_permutations:optimal.length,
      accepted_permutations:accepted.length,paid_work:55,records:base.records.length,
      resolution_premise_references:102});
  }
  const x=rename(make(120),rows.at(-1).one_optimal_assignment);
  const bad=[
    ["colliding_output",d=>{d.gate_defs[3][1]=d.gate_defs[2][1];}],
    ["wrong_facet",d=>{const q=d.records.find(r=>r.kind==="DEF"&&r.gate===3);q.c=[1,-9999];}],
    ["underpaid_owner",d=>{d.summary.paid_gates--;}],
    ["forged_SOURCE",d=>{d.records[0].c=[-d.spec.guard];}],
    ["wrong_RES_pivot",d=>{d.records.at(-1).pivot=123456;}]
  ];
  for(const [label,modify] of bad) {
    const p=clone(x);modify(p);
    const rejected=originalRejects(p);
    assert.equal(rejected,true,"unexpected accept of "+label);
    negatives.push({label,rejected});
  }
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
const out={
  status:"COMPUTATIONAL original OS Node original-CLI tests plus PROVED/RESTRICTED exchange theorem",
  checker_git_blob:gitBlob(checker),seed_git_blob:gitBlob(seedpath),
  scope:"archived /386 SOURCE/DEF/RES, fixed guarded SOURCE clause occurrences, guard=7, four paid gate wires, exact JSON.stringify serialization",
  language:"unchanged original /386 CLI including eleven native negative controls for EACH positive variant",
  seed:"no randomness; exhaustive 24 permutations for each of five k values",
  rows,negative_controls:negatives,
  qualification:"Neither physical FLMV time-space measurement nor complete historical R_mix341 grammar; artificial redundant facets do not imply minimum-proof hardness."
};
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(out,null,2)+"\n");
console.log(JSON.stringify(out,null,2));
