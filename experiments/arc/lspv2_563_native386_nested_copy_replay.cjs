#!/usr/bin/env node
'use strict';
/*
 * LSPV-2/563, original-/386 nested paid-DEF copy chain.
 * This is a REFERENCE CONSTRUCTOR, never the authoritative historical checker.
 * Run at repository root:
 *   node experiments/arc/lspv2_563_native386_nested_copy_replay.cjs
 * Uses unchanged archived /386 checker with actual Node.js subprocesses.
 */
const fs=require('node:fs');
const cp=require('node:child_process');
const path=require('node:path');
const os=require('node:os');
const crypto=require('node:crypto');
const assert=require('node:assert/strict');
const root=process.cwd();
const seedPath=path.join(root,'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json');
const checkerPath=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const gitblob=b=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex');
const sha256=b=>crypto.createHash('sha256').update(b).digest('hex');
assert.equal(gitblob(fs.readFileSync(seedPath)),'318c52d99977ea4e91bc8554051138a700c1dc94');
assert.equal(gitblob(fs.readFileSync(checkerPath)),'338305c0ce101704205e57543756b8127074a986');
const seed=JSON.parse(fs.readFileSync(seedPath,'utf8'));
const clone=x=>JSON.parse(JSON.stringify(x));
const canon=c=>[...new Set(c)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
function produce(k){
  assert(Number.isSafeInteger(k)&&k>=0&&k<=64);
  let packet=clone(seed);
  for(let j=1;j<=k;j++)packet.gate_defs.push([j,8+j,7+j,7+j]);
  const facets=[{kind:'DEF',c:canon([1,-8]),parents:[],gate:0}];
  for(let j=1;j<=k;j++)facets.push({kind:'DEF',c:canon([7+j,-(8+j)]),parents:[],gate:j});
  for(let j=1;j<=k;j++)facets.push({kind:'DEF',c:canon([8+j,-(7+j)]),parents:[],gate:j});
  facets.push({kind:'DEF',c:canon([8,-1,-4]),parents:[],gate:0});
  const rec=packet.records.slice(0,17).concat(facets);
  function add(Ai,Bi,pivot){
    const A=rec[Ai].c,B=rec[Bi].c;
    assert(A.includes(pivot)&&B.includes(-pivot),'oriented RES ports');
    const c=canon([...A.filter(x=>x!==pivot),...B.filter(x=>x!==-pivot)]);
    assert(!c.some(x=>c.includes(-x)),'tautological RES');
    rec.push({kind:'RES',c,parents:[Ai,Bi],pivot});
    return rec.length-1;
  }
  const first=17,forward=j=>17+j,backward=j=>17+k+j,finish=17+2*k+1;
  let tail=add(first,7,1);
  for(let j=1;j<=k;j++)tail=add(tail,forward(j),-(7+j));
  for(let j=k;j>=1;j--)tail=add(tail,backward(j),-(8+j));
  tail=add(tail,finish,-8);
  assert.deepEqual(rec[tail].c,seed.records[7].c,'restored SOURCE signed clause');
  const delta=4+4*k;
  for(let j=17;j<seed.records.length;j++){
    const r=clone(seed.records[j]);
    r.parents=r.parents.map(i=>i>=17?i+delta:i);
    if(j===20)r.parents=r.parents.map(i=>i===7?tail:i);
    rec.push(r);
  }
  packet.records=rec;
  const nres=rec.filter(x=>x.kind==='RES').length;
  const ndef=rec.filter(x=>x.kind==='DEF').length;
  packet.summary={source:17,resolution:nres,def_views:ndef,paid_gates:1+k,paid_total:nres+1+k,live_records:rec.length};
  assert.equal(nres,30+2*k);
  assert.equal(ndef,2+2*k);
  assert.equal(rec.length,49+4*k);
  assert.equal(packet.summary.paid_total,31+3*k);
  const seen=new Set(),stack=[rec.length-1];
  while(stack.length){
    const j=stack.pop();
    if(seen.has(j))continue;
    seen.add(j);
    stack.push(...rec[j].parents);
  }
  for(let j=17;j<17+delta;j++)assert(seen.has(j),'inserted paid/facet step must reach terminal');
  return packet;
}
function native(file){
  const r=cp.spawnSync(process.execPath,[checkerPath,file],{encoding:'utf8',timeout:15000});
  return {accepted:r.status===0,status:r.status,stdout:r.stdout,stderr:r.stderr,
          parsed:r.status===0?JSON.parse(r.stdout.trim().split('\n').at(-1)):null};
}
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2-563-'));
const positives=[],negative={};
try{
  for(const k of [0,1,2,4,8]){
    const packet=produce(k);
    const bytes=Buffer.from(JSON.stringify(packet)+'\n','utf8');
    const filename=path.join(tmp,'k'+k+'.json');
    fs.writeFileSync(filename,bytes);
    if([1,2,4].includes(k)){
      const committed=path.join(root,'results/raw/arc/2026-11-11_1212_LSPV2_563_ACCEPTED_NESTED_COPY_K'+k+'.json');
      assert(fs.readFileSync(committed).equals(bytes),'committed accepted bytes changed: k='+k);
    }
    const result=native(filename);
    assert(result.accepted,'original complete checker rejected k='+k+' '+result.stderr);
    assert.equal(result.parsed.paid,31+3*k);
    assert.equal(result.parsed.negativeTests,11);
    positives.push({k,bytes:bytes.length,sha256:sha256(bytes),blob:gitblob(bytes),
      records:packet.records.length,paid:31+3*k,assertions:result.parsed.assertions,
      native_original_full_cli:true,negativeTests:11});
  }
  const corruptions={
    wrong_source:p=>p.records[7].c[0]=-p.records[7].c[0],
    unknown_owner:p=>p.records[18].gate=9876,
    forward_parent:p=>p.records[23].parents[0]=1000,
    corrupt_copy_port:p=>p.records[18].c=[1,-9],
    undercharge:p=>p.summary.paid_total--,
    missing_copy_owner:p=>p.gate_defs.pop(),
    wrong_terminal:p=>p.records.at(-1).c=[7]
  };
  for(const [label,edit] of Object.entries(corruptions)){
    const p=produce(2);
    edit(p);
    const f=path.join(tmp,label+'.json');
    fs.writeFileSync(f,JSON.stringify(p)+'\n');
    const r=native(f);
    negative[label]=!r.accepted;
    assert(negative[label],'original checker accepted hostile: '+label);
  }
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
console.log(JSON.stringify({id:'LSPV-2/563',status:'PASS',scope:'archived /386 original complete CLI only',
  checker_git_blob:gitblob(fs.readFileSync(checkerPath)),
  seed_git_blob:gitblob(fs.readFileSync(seedPath)),positives,negative,
  unknown_historical_mixed_rules:'OPEN',P_versus_NP:'OPEN'},null,2));
