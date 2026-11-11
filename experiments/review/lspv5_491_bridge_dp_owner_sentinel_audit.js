'use strict';

const scriptStart = process.hrtime.bigint();
const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');
const { spawnSync } = require('child_process');

const ROOT = path.resolve(__dirname, '../..');
const CHECKER = path.join(ROOT, 'experiments/arc/lspv2_386_independent_verify.js');
const PACKET = path.join(ROOT, 'results/raw/arc/2026-11-11_0900_LSPV1_575_BRIDGE_GUARDED_DP_NATIVE_ACCEPTED.json');
const RAW_OUT = path.join(ROOT, 'results/raw/arc/2026-11-11_0948_LSPV5_491_BRIDGE_DP_OWNER_SENTINEL_RAW.json');
const HOSTILE_OUT = path.join(ROOT, 'results/raw/arc/2026-11-11_0948_LSPV5_491_MAX_SAFE_OWNER_ACCEPTED.json');
const EXPECTED = {
  checkerBlob: '338305c0ce101704205e57543756b8127074a986',
  packetBlob: 'd5de0f477cd736ec5fd7b01be18350f9cb594fd2'
};
const BASE_ORDER = [7,5,3,6,4,1,2,8,11,10,13,9,14,12,15];

function gitBlob(buf) {
  return crypto.createHash('sha1').update(Buffer.from('blob '+buf.length+'\0')).update(buf).digest('hex');
}
function sha256(buf) { return crypto.createHash('sha256').update(buf).digest('hex'); }
function clone(x) { return structuredClone(x); }
function key(c) { return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b); }
function clauseKey(c) { return JSON.stringify(c); }
function equal(a,b) { return JSON.stringify(a) === JSON.stringify(b); }

const checkerBuf = fs.readFileSync(CHECKER);
const packetBuf = fs.readFileSync(PACKET);
const pins = {
  checkerBlob: gitBlob(checkerBuf),
  packetBlob: gitBlob(packetBuf),
  checkerSha256: sha256(checkerBuf),
  packetSha256: sha256(packetBuf)
};
for (const [k,v] of Object.entries(EXPECTED)) if (pins[k] !== v) throw new Error('pin mismatch '+k);
const seed = JSON.parse(packetBuf);

const checkerSource = checkerBuf.toString('utf8');
const coreCut = checkerSource.indexOf('function corrupt');
if (coreCut < 0) throw new Error('original core boundary missing');
const coreFactory = new Function('require', checkerSource.slice(0,coreCut) + '\nreturn {checkProof, tests:()=>tests};');
const originalCore = coreFactory(require);
function runCore(obj) {
  try {
    const outcome = originalCore.checkProof(clone(obj));
    return {accepted:true,outcome,assertions:originalCore.tests()};
  } catch (e) {
    return {accepted:false,error:e.message,assertions:originalCore.tests()};
  }
}

function runCLI(obj, tempDir, label, raw=null) {
  const bytes = raw || Buffer.from(JSON.stringify(obj) + '\n');
  const file = path.join(tempDir, label+'.json');
  fs.writeFileSync(file, bytes);
  const t0 = process.hrtime.bigint();
  const p = spawnSync(process.execPath, [CHECKER, file], {encoding:'utf8', maxBuffer:32*1024*1024});
  const elapsedMs = Number(process.hrtime.bigint()-t0)/1e6;
  let outcome = null;
  if (p.status === 0) outcome = JSON.parse(p.stdout.trim().split(/\r?\n/).at(-1));
  const m = /Error: ([^\n]+)/.exec(p.stderr || '');
  return {label,accepted:p.status===0,status:p.status,bytes:bytes.length,sha256:sha256(bytes),elapsedMs,outcome,error:m?m[1]:null};
}

function terminalAncestry(records) {
  const seen = new Set(), stack=[records.length-1];
  while (stack.length) {
    const i=stack.pop();
    if (seen.has(i)) continue;
    seen.add(i);
    for (const p of records[i].parents || []) stack.push(p);
  }
  return seen;
}
function replayResolution(records) {
  const known=[]; let nres=0;
  for (let i=0;i<records.length;i++) {
    const r=records[i];
    if (r.kind === 'RES') {
      if (!Array.isArray(r.parents) || r.parents.length !== 2 || r.parents.some(p=>p<0||p>=i)) throw new Error('bad parents '+i);
      const A=known[r.parents[0]], B=known[r.parents[1]], p=r.pivot;
      if (!A.includes(p) || !B.includes(-p)) throw new Error('pivot '+i);
      const got=key([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)]);
      if (!equal(got,r.c)) throw new Error('resolvent '+i);
      nres++;
    }
    known.push(r.c);
  }
  return {resolution:nres,terminal:known.at(-1)};
}
function countOriginalModels() {
  const {h,edges,charge}=seed.spec;
  let models=0;
  for (let mask=0;mask<2**edges.length;mask++) {
    const parity=Array(h).fill(0);
    edges.forEach(([u,v],i)=>{const bit=(mask>>i)&1;parity[u]^=bit;parity[v]^=bit;});
    if (parity.every((x,i)=>x===charge[i])) models++;
  }
  return {assignmentsChecked:2**edges.length,satisfyingAssignments:models};
}

function makeSourceRecords() {
  const out=seed.records.slice(0,41).map(clone);
  if (out.some(r=>r.kind!=='SOURCE')) throw new Error('SOURCE prefix changed');
  return out;
}
function buildForOrder(order) {
  const rec=makeSourceRecords();
  const seen=new Map(rec.map((r,i)=>[clauseKey(r.c),i]));
  let active=new Map(rec.map((r,i)=>[clauseKey(r.c),i]));
  for (const p of order) {
    const pos=[],neg=[],remain=new Map();
    for (const [json,i] of active) {
      const c=JSON.parse(json);
      if (c.includes(p)) pos.push([c,i]);
      else if (c.includes(-p)) neg.push([c,i]);
      else remain.set(json,i);
    }
    for (const [A,ia] of pos) for (const [B,ib] of neg) {
      const c=key([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)]);
      if (c.some(x=>c.includes(-x))) continue;
      const s=clauseKey(c);
      if (!seen.has(s)) {
        const id=rec.length;
        rec.push({kind:'RES',c,parents:[ia,ib],pivot:p});
        seen.set(s,id);
      }
      remain.set(s,seen.get(s));
    }
    active=remain;
  }
  const endpoint=active.get(clauseKey([-seed.spec.guard]));
  if (endpoint===undefined) return null;
  const keep=new Set(Array.from({length:41},(_,i)=>i)), work=[endpoint];
  while (work.length) {
    const i=work.pop();
    if (keep.has(i)) continue;
    keep.add(i);
    if (rec[i].kind==='RES') work.push(...rec[i].parents);
  }
  const ix=[...keep].sort((a,b)=>a-b), trans=new Map(ix.map((old,i)=>[old,i]));
  const records=ix.map(i=>({...rec[i],parents:rec[i].parents.map(j=>trans.get(j))}));
  records.push({kind:'RES',c:[],parents:[trans.get(40),trans.get(endpoint)],pivot:seed.spec.guard});
  const nres=records.filter(r=>r.kind==='RES').length;
  return {
    spec:clone(seed.spec),
    gate_defs:[[0,17,1,2]],
    records,
    summary:{source:41,resolution:nres,def_views:0,paid_gates:1,paid_total:nres+1,live_records:records.length}
  };
}

function xorshift32(seedValue) {
  let x=seedValue>>>0;
  return ()=>{x^=x<<13;x^=x>>>17;x^=x<<5;return (x>>>0)/4294967296};
}
function shuffle(base,rnd) {
  const a=base.slice();
  for (let i=a.length-1;i>0;i--) { const j=Math.floor(rnd()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; }
  return a;
}
function searchOrders() {
  const rnd=xorshift32(0x5a17c0de);
  let tested=0, bestPacket=buildForOrder(BASE_ORDER), bestOrder=BASE_ORDER.slice();
  if (!bestPacket) throw new Error('baseline order failed');
  let best=bestPacket.summary.resolution;
  const histogram={};
  function test(order) {
    const packet=buildForOrder(order); tested++;
    if (!packet) return;
    const w=packet.summary.resolution;
    histogram[w]=(histogram[w]||0)+1;
    if (w<best) {best=w;bestOrder=order.slice();bestPacket=packet;}
  }
  test(BASE_ORDER);
  for (let r=0;r<4000;r++) test(shuffle(BASE_ORDER,rnd));
  let improved=true;
  while (improved) {
    improved=false;
    const start=best;
    for (let i=0;i<bestOrder.length;i++) for (let j=i+1;j<bestOrder.length;j++) {
      const q=bestOrder.slice();[q[i],q[j]]=[q[j],q[i]];test(q);
    }
    improved=best<start;
  }
  return {tested,best,bestOrder,bestPacket,histogram};
}

const ancestry=terminalAncestry(seed.records);
const sourceIndices=seed.records.map((r,i)=>r.kind==='SOURCE'?i:null).filter(i=>i!==null);
const resIndices=seed.records.map((r,i)=>r.kind==='RES'?i:null).filter(i=>i!==null);
const deadSources=sourceIndices.filter(i=>!ancestry.has(i));
const deadResolution=resIndices.filter(i=>!ancestry.has(i));
const replay=replayResolution(seed.records);
if (!equal(replay.terminal,[]) || replay.resolution!==62) throw new Error('seed RES replay failed');
if (deadResolution.length!==0) throw new Error('unexpected dead RES '+deadResolution);
if (seed.records.some(r=>r.kind==='DEF')) throw new Error('unexpected DEF facet');
const ownerOutput=seed.gate_defs[0][1];
const ownerOccurrences=seed.records.reduce((n,r)=>n+r.c.filter(x=>Math.abs(x)===ownerOutput).length,0);
if (ownerOccurrences!==0) throw new Error('owner is not syntactically dead');
const sourceEnumeration=countOriginalModels();
if (sourceEnumeration.satisfyingAssignments!==0) throw new Error('original source unexpectedly SAT');

const noOwner=clone(seed);
noOwner.gate_defs=[];
noOwner.summary.paid_gates=0;
noOwner.summary.paid_total=62;
const ownerVariants=[
  {label:'owner_original',tuple:[0,17,1,2]},
  {label:'owner_repeated_positive_input',tuple:[0,17,1,1]},
  {label:'owner_complementary_inputs',tuple:[0,17,1,-1]},
  {label:'owner_repeated_negative_input',tuple:[0,17,-15,-15]},
  {label:'owner_max_safe_ids_complementary_inputs',tuple:[Number.MAX_SAFE_INTEGER,Number.MAX_SAFE_INTEGER,15,-15]},
  {label:'owner_large_gate_id',tuple:[123456789,17,1,2]}
];
const invalidOwners=[
  {label:'invalid_owner_output_guard',tuple:[0,16,1,2]},
  {label:'invalid_owner_output_edge',tuple:[0,15,1,2]},
  {label:'invalid_owner_input_guard',tuple:[0,17,16,2]},
  {label:'invalid_owner_forward_input',tuple:[0,18,17,2]},
  {label:'invalid_owner_unsafe_output',tuple:[0,Number.MAX_SAFE_INTEGER+1,1,2]},
  {label:'invalid_owner_negative_id',tuple:[-1,17,1,2]}
];

const search=searchOrders();
const tempDir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv5-491-'));
try {
  const cli=[];
  cli.push(runCLI(seed,tempDir,'baseline_exact_bytes',packetBuf));
  cli.push(runCLI(noOwner,tempDir,'owner_free_core_W62'));
  for (const v of ownerVariants) {
    const p=clone(seed);p.gate_defs=[v.tuple];
    if (v.label==='owner_max_safe_ids_complementary_inputs') fs.writeFileSync(HOSTILE_OUT,JSON.stringify(p)+'\n');
    cli.push(runCLI(p,tempDir,v.label));
  }
  for (const v of invalidOwners) {
    const p=clone(seed);p.gate_defs=[v.tuple];
    cli.push(runCLI(p,tempDir,v.label));
  }
  const searchedPacket=search.bestPacket;
  cli.push(runCLI(searchedPacket,tempDir,'searched_best_RES'+search.best));

  const baseline=cli.find(x=>x.label==='baseline_exact_bytes');
  if (!baseline.accepted || baseline.outcome.paid!==63 || baseline.outcome.res!==62) throw new Error('baseline CLI failed');
  if (cli.find(x=>x.label==='owner_free_core_W62').accepted) throw new Error('owner-free full CLI accepted');
  for (const v of ownerVariants) if (!cli.find(x=>x.label===v.label).accepted) throw new Error('valid owner variant rejected '+v.label);
  for (const v of invalidOwners) if (cli.find(x=>x.label===v.label).accepted) throw new Error('invalid owner accepted '+v.label);
  const searchedCLI=cli.find(x=>x.label==='searched_best_RES'+search.best);
  if (!searchedCLI.accepted) throw new Error('searched best CLI rejected');

  const coreBaseline=runCore(seed), coreNoOwner=runCore(noOwner);
  if (!coreBaseline.accepted || !coreNoOwner.accepted || coreNoOwner.outcome.paid!==62) throw new Error('core split failed');

  const output={
    schema:'LSPV5_491_BRIDGE_DP_OWNER_SENTINEL/v1',
    timestampPacific:'2026-11-11 09:48 PST',
    status:'PROVED/RESTRICTED owner-sentinel parametricity + COMPUTATIONAL exact OS replay and bounded order search',
    pins,
    independentReplay:{
      records:seed.records.length,
      sourceRecords:sourceIndices.length,
      resolutionRecords:resIndices.length,
      terminalAncestors:ancestry.size,
      terminalDeadSources:deadSources,
      terminalDeadResolution:deadResolution,
      ownerOutput,
      ownerLiteralOccurrences:ownerOccurrences,
      defFacetRecords:0,
      sourceEnumeration
    },
    originalCore:{baseline:coreBaseline,ownerFreeW62:coreNoOwner},
    exactOSCLI:cli,
    ownerVariants,
    invalidOwners,
    orderSearch:{
      deterministicSeed:'0x5a17c0de',
      tested:search.tested,
      baselineResolution:62,
      bestResolution:search.best,
      bestOrder:search.bestOrder,
      histogram:search.histogram
    },
    resourceLedger:{
      cliRuns:cli.length,
      cliAccepts:cli.filter(x=>x.accepted).length,
      cliRejects:cli.filter(x=>!x.accepted).length,
      cliElapsedMs:cli.reduce((s,x)=>s+x.elapsedMs,0),
      auditElapsedMs:Number(process.hrtime.bigint()-scriptStart)/1e6,
      auditProcessMaxRSSKiB:process.resourceUsage().maxRSS,
      note:'auditProcessMaxRSSKiB is the parent audit process high-water mark on this host; child-checker RSS, caches, Git retrieval, publication and proof discovery are not included'
    },
    conclusion:'The exact /575 W=63 packet and all 62 signed RES steps independently replay. Every RES node is terminal-live; four mandatory SOURCE records are terminal-dead. Removing the only dead owner and repairing summaries yields a genuine mathematical-core W=62 proof but the full CLI rejects through its self-test. Six semantically unrelated but syntactically legal single dead owners, including repeated/complementary inputs and MAX_SAFE_INTEGER IDs, all restore full-CLI acceptance at W=63. The paid owner is therefore a one-unit CLI sentinel in this family, not terminal proof work.',
    limitation:'The deterministic order search is finite and does not prove 62 RES optimal. Archived /386 sibling only; no complete historical R_mix341 dispatcher, all-rule lower bound, memory lower bound, or B2/B3 transfer.'
  };
  fs.writeFileSync(RAW_OUT,JSON.stringify(output,null,2)+'\n');
  process.stdout.write(JSON.stringify(output,null,2)+'\n');
} finally {
  fs.rmSync(tempDir,{recursive:true,force:true});
}
