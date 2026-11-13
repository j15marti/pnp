#!/usr/bin/env node
'use strict';
// LSPV-3/606. Pinned original checker OS replay and exact support-string cloud.
// Usage: node experiments/arc/lspv3_606_native341_support_string_cloud.cjs [output.json]
const fs=require('fs'),path=require('path'),os=require('os'),crypto=require('crypto');
const cp=require('child_process'),assert=require('assert/strict');
const root=path.resolve(__dirname,'../..');
const chk=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const pkt=path.join(root,'results/raw/arc/2026-11-12_2100_LSPV1_609_BRIDGE_SLICE_SAT_ACCEPTED.json');
function blob(b){return crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex')}
const checkerBlob=blob(fs.readFileSync(chk)),packetBlob=blob(fs.readFileSync(pkt));
assert.equal(checkerBlob,'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0');
assert.equal(packetBlob,'8d6d9bc7f2940a77edf2a07fcb72af111ba5b928');
const base=JSON.parse(fs.readFileSync(pkt,'utf8')),f=base.fixtures[0];
assert.equal(f.proof[17].support,'102');
function gram(s){return s.length===3&&new Set(s).size===3&&[0,1,10].every(i=>s.includes(i))}
const prev=f.proof[16],src=f.clauses[23];
function local(s){
 let table=0;
 for(let m=0;m<8;m++){
  const bits=Array(18).fill(0);
  for(let j=0;j<3;j++)bits[s[j]]=(m>>j)&1;
  let k=0;
  for(let j=0;j<prev.support.length;j++)k|=Number(bits[prev.support[j]])<<j;
  const a=(prev.table>>k)&1;
  const b=Number(src.literals.some(l=>l>0?bits[l-1]===1:bits[-l-1]===0));
  const v=a&b;
  if(v!==Number((bits[0]^bits[1]^bits[10])===0))return null;
  table|=v<<m;
 }
 return table;
}
let count=0,errors=0;
for(let i=0;i<65536;i++){
 const u=String.fromCharCode(i);
 for(const [s,table] of [['10'+u,153],[u+'10',195]]){
  const expected=i!==48&&i!==49;
  if(gram(s)!==expected)errors++;
  if(expected){count++;if(local(s)!==table)errors++}
 }
}
assert.equal(count,131068);assert.equal(errors,0);
let models=0,edge10=0,wrong=0;
for(let a=0;a<1<<18;a++){
 if(!f.clauses.every(c=>c.literals.some(l=>l>0?((a>>(l-1))&1)===1:((a>>(-l-1))&1)===0)))continue;
 models++;const x10=(a>>10)&1;edge10+=x10;
 if((((a>>0)&1)^((a>>1)&1)^x10)!==0)wrong++;
}
assert.equal(models,64);assert.equal(edge10,64);assert.equal(wrong,64);
const cases=[
 ['baseline','102',153,true],['prefix_ascii','10x',153,true],['suffix_ascii','x10',195,true],
 ['prefix_NUL','10\u0000',153,true],['suffix_NUL','\u000010',195,true],
 ['prefix_surrogate','10\uD800',153,true],['suffix_surrogate','\uDC0010',195,true],
 ['prefix_whitespace','10 ',153,true],['suffix_newline','\n10',195,true],
 ['prefix_digit','109',153,true],['suffix_digit','910',195,true],
 ['duplicate_prefix','100',153,false],['duplicate_suffix','110',195,false],
 ['wrong_substring','012',153,false],['wrong_table','x10',153,false],
 ['bad_row','10x',153,false],['bad_parent','10x',153,false],
 ['typed_array',[0,1,10],153,false]
];
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp606-')),runs=[];
try{
 for(let i=0;i<cases.length;i++){
  const [name,s,table,expected]=cases[i],d=JSON.parse(JSON.stringify(base));
  d.fixtures[0].proof[17].support=s;d.fixtures[0].proof[17].table=table;
  if(name==='bad_row')d.fixtures[0].proof[17].row.mask='0x7';
  if(name==='bad_parent')d.fixtures[0].proof[17].parents[1]='NO_SUCH_PARENT';
  const file=path.join(tmp,i+'.json');fs.writeFileSync(file,JSON.stringify(d));
  const r=cp.spawnSync(process.execPath,[chk,file],{encoding:'utf8',timeout:30000});
  const accept=r.status===0&&!r.error;
  assert.equal(accept,expected,name+': checker unexpected '+r.stderr);
  let checks=null;if(accept){checks=JSON.parse(r.stdout).checks;assert.equal(checks,5155)}
  runs.push({name,support:JSON.stringify(s),table,accept,checks,
    rejection:accept?null:(r.stderr||r.error?.message||'').trim().slice(0,160)});
 }
}finally{fs.rmSync(tmp,{recursive:true,force:true})}
const result={run:'LSPV3/606',checker_blob:checkerBlob,source_packet_blob:packetBlob,
 exact_string_support_count:count,per_orientation:65534,
 grammar_errors:errors,source_models:models,all_models_force_edge10:edge10,
 all_models_falsify_derived_row:wrong,
 hosted_or_os:'original Node operating-system subprocess',
 samples:runs,positives:runs.filter(x=>x.accept).length,
 negative_controls:runs.filter(x=>!x.accept).length,
 accepted_assertion_groups:runs.reduce((s,x)=>s+(x.checks||0),0),
 original_source_occurrences:48,paid_AND3:36,paid_GF2:11,logical_work:47,
 historical_full_Rmix341:'OPEN',P2_D1:'OPEN',P2_C3:'OPEN',P2_B1:'OPEN',
 P2_B2:'OPEN',P2_B3:'OPEN',P_vs_NP:'OPEN'};
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+'\n');
else console.log(JSON.stringify(result,null,2));
