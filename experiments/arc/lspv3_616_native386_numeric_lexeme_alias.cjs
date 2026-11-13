#!/usr/bin/env node
'use strict';
// LSPV-3/616, original archived /386 complete CLI numeric-lexeme verification.
// Usage: node experiments/arc/lspv3_616_native386_numeric_lexeme_alias.cjs [output.json]
// This is a standalone operating-system Node reproduction. It does not invent new proof rules.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const os=require('node:os');
const cp=require('node:child_process');
const crypto=require('node:crypto');
const root=path.resolve(__dirname,'../..');
const checker='experiments/arc/lspv2_386_independent_verify.js';
const seedfile='results/raw/arc/2026-11-11_0407_LSPV2_555_ACCEPTED_LIVE_DEF_RES_K1.json';
const pins={
  checker:'338305c0ce101704205e57543756b8127074a986',
  seed:'aeeb555c4dcf7f510a9a501c8afc609b629a9298'
};
function blobsha(b){return crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');}
const cbuf=fs.readFileSync(path.join(root,checker));
const sbuf=fs.readFileSync(path.join(root,seedfile));
assert.equal(blobsha(cbuf),pins.checker,'original checker Git blob mismatch');
assert.equal(blobsha(sbuf),pins.seed,'original seed Git blob mismatch');
const base=sbuf.toString('utf8');
function rep(txt,a,b){assert(txt.includes(a),'missing mutation source '+a);return txt.replace(a,b);}
const substitutions=[
 ['"h":4','"h":4.0'],
 ['"edges":[[0,1]','"edges":[[-0,1e0]'],
 ['"charge":[1,0,0,0]','"charge":[1e0,0.0,0,0]'],
 ['"guard":7','"guard":7e0'],
 ['"gate_defs":[[0,8,1,4]','"gate_defs":[[-0,8.0,1e0,4.0]'],
 ['"kind":"DEF","gate":0','"kind":"DEF","gate":0e0'],
 ['"source":0}','"source":-0}'],
 ['"parents":[0,11],"pivot":1','"parents":[0e0,11.0],"pivot":1e0'],
 ['"paid_total":33','"paid_total":33.0'],
 ['"source":17','"source":17e0']
];
const alias=substitutions.reduce((t,[a,b])=>rep(t,a,b),base);
assert.equal(JSON.stringify(JSON.parse(alias)),JSON.stringify(JSON.parse(base)),'JSON serialization differs');
assert.equal(Object.is(JSON.parse('-0'),JSON.parse('0')),false,'negative-zero distinct under Object.is');
assert.equal(new Map([[-0,'a']]).get(0),'a','native Map SameValueZero');
const tests=[
 ['baseline',base,true],
 ['all_numeric_lexemes',alias,true],
 ['gate_owner_exponent',rep(base,'"gate_defs":[[0,8,1,4]','"gate_defs":[[0e0,8,1,4]'),true],
 ['DEF_gate_negative_zero',rep(base,'"kind":"DEF","gate":0','"kind":"DEF","gate":-0'),true],
 ['RES_parent_exponent',rep(base,'"parents":[0,11],"pivot":1','"parents":[0e0,11],"pivot":1'),true],
 ['RES_pivot_decimal',rep(base,'"parents":[0,11],"pivot":1','"parents":[0,11],"pivot":1.0'),true],
 ['SOURCE_index_exponent',rep(base,'"source":0}','"source":0e0}'),true],
 ['parent_negative_zero',rep(base,'"parents":[0,11],"pivot":1','"parents":[-0,11],"pivot":1'),true],
 ['wire_z_exponent',rep(base,'"gate_defs":[[0,8,1,4]','"gate_defs":[[0,8e0,1,4]'),true],
 ['invalid_owner_string',rep(base,'"kind":"DEF","gate":0','"kind":"DEF","gate":"0"'),false],
 ['invalid_owner_infinity',rep(base,'"kind":"DEF","gate":0','"kind":"DEF","gate":1e309'),false],
 ['malformed_json_00',rep(base,'"gate_defs":[[0,8,1,4]','"gate_defs":[[00,8,1,4]'),false],
 ['underpaid',rep(base,'"paid_total":33','"paid_total":32'),false],
 ['wrong_source_index',rep(base,'"source":0}','"source":5}'),false],
 ['bad_RES_parent',rep(base,'"parents":[0,11],"pivot":1','"parents":[999,11],"pivot":1'),false],
 ['wrong_pivot',rep(base,'"parents":[0,11],"pivot":1','"parents":[0,11],"pivot":9'),false]
];
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-616-'));
const results=[];
try{
 for(let i=0;i<tests.length;i++){
  const [name,bytes,accept]=tests[i],f=path.join(tmp,'case_'+i+'.json');
  fs.writeFileSync(f,bytes,'utf8');
  const run=cp.spawnSync(process.execPath,[path.join(root,checker),f],
     {encoding:'utf8',maxBuffer:8*1024*1024});
  let j=null;if(run.status===0){try{j=JSON.parse(run.stdout)}catch(e){}}
  const actual=run.status===0&&j!==null;
  assert.equal(actual,accept,'wrong original checker verdict for '+name+': '+run.stderr);
  if(actual){
   assert.equal(j.paid,33);assert.equal(j.res,30);assert.equal(j.def,3);
   assert.equal(j.records,51);assert.equal(j.sources,17);
   assert.equal(j.assertions,3509);assert.equal(j.negativeTests,11);
   assert.equal(j.sha256,crypto.createHash('sha256').update(bytes).digest('hex'));
  }
  results.push({name,expected:accept?'ACCEPT':'REJECT',actual:actual?'ACCEPT':'REJECT',
    bytes:Buffer.byteLength(bytes),paid:j?.paid??null,
    assertions:j?.assertions??null,
    sha256:crypto.createHash('sha256').update(bytes).digest('hex'),
    stderr:actual?null:run.stderr.slice(0,400)});
 }
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
const output={run:'LSPV3-616-NATIVE386-NUMERIC-LEXEMES-OS',execution:'original checker separate Node processes',pins,cases:results,positive:9,negative:7,unexpected:0,complete_mixed_Rmix341:false,p_vs_np:'OPEN'};
const serialized=JSON.stringify(output,null,2)+'\n';
if(process.argv[2])fs.writeFileSync(process.argv[2],serialized);
process.stdout.write(serialized);
