#!/usr/bin/env node
'use strict';
/* LSPV-1/580. Original-/386 source-pinned signed weakening, OS replay.
 * Run from a full j15marti/pnp checkout:
 * node experiments/arc/lspv1_580_native_two_res_weakening.cjs
 * No full R_mix341 mixed-rule checker is claimed.
 */
const fs=require('fs'),path=require('path'),crypto=require('crypto'),cp=require('child_process');
const assert=require('assert/strict'),os=require('os');
const repo=process.cwd();
const seed=path.join(repo,'results/raw/arc/2026-11-11_1200_LSPV1_579_BRIDGE_DP_W61.json');
const checker=path.join(repo,'experiments/arc/lspv2_386_independent_verify.js');
const target=path.join(repo,'results/raw/arc/2026-11-11_1256_LSPV1_580_NATIVE_TWO_RES_WEAKENING_PACKET.json');
const git=b=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\\0'),b])).digest('hex');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
assert.equal(git(fs.readFileSync(seed)),'807aaf7b7cf5e4a4feb29c2599f9e582ea140e30');
assert.equal(git(fs.readFileSync(checker)),'338305c0ce101704205e57543756b8127074a986');
const original=JSON.parse(fs.readFileSync(seed,'utf8'));
assert.equal(original.records.length,101);
assert.equal(original.summary.paid_total,61);
assert.deepEqual(original.gate_defs,[[0,17,1,2]]);
assert.deepEqual(original.records[13].c,[1,-4,6,-16]);
const rows=original.records;
const added=[
 {kind:'DEF',gate:0,c:[-1,-2,17],parents:[]},
 {kind:'DEF',gate:0,c:[1,-17],parents:[]},
 {kind:'RES',c:[-2,-4,6,-16,17],parents:[13,100],pivot:1},
 {kind:'RES',c:[1,-2,-4,6,-16],parents:[102,101],pivot:17}
];
const packet={...original,records:[...rows.slice(0,-1),...added,rows.at(-1)],
 summary:{...original.summary,resolution:62,def_views:2,paid_total:63,live_records:105}};
const payload=Buffer.from(JSON.stringify(packet)+'\\n');
assert.equal(payload.length,6755);
assert.equal(fs.readFileSync(target).equals(payload),true,'published packet differs');
const exec=f=>cp.spawnSync(process.execPath,[checker,f],{encoding:'utf8',timeout:10000});
const valid=exec(target);
assert.equal(valid.status,0,valid.stderr);
const evidence=JSON.parse(valid.stdout.trim().split('\\n').at(-1));
for(const [k,v] of Object.entries({paid:63,res:62,def:1,records:105,sources:41,negativeTests:11}))
 assert.equal(evidence[k],v,'checker field '+k);
const corrupt={
 source:d=>d.records[13].c[0]*=-1,
 facet:d=>d.records[100].c[0]*=-1,
 pivot1:d=>d.records[102].pivot=2,
 pivot2:d=>d.records[103].pivot=1,
 parent:d=>d.records[102].parents[1]=104,
 undercharge:d=>d.summary.paid_total=62,
 terminal:d=>d.records[104].c=[16]
};
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv1-580-')),rejections={};
try {
 for(const [name,edit] of Object.entries(corrupt)){
  const d=structuredClone(packet);edit(d);
  const f=path.join(dir,name+'.json');fs.writeFileSync(f,JSON.stringify(d)+'\\n');
  const out=exec(f);rejections[name]=out.status!==0;
  assert.equal(rejections[name],true,'hostile accepted '+name);
 }
} finally {fs.rmSync(dir,{recursive:true,force:true})}
console.log(JSON.stringify({status:'PASS',id:'LSPV-1/580',scope:'original archived /386 ONLY',
 previous_paid:61,constructed_paid:63,work_added:2,
 source_clause:[1,-4,6,-16],output_clause:[1,-2,-4,6,-16],
 source_unchanged:true,checker_git_blob:git(fs.readFileSync(checker)),
 packet_git_blob:git(payload),packet_sha256:sha(payload),
 full_original_cli:evidence,hostile_controls:rejections},null,2));
