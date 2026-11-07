#!/usr/bin/env node
// Independent field-binding replay for LSPV-5/419.
import assert from "node:assert/strict";
import crypto from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, "../..");
const packetPath = path.join(root, "replay/413/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json");
const checker = path.join(root, "replay/413/lspv2_341_independent_verify.js");
const base = JSON.parse(fs.readFileSync(packetPath, "utf8"));
const compact = x => JSON.stringify(x);
const hash = s => crypto.createHash("sha256").update(s).digest("hex");

function mutate(scope, parts, value) {
  const obj = structuredClone(base); let cur = scope === "root" ? obj : obj.fixtures[0];
  for (const step of parts.slice(0, -1)) cur = cur[step];
  cur[parts.at(-1)] = structuredClone(value); return obj;
}

function strictMetadata(obj) {
  assert.equal(obj.version, base.version); assert.equal(obj.definition, base.definition);
  assert.equal(obj.fixtures.length, obj.summary.length);
  for (let i=0;i<obj.fixtures.length;i++) {
    const f=obj.fixtures[i], g=f.graph, p=f.properties, s=obj.summary[i];
    const V=g.n,E=g.edges.length;
    assert.equal(f.charges.length,V);assert.equal(f.charges.reduce((a,b)=>a^b,0),1);
    const degree=Array(V).fill(0), edgeKeys=new Set();
    for(const [a,b] of g.edges){assert(Number.isInteger(a)&&Number.isInteger(b)&&a>=0&&b>=0&&a<V&&b<V&&a!==b);const key=[a,b].sort((x,y)=>x-y).join(":");assert(!edgeKeys.has(key));edgeKeys.add(key);degree[a]++;degree[b]++;}
    assert(degree.every(x=>x===3));
    assert.equal(s.name,g.name); assert.equal(s.vertices,V); assert.equal(s.variables,E);
    assert.equal(s.clauses,f.clauses.length); assert.equal(s.essential,p.essential);
    assert.equal(s.inferences,f.proof.length); assert.equal(s.predictedMinimum,p.predictedMinimum);
    assert.equal(s.allEssential,p.essential===f.clauses.length);
    assert.equal(p.variables,E); assert.equal(p.sourceClauses,f.clauses.length);
    assert.equal(p.inferences,f.proof.length); assert.equal(p.oddUnsat,true); assert.equal(p.evenSat,true);
    assert.equal(p.predictedMinimum,p.essential===f.clauses.length?f.proof.length:null);
    const incid=Array.from({length:V},()=>[]);
    g.edges.forEach(([a,b],e)=>{incid[a].push(e);incid[b].push(e)});
    const sourceIds=new Set();
    for (const c of f.clauses) {
      assert(Number.isInteger(c.vertex)&&c.vertex>=0&&c.vertex<V);assert(!sourceIds.has(c.id));sourceIds.add(c.id);
      let pattern=0;
      incid[c.vertex].forEach((edge,bit)=>{const lit=c.literals.find(x=>Math.abs(x)===edge+1);assert.notEqual(lit,undefined);if(lit<0)pattern|=1<<bit});
      assert.equal(c.pattern,pattern);
    }
    assert.equal(f.deleted.length,f.clauses.length);
    f.deleted.forEach((d,j)=>assert.equal(d.sourceId,f.clauses[j].id));
    assert.equal(p.essential,f.deleted.filter(d=>d.assignment!==null).length);
    assert.equal(typeof f.evenWitness,"string");assert.equal(f.evenWitness.length,E);assert(/^[01]+$/.test(f.evenWitness));
    for(const edges of incid)assert.equal(edges.reduce((a,e)=>a^Number(f.evenWitness[e]),0),0);
    const known=new Set(sourceIds);
    for(const node of f.proof){assert(!known.has(node.id));assert.equal(node.parents?.length,2);assert(node.parents.every(x=>known.has(x)));known.add(node.id)}
  }
  return true;
}

function check(obj) {
  const raw=compact(obj), tmp=path.join(os.tmpdir(),`lspv5-419-${process.pid}-${crypto.randomUUID()}.json`);
  fs.writeFileSync(tmp,raw);
  try {const cp=spawnSync(process.execPath,[checker,tmp],{encoding:"utf8"});return {accepted:cp.status===0,stdoutHash:hash(cp.stdout)}}
  finally {fs.unlinkSync(tmp)}
}

const f=base.fixtures[0], ew=(f.evenWitness[0]==="0"?"1":"0")+f.evenWitness.slice(1);
const specs=[
 ["version","root",["version"],"FORGED/v99",true],
 ["definition","root",["definition"],"FORGED: RES and DEF are free",true],
 ["summary contents","root",["summary",0],{},true],
 ["clause pattern","fixture",["clauses",0,"pattern"],7,true],
 ["property variables","fixture",["properties","variables"],999,true],
 ["property source clauses","fixture",["properties","sourceClauses"],0,true],
 ["property inferences","fixture",["properties","inferences"],0,true],
 ["property odd UNSAT","fixture",["properties","oddUnsat"],false,true],
 ["property even SAT","fixture",["properties","evenSat"],false,true],
 ["property predicted minimum","fixture",["properties","predictedMinimum"],0,true],
 ["graph self loop","fixture",["graph","edges",0],[0,0],false],
 ["charge parity","fixture",["charges",0],f.charges[0]^1,false],
 ["clause vertex","fixture",["clauses",0,"vertex"],999,false],
 ["clause literal","fixture",["clauses",0,"literals",0],999,false],
 ["source id duplicate","fixture",["clauses",1,"id"],f.clauses[0].id,false],
 ["deleted source","fixture",["deleted",0,"sourceId"],"forged",false],
 ["even witness","fixture",["evenWitness"],ew,false],
 ["proof parent","fixture",["proof",0,"parents",0],"forged",false],
 ["essential count","fixture",["properties","essential"],0,false],
 ["summary length","root",["summary"],base.summary.slice(0,-1),false],
];

const baseline=check(base);assert.equal(baseline.accepted,true);assert.equal(strictMetadata(base),true);
let checks=2, accepted=0,rejected=0;
for(const [name,scope,parts,value,expected] of specs){
 const obj=mutate(scope,parts,value);assert.throws(()=>strictMetadata(obj));checks++;
 const got=check(obj);assert.equal(got.accepted,expected,name);checks++;
 if(expected){assert.equal(got.stdoutHash,baseline.stdoutHash,name);checks++;accepted++;}else rejected++;
}
console.log(JSON.stringify({status:"PASS",checks,cases:specs.length,acceptedUnbound:accepted,rejectedBoundControls:rejected,baselineStdoutSha256:baseline.stdoutHash}));
