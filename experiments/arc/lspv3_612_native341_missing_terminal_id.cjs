#!/usr/bin/env node
'use strict';
// LSPV-3/612. Run from any directory with: node experiments/arc/lspv3_612_native341_missing_terminal_id.cjs
// Executes the original archived checker in OS Node subprocesses, not a reconstructed checker.
const fs=require('fs'),path=require('path'),os=require('os'),cp=require('child_process'),crypto=require('crypto'),assert=require('assert');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const original=path.join(root,'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json');
const typedPath=path.join(root,'results/raw/arc/2026-11-13_0319_LSPV3_611_TYPED_ID_ACCEPTED.json');
function gitSHA(file){const bytes=fs.readFileSync(file);return crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+bytes.length+'\0'),bytes])).digest('hex');}
assert.strictEqual(gitSHA(checker),'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0');
assert.strictEqual(gitSHA(original),'fe27fe1011d0021e721ccaeb747ed58da65d7464');
const seven=JSON.parse(fs.readFileSync(original,'utf8')),typed=JSON.parse(fs.readFileSync(typedPath,'utf8'));
const clone=x=>JSON.parse(JSON.stringify(x));
const k4=clone(seven);k4.fixtures=[k4.fixtures[0]];k4.summary=[k4.summary[0]];
const tmpdir=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-l3-612-'));
const tmp=path.join(tmpdir,'input.json');const tests=[];
try {
 function check(name,base,edit,expected){
   const p=clone(base);edit(p);fs.writeFileSync(tmp,JSON.stringify(p)+'\n');
   const proc=cp.spawnSync(process.execPath,[checker,tmp],{encoding:'utf8',timeout:25000,maxBuffer:16*1024*1024});
   if(proc.error)throw proc.error;
   const accepted=proc.status===0;
   const actual=accepted?'ACCEPT':'REJECT';
   if(accepted!== (expected==='ACCEPT'))throw new Error(name+' expected '+expected+' got '+actual+' '+proc.stdout+' '+proc.stderr);
   let checks=null;
   if(accepted){checks=JSON.parse(proc.stdout).checks;}
   tests.push({name,expected,actual,checks});
 }
 check('baseline_seven',seven,()=>{},'ACCEPT');
 check('omit_seven_terminal_ids',seven,d=>d.fixtures.forEach(f=>delete f.proof.at(-1).id),'ACCEPT');
 check('baseline_K4',k4,()=>{},'ACCEPT');
 for(let i=0;i<15;i++)check('remove_paid_id_'+i,k4,d=>delete d.fixtures[0].proof[i].id,i===14?'ACCEPT':'REJECT');
 for(let i=0;i<16;i++)check('remove_source_id_'+i,k4,d=>delete d.fixtures[0].clauses[i].id,'REJECT');
 check('omit_two_paid_ids',k4,d=>{delete d.fixtures[0].proof.at(-1).id;delete d.fixtures[0].proof.at(-2).id;},'REJECT');
 check('omit_source_and_deletion_reference',k4,d=>{delete d.fixtures[0].clauses[0].id;delete d.fixtures[0].deleted[0].sourceId;},'REJECT');
 check('mutate_AND3_table',k4,d=>d.fixtures[0].proof[0].table^=1,'REJECT');
 check('forge_first_parent',k4,d=>d.fixtures[0].proof[0].parents[0]='forged','REJECT');
 check('typed_terminal_absent',typed,d=>delete d.fixtures[0].proof.at(-1).id,'ACCEPT');
 check('typed_terminal_null_alias',typed,d=>d.fixtures[0].proof.at(-1).id=null,'REJECT');
 check('typed_terminal_fresh_string',typed,d=>d.fixtures[0].proof.at(-1).id='fresh-612','ACCEPT');
 const accept=tests.filter(t=>t.actual==='ACCEPT');const reject=tests.filter(t=>t.actual==='REJECT');
 assert.strictEqual(tests.length,41);assert.strictEqual(accept.length,6);assert.strictEqual(reject.length,35);
 assert.strictEqual(accept.reduce((a,t)=>a+t.checks,0),67032);
 console.log(JSON.stringify({evidence_id:'P2-L3-612',mode:'original checker OS Node subprocess',total:tests.length,accept:accept.length,reject:reject.length,positive_assertions:67032,tests},null,2));
} finally {fs.rmSync(tmpdir,{recursive:true,force:true});}
