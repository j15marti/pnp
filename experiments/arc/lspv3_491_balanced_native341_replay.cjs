#!/usr/bin/env node
"use strict";
/*
 LSPV-3/491: replay independently the already published balanced historical /341
 SOURCE/AND3/XOR proof packet against the original recovered /341 checker.
 Not a checker for RES, DEF, LOCAL-CONVERT or split/discharge. Does not modify R_mix341.
 Usage from repository root:
    node experiments/arc/lspv3_491_balanced_native341_replay.cjs
*/
const fs=require("node:fs");
const path=require("node:path");
const os=require("node:os");
const cp=require("node:child_process");
const crypto=require("node:crypto");
const assert=require("node:assert/strict");
const root=path.resolve(__dirname,"../..");
const original=path.join(root,"results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json");
const balanced=path.join(root,"results/raw/arc/2026-11-07_2224_LSPV3_491_BALANCED_341_PACKET.json");
const checker=path.join(root,"experiments/arc/lspv2_341_independent_verify.js");
const sha256=p=>crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
const expectedOriginal="12d723c92c683ec1a59e17d95d0d47156babe7febe27b7432dc01279abcb8d95";
const expectedChecker="0a8167fc65f324860f60abd2a0e0176d0def968cb6ee7055b6aa1bfd43c255ae";
assert.equal(sha256(original),expectedOriginal,"original historical packet changed");
assert.equal(sha256(checker),expectedChecker,"recovered historical checker changed");
const orig=JSON.parse(fs.readFileSync(original,"utf8"));
const replacement=JSON.parse(fs.readFileSync(balanced,"utf8"));
assert.equal(orig.version,"LSPV2-MIXED-TSEITIN-MINDAG341/v1");
assert.equal(JSON.stringify(orig.summary),JSON.stringify(replacement.summary));
assert.equal(orig.fixtures.length,replacement.fixtures.length);
function span(f){
 const d=new Map(f.clauses.map(c=>[c.id,0]));
 const seen=new Set(f.clauses.map(c=>c.id));
 for(const p of f.proof){
   assert.ok(!seen.has(p.id),"duplicate inference ID");
   assert.ok(Array.isArray(p.parents)&&p.parents.length===2,"not binary");
   assert.ok(p.parents.every(a=>seen.has(a)),"forward or missing reference");
   seen.add(p.id);
   d.set(p.id,1+Math.max(...p.parents.map(a=>d.get(a))));
 }
 return d.get(f.proof.at(-1).id);
}
const rows=[];
for(let i=0;i<orig.fixtures.length;i++){
 const a=orig.fixtures[i],b=replacement.fixtures[i],m=a.clauses.length;
 for(const key of ["graph","charges","clauses","deleted","evenWitness","properties"])
   assert.equal(JSON.stringify(a[key]),JSON.stringify(b[key]),"original source or witness drift: "+key);
 assert.equal(b.proof.length,a.proof.length,"logical work must be unchanged");
 assert.equal(b.proof.length,4*a.graph.n-1,"native source+binary arity work formula");
 const oldD=span(a),newD=span(b),lb=Math.ceil(Math.log2(m));
 assert.equal(newD,lb,"new span fails binary source-capacity lower bound");
 assert.ok(newD<=oldD,"no depth improvement");
 const nodeIds=new Set(b.proof.map(p=>p.id));
 assert.equal(nodeIds.size,b.proof.length,"duplicate charged nodes");
 assert.ok(b.proof.every(p=>p.rule==="AND3"||p.rule==="XOR"),"unimplemented rule");
 rows.push({name:a.graph.name,sourceClauses:m,originalSourceVariables:a.graph.edges.length,
  signed3CNF:true,allSourceClausesEssential:a.properties.essential===m,
  paidDistinctNodes:b.proof.length,oldSpan:oldD,balancedSpan:newD,
  lowerBoundIfEssential: a.properties.essential===m?lb:null});
}
function runChecker(filename){
 return cp.spawnSync(process.execPath,[checker,filename],
   {encoding:"utf8",maxBuffer:16*1024*1024});
}
const valid=runChecker(balanced);
assert.equal(valid.status,0,"recovered historical checker rejected balanced packet: "+valid.stderr);
const result=JSON.parse(valid.stdout);
assert.equal(result.checks,30714,"original verified-check count changed");
assert.equal(result.cases.length,7);
assert.equal(result.corruptions,5);
assert.equal(result.malformed,7);
assert.equal(rows.slice(0,6).every(r=>r.allSourceClausesEssential),true);
assert.equal(rows[6].allSourceClausesEssential,false,"bridged negative control");
const hostile=[];
function negative(label,mutate){
 const d=fs.mkdtempSync(path.join(os.tmpdir(),"lspv3-491-"));
 const temp=path.join(d,"mutated.json");
 const v=JSON.parse(JSON.stringify(replacement));
 mutate(v);
 fs.writeFileSync(temp,JSON.stringify(v));
 const got=runChecker(temp);
 fs.rmSync(d,{recursive:true,force:true});
 assert.notEqual(got.status,0,"corrupt "+label+" was accepted");
 hostile.push(label);
}
negative("bad AND3 truth table",v=>{v.fixtures[0].proof[0].table^=1;});
negative("bad XOR rhs",v=>{v.fixtures[0].proof.at(-1).row.rhs^=1;});
negative("missing source parent",v=>{v.fixtures[0].proof[0].parents[0]="unbound-source";});
negative("tampered source literal",v=>{v.fixtures[0].clauses[0].literals[0]*=-1;});
const report={
 run:"LSPV-3/491",status:"PROVED/RESTRICTED historical AND3/XOR accepted sublanguage; full R_mix341 OPEN",
 historicalCheckerBlob:"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0",
 historicalPacketBlob:"fe27fe1011d0021e721ccaeb747ed58da65d7464",
 originalSha256:sha256(original),checkerSha256:sha256(checker),balancedPacketSha256:sha256(balanced),
 originalPacketBytes:fs.statSync(original).size,
 balancedPacketBytes:fs.statSync(balanced).size,
 recoveredChecks:result.checks,
 originalNegativeControls:{malformed:result.malformed,corrupted:result.corruptions},
 additionalCorruptPacketsRejected:hostile,
 caveat:"The original recovered checker accepts only SOURCE/AND3/XOR. An external source requires the distinct exact LSPV3/490 binder. No claim about RES/DEF/LOCAL-CONVERT/branching grammar, algorithmic time or B3.",
 rows
};
console.log(JSON.stringify(report,null,2));
