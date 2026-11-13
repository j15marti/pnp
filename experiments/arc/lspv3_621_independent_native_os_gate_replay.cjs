'use strict';
// LSPV-3/621 reproducibility runner. Requires Node.js >=18 and a local
// j15marti/pnp checkout. This is a runner of the UNMODIFIED archived checkers,
// not a new checker or an independent implementation of R_mix341.
// Usage: node experiments/arc/lspv3_621_independent_native_os_gate_replay.cjs [output.json]
const fs=require('node:fs');
const cp=require('node:child_process');
const os=require('node:os');
const path=require('node:path');
const crypto=require('node:crypto');
const assert=require('node:assert/strict');
const ROOT=path.resolve(__dirname,'../..');
const files={
 checker341:'experiments/arc/lspv2_341_independent_verify.js',
 packet341:'results/raw/arc/2026-11-10_1724_LSPV3_557_SINGLE_SAT_PACKET.json',
 source341:'results/raw/arc/2026-11-13_1128_LSPV3_620_ACCEPTED_341_SAT_SOURCE.cnf',
 checker386:'experiments/arc/lspv2_386_independent_verify.js',
 packet386:'results/raw/arc/2026-11-11_0407_LSPV2_555_ACCEPTED_LIVE_DEF_RES_K1.json'
};
const pins={
 checker341:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
 packet341:'6cf9b0fe1e5a9419e8967d836c707c385418b810',
 source341:'c6f8bbf09baf6547de6fea04ac74dd0ecb32f6bd',
 checker386:'338305c0ce101704205e57543756b8127074a986',
 packet386:'aeeb555c4dcf7f510a9a501c8afc609b629a9298'
};
function blobHash(buffer) {
 return crypto.createHash('sha1').update(Buffer.from('blob '+buffer.length+'\0')).update(buffer).digest('hex');
}
const payload={};
for(const [k,file] of Object.entries(files)){
 const bytes=fs.readFileSync(path.join(ROOT,file));
 assert.equal(blobHash(bytes),pins[k],'immutable Git blob mismatch '+file);
 payload[k]=bytes;
}
const one=JSON.parse(payload.packet341.toString('utf8'));
const k4=JSON.parse(payload.packet386.toString('utf8'));
assert.equal(one.fixtures.length,1);
assert.equal(one.fixtures[0].clauses.length,48);
assert.equal(one.fixtures[0].proof.length,47);
assert.equal(one.fixtures[0].charges[0],'1');
assert.equal(one.fixtures[0].proof[2].support,'012');
function dimacs(text){
 const t=text.trim().split(/\s+/);
 assert.deepEqual(t.slice(0,4),['p','cnf','18','48']);
 let rows=[],r=[];
 for(const w of t.slice(4)){
  const v=Number(w); assert(Number.isSafeInteger(v));
  if(v===0){ rows.push(r);r=[]; } else r.push(v);
 }
 assert.equal(r.length,0);assert.equal(rows.length,48);
 return rows;
}
const clauses=dimacs(payload.source341.toString('utf8'));
assert.deepEqual(clauses,one.fixtures[0].clauses.map(x=>x.literals));
function sat(c,assignment) {
 return c.some(l=>assignment[Math.abs(l)-1]===(l>0?1:0));
}
const witness='101001000000100000'.split('').map(Number);
assert(clauses.every(c=>sat(c,witness)));
const z=Array(18).fill(0);
assert.deepEqual(clauses.map((c,i)=>sat(c,z)?null:i).filter(x=>x!==null),[0]);
let modelCount=0;
for(let m=0;m<(1<<18);m++){
 const a=Array.from({length:18},(_,j)=>(m>>j)&1);
 if(clauses.every(c=>sat(c,a)))modelCount++;
}
assert.equal(modelCount,64);
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-621-'));
function clone(d){return JSON.parse(JSON.stringify(d));}
function original(id,dat) {
 const packetFile=path.join(temp,'packet.json');
 fs.writeFileSync(packetFile,JSON.stringify(dat));
 const runner=path.join(ROOT,files['checker'+id]);
 const r=cp.spawnSync(process.execPath,[runner,packetFile],{cwd:ROOT,encoding:'utf8',maxBuffer:10_000_000});
 if(r.error)throw r.error;
 if(r.status===0){
  const j=JSON.parse(r.stdout);
  return {accepted:true,assertions:j.checks??j.assertions,paid:j.paid??null};
 }
 const stderr=(r.stderr||r.stdout||'');
 const match=stderr.match(/(?:Error|TypeError): [^\r\n]+/);
 return {accepted:false,error:match?match[0]:stderr.slice(0,240),exit_status:r.status};
}
const tests=[
 ['341_single_sat_source','341',one,true,d=>{}],
 ['341_invalid_numeric_charge','341',one,false,d=>{d.fixtures[0].charges[0]=1;}],
 ['341_valid_typed_support_rejected','341',one,false,d=>{d.fixtures[0].proof[2].support=[0,1,12];}],
 ['341_bad_original_clause','341',one,false,d=>{d.fixtures[0].clauses[0].literals[0]=999;}],
 ['341_bad_sink','341',one,false,d=>{d.fixtures[0].proof.at(-1).row.rhs^=1;}],
 ['341_untrusted_sat_external_sidecar','341',one,true,d=>{d.externalOriginal={clauses:[[1],[-1]],claim:'SAT or UNSAT'};}],
 ['341_untrusted_context_sidecar','341',one,true,d=>{d.fixtures[0].untrustedAssumptions=['x1'];}],
 ['386_original_odd_K4','386',k4,true,d=>{}],
 ['386_even_charge_rejected','386',k4,false,d=>{d.spec.charge[0]=0;}],
 ['386_local_convert_rejected','386',k4,false,d=>{d.records[21].kind='LOCAL-CONVERT';}],
 ['386_and3_rejected','386',k4,false,d=>{d.records[21].kind='AND3';}],
 ['386_untrusted_external_sat_sidecar','386',k4,true,d=>{d.externalOriginal={clauses:[[1],[-1]],assumptions:['x1'],closed:true};}]
];
let outcomes=[];
try {
 for(const [id,checker,seed,expected,change] of tests){
  let d=clone(seed);change(d);
  let obs=original(checker,d);
  assert.equal(obs.accepted,expected,'unexpected original checker verdict: '+id);
  outcomes.push({id,checker,expected,...obs});
 }
} finally {
 fs.rmSync(temp,{recursive:true,force:true});
}
const result={
 id:'LSPV-3/621',
 execution:'actual Node.js OS subprocess, one unchanged archived checker per case',
 source_sha256:crypto.createHash('sha256').update(payload.source341).digest('hex'),
 pins,source:{variables:18,clauses:48,models:modelCount,witness:witness.join(''),zero_assignment_falsifies_only_source:0},
 packet341:{sourceClauses:48,paidNodes:47,oneFixture:true,rawBytes:payload.packet341.length},
 packet386:{recordKinds:['SOURCE','DEF','RES'],originalSourceDomain:'guarded odd-charge cubic Tseitin only'},
 outcomes,all_expected:true,
 limitations:['Not full historical R_mix341','No full mixed RES-to-AND3 or DEF-to-LOCAL-CONVERT authority','Not a new proof system or complexity lower bound']
};
const pretty=JSON.stringify(result,null,2)+'\n';
if(process.argv[2])fs.writeFileSync(process.argv[2],pretty);
console.log(pretty);
