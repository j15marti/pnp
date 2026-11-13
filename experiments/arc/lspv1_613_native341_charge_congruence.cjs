#!/usr/bin/env node
"use strict";
/* LSPV-1/613. Exact original-checker charge-type congruence.
   From repository root:
     node experiments/arc/lspv1_613_native341_charge_congruence.cjs
   Run uses original checker as a separate OS Node process, with pinned Git
   blobs, not a replacement checker. Scope: recovered /341 fixture ONLY. */
const fs=require("node:fs"),path=require("node:path"),os=require("node:os");
const cp=require("node:child_process"),crypto=require("node:crypto");
const assert=require("node:assert/strict");
const root=path.resolve(__dirname,"../..");
const ck=path.join(root,"experiments/arc/lspv2_341_independent_verify.js");
const bp=path.join(root,"results/raw/arc/2026-11-12_2100_LSPV1_609_BRIDGE_SLICE_SAT_ACCEPTED.json");
function blob(b){return crypto.createHash("sha1").update(Buffer.from("blob "+b.length+"\0")).update(b).digest("hex");}
const c=fs.readFileSync(ck),b=fs.readFileSync(bp);
assert.equal(blob(c),"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0");
assert.equal(blob(b),"8d6d9bc7f2940a77edf2a07fcb72af111ba5b928");
const base=JSON.parse(b.toString("utf8"));
assert.equal(base.fixtures.length,1);
const orig=base.fixtures[0];
assert.deepEqual(orig.charges,[1,0,0,0,0,"0",0,0,0,0,0,0]);
const copy=x=>JSON.parse(JSON.stringify(x)),row=(first,other)=>Array.from({length:12},(_,i)=>i?other:first);
function run(label,charges,mutate){
 const p=copy(base);p.fixtures[0].charges=charges;
 if(mutate)mutate(p);
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),"pnp-lspv1-613-"));
 const file=path.join(dir,"packet.json");
 let child;
 try {
   fs.writeFileSync(file,JSON.stringify(p));
   child=cp.spawnSync(process.execPath,[ck,file],{encoding:"utf8",timeout:10000,maxBuffer:200000});
 } finally {fs.rmSync(dir,{recursive:true,force:true});}
 const accepted=child.status===0&&!child.error;
 let checks=null;
 if(accepted)checks=JSON.parse(child.stdout).checks;
 return {label,accepted,checks,bytes:Buffer.byteLength(JSON.stringify(p)),
   rejected_reason:accepted?null:(child.stderr||String(child.error)).trim().slice(0,250),
   charge_xor:charges.reduce((x,y)=>x^y,0)};
}
const tests=[
 run("baseline",orig.charges),
 run("all_boolean",row(true,false)),
 run("all_arrays",Array.from({length:12},(_,i)=>[i?0:1])),
 run("true_plus_null",row(true,null)),
 run("true_plus_objects",Array.from({length:12},(_,i)=>i?{}:true)),
 run("false_vertex5",(()=>{let q=orig.charges.slice();q[5]=false;return q;})()),
 run("numeric_zero_vertex5",(()=>{let q=orig.charges.slice();q[5]=0;return q;})()),
 run("all_false",row(false,false)),
 run("one_true_other_numeric",row(true,0)),
 run("bad_AND_table",row(true,false),p=>{p.fixtures[0].proof[0].table^=1;}),
 run("bad_terminal",row(true,false),p=>{p.fixtures[0].proof.at(-1).row.rhs=0;})
];
for(const t of tests.slice(0,6)){assert.equal(t.accepted,true,t.label);assert.equal(t.checks,5155,t.label);}
for(const t of tests.slice(6))assert.equal(t.accepted,false,t.label);
const E=orig.graph.edges.length;
let models=0,first=null;
for(let x=0;x<2**E;x++){
 let ok=true;
 for(const c of orig.clauses){
   let sat=false;
   for(const l of c.literals){
     let bit=(x>>(Math.abs(l)-1))&1;
     if((l>0&&bit===1)||(l<0&&bit===0)){sat=true;break;}
   }
   if(!sat){ok=false;break;}
 }
 if(ok){models++;if(first===null)first=x;}
}
assert.equal(models,64);
const witness=Array.from({length:E},(_,i)=>(first>>i)&1).join("");
assert.equal(witness,"000000010010000001");
const evidence={status:"PASS",scope:"original /341 SOURCE/AND3/XOR fixture only",
  checkerGitBlob:blob(c),packetGitBlob:blob(b),
  source:{n:orig.graph.n,variables:E,clauses:orig.clauses.length,paid:orig.proof.length,models,firstWitness:witness},
  charge_references_in_original:"charges.reduce((x,y)=>x^y,0) === 1; parity !== f.charges[v]",
  tests,accepted:tests.filter(x=>x.accepted).length,rejected:tests.filter(x=>!x.accepted).length,
  conclusion:"Non-number JSON charge values can bypass the SOURCE parity comparison while preserving 32-bit XOR; all-Boolean accepted source is SAT.",
  limit:"Not the full historical R_mix341, not a sound UNSAT proof, not a worst-case lower bound."};
console.log(JSON.stringify(evidence,null,2));
