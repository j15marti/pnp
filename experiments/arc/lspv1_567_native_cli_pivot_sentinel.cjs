#!/usr/bin/env node
'use strict';
/*
 * LSPV-1/567. Run: node experiments/arc/lspv1_567_native_cli_pivot_sentinel.cjs
 * Executes unchanged archived /386 source (core via vm, full CLI via real Node subprocess).
 * No network dependencies; execute from any current working directory.
 */
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const cp = require('node:child_process');
const crypto = require('node:crypto');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '../..');
const checkerPath = path.join(root, 'experiments/arc/lspv2_386_independent_verify.js');
const seedPath = path.join(root, 'results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json');
const source = fs.readFileSync(checkerPath, 'utf8');
const seedText = fs.readFileSync(seedPath, 'utf8');
function gitBlob(s) {
  const b = Buffer.from(s, 'utf8');
  return crypto.createHash('sha1').update('blob ' + b.length + '\0').update(b).digest('hex');
}
assert.equal(gitBlob(source), '338305c0ce101704205e57543756b8127074a986', 'pinned original checker');
assert.equal(gitBlob(seedText), '08aa169b5db49b2ddd1cb5a9b6890fcc3b790916', 'pinned original source-bound packet');
const seed = JSON.parse(seedText);
const clone = x => JSON.parse(JSON.stringify(x));
function makeBridge(z, reversed) {
  const d = clone(seed), old = d.records.pop(), p = old.pivot, i = d.records.length;
  assert.deepEqual(d.records[old.parents[0]].c, [p]);
  assert.deepEqual(d.records[old.parents[1]].c, [-p]);
  assert.ok(Number.isSafeInteger(z) && z > d.spec.edges.length && z !== d.spec.guard);
  assert.ok(!d.gate_defs.some(g => g[1] === z));
  const id = Math.max(...d.gate_defs.map(g => g[0])) + 1;
  d.gate_defs.push([id, z, p, p]);
  d.records.push(
    {kind:'DEF', c:[p,-z], parents:[], gate:id},
    {kind:'DEF', c:[-p,z], parents:[], gate:id},
    {kind:'RES', c:[z], parents:[old.parents[0],i+1], pivot:p},
    {kind:'RES', c:[-z], parents:[old.parents[1],i], pivot:-p},
    {kind:'RES', c:[], parents:reversed?[i+3,i+2]:[i+2,i+3], pivot:reversed?-z:z}
  );
  d.summary.def_views += 2;
  d.summary.resolution += 2;
  d.summary.paid_gates += 1;
  d.summary.paid_total += 3;
  d.summary.live_records += 4;
  return d;
}
// Preserve the original checker body verbatim and evaluate checkProof from its lexical scope.
const core = vm.runInNewContext(source + '\ncheckProof;', {
  require, process:{argv:['node','checker']}, console:{log(){}}, structuredClone
});
function coreCase(d) {
  try { return {accept:true, outcome:core(d,{control:true})}; }
  catch(e) { return {accept:false, error:String(e)}; }
}
function cliCase(d) {
  const folder = fs.mkdtempSync(path.join(os.tmpdir(), 'pnp567-'));
  try {
    const filename = path.join(folder, 'witness.json');
    fs.writeFileSync(filename, JSON.stringify(d));
    const run = cp.spawnSync(process.execPath, [checkerPath, filename], {
      encoding:'utf8', timeout:30000, maxBuffer:10485760
    });
    assert.equal(run.error, undefined, 'native subprocess failed');
    return {accept:run.status === 0, exit:run.status,
      stdout:run.stdout.trim(), stderr:run.stderr.trim()};
  } finally { fs.rmSync(folder,{recursive:true,force:true}); }
}
function sourceModels(d) {
  const cs = d.records.filter(r => r.kind==='SOURCE').map(r => r.c);
  const variables = d.spec.guard;
  assert.equal(variables,7,'source K4 exact width');
  let total = 0;
  for(let assignment=0;assignment<2**variables;assignment++){
    const holds=cs.every(cl=>cl.some(l=>{const bit=(assignment>>(Math.abs(l)-1))&1;return l>0?bit===1:bit===0}));
    if(holds)total++;
  }
  return total;
}
function ancestry(d) {
  const seen=new Set();
  function visit(i){if(seen.has(i))return;seen.add(i);for(const j of d.records[i].parents)visit(j)}
  visit(d.records.length-1);
  const out={};
  for(const k of ['SOURCE','DEF','RES'])out[k]=d.records.filter((r,i)=>seen.has(i)&&r.kind===k).length;
  return out;
}
const plus=makeBridge(999999,false), minus=makeBridge(999999,true), nearby=makeBridge(1000000,false);
const bad={
  wrongSign:clone(minus), wrongFacet:clone(minus),
  wrongSource:clone(minus), underpayment:clone(minus)
};
bad.wrongSign.records.at(-1).pivot=999999;
bad.wrongFacet.records[73].c=[-6,-999999];
bad.wrongSource.records[0].c=[-7];
bad.underpayment.summary.paid_total--;
const cases={seed:{core:coreCase(seed),cli:cliCase(seed)},
  positive999999:{core:coreCase(plus),cli:cliCase(plus)},
  negative999999:{core:coreCase(minus),cli:cliCase(minus)},
  positive1000000:{core:coreCase(nearby),cli:cliCase(nearby)}};
assert.equal(sourceModels(seed),0);
assert.equal(sourceModels(plus),0);
assert.equal(cases.positive999999.core.accept,true);
assert.equal(cases.positive999999.cli.accept,false);
assert.match(cases.positive999999.cli.stderr,/accepted a corrupted proof/);
assert.equal(cases.negative999999.core.accept,true);
assert.equal(cases.negative999999.cli.accept,true);
assert.equal(cases.positive1000000.cli.accept,true);
for(const [name,x] of Object.entries(bad)) {
  const r=coreCase(x);assert.equal(r.accept,false,name);
}
assert.equal(cases.positive999999.core.outcome.paid,56);
assert.equal(cases.negative999999.core.outcome.paid,56);
assert.deepEqual(ancestry(plus),{SOURCE:17,DEF:6,RES:53});
assert.deepEqual(ancestry(minus),{SOURCE:17,DEF:6,RES:53});
const out={status:'PASS',source_models:0,checker_git_blob:gitBlob(source),
 seed_git_blob:gitBlob(seedText),cases,negative_controls:Object.fromEntries(
 Object.entries(bad).map(([name,x])=>[name,coreCase(x)])),
 ancestry:ancestry(plus)};
console.log(JSON.stringify(out,null,2));
