#!/usr/bin/env node
'use strict';
// LSPV-1/590. Node 18+, standard library only. Run from repository root.
// Replays UNMODIFIED archived /386 checker as actual Node OS subprocesses.
// Distinct from absent authoritative full R_mix341 checker.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const cp=require('node:child_process'),vm=require('node:vm');
const crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=process.cwd();
const pinned={
 checker:['experiments/arc/lspv2_386_independent_verify.js','338305c0ce101704205e57543756b8127074a986'],
 dead:['results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json','318c52d99977ea4e91bc8554051138a700c1dc94'],
 live:['results/raw/arc/2026-11-11_0407_LSPV2_555_ACCEPTED_LIVE_DEF_RES_K1.json','aeeb555c4dcf7f510a9a501c8afc609b629a9298'],
 source:['results/raw/arc/2026-11-11_0812_LSPV2_559_EXTERNAL_K4_SIGNED_SOURCE.cnf','e8bc4300f1f4518cb447edaf3f699bcee4839803']
};
const sha256=b=>crypto.createHash('sha256').update(b).digest('hex');
function load(k){let [p,expected]=pinned[k],b=fs.readFileSync(path.join(root,p));
 let got=crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
 assert.equal(got,expected,'pinned Git blob '+k);return b;}
const checkerBytes=load('checker'),deadBytes=load('dead'),liveBytes=load('live'),sourceBytes=load('source');
const checker=checkerBytes.toString('utf8'),dead=JSON.parse(deadBytes),live=JSON.parse(liveBytes);
const clone=x=>JSON.parse(JSON.stringify(x));
function verifySource(P){
 const lines=sourceBytes.toString('utf8').trim().split(/\r?\n/);
 assert.equal(lines.shift().trim(),'p cnf 7 17');
 const external=lines.map(s=>{let v=s.trim().split(/\s+/).map(Number);assert.equal(v.pop(),0);return v});
 assert.deepEqual(P.records.filter(r=>r.kind==='SOURCE').map(r=>r.c),external);
}
function normalize(P){
 const Q=clone(P),n=Q.records.length,keep=new Set([n-1]),queue=[n-1];
 while(queue.length){let i=queue.pop();for(let j of Q.records[i].parents){
   assert.ok(j>=0&&j<i);if(!keep.has(j)){keep.add(j);queue.push(j)} }}
 Q.records.forEach((r,i)=>{if(r.kind==='SOURCE')keep.add(i)});
 let byId=new Map(Q.gate_defs.map(d=>[d[0],d])),byOutput=new Map(Q.gate_defs.map(d=>[d[1],d]));
 let necessary=new Set();
 function owner(d){assert.ok(d);if(necessary.has(d[0]))return;necessary.add(d[0]);
   for(let x of [d[2],d[3]]){let p=byOutput.get(Math.abs(x));if(p)owner(p)}}
 for(let i of keep){let r=Q.records[i];if(r.kind==='DEF')owner(byId.get(r.gate));
   for(let x of r.c){let d=byOutput.get(Math.abs(x));if(d)owner(d)}}
 let essential=necessary.size;
 if(!essential){assert.ok(Q.gate_defs.length>0);necessary.add(Q.gate_defs[0][0])}
 let indices=[...keep].sort((a,b)=>a-b),newId=new Map(indices.map((old,i)=>[old,i]));
 Q.records=indices.map(i=>{let r=clone(P.records[i]);r.parents=r.parents.map(j=>{assert.ok(newId.has(j));return newId.get(j)});return r});
 Q.gate_defs=Q.gate_defs.filter(d=>necessary.has(d[0]));
 let S=Q.summary;
 S.source=Q.records.filter(r=>r.kind==='SOURCE').length;
 S.def_views=Q.records.filter(r=>r.kind==='DEF').length;
 S.resolution=Q.records.filter(r=>r.kind==='RES').length;
 S.paid_gates=Q.gate_defs.length;S.paid_total=S.resolution+S.paid_gates;S.live_records=Q.records.length;
 assert.ok(Q.gate_defs.length>0&&S.paid_total<=P.summary.paid_total);
 return {packet:Q,essential,sentinel:essential===0};
}
const sandbox={require,process:{argv:['node','checker']},console:{log(){}},structuredClone};
vm.runInNewContext(checker+'\nthis.__nativeCore=checkProof;',sandbox,{timeout:3000});
function originalCore(P){try{sandbox.__nativeCore(clone(P),{control:true});return {accepted:true}}
 catch(e){return {accepted:false,error:String(e.message)}}}
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-lspv1-590-'));
function originalCLI(P){let b=Buffer.from(JSON.stringify(P)+'\n'),p=path.join(temp,'case.json');fs.writeFileSync(p,b);
 let r=cp.spawnSync(process.execPath,[path.join(root,pinned.checker[0]),p],
  {encoding:'utf8',timeout:20000,maxBuffer:1024*1024});assert.ifError(r.error);
 let accepted=r.status===0,detail=accepted?JSON.parse(r.stdout.trim()):null;
 if(accepted)assert.equal(detail.negativeTests,11);
 return {accepted,exit:r.status,error:accepted?null:r.stderr.trim().slice(0,250),
  bytes:b.length,sha256:sha256(b),detail}}
let cases=[];
function test(label,P,cli,core){let A=originalCore(P),B=originalCLI(P);
 assert.equal(A.accepted,core,label+' mathematical core');
 assert.equal(B.accepted,cli,label+' full CLI');
 cases.push({label,paid:P.summary.paid_total,records:P.records.length,owners:P.gate_defs.length,
  core:A,CLI:B});}
try{
 verifySource(dead);verifySource(live);
 const d=normalize(dead),l=normalize(live);
 assert.equal(d.essential,0);assert.equal(d.packet.summary.paid_total,29);
 assert.equal(l.essential,1);assert.equal(l.packet.summary.paid_total,31);
 let zero=clone(d.packet);zero.gate_defs=[];zero.summary.paid_gates=0;zero.summary.paid_total=28;
 test('baseline_dead_owner_W29',dead,true,true);
 test('unqualified_560_prune_zero_owner_W28',zero,false,true);
 test('corrected_sentinel_W29',d.packet,true,true);
 test('baseline_live_owner_W33',live,true,true);
 test('corrected_live_owner_W31',l.packet,true,true);
 for(let [label,a,b] of [['complementary',1,-1],['repeated',1,1],['different',2,5]]){
  let P=clone(d.packet);P.gate_defs[0]=[0,8,a,b];test('valid_root_'+label,P,true,true);}
 let wrong=clone(d.packet);wrong.gate_defs[0][1]=wrong.spec.guard;
 test('bad_sentinel_output_guard',wrong,false,false);
 wrong=clone(d.packet);wrong.records[0].c[0]*=-1;
 test('forged_signed_source',wrong,false,false);
 wrong=clone(d.packet);wrong.summary.paid_total--;
 test('underpaid',wrong,false,false);
 wrong=clone(d.packet);wrong.records.at(-1).parents[0]=wrong.records.length;
 test('future_parent',wrong,false,false);
 let output=process.argv[2]||'results/raw/arc/2026-11-12_0503_LSPV1_590_NATIVE386_OS_RAW.json';
 let result={run:'LSPV-1/590',date:'2026-11-12 05:03 PST',
 scope:'original pinned /386 full CLI, not unified historical R_mix341',
 pins:pinned,sourceSha256:sha256(sourceBytes),cases,
 exact_result:'naive removal of all dead owner gates fails full CLI; retain one root gate when needed',
 corrected_dead_work:29,naive_dead_work:28,corrected_live_work:31,
 open:['P2-D1','P2-C3','P2-B1','P2-B2','P2-B3','P versus NP'],
 execution:'real unchanged Node OS subprocess for every CLI case',
 note:'Logical work excludes evidence bytes, discovery, actual time, span and physical memory'};
 fs.mkdirSync(path.dirname(output),{recursive:true});fs.writeFileSync(output,JSON.stringify(result,null,2)+'\n');
 console.log(JSON.stringify({cases:cases.length,passed:cases.length,accepted:cases.filter(x=>x.CLI.accepted).length,
   rejected:cases.filter(x=>!x.CLI.accepted).length,output}));
}finally{fs.rmSync(temp,{recursive:true,force:true})}
