#!/usr/bin/env node
"use strict";
// LSPV-4/586: Native /341 acceptance, SOURCE-token order and byte sensitivity.
// Run at repository root:
// node experiments/arc/lspv4_586_native341_byte_sensitivity.cjs
// The original checker is executed UNMODIFIED in an OS child process.
const fs=require("node:fs"),os=require("node:os"),path=require("node:path");
const crypto=require("node:crypto"),cp=require("node:child_process");
const checker=path.join("experiments","arc","lspv2_341_independent_verify.js");
const corpus=path.join("results","raw","arc","2026-11-10_1112_LSPV2_537_NATIVE_BYTE_CORPUS_RAW.json");
const source=fs.readFileSync(checker);
function gitblob(b){return crypto.createHash("sha1").update("blob "+b.length+"\0").update(b).digest("hex");}
const checkerBlob=gitblob(source);
if(checkerBlob!=="fcb7d4ced8f922de14c0bda16263a8cc7853e8e0")throw Error("original checker changed");
const corpusBuf=fs.readFileSync(corpus);
if(gitblob(corpusBuf)!=="d5e2d22674b0af365e9b82e4f1b2af8307182ba6")throw Error("corpus changed");
const orig=JSON.parse(corpusBuf.toString("utf8")).minimal.packetBytes;
const base=JSON.parse(orig),dir=fs.mkdtempSync(path.join(os.tmpdir(),"lspv4-586-"));
function run(name,bytes,expected){
  const file=path.join(dir,name+".json");
  fs.writeFileSync(file,bytes,"utf8");
  const out=cp.spawnSync(process.execPath,[checker,file],{encoding:"utf8",timeout:30000,maxBuffer:1<<22});
  const ok=out.status===0&&out.stdout.includes('"checks": 1401');
  if(ok!==expected)throw Error("unexpected original-checker verdict "+name+": "+out.stderr);
  return {name,bytes:Buffer.byteLength(bytes,"utf8"),accepted:ok,exit:out.status};
}
const results={run:"LSPV-4/586",checker_blob:checkerBlob,corpus_blob:gitblob(corpusBuf),original_bytes:orig.length,original_checker_os:true,positive:[],negative:[],parser_mutants:0};
try{
  results.positive.push(run("base",orig,true));
  const orders=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
  for(const order of orders){
    const p=JSON.parse(orig),lit=base.fixtures[0].clauses[0].literals;
    p.fixtures[0].clauses[0].literals=order.map(i=>lit[i]);
    const txt=JSON.stringify(p);
    if(Buffer.byteLength(txt)!==Buffer.byteLength(orig))throw Error("SOURCE permutation changed canonical byte count");
    results.positive.push(run("perm_"+order.join(""),txt,true));
  }
  for(const n of [1,7,31,256,1024]){
    const txt=" ".repeat(n)+orig;
    results.positive.push(run("pad_"+n,txt,true));
    for(let i=0;i<n;i++){
      let invalid=txt.substring(0,i)+"#"+txt.substring(i+1);
      let rejected=false;try{JSON.parse(invalid);}catch(e){rejected=true;}
      if(!rejected)throw Error("JSON parser accepted invalid padding mutation");
      results.parser_mutants++;
    }
    for(const i of [...new Set([0,Math.floor(n/2),n-1])])
      results.negative.push(run("bad_"+n+"_"+i,txt.substring(0,i)+"#"+txt.substring(i+1),false));
  }
  const bad=JSON.parse(orig);bad.fixtures[0].proof[0].parents[0]="missing";
  results.negative.push(run("bad_parent",JSON.stringify(bad),false));
  results.passed=true;
} finally {fs.rmSync(dir,{recursive:true,force:true});}
console.log(JSON.stringify(results,null,2));
