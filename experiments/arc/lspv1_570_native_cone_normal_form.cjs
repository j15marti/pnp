#!/usr/bin/env node
"use strict";
/* LSPV-1/570, 2026-11-11 04:00 PST.
 * Replays the ORIGINAL archived /386 checker, not historical full R_mix341.
 * node experiments/arc/lspv1_570_native_cone_normal_form.cjs [--write]
 */
const fs=require("node:fs"),path=require("node:path"),crypto=require("node:crypto"),
      assert=require("node:assert/strict"),vm=require("node:vm"),
      os=require("node:os"),cp=require("node:child_process");
const root=path.resolve(__dirname,"../..");
const files={
 checker:"experiments/arc/lspv2_386_independent_verify.js",
 base:"results/raw/arc/2026-11-11_0203_LSPV1_568_K4_DP_CLI29.json",
 active:"results/raw/arc/2026-11-10_2124_LSPV3_561_ARCHIVED_386_NATIVE_PACKET.json",
 nested:"results/raw/arc/2026-11-11_0304_LSPV1_569_NORMALIZED_TWO_OWNER_ACCEPTED_NATIVE_PACKET.json",
 inflated:"results/raw/arc/2026-11-11_0400_LSPV1_570_INFLATED_GUARDED_K4_ACCEPTED_PACKET.json",
 raw:"results/raw/arc/2026-11-11_0400_LSPV1_570_NATIVE_CONE_NORMAL_FORM_RAW.json"
};
const blobs={
 checker:"338305c0ce101704205e57543756b8127074a986",
 base:"e3eb2a46857776089ab83f4ad50159ef622d2869",
 active:"d0fa96a155672f8f6a6a3428eacafa15e79b9e88",
 nested:"d09dafc9a197fb0227b2af7ceeb41675b714acbb"
};
let assertions=0;
function ok(x,m){assert.ok(x,m);assertions++}
const copy=x=>JSON.parse(JSON.stringify(x));
function load(k){
 const buf=fs.readFileSync(path.join(root,files[k]));
 if(blobs[k]){
  let sha=crypto.createHash("sha1").update(Buffer.from("blob "+buf.length+"\0")).update(buf).digest("hex");
  ok(sha===blobs[k],"incorrect exact Git blob "+k+": "+sha);
 }
 return k==="checker"?buf.toString("utf8"):JSON.parse(buf.toString("utf8"));
}
const source=load("checker"),ctx={require,process:{argv:[]},console,structuredClone};
vm.runInNewContext(source+"\n;globalThis.checker = checkProof;",ctx,{filename:files.checker});
const original=ctx.checker;
function pruneCone(obj){
 let p=copy(obj),reach=new Set();
 function visit(i){ok(Number.isInteger(i)&&i>=0&&i<p.records.length,"bad ancestor index");
  if(reach.has(i))return;reach.add(i);p.records[i].parents.forEach(visit)}
 visit(p.records.length-1);
 let keep=p.records.map((r,i)=>r.kind==="SOURCE"||reach.has(i));
 let byWire=new Map(p.gate_defs.map(t=>[t[1],t])),owners=new Set();
 function mark(x){let t=byWire.get(Math.abs(x));
  if(!t||owners.has(t[0]))return;owners.add(t[0]);mark(t[2]);mark(t[3])}
 p.records.forEach((r,i)=>{if(keep[i]){r.c.forEach(mark);if(r.kind==="DEF")owners.add(r.gate)}});
 let oldToNew=new Map(),records=[];
 p.records.forEach((r,i)=>{if(keep[i]){
  let parents=r.parents.map(j=>{ok(oldToNew.has(j),"lost parent");return oldToNew.get(j)});
  oldToNew.set(i,records.length);records.push({...r,parents})}});
 p.records=records;
 p.gate_defs=p.gate_defs.filter(t=>owners.has(t[0]));
 let cnt=k=>records.filter(r=>r.kind===k).length;
 p.summary={source:cnt("SOURCE"),def_views:cnt("DEF"),resolution:cnt("RES"),
  paid_gates:p.gate_defs.length,paid_total:cnt("RES")+p.gate_defs.length,
  live_records:records.length};
 return p;
}
const base=load("base"),active=load("active"),nested=load("nested"),inflated=copy(base);
inflated.gate_defs.push([1,9,8,2],[2,10,9,3]);
inflated.records.splice(inflated.records.length-1,0,
 {kind:"RES",c:[2,3,4,5,-7],parents:[0,4],pivot:1},
 {kind:"DEF",c:[1,-8],parents:[],gate:0},
 {kind:"DEF",c:[8,-9],parents:[],gate:1},
 {kind:"DEF",c:[3,-10],parents:[],gate:2});
inflated.summary={source:17,def_views:3,resolution:29,paid_gates:3,paid_total:32,live_records:49};
ok(JSON.stringify(inflated)===JSON.stringify(load("inflated")),"inflated published byte packet not equal");
let cases={baseline29:base,inflated32:inflated,activeOwner50:active,nestedUnused30:nested};
let result=[];
for(let [name,p] of Object.entries(cases)){
 let before=original(p,{control:true}),q=pruneCone(p),after=original(q,{control:true});
 ok(after.paid<=before.paid,"cost increase");ok(JSON.stringify(pruneCone(q))===JSON.stringify(q),"not idempotent");
 ok(q.summary.source===p.summary.source,"SOURCE lost");ok(JSON.stringify(q.spec)===JSON.stringify(p.spec),"source altered");
 result.push({case:name,work_before:before.paid,work_after:after.paid,
  records_before:before.records,records_after:after.records,
  owners_before:p.gate_defs.length,owners_after:q.gate_defs.length,
  facets_before:p.summary.def_views,facets_after:q.summary.def_views});
}
ok(result[1].work_before===32&&result[1].work_after===28,"wrong 32->28");
ok(result[2].work_before===50&&result[2].work_after===50&&result[2].facets_after===2,"live owner lost");
ok(result[3].work_before===30&&result[3].work_after===28,"wrong 30->28");
function reject(label,mutate){
 const p=pruneCone(active);mutate(p);let fails=false;try{original(p,{control:true})}catch(e){fails=true}
 ok(fails,"hostile control accepted: "+label);return label;
}
let hostile=[
 reject("original source removed",p=>{p.records.shift();p.summary.source--;p.summary.live_records--}),
 reject("live paid owner removed",p=>{p.gate_defs=[];p.summary.paid_gates=0;p.summary.paid_total--}),
 reject("wrong terminal pivot",p=>{p.records.at(-1).pivot=123456}),
 reject("future parent",p=>{p.records.at(-1).parents[0]=p.records.length}),
 reject("underpaid summary",p=>{p.summary.paid_total--})
];
let tmp=fs.mkdtempSync(path.join(os.tmpdir(),"pnp570-")),cli=[];
try{
 for(let [name,p] of Object.entries({...cases,prunedInflated28:pruneCone(inflated),prunedActive50:pruneCone(active),prunedNested28:pruneCone(nested)})){
  let pathname=path.join(tmp,name+".json");
  fs.writeFileSync(pathname,JSON.stringify(p)+"\n");
  let o=cp.spawnSync(process.execPath,[path.join(root,files.checker),pathname],{encoding:"utf8",timeout:15000});
  let entry={case:name,accept:o.status===0,exit_status:o.status};
  if(o.status===0){let k=JSON.parse(o.stdout.trim());entry.work=k.paid;entry.assertions=k.assertions;entry.negative_tests=k.negativeTests}
  else entry.error=(o.stderr||"").trim().split("\n").slice(0,2).join(" | ");
  cli.push(entry);
 }
}finally{fs.rmSync(tmp,{force:true,recursive:true})}
let accepts=new Map(cli.map(x=>[x.case,x.accept]));
ok(accepts.get("baseline29")&&accepts.get("inflated32"),"CLI positive failed");
ok(accepts.get("activeOwner50")&&accepts.get("nestedUnused30"),"original CLI fixture failed");
ok(!accepts.get("prunedInflated28")&&accepts.get("prunedActive50")&&!accepts.get("prunedNested28"),"CLI/core mismatch unexpected");
let raw={date_pst:"2026-11-11 04:00 PST",result:"LSPV-1/570",
 scope:"original archived /386 mathematical checker only",checker_git_blob:blobs.checker,
 seed_git_blobs:blobs,node:process.version,assertions,cases:result,
 hostile_controls:hostile,os_node_complete_cli:cli,
 limitations:["No full historical R_mix341 grammar","Full CLI executes synthetic corruptions, not only inference verification",
 "These are upper bounds, not proof minima","No discovery, span, peak-space or certificate-bit bound"],
 p_versus_np:"OPEN"};
if(process.argv.includes("--write"))fs.writeFileSync(path.join(root,files.raw),JSON.stringify(raw,null,2)+"\n");
console.log(JSON.stringify(raw,null,2));
