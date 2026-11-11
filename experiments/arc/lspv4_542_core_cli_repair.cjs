#!/usr/bin/env node
'use strict';
/*
 * LSPV-4/542, 2026-11-11 05:36 PST.
 * Independent OS-Node differential for the unchanged archived /386 checker.
 * Usage: node experiments/arc/lspv4_542_core_cli_repair.cjs [output.json]
 * Read-only checker and seeds are pinned by Git blob identity. No change to
 * the checker or its original mathematical/eleven negative control bodies.
 */
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const crypto = require('node:crypto');
const vm = require('node:vm');
const cp = require('node:child_process');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '../..');
const checkerRel = 'experiments/arc/lspv2_386_independent_verify.js';
const seedRel = 'results/raw/arc/2026-11-11_0203_LSPV1_568_K4_DP_CORE28.json';
const positiveRel = 'results/raw/arc/2026-11-11_0057_LSPV1_567_PIVOT999999_CORE_ONLY_PACKET.json';
const negativeRel = 'results/raw/arc/2026-11-11_0057_LSPV1_567_NEGATIVE_PIVOT_CLI_ACCEPT_PACKET.json';
const activeRel = 'results/raw/arc/2026-11-11_0336_LSPV4_540_OWNER_FACET_CROSS_CONE_ACCEPTED.json';
const checkerSha = '338305c0ce101704205e57543756b8127074a986';
const seedSha = 'c68eeaf67015416dae49a34ad5ce25432b839bee';
const activeSha = '25b5c1f95734f6eae36bdbb4a17c948c00753cff';
const positiveSha = 'b2216a95f65d765028410ec3db9520dfcb104015';
const negativeSha = '717970007a1988cda31b70ac5abce8fd81519f4c';
function gitBlob(buf) {
  return crypto.createHash('sha1').update(Buffer.from('blob '+buf.length+'\0')).update(buf).digest('hex');
}
function pinned(rel, sha) {
  const bytes = fs.readFileSync(path.join(root, rel));
  assert.equal(gitBlob(bytes), sha, 'Git blob mismatch: '+rel);
  return bytes;
}
function deep(P) { return structuredClone(P); }
function makeSentinel(P) {
  const q = deep(P), old = q.spec.guard, target = 999999;
  assert.equal(q.gate_defs.length,0);
  assert(old !== target && Number.isSafeInteger(old));
  q.spec.guard = target;
  for (const r of q.records) {
    r.c = r.c.map(x => x===old?target:(x===-old?-target:x));
    if (r.kind==='RES' && r.pivot===old) r.pivot=target;
    else if (r.kind==='RES' && r.pivot===-old) r.pivot=-target;
  }
  assert.equal(q.records.at(-1).pivot,target, 'seed final pivot not guard');
  return q;
}
function addUnusedOwner(P) {
  const q=deep(P), E=q.spec.edges.length;
  assert.equal(q.gate_defs.length,0);
  let z=E+1;
  if (z===q.spec.guard) z=E+2;
  assert(Number.isSafeInteger(z) && z>E && z!==q.spec.guard);
  // A paid but unused AND2 definition, no DEF/RES records, no new parents.
  q.gate_defs.push([0,z,1,2]);
  q.summary.paid_gates++;
  q.summary.paid_total++;
  return q;
}
function repair(P) {
  const q=P.gate_defs.length===0?addUnusedOwner(P):deep(P);
  const last=q.records.at(-1);
  if (last.pivot===999999) {
    last.pivot=-999999;
    last.parents.reverse(); // strict oriented Resolution: swap +p and -p
  }
  return q;
}
function sourceRecords(P) {
  return P.records.filter(r=>r.kind==='SOURCE');
}
function refs(P) {
  return P.records.filter(r=>r.kind==='RES').reduce((n,r)=>n+r.parents.length,0);
}
function depth(P) {
  const d=[];
  for (let i=0;i<P.records.length;i++) {
    const r=P.records[i];
    d.push(r.kind==='RES'?1+Math.max(...r.parents.map(j=>d[j])):0);
  }
  return d.at(-1);
}
function nativeCoreFactory(checkerText) {
  const ctx={require, structuredClone, process:{argv:['node','checker']},console:{log(){}},__core:null};
  vm.runInNewContext(checkerText+'\nthis.__core=checkProof;',ctx,{filename:'pinned_original_386.js'});
  assert.equal(typeof ctx.__core,'function');
  return ctx.__core;
}
function coreAccept(core,P) {
  try { const v=core(deep(P),{control:true}); return {accepted:true,paid:v.paid,res:v.res,def:v.def}; }
  catch(e) { return {accepted:false,error:String(e.message||e)}; }
}
function runCli(checker,dir,name,P) {
  const raw=Buffer.from(JSON.stringify(P)+'\n','utf8');
  const file=path.join(dir,name+'.json');
  fs.writeFileSync(file,raw);
  const r=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',maxBuffer:4*1024*1024,timeout:120000});
  const accepted=r.status===0&&!r.error;
  let output=null;
  if(accepted) {
    const rows=r.stdout.trim().split('\n').filter(Boolean);
    output=JSON.parse(rows.at(-1));
    assert.equal(output.negativeTests,11);
    assert.equal(output.sha256,crypto.createHash('sha256').update(raw).digest('hex'));
  }
  return {accepted,bytes:raw.length,sha256:crypto.createHash('sha256').update(raw).digest('hex'),
    paid:output?.paid??null,assertions:output?.assertions??null,negativeTests:output?.negativeTests??null,
    rejectedMessage:accepted?null:(r.stderr||String(r.error)||'').slice(0,180)};
}
function main() {
  const checkerPath=path.join(root,checkerRel);
  const checkerBytes=pinned(checkerRel,checkerSha);
  const base=JSON.parse(pinned(seedRel,seedSha).toString('utf8'));
  const nativeCore=nativeCoreFactory(checkerBytes.toString('utf8'));
  const variants=[
    ['core28_no_gate_normal',deep(base)],
    ['core28_no_gate_sentinel',makeSentinel(base)],
    ['core29_one_gate_normal',repair(base)],
    ['core29_one_gate_sentinel',addUnusedOwner(makeSentinel(base))]
  ];
  const active=JSON.parse(pinned(activeRel,activeSha).toString('utf8'));
  variants.push(['active_shared_owner31',active]);
  variants.push(['nested_56_paid_positive_sentinel',JSON.parse(pinned(positiveRel,positiveSha).toString('utf8'))]);
  variants.push(['nested_56_paid_negative_sentinel',JSON.parse(pinned(negativeRel,negativeSha).toString('utf8'))]);
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv4_542_'));
  const cases=[], negatives=[];
  try {
    for(const [name,P] of variants) {
      const Q=repair(P),before=coreAccept(nativeCore,P),after=coreAccept(nativeCore,Q);
      assert(before.accepted && after.accepted, 'core rejected '+name);
      assert.equal(after.paid,before.paid+(P.gate_defs.length===0?1:0));
      assert.deepEqual(P.spec,Q.spec,'source spec changed');
      assert.deepEqual(sourceRecords(P),sourceRecords(Q),'source rows changed');
      assert.deepEqual(P.records.slice(0,-1),Q.records.slice(0,-1),'prefix changed');
      assert.deepEqual(P.records.at(-1).c,Q.records.at(-1).c,'sink changed');
      assert.deepEqual([...P.records.at(-1).parents].sort(),[...Q.records.at(-1).parents].sort(),'sink ancestry changed');
      assert.equal(refs(P),refs(Q));
      assert.equal(depth(P),depth(Q));
      assert.equal(P.records.length,Q.records.length);
      const old=runCli(checkerPath,dir,name+'_before',P);
      const fresh=runCli(checkerPath,dir,name+'_after',Q);
      assert.equal(old.accepted,P.gate_defs.length>0&&P.records.at(-1).pivot!==999999);
      assert(fresh.accepted,'repaired CLI rejected '+name+': '+fresh.rejectedMessage);
      assert.equal(fresh.paid,Q.summary.paid_total);
      cases.push({name,original:old,repaired:fresh,coreBefore:before,coreAfter:after,
        originalOwners:P.gate_defs.length,ownersAfter:Q.gate_defs.length,
        pivotBefore:P.records.at(-1).pivot,pivotAfter:Q.records.at(-1).pivot,
        records:P.records.length,resReferences:refs(P),sinkSpan:depth(P),sameSource:true});
    }
    const P=repair(makeSentinel(base));
    const bad={
      underpaid:()=>{const q=deep(P);q.summary.paid_total--;return q;},
      alteredSource:()=>{const q=deep(P);q.records[0].c=[0];return q;},
      invalidOwnerInput:()=>{const q=deep(P);q.gate_defs[0][2]=0;return q;},
      terminalPivotWithoutParentSwap:()=>{const q=deep(P);q.records.at(-1).pivot=999999;return q;},
      futureParent:()=>{const q=deep(P);q.records.at(-1).parents[0]=q.records.length;return q;},
      malformedGoal:()=>{const q=deep(P);q.records.at(-1).c=[1];return q;}
    };
    for(const [name,f] of Object.entries(bad)) {
      const q=f(),core=coreAccept(nativeCore,q),cli=runCli(checkerPath,dir,'hostile_'+name,q);
      assert(!core.accepted && !cli.accepted,'hostile accepted '+name);
      negatives.push({name,coreReject:true,originalCliReject:true,bytes:cli.bytes,sha256:cli.sha256});
    }
    const out={
      id:'LSPV-4/542',status:'COMPUTATIONAL + PROVED/RESTRICTED source-code theorem',
      timestamp:'2026-11-11 05:36 PST',checkerBlob:checkerSha,seedBlob:seedSha,activeBlob:activeSha,positiveBlob:positiveSha,negativeBlob:negativeSha,
      node:process.version,platform:process.platform,arch:process.arch,
      originalCodeUnmodified:true,exactOriginalOSSubprocesses:cases.length*2+negatives.length,
      observations:cases,hostiles:negatives,caseCount:cases.length,hostileCount:negatives.length,
      noFullMix341Checker:true,noPhysicalPeakSpaceMeasurement:true,
      proofObligations:['P2-D1 OPEN','P2-C3 OPEN','P2-B1 OPEN','P2-B2/B3 OPEN','P vs NP OPEN']
    };
    const destination=process.argv[2]||path.join(root,'results/raw/arc/2026-11-11_0536_LSPV4_542_CORE_CLI_CHARGE_TRANSFER_OS_RAW.json');
    fs.mkdirSync(path.dirname(destination),{recursive:true});
    fs.writeFileSync(destination,JSON.stringify(out,null,2)+'\n');
    console.log(JSON.stringify({cases:cases.length,hostiles:negatives.length,osSubprocesses:out.exactOriginalOSSubprocesses,
      acceptedRepairs:cases.every(c=>c.repaired.accepted),
      output:destination,summary:cases.map(c=>[c.name,c.original.accepted,c.repaired.accepted,c.coreBefore.paid,c.coreAfter.paid])},null,2));
  } finally {
    for(const f of fs.readdirSync(dir))fs.unlinkSync(path.join(dir,f));
    fs.rmdirSync(dir);
  }
}
main();
