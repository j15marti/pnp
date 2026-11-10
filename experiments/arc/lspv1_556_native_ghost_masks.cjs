#!/usr/bin/env node
"use strict";
/* LSPV-1/556: accepted-byte ghost-mask closure in pinned /341 fixture checker.
 * This is NOT the authoritative full historical R_mix341 grammar.
 * Usage from j15marti/pnp root:
 *   node experiments/arc/lspv1_556_native_ghost_masks.cjs
 */
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto"),vm=require("node:vm"),assert=require("node:assert/strict");
const root=path.resolve(__dirname,"../..");
const files={
 producer:"experiments/arc/lspv2_341_mixed_tseitin_min_dag.js",
 checker:"experiments/arc/lspv2_341_independent_verify.js",
 reference:"experiments/arc/lspv2_539_strict_fragment_reference.cjs"
};
const pins={producer:"4081022e8a3841d79f751a3d3a7a10decbb026da",checker:"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0",reference:"fc91a6f33d0d010d6225365a3d9ce72a090af21f"};
function blob(s){return crypto.createHash("sha1").update("blob "+Buffer.byteLength(s)+"\0"+s).digest("hex")}
const src={};
for(const k of Object.keys(files)){src[k]=fs.readFileSync(path.join(root,files[k]),"utf8");assert.equal(blob(src[k]),pins[k],"pinned original source "+k)}
const produced=[];
vm.runInNewContext(src.producer,{console:{log:v=>produced.push(v)}},{timeout:60000});
assert.equal(produced.length,1);
const fixtures=JSON.parse(produced[0]).fixtures;
const copy=x=>JSON.parse(JSON.stringify(x));
function native(f){
 const packet=JSON.stringify({fixtures:[f],summary:[null]}),out=[];
 try{
   vm.runInNewContext(src.checker,{
     require:n=>{assert.equal(n,"fs");return {readFileSync:()=>packet}},
     process:{argv:["node","checker","packet.json"]},console:{log:v=>out.push(v)}
   },{timeout:60000});
   return {accepted:true,checks:JSON.parse(out[0]).checks};
 }catch(e){return {accepted:false,diagnostic:String(e.message)}}
}
const mod={exports:{}};
const requireForRef=n=>{if(n==="fs")return fs;if(n==="crypto")return crypto;throw Error("Unexpected reference dependency "+n)};
vm.runInNewContext(src.reference.replace(/^#![^\n]*\n/,""),{
 module:mod,require:requireForRef,Buffer,console,process:{argv:[]}
},{timeout:60000});
function originalDimacs(f){return "p cnf "+f.graph.edges.length+" "+f.clauses.length+"\n"+f.clauses.map(c=>c.literals.join(" ")+" 0").join("\n")+"\n"}
function typed(f,base){return mod.exports.tryAudit(originalDimacs(base),JSON.stringify({fixtures:[f]}))}
function lift(f,ghost,shift){
 const g=copy(f),rows=g.proof.filter(p=>p.rule==="AND3"&&p.row),nodes=new Map(g.clauses.map(c=>[c.id,c]));
 assert.equal(rows.length,f.graph.n);assert.equal(ghost.length,rows.length);
 rows.forEach((p,i)=>{assert(Number.isSafeInteger(ghost[i])&&ghost[i]>=0);
   p.row.mask="0x"+(BigInt(p.row.mask)^(BigInt(ghost[i])<<BigInt(shift))).toString(16);
 });
 for(const p of g.proof){
   if(p.rule==="XOR"){
     const a=nodes.get(p.parents[0]),b=nodes.get(p.parents[1]);
     p.row.mask="0x"+(BigInt(a.row.mask)^BigInt(b.row.mask)).toString(16);
   }
   nodes.set(p.id,p);
 }
 return g;
}
let tests=0;
function verify(v,msg){tests++;assert(v,msg)}
const base=fixtures[0],E=base.graph.edges.length,V=base.graph.n;
verify(native(base).accepted,"original K4 baseline");
verify(typed(base,base).accepted,"strict K4 baseline");
let k4Native=0,k4Typed=0;
for(let code=0;code<64;code++){
 const g=[code&3,(code>>2)&3,(code>>4)&3];
 g.push(g[0]^g[1]^g[2]);
 const mutated=lift(base,g,E),nat=native(mutated),ref=typed(mutated,base);
 verify(nat.accepted,"ghost K4 variant native "+code);
 verify(ref.accepted===(code===0),"typed mask boundary "+code);
 verify(BigInt(mutated.proof[mutated.proof.length-1].row.mask)===0n,"terminal "+code);
 verify(mutated.proof.length===base.proof.length,"same paid work "+code);
 k4Native+=Number(nat.accepted);k4Typed+=Number(ref.accepted);
}
const suite=[];
for(const f of fixtures){
 const near=Array(f.graph.n).fill(0);near[0]=1;near[1]=1;
 const far=Array(f.graph.n).fill(0);far[0]=7;far[1]=7;
 const a=native(f),b=native(lift(f,near,f.graph.edges.length)),c=native(lift(f,far,f.graph.edges.length+256));
 verify(a.accepted&&b.accepted&&c.accepted,"fixture positive "+f.graph.name);
 verify(a.checks===b.checks&&b.checks===c.checks,"unchanged assertions "+f.graph.name);
 suite.push({name:f.graph.name,vertices:f.graph.n,variables:f.graph.edges.length,sourceClauses:f.clauses.length,
 paidNodes:f.proof.length,baselineChecks:a.checks,nearAccepted:b.accepted,farAccepted:c.accepted});
}
const bad=Array(V).fill(0);bad[0]=1;
const odd=native(lift(base,bad,E));
verify(!odd.accepted&&odd.diagnostic.includes("invalid sink"),"odd ghost must fail sink");
const flipped=copy(base);
const first=flipped.proof.find(p=>p.rule==="AND3"&&p.row);
first.row.mask="0x"+(BigInt(first.row.mask)^1n).toString(16);
const low=native(flipped);
verify(!low.accepted&&low.diagnostic.includes("invalid affine alias"),"low-bit corruption must fail");
const farGhost=lift(base,[1,1,0,0],E+256);
verify(native(farGhost).accepted&&!typed(farGhost,base).accepted,"far out-of-range ghost strict differential");
// An unconstrained ghost bit falsifies the allegedly equivalent extended row on
// an assignment satisfying all four local sources. The true source has E variables.
const localSources=base.clauses.filter(c=>c.vertex===0),row0=base.proof.find(p=>p.rule==="AND3"&&p.row);
let localWitness=null;
for(let m=0;m<(1<<E);m++){
 const all=localSources.every(c=>c.literals.some(l=>((m>>(Math.abs(l)-1))&1)===(l>0?1:0)));
 if(all){localWitness=m;break}
}
verify(localWitness!==null,"local premise conjunction is satisfiable");
const lowParity=Array.from({length:E},(_,e)=>((BigInt(row0.row.mask)>>BigInt(e))&1n)?((localWitness>>e)&1):0).reduce((a,b)=>a^b,0);
verify(lowParity===row0.row.rhs,"valid original affine alias");
const augmentedParity=lowParity^1;
verify(augmentedParity!==row0.row.rhs,"ghost extension violates claimed row");
const output={result:"PROVED/RESTRICTED ACCEPTED-BYTE GHOST-MASK FAMILY, NOT FULL R_mix341",
date:"2026-11-10 PST",pins,checks:tests,k4:{nativeAccepted:k4Native,strictAccepted:k4Typed,
ghostSpaceDimension:2*(V-1),count:64},fixtures:suite,
hostile:{oddGhost:odd,lowBit:low,farGhostNative:native(farGhost),farGhostStrict:typed(farGhost,base).diagnostic},
localCountermodel:{lowAssignmentBits:localWitness,ghostBit:1,claimedRhs:row0.row.rhs,augmentedParity},
limit:"Original pinned checker V8 through Node; ordinary host runtime, not full historical R_mix341, no general SAT lower bound"};
console.log(JSON.stringify(output,null,2));
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(output,null,2)+"\n");
