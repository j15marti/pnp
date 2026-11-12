#!/usr/bin/env node
'use strict';
/*
LSPV-2/573: original /386 owner-bank discriminability.
This is a differential harness and non-authoritative abstraction projector.
It is NOT a historical full R_mix341 parser/checker.
Run: node experiments/arc/lspv2_573_native386_owner_facet_cegar.cjs
*/
const fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process');
const crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checker='experiments/arc/lspv2_386_independent_verify.js';
const seedPath='results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json';
const sourcePath='results/raw/arc/2026-11-11_0812_LSPV2_559_EXTERNAL_K4_SIGNED_SOURCE.cnf';
const sha=s=>crypto.createHash('sha256').update(s).digest('hex');
function pin(file,expected){
 const b=fs.readFileSync(path.join(root,file));
 const git=crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');
 assert.equal(git,expected,'input Git blob drift: '+file);
 return b;
}
pin(checker,'338305c0ce101704205e57543756b8127074a986');
const input=pin(seedPath,'318c52d99977ea4e91bc8554051138a700c1dc94');
const source=pin(sourcePath,'e8bc4300f1f4518cb447edaf3f699bcee4839803');
const seed=JSON.parse(input);
const sourceClauses=source.toString('utf8').trim().split(/\r?\n/).slice(1)
 .map(s=>s.trim().split(/\s+/).map(Number).slice(0,-1));
assert.deepEqual(sourceClauses,seed.records.filter(r=>r.kind==='SOURCE').map(r=>r.c),
 'externally bound signed SOURCE occurrences');
const clone=x=>structuredClone(x);
const dir=path.join(root,'results/raw/arc/573_cases');fs.mkdirSync(dir,{recursive:true});
function variant(a,b){const x=clone(seed);x.gate_defs[0]=[0,8,a,b];return x}
function facet(d,c,id=0){
 const q=clone(d);
 q.records=q.records.map(r=>({...r,parents:r.parents.map(p=>p+1)}));
 q.records.unshift({kind:'DEF',gate:id,c,parents:[]});
 q.summary.def_views++;q.summary.live_records++;return q;
}
function alpha(d){
 // Deliberately forget gate input operands. This is NOT an exact abstraction.
 return JSON.stringify({spec:d.spec,gateIdsOutputs:d.gate_defs.map(x=>x.slice(0,2)),
  clauses:d.records.map(x=>x.c),kinds:d.records.map(x=>x.kind),
  ports:d.records.map(x=>x.parents),summary:d.summary});
}
function run(label,d,expected){
 const bytes=Buffer.from(JSON.stringify(d));
 const file=path.join(dir,label+'.json');fs.writeFileSync(file,bytes);
 const p=cp.spawnSync(process.execPath,[path.join(root,checker),file],
  {encoding:'utf8',timeout:10000,maxBuffer:8*1024*1024});
 const accepted=p.status===0;
 assert.equal(accepted,expected,'native mismatch '+label+' '+p.stderr);
 return {label,accepted,expected,paid:d.summary.paid_total,
  nativeAssertions:accepted?JSON.parse(p.stdout.trim()).assertions:null,
  bytes:bytes.length,sha256:sha(bytes),
  error:accepted?null:(p.stderr.split('\n').find(x=>x.includes('Error:'))||p.stderr.slice(0,300))};
}
const A=variant(1,4),B=variant(2,5);
assert.equal(alpha(A),alpha(B),'expected coarse-state collision');
const cases=[
 ['base_A_owner_1_4',A,true],['base_B_owner_2_5',B,true],
 ['facet_1_A',facet(A,[1,-8]),true],['facet_1_B_wrong',facet(B,[1,-8]),false],
 ['facet_2_B',facet(B,[2,-8]),true],['facet_2_A_wrong',facet(A,[2,-8]),false],
 ['facet_foreign_owner_A',facet(A,[1,-8],1),false],
 ['facet_wrong_clause_A',facet(A,[3,-8]),false],
 ['facet_paid_undercharge_A',(()=>{let q=facet(A,[1,-8]);q.summary.paid_total--;return q})(),false],
 ['facet_forward_parent_A',(()=>{let q=facet(A,[1,-8]);q.records[0].parents=[1];return q})(),false],
];
const rows=cases.map(([label,d,e])=>run(label,d,e));
assert.equal(rows.filter(x=>x.accepted).length,4);
assert.equal(rows.filter(x=>!x.accepted).length,6);
const result={
 id:'LSPV-2/573',scope:'pinned original /386 only; full R_mix341 still OPEN',
 stateCollision:alpha(A)===alpha(B),sourceSHA256:sha(source),sourceSpecSHA256:sha(Buffer.from(JSON.stringify(seed.spec))),
 checkerSHA256:sha(fs.readFileSync(path.join(root,checker))),seedSHA256:sha(input),
 conclusion:'exact zero-cost DEF facet legal in A but illegal in B with same projected clause records, owner ID/output, paid work and external source',
 status:'PROVED/RESTRICTED plus COMPUTATIONAL',
 nodeVersion:process.version,positives:4,negatives:6,rows
};
const out='results/raw/arc/2026-11-12_0412_LSPV2_573_OWNER_FACET_DISCRIMINATION_OS_RAW.json';
fs.writeFileSync(path.join(root,out),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({out,positives:4,negatives:6,assertions:rows.reduce((t,x)=>t+(x.nativeAssertions||0),0),rows},null,2));
