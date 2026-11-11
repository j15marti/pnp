#!/usr/bin/env node
"use strict";
// LSPV-3/566. Native archived-/386 source-component acceptance cliff.
// Run in a full j15marti/pnp checkout:
//   node experiments/arc/lspv3_566_disconnected_386_native_replay.cjs
//   node experiments/arc/lspv3_566_disconnected_386_native_replay.cjs --write
// Executes the ORIGINAL UNMODIFIED archived /386 checker in a Node VM for
// checkProof and in a separate actual OS Node process for its complete CLI.
// Does NOT implement or authenticate the historical full R_mix341 calculus.
const assert=require("node:assert/strict");
const fs=require("node:fs"),path=require("node:path"),os=require("node:os");
const crypto=require("node:crypto"),vm=require("node:vm");
const cp=require("node:child_process");
const ROOT=path.resolve(__dirname,"../..");
const ckPath=path.join(ROOT,"experiments/arc/lspv2_386_independent_verify.js");
const seedPath=path.join(ROOT,"results/raw/arc/2026-11-11_0203_LSPV1_568_K4_DP_CLI29.json");
const EXPECT_CK="338305c0ce101704205e57543756b8127074a986";
const EXPECT_SEED="e3eb2a46857776089ab83f4ad50159ef622d2869";
const blob=buf=>crypto.createHash("sha1").update(Buffer.concat([Buffer.from("blob "+buf.length+"\0"),buf])).digest("hex");
const cb=fs.readFileSync(ckPath),sb=fs.readFileSync(seedPath);
assert.equal(blob(cb),EXPECT_CK,"original checker SHA changed");
assert.equal(blob(sb),EXPECT_SEED,"native seed SHA changed");
const ckCode=cb.toString("utf8"),base=JSON.parse(sb.toString("utf8"));
assert.deepEqual(base.summary,{source:17,def_views:0,resolution:28,paid_gates:1,paid_total:29,live_records:45});
const ctx={require,console,process,structuredClone};
vm.createContext(ctx);
const stop=ckCode.indexOf("for(const f of process.argv.slice(2)){");
assert(stop>0,"original CLI boundary missing");
vm.runInContext(ckCode.slice(0,stop)+"\nglobalThis._native_checkProof=checkProof;",ctx,{filename:ckPath});
const originalCore=ctx._native_checkProof;
const copy=x=>JSON.parse(JSON.stringify(x));
const canon=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function build(k){
 assert(Number.isInteger(k)&&k>=1);
 const E=6*k,h=4*k,guard=E+1,z=guard+1;
 const lit=x=>Math.sign(x)*(Math.abs(x)===7?guard:Math.abs(x)===8?z:Math.abs(x));
 const d=copy(base),edges=[];
 for(let j=0;j<k;j++)for(const [u,v] of base.spec.edges)edges.push([u+4*j,v+4*j]);
 d.spec={h,edges,charge:[1,...Array(h-1).fill(0)],guard};
 d.gate_defs=d.gate_defs.map(([id,out,a,b])=>[id,lit(out),lit(a),lit(b)]);
 d.records=d.records.map(r=>({...r,c:canon(r.c.map(lit)),pivot:r.kind==="RES"?lit(r.pivot):r.pivot}));
 const added=[];
 for(let v=4;v<h;v++){
  const inc=[];edges.forEach(([u,w],e)=>{if(u===v||w===v)inc.push(e+1)});
  assert.equal(inc.length,3);
  for(let mask=0;mask<8;mask++){
   const bits=[mask&1,(mask>>1)&1,(mask>>2)&1];
   if(bits.reduce((a,b)=>a+b,0)%2!==d.spec.charge[v])
    added.push({kind:"SOURCE",source:v,parents:[],c:canon([...inc.map((e,i)=>bits[i]?-e:e),-guard])});
  }
 }
 // Insert before the existing terminal RES, so ALL existing parent indices
 // and the paid RES DAG remain byte-for-byte identical.
 d.records.splice(-1,0,...added);
 d.summary.source+=added.length;
 d.summary.live_records+=added.length;
 return d;
}
function independentSource(d,k){
 const expected=new Set(),guard=d.spec.guard,edges=d.spec.edges;
 expected.add("-1:"+JSON.stringify([guard]));
 const deg=Array(d.spec.h).fill(0);
 for(const [u,v] of edges){deg[u]++;deg[v]++}
 assert(deg.every(x=>x===3));
 for(let v=0;v<d.spec.h;v++){
  const inc=[];edges.forEach(([u,w],e)=>{if(u===v||w===v)inc.push(e+1)});
  for(let pat=0;pat<8;pat++){
   const signs=[pat&1,(pat>>1)&1,(pat>>2)&1];
   if(signs.reduce((a,b)=>a+b,0)%2!==d.spec.charge[v]){
    expected.add(v+":"+JSON.stringify(canon([...inc.map((e,i)=>signs[i]?-e:e),-guard])));
   }
  }
 }
 const actual=d.records.filter(r=>r.kind==="SOURCE").map(r=>r.source+":"+JSON.stringify(r.c));
 assert.equal(actual.length,16*k+1);
 assert.equal(new Set(actual).size,expected.size);
 assert(actual.every(x=>expected.has(x)));
 const adj=Array.from({length:d.spec.h},()=>[]);
 for(const [u,v] of edges){adj[u].push(v);adj[v].push(u)}
 const seen=new Set(),components=[];
 for(let i=0;i<adj.length;i++)if(!seen.has(i)){
  const q=[i];seen.add(i);let count=0;
  while(q.length){const x=q.pop();count++;for(const y of adj[x])if(!seen.has(y)){seen.add(y);q.push(y)}}
  components.push(count);
 }
 assert.equal(components.length,k);
 assert(components.every(x=>x===4));
 return {signedSourceExact:true,components};
}
function mathematical(d,control=false){
 try{return {accepted:true,result:originalCore(d,{control})}}
 catch(e){return {accepted:false,error:String(e)}}
}
function nativeCli(d){
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),"lspv3-566-"));
 const packet=path.join(tmp,"packet.json");
 try{
  fs.writeFileSync(packet,JSON.stringify(d));
  const p=cp.spawnSync(process.execPath,[ckPath,packet],{encoding:"utf8",timeout:30000,maxBuffer:1<<20});
  const output=p.stdout.trim();
  return p.status===0?
   {accepted:true,originalCLI:JSON.parse(output)}:
   {accepted:false,error:p.stderr.trim().split("\n").slice(0,2).join(" | "),exitCode:p.status};
 }finally{fs.rmSync(tmp,{recursive:true,force:true})}
}
function generate(){
 const cases=[];
 for(let k=1;k<=5;k++){
  const d=build(k),core=mathematical(d),control=mathematical(d,true),cli=nativeCli(d);
  assert(core.accepted);
  assert.equal(control.accepted,k!==2);
  assert.equal(cli.accepted,k!==2);
  assert.equal(d.summary.paid_total,29);
  cases.push({k,m:d.summary.source,W:d.summary.paid_total,records:d.records.length,
   bytes:Buffer.byteLength(JSON.stringify(d)),source:independentSource(d,k),core,control,cli});
 }
 const original=build(3),hostile=[
  ["missing_source",d=>{const i=d.records.findIndex(r=>r.kind==="SOURCE"&&r.source===6);d.records.splice(i,1);d.summary.source--;d.summary.live_records--}],
  ["forged_source",d=>{const r=d.records.find(r=>r.kind==="SOURCE"&&r.source===4);r.c=canon(r.c.map((x,i)=>i===0?-x:x))}],
  ["duplicate_source",d=>{d.records.splice(-1,0,copy(d.records[0]));d.summary.source++;d.summary.live_records++}],
  ["wrong_charge",d=>{d.spec.charge[0]^=1}],
  ["underpayment",d=>{d.summary.paid_total--}],
  ["bad_pivot",d=>{d.records.at(-1).pivot=999999}],
  ["malformed_owner",d=>{d.gate_defs[0][2]=0}],
  ["duplicate_edge",d=>{d.spec.edges[7]=d.spec.edges[6].slice()}],
  ["source_parent",d=>{d.records.find(r=>r.source===7).parents=[0]}]
 ];
 const hostiles=hostile.map(([name,fn])=>{const d=copy(original);fn(d);return{name,...mathematical(d)}});
 assert(hostiles.every(x=>!x.accepted),"a hostile corrupted certificate was accepted");
 const unowned=copy(original);unowned.gate_defs=[];unowned.summary.paid_gates=0;unowned.summary.paid_total=28;
 const legalShortcut={name:"remove_unused_owner",W:28,core:mathematical(unowned),cli:nativeCli(unowned)};
 assert(legalShortcut.core.accepted&&!legalShortcut.cli.accepted);
 return {run:"LSPV3-566-OS-native-independent-replay",archived386Blob:EXPECT_CK,seedBlob:EXPECT_SEED,
   fullHistoricalRmix341Authenticated:false,results:cases,hostiles,legalShortcut,pass:true};
}
const result=generate();
if(process.argv.includes("--write")){
 const target=path.join(ROOT,"results/raw/arc/2026-11-11_0224_LSPV3_566_OS_NODE_REPLAY_RAW.json");
 fs.writeFileSync(target,JSON.stringify(result,null,2)+"\n");
 console.log("written "+target);
}
console.log(JSON.stringify(result,null,2));
