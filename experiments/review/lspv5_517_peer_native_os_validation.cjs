#!/usr/bin/env node
'use strict';
/* LSPV-5/517. Fresh-process audit of the exact current LSPV-1/608,
 * LSPV-2/588, LSPV-3/604, and LSPV-4/576 peer runners. This authenticates
 * only the pinned historical /341 and /386 fixture checkers exercised by
 * those runners. It is not the unrecovered complete R_mix341 dispatcher.
 *
 * Run from repository root:
 *   node experiments/review/lspv5_517_peer_native_os_validation.cjs [raw.json]
 */
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const crypto=require('node:crypto'),cp=require('node:child_process'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const rel={
  r608:'experiments/arc/lspv1_608_native341_both_escapes.cjs',
  r588:'experiments/arc/lspv2_588_native386_live_guard_ports.cjs',
  r604:'experiments/arc/lspv3_604_restored_signed_source_replay.cjs',
  r576:'experiments/arc/lspv4_576_dual_native_reference_accounting.cjs',
  c341:'experiments/arc/lspv2_341_independent_verify.js',
  c386:'experiments/arc/lspv2_386_independent_verify.js',
  source:'results/raw/arc/574_k01_SIGNED_SOURCE.cnf',
  alias:'results/raw/arc/2026-11-12_1412_LSPV2_583_SIGNED_K4_SOURCE.cnf',
  seed386:'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json',
  seed341:'results/raw/arc/2026-11-12_1725_LSPV3_600_NATIVE341_K4_EDGE_SUFFIX_ACCEPTED.json',
  fixture341:'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json'
};
const expected={
  r608:'b7577e04678f55b9fc423b887bfdd58909773c02aafcf1d18c954a4c1c55a171',
  r588:'c4c92e32626593e5c2f1fb220c4a90217ca9eaa05eee2bed5c19566ca4a06a91',
  r604:'93d9ed798306c7d5287f524a02d7f5456ba1812dce804924afc1bdc5cb1df07d',
  r576:'7f98b21beab05af214d71beaa429a425be022c88134e57654be9ead4bbec95dd',
  c341:'0a8167fc65f324860f60abd2a0e0176d0def968cb6ee7055b6aa1bfd43c255ae',
  c386:'22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113',
  source:'3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c',
  alias:'3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c',
  seed386:'0d8b1894f91d00c554727a92fed35b2bb58f2b1602f2a3cfcb949effda43ceb0',
  seed341:'7d286409081e3b5551e4c81a40cc2d05378fc732a6188ab6b36222c5f13d5cb4',
  fixture341:'12d723c92c683ec1a59e17d95d0d47156babe7febe27b7432dc01279abcb8d95'
};
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const bytes={};
for(const [key,file] of Object.entries(rel)){
  bytes[key]=fs.readFileSync(path.join(root,file));
  assert.equal(sha(bytes[key]),expected[key],key+' SHA-256 drift');
}
assert.deepEqual(bytes.source,bytes.alias,'restored signed-source alias differs bytewise');
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv5-517-'));
function run(label,args){
  const t0=process.hrtime.bigint();
  const p=cp.spawnSync(process.execPath,args,{cwd:root,encoding:'utf8',timeout:30000,maxBuffer:8*1024*1024});
  assert.ifError(p.error);assert.equal(p.status,0,label+': '+p.stderr.slice(0,800));
  const parsed=JSON.parse(p.stdout);
  return {parsed,elapsedMs:Number(process.hrtime.bigint()-t0)/1e6,stderr:p.stderr};
}
try{
  const a608=run('LSPV-1/608',[path.join(root,rel.r608),path.join(tmp,'608.json')]);
  assert.equal(a608.parsed.accepted,4);assert.equal(a608.parsed.rejected,8);
  assert.equal(a608.parsed.assertion_groups,5604);
  const both=a608.parsed.cases.find(x=>x.name==='escape_both_corrected');
  assert.ok(both.accepted&&both.evenEscaped&&both.deletedEscaped&&both.escapes===2);

  const dir588=path.join(tmp,'588');fs.mkdirSync(dir588);
  const a588=run('LSPV-2/588',[path.join(root,rel.r588),path.join(root,rel.c386),
    path.join(root,rel.seed386),path.join(root,rel.source),dir588,path.join(root,rel.fixture341)]);
  assert.equal(a588.parsed.status,'PASS');assert.deepEqual(a588.parsed.count,{testCount:13,accepts:4,rejects:9,originalAcceptedAssertions:17094});
  assert.deepEqual(a588.parsed.variants.map(x=>x.work),[44,44,48]);
  assert.deepEqual(a588.parsed.variants.map(x=>x.ports),[16,16,16]);

  const a604=run('LSPV-3/604',[path.join(root,rel.r604),path.join(tmp,'604.json')]);
  assert.equal(a604.parsed.externalSourceBytes,215);assert.equal(a604.parsed.sourceModels,0);
  assert.equal(a604.parsed.originalVerifierPositive.paid,29);
  assert.equal(a604.parsed.originalVerifierPositive.assertions,3542);
  assert.equal(a604.parsed.hostileBadPivotRejected,true);

  const a576=run('LSPV-4/576',[path.join(root,rel.r576),'--native']);
  assert.equal(a576.parsed.original341.totalsAcrossIndependentFixtures.paid,321);
  assert.equal(a576.parsed.original341.totalsAcrossIndependentFixtures.referenceBytes,1840);
  assert.equal(a576.parsed.original386.sharedDag.nativeLogicalW,38);
  assert.equal(a576.parsed.original386.sharedDag.unfoldedNaiveWork,39);
  assert.deepEqual(a576.parsed.native.map(x=>x.exit),[0,0]);
  const native341Checks=Number((a576.parsed.native.find(x=>x.tag==='341').stdout.match(/"checks":\s*(\d+)/)||[])[1]);
  assert.equal(native341Checks,30714);
  const native386=JSON.parse(a576.parsed.native.find(x=>x.tag==='386').stdout);
  assert.equal(native386.paid,38);assert.equal(native386.assertions,3915);

  const ledger={
    schema:'LSPV5-517-PEER-NATIVE-OS-VALIDATION/v1',
    timestamp_pst:'2026-11-12T20:48:00-08:00',
    status:'COMPUTATIONAL fresh-process validation; full R_mix341 remains OPEN',
    scope:'Exact pinned peer runners and separate historical /341 and /386 fixture checkers only',
    pins:{sha256:expected,sourceAliasByteIdentical:true,sourceBytes:bytes.source.length},
    validations:{
      lspv1_608:{accepted:4,rejected:8,assertionGroups:5604,dualEscapeAccepted:true,elapsedMs:a608.elapsedMs},
      lspv2_588:{tests:13,accepted:4,rejected:9,assertionGroups:17094,works:[44,44,48],allSixteenPortsLive:true,elapsedMs:a588.elapsedMs},
      lspv3_604:{sourceBytes:215,assignmentsChecked:128,sourceModels:0,paid:29,assertionGroups:3542,badPivotRejected:true,elapsedMs:a604.elapsedMs},
      lspv4_576:{nativeExits:[0,0],work341:321,referenceBytes341:1840,work386:38,unfoldedNaiveWork386:39,assertionGroups341:30714,assertionGroups386:3915,elapsedMs:a576.elapsedMs}
    },
    aggregate:{freshPeerRunnerProcesses:4,explicitPositiveCases:11,explicitHostileCases:18,observedAssertionGroups:60869},
    cegar:'Both lexical escapes are genuine accepted paths and remain; only concretely rejected corruptions justify exclusions.',
    open:['P2-D1','P2-C3','P2-B1','P2-B2','P2-B3'],
    nonClaims:['No complete historical mixed dispatcher was recovered.','No cross-calculus transfer was authenticated.','No lower bound or P versus NP result follows.']
  };
  const output=JSON.stringify(ledger,null,2)+'\n';
  if(process.argv[2]){fs.mkdirSync(path.dirname(process.argv[2]),{recursive:true});fs.writeFileSync(process.argv[2],output);}
  process.stdout.write(output);
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
