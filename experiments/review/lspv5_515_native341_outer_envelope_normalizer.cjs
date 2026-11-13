'use strict';

// LSPV-5/515: original-OS-CLI replay and exact outer-envelope normalizer for
// the pinned recovered /341 checker. This is not a full R_mix341 checker.

const assert=require('assert/strict');
const crypto=require('crypto');
const fs=require('fs');
const os=require('os');
const path=require('path');
const {spawnSync}=require('child_process');

const checkerPath='experiments/arc/lspv2_341_independent_verify.js';
const packetPath='results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json';
const expectedCheckerBlob='fcb7d4ced8f922de14c0bda16263a8cc7853e8e0';
const expectedPacketBlob='fe27fe1011d0021e721ccaeb747ed58da65d7464';
const sha256=x=>crypto.createHash('sha256').update(x).digest('hex');
const gitBlob=x=>crypto.createHash('sha1').update('blob '+Buffer.byteLength(x)+'\0').update(x).digest('hex');
const compact=x=>JSON.stringify(x);
const clone=x=>JSON.parse(compact(x));
const checkerText=fs.readFileSync(checkerPath,'utf8');
const packetText=fs.readFileSync(packetPath,'utf8');
assert.equal(gitBlob(checkerText),expectedCheckerBlob,'pinned checker changed');
assert.equal(gitBlob(packetText),expectedPacketBlob,'pinned packet changed');
const baseline=JSON.parse(packetText);

const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv5-515-'));
let serial=0;
function runNative(packet){
  const raw=compact(packet),input=path.join(tmp,`case-${serial++}.json`);
  fs.writeFileSync(input,raw);
  const p=spawnSync(process.execPath,[checkerPath,input],{encoding:'utf8',timeout:30000});
  if(p.status!==0)return {accepted:false,status:p.status,signal:p.signal,
    error:(p.stderr||p.stdout).trim().slice(0,320),inputBytes:Buffer.byteLength(raw)};
  const output=JSON.parse(p.stdout);
  return {accepted:true,status:p.status,output,stdoutSha256:sha256(p.stdout),
    inputBytes:Buffer.byteLength(raw)};
}

function canonicalSummary(n){
  const asString='x'.repeat(n),asObject={length:n};
  return Buffer.byteLength(compact(asString))<=Buffer.byteLength(compact(asObject))
    ? asString : asObject;
}

// Partial on the exact checker-observed summary predicate. A rejected packet
// with a wrong/missing length is refused, never silently repaired.
function normalizeEnvelope(packet){
  if(!packet||!Array.isArray(packet.fixtures))throw Error('fixtures is not an array');
  if(packet.summary==null||packet.summary.length!==packet.fixtures.length)
    throw Error('summary length mismatch');
  return {
    fixtures:packet.fixtures.map(f=>({
      graph:{name:f.graph.name,n:f.graph.n,edges:f.graph.edges},
      charges:f.charges,
      clauses:f.clauses,
      proof:f.proof,
      deleted:f.deleted,
      properties:{essential:f.properties.essential},
      evenWitness:f.evenWitness
    })),
    summary:canonicalSummary(packet.fixtures.length)
  };
}

function enrichEnvelope(packet){
  const out=clone(packet);
  out.version={claimed:'R_mix341-full',weight:0};
  out.definition={SOURCE:'forged',Resolution:'forged',AND3:'forged',GF2:'forged',
    LOCAL_CONVERT:'forged',paid_DEF:0,contexts:'forged',source_hash:'00'.repeat(32)};
  out.claimed_total_work=-999;
  out.exported_wires=['ghost'];
  out.summary={length:out.fixtures.length,paid_total:-999,source_hash:'FORGED',
    accepted:true,contexts:['leaked'],parents:['fake'],weights:{AND3:0,XOR:0}};
  out.fixtures.forEach((f,i)=>{
    f.name=`forged-fixture-${i}`;
    f.source_hash='FORGED';
    f.context=['branch-local-leak'];
    f.private_wires=['ghost'];
    f.claimed_cost=-999;
    f.graph.source_hash='FORGED';
    f.graph.claimed_edges=999999;
    f.graph.kind='Resolution';
    f.properties={...f.properties,paid_total:-999,source_hash:'FORGED',
      parents:['fake'],accepted:true,contexts:['leaked'],weights:{AND3:0,XOR:0}};
  });
  return out;
}

function sameNative(a,b,label){
  assert(a.accepted&&b.accepted,`${label}: expected accepts`);
  assert.deepEqual(a.output,b.output,`${label}: output changed`);
  assert.equal(a.stdoutSha256,b.stdoutSha256,`${label}: stdout changed`);
}

const baseRun=runNative(baseline);
assert(baseRun.accepted,'baseline rejected');
const normalized=normalizeEnvelope(baseline),normalizedRun=runNative(normalized);
sameNative(baseRun,normalizedRun,'baseline normalization');
assert.deepEqual(normalizeEnvelope(normalized),normalized,'normalizer not idempotent');
assert(normalizedRun.inputBytes<=baseRun.inputBytes,'baseline bytes increased');

const enriched=enrichEnvelope(baseline),enrichedRun=runNative(enriched);
sameNative(baseRun,enrichedRun,'enriched envelope');
const enrichedNormalized=normalizeEnvelope(enriched),enrichedNormalizedRun=runNative(enrichedNormalized);
sameNative(baseRun,enrichedNormalizedRun,'enriched normalization');
assert.deepEqual(enrichedNormalized,normalized,'enriched image differs from normal form');

const summaryShapes=[
  ['reference_array',clone(baseline.summary)],
  ['ascii_string','x'.repeat(baseline.fixtures.length)],
  ['object_length',{length:baseline.fixtures.length,source_hash:'FORGED',paid_total:-999}],
  ['wrong_payload_array',Array(baseline.fixtures.length).fill({claimed_cost:0})]
].map(([name,summary])=>{
  const p=clone(baseline);p.summary=summary;
  const r=runNative(p),n=normalizeEnvelope(p),nr=runNative(n);
  sameNative(r,nr,`summary ${name}`);
  assert(nr.inputBytes<=r.inputBytes,`summary ${name}: bytes increased`);
  return {name,beforeBytes:r.inputBytes,afterBytes:nr.inputBytes,
    savedBytes:r.inputBytes-nr.inputBytes,stdoutSha256:r.stdoutSha256};
});

const perFixture=baseline.fixtures.map((fixture,i)=>{
  const p={fixtures:[clone(fixture)],summary:{length:1,untrusted:'FORGED'}};
  p.fixtures[0].properties.extra='FORGED';
  p.fixtures[0].graph.extra='FORGED';
  const r=runNative(p),n=normalizeEnvelope(p),nr=runNative(n);
  sameNative(r,nr,`fixture ${i}`);
  assert(nr.inputBytes<=r.inputBytes);
  return {index:i,graph:fixture.graph.name,paid:fixture.proof.length,
    beforeBytes:r.inputBytes,afterBytes:nr.inputBytes,savedBytes:r.inputBytes-nr.inputBytes,
    checks:r.output.checks,stdoutSha256:r.stdoutSha256};
});

function hostile(name,fn){
  const p=clone(baseline);fn(p);
  const r=runNative(p);
  let nr=null,refused=null;
  try{nr=runNative(normalizeEnvelope(p));}catch(e){refused=String(e)}
  assert(!r.accepted,`${name}: hostile packet accepted`);
  assert(refused!==null||!nr.accepted,`${name}: hostile normalized packet accepted`);
  return {name,originalAccepted:r.accepted,normalizedAccepted:nr?nr.accepted:null,
    normalizerRefused:refused!==null,originalError:r.error||null,
    normalizedError:refused||(nr&&nr.error)||null};
}
const hostileCases=[
  hostile('wrong_summary_length',p=>p.summary={length:p.fixtures.length-1}),
  hostile('missing_summary',p=>delete p.summary),
  hostile('forged_signed_source',p=>p.fixtures[0].clauses[0].literals[0]=999),
  hostile('forged_parent',p=>p.fixtures[0].proof[0].parents[0]='FAKE'),
  hostile('bad_terminal',p=>p.fixtures[0].proof.at(-1).row.rhs^=1),
  hostile('forged_essential',p=>p.fixtures[0].properties.essential=-1),
  hostile('bad_deletion_witness',p=>{
    const d=p.fixtures[0].deleted[0];
    d.assignment=d.assignment.replace(/^./,b=>b==='0'?'1':'0');
  })
];

const result={
  run:'LSPV-5/515',timestamp:'2026-11-12T18:48:00-08:00',node:process.version,
  provenance:{checkerPath,checkerGitBlob:gitBlob(checkerText),checkerSha256:sha256(checkerText),
    packetPath,packetGitBlob:gitBlob(packetText),packetSha256:sha256(packetText),
    execution:'unchanged authoritative checker as OS Node subprocess for every case'},
  target:'Erase checker-unread top-level, fixture, graph, properties, and summary payload fields while preserving every checker-observed field and choosing a shortest declared summary shape.',
  theoremScope:'Ordinary finite JSON packets accepted by the pinned recovered /341 SOURCE/AND3/XOR checker; not the complete historical R_mix341 accepted-byte calculus.',
  observedReadSurface:{top:['fixtures','summary.length'],fixture:['graph','charges','clauses','proof','deleted','properties.essential','evenWitness'],graph:['name','n','edges']},
  baseline:{accepted:baseRun.accepted,beforeBytes:baseRun.inputBytes,afterBytes:normalizedRun.inputBytes,
    savedBytes:baseRun.inputBytes-normalizedRun.inputBytes,checks:baseRun.output.checks,
    stdoutSha256:baseRun.stdoutSha256},
  enriched:{accepted:enrichedRun.accepted,beforeBytes:enrichedRun.inputBytes,
    afterBytes:enrichedNormalizedRun.inputBytes,savedBytes:enrichedRun.inputBytes-enrichedNormalizedRun.inputBytes,
    checks:enrichedRun.output.checks,stdoutSha256:enrichedRun.stdoutSha256,
    exactSameNormalForm:compact(enrichedNormalized)===compact(normalized)},
  normalForm:{bytes:normalizedRun.inputBytes,idempotent:compact(normalizeEnvelope(normalized))===compact(normalized),
    sameStdout:baseRun.stdoutSha256===normalizedRun.stdoutSha256,
    summary:normalized.summary},
  summaryShapes,perFixture,hostile:hostileCases,
  totals:{positiveNativeCliRuns:4+2*summaryShapes.length+2*perFixture.length,
    hostileOriginalRejected:hostileCases.length,
    hostileNormalizedRejectedOrRefused:hostileCases.length},
  conclusion:'PROVED/RESTRICTED outer-envelope normalization lemma plus COMPUTATIONAL original OS-CLI validation; summary payload subcase credits LSPV-3/596; P2-D1/C3/B1 OPEN; P2-B2/B3 separate; P versus NP OPEN.'
};
fs.rmSync(tmp,{recursive:true,force:true});
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+'\n');
if(process.argv[3])fs.writeFileSync(process.argv[3],compact(enriched)+'\n');
if(process.argv[4])fs.writeFileSync(process.argv[4],compact(enrichedNormalized)+'\n');
process.stdout.write(JSON.stringify(result,null,2)+'\n');
