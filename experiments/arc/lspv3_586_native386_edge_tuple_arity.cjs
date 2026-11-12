#!/usr/bin/env node
'use strict';
/*
 LSPV-3/586 (2026-11-12 03:24 PST). Execute from j15marti/pnp root:
 node experiments/arc/lspv3_586_native386_edge_tuple_arity.cjs [output-directory]
 Replays the unchanged archived /386 checker as a real OS Node subprocess.
 Independent simulations are NOT used for any acceptance verdict.
 This reproducer was published but not OS-executed by its author during this run.
*/
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const crypto=require('node:crypto'),assert=require('node:assert/strict');
const cp=require('node:child_process');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedFile=path.join(root,'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json');
const outDir=process.argv[2]?path.resolve(process.argv[2]):path.join(root,'results/raw/arc');
const prefix='2026-11-12_0324_LSPV3_586';
function gitBlob(b){return crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex')}
function sha256(b){return crypto.createHash('sha256').update(b).digest('hex')}
const checkerBytes=fs.readFileSync(checker),seedBytes=fs.readFileSync(seedFile);
assert.equal(gitBlob(checkerBytes),'338305c0ce101704205e57543756b8127074a986','checker revision mismatch');
assert.equal(gitBlob(seedBytes),'318c52d99977ea4e91bc8554051138a700c1dc94','seed revision mismatch');
const seed=JSON.parse(seedBytes);
assert.equal(seed.summary.paid_total,29);assert.equal(seed.records.length,45);
const copy=x=>JSON.parse(JSON.stringify(x));
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-lspv3-586-'));
const cases=[];
function replay(label,mutate,expectAccept) {
 const p=copy(seed);mutate(p);
 const bytes=Buffer.from(JSON.stringify(p)+'\n','utf8');
 const input=path.join(tmp,'packet.json');fs.writeFileSync(input,bytes);
 const proc=cp.spawnSync(process.execPath,[checker,input],{cwd:root,encoding:'utf8',timeout:20000,maxBuffer:1<<20});
 const accepted=proc.status===0&&!proc.error;
 assert.equal(accepted,expectAccept,label+': unexpected verdict '+(proc.error||proc.stderr||''));
 const entry={label,accepted,bytes:bytes.length,sha256:sha256(bytes),exit_status:proc.status};
 if(accepted) {
   const lines=proc.stdout.trim().split(/\r?\n/);const result=JSON.parse(lines.at(-1));
   assert.equal(result.paid,29,label+' W29');assert.equal(result.sources,17,label+' original SOURCE count');
   assert.equal(result.records,45,label+' unchanged DAG');assert.equal(result.negativeTests,11,label+' internal hostile controls');
   entry.assertions=result.assertions;entry.builtin_negative_tests=result.negativeTests;
   entry.paid=result.paid;entry.sources=result.sources;entry.records=result.records;
 } else {
   entry.error=String(proc.error||proc.stderr).trim().split('\n')[0];
 }
 cases.push(entry);return {p,bytes};
}
try {
 replay('baseline',()=>{},true);
 for(let mask=0;mask<16;mask++){
   replay('4bit_shadow_'+mask,p=>p.spec.edges[0].push(...[0,1,2,3].map(b=>(mask>>b)&1)),true);
 }
 replay('third_null',p=>p.spec.edges[0].push(null),true);
 replay('third_string',p=>p.spec.edges[0].push('SOURCE'),true);
 const witness=replay('third_object',p=>p.spec.edges[0].push({shadow:{source:'not-original',payload:[0,1,null]}}),true);
 replay('all_edges_shadow',p=>p.spec.edges.forEach((e,i)=>e.push({ignored:i})),true);
 replay('wrong_edge_arity_one',p=>{p.spec.edges[0]=[0]},false);
 replay('wrong_edge_orientation',p=>{p.spec.edges[0]=[1,0]},false);
 replay('wrong_edge_endpoint_type',p=>{p.spec.edges[0]=[0,'1']},false);
 replay('wrong_owner_arity_five',p=>p.gate_defs[0].push(777),false);
 replay('wrong_RES_parents',p=>p.records.at(-1).parents.push(15),false);
 replay('forged_signed_SOURCE',p=>{p.records[0].c[0]=-1},false);
 replay('underpaid',p=>{p.summary.paid_total=28},false);
 replay('illegal_record_op',p=>{p.records[17].kind='LOCAL-CONVERT'},false);
 assert.equal(cases.filter(c=>c.accepted).length,21);
 assert.equal(cases.filter(c=>!c.accepted).length,8);
 assert.equal(cases.filter(c=>c.accepted).reduce((a,c)=>a+c.assertions,0),74382);
 fs.mkdirSync(outDir,{recursive:true});
 const result={
   id:'LSPV-3/586',scope:'original archived /386 unchanged checker OS Node subprocess; NOT full historical R_mix341',
   original_checker_git_blob:gitBlob(checkerBytes),seed_git_blob:gitBlob(seedBytes),
   positives:21,hostile_rejections:8,total_assertions:74382,
   native_sha256_computed:true,all_accepted_paid:29,
   cases
 };
 const rawPath=path.join(outDir,prefix+'_EDGE_SUFFIX_NATIVE386_OS_RAW.json');
 const packetPath=path.join(outDir,prefix+'_EDGE_SUFFIX_ACCEPTED_PACKET.json');
 fs.writeFileSync(rawPath,JSON.stringify(result,null,2)+'\n');
 fs.writeFileSync(packetPath,witness.bytes);
 console.log(JSON.stringify({positive:21,rejected:8,assertions:74382,raw:rawPath,packet:packetPath}));
} finally {fs.rmSync(tmp,{recursive:true,force:true})}
