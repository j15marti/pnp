#!/usr/bin/env node
'use strict';
// LSPV-3/568: reproducible original-checker numerical charge regression.
// Run from repo root: node experiments/arc/lspv3_568_numeric_wrap32_source_forgery.cjs [--write]
// The unmodified archived /341 fixture checker, not the complete R_mix341 grammar.
const fs=require('node:fs'),os=require('node:os'),path=require('node:path'),
  cp=require('node:child_process'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const seed=path.join(root,'results/raw/arc/2026-11-10_1724_LSPV3_557_SINGLE_SAT_PACKET.json');
const packet=path.join(root,'results/raw/arc/2026-11-11_0424_LSPV3_568_NUMERIC_WRAP32_SAT_ACCEPTED_PACKET.json');
const outFile=path.join(root,'results/raw/arc/2026-11-11_0424_LSPV3_568_NUMERIC_WRAP32_OS_NODE_RAW.json');
function blob(s){return crypto.createHash('sha1').update(Buffer.concat([
  Buffer.from('blob '+Buffer.byteLength(s)+'\0'),Buffer.from(s)])).digest('hex');}
const checkSource=fs.readFileSync(checker,'utf8');
const seedSource=fs.readFileSync(seed,'utf8');
assert.equal(blob(checkSource),'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0');
assert.equal(blob(seedSource),'6cf9b0fe1e5a9419e8967d836c707c385418b810');
const clone=x=>JSON.parse(JSON.stringify(x));
const source=JSON.parse(seedSource),forged=clone(source);
forged.fixtures[0].charges[0]=4294967297; // 2^32+1, exactly representable safe integer
const raw=JSON.stringify(forged);
assert.equal(Buffer.byteLength(raw),8580);
assert.equal(fs.readFileSync(packet,'utf8'),raw,'published accepted bytes must match');
const f=forged.fixtures[0],a='101001000000100000';
const sat=(c,bits)=>c.literals.some(l=>Number(bits[Math.abs(l)-1])===(l>0?1:0));
assert.equal(f.clauses.filter(c=>sat(c,a)).length,48);
assert.equal(f.clauses.filter(c=>sat(c,'0'.repeat(18))).length,47);
assert.equal(f.proof.length,47);
assert.equal(f.charges.reduce((x,y)=>x^y,0),1);
assert(f.charges.every(Number.isSafeInteger));
assert(!f.charges.every(x=>x===0||x===1));
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-568-'));
function originalChecker(o){
  const tmp=path.join(dir,'fixture.json');
  fs.writeFileSync(tmp,JSON.stringify(o));
  const p=cp.spawnSync(process.execPath,[checker,tmp],
    {encoding:'utf8',timeout:10000,maxBuffer:10000000});
  if(p.error)throw p.error;
  if(p.status===0)return {accepted:true,assertions:JSON.parse(p.stdout).checks};
  const e=(p.stderr||p.stdout||'').trim().split('\n');
  return {accepted:false,error:e.find(x=>x.includes('Verifier:'))||e.at(-1)||'no error text'};
}
const cases=[
 ['wrap32_positive',()=>{},true],
 ['base_prior_string',f=>{f.charges[0]='1'},true],
 ['single_safe_1',f=>{f.charges[0]=1},false],
 ['single_zero',f=>{f.charges[0]=0},false],
 ['single_2pow32',f=>{f.charges[0]=4294967296},false],
 ['single_2pow31_plus1',f=>{f.charges[0]=2147483649},false],
 ['another_2pow33_plus1',f=>{f.charges[0]=8589934593},true],
 ['single_fractional',f=>{f.charges[0]=1.5},true],
 ['pair_2_3',f=>{f.charges[0]=2;f.charges[1]=3},true],
 ['typed_support',f=>{f.proof[2].support=[0,1,12]},false],
 ['bad_affine_mask',f=>{f.proof[2].row.mask='0x1002'},false],
 ['bad_table',f=>{f.proof[2].table^=1},false],
 ['bad_sink',f=>{f.proof.at(-1).row.rhs^=1},false],
 ['bad_source',f=>{f.clauses[0].literals[0]=999},false],
 ['bad_parent',f=>{f.proof[0].parents[0]=999},false],
 ['bad_deletion',f=>{f.deleted[0].assignment='1'+'0'.repeat(17)},false]
];
let results=[];
try{
 for(const [name,change,expected] of cases){
   const z=clone(forged);change(z.fixtures[0]);
   const observed=originalChecker(z);
   assert.equal(observed.accepted,expected,'unexpected native outcome: '+name);
   if(observed.accepted)assert.equal(observed.assertions,3273);
   results.push({name,expected,...observed});
 }
}finally{fs.rmSync(dir,{recursive:true,force:true});}
const out={label:'LSPV3-568 original OS Node replay',native:true,node:process.version,
 checker_blob:blob(checkSource),seed_blob:blob(seedSource),packet_sha256:crypto.createHash('sha256').update(raw).digest('hex'),
 packet_bytes:Buffer.byteLength(raw),source_sat_witness:a,source_clauses_satisfied:48,
 paid_nodes:47,charges:f.charges,all_numeric_safe_int:true,all_binary:false,
 tests:results.length,accepted:results.filter(x=>x.accepted).length,
 rejected:results.filter(x=>!x.accepted).length,all_passed:true,results,
 status:'Original /341 specialized fixture checker UNSOUND on this raw source; not full R_mix341' };
if(process.argv.includes('--write'))fs.writeFileSync(outFile,JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify(out,null,2));
