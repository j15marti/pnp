#!/usr/bin/env node
"use strict";
// LSPV-3/575. Original /386 accepted-byte checker, NOT full historical R_mix341.
// Node 18+: node experiments/arc/lspv3_575_charge_compensated_source_symmetry.cjs [--write]
// Uses the unchanged archived original checker as an operating-system subprocess.
const fs=require("node:fs"), path=require("node:path"),os=require("node:os");
const cp=require("node:child_process"), crypto=require("node:crypto"),assert=require("node:assert/strict");
const root=path.resolve(__dirname,"../..");
const checkerPath=path.join(root,"experiments/arc/lspv2_386_independent_verify.js");
const seedPath=path.join(root,"results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json");
const blob=x=>crypto.createHash("sha1").update("blob "+Buffer.byteLength(x)+"\\0").update(x).digest("hex");
const checker=fs.readFileSync(checkerPath,"utf8"),source=fs.readFileSync(seedPath,"utf8");
assert.equal(blob(checker),"338305c0ce101704205e57543756b8127074a986");
assert.equal(blob(source),"08aa169b5db49b2ddd1cb5a9b6890fcc3b790916");
const base=JSON.parse(source),edges=base.spec.edges,b=base.spec.charge,E=edges.length;
const clone=x=>JSON.parse(JSON.stringify(x)),canon=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
const perms=a=>a.length?a.flatMap((v,i)=>perms(a.filter((_,j)=>j!==i)).map(p=>[v,...p])):[[]];
const sigmas=perms([0,1,2,3]);
function valid(s,f){return b.every((bit,v)=>{let q=0;edges.forEach(([a,z],e)=>{if(a===v||z===v)q^=(f>>e)&1});return (bit^q)===b[s[v]]})}
const lifts=sigmas.flatMap(s=>Array.from({length:1<<E},(_,f)=>({s,f})).filter(x=>valid(x.s,x.f)));
function edgePerm(s){return edges.map(([u,v])=>edges.findIndex(([a,z])=>a===Math.min(s[u],s[v])&&z===Math.max(s[u],s[v])))}
function action(p,s,f){
 const ep=edgePerm(s);assert(!ep.includes(-1));
 const lit=x=>Math.abs(x)>E?x:Math.sign(x)*(f&(1<<(Math.abs(x)-1))?-1:1)*(ep[Math.abs(x)-1]+1);
 const sourceIndex=new Map(p.records.map((r,i)=>[r.source+":"+JSON.stringify(r.c),i]).filter(([_,i])=>p.records[i].kind==="SOURCE"));
 const redirect=new Map();
 p.records.forEach((r,i)=>{if(r.kind!=="SOURCE")return;
  const j=sourceIndex.get((r.source<0?-1:s[r.source])+":"+JSON.stringify(canon(r.c.map(lit))));
  if(j===undefined)throw Error("no authenticated source-clause bijection");redirect.set(i,j);
 });
 assert.equal(new Set(redirect.values()).size,redirect.size);
 const q=clone(p);
 q.gate_defs=q.gate_defs.map(([id,z,a,y])=>[id,z,lit(a),lit(y)]);
 q.records=q.records.map(r=>{if(r.kind==="SOURCE")return r;
  const a=clone(r);a.c=canon(r.c.map(lit));if(r.kind==="RES")a.pivot=lit(r.pivot);
  a.parents=r.parents.map(j=>p.records[j].kind==="SOURCE"?redirect.get(j):j);return a;
 });
 return q;
}
function result(packet,tmp){
 const file=path.join(tmp,"packet.json");fs.writeFileSync(file,JSON.stringify(packet));
 const r=cp.spawnSync(process.execPath,[checkerPath,file],{encoding:"utf8",timeout:15000,maxBuffer:2e6});
 if(r.error)throw r.error;
 if(r.status!==0)return {accepted:false,error:(r.stderr||"").trim().split("\\n").at(-1)};
 const o=JSON.parse(r.stdout);return {accepted:true,paid:o.paid,assertions:o.assertions,negativeTests:o.negativeTests};
}
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),"pnp-lspv3-575-"));
try {
 const rows=[],bad=[],b0=result(base,tmp);
 assert(b0.accepted&&b0.paid===53);
 for(const {s,f} of lifts){
  const p=action(base,s,f),r=result(p,tmp);
  assert(r.accepted&&r.paid===53&&r.assertions===4663,"native failed "+s+" mask "+f+": "+r.error);
  assert.deepEqual(p.records.filter(x=>x.kind==="SOURCE"),base.records.filter(x=>x.kind==="SOURCE"));
  rows.push({sigma:s,mask:f,...r});
 }
 assert.equal(lifts.length,192);
 assert.equal(new Set(lifts.map(({s,f})=>JSON.stringify(action(base,s,f)))).size,192);
 const byKey=new Set(lifts.map(x=>x.s.join(",")+"|"+x.f));let group=0;
 for(const x of lifts)for(const y of lifts){
  const ep=edgePerm(x.s),s=x.s.map(v=>y.s[v]);let f=x.f;
  for(let e=0;e<E;e++)if(y.f&(1<<ep[e]))f^=(1<<e);
  assert(byKey.has(s.join(",")+"|"+f));group++;
 }
 assert.equal(group,36864);
 const example=lifts.find(x=>x.s[0]!==0);
 for(const [name,mut] of [
  ["invalid pivot",p=>p.records.find(r=>r.kind==="RES").pivot=123],
  ["forged SOURCE",p=>p.records.find(r=>r.kind==="SOURCE").c[0]*=-1],
  ["bad parent",p=>p.records.find(r=>r.kind==="RES").parents[0]=999],
  ["underpaid",p=>p.summary.paid_total--],
  ["foreign AND3",p=>p.records.find(r=>r.kind==="RES").kind="AND3"],
  ["wire collision",p=>p.gate_defs[1][1]=p.gate_defs[0][1]]
 ]){
  const p=action(base,example.s,example.f);mut(p);let r=result(p,tmp);
  assert(!r.accepted,"accepted "+name);bad.push({name,...r});
 }
 const summary={run:"LSPV-3/575 ORIGINAL_NODE_OS_REPLAY",checker_git_blob:blob(checker),seed_git_blob:blob(source),
  model:"original archived /386 SOURCE/DEF/RES full CLI, NOT historical mixed R_mix341",
  accepted:rows.length,charge_moving:rows.filter(x=>x.s[0]!==0).length,distinct:192,
  group_composition:group,negative_rejections:bad.length,paid:53,source_records_unchanged:true,results:rows,hostiles:bad};
 console.log(JSON.stringify(summary,null,2));
 if(process.argv.includes("--write")){
  fs.writeFileSync(path.join(root,"results/raw/arc/2026-11-11_1124_LSPV3_575_CHARGE_COMPENSATED_NODE_OS_RAW.json"),JSON.stringify(summary,null,2)+"\\n");
  fs.writeFileSync(path.join(root,"results/raw/arc/2026-11-11_1124_LSPV3_575_CHARGE_MOVING_ACCEPTED_PACKET.json"),JSON.stringify(action(base,example.s,example.f))+"\\n");
 }
} finally {fs.rmSync(tmp,{recursive:true,force:true})}
