#!/usr/bin/env node
'use strict';
/* LSPV-2/583: restricted archived /386 native rule-dispatch packet matrix.
   This is an original-checker OS DRIVER, NOT an authoritative parser or a
   reconstructed historical R_mix341 checker. Requires the four pinned files
   supplied by repository or companion evidence archive. */
const fs = require('fs'), os=require('os'), path=require('path');
const crypto=require('crypto'), cp=require('child_process'),assert=require('assert');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const source=path.join(root,'results/raw/arc/2026-11-12_1412_LSPV2_583_SIGNED_K4_SOURCE.cnf');
const w29=path.join(root,'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json');
const w31=path.join(root,'results/raw/arc/580_DEF_THEN_RES_W31.json');
const out=process.argv[2]||path.join(root,'results/raw/arc/2026-11-12_1412_LSPV2_583_NATIVE_RULE_MATRIX_RAW.json');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
function read(p,want){let b=fs.readFileSync(p);assert.strictEqual(sha(b),want,`pinned bytes ${p}`);return b;}
const ck=read(checker,'22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113');
const src=read(source,'3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c');
const seed=JSON.parse(read(w29,'0d8b1894f91d00c554727a92fed35b2bb58f2b1602f2a3cfcb949effda43ceb0'));
const live=JSON.parse(fs.readFileSync(w31));
const rawsrc=src.toString('utf8').trim().split(/\s+/).map(Number);
assert.deepStrictEqual(rawsrc.slice(0,4),[NaN,NaN,7,17]);
let rawClauses=[],one=[];for(const n of rawsrc.slice(4)){if(n===0){rawClauses.push(one);one=[]}else one.push(n)}
assert.strictEqual(rawClauses.length,17);assert.deepStrictEqual(one,[]);
const norm = a => [...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
const expected=[];const {edges,charge,guard,h}=seed.spec;
for(let v=0;v<h;v++){
  let inc=[];edges.forEach(([a,b],i)=>{if(a===v||b===v)inc.push(i+1)});
  for(let t=0;t<8;t++){
    let bits=[t&1,(t>>1)&1,(t>>2)&1];
    if((bits[0]^bits[1]^bits[2])!==charge[v]) expected.push(norm(inc.map((e,i)=>bits[i]?-e:e).concat([-guard])));
  }
}
expected.push([guard]);
const sorted = rows => rows.map(a=>JSON.stringify(a)).sort();
assert.deepStrictEqual(sorted(expected),sorted(rawClauses),'external signed SOURCE does not match in-band spec');
for(let d of [seed,live]){
 assert.strictEqual(d.summary.source,17);assert.strictEqual(d.summary.paid_total,d.summary.resolution+d.summary.paid_gates);
 assert.deepStrictEqual(sorted(d.records.filter(r=>r.kind==='SOURCE').map(r=>r.c)),sorted(rawClauses));
}
const keys=['SOURCE','DEF','RES','AND3','XOR','GF(2)','GF2','LOCAL-CONVERT',
 'LOCAL_CONVERT','PAID-DEF','BRANCH','SPLIT','ASSUME','WEAKEN','DISCHARGE',
 'JOIN','DELETE','COPY','RESOLUTION','AND2'];
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2_583_'));
const cases=[];let totalAssertions=0;
function run(name,obj,expect){
 let bytes=Buffer.from(JSON.stringify(obj)+'\n','utf8');let filename=path.join(temp,`case${cases.length}.json`);
 fs.writeFileSync(filename,bytes);
 const r=cp.spawnSync(process.execPath,[checker,filename],{encoding:'utf8',maxBuffer:2e6});
 const accepted=r.status===0;const first=(r.stderr||'').split('\n').find(x=>x.includes('Error:'))||'';
 let assertions=null,originalNegatives=null;
 if(accepted){let parsed=JSON.parse(r.stdout.trim());assertions=parsed.assertions;originalNegatives=parsed.negativeTests;totalAssertions+=assertions}
 assert.strictEqual(accepted,expect,`unexpected native checker result: ${name}: ${first}`);
 cases.push({name,verdict:accepted?'ACCEPT':'REJECT',sha256:sha(bytes),bytes:bytes.length,
  rule_error:first.slice(0,200),assertions,original_negative_tests:originalNegatives,
  paid:obj.summary.paid_total,records:obj.records.length});
 fs.unlinkSync(filename);
}
run('baseline_W29_NATIVE_RES',structuredClone(seed),true);
run('baseline_W31_NATIVE_DEF_RES',structuredClone(live),true);
const slots=[{name:'source',base:seed,index:0,accepted:'SOURCE'},
 {name:'facet',base:live,index:17,accepted:'DEF'},
 {name:'terminal',base:live,index:live.records.length-1,accepted:'RES'}];
for(const slot of slots){
 for(const tag of keys){
  const d=structuredClone(slot.base);d.records[slot.index].kind=tag;
  run(`${slot.name}_${tag}`,d,tag===slot.accepted);
 }
}
for(const [name,mutate] of [
 ['bad_source_literal',d=>{d.records[0].c=[-d.spec.guard]}],
 ['bad_RES_signed_pivot',d=>{d.records.at(-1).pivot=123}],
 ['bad_DEF_owner',d=>{d.records.find(r=>r.kind==='DEF').gate=777}],
 ['bad_DEF_view',d=>{d.records.find(r=>r.kind==='DEF').c=[99999]}],
 ['bad_paid_total',d=>{d.summary.paid_total--}],
 ['bad_parent_future',d=>{d.records.at(-1).parents[0]=d.records.length}],
 ['bad_source_spec',d=>{d.spec.charge[0]^=1}],
 ['bad_fresh_wire',d=>{d.gate_defs[0][1]=1}]
]){const d=structuredClone(live);mutate(d);run(name,d,false)}
let metadata=structuredClone(live);metadata.records.at(-1).annotations={
  'LOCAL-CONVERT':'untrusted user annotation','GF(2)':'untrusted',
  'context':'not checked','discharge':'not checked'};
run('ignored_final_annotations_NATIVE_RES',metadata,true);
fs.rmSync(temp,{recursive:true,force:true});
const manifest={schema:'LSPV2-583-ORIGINAL386-NATIVE-OS-MATRIX/v1',
 status:'COMPUTATIONAL, original checker restricted /386 ONLY; full historical R_mix341 OPEN',
 checker_sha256:sha(ck),external_signed_source_sha256:sha(src),
 original_seed_sha256:sha(fs.readFileSync(w29)),
 positive_live_seed_sha256:sha(fs.readFileSync(w31)),
 node:process.version,source_clauses:17,rule_candidate_tags:keys,
 note:'Original CLI parses JSON via Node and tests 11 internal corruptions for accepted cases. A rejected mutation to an unknown kind demonstrates only absence in this archived checker.',
 totals:{cases:cases.length,positive:cases.filter(x=>x.verdict==='ACCEPT').length,
 negative:cases.filter(x=>x.verdict==='REJECT').length,accepted_assertions:totalAssertions},cases};
fs.mkdirSync(path.dirname(out),{recursive:true});fs.writeFileSync(out,JSON.stringify(manifest,null,2)+'\n');
console.log(JSON.stringify({status:'PASS',manifest:out,...manifest.totals,checker_sha256:manifest.checker_sha256}));
