#!/usr/bin/env node
'use strict';
/*
 * LSPV-3/585. Execute from j15marti/pnp root:
 *   node experiments/arc/lspv3_585_native386_facet_interleaving.cjs
 *
 * Replays the unchanged original archived /386 CLI as a separate Node OS
 * subprocess.  The source code and exact starting packet are Git-blob pinned.
 * No replacement verifier is used to decide any acceptance.
 */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const {spawnSync} = require('node:child_process');
const root = path.resolve(__dirname, '..', '..');
const checkerPath = path.join(root, 'experiments/arc/lspv2_386_independent_verify.js');
const seedPath = path.join(root, 'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json');
const outputDir = process.argv[2] ? path.resolve(process.argv[2]) : path.join(root, 'results/raw/arc');
const rawName = '2026-11-12_0224_LSPV3_585_INTERLEAVING_NATIVE_OS_RAW.json';
const witnessName = '2026-11-12_0224_LSPV3_585_INTERLEAVED_K4_ACCEPTED.json';
function gitBlob(buffer) {
  return crypto.createHash('sha1').update(Buffer.from('blob ' + buffer.length + '\0')).update(buffer).digest('hex');
}
function sha256(buffer) { return crypto.createHash('sha256').update(buffer).digest('hex'); }
const checkerBytes = fs.readFileSync(checkerPath), seedBytes = fs.readFileSync(seedPath);
assert.equal(gitBlob(checkerBytes), '338305c0ce101704205e57543756b8127074a986', 'checker changed');
assert.equal(gitBlob(seedBytes), '318c52d99977ea4e91bc8554051138a700c1dc94', 'seed changed');
const seed = JSON.parse(seedBytes);
const originalRecords = JSON.stringify(seed.records);
const originalSpec = JSON.stringify(seed.spec);
const N = seed.records.length;
assert.equal(N, 45);
assert.deepEqual(seed.gate_defs, [[0,8,1,4]]);
assert.equal(seed.summary.paid_total,29);
function interleave(slots) {
  const chosen = [...slots].sort((a,b)=>a-b);
  assert(chosen.every(x=>Number.isInteger(x)&&x>=0&&x<N), 'slot outside preterminal range');
  const out = structuredClone(seed);
  const shift = oldIndex => oldIndex + chosen.filter(j=>j<=oldIndex).length;
  out.records = [];
  for (let i=0;i<N;i++) {
    for (let j=0;j<chosen.length;j++) if (chosen[j]===i)
      out.records.push({kind:'DEF',gate:0,c:[1,-8],parents:[]});
    const old = structuredClone(seed.records[i]);
    old.parents = old.parents.map(shift);
    out.records.push(old);
  }
  out.summary.def_views += chosen.length;
  out.summary.live_records += chosen.length;
  assert.equal(JSON.stringify(out.spec), originalSpec);
  assert.equal(out.summary.paid_total, 29);
  return out;
}
const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'pnp-lspv3-585-'));
function replay(packet,label,expectAccept) {
  const body = Buffer.from(JSON.stringify(packet)+'\n','utf8');
  const file = path.join(tmpDir, 'case.json');
  fs.writeFileSync(file, body);
  const child = spawnSync(process.execPath,[checkerPath,file],{
    cwd:root,encoding:'utf8',timeout:20000,maxBuffer:1024*1024
  });
  const accepted = child.status===0 && !child.error;
  assert.equal(accepted,expectAccept,
    label + ' unexpected original-CLI verdict: ' + (child.error||child.stderr));
  let result=null;
  if(accepted){
    const lines = child.stdout.trim().split(/\r?\n/);
    result = JSON.parse(lines.at(-1));
    assert.equal(result.paid,29,label+' paid work');
    assert.equal(result.def,1,label+' paid gate ownership');
    assert.equal(result.res,28,label+' Resolution count');
    assert.equal(result.sources,17,label+' SOURCE count');
    assert.equal(result.negativeTests,11,label+' built-in hostile battery');
  }
  return {
    label,accepted,exit_status:child.status,bytes:body.length,
    packet_sha256:sha256(body),
    paid:result?.paid??null,
    records:result?.records??null,
    original_assertions:result?.assertions??null,
    negative_tests:result?.negativeTests??null,
    error:accepted?null:((child.stderr||String(child.error)).trim().split('\n')[0])
  };
}
const cases=[];
try {
  cases.push(replay(seed,'baseline',true));
  for(let s=0;s<N;s++)cases.push(replay(interleave([s]),'k1_slot_'+s,true));
  const doubles=[[0,0],[0,44],[1,22],[12,12],[15,16],[22,44],[44,44],[1,43]];
  for(const [a,b] of doubles) cases.push(replay(interleave([a,b]),'k2_'+a+'_'+b,true));
  const four=interleave([0,5,19,44]);
  cases.push(replay(four,'k4_mixed',true));
  fs.mkdirSync(outputDir,{recursive:true});
  fs.writeFileSync(path.join(outputDir,witnessName),JSON.stringify(four)+'\n');
  const hostile = [
    ['invalid_facet',x=>{x.records[0].c=[1,-9];}],
    ['foreign_owner',x=>{x.records[0].gate=123;}],
    ['facet_with_parent',x=>{x.records[0].parents=[0];}],
    ['underreported_facets',x=>{x.summary.def_views=3;}],
    ['underreported_records',x=>{x.summary.live_records=N+3;}],
    ['bad_final_parent',x=>{x.records.at(-1).parents[1]=0;}],
    ['forged_source',x=>{x.records[1].c=[-1,-2,-3,-7];}],
    ['invalid_facet_literal',x=>{x.records[0].c=[1,-8,-6];}]
  ];
  for(const [name,mutate] of hostile) {
    const packet=structuredClone(four);mutate(packet);
    cases.push(replay(packet,'reject_'+name,false));
  }
  const positives=cases.filter(x=>x.accepted),rejects=cases.filter(x=>!x.accepted);
  assert.equal(positives.length,55);
  assert.equal(rejects.length,8);
  const result={
    run:'LSPV-3/585',time_zone:'America/Los_Angeles',
    scope:'unchanged original archived /386 Node OS subprocess, NOT R_mix341',
    checker_blob:gitBlob(checkerBytes),seed_blob:gitBlob(seedBytes),
    original_spec_sha256:sha256(Buffer.from(originalSpec)),
    original_records_sha256:sha256(Buffer.from(originalRecords)),
    theorem:'arbitrary zero-cost DEF interleaving with source/DAG identity and chronological parent rebasing',
    N,slot_count:N,k1_all:N,k2_selected:doubles.length,
    k4_slots:[0,5,19,44],
    k2_distinct_interleavings:(N*(N+1))/2,
    positives:positives.length,hostile_rejects:rejects.length,
    original_assertion_groups:positives.reduce((a,x)=>a+x.original_assertions,0),
    cases
  };
  fs.writeFileSync(path.join(outputDir,rawName),JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify({positives:result.positives,rejected:result.hostile_rejects,
    original_assertions:result.original_assertion_groups,witness:path.join(outputDir,witnessName),
    raw:path.join(outputDir,rawName)}));
} finally {fs.rmSync(tmpDir,{recursive:true,force:true});}
