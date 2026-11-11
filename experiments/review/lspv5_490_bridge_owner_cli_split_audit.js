'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');
const { spawnSync } = require('child_process');

const ROOT = path.resolve(__dirname, '../..');
const CHECKER = path.join(ROOT, 'experiments/arc/lspv2_386_independent_verify.js');
const PACKET = path.join(ROOT, 'results/raw/arc/2026-11-11_0756_LSPV1_574_BRIDGE_PACKET.json');
const RAW_OUT = path.join(ROOT, 'results/raw/arc/2026-11-11_0852_LSPV5_490_BRIDGE_OWNER_CLI_SPLIT_RAW.json');
const EXPECTED = {
  checkerBlob: '338305c0ce101704205e57543756b8127074a986',
  packetBlob: '1efb525f0c84dfffb626c00e592f4952cc796c69'
};

function gitBlob(buf) {
  return crypto.createHash('sha1').update(Buffer.from(`blob ${buf.length}\0`)).update(buf).digest('hex');
}
function sha256(buf) { return crypto.createHash('sha256').update(buf).digest('hex'); }
function clone(x) { return structuredClone(x); }
function key(c) { return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b); }
function equal(a,b) { return JSON.stringify(a) === JSON.stringify(b); }

const checkerBuf = fs.readFileSync(CHECKER);
const packetBuf = fs.readFileSync(PACKET);
const pins = {
  checkerBlob: gitBlob(checkerBuf), packetBlob: gitBlob(packetBuf),
  checkerSha256: sha256(checkerBuf), packetSha256: sha256(packetBuf)
};
for (const [k,v] of Object.entries(EXPECTED)) if (pins[k] !== v) throw new Error(`pin mismatch ${k}`);
const seed = JSON.parse(packetBuf);

function runRawCLI(raw, tempDir, label) {
  const file = path.join(tempDir, `${label}.json`);
  fs.writeFileSync(file, raw);
  const t0 = process.hrtime.bigint();
  const p = spawnSync(process.execPath, [CHECKER, file], {encoding:'utf8', maxBuffer:16*1024*1024});
  const elapsedMs = Number(process.hrtime.bigint()-t0)/1e6;
  let outcome = null;
  if (p.status === 0) outcome = JSON.parse(p.stdout.trim().split(/\r?\n/).at(-1));
  const m = /Error: ([^\n]+)/.exec(p.stderr || '');
  return {label,accepted:p.status===0,status:p.status,signal:p.signal,bytes:raw.length,sha256:sha256(raw),elapsedMs,outcome,error:m?m[1]:null};
}
function runCLI(obj, tempDir, label) {
  return runRawCLI(Buffer.from(JSON.stringify(obj) + '\n'), tempDir, label);
}

// Load the exact original core function text, stopping before the CLI corruption harness.
const source = checkerBuf.toString('utf8');
const cut = source.indexOf('function corrupt');
if (cut < 0) throw new Error('original core boundary missing');
const coreFactory = new Function('require', source.slice(0,cut) + '\nreturn {checkProof, tests:()=>tests};');
const originalCore = coreFactory(require);
function runOriginalCore(obj) {
  try { const outcome = originalCore.checkProof(clone(obj)); return {accepted:true,outcome,assertions:originalCore.tests()}; }
  catch (e) { return {accepted:false,error:e.message,assertions:originalCore.tests()}; }
}

function terminalAncestry(records) {
  const seen = new Set(), stack=[records.length-1];
  while (stack.length) {
    const i=stack.pop(); if (seen.has(i)) continue; seen.add(i);
    for (const p of records[i].parents || []) stack.push(p);
  }
  return seen;
}
function replayResolution(records) {
  const known=[]; let res=0;
  for (let i=0;i<records.length;i++) {
    const r=records[i];
    if (r.kind === 'RES') {
      if (!Array.isArray(r.parents) || r.parents.length !== 2) throw new Error(`arity ${i}`);
      const A=known[r.parents[0]], B=known[r.parents[1]], p=r.pivot;
      if (!A.includes(p) || !B.includes(-p)) throw new Error(`pivot ${i}`);
      const got=key([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)]);
      if (!equal(got,r.c)) throw new Error(`resolvent ${i}`);
      res++;
    }
    known.push(r.c);
  }
  return {resolution:res,terminal:known.at(-1)};
}
function satisfiesClause(clause, mask) {
  return clause.some(lit => {
    const bit=(mask >> (Math.abs(lit)-1)) & 1;
    return lit > 0 ? bit===1 : bit===0;
  });
}
function findModel(clauses, n=16) {
  for (let mask=0; mask<2**n; mask++) if (clauses.every(c=>satisfiesClause(c,mask))) return mask;
  return null;
}
function bits(mask,n=16) { return mask===null?null:mask.toString(2).padStart(n,'0').split('').reverse().join(''); }

const records=seed.records;
const ancestry=terminalAncestry(records);
const sourceIndices=records.map((r,i)=>r.kind==='SOURCE'?i:null).filter(i=>i!==null);
const ancestrySources=sourceIndices.filter(i=>ancestry.has(i));
const deadSources=sourceIndices.filter(i=>!ancestry.has(i));
const allSourceClauses=sourceIndices.map(i=>records[i].c);
const coreClauses=ancestrySources.map(i=>records[i].c);
const nonGuardCore=ancestrySources.filter(i=>records[i].source!==-1);
const deletionWitnesses=nonGuardCore.map(drop=>{
  const clauses=ancestrySources.filter(i=>i!==drop).map(i=>records[i].c);
  const model=findModel(clauses);
  if (model===null) throw new Error(`core deletion ${drop} remained UNSAT`);
  return {record:drop,source:records[drop].source,witnessLSBFirst:bits(model)};
});
const replay=replayResolution(records);
if (!equal(replay.terminal,[])) throw new Error('not a refutation');
if (findModel(allSourceClauses)!==null || findModel(coreClauses)!==null) throw new Error('source/core unexpectedly SAT');
if (!equal(deadSources,[1,2,21,22])) throw new Error(`dead source mismatch ${deadSources}`);
if (seed.records.some(r=>r.kind==='DEF')) throw new Error('unexpected live DEF facet');
const ownerOutput=seed.gate_defs[0][1];
const ownerLiteralOccurrences=seed.records.reduce((n,r)=>n+r.c.filter(x=>Math.abs(x)===ownerOutput).length,0);
if (ownerLiteralOccurrences!==0) throw new Error('declared owner is not syntactically dead');

const noOwner=clone(seed);
noOwner.gate_defs=[];
noOwner.summary.paid_gates=0;
noOwner.summary.paid_total=noOwner.summary.resolution;
const staleOwnerRemoval=clone(seed); staleOwnerRemoval.gate_defs=[];
const staleSummary=clone(seed); staleSummary.summary.paid_gates=0; staleSummary.summary.paid_total=staleSummary.summary.resolution;

const tempDir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv5-490-'));
try {
  const cli = [];
  cli.push(runRawCLI(packetBuf,tempDir,'baseline_exact_published_bytes_W103'));
  cli.push(runCLI(noOwner,tempDir,'coordinated_owner_removal_W102'));
  cli.push(runCLI(staleOwnerRemoval,tempDir,'owner_removed_stale_summary'));
  cli.push(runCLI(staleSummary,tempDir,'owner_present_zero_summary'));
  const badSource=clone(seed); badSource.records[1].c=[12345]; cli.push(runCLI(badSource,tempDir,'bad_source'));
  const badPivot=clone(seed); badPivot.records.at(-1).pivot=999999; cli.push(runCLI(badPivot,tempDir,'bad_terminal_pivot'));
  const dangling=clone(seed); dangling.records.at(-1).parents[0]=seed.records.length+1; cli.push(runCLI(dangling,tempDir,'dangling_parent'));
  const and3=clone(seed); and3.records.at(-1).kind='AND3'; cli.push(runCLI(and3,tempDir,'unrecognized_AND3'));

  if (!cli[0].accepted) throw new Error('baseline CLI rejected');
  if (cli.slice(1).some(x=>x.accepted)) throw new Error('a hostile CLI packet accepted');
  const coreBaseline=runOriginalCore(seed);
  const coreNoOwner=runOriginalCore(noOwner);
  if (!coreBaseline.accepted || !coreNoOwner.accepted || coreNoOwner.outcome.paid!==102) throw new Error('core split not reproduced');
  if (cli[1].error!=='accepted a corrupted proof') throw new Error(`unexpected full CLI reason: ${cli[1].error}`);

  const report={
    schema:'LSPV5_490_BRIDGE_OWNER_CLI_SPLIT/v1',
    timestampPacific:'2026-11-11 08:52 PST',
    status:'PROVED/RESTRICTED source/ancestry and checker-harness split + COMPUTATIONAL exact OS replay',
    pins,
    independent:{
      sourceRecords:sourceIndices.length,
      ancestrySourceRecords:ancestrySources.length,
      terminalDeadSourceRecords:deadSources,
      originalSourceModels:0,
      reducedCoreModels:0,
      deletionWitnesses,
      resolutionRecords:replay.resolution,
      proofRecords:records.length,
      ownerOutput,
      ownerLiteralOccurrences,
      defFacetRecords:0
    },
    exactOSCLI:cli,
    originalCoreWithoutCLIHarness:{baseline:coreBaseline,coordinatedOwnerRemoval:coreNoOwner},
    conclusion:'The /574 source-versus-terminal-ancestry theorem reproduces. The one-unit dead owner cannot be removed from the full CLI language: although the exact original checkProof core accepts the coordinated W=102 packet, the original CLI corruption harness rejects it because shifting an empty gate_defs array is a no-op and is therefore reported as an accepted corruption. Thus the full CLI enforces a nonempty paid-owner floor extralogically.',
    limitation:'Archived /386 sibling only; no complete historical R_mix341 dispatcher, no minimum-W proof, no all-rule lower bound, no P2-B2/B3 transfer.'
  };
  fs.writeFileSync(RAW_OUT,JSON.stringify(report,null,2)+'\n');
  process.stdout.write(JSON.stringify(report,null,2)+'\n');
} finally { fs.rmSync(tempDir,{recursive:true,force:true}); }
