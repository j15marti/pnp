#!/usr/bin/env node
'use strict';
// LSPV-5/505: independent corpus-wide OS replay of LSPV-1/591's exact
// complete-CLI predicate for the unchanged archived /386 checker.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),
  vm=require('node:vm'),cp=require('node:child_process'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const checkerText=fs.readFileSync(checker,'utf8');
function blob(b){return crypto.createHash('sha1').update('blob '+Buffer.byteLength(b)+'\0').update(b).digest('hex')}
function sha(b){return crypto.createHash('sha256').update(b).digest('hex')}
assert.equal(blob(checkerText),'338305c0ce101704205e57543756b8127074a986');
const sandbox={require,process:{argv:[process.execPath,checker]},console:{log(){}},structuredClone};
vm.runInNewContext(checkerText+'\n;globalThis.nativeCore=checkProof;',sandbox,{filename:checker});
function walk(d,out=[]){for(const ent of fs.readdirSync(d,{withFileTypes:true})){
  const p=path.join(d,ent.name);if(ent.isDirectory())walk(p,out);else if(ent.name.endsWith('.json'))out.push(p);
}return out}
const roots=['results/raw/arc','results/raw/review'].map(x=>path.join(root,x)).filter(fs.existsSync);
const files=roots.flatMap(x=>walk(x)).sort();
const rows=[];let parsed=0,packetShaped=0,coreAccepted=0,cliRuns=0;
for(const file of files){
  const bytes=fs.readFileSync(file);let d;try{d=JSON.parse(bytes)}catch{continue}parsed++;
  if(!(d&&d.spec&&d.records&&d.gate_defs&&d.summary))continue;packetShaped++;
  let core;try{core=sandbox.nativeCore(d,{control:true})}catch{continue}coreAccepted++;
  const recordsIsArray=Array.isArray(d.records),owners=d.gate_defs.length;
  const last=recordsIsArray?d.records.at(-1):d.records[d.records.length-1],pivot=last&&last.pivot;
  const theorem591Prediction=owners>=1&&pivot!==999999;
  const predicted=recordsIsArray&&theorem591Prediction;
  const run=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',timeout:15000});cliRuns++;
  if(run.error)throw run.error;
  const actual=run.status===0;
  const stderr=(run.stderr||'').trim();
  rows.push({file:path.relative(root,file),bytes:bytes.length,sha256:sha(bytes),
    records_is_array:recordsIsArray,owners,pivot,paid:core.paid,records:core.records,source_bits:core.sourceBits,
    theorem_591_prediction:theorem591Prediction,repaired_cli_prediction:predicted,actual_cli_accept:actual,
    assertions:actual?JSON.parse(run.stdout.trim().split(/\r?\n/).at(-1)).assertions:null,
    rejection:actual?null:(stderr.match(/accepted a corrupted proof|[A-Za-z]+ mismatch|bad pivot|wrong source|paid cost/)||[])[0]||stderr.slice(0,160)});
  assert.equal(actual,predicted,'repaired predicate mismatch: '+file);
}
assert(coreAccepted>0&&rows.length===coreAccepted&&cliRuns===coreAccepted);
// Directly attack /591's displayed theorem, which omits the already-known
// Array.isArray(records) side condition from /577.  The mathematical core uses
// only numeric indexing and length, while the wrapper calls records.at(-1).
const objectBase=path.join(root,'results/raw/arc/2026-11-11_0900_LSPV1_575_BRIDGE_GUARDED_DP_NATIVE_ACCEPTED.json');
const objectPacket=JSON.parse(fs.readFileSync(objectBase,'utf8'));
objectPacket.records=Object.assign(Object.fromEntries(objectPacket.records.map((r,i)=>[String(i),r])),
  {length:objectPacket.records.length});
const objectBytes=Buffer.from(JSON.stringify(objectPacket)+'\n');
const objectWitness=path.join(root,'results/raw/review/2026-11-12_0648_LSPV5_505_RECORDS_OBJECT_CORE_ACCEPT_CLI_REJECT.json');
fs.writeFileSync(objectWitness,objectBytes);
const objectCore=sandbox.nativeCore(objectPacket,{control:true});
const objectRun=cp.spawnSync(process.execPath,[checker,objectWitness],{encoding:'utf8',timeout:15000});
if(objectRun.error)throw objectRun.error;
const objectActual=objectRun.status===0;
const object591Prediction=objectCore&&objectPacket.gate_defs.length>=1&&objectPacket.records[objectPacket.records.length-1].pivot!==999999;
const objectRepairedPrediction=object591Prediction&&Array.isArray(objectPacket.records);
assert.equal(object591Prediction,true);assert.equal(objectActual,false);assert.equal(objectRepairedPrediction,false);
const byOwners={},byVerdict={accept:0,reject:0};
for(const r of rows){byOwners[r.owners]=(byOwners[r.owners]||0)+1;byVerdict[r.actual_cli_accept?'accept':'reject']++}
const rejected=rows.filter(r=>!r.actual_cli_accept);
const theorem591Mismatches=rows.filter(r=>r.actual_cli_accept!==r.theorem_591_prediction);
const out={id:'LSPV-5/505',checker_git_blob:blob(checkerText),
  scope:'Finite local published JSON corpus; validates but does not prove or extend the original-/386 theorem, and does not authenticate full R_mix341.',
  scanned_json:files.length,parsed_json:parsed,packet_shaped:packetShaped,core_accepted:coreAccepted,
  os_cli_runs:cliRuns,repaired_predicate_mismatches:0,theorem_591_mismatches:theorem591Mismatches.length,
  by_owner_count:byOwners,by_cli_verdict:byVerdict,
  theorem_591_counterexample:{file:path.relative(root,objectWitness),bytes:objectBytes.length,sha256:sha(objectBytes),
    records_is_array:false,records_length:objectPacket.records.length,owners:objectPacket.gate_defs.length,
    final_pivot:objectPacket.records[objectPacket.records.length-1].pivot,paid:objectCore.paid,
    theorem_591_prediction:object591Prediction,actual_cli_accept:objectActual,
    repaired_prediction:objectRepairedPrediction,
    rejection:(objectRun.stderr||'').includes('.at is not a function')?'TypeError: o.records.at is not a function':(objectRun.stderr||'').slice(-200)},
  rejected_core_accepted:rejected,accepted_examples:rows.filter(r=>r.actual_cli_accept).slice(0,12),
  all_core_accepted_rows:rows};
const target=path.resolve(process.argv[2]||path.join(root,'results/raw/review/2026-11-12_0648_LSPV5_505_NATIVE386_CLI_PREDICATE_CORPUS_RAW.json'));
fs.mkdirSync(path.dirname(target),{recursive:true});fs.writeFileSync(target,JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify({id:out.id,scanned_json:out.scanned_json,packet_shaped:out.packet_shaped,
  core_accepted:out.core_accepted,cli:out.by_cli_verdict,owners:out.by_owner_count,
  theorem_591_counterexample:out.theorem_591_counterexample,
  rejected:rejected.map(r=>({file:r.file,owners:r.owners,pivot:r.pivot,rejection:r.rejection})),
  output:path.relative(root,target),sha256:sha(fs.readFileSync(target))},null,2));
