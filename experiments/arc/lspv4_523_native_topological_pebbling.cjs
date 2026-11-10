#!/usr/bin/env node
"use strict";
/*
 * LSPV-4/523 native-341 fixture-only proof scheduling audit.
 * Run at j15marti/pnp repository root:
 *   node experiments/arc/lspv4_523_native_topological_pebbling.cjs
 * No npm dependencies; invokes pinned ORIGINAL producer and ORIGINAL checker
 * as subprocesses. This is NOT a full R_mix341 proof checker.
 */
const fs=require("fs"),os=require("os"),path=require("path");
const crypto=require("crypto"),cp=require("child_process");
const root=path.resolve(__dirname,"../..");
const producer=path.join(root,"experiments/arc/lspv2_341_mixed_tseitin_min_dag.js");
const checker=path.join(root,"experiments/arc/lspv2_341_independent_verify.js");
function gitBlob(p) {
 const b=fs.readFileSync(p);
 return crypto.createHash("sha1").update(Buffer.from("blob "+b.length+"\0")).update(b).digest("hex");
}
const expected={
 producer:"4081022e8a3841d79f751a3d3a7a10decbb026da",
 checker:"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0"
};
for(const [key,p] of [["producer",producer],["checker",checker]]) {
 if(gitBlob(p)!==expected[key])throw Error("pinned original "+key+" Git blob drift");
}
function paid(id){return /^d[0-9]+$/.test(id);}
function optimal(f){
 const nodes=new Map(f.proof.map(p=>[p.id,p])),seen=new Set(),order=[];
 function visit(id){
  if(!nodes.has(id)||seen.has(id))return;
  seen.add(id);
  for(const a of nodes.get(id).parents||[])visit(a);
  order.push(nodes.get(id));
 }
 visit(f.proof.at(-1).id);
 if(order.length!==f.proof.length)throw Error("disconnected paid node");
 return order;
}
function profile(nodes){
 const uses=new Map(),depth=new Map(),live=new Set();let max=0;
 for(const p of nodes)for(const a of p.parents||[])
  if(paid(a))uses.set(a,(uses.get(a)||0)+1);
 const degrees=[...uses.values()];
 for(const p of nodes){
  const inPaid=(p.parents||[]).filter(paid);
  if(inPaid.some(a=>!live.has(a)))throw Error("invalid construction order");
  depth.set(p.id,1+Math.max(0,...inPaid.map(a=>depth.get(a))));
  live.add(p.id);max=Math.max(max,live.size);
  for(const a of inPaid){
   uses.set(a,uses.get(a)-1);
   if(uses.get(a)===0)live.delete(a);
  }
 }
 return {paid:nodes.length,peak:max,span:depth.get(nodes.at(-1).id),
         allPaidConsumersUnique:degrees.every(x=>x===1),liveSink:[...live]};
}
function countSatK4(f){
 let n=f.graph.edges.length,count=0;
 for(let x=0;x<(1<<n);x++)
  if(f.clauses.every(c=>c.literals.some(l=>((x>>(Math.abs(l)-1))&1)===(l>0?1:0))))count++;
 return count;
}
const original=JSON.parse(cp.execFileSync(process.execPath,[producer],{encoding:"utf8",maxBuffer:16000000}));
const revised=JSON.parse(JSON.stringify(original));
revised.fixtures.forEach(f=>f.proof=optimal(f));
const profiles=original.fixtures.map((f,i)=>{
 const u=revised.fixtures[i],before=profile(f.proof),after=profile(u.proof),V=f.graph.n;
 if(before.peak!==V+1||after.peak!==3||before.paid!==4*V-1||
    after.paid!==before.paid||before.span!==V+2||after.span!==before.span||
    !before.allPaidConsumersUnique||!after.allPaidConsumersUnique||
    JSON.stringify(f).length!==JSON.stringify(u).length)throw Error("pebbling invariant");
 return {graph:f.graph.name,V,original:before,reordered:after,
         sameSerializedLength:JSON.stringify(f).length===JSON.stringify(u).length};
});
const dir=fs.mkdtempSync(path.join(os.tmpdir(),"pnp-l4-523-"));
function verify(data){
 const fname=path.join(dir,"packet.json");
 fs.writeFileSync(fname,JSON.stringify(data));
 try {
  const out=cp.execFileSync(process.execPath,[checker,fname],{encoding:"utf8",maxBuffer:16000000});
  const obj=JSON.parse(out);
  return {accepted:true,checks:obj.checks,caseCount:obj.cases.length};
 }catch(e){
  return {accepted:false,diagnostic:String(e.stderr||e.message).slice(-500)};
 }
}
let result;
try{
 const a=verify(original),b=verify(revised);
 const adversarialOrder=JSON.parse(JSON.stringify(revised));
 [adversarialOrder.fixtures[0].proof[0],adversarialOrder.fixtures[0].proof[1]]=
 [adversarialOrder.fixtures[0].proof[1],adversarialOrder.fixtures[0].proof[0]];
 const wrongOrder=verify(adversarialOrder);
 const adversarialRow=JSON.parse(JSON.stringify(revised));
 adversarialRow.fixtures[0].proof.at(-1).row.rhs^=1;
 const wrongRow=verify(adversarialRow);
 if(!a.accepted||!b.accepted||a.checks!==30714||b.checks!==30714||
    wrongOrder.accepted||wrongRow.accepted||countSatK4(original.fixtures[0])!==0)
  throw Error("original checker or negative control failed");
 result={status:"COMPUTATIONAL; recovered fixture-only checker",
   pinnedBlobs:expected,original:a,reordered:b,
   profiles,
   adversarial:{childBeforeParent:wrongOrder,corruptXorRow:wrongRow},
   k4OddSatAssignments:countSatK4(original.fixtures[0]),
   caveat:"3 is a logical paid-buffer pebble count, not measured native WORK space"};
}finally{fs.rmSync(dir,{recursive:true,force:true});}
console.log(JSON.stringify(result,null,2));
