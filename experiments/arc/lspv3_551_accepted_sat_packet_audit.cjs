#!/usr/bin/env node
"use strict";
// LSPV-3/551: exact recovered /341 checker accepts a satisfiable signed 3CNF.
// Execute from the root of j15marti/pnp with Node >=18.
// The ORIGINAL independent_verify.js remains unchanged. This is not the full R_mix341 grammar.
const fs=require("fs"),cp=require("child_process"),crypto=require("crypto"),os=require("os"),path=require("path");
const packetPath="results/raw/arc/2026-11-10_1224_LSPV3_551_ACCEPTED_SAT_PACKET.json";
const checkerPath="experiments/arc/lspv2_341_independent_verify.js";
const sha=s=>crypto.createHash("sha1").update("blob "+Buffer.byteLength(s)+"\0").update(s).digest("hex");
const checker=fs.readFileSync(checkerPath,"utf8");
if(sha(checker)!=="fcb7d4ced8f922de14c0bda16263a8cc7853e8e0")throw Error("original checker Git blob changed");
const packetText=fs.readFileSync(packetPath,"utf8"), packet=JSON.parse(packetText);
const src=packet.fixtures[1];
if(src.graph.n!==12||src.graph.edges.length!==18||src.clauses.length!==48||src.proof.length!==47)throw Error("unexpected source dimensions");
function sat(c,a){return c.some(x=>x>0?a[Math.abs(x)-1]===1:a[Math.abs(x)-1]===0);}
const witness=Array(18).fill(0);for(const i of [0,2,5,12])witness[i]=1;
if(src.clauses.some(c=>!sat(c.literals,witness)))throw Error("source is not SAT under published witness");
const vertexCharge=Array(12).fill(0);
for(let i=0;i<18;i++)if(witness[i])for(const v of src.graph.edges[i])vertexCharge[v]^=1;
if(vertexCharge.some(x=>x!==0))throw Error("cycle witness not even");
const mismatches=[];
for(let m=0;m<8;m++){let a=m&1,b=(m>>1)&1,c=(m>>2)&1;
 if((a^b)!==(a^b^c))mismatches.push([a,b,c]);}
if(mismatches.length!==4)throw Error("semantic-alias mismatch count");
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),"lspv3-551-"));
function run(d){
 const file=path.join(tmp,"packet.json");
 fs.writeFileSync(file,JSON.stringify(d));
 const ret=cp.spawnSync(process.execPath,[checkerPath,file],{encoding:"utf8",maxBuffer:10000000});
 if(ret.error)throw ret.error;
 if(ret.status===0){const x=JSON.parse(ret.stdout);return{accepted:true,checks:x.checks,cases:x.cases.length};}
 return{accepted:false,error:(ret.stderr||ret.stdout).split("\n").filter(Boolean).slice(-4).join(" | ").slice(0,300)};
}
const clone=x=>JSON.parse(JSON.stringify(x));
let original, controls=[];
try {
 original=run(packet);
 const cases=[
  ["charge_as_number",x=>x.fixtures[1].charges[0]=1],
  ["support_as_array",x=>x.fixtures[1].proof[2].support=[0,1,12]],
  ["wrong_table",x=>x.fixtures[1].proof[2].table=150],
  ["bad_parent",x=>x.fixtures[1].proof[0].parents[0]="no-parent"],
  ["bad_sink",x=>x.fixtures[1].proof.at(-1).row.rhs^=1],
  ["bad_signed_source",x=>x.fixtures[1].clauses[0].literals[0]=999],
  ["even_charge",x=>x.fixtures[1].charges[0]="0"],
  ["bad_facet",x=>x.fixtures[1].proof[0].table^=1],
  ["forged_delete_witness",x=>x.fixtures[1].deleted[0].assignment="0".repeat(18)]
 ];
 controls=cases.map(([name,mut])=>{const x=clone(packet);mut(x);return{name,...run(x)};});
} finally {fs.rmSync(tmp,{force:true,recursive:true});}
if(!original.accepted||original.checks!==2273||controls.some(x=>x.accepted))throw Error("native checker regression");
const output={
 id:"LSPV-3/551",model:"unmodified pinned recovered /341 fixture checker in native Node CLI",
 checkerGitBlob:sha(checker),packetGitBlob:sha(packetText),accepted:original,
 source:{vertices:12,variables:18,clauses:48,paidNodes:47,sourceIsSAT:true,
 witness:witness.join(""),satisfiedSourceClauses:src.clauses.filter(c=>sat(c.literals,witness)).length},
 bogusFactor:{nodeId:src.proof[2].id,support:src.proof[2].support,table:src.proof[2].table,row:src.proof[2].row,mismatches},
 controls,scope:"SOUNDNESS FAILURE OF RECOVERED FIXTURE CHECKER ONLY; historical full R_mix341 parser and P versus NP OPEN"
};
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(output,null,2)+"\n");
console.log(JSON.stringify(output,null,2));
