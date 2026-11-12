#!/usr/bin/env node
'use strict';
/* LSPV-3/583 (2026-11-11 19:24 PST)
   Execute from j15marti/pnp repository root:
     node experiments/arc/lspv3_583_support_string_rotation_native_replay.cjs
   Uses the UNCHANGED original archived /341 checker body through vm.runInNewContext
   with only fs/argv/console adapters. It does NOT implement a replacement checker.
   Does not authenticate full historical R_mix341, which remains OPEN.
*/
const fs = require('node:fs');
const vm = require('node:vm');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const root = process.cwd();
const checkerPath = 'experiments/arc/lspv2_341_independent_verify.js';
const baselinePath = 'results/raw/arc/2026-11-11_1824_LSPV3_582_STRING_CHARGE_SAT_ACCEPTED_PACKET.json';
const rotatedPath = 'results/raw/arc/2026-11-11_1924_LSPV3_583_ROTATED_SUPPORT_SAT_ACCEPTED_PACKET.json';
const rawPath = 'results/raw/arc/2026-11-11_1924_LSPV3_583_SUPPORT_STRING_ROTATION_V8_RAW.json';
function gitBlob(buf) {
  return crypto.createHash('sha1')
    .update('blob ' + buf.length + '\0').update(buf).digest('hex');
}
function load(path, expectedSHA) {
  const b=fs.readFileSync(path);
  assert.equal(gitBlob(b),expectedSHA,'Git blob mismatch at ' + path);
  return b.toString('utf8');
}
const original=load(checkerPath,'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0');
const seedText=load(baselinePath,'6cf9b0fe1e5a9419e8967d836c707c385418b810');
const rotatedText=load(rotatedPath,'5d78d8f6eb5934bf805ee90736b1f88d4acd2729');
const seed=JSON.parse(seedText);
const rotated=JSON.parse(rotatedText);
const F=seed.fixtures[0],E=F.graph.edges.length,V=F.graph.n;
const clone=o=>JSON.parse(JSON.stringify(o));
const assignment='101001000000100000';
const bits=[...assignment].map(Number);
const satisfied=(c,b)=>c.literals.some(l=>l>0?b[l-1]===1:b[-l-1]===0);
const falsified=F.clauses.filter(c=>!satisfied(c,bits));
assert.equal(falsified.length,0,'source must be SAT');
assert.deepEqual(rotated.fixtures[0].clauses,F.clauses,'signed source changed');
assert.deepEqual(rotated.fixtures[0].charges,F.charges,'charge bytes changed');
assert.equal(F.proof.length,47,'paid work changed');
assert.equal(F.proof[2].id,50);
assert.deepEqual(F.proof[2].parents,[49,3]);
const incid=Array.from({length:V},()=>[]);
F.graph.edges.forEach(([u,v],e)=>{incid[u].push(e);incid[v].push(e)});
const factors=new Map;
for(const c of F.clauses) {
  const sup=incid[c.vertex].slice();
  let table=0;
  for(let m=0;m<8;m++){
    const a=Array(E).fill(0);
    sup.forEach((e,i)=>a[e]=(m>>i)&1);
    if(satisfied(c,a))table|=1<<m;
  }
  factors.set(c.id,{support:sup,table});
}
for(const p of F.proof.slice(0,2))factors.set(p.id,p);
const parents=F.proof[2].parents.map(id=>factors.get(id));
function tableValue(node,b) {
  let mask=0;
  for(let i=0;i<node.support.length;i++)
    mask|=Number(b[node.support[i]])<<i;
  return (node.table>>mask)&1;
}
function tableFor(s) {
  let t=0;
  for(let m=0;m<8;m++){
    const a=Array(E).fill(0);
    for(let j=0;j<3;j++)a[s[j]]=(m>>j)&1;
    if(parents.every(p=>tableValue(p,a)===1))t|=1<<m;
  }
  return t;
}
function rotatedSupport(s){
  const p=clone(seed);
  p.fixtures[0].proof[2].support=s;
  p.fixtures[0].proof[2].table=tableFor(s);
  return p;
}
function unchangedChecker(p){
  const logged=[];
  try {
    vm.runInNewContext(original,{
      require:n=>{
        assert.equal(n,'fs','unexpected module requested by original');
        return {readFileSync:()=>JSON.stringify(p)};
      },
      process:{argv:['node',checkerPath,'in-memory.json']},
      console:{log:s=>logged.push(s)}
    },{filename:checkerPath,timeout:15000});
    assert.equal(logged.length,1);
    const result=JSON.parse(logged[0]);
    return {accepted:true,checks:result.checks};
  } catch(e) {return {accepted:false,error:String(e.message)};}
}
const cases=[];
for(const s of ['012','120','102','021','210','201']){
  const p=rotatedSupport(s);
  cases.push({id:'string_'+s,support:s,table:p.fixtures[0].proof[2].table,...unchangedChecker(p)});
}
const negatives=[
 ['rotated_unadjusted_table',p=>{p.fixtures[0].proof[2].table=102}],
 ['correct_numeric_support',p=>{p.fixtures[0].proof[2].support=[0,1,12];p.fixtures[0].proof[2].table=90}],
 ['support_array_strings',p=>{p.fixtures[0].proof[2].support=['1','2','0']}],
 ['support_length_four',p=>{p.fixtures[0].proof[2].support='1200'}],
 ['source_parity_typed_numeric',p=>{p.fixtures[0].charges[0]=1}],
 ['forged_source_lit',p=>{p.fixtures[0].clauses[0].literals[0]=999}],
 ['unsupported_local_convert',p=>{p.fixtures[0].proof[2].rule='LOCAL-CONVERT'}],
 ['nonexistent_parent',p=>{p.fixtures[0].proof[2].parents[0]=987654}],
 ['wrong_sink',p=>{p.fixtures[0].proof.at(-1).row.rhs^=1}]
];
for(const [id,mutation] of negatives){
  const p=clone(rotated);
  mutation(p);
  cases.push({id,...unchangedChecker(p)});
}
assert.deepEqual(cases.slice(0,6).map(x=>x.accepted),[true,true,false,false,false,false]);
assert(cases.slice(6).every(x=>!x.accepted),'hostile certificate accepted');
assert(cases.slice(0,2).every(x=>x.checks===3273));
assert.deepEqual(rotated,rotatedSupport('120'),'published byte payload not generated from specified mutation');
assert.equal(JSON.stringify(rotated)+'\n',rotatedText,'published raw bytes mismatch');
const alias=['012','120'].map(s=>{
  const p=rotatedSupport(s),r=p.fixtures[0].proof[2];
  const idx=[...s].reduce((t,d,i)=>t|(bits[Number(d)]<<i),0);
  return {
    support:s,table:r.table,model_index:idx,
    claimed_factor_value:(r.table>>idx)&1,
    actual_row_left:bits[0]^bits[1]^bits[12],
    actual_row_rhs:r.row.rhs
  };
});
assert(alias.every(x=>x.claimed_factor_value===1&&x.actual_row_left===0&&x.actual_row_rhs===1));
const historicalRaw=JSON.parse(fs.readFileSync(rawPath,'utf8'));
assert.deepEqual(cases,historicalRaw.checks,'raw matrix changed');
assert.deepEqual(alias,historicalRaw.model_alias_evidence,'source countermodel mismatch');
assert.equal(historicalRaw.passes,2);
assert.equal(historicalRaw.rejections,13);
console.log(JSON.stringify({
  role:'LSPV-3/583',verifier:'unchanged archived /341 body in Node OS-hosted VM',
  checker_git_blob:gitBlob(Buffer.from(original,'utf8')),
  packet_git_blob:gitBlob(Buffer.from(rotatedText,'utf8')),
  original_clauses:F.clauses.length,source_falsified:0,
  paid_nodes:F.proof.length,
  positives:cases.filter(x=>x.accepted).length,
  negatives:cases.filter(x=>!x.accepted).length,
  accepted_checker_assertions:3273,
  exact_agreement_with_published_raw:true,
  historical_full_mix341_authenticated:false
},null,2));
