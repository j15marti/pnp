#!/usr/bin/env node
'use strict';
// LSPV-3/588: unchanged archived /341 checker in Node VM; no new proof grammar.
// Regenerate: node experiments/arc/lspv3_588_bridged_witness_subset_native341.cjs
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const cpath=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const fpath=path.join(root,'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json');
const blob=b=>crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
function pin(p,h){let b=fs.readFileSync(p);assert.equal(blob(b),h,p);return b;}
const checker=pin(cpath,'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0').toString();
const original=JSON.parse(pin(fpath,'fe27fe1011d0021e721ccaeb747ed58da65d7464'));
const clone=x=>JSON.parse(JSON.stringify(x));
const base=clone(original);
assert.equal(base.fixtures[0].graph.name,'K4');
assert.equal(base.fixtures[6].graph.name,'BRIDGE_K4x2');
base.fixtures=[original.fixtures[0],original.fixtures[6]];
base.summary=[original.summary[0],original.summary[6]];
const bridge=base.fixtures[1],n=bridge.clauses.length,E=bridge.graph.edges.length;
assert.equal(n,40);assert.equal(E,15);assert.equal(bridge.proof.length,39);
const srcHash=sha(Buffer.from(JSON.stringify({
 graph:bridge.graph,charges:bridge.charges,clauses:bridge.clauses,
 proof:bridge.proof,evenWitness:bridge.evenWitness
})));
const essential=Array(n).fill(false);
let sat=0;
for(let m=0;m<(1<<E);m++){
 let bad=0,last=-1;
 for(let j=0;j<n;j++){
  const holds=bridge.clauses[j].literals.some(l=>{
   const bit=(m>>(Math.abs(l)-1))&1;return l>0?bit===1:bit===0;
  });
  if(!holds){bad++;last=j;}
 }
 if(bad===0)sat++;
 if(bad===1)essential[last]=true;
}
const ids=essential.flatMap((v,i)=>v?[i]:[]);
assert.equal(sat,0);assert.equal(ids.length,36);
assert.deepEqual(essential.flatMap((v,i)=>v?[]:[i]),[18,19,36,37]);
assert(essential.every((v,i)=>v===(bridge.deleted[i].assignment!==null)));
function variant(indices){
 const p=clone(base),f=p.fixtures[1],set=new Set(indices);
 assert(indices.every(i=>essential[i]));
 for(let i=0;i<n;i++)if(!set.has(i))f.deleted[i].assignment=null;
 f.properties.essential=set.size;
 assert.equal(sha(Buffer.from(JSON.stringify({
  graph:f.graph,charges:f.charges,clauses:f.clauses,
  proof:f.proof,evenWitness:f.evenWitness
 }))),srcHash,'changed signed source or proof');
 return p;
}
const checks=[];
function replay(label,p,expect){
 const bytes=Buffer.from(JSON.stringify(p)+'\n'),output=[];
 let result=null,error=null;
 try{
  vm.runInNewContext(checker,{
   require:x=>{if(x==='fs')return {readFileSync:()=>bytes.toString()};throw Error('unexpected module '+x)},
   process:{argv:['node',cpath,'packet.json']},console:{log:x=>output.push(String(x))}
  },{filename:cpath,timeout:15000});
  result=JSON.parse(output.at(-1));
 }catch(e){error=String(e)}
 assert.equal(Boolean(result),expect,label+': '+error);
 if(result){assert.equal(result.cases[0].essential,16);assert.equal(result.cases[1].proofNodes,39)}
 checks.push({label,accepted:!!result,expected:expect,bytes:bytes.length,sha256:sha(bytes),
  assertions:result?.checks??null,claimedEssential:result?.cases?.[1]?.essential??null,error});
 return bytes;
}
replay('baseline_K4_bridge',base,true);
let zero;
for(const k of [0,1,2,4,8,16,24,35,36]){
 const b=replay('bridge_subset_'+k,variant(ids.slice(0,k)),true);
 if(k===0)zero=b;
}
replay('bridge_nonprefix_5',variant([0,5,16,28,39]),true);
let d=variant([]);d.fixtures[1].properties.essential=36;replay('bad_count',d,false);
d=variant([]);d.fixtures[0].properties.essential=0;replay('bad_bridgeless_count',d,false);
d=variant([]);d.fixtures[1].proof.at(-1).row.rhs=0;replay('bad_sink',d,false);
d=variant([]);d.fixtures[1].clauses[0].literals[0]=999;replay('bad_source',d,false);
d=variant([]);d.fixtures[1].deleted[0].sourceId='forged';replay('bad_source_id',d,false);
d=variant([]);d.fixtures[1].deleted[18].assignment='0'.repeat(15);
d.fixtures[1].properties.essential=1;replay('bad_extra_witness',d,false);
const positive=checks.filter(x=>x.accepted),negative=checks.filter(x=>!x.accepted);
assert.equal(positive.length,11);assert.equal(negative.length,6);
const raw={
 id:'LSPV-3/588',status:'PROVED/RESTRICTED original /341 code; COMPUTATIONAL unchanged original in Node VM',
 originalCheckerBlob:blob(fs.readFileSync(cpath)),originalFixtureBlob:blob(fs.readFileSync(fpath)),
 execution:'Original checker logic unchanged; VM file and stdout adapters. No OS subprocess claimed.',
 exhaustiveAssignments:1<<E,sourceSATModels:sat,trueEssentialCount:ids.length,
 nonEssentialSourceIndices:[18,19,36,37],
 unchangedSourceProofSHA256:srcHash,positive:positive.length,negative:negative.length,
 originalCheckerAssertionGroups:positive.reduce((s,x)=>s+x.assertions,0),
 proofNodes:bridge.proof.length,originalSourceClauses:bridge.clauses.length,
 conclusion:'All subsets of 36 true positive deletion witnesses remain accepted if the report count is reduced; reported essential count is not independently exact for bridged fixture.',
 cases:checks
};
const rp=process.argv[2]||path.join(root,'results/raw/arc/2026-11-12_0524_LSPV3_588_BRIDGE_WITNESS_SUBSET_HOSTED_RAW.json');
const pp=process.argv[3]||path.join(root,'results/raw/arc/2026-11-12_0524_LSPV3_588_BRIDGE_WITNESS_ZERO_ACCEPTED.json');
fs.mkdirSync(path.dirname(rp),{recursive:true});fs.mkdirSync(path.dirname(pp),{recursive:true});
fs.writeFileSync(rp,JSON.stringify(raw,null,2)+'\n');fs.writeFileSync(pp,zero);
console.log(JSON.stringify({raw:rp,packet:pp,positive:positive.length,negative:negative.length,
 assertions:raw.originalCheckerAssertionGroups,packetSHA256:sha(zero)}));
