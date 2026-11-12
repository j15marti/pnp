#!/usr/bin/env node
'use strict';
// LSPV-4/568 original checker OS replay, exact archived /386 executable.
// This runner is a future executable control, not proof of historical R_mix341.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const cp=require('node:child_process'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const actual=crypto.createHash('sha256').update(fs.readFileSync(checker)).digest('hex');
assert.equal(actual,'22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113');
const inputs=[
 ['P101_W39',39,'2026-11-12_1236_LSPV4_568_P101_W39_GUARD16_NATIVE386.json'],
 ['P105_W38',38,'2026-11-12_1236_LSPV4_568_P105_W38_GUARD16_NATIVE386.json'],
 ['P105_W39_AREA',39,'2026-11-12_1236_LSPV4_568_P105_W39_AREA_GUARD16_NATIVE386.json'],
];
const result=[];
for(const [name,work,file] of inputs){
  const full=path.join(root,'results/raw/arc',file);
  const parsed=JSON.parse(fs.readFileSync(full,'utf8'));
  assert.equal(parsed.summary.paid_total,work);
  assert.equal(parsed.records.at(-1).kind,'RES');
  assert.deepEqual(parsed.records.at(-1).c,[]);
  const run=cp.spawnSync(process.execPath,[checker,full],
    {encoding:'utf8',maxBuffer:8*1024*1024});
  assert.equal(run.status,0,name+' failed original /386 CLI: '+run.stderr);
  const report=JSON.parse(run.stdout.trim());
  assert.equal(report.negativeTests,11);
  result.push({name,accepted:true,assertions:report.assertions,negativeTests:11,
    bytes:fs.statSync(full).size,sha256:crypto.createHash('sha256')
      .update(fs.readFileSync(full)).digest('hex')});
}
console.log(JSON.stringify({run:'LSPV-4/568',checkerSha256:actual,
  node:process.version,originalOSReplay:result},null,2));
