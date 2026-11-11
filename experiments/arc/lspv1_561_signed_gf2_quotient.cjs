"use strict";
/* LSPV-1/561: run in a local j15marti/pnp checkout with Node >=18.
 node experiments/arc/lspv1_561_signed_gf2_quotient.cjs [replay-output.json]
 The original historical fixture checker is executed without mathematical changes. */
const fs=require("fs"),path=require("path"),vm=require("vm"),crypto=require("crypto"),assert=require("node:assert/strict");
const ROOT=path.resolve(__dirname,"../..");
const pinned={
 producer:["experiments/arc/lspv2_341_mixed_tseitin_min_dag.js","4081022e8a3841d79f751a3d3a7a10decbb026da"],
 checker:["experiments/arc/lspv2_341_independent_verify.js","fcb7d4ced8f922de14c0bda16263a8cc7853e8e0"],
 sat:["results/raw/arc/2026-11-10_1724_LSPV3_557_SINGLE_SAT_PACKET.json","6cf9b0fe1e5a9419e8967d836c707c385418b810"]};
function file(name){const [rel,sha]=pinned[name],src=fs.readFileSync(path.join(ROOT,rel),"utf8"),buf=Buffer.from(src,"utf8"),hash=crypto.createHash("sha1").update("blob "+buf.length+"\0").update(buf).digest("hex");assert.equal(hash,sha,"Git blob changed: "+name);return src;}
const producer=file("producer"),checker=file("checker"),clone=x=>JSON.parse(JSON.stringify(x));
function make(){const out=[];vm.runInNewContext(producer,{console:{log:x=>out.push(x)}},{timeout:20000});assert.equal(out.length,1);return JSON.parse(out[0]);}
function check(p){const out=[];try{vm.runInNewContext(checker,{
 require:name=>{assert.equal(name,"fs");return{readFileSync:()=>JSON.stringify(p)};},
 process:{argv:["node","checker","packet.json"]},console:{log:x=>out.push(x)}
},{timeout:20000});assert.equal(out.length,1);return{accepted:true,assertions:JSON.parse(out[0]).checks};}
catch(e){return{accepted:false,error:String(e&&e.message||e)};}}
const pack=f=>({fixtures:[f],summary:[{}]});
function quotient(p){const out=clone(p);for(const f of out.fixtures){const low=(1n<<BigInt(f.graph.edges.length))-1n;for(const d of f.proof)if(d.row)d.row.mask="0x"+(BigInt(d.row.mask)&low).toString(16);}return out;}
function signed(f,selected,bit,sign){const out=clone(f),byId=new Map(out.clauses.map(c=>[c.id,c]));let count=0;const extra=1n<<BigInt(bit);
 for(const d of out.proof){
  if(d.rule==="AND3"&&d.row){if(selected.has(count))d.row.mask=(sign<0?BigInt(d.row.mask)-extra:BigInt(d.row.mask)|extra).toString();count++;}
  else if(d.rule==="XOR"){const [a,b]=d.parents.map(id=>byId.get(id));d.row.mask=(BigInt(a.row.mask)^BigInt(b.row.mask)).toString();d.row.rhs=a.row.rhs^b.row.rhs;}
  byId.set(d.id,d);
 }
 return{fixture:out,annotations:count};
}
const original=make(),baseBefore=check(original),baseAfter=check(quotient(original));
assert.equal(original.fixtures.length,7);assert(baseBefore.accepted&&baseAfter.accepted);assert.equal(baseBefore.assertions,30714);assert.equal(baseAfter.assertions,30714);
assert.equal(JSON.stringify(quotient(quotient(original))),JSON.stringify(quotient(original)));
const K4=original.fixtures[0],E=K4.graph.edges.length,V=K4.graph.n,cases=[];
assert.equal(V,4);assert.equal(E,6);
for(let mask=0;mask<(1<<V);mask++){
 const selected=new Set(Array.from({length:V},(_,i)=>i).filter(i=>mask&(1<<i))),t=signed(K4,selected,E,-1);assert.equal(t.annotations,V);
 const before=check(pack(t.fixture)),after=check(quotient(pack(t.fixture)));
 assert.equal(before.accepted,selected.size%2===0,"subset "+mask);assert(after.accepted);assert.equal(after.assertions,1401);
 cases.push({mask,negativeRows:selected.size,originalAccepted:before.accepted,quotientAccepted:after.accepted});
}
assert.equal(cases.filter(x=>x.originalAccepted).length,8);
const others=original.fixtures.slice(1).map(f=>{const subset=new Set(Array.from({length:f.graph.n},(_,i)=>i)),v=signed(f,subset,f.graph.edges.length,-1),before=check(pack(v.fixture)),after=check(quotient(pack(v.fixture)));assert(before.accepted&&after.accepted);return{name:f.graph.name,V:f.graph.n,W:f.proof.length,assertions:before.assertions};});
const pos=signed(K4,new Set([0,1]),E+256,+1),posBefore=check(pack(pos.fixture)),posAfter=check(quotient(pack(pos.fixture)));assert(posBefore.accepted&&posAfter.accepted);
const odd=signed(K4,new Set([0]),E,-1),oddBefore=check(pack(odd.fixture)),oddAfter=check(quotient(pack(odd.fixture)));assert(!oddBefore.accepted&&oddAfter.accepted);
const sat=JSON.parse(file("sat")),witness="101001000000100000";
assert.equal(sat.fixtures.length,1);assert.equal(sat.fixtures[0].clauses.length,48);assert.equal(witness.length,18);
assert(sat.fixtures[0].clauses.every(c=>c.literals.some(l=>Number(witness[Math.abs(l)-1])===(l>0?1:0))));
const satBefore=check(sat),satAfter=check(quotient(sat));assert(satBefore.accepted&&satAfter.accepted);assert.equal(satBefore.assertions,3273);assert.equal(satAfter.assertions,3273);
const raw={run:"LSPV1-561-SIGNED-RESIDUE-QUOTIENT/v1",status:"PROVED/RESTRICTED + COMPUTATIONAL",pinnedBlobs:Object.fromEntries(Object.entries(pinned).map(([k,v])=>[k,v[1]])),scope:"recovered original SOURCE/AND3/XOR fixture checker, NOT all historical R_mix341",baseline:{fixtures:7,before:baseBefore,after:baseAfter,paid:original.fixtures.map(f=>f.proof.length),idempotent:true},k4:{V,E,subsets:cases,originalAccepted:8,originalRejected:8,allQuotientsAccepted:true},otherEvenVertexGraphs:others,positiveHighBit:{position:E+256,before:posBefore,after:posAfter},nonConverse:{before:oddBefore,after:oddAfter},SATCounterfeit:{clauses:48,variables:18,witness,sourceSAT:true,before:satBefore,after:satAfter},limits:["acceptedByChecker does not imply semantic UNSAT","full RES DEF LOCAL-CONVERT branch and context semantics unauthenticated","V8 original-body test is not a separately executed native CLI","no all-proof-system lower bound or B3/unrestricted P-versus-NP implication"]};
const output=JSON.stringify(raw,null,2)+"\n";
if(process.argv[2]){const filename=path.resolve(process.argv[2]);assert(!filename.endsWith("2026-11-10_1900_LSPV1_561_SIGNED_GF2_QUOTIENT_RAW.json"));fs.writeFileSync(filename,output);}
process.stdout.write(output);
