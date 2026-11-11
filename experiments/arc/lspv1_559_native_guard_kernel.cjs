#!/usr/bin/env node
"use strict";
/* LSPV-1/559, scoped semantic firewall for recovered /341 fixture checker.
   NOT a native full R_mix341 accepted-byte checker. */
const fs=require("node:fs"),path=require("node:path"),vm=require("node:vm"),
 crypto=require("node:crypto"),assert=require("node:assert/strict");
const root=path.resolve(__dirname,"../..");
const pins={
 producer:["experiments/arc/lspv2_341_mixed_tseitin_min_dag.js","4081022e8a3841d79f751a3d3a7a10decbb026da"],
 checker:["experiments/arc/lspv2_341_independent_verify.js","fcb7d4ced8f922de14c0bda16263a8cc7853e8e0"],
 counterfeit:["results/raw/arc/2026-11-10_1224_LSPV3_551_ACCEPTED_SAT_PACKET.json","706947c767361e7c979b8208677eb983d33838f4"]
};
function load(k){
 const [p,expected]=pins[k],s=fs.readFileSync(path.join(root,p),"utf8");
 const got=crypto.createHash("sha1").update("blob "+Buffer.byteLength(s)+"\0"+s).digest("hex");
 assert.equal(got,expected,"pinned Git blob "+k);return s;
}
const producer=load("producer"),checker=load("checker"),counterfeit=JSON.parse(load("counterfeit"));
const output=[];
vm.runInNewContext(producer,{console:{log:x=>output.push(x)}},{timeout:60000});
assert.equal(output.length,1);
const baseline=JSON.parse(output[0]),copy=x=>JSON.parse(JSON.stringify(x));
function native(pkt){
 const raw=JSON.stringify(pkt),printed=[];
 try{
  vm.runInNewContext(checker,{
   require:k=>{assert.equal(k,"fs");return {readFileSync:()=>raw};},
   process:{argv:["node","checker.js","packet.json"]},
   console:{log:x=>printed.push(x)}
  },{timeout:60000});
  assert.equal(printed.length,1);
  return {accept:true,checks:JSON.parse(printed[0]).checks};
 }catch(e){return {accept:false,error:String(e.message)}}
}
function extSource(f){return f.clauses.map(c=>c.literals.slice())}
function guard(f,external){
 const E=f.graph.edges.length;
 if(!Array.isArray(f.charges)||!f.charges.every(x=>typeof x==="number"&&(x===0||x===1)))
   return "CHARGE_NOT_BINARY_NUMBER";
 if(!Array.isArray(external)||external.length!==f.clauses.length)
   return "SOURCE_NOT_BOUND";
 for(let i=0;i<external.length;i++){
  const a=f.clauses[i].literals,b=external[i];
  if(!Array.isArray(a)||!Array.isArray(b)||a.length!==b.length||
    !a.every((x,j)=>typeof x==="number"&&Number.isSafeInteger(x)&&x!==0&&x===b[j]))
    return "SOURCE_NOT_BOUND_OR_TYPED";
 }
 for(const p of f.proof)if(p.rule==="AND3"){
  if(!Array.isArray(p.support))return "AND3_SUPPORT_NOT_ARRAY";
  if(p.row){
   let m;try{m=BigInt(p.row.mask)}catch(_){return "AFFINE_MASK_INVALID"}
   if(m<0n||(m>>BigInt(E))!==0n)return "AFFINE_MASK_OUT_OF_RANGE";
  }
 }
 return "SOURCE_BOUND_SEMANTICALLY_SOUND_FRAGMENT";
}
function packet(f){return {fixtures:[f],summary:[null]}}
function ghostPair(input){
 const f=copy(input),E=f.graph.edges.length,rows=f.proof.filter(p=>p.rule==="AND3"&&p.row);
 assert(rows.length>=2);
 for(const p of [rows[0],rows[1]])
  p.row.mask="0x"+(BigInt(p.row.mask)^(1n<<BigInt(E))).toString(16);
 const nodes=new Map(f.clauses.map(c=>[c.id,c]));
 for(const p of f.proof){
  if(p.rule==="XOR"){
   const a=nodes.get(p.parents[0]),b=nodes.get(p.parents[1]);
   p.row.mask="0x"+(BigInt(a.row.mask)^BigInt(b.row.mask)).toString(16);
  }
  nodes.set(p.id,p);
 }
 return f;
}
function models(f){
 const E=f.graph.edges.length;assert(E<=20,"finite enumeration guard");
 let count=0,first=null;
 for(let a=0;a<(1<<E);a++){
  if(f.clauses.every(c=>c.literals.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0)))){
   count++;if(first===null)first=a;
  }
 }
 return {count,first};
}
let assertions=0;const tests=[];function ck(cond,msg){assertions++;assert(cond,msg)}
function positive(name,f,expected,external=extSource(baseline.fixtures[0])){
 const r=native(packet(f)),g=guard(f,external);
 ck(r.accept&&g===expected,"positive "+name);
 tests.push({name,accepted:r.accept,checks:r.checks,guard:g,paid:f.proof.length});
}
let r=native(baseline);
ck(r.accept&&r.checks===30714,"seven original fixtures");
for(const f of baseline.fixtures)ck(guard(f,extSource(f))==="SOURCE_BOUND_SEMANTICALLY_SOUND_FRAGMENT","baseline typed");
tests.push({name:"seven-baseline-fixtures",accepted:r.accept,checks:r.checks,guarded:7});
let f=copy(baseline.fixtures[0]);f.charges[0]="1";
positive("charge-string-accepted",f,"CHARGE_NOT_BINARY_NUMBER");
f=copy(baseline.fixtures[0]);f.proof[2].support="012";
positive("support-string-accepted",f,"AND3_SUPPORT_NOT_ARRAY");
f=copy(baseline.fixtures[0]);
f.proof[2].row.mask=String(BigInt(f.proof[2].row.mask));
positive("semantically-valid-decimal-mask",f,"SOURCE_BOUND_SEMANTICALLY_SOUND_FRAGMENT");
f=ghostPair(baseline.fixtures[0]);
positive("ghost-mask-accepted",f,"AFFINE_MASK_OUT_OF_RANGE");
ck((BigInt(f.proof[2].row.mask)>>BigInt(f.graph.edges.length))!==0n,"high ghost bit");
const external=extSource(baseline.fixtures[0]);external[0][0]=-external[0][0];
positive("independent-source-mismatch",copy(baseline.fixtures[0]),"SOURCE_NOT_BOUND_OR_TYPED",external);
r=native(counterfeit);
const sat=counterfeit.fixtures[1],counted=models(sat);
ck(r.accept&&counted.count===64,"original accepts SAT counterfeit and 64 models");
ck(guard(sat,extSource(sat))==="CHARGE_NOT_BINARY_NUMBER","counterfeit intercepted");
tests.push({name:"accepted-SAT-counterfeit",accepted:r.accept,checks:r.checks,
 SATModels:counted.count,firstSATMask:counted.first,guard:guard(sat,extSource(sat))});
f=copy(baseline.fixtures[0]);
f.proof[2].row.mask="0x"+(BigInt(f.proof[2].row.mask)^1n).toString(16);
ck(!native(packet(f)).accept,"incorrect low alias rejected");
tests.push({name:"invalid-low-alias",accepted:false});
f=copy(baseline.fixtures[0]);f.clauses[0].literals[0]=999;
ck(!native(packet(f)).accept,"invalid source literal rejected");
tests.push({name:"invalid-source-literal",accepted:false});
f=copy(sat);f.charges[0]=1;
ck(!native({fixtures:[baseline.fixtures[0],f],summary:[null,null]}).accept,"charge repair exposes counterfeit");
tests.push({name:"charge-repair",accepted:false});
f=copy(sat);f.proof[2].support=[0,1,12];
ck(!native({fixtures:[baseline.fixtures[0],f],summary:[null,null]}).accept,"support repair exposes counterfeit");
tests.push({name:"support-repair",accepted:false});
const result={
 id:"LSPV-1/559",date:"2026-11-10 PST",assertions,pins,tests,
 theorem:"On every packet accepted by original fixture checker, independent source-clause equality, numeric bit charges and literals, AND3 support arrays and AND3 mask range <2^E suffice for every paid node to be a valid semantic derivation and the terminal 0=1 to certify UNSAT.",
 maskCharacterization:"For an accepted AND3 row with accurately typed support, a nonzero mask bit >=E is necessarily an unsound purported factor-equivalence over freely varying auxiliary coordinates.",
 limitations:"Not full historical R_mix341; external source supplied as signed arrays rather than an authoritative external DIMACS byte parser. No new RES/DEF/LOCAL-CONVERT or branch semantics; cannot infer P!=NP.",
 open:["P2-D1","P2-C3","P2-B1","P2-B2/B3","P versus NP"]
};
console.log(JSON.stringify(result,null,2));
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+"\n");
