'use strict';
// LSPV-3/611. Replays the archived /341 checker UNCHANGED as an OS Node process.
// Usage: node experiments/arc/lspv3_611_typed_json_id_namespace.cjs [--out FILE] [--packet FILE]
// This replayer is not an independent R_mix341 reimplementation.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const crypto=require('node:crypto'),cp=require('node:child_process'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const fixture=path.join(root,'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json');
const pinned={checker:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',fixture:'fe27fe1011d0021e721ccaeb747ed58da65d7464'};
function blobSha(b){const h=Buffer.from('blob '+b.length+'\0');return crypto.createHash('sha1').update(h).update(b).digest('hex')}
assert.equal(blobSha(fs.readFileSync(checker)),pinned.checker,'archived checker blob mismatch');
assert.equal(blobSha(fs.readFileSync(fixture)),pinned.fixture,'historical input blob mismatch');
const seed=JSON.parse(fs.readFileSync(fixture,'utf8'));
const ids=[...seed.fixtures[0].clauses.map(x=>x.id),...seed.fixtures[0].proof.map(x=>x.id)];
function base(){return{version:seed.version,definition:seed.definition,fixtures:[structuredClone(seed.fixtures[0])],summary:[structuredClone(seed.summary[0])]}}
function rename(f,oldid,newid){
 for(const c of f.clauses)if(c.id===oldid)c.id=newid;
 for(const d of f.deleted)if(d.sourceId===oldid)d.sourceId=newid;
 for(const p of f.proof){if(p.id===oldid)p.id=newid;p.parents=p.parents.map(id=>id===oldid?newid:id)}
}
function packet(pairs){const p=base();for(const [a,b] of pairs)rename(p.fixtures[0],a,b);return p}
const ten=[['s0',0],['s1','0'],['s2',false],['s3','false'],['s4',null],['s5','null'],['d0',1],['d1','1'],['d2',true],['d3','true']];
const positive=[
 ['baseline',[]],
 ['source_number_vs_text',[['s0',0],['s1','0']]],
 ['paid_number_vs_text',[['d0',1],['d1','1']]],
 ['source_boolean_vs_number',[['s0',false],['s1',0]]],
 ['source_null_vs_text',[['s0',null],['s1','null']]],
 ['paid_boolean_vs_text',[['d0',true],['d1','true']]],
 ['eight_mixed',ten.slice(0,8)],
 ['ten_mixed',ten],
 ['all_safe_numbers',ids.map((id,i)=>[id,1000+i])],
 ['all_numeric_strings',ids.map((id,i)=>[id,String(1000+i)])],
 ['all_alternating_types',ids.map((id,i)=>[id,i%2===0?1000+i:String(1000+i)])],
 ['source_zero_vs_false',[['s0',0],['s1',false]]],
 ['paid_zero_vs_false',[['d0',0],['d1',false]]]
];
const hostile=[
 ['source_number_collision',p=>{p.fixtures[0].clauses.find(c=>c.id==='0').id=0}],
 ['paid_number_collision',p=>{p.fixtures[0].proof.find(r=>r.id==='1').id=1}],
 ['source_bool_coalesces_number',p=>{p.fixtures[0].clauses.find(c=>c.id===false).id=0}],
 ['wrong_parent_namespace',p=>{p.fixtures[0].proof.find(r=>r.id===1).parents[0]='0'}],
 ['wrong_deletion_namespace',p=>{p.fixtures[0].deleted.find(d=>d.sourceId===0).sourceId='0'}],
 ['unreachable_object_id',p=>{p.fixtures[0].clauses.find(c=>c.id===0).id={id:0}}],
 ['bad_paid_parent_reference',p=>{p.fixtures[0].proof.find(r=>r.id==='1').parents[0]='1'}],
 ['stringify_every_id',p=>{
   const f=p.fixtures[0];for(const c of f.clauses)c.id=String(c.id);
   for(const d of f.deleted)d.sourceId=String(d.sourceId);
   for(const r of f.proof){r.id=String(r.id);r.parents=r.parents.map(String)}
 }]
];
function runOriginal(p){
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-lspv3-611-'));const file=path.join(dir,'packet.json');
 try{
   fs.writeFileSync(file,JSON.stringify(p));
   const r=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',maxBuffer:5*1024*1024});
   if(r.status===0){const j=JSON.parse(r.stdout);return{accepted:true,checks:j.checks,paid:j.cases[0].proofNodes,essential:j.cases[0].essential}}
   const line=String(r.stderr||r.stdout).split('\n').find(s=>s.includes('Verifier:'))||String(r.stderr).split('\n')[0];
   return{accepted:false,error:line.trim().slice(0,240),exit_code:r.status};
 }finally{fs.rmSync(dir,{recursive:true,force:true})}
}
const positives=positive.map(([name,mapping])=>({name,...runOriginal(packet(mapping))}));
const baseHostile=packet(ten);
const negatives=hostile.map(([name,mutate])=>{let p=structuredClone(baseHostile);mutate(p);return{name,...runOriginal(p)}});
assert(positives.every(x=>x.accepted&&x.checks===1401&&x.paid===15&&x.essential===16),'positive verdict differs');
assert(negatives.every(x=>!x.accepted),'hostile mutation erroneously accepted');
const result={schema:'LSPV3-611-TYPED-JSON-ID-ALIAS/v1',status:'PROVED/RESTRICTED + COMPUTATIONAL',
 scope:'unchanged original /341 checker; NOT the full historical R_mix341',pinned,
 positive_count:positives.length,rejection_count:negatives.length,positive_assertion_groups:positives.reduce((n,x)=>n+x.checks,0),
 positives,negatives,logical_paid_work_each_accepted:15,source_clauses_each_accepted:16,
 actual_machine_time:null,span:null,peak_space:null};
const out=process.argv.indexOf('--out'),pk=process.argv.indexOf('--packet');
if(out>=0){if(!process.argv[out+1])throw Error('missing --out path');fs.writeFileSync(process.argv[out+1],JSON.stringify(result,null,2)+'\n')}
if(pk>=0){if(!process.argv[pk+1])throw Error('missing --packet path');fs.writeFileSync(process.argv[pk+1],JSON.stringify(packet(ten),null,2)+'\n')}
console.log(JSON.stringify(result,null,2));
