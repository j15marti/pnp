#!/usr/bin/env node
'use strict';
// LSPV-1/621: original /386 zero-charge DEF duplication and raw-index future-language test.
// Usage: node experiments/arc/lspv1_621_native386_zero_cost_index_language.cjs [REPO_ROOT] [OUTPUT_JSON]
// Restricted SOURCE/DEF/RES checker, NOT the full historical R_mix341.
const fs=require('node:fs'),cp=require('node:child_process'),path=require('node:path');
const os=require('node:os'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(process.argv[2]||'.');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedPath=path.join(root,'results/raw/arc/2026-11-13_0612_LSPV2_599_W32_source-first_source-first.json');
const output=path.resolve(process.argv[3]||path.join(root,'results/raw/arc/2026-11-13_0804_LSPV1_621_ZERO_COST_INDEX_LANGUAGE_RAW.json'));
const sha256=x=>crypto.createHash('sha256').update(x).digest('hex');
const gitHash=x=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+x.length+'\0'),x])).digest('hex');
const checkerBytes=fs.readFileSync(checker),seedBytes=fs.readFileSync(seedPath);
assert.equal(sha256(checkerBytes),'22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113');
assert.equal(gitHash(seedBytes),'3a2f40d09b03089e8c86ce2ff2619ad83fbb8e5e');
const seed=JSON.parse(seedBytes),copy=x=>JSON.parse(JSON.stringify(x)),cut=47,facet=18;
assert.equal(seed.records[cut].kind,'RES');
assert.deepEqual(seed.records[cut].parents,[46,facet]);
assert.equal(seed.records[facet].kind,'DEF');
assert.equal(seed.summary.paid_total,32);
function build(n){
 assert(Number.isSafeInteger(n)&&n>=0);
 const d=copy(seed),pre=copy(seed.records.slice(0,cut)),repeated=Array.from({length:n},()=>copy(seed.records[facet]));
 const post=copy(seed.records.slice(cut));
 post.forEach((r,i)=>{r.parents=r.parents.map(j=>j>=cut?j+n:j);if(i===0&&n>0)r.parents[1]=cut+n-1;});
 d.records=[...pre,...repeated,...post];d.summary.def_views=2+n;d.summary.live_records=50+n;
 assert.equal(d.summary.paid_total,32);assert.equal(d.summary.resolution,31);
 assert.equal(d.records[cut+n].parents[1],n>0?cut+n-1:facet);
 return d;
}
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp621-')),cases=[];
function run(name,d,accept){
 const bytes=Buffer.from(JSON.stringify(d)+'\n'),file=path.join(tmp,name+'.json');fs.writeFileSync(file,bytes);
 const p=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',timeout:20000});
 assert.equal(p.status===0,accept,name+': expected '+accept+' got '+p.status+' stderr='+p.stderr);
 const obj=accept?JSON.parse(p.stdout):{};
 const entry={name,expected_accept:accept,actual_accept:p.status===0,sha256:sha256(bytes),bytes:bytes.length,
   paid_reported:accept?obj.paid:null,original_assertions:accept?obj.assertions:null,
   def_views:d.summary.def_views,records:d.records.length};
 cases.push(entry);return entry;
}
const ns=[0,1,2,3,5,8,16,32,64];
for(const n of ns){const d=build(n),x=run('accepted_n'+n,d,true);assert.equal(x.paid_reported,32);
 if(n===64){const file=output.replace('_RAW.json','_N64_ACCEPTED.json');fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,JSON.stringify(d)+'\n');}
}
let pairs=0;
for(let a=0;a<ns.length;a++)for(let b=a+1;b<ns.length;b++){
 const n=ns[a],m=ns[b],suffix=build(m).records.slice(cut+m),short=build(n);
 assert.equal(suffix[0].parents[1],cut+m-1);
 assert(cut+m-1>=cut+n);
 const d=copy(short);d.records=d.records.slice(0,cut+n).concat(copy(suffix));d.summary.live_records=d.records.length;
 if((n===0&&m===1)||(n===1&&m===2)||(n===3&&m===8)||(n===32&&m===64))
   run('cross_short'+n+'_long'+m,d,false);
 pairs++;
}
for(const [name,mutate] of [
 ['bad_clone_gate',d=>d.records[cut].gate=123],
 ['bad_clone_clause',d=>d.records[cut].c=[999999]],
 ['bad_payment',d=>d.summary.paid_total++],
 ['bad_kind_delete',d=>d.records[cut].kind='DELETE'],
 ['bad_fwd_parent',d=>d.records[cut+1].parents[1]=999999],
]){const d=build(2);mutate(d);run(name,d,false);}
const raw={id:'LSPV1-621',scope:'original /386 SOURCE/DEF/RES checker ONLY',status:'PROVED/RESTRICTED + COMPUTATIONAL',
 checker_sha256:sha256(checkerBytes),checker_git_blob:'338305c0ce101704205e57543756b8127074a986',
 seed_git_blob:gitHash(seedBytes),seed_sha256:sha256(seedBytes),positive:ns.length,
 negative:cases.filter(x=>!x.expected_accept).length,pairs,ns,paid:32,prefix_paid:29,cut,facet,cases};
fs.mkdirSync(path.dirname(output),{recursive:true});fs.writeFileSync(output,JSON.stringify(raw,null,2)+'\n');
fs.rmSync(tmp,{recursive:true,force:true});
console.log(JSON.stringify({id:raw.id,positive:raw.positive,negative:raw.negative,pairs,pass:true}));
