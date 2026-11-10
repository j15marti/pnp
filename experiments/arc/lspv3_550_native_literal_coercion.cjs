#!/usr/bin/env node
"use strict";
/*
 LSPV-3/550: byte-level source literal and charge coercion audit of the
 PINNED, UNMODIFIED 2026-11-02 /341 SOURCE/AND3/XOR fixture verifier.
 Run from repository root:
   node experiments/arc/lspv3_550_native_literal_coercion.cjs
   node experiments/arc/lspv3_550_native_literal_coercion.cjs OUT.json
 Node >=18. This does NOT authenticate the full historical R_mix341 grammar.
*/
const fs=require("fs"),os=require("os"),path=require("path"),crypto=require("crypto");
const {spawnSync}=require("child_process");
const assert=require("assert").strict;
const P="experiments/arc/lspv2_341_mixed_tseitin_min_dag.js";
const V="experiments/arc/lspv2_341_independent_verify.js";
const expected={
 P:"4081022e8a3841d79f751a3d3a7a10decbb026da",
 V:"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0"
};
const hash=x=>crypto.createHash("sha256").update(x).digest("hex");
const blobSha=b=>crypto.createHash("sha1").update(Buffer.concat([
 Buffer.from("blob "+b.length+"\0","utf8"),b])).digest("hex");
assert.equal(blobSha(fs.readFileSync(P)),expected.P);
assert.equal(blobSha(fs.readFileSync(V)),expected.V);
const exec=(file,args)=>spawnSync(process.execPath,[file,...args],{
 encoding:"utf8",maxBuffer:20*1024*1024,timeout:30000});
const generated=exec(P,[]);
assert.equal(generated.status,0,generated.stderr);
const source=JSON.parse(generated.stdout);
const compact=JSON.stringify(source);
const copy=o=>JSON.parse(JSON.stringify(o));
const temp=fs.mkdtempSync(path.join(os.tmpdir(),"lspv3-550-"));
let calls=0, asserted=0;
const ck=(b,m)=>{asserted++;assert.ok(b,m)};
function verifyPacket(o){
 const f=path.join(temp,"case.json");fs.writeFileSync(f,JSON.stringify(o));
 const r=exec(V,[f]);calls++;
 const accept=r.status===0;
 const answer=accept?JSON.parse(r.stdout):null;
 return {accept,checks:answer?answer.checks:null,
  stdoutSha256:accept?hash(r.stdout):null,
  diagnostic:accept?null:(r.stderr.match(/Verifier: [^\n]+|Error: unknown rule/)||[r.stderr.trim()])[0]};
}
const strictSource=o=>o.fixtures.every(f=>{
 const E=f.graph.edges.length;
 return f.charges.every(x=>typeof x==="number"&&(x===0||x===1))&&
 f.clauses.every(c=>c.literals.every(x=>typeof x==="number"&&Number.isSafeInteger(x)&&
 x!==0&&Math.abs(x)<=E));
});
const normalizedClauses=o=>o.fixtures.map(f=>f.clauses.map(c=>c.literals.map(Number)));
function modelCount(clauses,n){
 let count=0;
 for(let mask=0;mask<2**n;mask++){
  const sat=clauses.every(c=>c.some(l=>l>0?((mask>>(l-1))&1)===1:
         ((mask>>(-l-1))&1)===0));
  if(sat)count++;
 }
 return count;
}
const definitions=[
 ["literal_string_1",p=>p.fixtures[0].clauses[0].literals[0]="1",true],
 ["literal_plus_1",p=>p.fixtures[0].clauses[0].literals[0]="+1",true],
 ["literal_zeros_1",p=>p.fixtures[0].clauses[0].literals[0]="0001",true],
 ["literal_space_1",p=>p.fixtures[0].clauses[0].literals[0]=" 1 ",true],
 ["literal_exp_1",p=>p.fixtures[0].clauses[0].literals[0]="1e0",true],
 ["literal_hex_1",p=>p.fixtures[0].clauses[0].literals[0]="0x1",true],
 ["literal_array_1",p=>p.fixtures[0].clauses[0].literals[0]=[1],true],
 ["literal_nested_array_1",p=>p.fixtures[0].clauses[0].literals[0]=[[1]],true],
 ["literal_true",p=>p.fixtures[0].clauses[0].literals[0]=true,true],
 ["literal_large_zeros",p=>p.fixtures[0].clauses[0].literals[0]="0".repeat(4096)+"1",true],
 ["literal_negative_string",p=>{
   const c=p.fixtures[0].clauses.find(z=>z.literals.some(l=>l<0));
   c.literals[c.literals.findIndex(l=>l<0)]=String(c.literals.find(l=>l<0));
 },true],
 ["all_literals_string",p=>p.fixtures.forEach(f=>f.clauses.forEach(c=>{c.literals=c.literals.map(String)})),true],
 ["charge_string_one",p=>p.fixtures[0].charges[0]="1",true],
 ["charge_true",p=>p.fixtures[0].charges[0]=true,true],
 ["charge_array_one",p=>p.fixtures[0].charges[0]=[1],true],
 ["charge_frac_1.75",p=>p.fixtures[0].charges[0]=1.75,true],
 ["charge_high_2power40",p=>p.fixtures[0].charges[0]=2**40+1,true],
 ["charge_pair_3_2",p=>{p.fixtures[0].charges[0]=3;p.fixtures[0].charges[1]=2},true],
 ["all_charges_string",p=>p.fixtures.forEach(f=>{f.charges=f.charges.map(String)}),true],
 ["literal_wrong_2",p=>p.fixtures[0].clauses[0].literals[0]="2",false],
 ["literal_nan_string",p=>p.fixtures[0].clauses[0].literals[0]="nan",false],
 ["literal_null",p=>p.fixtures[0].clauses[0].literals[0]=null,false],
 ["literal_fraction",p=>p.fixtures[0].clauses[0].literals[0]="1.5",false],
 ["charge_wrong_2",p=>p.fixtures[0].charges[0]=2,false],
 ["charge_wrong_invalid",p=>p.fixtures[0].charges[0]="nan",false],
 ["sink_wrong",p=>{p.fixtures[0].proof.at(-1).row.rhs^=1},false],
 ["bad_parent",p=>p.fixtures[0].proof[0].parents[0]="fake",false]
];
try{
 const baseline=verifyPacket(source);
 ck(baseline.accept&&baseline.checks===30714,"original 341 fixture");
 ck(strictSource(source),"original signed source schema");
 const c0=normalizedClauses(source);
 ck(modelCount(c0[0],source.fixtures[0].graph.edges.length)===0,"K4 odd UNSAT");
 const even=source.fixtures[0].evenWitness;
 ck(even.length===6,"even witness length");
 const rows=[];
 for(const [name,modify,expect] of definitions){
   const o=copy(source);modify(o);const result=verifyPacket(o);
   ck(result.accept===expect,name+": acceptance polarity");
   const sameSemantic=JSON.stringify(normalizedClauses(o))===JSON.stringify(c0);
   if(expect){
     ck(result.checks===baseline.checks,name+": identical checks");
     ck(result.stdoutSha256===baseline.stdoutSha256,name+": identical output");
     ck(sameSemantic,name+": original CNF semantics preserved");
     ck(!strictSource(o),name+": strict syntax must reject");
   }
   rows.push({name,expectedAccept:expect,...result,
     deltaCompactBytes:JSON.stringify(o).length-compact.length,
     strictSource:strictSource(o),sameCanonicalCNF:sameSemantic});
 }
 const sensitive=[];
 let totalMutations=0;
 for(const k of [1,2,4,8,16,32,64]){
   const o=copy(source);
   o.fixtures[0].clauses[0].literals[0]="0".repeat(k)+"1";
   const accepted=verifyPacket(o);
   ck(accepted.accept&&accepted.stdoutSha256===baseline.stdoutSha256,
     "accepted leading zero family "+k);
   let badPositions=0;
   for(let i=0;i<k;i++){
     const bad=copy(o),s=bad.fixtures[0].clauses[0].literals[0];
     bad.fixtures[0].clauses[0].literals[0]=s.slice(0,i)+"2"+s.slice(i+1);
     const rr=verifyPacket(bad);totalMutations++;
     ck(!rr.accept,"zero-byte sensitivity "+k+"/"+i);
     ck(rr.diagnostic==="Verifier: signed incidence mismatch",
       "negative must reject by typed source incidence "+k+"/"+i);
     badPositions++;
   }
   sensitive.push({k,accept:accepted.accept,rejectedSingleByteNeighbors:badPositions,
     deltaCompactBytes:JSON.stringify(o).length-compact.length});
 }
 const out={
   experiment:"LSPV-3/550 native source-literal JSON numeric-coercion and byte sensitivity",
   status:["PROVED/RESTRICTED","COMPUTATIONAL"],
   pinnedOriginalGitBlobs:expected,
   execution:"original unchanged Node producer and verifier via child_process",
   baseline:{checks:baseline.checks,stdoutSha256:baseline.stdoutSha256,
      sourceIsStrict:true,firstOddK4SATModels:0},
   testedCases:rows.length,
   acceptedCoercionCases:rows.filter(x=>x.accept).length,
   rejectedAdversarialCases:rows.filter(x=>!x.accept).length,
   cases:rows,
   byteSensitivity:sensitive,
   rejectedSingleZeroMutations:totalMutations,
   nativeVerifierInvocations:calls,
   assertions:asserted,
   conclusion:"fixed paid DAG and fixed canonical CNF admit arbitrarily long literal-token padding; each inserted zero byte is decision-sensitive; no all-calculus or SAT lower bound",
   limitations:[
     "source-level schema audit on recovered 341 test checker only",
     "no authenticated RES/LOCAL-CONVERT/DEF/branch/discharge grammar",
     "does not show accepted SAT source or unsound arithmetic",
     "not a native FLMV time/space measurement"
   ]
 };
 const rendered=JSON.stringify(out,null,2)+"\n";
 if(process.argv[2])fs.writeFileSync(process.argv[2],rendered);
 else process.stdout.write(rendered);
} finally {fs.rmSync(temp,{force:true,recursive:true});}
