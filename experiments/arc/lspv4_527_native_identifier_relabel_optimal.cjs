#!/usr/bin/env node
"use strict";
/*
LSPV-4/527, exact native-/341 fixture string-ID relabeling.
Reproducible from j15marti/pnp repository root:
 node experiments/arc/lspv4_527_native_identifier_relabel_optimal.cjs [raw.json]
The ORIGINAL /341 producer/verifier are pinned and their bodies are not edited.
Scope: the recovered SOURCE/AND3/XOR fixture's STRING-ID sublanguage,
NOT the full historical R_mix341 accepted-byte calculus.
*/
const fs=require("fs"), path=require("path"), crypto=require("crypto");
const ROOT=path.resolve(__dirname,"../..");
const PRODUCER="experiments/arc/lspv2_341_mixed_tseitin_min_dag.js";
const CHECKER="experiments/arc/lspv2_341_independent_verify.js";
const PINS={producer:"4081022e8a3841d79f751a3d3a7a10decbb026da",
             checker:"fcb7d4ced8f922de14c0bda16263a8cc7853e8e0"};
const ALPHABET="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
function assert(x,msg){if(!x)throw Error("LSPV4/527 "+msg);}
function clone(x){return JSON.parse(JSON.stringify(x));}
function codewords(n){
  assert(Number.isSafeInteger(n)&&n>=0,"invalid codeword count");
  const out=[];
  for(let len=1;out.length<n;len++){
    // Only as many candidates as necessary are generated.
    const limit=Math.min(Math.pow(62,len),n-out.length);
    for(let i=0;i<limit;i++){
      let j=i,s="";
      for(let k=0;k<len;k++){s=ALPHABET[j%62]+s;j=Math.floor(j/62);}
      out.push(s);
    }
  }
  return out;
}
function frequency(f){
  const map=new Map(),add=id=>{
    assert(typeof id==="string"&&id.length>0,"nonstring or empty ID is outside certified sublanguage");
    assert(/^[0-9A-Za-z]+$/.test(id),"escaped/punctuated ID outside certified sublanguage");
    map.set(id,(map.get(id)||0)+1);
  };
  for(const c of f.clauses)add(c.id);
  for(const p of f.proof){add(p.id);for(const id of p.parents)add(id);}
  for(const d of f.deleted)add(d.sourceId);
  const defined=new Set(f.clauses.map(x=>x.id).concat(f.proof.map(x=>x.id)));
  assert(defined.size===f.clauses.length+f.proof.length,"nonunique IDs in packet");
  assert([...map.keys()].every(k=>defined.has(k)),"unresolved reference");
  return map;
}
function optimize(f){
  const fr=frequency(f);
  const ordered=[...fr.keys()].sort((a,b)=>fr.get(b)-fr.get(a)||a.localeCompare(b));
  const labels=codewords(ordered.length);
  const remap=new Map(ordered.map((s,i)=>[s,labels[i]]));
  const out=clone(f);
  for(const c of out.clauses)c.id=remap.get(c.id);
  for(const p of out.proof){p.id=remap.get(p.id);p.parents=p.parents.map(x=>remap.get(x));}
  for(const d of out.deleted)d.sourceId=remap.get(d.sourceId);
  const oldCharge=ordered.reduce((z,id)=>z+fr.get(id)*id.length,0);
  const minCharge=ordered.reduce((z,id,i)=>z+fr.get(id)*labels[i].length,0);
  const before=Buffer.byteLength(JSON.stringify(f),"utf8");
  const after=Buffer.byteLength(JSON.stringify(out),"utf8");
  assert(after-before===minCharge-oldCharge,"exact byte difference failed");
  assert(frequency(out).size===fr.size,"bijection failed");
  return {out,metrics:{
    name:f.graph.name,distinct_identifiers:fr.size,
    identifier_occurrences:[...fr.values()].reduce((a,b)=>a+b,0),
    paid_nodes:f.proof.length,
    original_bytes:before,optimized_bytes:after,saved_bytes:before-after,
    original_identifier_bytes:oldCharge,minimum_identifier_bytes:minCharge,
    exact_delta_verified:true
  }};
}
function nativeChecker(originalVerifier,packet){
  const records=[];
  try {
    // Original checker function body, only CLI I/O replaced.
    new Function("require","process","console",originalVerifier)(
      ()=>({readFileSync:()=>JSON.stringify(packet)}),
      {argv:["node","original-verifier","packet.json"]},
      {log:s=>records.push(s)});
    return {accepted:true,assertions:JSON.parse(records[0]).checks};
  } catch(e){return {accepted:false,why:String(e).slice(0,180)};}
}
function testOptimality(){
  // Exhaustively enumerate every assignment of four available lengths.
  const weights=[4,3,2,1],lengths=[1,1,2,3],a=[0,1,2,3];
  let minimum=Infinity,count=0;
  function rec(i){
    if(i===a.length){count++;const cost=a.reduce((s,j,k)=>s+weights[k]*lengths[j],0);
      if(cost<minimum)minimum=cost;return;}
    for(let k=i;k<a.length;k++){[a[k],a[i]]=[a[i],a[k]];rec(i+1);[a[k],a[i]]=[a[i],a[k]];}
  }
  rec(0);
  const exchangeOpt=weights.reduce((s,w,i)=>s+w*lengths[i],0);
  assert(minimum===exchangeOpt&&count===24,"exhaustive assignment exchange lemma");
  return {assignments:count,minimum,exchangeOpt};
}
function run(producer,verifier){
  const outs=[];new Function("console",producer)({log:s=>outs.push(s)});
  assert(outs.length===1,"producer did not emit exactly one packet");
  const orig=JSON.parse(outs[0]),opt=clone(orig),stats=[];
  const base=nativeChecker(verifier,orig);
  assert(base.accepted&&base.assertions===30714,"original historical fixture baseline drift");
  for(let i=0;i<orig.fixtures.length;i++){
    const o=optimize(orig.fixtures[i]);opt.fixtures[i]=o.out;stats.push(o.metrics);
  }
  const compressed=nativeChecker(verifier,opt);
  assert(compressed.accepted&&compressed.assertions===base.assertions,"relabelled proof rejected");
  const totalBytesOriginal=Buffer.byteLength(JSON.stringify(orig));
  const totalBytesOptimized=Buffer.byteLength(JSON.stringify(opt));
  const saved=stats.reduce((s,x)=>s+x.saved_bytes,0);
  assert(totalBytesOriginal-totalBytesOptimized===saved,"aggregate formula failed");
  const badParent=clone(opt);badParent.fixtures[0].proof[0].parents[0]="NoSuchID";
  assert(!nativeChecker(verifier,badParent).accepted,"bad parent accepted");
  const duplicate=clone(opt);duplicate.fixtures[0].proof[0].id=duplicate.fixtures[0].proof[1].id;
  assert(!nativeChecker(verifier,duplicate).accepted,"duplicate paid ID accepted");
  const badSource=clone(opt);badSource.fixtures[0].clauses[0].literals[0]=999;
  assert(!nativeChecker(verifier,badSource).accepted,"corrupted source accepted");
  const badTable=clone(opt);badTable.fixtures[0].proof[0].table^=1;
  assert(!nativeChecker(verifier,badTable).accepted,"false AND3 accepted");
  const badWitness=clone(opt);
  badWitness.fixtures[0].deleted[0].assignment=
    badWitness.fixtures[0].deleted[0].assignment.replace(/^./,x=>x==="0"?"1":"0");
  assert(!nativeChecker(verifier,badWitness).accepted,"corrupted deletion witness accepted");
  const illegal=clone(opt);illegal.fixtures[0].proof[0].id=3.14;
  let typedReject=false;try{optimize(illegal.fixtures[0]);}catch(e){typedReject=true;}
  assert(typedReject,"unsafe numeric ID was normalized without semantic proof");
  // accepted 16KiB STRING-ID stress, then optimal recovery, zero change in paid nodes.
  const stressed=clone(orig),f=stressed.fixtures[0],old=f.clauses[0].id;
  const longID="Q".repeat(16384);
  for(const c of f.clauses)if(c.id===old)c.id=longID;
  for(const p of f.proof)p.parents=p.parents.map(x=>x===old?longID:x);
  for(const d of f.deleted)if(d.sourceId===old)d.sourceId=longID;
  const longPacket=nativeChecker(verifier,stressed);
  assert(longPacket.accepted&&longPacket.assertions===30714,"long string ID rejected");
  const longBytes=Buffer.byteLength(JSON.stringify(f)),restored=optimize(f);
  assert(restored.metrics.optimized_bytes===stats[0].optimized_bytes,"long-ID optimum drift");
  stressed.fixtures[0]=restored.out;
  assert(nativeChecker(verifier,stressed).accepted,"restored short-ID packet rejected");
  const exhaustive=testOptimality();
  return {
    experiment:"LSPV-4/527 cost-optimal STRING-ID relabeling in recovered /341 fixture",
    status:["PROVED/RESTRICTED","COMPUTATIONAL"],native_checker_scope:"SOURCE/AND3/XOR fixture only",
    baseline_native_assertions:base.assertions,optimized_native_assertions:compressed.assertions,
    graph_fixtures:stats.length,total_packet_original_bytes:totalBytesOriginal,
    total_packet_optimized_bytes:totalBytesOptimized,total_bytes_saved:saved,
    fixtures:stats,negative_controls:["missing_parent","collision","corrupt_original_clause",
       "wrong_AND3","corrupt_deletion_witness","unsupported_numeric_ID"],
    accepted_long_ID_stress:{id_length:16384,K4_packet_bytes:longBytes,
      K4_reoptimized_bytes:restored.metrics.optimized_bytes,paid_nodes:f.proof.length},
    exhaustive_exchange_control:exhaustive,
    proof_scope:"all finite name-bijective certificates in explicit 62-character string-ID grammar",
    limitations:"does not authenticate native RES/DEF/LOCAL-CONVERT/CASE/joins or any per-reference tariff"
  };
}
function gitBlob(text){return crypto.createHash("sha1")
 .update(Buffer.from("blob "+Buffer.byteLength(text)+"\0"+text)).digest("hex");}
if(require.main===module){
  const producer=fs.readFileSync(path.join(ROOT,PRODUCER),"utf8");
  const verifier=fs.readFileSync(path.join(ROOT,CHECKER),"utf8");
  assert(gitBlob(producer)===PINS.producer&&gitBlob(verifier)===PINS.checker,
    "pinned source drift");
  const results=run(producer,verifier);
  const out=process.argv[2];
  if(out){fs.mkdirSync(path.dirname(out),{recursive:true});
    fs.writeFileSync(out,JSON.stringify(results,null,2)+"\n");}
  process.stdout.write(JSON.stringify(results,null,2)+"\n");
}
module.exports={run,optimize,codewords,frequency};
