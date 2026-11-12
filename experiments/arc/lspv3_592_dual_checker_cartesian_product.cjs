#!/usr/bin/env node
'use strict';
// LSPV-3/592. Requires a complete j15marti/pnp checkout and Node.js.
// Executes the TWO UNCHANGED archived original checkers as independent OS
// subprocesses. Their intersection DOES NOT authenticate full R_mix341.
const fs=require('node:fs'), os=require('node:os'),path=require('node:path');
const crypto=require('node:crypto'),cp=require('node:child_process');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const paths={
 c341:'experiments/arc/lspv2_341_independent_verify.js',
 c386:'experiments/arc/lspv2_386_independent_verify.js',
 input341:'results/raw/arc/2026-11-11_1824_LSPV3_582_STRING_CHARGE_SAT_ACCEPTED_PACKET.json',
 input386:'results/raw/arc/2026-11-12_0424_LSPV3_587_NATIVE_CONSTANT_FACET_ACCEPTED_PACKET.json',
 dual:'results/raw/arc/2026-11-12_0924_LSPV3_592_DUAL_SAT_UNSAT_ACCEPTED_PACKET.json'
};
const pins={
 c341:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
 c386:'338305c0ce101704205e57543756b8127074a986',
 input341:'6cf9b0fe1e5a9419e8967d836c707c385418b810',
 input386:'4177ec15a0c7253378d5652a6b13b7152601d300',
 dual:'d104f7cfc8a10709919d65289bb0a31c0cc1c4ff'
};
function gitBlob(buf){
 return crypto.createHash('sha1')
  .update(Buffer.from('blob '+buf.length+'\0')).update(buf).digest('hex');
}
for(const [k,p] of Object.entries(paths)){
 const actual=gitBlob(fs.readFileSync(path.join(root,p)));
 assert.equal(actual,pins[k],'PINNED HISTORICAL CONTENT CHANGED: '+p);
}
const read=k=>JSON.parse(fs.readFileSync(path.join(root,paths[k]),'utf8'));
const a=read('input341'),b=read('input386'),d=read('dual');
const expected={fixtures:a.fixtures,spec:b.spec,gate_defs:b.gate_defs,
 records:b.records,summary:{length:1,...b.summary}};
assert.deepEqual(d,expected,'published dual packet differs from source-bound join');
const bits='101001000000100000';
assert.equal(bits.length,a.fixtures[0].graph.edges.length);
const sat=(clause,assignment)=>clause.some(l=>{
 const val=assignment[Math.abs(l)-1];
 return l>0?val===1:val===0;
});
const bs=[...bits].map(Number);
assert.equal(a.fixtures[0].clauses.filter(c=>sat(c.literals,bs)).length,48);
const source386=b.records.filter(r=>r.kind==='SOURCE');
assert.equal(source386.length,17);
let models386=0;
for(let m=0;m<64;m++){
 const v=Array.from({length:7},(_,i)=>i===6?1:(m>>i)&1);
 models386+=Number(source386.every(r=>sat(r.c,v)));
}
assert.equal(models386,0,'original /386 source should be UNSAT');
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-592-'));
const clone=v=>JSON.parse(JSON.stringify(v));
function run(checker,pkt){
 const local=path.join(tmp,'packet.json');
 fs.writeFileSync(local,JSON.stringify(pkt)+'\n');
 const res=cp.spawnSync(process.execPath,[path.join(root,paths[checker]),local],
 {encoding:'utf8',timeout:30000,maxBuffer:32000000});
 if(res.error)throw res.error;
 if(res.status!==0)return {accepted:false,
  diagnostic:(res.stderr||'').slice(-350)};
 const o=JSON.parse(res.stdout);
 return {accepted:true,assertions:o.assertions??o.checks,
  paid:o.paid??o.cases[0].proofNodes,
  negative_controls:o.negativeTests??o.corruptions};
}
const specs=[
 ['dual-positive',()=>{},true,true],
 ['forge-341-SOURCE',p=>{p.fixtures[0].clauses[0].literals[0]=999},false,true],
 ['forge-386-SOURCE',p=>{p.records.find(r=>r.kind==='SOURCE').c=[-p.spec.guard]},true,false],
 ['missing-341-parent',p=>{p.fixtures[0].proof[0].parents[0]='NO_SUCH_NODE'},false,true],
 ['missing-386-parent',p=>{p.records.at(-1).parents[0]=p.records.length+1},true,false],
 ['wrong-341-GF2-sink',p=>{p.fixtures[0].proof.at(-1).row.rhs^=1},false,true],
 ['wrong-386-RES-pivot',p=>{p.records.at(-1).pivot=999},true,false]
];
let results;
try{
 results=specs.map(([name,mut,expA,expB])=>{
  const pkt=clone(d);mut(pkt);
  const c341=run('c341',pkt),c386=run('c386',pkt);
  assert.equal(c341.accepted,expA,'341 '+name);
  assert.equal(c386.accepted,expB,'386 '+name);
  return {name,c341,c386};
 });
}finally{fs.rmSync(tmp,{recursive:true,force:true})}
assert.equal(results[0].c341.assertions,3273);
assert.equal(results[0].c386.assertions,3125);
const result={id:'LSPV-3/592',mode:'ACTUAL OS NODE TWO UNCHANGED ORIGINAL CHECKERS',
 status:'PASS; restricted dual-checker product only',source_341_SAT:48,
 source_386_models_guard_true:models386,dual_blob:pins.dual,checks:results};
console.log(JSON.stringify(result,null,2));
