'use strict';

// LSPV-5/514: independent original-OS-CLI replay and exact arity-two
// canonicalizer for graph edge tuples in the pinned recovered /341 checker.
// This authenticates one checker-observable quotient, not full R_mix341.

const assert=require('assert/strict');
const crypto=require('crypto');
const fs=require('fs');
const os=require('os');
const path=require('path');
const {spawnSync}=require('child_process');

const checkerPath='experiments/arc/lspv2_341_independent_verify.js';
const packetPath='results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json';
const peerWitnessPath='results/raw/arc/2026-11-12_1725_LSPV3_600_NATIVE341_K4_EDGE_SUFFIX_ACCEPTED.json';
const expectedCheckerBlob='fcb7d4ced8f922de14c0bda16263a8cc7853e8e0';
const expectedPacketBlob='fe27fe1011d0021e721ccaeb747ed58da65d7464';
const expectedPeerWitnessBlob='393d13265192b4e43073c6f6559bc22b6a71ece5';
const sha256=x=>crypto.createHash('sha256').update(x).digest('hex');
const gitBlob=x=>crypto.createHash('sha1').update('blob '+Buffer.byteLength(x)+'\0').update(x).digest('hex');
const compact=x=>JSON.stringify(x);
const clone=x=>JSON.parse(compact(x));
const checkerText=fs.readFileSync(checkerPath,'utf8');
const packetText=fs.readFileSync(packetPath,'utf8');
const peerWitnessText=fs.readFileSync(peerWitnessPath,'utf8');
assert.equal(gitBlob(checkerText),expectedCheckerBlob,'pinned checker changed');
assert.equal(gitBlob(packetText),expectedPacketBlob,'pinned packet changed');
assert.equal(gitBlob(peerWitnessText),expectedPeerWitnessBlob,'peer witness changed');
const baseline=JSON.parse(packetText),peerWitness=JSON.parse(peerWitnessText);

const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv5-514-'));
let serial=0;
function runNative(packet){
  const raw=compact(packet),input=path.join(tmp,`case-${serial++}.json`);
  fs.writeFileSync(input,raw);
  const p=spawnSync(process.execPath,[checkerPath,input],{encoding:'utf8',timeout:30000});
  if(p.status!==0)return {accepted:false,status:p.status,signal:p.signal,
    error:(p.stderr||p.stdout).trim().slice(0,280),inputBytes:Buffer.byteLength(raw)};
  const parsed=JSON.parse(p.stdout);
  return {accepted:true,status:p.status,output:parsed,stdoutSha256:sha256(p.stdout),
    inputBytes:Buffer.byteLength(raw)};
}

function suffixAll(packet){
  const out=clone(packet);
  for(const fixture of out.fixtures)for(let i=0;i<fixture.graph.edges.length;i++){
    fixture.graph.edges[i].push(
      null,
      {source_hash:'FORGED_UNTRUSTED_SUFFIX',edge_index:i,
       claimed_endpoints:[999,-999],claimed_parent:'FAKE',kind:'SOURCE',
       nested:[false,1,'x',{private_wire:'FORGED'}]},
      [fixture.graph.edges[i][1],fixture.graph.edges[i][0]],
      'IGNORED'
    );
  }
  return JSON.parse(compact(out));
}

function normalizeEdges(packet){
  const out=clone(packet);
  for(const fixture of out.fixtures){
    if(!Array.isArray(fixture.graph.edges))throw Error('non-array edge bank');
    fixture.graph.edges=fixture.graph.edges.map(edge=>{
      if(!Array.isArray(edge)||edge.length<2)throw Error('noncanonical edge tuple');
      return [edge[0],edge[1]];
    });
  }
  return out;
}

function sameNative(a,b,label){
  assert(a.accepted&&b.accepted,`${label}: expected accepts`);
  assert.deepEqual(a.output,b.output,`${label}: output changed`);
  assert.equal(a.stdoutSha256,b.stdoutSha256,`${label}: stdout changed`);
}

const baseRun=runNative(baseline);
assert(baseRun.accepted,'baseline rejected');
const suffixed=suffixAll(baseline),suffixRun=runNative(suffixed);
sameNative(baseRun,suffixRun,'all-edge suffix');
const canonical=normalizeEdges(suffixed),canonicalRun=runNative(canonical);
sameNative(baseRun,canonicalRun,'canonical image');
assert.deepEqual(canonical,baseline,'canonical image differs from baseline packet');
assert.deepEqual(normalizeEdges(canonical),canonical,'normalizer not idempotent');
const suffixBytes=Buffer.byteLength(compact(suffixed)),canonicalBytes=Buffer.byteLength(compact(canonical));
assert(canonicalBytes<suffixBytes,'canonical bytes did not shrink');

const perFixture=baseline.fixtures.map((fixture,i)=>{
  const one=clone(baseline);one.fixtures=[clone(fixture)];
  one.summary=[clone(baseline.summary[i])];
  const s=suffixAll(one),c=normalizeEdges(s),sr=runNative(s),cr=runNative(c);
  sameNative(sr,cr,`fixture ${i}`);
  const sb=Buffer.byteLength(compact(s)),cb=Buffer.byteLength(compact(c));
  assert(cb<sb);
  return {index:i,graph:fixture.graph.name,edges:fixture.graph.edges.length,
    paid:fixture.proof.length,suffixBytes:sb,canonicalBytes:cb,savedBytes:sb-cb,
    checks:sr.output.checks,stdoutSha256:sr.stdoutSha256};
});

const peerRun=runNative(peerWitness),peerCanonical=normalizeEdges(peerWitness);
const peerCanonicalRun=runNative(peerCanonical);
sameNative(peerRun,peerCanonicalRun,'peer /600 exact witness');
assert(peerCanonical.fixtures[0].graph.edges.every(e=>e.length===2));

function hostile(name,fn){
  const p=suffixAll(baseline);fn(p);
  const r=runNative(p);
  let nr=null,ne=null;
  try{nr=runNative(normalizeEdges(p));}catch(e){ne=String(e)}
  assert(!r.accepted,`${name}: hostile suffixed packet accepted`);
  assert(ne!==null||!nr.accepted,`${name}: hostile canonical image accepted`);
  return {name,suffixedAccepted:r.accepted,canonicalAccepted:nr?nr.accepted:null,
    normalizerRefused:ne!==null,suffixedError:r.error||null,
    canonicalError:ne||(nr&&nr.error)||null};
}
const hostileCases=[
  hostile('same_effective_endpoints',p=>p.fixtures[0].graph.edges[0][1]=p.fixtures[0].graph.edges[0][0]),
  hostile('noninteger_effective_endpoint',p=>p.fixtures[0].graph.edges[0][0]=0.5),
  hostile('missing_effective_endpoint',p=>p.fixtures[0].graph.edges[0]=[p.fixtures[0].graph.edges[0][0]]),
  hostile('duplicate_effective_edge',p=>{const e=p.fixtures[0].graph.edges[1];p.fixtures[0].graph.edges[0]=[e[0],e[1],{suffix:'x'}]}),
  hostile('forged_signed_source',p=>p.fixtures[0].clauses[0].literals[0]=999),
  hostile('forged_parent',p=>p.fixtures[0].proof[0].parents[0]='FAKE'),
  hostile('bad_terminal',p=>p.fixtures[0].proof.at(-1).row.rhs^=1)
];

const result={
  run:'LSPV-5/514',timestamp:'2026-11-12T17:48:00-08:00',node:process.version,
  provenance:{checkerPath,checkerGitBlob:gitBlob(checkerText),checkerSha256:sha256(checkerText),
    packetPath,packetGitBlob:gitBlob(packetText),packetSha256:sha256(packetText),
    peerWitnessPath,peerWitnessGitBlob:gitBlob(peerWitnessText),peerWitnessSha256:sha256(peerWitnessText),
    execution:'unchanged authoritative checker as OS Node subprocess for every case'},
  target:'Every accepted parsed edge tuple in the pinned /341 checker has an exact arity-two canonical image preserving checker output, source semantics, proof DAG, goal, and logical work.',
  theoremScope:'Pinned recovered /341 SOURCE/AND3/XOR checker only; not the complete historical R_mix341 accepted-byte calculus.',
  baseline:{accepted:baseRun.accepted,bytes:baseRun.inputBytes,checks:baseRun.output.checks,
    stdoutSha256:baseRun.stdoutSha256},
  allEdgesSuffixed:{accepted:suffixRun.accepted,bytes:suffixBytes,checks:suffixRun.output.checks,
    stdoutSha256:suffixRun.stdoutSha256},
  canonicalArityTwo:{accepted:canonicalRun.accepted,bytes:canonicalBytes,checks:canonicalRun.output.checks,
    stdoutSha256:canonicalRun.stdoutSha256,savedBytes:suffixBytes-canonicalBytes,
    exactBaselinePacket:compact(canonical)===compact(baseline),
    idempotent:compact(normalizeEdges(canonical))===compact(canonical)},
  peer600ExactWitness:{accepted:peerRun.accepted,bytes:peerRun.inputBytes,
    canonicalBytes:peerCanonicalRun.inputBytes,savedBytes:peerRun.inputBytes-peerCanonicalRun.inputBytes,
    sameStdout:peerRun.stdoutSha256===peerCanonicalRun.stdoutSha256},
  perFixture,hostile:hostileCases,
  totals:{positiveNativeCliRuns:3+2*perFixture.length+2,
    hostileSuffixedRejected:hostileCases.length,
    hostileCanonicalRejectedOrRefused:hostileCases.length,
    perFixtureSavedBytes:perFixture.reduce((s,x)=>s+x.savedBytes,0)},
  conclusion:'PROVED/RESTRICTED edge-tuple normalization lemma plus COMPUTATIONAL original OS-CLI validation; suffix provenance is unauthenticated; P2-D1/C3/B1 OPEN; P2-B2/B3 separate; P versus NP OPEN.'
};
fs.rmSync(tmp,{recursive:true,force:true});
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+'\n');
process.stdout.write(JSON.stringify(result,null,2)+'\n');
