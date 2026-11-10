#!/usr/bin/env node
"use strict";
/*
 LSPV-3/554: Exact operational-vs-semantic-goal separation.
 Requires the pinned original files from j15marti/pnp main in the same checkout.
 Uses the unchanged historical /341 checker body via an I/O wrapper.
 THIS DOES NOT RUN OR AUTHENTICATE THE FULL R_mix341 CHECKER.
*/
const fs = require("fs");
const originalPath = "experiments/arc/lspv2_341_independent_verify.js";
const originalPacketPath = "results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json";
const forgedPacketPath = "results/raw/arc/2026-11-10_1224_LSPV3_551_ACCEPTED_SAT_PACKET.json";
function insist(b,msg) { if(!b) throw Error("LSPV3_554: "+msg); }
const checkerText = fs.readFileSync(originalPath,"utf8");
const original = JSON.parse(fs.readFileSync(originalPacketPath,"utf8"));
const forged = JSON.parse(fs.readFileSync(forgedPacketPath,"utf8"));
function native(packet) {
  const lines = [];
  try {
    const execute = new Function("require","process","console",checkerText);
    execute(name=>{
      insist(name==="fs","unexpected dependency "+name);
      return {readFileSync:()=>JSON.stringify(packet)};
    }, {argv:["node","original_checker.js","fixture.json"]},
       {log:(...v)=>lines.push(v.map(String).join(" "))});
    const report = JSON.parse(lines.at(-1));
    return {accepted:true,checks:report.checks,fixtures:report.cases.length};
  } catch(e) {
    return {accepted:false,error:String(e)};
  }
}
function satisfies(clauses,witness) {
  return clauses.reduce((n,c)=>{
    insist(Array.isArray(c.literals),"literals");
    let ok=c.literals.some(lit=>{
      insist(Number.isInteger(lit)&&lit!==0,"integer literal");
      let i=Math.abs(lit)-1;
      insist(i<witness.length,"out of range literal");
      return lit>0?witness[i]==="1":witness[i]==="0";
    });
    return n+(ok?1:0);
  },0);
}
function checkOriginalConjunction(f) {
  const p=f.proof[0], a=f.clauses.find(x=>x.id===p.parents[0]),
      b=f.clauses.find(x=>x.id===p.parents[1]);
  insist(a&&b&&p.rule==="AND3","original K4 first inference");
  let table=0;
  for(let mask=0;mask<8;mask++) {
    let bits=Array(f.properties.variables).fill("0");
    p.support.forEach((v,i)=>bits[v]=String((mask>>i)&1));
    const cSat=(c)=>c.literals.some(l=>litSat(l,bits));
    if(cSat(a)&&cSat(b))table|=1<<mask;
  }
  insist(table===p.table,"redundant AND3 truth table");
}
function litSat(lit,bits) {
  return lit>0?bits[lit-1]==="1":bits[-lit-1]==="0";
}
const baseline=native(original);
insist(baseline.accepted&&baseline.checks===30714&&baseline.fixtures===7,
       "original seven-fixture byte checker must accept");
const forgedResult=native(forged);
insist(forgedResult.accepted&&forgedResult.checks===2273&&forgedResult.fixtures===2,
       "pinned forged SAT source must be checker accepted");
const second=forged.fixtures[1];
const witness="101001000000100000";
insist(second.clauses.length===48&&second.properties.variables===18,
       "signed strict3 source dimensions");
insist(witness.length===18&&/^[01]+$/.test(witness),"witness format");
const satCount=satisfies(second.clauses,witness);
insist(satCount===48,"SAT witness must satisfy every original clause");
insist(second.proof.length===47,"paid count in accepted SAT packet");
insist(second.proof.some(p=>typeof p.support==="string"),
       "forgery should contain type-invalid support");
const padded=JSON.parse(JSON.stringify(original));
checkOriginalConjunction(padded.fixtures[0]);
const originalFirst=padded.fixtures[0].proof[0];
padded.fixtures[0].proof.splice(1,0,{...originalFirst,id:"PAID_REDUNDANT_AND3_554"});
const paddedResult=native(padded);
insist(!paddedResult.accepted&&paddedResult.error.includes("proof candidate length"),
       "semantically legal extra paid AND3 must be rejected by fixed fixture length");
const wrongSink=JSON.parse(JSON.stringify(forged));
wrongSink.fixtures[1].proof.at(-1).row.rhs ^= 1;
const wrongResult=native(wrongSink);
insist(!wrongResult.accepted,"sink corruption negative control");
const output={
 run:"LSPV-3/554", status:["PROVED/RESTRICTED conditional abstract-goal no-go",
 "COMPUTATIONAL actual original-checker V8 replay"],
 pinnedChecker:"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0",
 pinnedOriginalPacket:"fe27fe1011d0021e721ccaeb747ed58da65d7464",
 pinnedAcceptedSatPacket:"706947c767361e7c979b8208677eb983d33838f4",
 original:{...baseline, paidK4:original.fixtures[0].proof.length},
 acceptedSat:{...forgedResult, originalSignedClauses:48, variables:18,
  paidNodes:47, witness, witnessSatisfiedClauses:satCount,
  typedInvalidSupport:second.proof.filter(p=>typeof p.support==="string").map(p=>p.id)},
 paidRedundant:{accepted:paddedResult.accepted,reason:paddedResult.error,
   paidK4:padded.fixtures[0].proof.length,
   locallyExactAnd3:true},
 corruptSink:{accepted:wrongResult.accepted,reason:wrongResult.error},
 conclusion:"Native fixture ACCEPTED is not an UNSAT certification goal. No source-preserving semantic-sound goal abstraction can preserve all its accepted terminals."
};
console.log(JSON.stringify(output,null,2));
