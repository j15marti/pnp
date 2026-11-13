#!/usr/bin/env node
'use strict';
// LSPV-3/600 independent OS reproduction driver. Requires Node >=18.
// Runs exact archived checker source in Node V8 vm with only I/O adapters,
// no rewrite of the historical mathematical verifier.
// Usage: node experiments/arc/lspv3_600_native341_edge_suffix.cjs [raw-output.json]
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checkerFile=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const packetFile=path.join(root,'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json');
function gitBlob(b){return crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\\0')).update(b).digest('hex')}
const checkerBytes=fs.readFileSync(checkerFile),packetBytes=fs.readFileSync(packetFile);
assert.equal(gitBlob(checkerBytes),'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0','wrong archived checker');
assert.equal(gitBlob(packetBytes),'fe27fe1011d0021e721ccaeb747ed58da65d7464','wrong original fixture');
const source=checkerBytes.toString('utf8'),original=JSON.parse(packetBytes.toString('utf8'));
const cp=x=>JSON.parse(JSON.stringify(x));
function native(p){
  const serialized=JSON.stringify(p),stdout=[];
  const fakeFs={readFileSync:()=>serialized};
  const scope={require:n=>{if(n==='fs')return fakeFs;throw Error('unexpected require: '+n)},
    process:{argv:['node','archived341','inmemory.json']},console:{log:s=>stdout.push(s)}};
  vm.runInNewContext(source,scope,{filename:'unchanged_lspv2_341_independent_verify.js',timeout:20000});
  assert.equal(stdout.length,1,'unexpected original output');
  return JSON.parse(stdout[0]);
}
const trials=[];
function checkCase(name,fn,expected){
  const p=cp(original);fn(p);
  let accepted=false,out=null,error=null;
  try{out=native(p);accepted=true}catch(e){error=String(e)}
  assert.equal(accepted,expected,'unexpected native verdict: '+name+' '+error);
  trials.push({name,accepted,expected,checks:out?.checks??null,
    original_builtin_negative_controls:out?.corruptions??null,
    total_paid_nodes_seven:out?.cases?.reduce((s,x)=>s+x.proofNodes,0)??null,
    bytes:Buffer.byteLength(JSON.stringify(p),'utf8'),error});
  return p;
}
checkCase('baseline_7_fixtures',()=>{},true);
for(let v=0;v<32;v++)checkCase('K4_first_edge_binary_suffix_'+String(v).padStart(2,'0'),p=>{
  p.fixtures[0].graph.edges[0].push(...Array.from({length:5},(_,i)=>(v>>i)&1));
},true);
checkCase('all_7_fixtures_every_edge_heterogeneous',p=>{
  for(let i=0;i<p.fixtures.length;i++)for(let j=0;j<p.fixtures[i].graph.edges.length;j++)
    p.fixtures[i].graph.edges[j].push(null,{source_hash:'UNTRUSTED_NOT_BINDING',edge_index:j,
      mix:[false,1,{x:'z'}]});
},true);
checkCase('K4_edge_128_member_suffix',p=>{
  p.fixtures[0].graph.edges[0].push(...Array.from({length:128},(_,i)=>i%2));
},true);
const negatives=[
  ['invalid_same_endpoints',p=>p.fixtures[0].graph.edges[0][1]=p.fixtures[0].graph.edges[0][0]],
  ['invalid_noninteger_endpoint',p=>p.fixtures[0].graph.edges[0][0]=0.5],
  ['missing_second_endpoint',p=>p.fixtures[0].graph.edges[0]=[p.fixtures[0].graph.edges[0][0]]],
  ['duplicate_edge_pair',p=>p.fixtures[0].graph.edges[0]=[...p.fixtures[0].graph.edges[1]]],
  ['forged_original_literal',p=>p.fixtures[0].clauses[0].literals[0]=999],
  ['nonexistent_parent_reference',p=>p.fixtures[0].proof[0].parents[0]='FAKE'],
  ['invalid_affine_terminal_rhs',p=>p.fixtures[0].proof.at(-1).row.rhs^=1]
];
for(const [name,change]of negatives)checkCase(name,change,false);
const specimen=cp(original);specimen.fixtures=[cp(original.fixtures[0])];
specimen.summary=Array.isArray(original.summary)?[cp(original.summary[0])]:[{}];
specimen.fixtures[0].graph.edges[0].push({
  UNTRUSTED_source_hash:'not bound by verifier',nested:[null,{X:7}]
});
const single=native(specimen);
assert.equal(single.cases.length,1);assert.equal(single.cases[0].proofNodes,15);
const result={run:'LSPV-3/600',checker_git_blob:gitBlob(checkerBytes),
  input_git_blob:gitBlob(packetBytes),mode:'original mathematical body in Node V8 vm, I/O adapters only',
  positives:trials.filter(t=>t.accepted).length,negatives:trials.filter(t=>!t.accepted).length,
  positive_assertions:trials.reduce((s,t)=>s+(t.checks||0),0),
  K4_specimen_checks:single.checks,trials};
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+'\\n');
console.log(JSON.stringify({status:'PASS',positives:result.positives,negatives:result.negatives,
  positive_assertions:result.positive_assertions,K4_specimen_checks:single.checks},null,2));
