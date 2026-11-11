#!/usr/bin/env node
'use strict';
// LSPV-4/540. Native /386 paid-owner cone overlap and RES sharing audit.
// Run in repo: node experiments/arc/lspv4_540_native_paid_owner_cone_audit.cjs
const fs=require('fs'), path=require('path'),vm=require('vm'),crypto=require('crypto'),assert=require('assert');
const root=path.resolve(__dirname,'../..');
const source=fs.readFileSync(path.join(root,'experiments/arc/lspv2_386_independent_verify.js'),'utf8');
function cli(buf){
  let messages=[];
  const ctx={require:n=>n==='fs'?{readFileSync:()=>buf}:n==='crypto'?crypto:assert,
    process:{argv:['node','original.js','certificate.json']},
    console:{log:s=>messages.push(s)},
    structuredClone:global.structuredClone||((x)=>JSON.parse(JSON.stringify(x)))};
  vm.runInNewContext(source,ctx,{timeout:60000});
  assert.strictEqual(messages.length,1);
  let outcome=JSON.parse(messages[0]);
  assert.strictEqual(outcome.negativeTests,11);
  return outcome;
}
function cone(rs,i){
  let out=new Set(),stack=[i];
  while(stack.length){
    const j=stack.pop();
    if(out.has(j))continue;
    assert(j>=0&&j<rs.length);
    out.add(j);
    stack.push(...rs[j].parents);
  }
  return out;
}
function union(A,B){return new Set([...A,...B]);}
function intersection(A,B){return new Set([...A].filter(i=>B.has(i)));}
function charge(rs,C){
  let R=0,owners=new Set(),views=0,sources=0;
  for(const i of C){const r=rs[i];
    if(r.kind==='RES')R++;
    if(r.kind==='DEF'){owners.add(r.gate);views++;}
    if(r.kind==='SOURCE')sources++;
  }
  return {res:R,owners:[...owners].sort((a,b)=>a-b),views,sources,W:R+owners.size};
}
function audit(kind,file){
  const raw=fs.readFileSync(path.join(root,file)),p=JSON.parse(raw),outcome=cli(raw),rs=p.records;
  const sourceN=rs.filter(r=>r.kind==='SOURCE').length;
  const views=rs.filter(r=>r.kind==='DEF').length, R=rs.filter(r=>r.kind==='RES').length;
  assert.strictEqual(outcome.paid,R+p.gate_defs.length);
  assert.strictEqual(outcome.sources,sourceN);
  assert.strictEqual(outcome.records,rs.length);
  let depth=[];for(const r of rs)depth.push(r.kind==='RES'?1+Math.max(...r.parents.map(i=>depth[i])):0);
  const sink=charge(rs,cone(rs,rs.length-1));
  const result={kind,sha256:crypto.createHash('sha256').update(raw).digest('hex'),bytes:raw.length,
    paid:outcome.paid,records:rs.length,source:sourceN,freeFacets:views,res:R,
    owners:p.gate_defs.length,refs:2*R,span:depth.at(-1),
    assertions:outcome.assertions,originalCLIMutations:outcome.negativeTests,
    sink,globallyPaidOutsideSink:outcome.paid-sink.W};
  if(kind==='owner'){
    const A=cone(rs,45),B=cone(rs,47),I=intersection(A,B),U=union(A,B);
    const a=charge(rs,A),b=charge(rs,B),i=charge(rs,I),u=charge(rs,U);
    assert.strictEqual(I.size,0);
    assert.deepStrictEqual(a.owners,[0]);
    assert.deepStrictEqual(b.owners,[0]);
    assert.strictEqual(a.W,2);assert.strictEqual(b.W,2);
    assert.strictEqual(i.W,0);assert.strictEqual(u.W,3);
    assert.strictEqual(outcome.paid,31);
    assert.strictEqual(result.globallyPaidOutsideSink,3);
    result.ownerOverlap={first:a,second:b,sharedRecordCount:I.size,intersection:i,union:u,
      naiveRecordOverlapCharge:a.W+b.W-i.W,correctOwnerAwareCharge:u.W,overcharge:1};
  }else{
    const parents=rs.at(-1).parents;
    const A=cone(rs,parents[0]),B=cone(rs,parents[1]),I=intersection(A,B),U=union(A,B);
    const a=charge(rs,A),b=charge(rs,B),i=charge(rs,I),u=charge(rs,U);
    assert.strictEqual(outcome.paid,50);
    assert.strictEqual(a.W,30);assert.strictEqual(b.W,30);
    assert.strictEqual(i.W,11);assert.strictEqual(u.W,49);
    assert.strictEqual(a.W+b.W-i.W+1,outcome.paid);
    result.reconvergence={first:a,second:b,commonRecords:I.size,intersection:i,union:u,
      paidTerminal:1,naiveSum:a.W+b.W+1,corrected:a.W+b.W-i.W+1,overcharge:i.W};
  }
  return result;
}
const result={run:'LSPV-4/540',checkerBlob:'338305c0ce101704205e57543756b8127074a986',
  status:'PROVED/RESTRICTED + COMPUTATIONAL',PvsNP:'OPEN',
  fixtures:[
    audit('owner','results/raw/arc/2026-11-11_0336_LSPV4_540_OWNER_FACET_CROSS_CONE_ACCEPTED.json'),
    audit('shared','results/raw/arc/2026-11-11_0336_LSPV4_540_SHARED_K4_ORIGINAL_COPY.json')
  ]};
console.log(JSON.stringify(result,null,2));
