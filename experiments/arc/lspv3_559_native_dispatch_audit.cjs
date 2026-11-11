#!/usr/bin/env node
'use strict';
/* LSPV-3/559. Run from j15marti/pnp repository root:
 * node experiments/arc/lspv3_559_native_dispatch_audit.cjs [output.json]
 * Replays exact original /341 producer and specialized checker from disk.
 * Their source bodies are NOT modified; only file I/O is adapted in vm.
 * DOES NOT authenticate the full historical R_mix341 grammar.
 */
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const assert=require('node:assert/strict');
const root=process.cwd();
const producerPath=path.join(root,'experiments/arc/lspv2_341_mixed_tseitin_min_dag.js');
const checkerPath=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const producer=fs.readFileSync(producerPath,'utf8');
const checker=fs.readFileSync(checkerPath,'utf8');
assert.match(checker,/if\(p\.rule==="AND3"\)/);
assert.match(checker,/else if\(p\.rule==="XOR"\)/);
assert.match(checker,/else throw Error\("unknown rule"\)/);
function originalProducer(){
 const output=[];
 vm.runInNewContext(producer,{console:{log:s=>output.push(s)}},{filename:producerPath});
 assert.equal(output.length,1);
 return JSON.parse(output[0]);
}
function originalChecker(packet){
 const output=[];
 try {
  vm.runInNewContext(checker,{
   require:name=>{if(name==='fs')return {readFileSync:()=>JSON.stringify(packet)};
     throw Error('forbidden require: '+name);},
   process:{argv:['node',checkerPath,'memory.json']},
   console:{log:s=>output.push(s)}
  },{filename:checkerPath});
  assert.equal(output.length,1);
  return {accepted:true,checks:JSON.parse(output[0]).checks};
 } catch(e){return {accepted:false,error:String(e.message)};}
}
const data=originalProducer(),deepcopy=x=>JSON.parse(JSON.stringify(x));
const codes=['RES','DEF','LOCAL-CONVERT','SPLIT_AND','AND3','XOR'];
const baseline=originalChecker(data);
assert.equal(baseline.accepted,true);
const rows=[];
for(let i=0;i<data.fixtures.length;i++){
 const f=data.fixtures[i];
 const row={graph:f.graph.name,V:f.graph.n,paid:f.proof.length,mutations:[]};
 for(const place of ['first_AND3','last_XOR']){
  const index=place==='first_AND3'?0:f.proof.length-1;
  for(const opcode of codes){
   const packet=deepcopy(data);
   packet.fixtures[i].proof[index].rule=opcode;
   const result=originalChecker(packet);
   const expected=(place==='first_AND3'&&opcode==='AND3')||
                  (place==='last_XOR'&&opcode==='XOR');
   assert.equal(result.accepted,expected,f.graph.name+' '+place+' '+opcode);
   if(['RES','DEF','LOCAL-CONVERT','SPLIT_AND'].includes(opcode))
     assert.equal(result.error,'unknown rule');
   row.mutations.push({placement:place,opcode,...result});
  }
 }
 rows.push(row);
}
const all=rows.flatMap(row=>row.mutations);
const raw={run:'LSPV-3/559',historical_model:'recovered /341 fixture only',
 original_body_unchanged:true,baseline_assertions:baseline.checks,
 graphs:rows.length,probes:all.length,
 accepted:all.filter(x=>x.accepted).length,
 unknown_rule_rejections:all.filter(x=>x.error==='unknown rule').length,
 wrong_type_rejections:all.filter(x=>x.error&&x.error!=='unknown rule').length,
 theorem:'The pinned verifier only recognizes AND3 or XOR, with an exhaustive throw for any other paid opcode.',
 open:['P2-D1','P2-C3','P2-B1','P2-B2'],results:rows};
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(raw,null,2)+'\n');
console.log(JSON.stringify({graphs:raw.graphs,probes:raw.probes,
 accepted:raw.accepted,unknown:raw.unknown_rule_rejections,
 type:raw.wrong_type_rejections,baseline_assertions:raw.baseline_assertions}));
