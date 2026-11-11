#!/usr/bin/env node
'use strict';
// LSPV-4/543 reproducible OS Node test of the unchanged archived /386 checker.
// Run from repository root: node experiments/arc/lspv4_543_native_inmemory_firewall.cjs
// Outputs deterministic JSON; high-level JS array-slot accounting is a source-code
// theorem, not a process RSS or heap-byte measurement.
const fs=require('fs');
const os=require('os');
const path=require('path');
const assert=require('assert/strict');
const {spawnSync}=require('child_process');
const root=path.resolve(__dirname,'../..');
const original=path.join(__dirname,'lspv2_386_independent_verify.js');
const seedPath=path.join(root,'results/raw/arc/2026-11-11_0336_LSPV4_540_OWNER_FACET_CROSS_CONE_ACCEPTED.json');
assert.ok(fs.existsSync(original),'pinned original checker missing');
const seed=JSON.parse(fs.readFileSync(seedPath,'utf8'));
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv4-543-'));
const cases=[0,1,16,128,512];
function extend(k){
  const d=JSON.parse(JSON.stringify(seed));
  const facets=Array.from({length:k},()=>({kind:'DEF',c:[1,-8],parents:[],gate:0}));
  d.records=facets.concat(d.records.map(r=>({...r,parents:r.parents.map(n=>n+k)})));
  d.summary.def_views+=k;
  d.summary.live_records+=k;
  return d;
}
function checkNative(d, tag){
  const f=path.join(temp,tag+'.json');
  fs.writeFileSync(f,JSON.stringify(d));
  const p=spawnSync(process.execPath,[original,f],{encoding:'utf8',timeout:25000,maxBuffer:2*1024*1024});
  const ok=p.status===0 && !p.error;
  let output=null;
  if(ok)output=JSON.parse(p.stdout.trim().split('\n').filter(Boolean).at(-1));
  return {ok,output,error:p.error?String(p.error):(ok?null:p.stderr.trim().slice(0,500))};
}
const rows=[], bad=[];
try{
  for(const k of cases){
    const d=extend(k),c=checkNative(d,'positive_'+k);
    assert.equal(c.ok,true,'Original checker rejected a positive: '+k+' '+c.error);
    assert.equal(c.output.paid,31);assert.equal(c.output.res,30);
    assert.equal(c.output.def,1);assert.equal(c.output.records,49+k);
    assert.equal(c.output.negativeTests,11);
    rows.push({
      k,bytes:Buffer.byteLength(JSON.stringify(d)),records:d.records.length,
      def_views:d.summary.def_views,paid:d.summary.paid_total,
      ref_count:2*d.summary.resolution,positive_cli:true,
      original_checker_negative_tests:c.output.negativeTests,
      assertion_groups:c.output.assertions,
      source_code_min_simultaneous_reference_entries:2*d.records.length
    });
  }
  for(const name of ['bad_paid','bad_facet','bad_parent','bad_source','no_owner']){
    const d=extend(16);
    if(name==='bad_paid')d.summary.paid_total--;
    if(name==='bad_facet')d.records[0].c=[-2,8];
    if(name==='bad_parent')d.records.at(-1).parents[0]=d.records.length+1;
    if(name==='bad_source')d.spec.charge[0]=0;
    if(name==='no_owner')d.gate_defs=[];
    const c=checkNative(d,'invalid_'+name);
    assert.equal(c.ok,false,'Original checker accepted a hostile case: '+name);
    bad.push({name,rejected:true});
  }
  console.log(JSON.stringify({
    scope:'Unchanged original /386 CLI in OS Node subprocess, if executed',
    checker:'experiments/arc/lspv2_386_independent_verify.js',
    seed:'results/raw/arc/2026-11-11_0336_LSPV4_540_OWNER_FACET_CROSS_CONE_ACCEPTED.json',
    rows,bad,all_passed:true,
    caveat:'Simultaneous JS array slot result follows from source code, not measured physical peak RSS or a SAT lower bound.'
  },null,2));
}finally{fs.rmSync(temp,{recursive:true,force:true})}
