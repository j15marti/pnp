#!/usr/bin/env node
'use strict';
// LSPV-3/613. Run from repository checkout:
// node experiments/arc/lspv3_613_terminal_object_id_native.cjs [raw-output.json]
// Executes the pinned original /341 checker as a fresh OS Node process for EVERY case.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),cp=require('node:child_process'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const corpus=path.join(root,'results/raw/arc/2026-11-10_1112_LSPV2_537_NATIVE_BYTE_CORPUS_RAW.json');
function gitBlob(p){const b=fs.readFileSync(p);return crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\\0'),b])).digest('hex');}
assert.equal(gitBlob(checker),'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0','original checker SHA');
assert.equal(gitBlob(corpus),'d5e2d22674b0af365e9b82e4f1b2af8307182ba6','original corpus SHA');
const seed=JSON.parse(JSON.parse(fs.readFileSync(corpus,'utf8')).minimal.packetBytes);
const clone=x=>JSON.parse(JSON.stringify(x));
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-l3-613-'));
const packetFile=path.join(dir,'packet.json'),tests=[];
function test(name,modify,expected){
 const p=clone(seed);modify(p.fixtures[0]);fs.writeFileSync(packetFile,JSON.stringify(p)+'\\n');
 const r=cp.spawnSync(process.execPath,[checker,packetFile],{encoding:'utf8',timeout:25000,maxBuffer:8*1024*1024});
 if(r.error)throw r.error;
 const verdict=r.status===0?'ACCEPT':'REJECT';
 if(verdict!==expected)throw Error(name+' expected '+expected+' got '+verdict+' '+r.stdout+' '+r.stderr);
 const checks=verdict==='ACCEPT'?JSON.parse(r.stdout).checks:null;
 tests.push({name,expected,verdict,checks,error:verdict==='REJECT'?r.stderr.slice(0,200):undefined});
}
try{
 test('baseline',()=>{},'ACCEPT');
 const vals=[
 ['terminal_empty_object',{}],
 ['terminal_nested_object',{x:[{},[1,null,{a:'s0'}]]}],
 ['terminal_empty_array',[]],
 ['terminal_nested_array',['s0',4,false,{}]],
 ['terminal_null',null],['terminal_false',false],['terminal_number',17],
 ['terminal_mimics_existing_source_literal',{id:'s0'}],
 ['terminal_mimics_parent_array',['d13','d11']]
 ];
 for(const [name,id] of vals)test(name,f=>f.proof.at(-1).id=id,'ACCEPT');
 test('terminal_absent',f=>delete f.proof.at(-1).id,'ACCEPT');
 test('source_object_duplicate_structure',f=>{f.clauses[0].id={a:1};f.proof[0].parents[0]={a:1};f.deleted[0].sourceId={a:1}},'REJECT');
 test('source_array_duplicate_structure',f=>{f.clauses[0].id=['s0'];f.proof[0].parents[0]=['s0'];f.deleted[0].sourceId=['s0']},'REJECT');
 test('nonterminal_object_id_equal_structure',f=>{f.proof[0].id={a:1};f.proof[1].parents[0]={a:1}},'REJECT');
 test('nonterminal_array_id_equal_structure',f=>{f.proof[0].id=['d0'];f.proof[1].parents[0]=['d0']},'REJECT');
 test('terminal_mutate_parent_undefined',f=>{f.proof.at(-1).id={};f.proof.at(-1).parents[0]={}},'REJECT');
 test('terminal_duplicate_primitive',f=>f.proof.at(-1).id='s0','REJECT');
 test('terminal_invalid_parent',f=>{f.proof.at(-1).id={};f.proof.at(-1).parents[0]='fake'},'REJECT');
 const yes=tests.filter(t=>t.verdict==='ACCEPT'),no=tests.filter(t=>t.verdict==='REJECT');
 assert.equal(tests.length,18);assert.equal(yes.length,11);assert.equal(no.length,7);
 assert.equal(yes.reduce((a,t)=>a+t.checks,0),15411);
 const out={evidence_id:'P2-L3-613',execution:'original checker OS Node subprocess',checker_blob:gitBlob(checker),corpus_blob:gitBlob(corpus),counts:{total:18,accept:11,reject:7,positive_assertions:15411},tests};
 const target=process.argv[2];if(target)fs.writeFileSync(target,JSON.stringify(out,null,2)+'\\n');
 process.stdout.write(JSON.stringify(out,null,2)+'\\n');
}finally{fs.rmSync(dir,{recursive:true,force:true});}
