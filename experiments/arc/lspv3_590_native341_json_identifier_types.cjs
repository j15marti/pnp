#!/usr/bin/env node
'use strict';
/* LSPV-3/590. Reproduce the checked lexical identifier domain in the ORIGINAL
   unchanged archived /341 checker using actual Node OS subprocesses.
   The original checker, original fixture and published witness are pinned by
   Git blob SHA-1. It is not a new R_mix341 verifier. */
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const os=require('node:os'),cp=require('node:child_process'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const files={
 checker:['experiments/arc/lspv2_341_independent_verify.js','fcb7d4ced8f922de14c0bda16263a8cc7853e8e0'],
 original:['results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json','fe27fe1011d0021e721ccaeb747ed58da65d7464'],
 witness:['results/raw/arc/2026-11-12_0728_LSPV3_590_NULL_SOURCE_OBJECT_TERMINAL_NATIVE341.json','PIN_WITNESS_SHA_ON_READBACK']
};
function blob(b){return crypto.createHash('sha1').update('blob '+b.length+'\\0').update(b).digest('hex')}
const raw={};
for(const [name,[p,sha]] of Object.entries(files)){
 const bytes=fs.readFileSync(path.join(root,p));
 if(sha!=='PIN_WITNESS_SHA_ON_READBACK')assert.equal(blob(bytes),sha,'drift '+p);
 raw[name]=JSON.parse(name==='checker'?'null':bytes.toString('utf8'));
}
const cpj=x=>JSON.parse(JSON.stringify(x));
const original=raw.original,base=original.fixtures[0];
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-590-'));
function change(f,which,val){
 const target=which==='source'?f.clauses[0]:which==='proof'?f.proof[0]:f.proof.at(-1);
 const old=target.id;target.id=val;
 if(which==='source')for(const d of f.deleted)if(d.sourceId===old)d.sourceId=val;
 if(which!=='terminal')for(const p of f.proof)p.parents=p.parents.map(x=>x===old?val:x);
}
function checkOne(name,mut,expected){
 const f=cpj(base);mut(f);
 const pkt=cpj({fixtures:[f],summary:[original.summary[0]]});
 const file=path.join(temp,name+'.json');
 fs.writeFileSync(file,JSON.stringify(pkt)+'\\n');
 const run=cp.spawnSync(process.execPath,[path.join(root,files.checker[0]),file],
  {encoding:'utf8',timeout:30000});
 const ok=run.status===0;
 assert.equal(ok,expected,name+' '+run.stderr);
 return {name,accepted:ok,expected,
  checks:ok?JSON.parse(run.stdout).checks:null,
  rejection:ok?null:run.stderr.slice(0,200),
  bytes:Buffer.byteLength(JSON.stringify(pkt)+'\\n')};
}
const rows=[];
try{
 function t(name,mut,expected){rows.push(checkOne(name,mut,expected))}
 t('unmodified_K4',()=>{},true);
 for(const [name,val] of [['null',null],['false',false],['true',true],['zero',0],['minus7',-7],['empty_string',''],['array',[]],['object',{}]])
  t('referenced_source_'+name,f=>change(f,'source',val),name!=='array'&&name!=='object');
 for(const [name,val] of [['null',null],['false',false],['true',true],['zero',0],['minus7',-7],['empty_string',''],['array',[]],['object',{}]])
  t('referenced_proof_'+name,f=>change(f,'proof',val),name!=='array'&&name!=='object');
 for(const [name,val] of [['null',null],['true',true],['zero',0],['array',[]],['object',{}],['nested',{nest:[null,{p:1}]}]])
  t('terminal_'+name,f=>change(f,'terminal',val),true);
 t('hostile_collision',f=>{change(f,'source',null);f.clauses[1].id=null;f.deleted[1].sourceId=null},false);
 t('hostile_deletion_lexeme',f=>{change(f,'source',null);f.deleted[0].sourceId='null'},false);
 t('hostile_parent_lexeme',f=>{change(f,'source',null);for(const p of f.proof){let i=p.parents.indexOf(null);if(i>=0){p.parents[i]='null';break}}},false);
 t('hostile_terminal_source_reference',f=>{change(f,'terminal',{});f.proof.at(-1).parents[0]={}},false);
 t('mixed_null_source_object_terminal',f=>{change(f,'source',null);change(f,'terminal',{namespace:'native341',opaque:[null,false,{x:1}]})},true);
 const file=path.join(temp,'mixed_null_source_object_terminal.json');
 assert.deepEqual(JSON.parse(fs.readFileSync(file,'utf8')),raw.witness);
 console.log(JSON.stringify({id:'LSPV-3/590',outcomes:rows,positives:rows.filter(x=>x.accepted).length,negatives:rows.filter(x=>!x.accepted).length},null,2));
}finally{fs.rmSync(temp,{recursive:true,force:true})}
