"use strict";
/*
 LSPV-4/579: original /341 checker, balanced per-vertex 4-SOURCE AND3 tree
 with three string supports rather than one. Original source/parser pins.
 Run: node experiments/arc/lspv4_579_balanced_string_internal_native341.cjs
 Optional: --out /tmp/lspv4_579.json
 This is NOT the unified historical R_mix341 mixed calculus.
*/
const fs=require("node:fs"), os=require("node:os"), path=require("node:path");
const cp=require("node:child_process"), crypto=require("node:crypto");
const assert=require("node:assert/strict");
const root=path.resolve(__dirname,"../..");
const packetPath=path.join(root,"results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json");
const checkerPath=path.join(root,"experiments/arc/lspv2_341_independent_verify.js");
function gitBlob(b){return crypto.createHash("sha1").update("blob "+b.length+"\0").update(b).digest("hex");}
const packetBytes=fs.readFileSync(packetPath),checkerBytes=fs.readFileSync(checkerPath);
assert.equal(gitBlob(packetBytes),"fe27fe1011d0021e721ccaeb747ed58da65d7464");
assert.equal(gitBlob(checkerBytes),"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0");
const original=JSON.parse(packetBytes.toString("utf8"));
const clone=o=>JSON.parse(JSON.stringify(o));
const permutations=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
function size(o){return Buffer.byteLength(JSON.stringify(o)+"\n","utf8");}
function sourceFactor(f,c){
 const E=f.graph.edges.length;
 const support=f.graph.edges.map((e,i)=>e.includes(c.vertex)?i:-1).filter(i=>i>=0);
 assert.equal(support.length,3);
 let table=0;
 for(let m=0;m<8;m++){
  const bits=Array(E).fill(0);
  for(let j=0;j<3;j++)bits[support[j]]=(m>>j)&1;
  if(c.literals.some(l=>l>0?bits[l-1]===1:bits[-l-1]===0))table|=1<<m;
 }
 return {support,table};
}
function tableAt(term,bits){
 let a=0;
 for(let j=0;j<term.support.length;j++)a|=Number(bits[term.support[j]])<<j;
 return (term.table>>a)&1;
}
function balanceStrings(packet,targets=["K4","K33"],perm=[0,1,2]){
 const changed=clone(packet),log=[];
 for(const f of changed.fixtures){
  if(!targets.includes(f.graph.name))continue;
  const E=f.graph.edges.length,V=f.graph.n;
  assert(E<=9,"not a one-digit coordinate fixture");
  assert.equal(f.proof.length,4*V-1);
  const byId=new Map(f.clauses.map(c=>[c.id,sourceFactor(f,c)]));
  for(let v=0;v<V;v++){
   const sources=f.clauses.filter(c=>c.vertex===v).map(c=>c.id);
   assert.equal(sources.length,4);
   const [a,b,c]=f.proof.slice(3*v,3*v+3);
   assert(a&&b&&c&&c.row&&a.rule==="AND3"&&b.rule==="AND3"&&c.rule==="AND3");
   a.parents=sources.slice(0,2);
   b.parents=sources.slice(2,4);
   c.parents=[a.id,b.id];
  }
  for(const p of f.proof){
   if(p.rule!=="AND3")continue;
   const [a,b]=p.parents.map(x=>byId.get(x));
   assert(a&&b,"topological dependencies");
   const union=[...new Set([...a.support,...b.support])];
   assert.equal(union.length,3);
   const ordered=union.map(String).sort((x,y)=>Number(x)-Number(y));
   assert(ordered.every(x=>/^[0-9]$/.test(x)));
   const support=perm.map(i=>ordered[i]).join("");
   let table=0;
   for(let m=0;m<8;m++){
    const bits=Array(E).fill(0);
    for(let j=0;j<3;j++)bits[support[j]]=(m>>j)&1;
    if(tableAt(a,bits)&&tableAt(b,bits))table|=1<<m;
   }
   p.support=support;
   p.table=table;
   byId.set(p.id,{support,table});
   log.push({fixture:f.graph.name,id:p.id,support,table,parents:p.parents});
  }
 }
 return {packet:changed,log};
}
function verifyLocal(f){
 const E=f.graph.edges.length;
 let rowChecks=0;
 for(let v=0;v<f.graph.n;v++){
  const cs=f.clauses.filter(c=>c.vertex===v);
  const final=f.proof[3*v+2];
  assert.equal(cs.length,4);
  assert.equal(final.rule,"AND3");
  assert.equal(typeof final.support,"string");
  const support=[...final.support].map(Number);
  const mask=BigInt(final.row.mask);
  for(let m=0;m<8;m++){
   const bits=Array(E).fill(0);
   support.forEach((e,j)=>bits[e]=(m>>j)&1);
   const conjunct=cs.every(c=>c.literals.some(l=>l>0?bits[l-1]===1:bits[-l-1]===0));
   let lhs=0;
   for(let e=0;e<E;e++)if((mask>>BigInt(e))&1n)lhs^=bits[e];
   const row=lhs===final.row.rhs;
   assert.equal(conjunct,row);
   assert.equal((final.table>>m)&1,Number(conjunct));
   rowChecks++;
  }
 }
 let models=0;
 for(let m=0;m<(1<<E);m++){
  const bits=Array.from({length:E},(_,i)=>(m>>i)&1);
  if(f.clauses.every(c=>c.literals.some(l=>l>0?bits[l-1]===1:bits[-l-1]===0)))models++;
 }
 assert.equal(models,0,"odd-charge original source should be UNSAT");
 return {fixture:f.graph.name,rowChecks,enumeratedAssignments:2**E,sourceModels:models};
}
function nativeRun(temp,label,packet,accept){
 const file=path.join(temp,"test.json");
 fs.writeFileSync(file,JSON.stringify(packet)+"\n","utf8");
 const out=cp.spawnSync(process.execPath,[checkerPath,file],{encoding:"utf8",maxBuffer:16*1024*1024});
 if(out.error)throw out.error;
 const okay=out.status===0;
 assert.equal(okay,accept,label+" rejected/accepted unexpectedly "+(out.stderr||"").slice(0,500));
 const checks=okay?JSON.parse(out.stdout).checks:null;
 if(okay)assert.equal(checks,30714,"unexpected change in native original checker assertion groups");
 return {label,accepted:okay,checks,bytes:size(packet)};
}
const both=balanceStrings(original);
const k4=balanceStrings(original,["K4"]);
const k33=balanceStrings(original,["K33"]);
assert.equal(both.log.length,30);
assert.equal(k4.log.length,12);
assert.equal(k33.log.length,18);
assert.equal(size(original),77714);
assert.equal(size(k4.packet),77690);
assert.equal(size(k33.packet),77678);
assert.equal(size(both.packet),77654);
for(const f of both.packet.fixtures.slice(0,2)){
 const old=original.fixtures.find(x=>x.graph.name===f.graph.name);
 assert.equal(JSON.stringify(f.clauses),JSON.stringify(old.clauses));
 assert.equal(JSON.stringify(f.charges),JSON.stringify(old.charges));
 assert.equal(JSON.stringify(f.graph),JSON.stringify(old.graph));
 assert.equal(f.proof.length,old.proof.length);
 for(let i=0;i<f.proof.length;i++){
  assert.equal(f.proof[i].id,old.proof[i].id);
  assert.equal(f.proof[i].rule,old.proof[i].rule);
  assert.equal(JSON.stringify(f.proof[i].row),JSON.stringify(old.proof[i].row));
 }
}
const semantic=both.packet.fixtures.slice(0,2).map(verifyLocal);
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),"lspv4_579_"));
const runs=[];
try{
 runs.push(nativeRun(tmp,"baseline",original,true));
 runs.push(nativeRun(tmp,"K4-all-string",k4.packet,true));
 runs.push(nativeRun(tmp,"K33-all-string",k33.packet,true));
 runs.push(nativeRun(tmp,"both-all-string",both.packet,true));
 for(let i=0;i<permutations.length;i++){
  const variant=balanceStrings(original,["K4","K33"],permutations[i]).packet;
  runs.push(nativeRun(tmp,"both-permutation-"+i,variant,true));
 }
 let invalid=clone(original);
 invalid.fixtures[0].proof[0].support="012";
 runs.push(nativeRun(tmp,"left-deep-early-string",invalid,false));
 invalid=clone(both.packet);
 invalid.fixtures[0].proof[1].table^=1;
 runs.push(nativeRun(tmp,"incorrect-internal-table",invalid,false));
 invalid=clone(both.packet);
 invalid.fixtures[0].proof[2].row.rhs^=1;
 runs.push(nativeRun(tmp,"incorrect-parity-row",invalid,false));
 invalid=clone(both.packet);
 invalid.fixtures[0].proof[2].parents[1]="no-such-id";
 runs.push(nativeRun(tmp,"missing-parent",invalid,false));
 invalid=clone(both.packet);
 invalid.fixtures[0].clauses[0].literals[0]*=-1;
 runs.push(nativeRun(tmp,"signed-source-corruption",invalid,false));
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
const positives=runs.filter(x=>x.accepted).length,negatives=runs.length-positives;
assert.equal(positives,10);assert.equal(negatives,5);
const result={
 report:"LSPV-4/579",date:"2026-11-12 23:36 PST",
 status:"PROVED/RESTRICTED code theorem and COMPUTATIONAL original OS checker replay",
 original_checker_git_blob:gitBlob(checkerBytes),original_packet_git_blob:gitBlob(packetBytes),
 counts:{original_packet_bytes:size(original),K4_only_bytes:size(k4.packet),K33_only_bytes:size(k33.packet),both_bytes:size(both.packet),saved_bytes:60,transformed_AND3:30,paid_global_7_fixture:321,parent_applications_global:642,source_local_checks:semantic.reduce((s,x)=>s+x.rowChecks,0)},
 semantic,runs,
 note:"/341 SOURCE/AND3/XOR fixture checker only; full historical mixed R_mix341 and original fixed mixed tariff unauthenticated."
};
const at=process.argv.indexOf("--out");
if(at>=0){assert(process.argv[at+1],"--out needs a path");fs.writeFileSync(process.argv[at+1],JSON.stringify(result,null,2)+"\n","utf8");}
console.log(JSON.stringify(result,null,2));
