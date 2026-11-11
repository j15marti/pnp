#!/usr/bin/env node
"use strict";
// LSPV-1/573: original dual-checker SAT-source polyglot, independent OS replay.
// Run from j15marti/pnp root: node experiments/arc/lspv1_573_dual_native_sat_polyglot.cjs
// No new proof calculus is defined or inferred by this experiment.
const fs=require("node:fs"),path=require("node:path"),os=require("node:os");
const cp=require("node:child_process"),crypto=require("node:crypto"),assert=require("node:assert/strict");
const repo=process.cwd(), at=p=>path.join(repo,p);
const A_CHECK="experiments/arc/lspv2_341_independent_verify.js";
const B_CHECK="experiments/arc/lspv2_386_independent_verify.js";
const A_SEED="results/raw/arc/2026-11-10_1224_LSPV3_551_ACCEPTED_SAT_PACKET.json";
const B_SEED="results/raw/arc/2026-11-11_0203_LSPV1_568_K4_DP_CLI29.json";
const PACKET="results/raw/arc/2026-11-11_0704_LSPV1_573_DUAL_NATIVE_SAT_POLYGLOT_PACKET.json";
const pins=new Map([
 [A_CHECK,"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0"],
 [B_CHECK,"338305c0ce101704205e57543756b8127074a986"],
 [A_SEED,"706947c767361e7c979b8208677eb983d33838f4"],
 [B_SEED,"e3eb2a46857776089ab83f4ad50159ef622d2869"],
 [PACKET,"cdd96103aa1cff848d03b25872a72a21c0f5d59c"],
]);
function sha(s){return crypto.createHash("sha1").update("blob "+Buffer.byteLength(s)+"\0"+s).digest("hex");}
for(const [p,pin] of pins)assert.equal(sha(fs.readFileSync(at(p),"utf8")),pin,"pinned Git blob mismatch: "+p);
const A=JSON.parse(fs.readFileSync(at(A_SEED),"utf8"));
const B=JSON.parse(fs.readFileSync(at(B_SEED),"utf8"));
const poly={fixtures:A.fixtures,spec:B.spec,gate_defs:B.gate_defs,records:B.records,summary:{...B.summary,length:A.fixtures.length}};
const raw=JSON.stringify(poly)+"\n";
assert.equal(fs.readFileSync(at(PACKET),"utf8"),raw,"packet not exact canonical join");
const witness=[..."101001000000100000"].map(Number);
const sat=c=>c.literals.some(l=>witness[Math.abs(l)-1]===(l>0?1:0));
const satFixture=poly.fixtures[1];
assert.equal(satFixture.clauses.length,48);
assert.equal(satFixture.clauses.filter(sat).length,48,"forged source unexpectedly UNSAT");
assert.equal(witness[0]^witness[1]^witness[12],0,"claimed parity should be false");
assert.equal(poly.records.length,45);
assert.equal(poly.summary.paid_total,29);
assert.equal(poly.fixtures[1].proof.length,47);
const temp=fs.mkdtempSync(path.join(os.tmpdir(),"lspv1_573_"));
function run(checker,packet){
 const f=path.join(temp,"case.json");
 fs.writeFileSync(f,JSON.stringify(packet)+"\n");
 const r=cp.spawnSync(process.execPath,[at(checker),f],{encoding:"utf8",timeout:25000,maxBuffer:2**20});
 return{accepted:r.status===0&&!r.error,status:r.status,signal:r.signal,stderr:(r.stderr||"").slice(0,220),out:(r.stdout||"").slice(0,1200)};
}
const observed=[];
try{
 const test=(name,p,expectA,expectB)=>{
  const a=run(A_CHECK,p),b=run(B_CHECK,p);
  assert.equal(a.accepted,expectA,name+" /341 mismatch: "+a.stderr);
  assert.equal(b.accepted,expectB,name+" /386 mismatch: "+b.stderr);
  observed.push({name,A341:a,B386:b});
 };
 test("original exact SAT-source dual polyglot",poly,true,true);
 const copy=x=>JSON.parse(JSON.stringify(x));
 let t=copy(poly);t.fixtures[1].charges[0]=1;test("repaired A numeric charge",t,false,true);
 t=copy(poly);t.fixtures[1].proof[2].support=[0,1,12];test("repaired A typed support",t,false,true);
 t=copy(poly);t.summary.paid_total--;test("underpaid B summary",t,true,false);
 t=copy(poly);t.records.at(-1).pivot=999999;test("B invalid terminal pivot",t,true,false);
}finally{fs.rmSync(temp,{recursive:true,force:true});}
console.log(JSON.stringify({
 run:"LSPV1/573",status:"COMPUTATIONAL OS replay; restricted two separate archived checker languages",
 gitBlobs:Object.fromEntries(pins),packetBytes:Buffer.byteLength(raw),
 sourceASAT:{variables:18,clauses:48,witness:witness.join(""),satisfied:48},
 proofA:{paid:47,clausesSource:48},proofB:{paid:29,records:45},
 observed,limitations:"Not a unified R_mix341 checker, not a sound /341 refutation, no P!=NP proof."
},null,2));
