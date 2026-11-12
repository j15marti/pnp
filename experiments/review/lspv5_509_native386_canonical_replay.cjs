#!/usr/bin/env node
'use strict';
// LSPV-5/509: exact accepted-language replay under JSON parse/reserialize.
// Run from repository root:
// node experiments/review/lspv5_509_native386_canonical_replay.cjs [raw.json] [canonical-witness.json]
// The unchanged archived /386 CLI is the sole acceptance oracle.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),
 cp=require('node:child_process'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const rel={
 checker:'experiments/arc/lspv2_386_independent_verify.js',
 alias508:'results/raw/review/2026-11-12_1048_LSPV5_508_NATIVE386_WIRE_ALIAS_ACCEPTED.json',
 seed587:'results/raw/arc/2026-11-12_0424_LSPV3_587_NATIVE_CONSTANT_FACET_ACCEPTED_PACKET.json',
 live597:'results/raw/arc/2026-11-12_1100_LSPV1_597_NATIVE386_LIVE16_W44_ACCEPTED.json',
 live580:'results/raw/arc/580_LIVE_TWO_BRANCHES_W33.json',
 quotient580:'results/raw/arc/580_DEF_THEN_RES_W31.json',
 work566:'results/raw/arc/2026-11-12_1031_LSPV4_566_W38_P45_AREA958_NATIVE386_ACCEPTED.json',
 area566:'results/raw/arc/2026-11-12_1031_LSPV4_566_W39_P45_AREA748_NATIVE386_ACCEPTED.json'
};
const pins={checker:'338305c0ce101704205e57543756b8127074a986',
 alias508:'5ed2d1882cd475569aac47438bb6a270ec99c49f',
 seed587:'4177ec15a0c7253378d5652a6b13b7152601d300',
 live597:'a9514ed6d28d19403d745a583c3096d36cd1a399',
 live580:'1879118e4e4f4244961f75f62e6207da67f0f345',
 quotient580:'6b2c343ab68634767b87bf0f7bce771529cb0c41',
 work566:'28fc9f41ec151a741e70274637c06629fb9a224f',
 area566:'07a43d1a3edd9fc2e97a26e0fd0a4c769145ba4d'};
const at=k=>path.join(root,rel[k]);
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const blob=b=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex');
for(const k of Object.keys(rel))assert.equal(blob(fs.readFileSync(at(k))),pins[k],'Git blob drift '+k);
const canonical=b=>Buffer.from(JSON.stringify(JSON.parse(b.toString('utf8')))+'\n');
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv5-509-'));
const rows=[];
function native(name,bytes,want){
 const f=path.join(dir,name.replace(/[^A-Za-z0-9_-]/g,'_')+'.json');fs.writeFileSync(f,bytes);
 const p=cp.spawnSync(process.execPath,[at('checker'),f],{encoding:'utf8',timeout:30000,maxBuffer:32*1024*1024});
 if(p.error)throw p.error;const accepted=p.status===0;
 assert.equal(accepted,want,name+' native verdict '+p.stderr.slice(-300));
 const out=accepted?JSON.parse(p.stdout):null;
 if(out)assert.equal(out.sha256,sha(bytes),'checker raw SHA diagnostic');
 return {name,accepted,bytes:bytes.length,sha256:sha(bytes),paid:out?.paid??null,
  records:out?.records??null,assertions:out?.assertions??null,negativeTests:out?.negativeTests??null,
  rejection:accepted?null:p.stderr.trim().slice(-240)};
}
function pair(name,bytes,want){
 const c=canonical(bytes),a=native(name+':raw',bytes,want),b=native(name+':canonical',c,want);
 assert.equal(a.accepted,b.accepted,name+' acceptance mismatch');
 if(want){assert.equal(a.paid,b.paid,name+' paid mismatch');assert.equal(a.records,b.records,name+' record mismatch');}
 rows.push({name,want,raw:a,canonical:b,raw_differs:!bytes.equals(c),
  parsed_roundtrip_equal:JSON.stringify(JSON.parse(bytes))===JSON.stringify(JSON.parse(c))});
 return c;
}
try{
 for(const k of ['alias508','seed587','live597','live580','quotient580','work566','area566'])
  pair('published-'+k,fs.readFileSync(at(k)),true);
 const base=JSON.parse(fs.readFileSync(at('alias508'),'utf8'));
 const compact=JSON.stringify(base)+'\n';
 const reversed=Object.fromEntries(Object.entries(base).reverse());
 const positive={
  'pretty-whitespace':Buffer.from(JSON.stringify(base,null,2)+'\n'),
  'reverse-top-property-order':Buffer.from(JSON.stringify(reversed)+'\n'),
  'duplicate-summary-last-wins':Buffer.from('{"summary":{"paid_total":0},'+compact.slice(1)),
  'duplicate-paid-last-wins':Buffer.from(compact.replace('"paid_total":39','"paid_total":0,"paid_total":39')),
  'duplicate-kind-last-wins':Buffer.from(compact.replace('"kind":"SOURCE"','"kind":"NOPE","kind":"SOURCE"')),
  'h-decimal-alias':Buffer.from(compact.replace('"h":4','"h":4.0')),
  'gate-id-negative-zero':Buffer.from(compact.replace('"gate_defs":[[0,','"gate_defs":[[-0,')),
  'ignored-overflow-number':Buffer.from(compact.trimEnd().slice(0,-1)+',"ignored":1e400}\n')
 };
 for(const [name,b] of Object.entries(positive))pair(name,b,true);
 const hostile=[];
 let x=structuredClone(base);x.records.at(-1).pivot=999999;hostile.push(['terminal-pivot',x]);
 x=structuredClone(base);x.summary.paid_total--;hostile.push(['underpaid',x]);
 x=structuredClone(base);x.records[0].c=[-x.spec.guard];hostile.push(['forged-source',x]);
 x=structuredClone(base);x.gate_defs[0][0]={bad:true};hostile.push(['object-gate-id',x]);
 x=structuredClone(base);x.records[0]=[];hostile.push(['object-record-shape',x]);
 for(const [name,d] of hostile)pair('hostile-'+name,Buffer.from(JSON.stringify(d)+'\n'),false);
 const canonicalWitness=canonical(fs.readFileSync(at('alias508')));
 const witnessPath=path.resolve(process.argv[3]||'results/raw/review/2026-11-12_1148_LSPV5_509_NATIVE386_CANONICAL_ACCEPTED.json');
 fs.mkdirSync(path.dirname(witnessPath),{recursive:true});fs.writeFileSync(witnessPath,canonicalWitness);
 const raw={id:'LSPV-5/509',timestamp:'2026-11-12 11:48 America/Los_Angeles',
  target:'archived /386 acceptance under canonical JSON parse/reserialize',
  checker:{path:rel.checker,git_blob:pins.checker,sha256:sha(fs.readFileSync(at('checker'))),unchanged:true},
  execution:'actual OS Node subprocess for every raw and canonical packet; complete original CLI and eleven bundled negative controls on every accepted run',
  theorem_scope:'finite replay plus source-inspection lemma for accepted /386 packets; diagnostic raw SHA changes and is not acceptance',
  corpus:{published_packets:7,accepted_alias_variants:8,rejected_hostile_variants:5,pairs:rows.length,native_runs:2*rows.length},
  counts:{accepted_pairs:rows.filter(r=>r.want).length,rejected_pairs:rows.filter(r=>!r.want).length,
   verdict_mismatches:rows.filter(r=>r.raw.accepted!==r.canonical.accepted).length,
   paid_mismatches:rows.filter(r=>r.want&&r.raw.paid!==r.canonical.paid).length,
   byte_distinct_pairs:rows.filter(r=>r.raw_differs).length},
  canonical_witness:{path:path.relative(root,witnessPath),bytes:canonicalWitness.length,sha256:sha(canonicalWitness),paid:39},
  rows,limitations:['not the unavailable unified historical R_mix341 dispatcher','not a proof-size lower bound','not a raw-byte-output equivalence: the CLI reports the raw input SHA','P2-C3, P2-B1 and P2-B2/B3 remain OPEN; P versus NP OPEN']};
 const rawPath=path.resolve(process.argv[2]||'results/raw/review/2026-11-12_1148_LSPV5_509_NATIVE386_CANONICAL_REPLAY_RAW.json');
 fs.mkdirSync(path.dirname(rawPath),{recursive:true});fs.writeFileSync(rawPath,JSON.stringify(raw,null,2)+'\n');
 console.log(JSON.stringify({status:'PASS',counts:raw.counts,canonical_witness:raw.canonical_witness,raw:path.relative(root,rawPath)}));
}finally{fs.rmSync(dir,{recursive:true,force:true})}
