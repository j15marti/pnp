#!/usr/bin/env node
'use strict';
// LSPV-4/569. Execute from any complete j15marti/pnp checkout:
// node experiments/arc/lspv4_569_free_facet_reference_width.cjs
// Unmodified original /386 CLI, pinned by checker SHA256, is run for each packet.
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const crypto=require('node:crypto'),assert=require('node:assert/strict'),child=require('node:child_process');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const source=path.join(root,'results/raw/arc/2026-11-12_1031_LSPV4_566_W38_P45_AREA958_NATIVE386_ACCEPTED.json');
const expectedChecker='22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113';
assert.equal(crypto.createHash('sha256').update(fs.readFileSync(checker)).digest('hex'),expectedChecker);
const f=JSON.parse(fs.readFileSync(source,'utf8'));
const clone=x=>JSON.parse(JSON.stringify(x));
const at=f.records.findIndex(r=>r.kind==='RES'),end=f.records.length-1;
assert.equal(at,23);assert.equal(end,57);assert.equal(f.summary.paid_total,38);
const facet=clone(f.records.find(r=>r.kind==='DEF'));
assert.deepEqual(facet,{kind:'DEF',c:[1,-8],parents:[],gate:0});
const digits=n=>String(n).length;
function variant(k,where){
  const d=clone(f);d.records=[];
  for(let i=0;i<f.records.length;i++){
    if(i===where)for(let j=0;j<k;j++)d.records.push(clone(facet));
    const r=clone(f.records[i]);r.parents=r.parents.map(p=>p>=where?p+k:p);d.records.push(r);
  }
  d.summary.def_views+=k;d.summary.live_records+=k;return d;
}
const scan=d=>d.records.reduce((a,r)=>a+r.parents.reduce((s,p)=>s+Buffer.byteLength(JSON.stringify(d.records[p].c)),0),0);
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv4-569-'));
let results=[],hostiles=[];
function native(d,name,expect){
  const file=path.join(tmp,'packet.json');fs.writeFileSync(file,JSON.stringify(d));
  const p=child.spawnSync(process.execPath,[checker,file],{encoding:'utf8',maxBuffer:16*1024*1024});
  assert.equal(p.status===0,expect,'original CLI mismatch '+name+': '+p.stderr);
  return expect?JSON.parse(p.stdout.trim()):p.stderr.slice(0,400);
}
try{
  for(const k of [0,1,32,43,44,64,76,77,85,256,1024]){
    const a=variant(k,at),b=variant(k,end);
    const oa=native(a,'front_'+k,true),ob=native(b,'late_'+k,true);
    const predicted=f.records.reduce((s,r)=>s+(r.kind==='RES'?r.parents.reduce((t,p)=>t+(p>=at?digits(p+k)-digits(p):0),0):0),0);
    const bytesA=Buffer.byteLength(JSON.stringify(a)),bytesB=Buffer.byteLength(JSON.stringify(b));
    assert.equal(bytesA-bytesB,predicted);assert.equal(scan(a),790);assert.equal(scan(b),790);
    for(const o of [oa,ob]){assert.equal(o.paid,38);assert.equal(o.negativeTests,11)}
    results.push({k,front_bytes:bytesA,late_bytes:bytesB,delta_bytes:predicted,
      logical_work:38,parent_clause_scan_proxy:790,assertions_each:oa.assertions});
  }
  const f77=variant(77,at);
  const bad=[
    ['SOURCE_CLAUSE_FORGED',d=>d.records[0].c=[-7]],
    ['FREE_FACET_FORGED',d=>d.records[at].c=[7]],
    ['TERMINAL_PIVOT_FORGED',d=>d.records.at(-1).pivot=123456],
    ['FORWARD_REFERENCE',d=>d.records.at(-1).parents[0]=d.records.length],
    ['UNDERPAID_TOTAL',d=>d.summary.paid_total--],
    ['WRONG_FREE_FACET_COUNT',d=>d.summary.def_views--]];
  for(const [name,mutate] of bad){const d=clone(f77);mutate(d);hostiles.push({name,rejected:true,stderr:native(d,name,false)})}
  console.log(JSON.stringify({run:'LSPV-4/569',node:process.version,originalCheckerSHA256:expectedChecker,results,hostiles},null,2));
}finally{fs.rmSync(tmp,{recursive:true,force:true})}
