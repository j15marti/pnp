#!/usr/bin/env node
// Independent JavaScript replay of LSPV-5/435. Exact recovered checker is unchanged.
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import crypto from "node:crypto";
import {spawnSync} from "node:child_process";
import assert from "node:assert/strict";

const root=path.resolve(path.dirname(new URL(import.meta.url).pathname),"../..");
let checker=path.join(root,"experiments/arc/lspv2_341_independent_verify.js");
let packetPath=path.join(root,"results/raw/arc/2026-11-07_2224_LSPV3_491_BALANCED_341_PACKET.json");
if(!fs.existsSync(checker)) checker=path.join(root,"tmp_native/lspv2_341_independent_verify.js");
if(!fs.existsSync(packetPath)) packetPath=path.join(root,"tmp_native/balanced_packet.json");
const packetBytes=fs.readFileSync(packetPath), packet=JSON.parse(packetBytes);
const gitBlob=b=>crypto.createHash("sha1").update(Buffer.from(`blob ${b.length}\0`)).update(b).digest("hex");
assert.equal(gitBlob(fs.readFileSync(checker)),"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0");
assert.equal(gitBlob(packetBytes),"481423a2f5271ab600bbc2f9a526fe62523239a9");
function run(obj){
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),"lspv5-435-js-")), f=path.join(dir,"p.json");
  fs.writeFileSync(f,typeof obj==="string"?obj:JSON.stringify(obj,null,1)+"\n");
  const r=spawnSync(process.execPath,[checker,f],{encoding:"utf8",timeout:15000});
  fs.rmSync(dir,{recursive:true,force:true}); return r;
}
const base=run(fs.readFileSync(packetPath,"utf8"));
assert.equal(base.status,0); const baseline=JSON.parse(base.stdout); assert.equal(baseline.checks,30714);
const clone=()=>structuredClone(packet); let pass=0,reject=0;
function same(mut){const v=clone();mut(v);const r=run(v);assert.equal(r.status,0);assert.equal(r.stdout,base.stdout);pass++;}
same(v=>{v.version="BRANCHING-NATIVE/v999";v.definition="native SPLIT and DISCHARGE";});
same(v=>{v.branchDAG={edges:[["a","b"],["b","a"]],andCases:["a"]};});
same(v=>v.fixtures.forEach(f=>f.proof.forEach(p=>p.context=["x=1"])));
same(v=>v.fixtures.forEach(f=>f.proof.at(-1).context=["x=0","x=1"]));
same(v=>v.fixtures.forEach(f=>f.proof.forEach(p=>{p.rule_alias="DISCHARGE";p.paid_weight_override=0;})));
same(v=>v.fixtures.forEach(f=>f.clauses.forEach(c=>c.branch_local=true)));
function no(mut){const v=clone();mut(v);const r=run(v);assert.notEqual(r.status,0);reject++;}
no(v=>v.fixtures[0].proof[0].rule="SPLIT");
no(v=>v.fixtures[0].proof[0].parents.length=1);
no(v=>v.fixtures[0].proof.at(-1).row.rhs=0);
no(v=>v.fixtures[0].clauses[0].literals[0]=999);
const source=fs.readFileSync(checker,"utf8");
for(const needle of ['p.rule==="AND3"','p.rule==="XOR"','else throw Error("unknown rule")','p.parents?.length===2'])assert.ok(source.includes(needle));
for(const absent of ["context","assumptions","discharged","branchDAG","rule_alias","paid_weight_override"])assert.ok(!source.includes(absent));
console.log(JSON.stringify({run:"LSPV-5/435 independent JS",baseline_checks:baseline.checks,ignored_mutants_accepted:pass,semantic_mutants_rejected:reject,static_absent_branch_fields:6,status:"PASS"},null,2));
