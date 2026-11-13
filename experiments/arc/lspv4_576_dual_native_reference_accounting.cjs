#!/usr/bin/env node
"use strict";
/* LSPV-4/576. Independent reference-occurrence and once-paid DAG auditor.
 * Run: node experiments/arc/lspv4_576_dual_native_reference_accounting.cjs
 * Optional: append --native to run the TWO ORIGINAL separate checker CLIs.
 * Source pins are Git blob SHA-1, not parsed-object hashes.
 */
const fs=require("fs"),path=require("path"),crypto=require("crypto"),cp=require("child_process"),assert=require("assert").strict;
const root=path.resolve(__dirname,"../..");
const path341=path.join(root,"results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json");
const path386=path.join(root,"results/raw/arc/2026-11-12_1031_LSPV4_566_W38_P45_AREA958_NATIVE386_ACCEPTED.json");
function blobId(file){const raw=fs.readFileSync(file);return crypto.createHash("sha1").update(Buffer.from("blob "+raw.length+"\0")).update(raw).digest("hex");}
assert.equal(blobId(path341),"fe27fe1011d0021e721ccaeb747ed58da65d7464");
assert.equal(blobId(path386),"28fc9f41ec151a741e70274637c06629fb9a224f");
const packet=JSON.parse(fs.readFileSync(path341,"utf8")),proof=JSON.parse(fs.readFileSync(path386,"utf8"));
function audit341(f){
 const S=new Set(f.clauses.map(c=>c.id)),D=new Set(f.proof.map(p=>p.id)),seen=new Set(S),fan=new Map();
 assert.equal(S.size,f.clauses.length);assert.equal(D.size,f.proof.length);
 const out={name:f.graph.name,V:f.graph.n,source:f.clauses.length,paid:f.proof.length,applications:0,sourceApplications:0,paidApplications:0,sourceRefAsciiBytes:0,paidRefAsciiBytes:0};
 for(const d of f.proof){
   assert(!seen.has(d.id));assert.equal(d.parents.length,2);
   for(const id of d.parents){
     assert.equal(typeof id,"string");assert(/^[\x00-\x7f]*$/.test(id));assert(seen.has(id));
     fan.set(id,(fan.get(id)||0)+1);out.applications++;
     if(S.has(id)){out.sourceApplications++;out.sourceRefAsciiBytes+=Buffer.byteLength(id);}
     else {out.paidApplications++;out.paidRefAsciiBytes+=Buffer.byteLength(id);}
   }
   seen.add(d.id);
 }
 out.sharedOwners=[...fan.values()].filter(c=>c>1).length;out.root=f.proof.at(-1).id;
 out.referenceBytes=out.sourceRefAsciiBytes+out.paidRefAsciiBytes;
 assert.equal(out.source,4*out.V);assert.equal(out.paid,4*out.V-1);
 assert.equal(out.sourceApplications,4*out.V);assert.equal(out.paidApplications,4*out.V-2);
 assert.equal(out.sharedOwners,0);assert.equal(out.applications,2*out.paid);
 return out;
}
const rows=packet.fixtures.map(audit341);
const sums=rows.reduce((out,r)=>{for(const [k,v]of Object.entries(r))if(typeof v==="number")out[k]=(out[k]||0)+v;return out;},{});
assert.equal(sums.paid,321);assert.equal(sums.applications,642);assert.equal(sums.referenceBytes,1840);
const rec=proof.records,fan=Array(rec.length).fill(0),ways=Array(rec.length).fill(0),counts={SOURCE:0,DEF:0,RES:0},unfold={SOURCE:0,DEF:0,RES:0};
let refDigits=0,parentApps=0;
rec.forEach((r,i)=>{assert(["SOURCE","DEF","RES"].includes(r.kind));counts[r.kind]++;
 for(const j of r.parents){assert(Number.isSafeInteger(j)&&j>=0&&j<i);fan[j]++;parentApps++;refDigits+=String(j).length;}
});
ways[rec.length-1]=1;
for(let i=rec.length-1;i>=0;i--)for(const j of rec[i].parents)ways[j]+=ways[i];
rec.forEach((r,i)=>unfold[r.kind]+=ways[i]);
const shared=rec.map((r,i)=>({index:i,kind:r.kind,fanout:fan[i]})).filter(x=>x.fanout>1);
const d386={source:counts.SOURCE,defFacets:counts.DEF,resolution:counts.RES,oncePaidGateOwners:proof.gate_defs.length,
 nativeLogicalW:counts.RES+proof.gate_defs.length,applications:parentApps,parentIndexDigitBytes:refDigits,
 distinctReferenced:fan.filter(x=>x>0).length,sharedNodes:shared.length,
 sharedResNodes:shared.filter(x=>x.kind==="RES").map(x=>x.index),maxFanout:Math.max(...fan),
 unfoldedResolution:unfold.RES,unfoldedNaiveWork:unfold.RES+proof.gate_defs.length,unfoldedByKind:unfold,sharedRecords:shared};
assert.equal(d386.nativeLogicalW,38);assert.equal(d386.applications,70);assert.equal(refDigits,121);
assert.equal(d386.sharedNodes,13);assert.deepEqual(d386.sharedResNodes,[23]);
assert.equal(d386.unfoldedResolution,36);assert.equal(d386.unfoldedNaiveWork,39);
const out={tag:"LSPV-4/576",status:"PROVED/RESTRICTED count-once identities; original checker CLI optional",original341:{individualProofs:rows,totalsAcrossIndependentFixtures:sums},original386:{sharedDag:d386}};
if(process.argv.includes("--native")){
 const cases=[["341",path341,"experiments/arc/lspv2_341_independent_verify.js","fcb7d4ced8f922de14c0bda16263a8cc7853e8e0"],["386",path386,"experiments/arc/lspv2_386_independent_verify.js","338305c0ce101704205e57543756b8127074a986"]];
 out.native=[];
 for(const [tag,input,rel,sha]of cases){const checker=path.join(root,rel);assert.equal(blobId(checker),sha);
 const run=cp.spawnSync(process.execPath,[checker,input],{encoding:"utf8",timeout:30000,maxBuffer:4*1024*1024});
 assert.ifError(run.error);assert.equal(run.status,0,tag+" original checker: "+run.stderr);
 out.native.push({tag,exit:run.status,stdout:run.stdout.trim().slice(0,1000)});
 }
}
process.stdout.write(JSON.stringify(out,null,2)+"\n");
