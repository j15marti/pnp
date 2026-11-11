#!/usr/bin/env node
'use strict';
/*
 * LSPV-2/552: archived native-dispatch accepted-byte atlas.
 * Run from j15marti/pnp root:
 *   node experiments/arc/lspv2_552_archived_dispatch_atlas.cjs results/raw/arc/local_552.json
 * Optional third argument --emit=DIR writes the 60 exact UTF-8 JSON packets.
 *
 * The ORIGINAL /341 and /386 checker files are invoked with real Node subprocesses.
 * This script is a differential packet generator, NOT an authoritative checker
 * and NOT a full R_mix341 rule dispatcher.
 */
const fs = require('node:fs');
const cp = require('node:child_process');
const os = require('node:os');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');

const R = 'experiments/arc/';
const PATHS = Object.freeze({
  producer: R + 'lspv2_341_mixed_tseitin_min_dag.js',
  checker341: R + 'lspv2_341_independent_verify.js',
  checker386: R + 'lspv2_386_independent_verify.js',
  seed386: 'results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json'
});
const PINNED_BLOBS = Object.freeze({
  producer:'4081022e8a3841d79f751a3d3a7a10decbb026da',
  checker341:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
  checker386:'338305c0ce101704205e57543756b8127074a986',
  seed386:'08aa169b5db49b2ddd1cb5a9b6890fcc3b790916'
});
const OPS = Object.freeze([
  'SOURCE','RES','DEF','AND3','XOR','GF2','LOCAL-CONVERT',
  'WEAKEN','DISCHARGE','JOIN','DELETE','SPLIT_AND'
]);
const clone = obj => JSON.parse(JSON.stringify(obj));
const sha256 = txt => crypto.createHash('sha256').update(Buffer.from(txt,'utf8')).digest('hex');
function gitBlob(text) {
  const buf = Buffer.from(text, 'utf8');
  return crypto.createHash('sha1').update(Buffer.from('blob '+buf.length+'\0')).update(buf).digest('hex');
}
function fnv32(text) {
  let h = 2166136261;
  for(let i=0;i<text.length;i++) h = Math.imul(h ^ text.charCodeAt(i),16777619)>>>0;
  return h.toString(16).padStart(8,'0');
}
function buildSuite(native341, native386, check341, check386, packetSink) {
  const base341=clone(native341), base386=clone(native386);
  const slots=[
    {checker:'341',slot:'first_AND3',index:0,field:'rule',original:'AND3'},
    {checker:'341',slot:'last_XOR',index:base341.fixtures[0].proof.length-1,field:'rule',original:'XOR'},
    {checker:'386',slot:'first_SOURCE',index:0,field:'kind',original:'SOURCE'},
    {checker:'386',slot:'first_DEF',index:base386.records.findIndex(r=>r.kind==='DEF'),field:'kind',original:'DEF'},
    {checker:'386',slot:'first_RES',index:base386.records.findIndex(r=>r.kind==='RES'),field:'kind',original:'RES'}
  ];
  for(const s of slots) assert.ok(s.index>=0,'missing role for '+s.slot);
  const baseline={341:check341(JSON.stringify(base341)),386:check386(JSON.stringify(base386))};
  assert.equal(baseline[341].ok,true,'original /341 baseline');
  assert.equal(baseline[386].ok,true,'original /386 baseline');
  assert.equal(baseline[341].checks,30714,'/341 original assertions');
  assert.equal(baseline[386].checks,4663,'/386 original assertions');
  const trials=[];
  for(const s of slots) for(const opcode of OPS) {
    const p=clone(s.checker==='341'?base341:base386);
    const record=s.checker==='341'?p.fixtures[0].proof[s.index]:p.records[s.index];
    record[s.field]=opcode;
    const bytes=JSON.stringify(p);
    const expected=opcode===s.original;
    const verdict=s.checker==='341'?check341(bytes):check386(bytes);
    assert.equal(verdict.ok,expected,'native-dispatch mismatch '+s.checker+'/'+s.slot+'/'+opcode+': '+JSON.stringify(verdict));
    const row={checker:s.checker,slot:s.slot,index:s.index,field:s.field,opcode,
      expected,utf8_bytes:Buffer.byteLength(bytes,'utf8'),sha256:sha256(bytes),fnv32:fnv32(bytes),...verdict};
    trials.push(row);
    if(packetSink) packetSink(s,opcode,bytes);
  }
  return {
    run:'LSPV-2/552',mode:'direct-original-checker-dispatch-packet-atlas',
    authority_scope:'/341 SOURCE/AND3/XOR fixture checker and separate /386 SOURCE/DEF-view/RES checker',
    cross_rule_authorized:false,full_historical_Rmix341_authenticated:false,
    source_sha256:{
      source341:sha256(JSON.stringify(base341.fixtures[0].clauses)),
      source386:sha256(JSON.stringify({spec:base386.spec,sources:base386.records.filter(r=>r.kind==='SOURCE')}))
    },
    baseline,graph341_K4_paid:base341.fixtures[0].proof.length,
    archive386_paid:base386.summary.paid_total,
    atlas_total:trials.length,accepted:trials.filter(r=>r.ok).length,
    rejected:trials.filter(r=>!r.ok).length,
    unknown341:trials.filter(r=>r.checker==='341'&&r.error==='unknown rule').length,
    invalid_kind386:trials.filter(r=>r.checker==='386'&&r.error&&r.error.startsWith('record kind or clause')).length,
    rules_attempted:OPS,slots:slots.map(s=>({checker:s.checker,slot:s.slot,original:s.original,index:s.index})),
    trials,
    open:['P2-D1','P2-C3','P2-B1','P2-B2','P2-B3'],
    caution:'Only mutations of native accepted packets. Nonaccepted opcodes are not proved illegal in unrecovered full R_mix341.'
  };
}
function main() {
  const root=process.cwd();
  const paths=Object.fromEntries(Object.entries(PATHS).map(([k,v])=>[k,path.join(root,v)]));
  for(const [name,f] of Object.entries(paths)) {
    const body=fs.readFileSync(f,'utf8');
    assert.equal(gitBlob(body),PINNED_BLOBS[name],'original pinned blob mismatch: '+name);
  }
  const producer=cp.spawnSync(process.execPath,[paths.producer],{cwd:root,encoding:'utf8',maxBuffer:8*1024*1024,timeout:120000});
  assert.equal(producer.status,0,'producer OS Node failed: '+producer.stderr);
  const p341=JSON.parse(producer.stdout);
  const p386=JSON.parse(fs.readFileSync(paths.seed386,'utf8'));
  assert.equal(p341.fixtures.length,7);
  const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2-552-'));
  const emit=process.argv.find(a=>a.startsWith('--emit='));
  const emitDir=emit?path.resolve(emit.slice('--emit='.length)):null;
  if(emitDir) fs.mkdirSync(emitDir,{recursive:true});
  let sequence=0;
  function execute(checker,text) {
    const filename=path.join(tmp,'packet.json');
    fs.writeFileSync(filename,Buffer.from(text,'utf8'));
    const run=cp.spawnSync(process.execPath,[checker,filename],
      {cwd:root,encoding:'utf8',maxBuffer:8*1024*1024,timeout:120000});
    if(run.error) throw run.error;
    if(run.status===0) {
      const obj=JSON.parse(run.stdout);
      return {ok:true,checks:obj.checks??obj.assertions};
    }
    const match=run.stderr.match(/Error: ([^\r\n]+)/);
    return {ok:false,error:match?match[1]:'native checker failed with status '+run.status};
  }
  try {
    const result=buildSuite(p341,p386,
      text=>execute(paths.checker341,text),
      text=>execute(paths.checker386,text),
      emitDir?(slot,opcode,bytes)=>{
        const filename=String(++sequence).padStart(3,'0')+'_'+slot.checker+'_'+slot.slot+'_'+opcode.replace(/[^a-zA-Z0-9]/g,'_')+'.json';
        fs.writeFileSync(path.join(emitDir,filename),Buffer.from(bytes,'utf8'));
      }:null);
    result.backend='original unchanged checker files executed as OS Node subprocesses';
    result.original_git_blobs=PINNED_BLOBS;
    result.node_version=process.version;
    const out=process.argv[2]&&!process.argv[2].startsWith('--')?process.argv[2]:null;
    if(out) fs.writeFileSync(out,JSON.stringify(result,null,2)+'\n','utf8');
    console.log(JSON.stringify({backend:result.backend,baseline:result.baseline,
      trials:result.atlas_total,accepted:result.accepted,rejected:result.rejected,
      unknown341:result.unknown341,invalid_kind386:result.invalid_kind386}));
  } finally {fs.rmSync(tmp,{recursive:true,force:true});}
}
if(require.main===module) main();
module.exports={buildSuite,OPS,PATHS,PINNED_BLOBS};
