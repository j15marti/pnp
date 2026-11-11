#!/usr/bin/env node
'use strict';
// LSPV-2/562 REFERENCE ONLY: original /386 core-to-CLI-safe value quotient.
// This code is NOT the historical checker and NOT a complete R_mix341 grammar.
// node experiments/arc/lspv2_562_native386_cli_safe_quotient.cjs [output-dir]
const fs=require('node:fs'), crypto=require('node:crypto'), cp=require('node:child_process');
const vm=require('node:vm'), os=require('node:os'), path=require('node:path');
const assert=require('node:assert/strict');
const checker='experiments/arc/lspv2_386_independent_verify.js';
const seedfile='results/raw/arc/2026-11-11_1012_LSPV2_561_ACCEPTED_LIVE_PAID_RES_FANOUT.json';
const originalCheckerBlob='338305c0ce101704205e57543756b8127074a986';
const originalSeedBlob='bf7cd9851e881fef47e617eb99f0c3b2e83bb0a0';
const copy=x=>JSON.parse(JSON.stringify(x));
const packetBytes=x=>Buffer.from(JSON.stringify(x)+'\n','utf8');
const hash=b=>crypto.createHash('sha256').update(b).digest('hex');
const gitblob=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
function pinned(file,expected){const b=fs.readFileSync(file);
 assert.equal(gitblob(b),expected,'historical blob mismatch: '+file);return b}
function tally(p){const count=kind=>p.records.filter(r=>r.kind===kind).length;
 p.summary={source:count('SOURCE'),def_views:count('DEF'),resolution:count('RES'),
 paid_gates:p.gate_defs.length,paid_total:count('RES')+p.gate_defs.length,
 live_records:p.records.length};return p}
function source(p){return JSON.stringify([p.spec,p.records.filter(r=>r.kind==='SOURCE')])}
function quotient(input){
 const p=copy(input),representatives=new Map(),index=new Map(),kept=[],removed=[];
 p.records.forEach((old,i)=>{
  const r=copy(old);r.parents=r.parents.map(j=>{assert.ok(index.has(j));return index.get(j)});
  const clause=JSON.stringify(r.c);
  if(r.kind==='RES'&&i!==input.records.length-1&&representatives.has(clause)){
   const rep=representatives.get(clause);
   index.set(i,rep.newIndex);removed.push({old:i,replaced_by:rep.oldIndex,kind:rep.kind});
   return;
  }
  const newIndex=kept.length;kept.push(r);index.set(i,newIndex);
  if(!representatives.has(clause))representatives.set(clause,{newIndex,oldIndex:i,kind:r.kind});
 });
 p.records=kept;return {packet:tally(p),removed};
}
function ancestry(p){
 const seen=new Set(),todo=[p.records.length-1];
 while(todo.length){const i=todo.pop();assert.ok(i>=0&&i<p.records.length);
  if(seen.has(i))continue;seen.add(i);todo.push(...p.records[i].parents)}
 return seen
}
function terminalCone(input){
 const needed=ancestry(input),old=[];
 input.records.forEach((r,i)=>{if(needed.has(i)||r.kind==='SOURCE')old.push(i)});
 const ren=new Map(old.map((i,j)=>[i,j])),p=copy(input);
 p.records=old.map(i=>{const r=copy(input.records[i]);
  r.parents=r.parents.map(j=>{assert.ok(ren.has(j));return ren.get(j)});return r});
 // Preserve every paid owner: the original CLI's own mutation needs >=1.
 // This is a checker wrapper property, not a logical proof-system axiom.
 return tally(p)
}
function runCore(p,checkerCode){
 const b={require,process:{argv:[]},__proof:copy(p),structuredClone,console};
 return vm.runInNewContext(checkerCode+'\ncheckProof(__proof,{control:true})',
  b,{timeout:8000})
}
function runCLI(p,checkerFile,tmp,name){
 const b=packetBytes(p),f=path.join(tmp,name+'.json');fs.writeFileSync(f,b);
 const r=cp.spawnSync(process.execPath,[checkerFile,f],
  {encoding:'utf8',timeout:20000,maxBuffer:1048576});
 assert.equal(r.error,undefined,'original verifier subprocess launch');
 const accepted=r.status===0;
 return {name,accepted,exit_code:r.status,paid:p.summary.paid_total,
  source:p.summary.source,res:p.summary.resolution,owners:p.summary.paid_gates,
  records:p.records.length,bytes:b.length,sha256:hash(b),
  original:accepted?JSON.parse(r.stdout.trim().split(/\r?\n/).at(-1)):null,
  error:accepted?null:(r.stderr||r.stdout).slice(0,140)}
}
function main(){
 const native=pinned(checker,originalCheckerBlob).toString('utf8');
 const seed=JSON.parse(pinned(seedfile,originalSeedBlob));
 const {packet:q,removed}=quotient(seed),terminal=terminalCone(q);
 assert.deepEqual(removed,[{old:20,replaced_by:9,kind:'SOURCE'},
  {old:21,replaced_by:9,kind:'SOURCE'}]);
 assert.equal(source(q),source(seed));assert.equal(source(terminal),source(seed));
 assert.deepEqual([seed.summary.paid_total,q.summary.paid_total,terminal.summary.paid_total],[32,30,29]);
 assert.deepEqual([seed.records.length,q.records.length,terminal.records.length],[50,48,45]);
 const gateFree=copy(terminal);gateFree.gate_defs=[];tally(gateFree);
 const proofCore=runCore(gateFree,native);assert.equal(proofCore.paid,28);
 const cases=[['seed_561_live',seed,true],['value_quotient_W30',q,true],
  ['terminal_cone_W29',terminal,true]];
 const bad=(name,base,fn)=>{const p=copy(base);fn(p);cases.push([name,p,false])};
 bad('wrong_source_sign',terminal,p=>p.records[7].c=[-1,-4,5,-7]);
 bad('source_occurrence_removed',terminal,p=>{p.records.splice(0,1);tally(p)});
 bad('underpaid',terminal,p=>p.summary.paid_total--);
 bad('bad_pivot',terminal,p=>p.records.at(-1).pivot=999);
 bad('false_resolvent',terminal,p=>p.records.at(-1).c=[-7]);
 bad('forward_parent',terminal,p=>p.records.at(-1).parents[0]=p.records.length);
 bad('bad_parent_alias',terminal,p=>p.records[20].parents[1]=2);
 bad('duplicate_gate_owner',terminal,p=>{p.gate_defs.push([0,8,1,4]);tally(p)});
 bad('wrong_output_clause',seed,p=>p.records[20].c=[-1,-4,-7]);
 cases.push(['core_W28_CLI_reject',gateFree,false]);
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2-562-'));
 try{
  const results=cases.map(([name,p,expected])=>{
   const actual=runCLI(p,checker,tmp,name);
   assert.equal(actual.accepted,expected,'original-checker differential failed: '+name);
   if(actual.accepted){assert.equal(actual.original.paid,actual.paid);
    assert.equal(actual.original.negativeTests,11)}
   return {...actual,expected};
  });
  const out={run:'LSPV-2/562',checker_git_blob:originalCheckerBlob,
   seed_git_blob:originalSeedBlob,source_occurrences_preserved:true,
   core_gatefree_W28_accepted:proofCore.paid===28,
   full_R_mix341_authenticated:false,owner_and_CLI_boundary:'must preserve >=1 owner',
   transformed_paid:[32,30,29],refuting_records:[50,48,45],
   removed_duplicate_RES:removed,positives:results.filter(x=>x.accepted).length,
   negatives:results.filter(x=>!x.accepted).length,results};
  const outdir=process.argv[2];
  if(outdir){fs.mkdirSync(outdir,{recursive:true});
   fs.writeFileSync(path.join(outdir,'value_quotient_W30.json'),packetBytes(q));
   fs.writeFileSync(path.join(outdir,'terminal_cone_W29.json'),packetBytes(terminal));
   fs.writeFileSync(path.join(outdir,'core_only_W28.json'),packetBytes(gateFree));
   fs.writeFileSync(path.join(outdir,'manifest.json'),JSON.stringify(out,null,2)+'\n')}
  console.log(JSON.stringify(out,null,2))
 }finally{fs.rmSync(tmp,{recursive:true,force:true})}
}
if(require.main===module)main();
module.exports={quotient,terminalCone,source,tally,runCore};
