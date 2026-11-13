#!/usr/bin/env node
"use strict";
/* LSPV-3/601. Run inside j15marti/pnp checkout:
 * node experiments/arc/lspv3_601_native341_charge_to_int32.cjs [output.json]
 * Executes the byte-identical archived /341 checker as a real Node OS subprocess.
 * The published hosted-V8 ledger is a separate result, not an OS run.
 */
const fs=require("node:fs"),path=require("node:path"),os=require("node:os"),cp=require("node:child_process"),crypto=require("node:crypto"),assert=require("node:assert/strict");
const ROOT=path.resolve(__dirname,"../..");
const checker=path.join(ROOT,"experiments/arc/lspv2_341_independent_verify.js");
const seed=path.join(ROOT,"results/raw/arc/2026-11-12_1725_LSPV3_600_NATIVE341_K4_EDGE_SUFFIX_ACCEPTED.json");
const sha=b=>crypto.createHash("sha1").update("blob "+Buffer.byteLength(b)+"\0").update(b).digest("hex");
const rawCheck=fs.readFileSync(checker),rawSeed=fs.readFileSync(seed);
assert.equal(sha(rawCheck),"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0");
assert.equal(sha(rawSeed),"393d13265192b4e43073c6f6559bc22b6a71ece5");
const original=JSON.parse(rawSeed),deep=x=>JSON.parse(JSON.stringify(x)),cases=[];
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),"lspv3-601-"));let number=0;
function run(label,charges,expected,mutator){
 const p=deep(original);p.fixtures[0].charges=deep(charges);if(mutator)mutator(p);
 const f=path.join(tmp,String(number++)+".json");fs.writeFileSync(f,JSON.stringify(p));
 const t=cp.spawnSync(process.execPath,[checker,f],{encoding:"utf8",timeout:10000});
 let result=null;try{result=JSON.parse(t.stdout)}catch(e){}
 const row={label,charges,expected,accepted:t.status===0,checks:result?.checks??null,stderr:t.stderr?.trim()??"",correct:(t.status===0)===expected};
 assert(row.correct,"Mismatch in "+label+": "+JSON.stringify(row));cases.push(row);
}
try{
 run("baseline",[1,0,0,0],true);
 for(const [name,q] of [["null",null],["false",false],["string0","0"],["emptyArray",[]],["arrayZero",[0]],["emptyObject",{}],["untrustedObject",{source_hash:"INJECTED_UNTRUSTED",payload:[1,2,3]}],["plus2^32",4294967296],["minus2^32",-4294967296],["hexZero","0x0"]])run("zero_"+name,[1,q,0,0],true);
 for(const [name,q] of [["true",true],["string1","1"],["arrayOne",[1]],["plus2^32+1",4294967297],["minus2^32+1",-4294967295],["hexOne","0x1"]])run("one_"+name,[q,0,0,0],true);
 run("all_heterogeneous",["1",{},[],null],true);
 for(const [name,c] of [["wrong_zero_true",[1,true,0,0]],["wrong_one_object",[{},0,0,0]],["wrong_zero_two",[1,2,0,0]],["wrong_one_two",[2,0,0,0]]])run("hostile_"+name,c,false);
 run("hostile_source_literal",[1,{},0,0],false,p=>p.fixtures[0].clauses[0].literals[0]=999);
 run("hostile_parent_id",[1,{},0,0],false,p=>p.fixtures[0].proof[0].parents[0]="INVALID-PARENT");
 run("hostile_terminal_rhs",[1,{},0,0],false,p=>p.fixtures[0].proof.at(-1).row.rhs^=1);
 const output={tag:"LSPV-3/601 CLI OS replayer",node:process.version,originalCheckerBlob:sha(rawCheck),originalSeedBlob:sha(rawSeed),cases,positive:cases.filter(x=>x.expected).length,negative:cases.filter(x=>!x.expected).length,originalPositiveChecks:cases.filter(x=>x.accepted).reduce((s,x)=>s+x.checks,0),scope:"Archived /341 core ONLY; not historical complete R_mix341"};
 const rendered=JSON.stringify(output,null,2)+"\n";
 if(process.argv[2])fs.writeFileSync(process.argv[2],rendered);process.stdout.write(rendered);
}finally{fs.rmSync(tmp,{force:true,recursive:true});}
