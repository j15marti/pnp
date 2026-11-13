#!/usr/bin/env node
'use strict';
// LSPV-1/623: byte-query lower bound control for original /386 checker.
// Reproducible test of syntactic sensitivity, not historical full R_mix341.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const cp=require('node:child_process'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const input=path.join(root,'results/raw/arc/2026-11-13_0900_LSPV1_622_K65536_NATIVE386_ACCEPTED.json');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const raw=fs.readFileSync(input),s=raw.toString('utf8');
const hash=crypto.createHash('sha1').update('blob '+raw.length+'\0').update(raw).digest('hex');
assert.equal(hash,'2a26fc9eeb78673b14bcfc69dc82e0308aa022ef');
const match=/1e\+(0{1000,})/.exec(s);
assert(match,'large positive exponent not found');
const zeros=match[1].length,base=match.index+3;
assert.equal(zeros,65537);
const d=JSON.parse(s);
assert.deepEqual(d.spec.charge,[1,0,0,0]);
assert.equal(d.records.length,50);
assert.equal(d.summary.paid_total,32);
const sample=new Set();
for(let j=0;j<zeros;j+=509)sample.add(j);
for(const j of [1,2,3,Math.floor(zeros/2),zeros-1])sample.add(j);
const mutated=j=>s.slice(0,base+j)+'x'+s.slice(base+j+1);
for(const j of sample){
  assert.equal(s.charAt(base+j),'0');
  assert.equal(mutated(j).length,s.length);
  assert.throws(()=>JSON.parse(mutated(j)),SyntaxError);
}
const synthetic=[];
for(const k of [1,2,16,128,1024,8192]){
  const tok='1e+'+'0'.repeat(k),txt='{"charge":['+tok+']}',start=txt.indexOf(tok)+3;
  assert.equal(JSON.parse(txt).charge[0],1);
  for(let j=0;j<k;j++)assert.throws(()=>JSON.parse(
    txt.slice(0,start+j)+'x'+txt.slice(start+j+1)),SyntaxError);
  synthetic.push({exponentZeros:k,mutationsRejected:k});
}
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv1-623-'));
const native=[];
try{
  const positive=cp.spawnSync(process.execPath,[checker,input],{encoding:'utf8',timeout:30000,maxBuffer:10000000});
  assert.equal(positive.status,0,'archived original /386 baseline rejected: '+positive.stderr);
  native.push({case:'accepted-pinned-packet',accepted:true});
  for(const j of [0,Math.floor(zeros/2),zeros-1]){
    const f=path.join(temp,'invalid_'+j+'.json');fs.writeFileSync(f,mutated(j));
    const r=cp.spawnSync(process.execPath,[checker,f],{encoding:'utf8',timeout:30000,maxBuffer:10000000});
    assert.notEqual(r.status,0,'malformed JSON unexpectedly accepted at '+j);
    native.push({case:'same-length-invalid-exponent-'+j,accepted:false});
  }
}finally{fs.rmSync(temp,{recursive:true,force:true})}
const output={
 status:'PASS',scope:'archived /386 accepted-byte language only',
 node:process.version,source_git_blob:hash,
 accepted_packet_bytes:raw.length,exponent_zero_positions:zeros,
 parsed_paid_work:32,parsed_records:50,
 original_OS_checker_replay:native,
 original_packet_invalid_byte_samples:sample.size,
 original_packet_sampled_invalid_mutations_rejected:sample.size,
 synthetic_exhaustive_cases:synthetic,
 deterministic_exact_byte_query_lower_bound:zeros,
 randomized_error_one_third_expected_byte_query_lower_bound:zeros/3,
 note:'Lower bounds count byte probes to verify raw JSON. Not SAT decision time, CPU cost, physical peak RAM or logical proof work.'
};
const dest=process.argv[2];if(dest)fs.writeFileSync(dest,JSON.stringify(output,null,2)+'\n');
console.log(JSON.stringify(output,null,2));
