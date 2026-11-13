#!/usr/bin/env node
/* LSPV-5/527: source-binding and all-algorithm transfer audit for /341. */
'use strict';
const fs = require('fs');
const crypto = require('crypto');
const {spawnSync} = require('child_process');

const checker = 'experiments/arc/lspv2_341_independent_verify.js';
const packet = 'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json';
const satPath = '/tmp/lspv5_527_sat.cnf';
const unsatPath = '/tmp/lspv5_527_unsat.cnf';
const satCNF = 'p cnf 1 1\n1 0\n';
const unsatCNF = 'p cnf 1 2\n1 0\n-1 0\n';
fs.writeFileSync(satPath, satCNF);
fs.writeFileSync(unsatPath, unsatCNF);

function sha(x){return crypto.createHash('sha256').update(x).digest('hex');}
function run(extra){
  const r=spawnSync(process.execPath,[checker,packet,...extra],{encoding:'utf8'});
  return {status:r.status,stdout:r.stdout,stderr:r.stderr,accepted:r.status===0};
}
const base=run([]), withSat=run([satPath]), withUnsat=run([unsatPath]);
if(!base.accepted || !withSat.accepted || !withUnsat.accepted) throw Error('positive replay failed');
if(base.stdout!==withSat.stdout || base.stdout!==withUnsat.stdout) throw Error('external source affected checker');

const checkerText=fs.readFileSync(checker,'utf8');
const argvRefs=[...checkerText.matchAll(/process\.argv\[(\d+)\]/g)].map(m=>Number(m[1]));
if(JSON.stringify([...new Set(argvRefs)])!=='[2]') throw Error('checker interface changed');

// Control: an in-packet source corruption is rejected, separating internal fixture checks
// from the absent external-F binding.
const obj=JSON.parse(fs.readFileSync(packet,'utf8'));
obj.fixtures[0].clauses[0].literals[0]=999;
const badPath='/tmp/lspv5_527_bad_embedded_source.json';
fs.writeFileSync(badPath,JSON.stringify(obj));
const bad=spawnSync(process.execPath,[checker,badPath],{encoding:'utf8'});
if(bad.status===0) throw Error('embedded source corruption unexpectedly accepted');

const parsed=JSON.parse(base.stdout);
const out={
  run:'LSPV-5/527',
  status:'PASS_RESTRICTED_INTERNAL_SOURCE; FAIL_EXTERNAL_SOURCE_BOUND_D1; OPEN_B2_B3',
  checker:{path:checker,sha256:sha(fs.readFileSync(checker)),argv_indices:[...new Set(argvRefs)]},
  packet:{path:packet,bytes:fs.statSync(packet).size,sha256:sha(fs.readFileSync(packet)),fixtures:parsed.cases.length,checks:parsed.checks},
  replays:[
    {label:'baseline',extra_argv:[],accepted:base.accepted,stdout_sha256:sha(base.stdout)},
    {label:'SAT_external_sidecar',formula:satCNF,formula_sha256:sha(satCNF),extra_argv:[satPath],accepted:withSat.accepted,stdout_sha256:sha(withSat.stdout)},
    {label:'UNSAT_external_sidecar',formula:unsatCNF,formula_sha256:sha(unsatCNF),extra_argv:[unsatPath],accepted:withUnsat.accepted,stdout_sha256:sha(withUnsat.stdout)}
  ],
  identical_stdout:true,
  embedded_bad_source_control:{accepted:bad.status===0,exit_status:bad.status,stderr_first_line:(bad.stderr||'').split(/\n/)[0]},
  finding:'The one-argument /341 program validates only its embedded fixture object. It does not define or authenticate V(F,pi) for an independently supplied CNF F; a third source argument is ignored. Reusing this accepted packet beside a satisfiable external F therefore defeats any wrapper that claims the unchanged checker is already a source-bound arbitrary-SAT refutation verifier.',
  scope:'This does not show the embedded K4/PRISM computations are logically wrong. It falsifies the stronger D1 external-source-binding/coverage claim for the unchanged checker. Any wrapper that binds F is a new construction requiring separate soundness, coverage, and cost proofs.',
  transfer_obligation:'For every correct deterministic polynomial-time SAT decider A, one still needs a same-calculus constructor with W_R(F) <= c_A (|F|+T_A(|F|))^r_A for every UNSAT F. No such all-A theorem is supplied or tested by this checker.',
  p_vs_np:'OPEN'
};
console.log(JSON.stringify(out,null,2));
