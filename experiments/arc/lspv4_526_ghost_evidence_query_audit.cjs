"use strict";
/* LSPV-4/526 byte-sensitive ghost XOR evidence. Run from repository root:
 * node experiments/arc/lspv4_526_ghost_evidence_query_audit.cjs
 * This audits the recovered SOURCE/AND3/XOR fixture, NOT full R_mix341.
 */
const fs=require("node:fs");
const pp="experiments/arc/lspv2_341_mixed_tseitin_min_dag.js";
const cp="experiments/arc/lspv2_341_independent_verify.js";
const producer=fs.readFileSync(pp,"utf8"),checker=fs.readFileSync(cp,"utf8");
function check(x,msg){if(!x)throw Error("Audit assertion: "+msg);}
const produced=[];
new Function("console",producer)({log:s=>produced.push(s)});
check(produced.length===1,"producer output");
const fixture=JSON.parse(produced[0]).fixtures[0];
check(fixture.graph.name==="K4"&&fixture.clauses.length===16&&fixture.proof.length===15,"K4 source and paid nodes");
const clone=x=>JSON.parse(JSON.stringify(x));
const packet=f=>JSON.stringify({fixtures:[f],summary:[null]});
function verify(bytes){
 const logs=[];
 try{new Function("require","process","console",checker)(
   name=>{check(name==="fs","checker dependency");return{readFileSync:()=>bytes}},
   {argv:["node","checker","packet.json"]},{log:s=>logs.push(s)});
   const obj=JSON.parse(logs[0]);
   return {accepted:true,checks:obj.checks};
 }catch(e){return {accepted:false,error:String(e.message)};}
}
function lift(H,pair=true){
 check(Number.isInteger(H)&&H>=8&&H%4===0,"height");
 const f=clone(fixture),rows=f.proof.filter(p=>p.rule==="AND3"&&p.row);
 for(const i of (pair?[0,1]:[0]))rows[i].row.mask="0x"+(BigInt(rows[i].row.mask)^(1n<<BigInt(H))).toString(16);
 const map=new Map(f.proof.map(p=>[p.id,p]));
 for(const p of f.proof)if(p.rule==="XOR"){
   const a=map.get(p.parents[0]),b=map.get(p.parents[1]);
   p.row.mask="0x"+(BigInt(a.row.mask)^BigInt(b.row.mask)).toString(16);
 }
 return f;
}
const base=packet(fixture),baseline=verify(base);
check(baseline.accepted&&baseline.checks===1401,"native baseline accepted");
const rows=fixture.proof.filter(p=>p.rule==="AND3"&&p.row);
check(rows[0].row.mask==="0x7"&&rows[1].row.mask==="0x19","two pinned vertex masks");
let pos=0,neg=0,numberOfRuns=1;
const cases=[];
for(const H of [8,16,64,256,1024,4096]){
 const f=lift(H),s=packet(f),res=verify(s);numberOfRuns++;
 check(res.accepted&&res.checks===1401,"paired ghost accepted "+H);
 check(s.length-base.length===H/2-1,"exact evidence delta "+H);
 check(f.proof.length===15&&f.clauses.length===16,"same logical DAG");
 const row=f.proof.filter(p=>p.rule==="AND3"&&p.row)[0],token='"mask":"'+row.row.mask+'"';
 const at=s.indexOf(token);check(at>=0,"find first row");
 const zeros=H/4-1,sample=H<=256?zeros:24;
 let checked=[];
 for(let t=0;t<sample;t++){
  const j=sample===zeros?t:Math.floor(t*(zeros-1)/(sample-1));
  const x=at+'"mask":"0x1'.length+j;
  check(s[x]==="0","padding byte zero");
  const bad=s.slice(0,x)+"1"+s.slice(x+1),r=verify(bad);numberOfRuns++;neg++;
  check(!r.accepted,"single-char mutation must reject at H="+H+", j="+j);
  checked.push(j);
 }
 pos++;cases.push({H,bytes:s.length,extra_bytes:s.length-base.length,
  exact_extra_bytes:H/2-1,sensitive_zero_nibbles:zeros,
  tested_rejected_mutants:sample,mutated_nibble_positions:checked,
  paid_nodes:15,source_clauses:16,verifier_assertions:res.checks});
}
const badUnpaired=verify(packet(lift(64,false)));numberOfRuns++;
check(!badUnpaired.accepted&&badUnpaired.error.includes("invalid sink"),"unpaired high bit rejected");
const badTerminal=clone(fixture);badTerminal.proof.at(-1).row.rhs=0;
check(!verify(packet(badTerminal)).accepted,"bad terminal rejected");numberOfRuns++;
const badSource=clone(fixture);badSource.clauses[0].literals[0]*=-1;
check(!verify(packet(badSource)).accepted,"bad original source rejected");numberOfRuns++;
console.log(JSON.stringify({
 run:"LSPV-4/526",scope:"pinned original SOURCE/AND3/XOR fixture verifier only, not complete historical R_mix341",
 status:"PROVED/RESTRICTED + COMPUTATIONAL",
 pins:{producer:"4081022e8a3841d79f751a3d3a7a10decbb026da",
 checker:"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0"},
 baseline:{original_signed_clauses:16,paid_nodes:15,packet_bytes:base.length,checks:baseline.checks},
 cases,controls:{accepted:pos,rejected_single_byte_neighbors:neg,unpaired_high_bit_rejected:true,
 terminal_rhs_rejected:true,original_source_corruption_rejected:true,total_native_checker_invocations:numberOfRuns},
 exact_theorem:"H multiple of four >=8: paired ghost rows add H/2-1 bytes, preserve 15 paid nodes, and make H/4-1 individual first-row zeros acceptance-sensitive",
 limitations:"No OS Node standalone execution, no native FLMV space measurement, no inference about all-rule R_mix341 or P versus NP"
},null,2));
