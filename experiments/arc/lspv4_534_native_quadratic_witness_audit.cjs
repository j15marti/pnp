#!/usr/bin/env node
'use strict';
// LSPV-4/534. Run from repository root:
// node experiments/arc/lspv4_534_native_quadratic_witness_audit.cjs
// Executes unchanged /341 producer/checker bodies with only Node I/O shims.
const fs=require('fs'),vm=require('vm'),assert=require('assert').strict,path=require('path');
const root=path.resolve(__dirname,'..','..');
const producerPath='experiments/arc/lspv2_341_mixed_tseitin_min_dag.js';
const checkerPath='experiments/arc/lspv2_341_independent_verify.js';
const producer=fs.readFileSync(path.join(root,producerPath),'utf8');
const checker=fs.readFileSync(path.join(root,checkerPath),'utf8');
const out=[];
vm.runInNewContext(producer,{console:{log:x=>out.push(x)}},{filename:producerPath,timeout:25000});
assert.equal(out.length,1);
const packet=JSON.parse(out[0]);
function verify(x){
  let lines=[];
  vm.runInNewContext(checker,{
    require:name=>{assert.equal(name,'fs');return {readFileSync:()=>JSON.stringify(x)};},
    process:{argv:['node',checkerPath,'fixture.json']},
    console:{log:y=>lines.push(y)}
  },{filename:checkerPath,timeout:25000});
  assert.equal(lines.length,1);
  return JSON.parse(lines[0]);
}
const baseline=verify(packet);
assert.equal(baseline.checks,30714);
const results=[];
for(const f of packet.fixtures){
 const V=f.graph.n,E=f.graph.edges.length,m=f.clauses.length,W=f.proof.length;
 const t=baseline.cases.find(x=>x.name===f.graph.name);
 const witnesses=f.deleted.filter(d=>d.assignment!==null);
 assert.equal(2*E,3*V);assert.equal(m,4*V);assert.equal(W,4*V-1);
 for(const d of witnesses){assert.equal(d.assignment.length,E);assert.match(d.assignment,/^[01]+$/);}
 assert.equal(f.evenWitness.length,E);assert.match(f.evenWitness,/^[01]+$/);
 const H=(witnesses.length+1)*E;
 if(t.bridgeless){assert.equal(witnesses.length,m);assert.equal(H,3*(W+1)*(W+2)/8);}
 results.push({name:f.graph.name,V,E,m,W,bridgeless:t.bridgeless,
    essential:witnesses.length,mandatory_binary_witness_bytes:H,
    serialized_fixture_bytes:Buffer.byteLength(JSON.stringify(f),'utf8')});
}
const tests=[];
function hostile(label,fn){
 const p=JSON.parse(JSON.stringify(packet));fn(p);
 let rejected=false,error='';
 try{verify(p);}catch(e){rejected=true;error=String(e.message).slice(0,150);}
 assert.ok(rejected,label);tests.push({label,rejected,error});
}
const mutate=(s,i)=>s.slice(0,i)+'2'+s.slice(i+1);
for(const k of [0,1,5,10,15])hostile('K4 deletion '+k,p=>{let s=p.fixtures[0].deleted[k].assignment;p.fixtures[0].deleted[k].assignment=mutate(s,0);});
for(const k of [0,2,5])hostile('K4 even witness '+k,p=>{let s=p.fixtures[0].evenWitness;p.fixtures[0].evenWitness=mutate(s,k);});
for(const k of [0,24,47])hostile('Prism16 deleted witness digit '+k,p=>{let s=p.fixtures[5].deleted[45].assignment;p.fixtures[5].deleted[45].assignment=mutate(s,k);});
hostile('short deletion',p=>{p.fixtures[0].deleted[0].assignment=p.fixtures[0].deleted[0].assignment.slice(1)});
hostile('null deletion',p=>{p.fixtures[0].deleted[0].assignment=null});
hostile('extra graph edge',p=>{p.fixtures[0].graph.edges.push([0,1])});
hostile('extra paid node',p=>{p.fixtures[0].proof.push({...p.fixtures[0].proof[0],id:'newNode'})});
hostile('missing paid node',p=>{p.fixtures[0].proof.pop()});
hostile('forged source literal',p=>{p.fixtures[0].clauses[0].literals[0]=0});
const ledger={report:'LSPV-4/534',execution:'native Node vm using unmodified historical JS mathematical bodies',
  original_producer:producerPath,original_checker:checkerPath,
  baseline_original_checker_assertions:baseline.checks,fixtures:results,
  hostile_rejected:tests.length,hostile_tests:tests,
  theorem:'For bridgeless accepted native fixture, H=(4V+1)E=3(W+1)(W+2)/8; E=3V/2, W=4V-1',
  limitations:'No historical full mixed RULE checker, external source binding, SAT lower bound, or measured peak writable memory.'};
const data=JSON.stringify(ledger,null,2)+'\n';
if(process.argv[2])fs.writeFileSync(process.argv[2],data);
process.stdout.write(data);
