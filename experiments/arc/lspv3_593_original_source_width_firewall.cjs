#!/usr/bin/env node
'use strict';
// LSPV-3/593. Run from j15marti/pnp root:
// node experiments/arc/lspv3_593_original_source_width_firewall.cjs [output.json]
// Calls BOTH unchanged original archived checkers in separate Node OS processes.
// Does NOT authenticate the full historical R_mix341 mixed-rule language.
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const cp=require('node:child_process'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const paths={
 c341:'experiments/arc/lspv2_341_independent_verify.js',
 c386:'experiments/arc/lspv2_386_independent_verify.js',
 original:'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json',
 dual:'results/raw/arc/2026-11-12_0924_LSPV3_592_DUAL_SAT_UNSAT_ACCEPTED_PACKET.json'
};
const pins={
 c341:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
 c386:'338305c0ce101704205e57543756b8127074a986',
 original:'fe27fe1011d0021e721ccaeb747ed58da65d7464',
 dual:'d104f7cfc8a10709919d65289bb0a31c0cc1c4ff'
};
const blob=b=>crypto.createHash('sha1')
 .update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
for(const [k,p] of Object.entries(paths))
 assert.equal(blob(fs.readFileSync(path.join(root,p))),pins[k],'pin mismatch '+p);
const read=k=>JSON.parse(fs.readFileSync(path.join(root,paths[k]),'utf8'));
const dual=read('dual'),original=read('original'),clone=x=>JSON.parse(JSON.stringify(x));
const sources341=p=>p.fixtures[0].clauses.map(c=>c.literals);
const sources386=p=>p.records.filter(r=>r.kind==='SOURCE').map(r=>r.c);
const widths=cs=>cs.reduce((h,c)=>(h[c.length]=(h[c.length]||0)+1,h),{});
const sig=c=>c.slice().sort((a,b)=>a-b).join(',');
const overlap=(A,B)=>{const s=new Set(B.map(sig));return A.filter(c=>s.has(sig(c))).length};
const A=sources341(dual),B=sources386(dual);
assert.deepEqual(widths(A),{'3':48});assert.deepEqual(widths(B),{'1':1,'4':16});
assert.equal(overlap(A,B),0);
const fixtures=original.fixtures.map(f=>{
 const cs=f.clauses.map(c=>c.literals);
 assert(cs.every(c=>c.length===3));assert.equal(overlap(cs,B),0);
 return {name:f.graph.name,clauses:cs.length,widths:widths(cs),overlap:0};
});
const tests=[
 ['baseline',p=>{},true,true],
 ['ignored-source-binding',p=>{p.authenticated_source={claimed_same_source:true,
   source_bytes:'NOT_A_MATCH',cross_parent:[48,16]}},true,true],
 ['341-width4',p=>p.fixtures[0].clauses[0].literals.push(19),false,true],
 ['341-width2',p=>p.fixtures[0].clauses[0].literals.pop(),false,true],
 ['386-width3',p=>{let r=p.records.find(r=>r.kind==='SOURCE'&&r.c.length===4);
    r.c=r.c.filter(x=>x!==-p.spec.guard)},true,false],
 ['386-unit-width3',p=>{p.records.find(r=>r.kind==='SOURCE'&&r.c.length===1)
    .c=[1,2,p.spec.guard]},true,false],
 ['341-replaced-by-386',p=>{p.fixtures[0].clauses[0].literals=clone(
    p.records.find(r=>r.kind==='SOURCE'&&r.c.length===4).c)},false,true],
 ['386-replaced-by-341',p=>{p.records.find(r=>r.kind==='SOURCE'&&r.c.length===4)
    .c=clone(p.fixtures[0].clauses[0].literals)},true,false]
];
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-593-'));
function execute(which,p){
 const file=path.join(tmp,'packet.json');fs.writeFileSync(file,JSON.stringify(p)+'\n');
 const r=cp.spawnSync(process.execPath,[path.join(root,paths[which]),file],
   {encoding:'utf8',timeout:30000,maxBuffer:32000000});
 if(r.error)throw r.error;
 if(r.status!==0)return {accepted:false,diagnostic:r.stderr.slice(-180)};
 const o=JSON.parse(r.stdout);
 return which==='c341'?{accepted:true,assertions:o.checks,
   proofNodes:o.cases[0].proofNodes}:{accepted:true,assertions:o.assertions,
   paid:o.paid,negativeTests:o.negativeTests};
}
let cases;
try {
 cases=tests.map(([name,mutate,w341,w386])=>{
  const p=clone(dual);mutate(p);
  const a=execute('c341',p),b=execute('c386',p);
  assert.equal(a.accepted,w341,'341 '+name);
  assert.equal(b.accepted,w386,'386 '+name);
  return {name,original341:a,original386:b};
 });
}finally{fs.rmSync(tmp,{recursive:true,force:true})}
assert.equal(cases[0].original341.assertions,3273);
assert.equal(cases[0].original386.assertions,3125);
const result={id:'LSPV-3/593',
 execution:'ACTUAL OS NODE TWO UNCHANGED ARCHIVED CHECKERS',
 status:'PASS, restricted source-width noncomposition only',
 checker_pins:{c341:pins.c341,c386:pins.c386},
 dual_widths:{a:widths(A),b:widths(B)},dual_overlap:0,fixtures,cases};
if(process.argv[2])fs.writeFileSync(path.resolve(process.argv[2]),
 JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
