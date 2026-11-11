#!/usr/bin/env node
'use strict';
// LSPV-1/578: independently executable exact archived /386 raw-core to CLI closure.
// Run from repository root:
//   node experiments/arc/lspv1_578_raw_core_cli_closure.cjs [raw-output.json]
// Requires Node >= 22, no third-party dependencies. Original checker is NEVER modified.
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const vm = require('node:vm');
const cp = require('node:child_process');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '../..');
const checker = path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const original = fs.readFileSync(checker,'utf8');
const pinnedBlob = '338305c0ce101704205e57543756b8127074a986';
const pinnedSHA256 = '22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113';
const sha = x => crypto.createHash('sha256').update(x).digest('hex');
const gitBlob = x => crypto.createHash('sha1').update('blob '+Buffer.byteLength(x)+'\0').update(x).digest('hex');
assert.equal(gitBlob(original), pinnedBlob, 'original Git blob changed');
assert.equal(sha(original), pinnedSHA256, 'original SHA-256 changed');
const originalCore = vm.runInNewContext(original+'\ncheckProof;', {
  require, process:{argv:['node',checker]}, console, structuredClone
}, {filename:checker,timeout:2000});
const clone = x => JSON.parse(JSON.stringify(x));
const key = c => [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
const taut = c => c.some(x=>c.includes(-x));
function buildK4(){
  const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]], charge=[1,0,0,0], guard=7;
  const records=[];
  for(let v=0;v<4;v++){
    const vs=edges.map(([a,b],i)=>a===v||b===v?i+1:0).filter(Boolean);
    for(let j=0;j<8;j++){
      const bs=[j&1,(j>>1)&1,(j>>2)&1];
      if(bs.reduce((x,y)=>x+y,0)%2!==charge[v])
        records.push({kind:'SOURCE',c:key(vs.map((x,i)=>bs[i]?-x:x).concat(-guard)),parents:[],source:v});
    }
  }
  records.push({kind:'SOURCE',c:[guard],parents:[],source:-1});
  const seen=new Map(records.map((r,i)=>[JSON.stringify(r.c),i]));
  let active=records.map((_,i)=>i);
  for(let pivot=1;pivot<=7;pivot++){
    const pos=active.filter(i=>records[i].c.includes(pivot));
    const neg=active.filter(i=>records[i].c.includes(-pivot));
    const newIds=[];
    for(const i of pos)for(const j of neg){
      const c=key(records[i].c.filter(x=>x!==pivot).concat(records[j].c.filter(x=>x!==-pivot)));
      if(taut(c))continue;
      const k=JSON.stringify(c);
      if(!seen.has(k)){
        seen.set(k,records.length);
        records.push({kind:'RES',c,parents:[i,j],pivot});
      }
      newIds.push(seen.get(k));
    }
    active=[...new Set(active.filter(i=>!records[i].c.includes(pivot)&&!records[i].c.includes(-pivot)).concat(newIds))];
    if(seen.has('[]'))break;
  }
  assert.ok(seen.has('[]'),'DP did not derive contradiction');
  const keep=new Set([...Array(17).keys()]);
  const todo=[seen.get('[]')];
  while(todo.length){const i=todo.pop();if(keep.has(i))continue;keep.add(i);todo.push(...records[i].parents);}
  const ids=[...keep].sort((a,b)=>a-b), index=new Map(ids.map((i,j)=>[i,j]));
  const out=ids.map(i=>({...records[i],parents:records[i].parents.map(j=>index.get(j))}));
  assert.deepEqual(out.at(-1).c,[]);
  const res=out.filter(x=>x.kind==='RES').length;
  return {spec:{h:4,edges,charge,guard},gate_defs:[],records:out,
    summary:{source:17,def_views:0,resolution:res,paid_gates:0,paid_total:res,live_records:out.length}};
}
function core(p){try{return {accept:true,result:originalCore(p,{control:true})};}catch(e){return {accept:false,error:String(e.message)};}}
function repair(raw){
  const p=JSON.parse(raw), verified=core(p);
  if(!verified.accept)throw new Error('not core accepted: '+verified.error);
  const n=p.summary.live_records;
  assert.ok(Number.isSafeInteger(n)&&n>0);
  if(!Array.isArray(p.records))p.records=Array.from({length:n},(_,i)=>p.records[i]);
  assert.equal(p.records.length,n);
  if(p.gate_defs.length===0){
    const E=p.spec.edges.length,guard=p.spec.guard;
    const z=(E+1===guard)?E+2:E+1;
    p.gate_defs.push([0,z,1,2]);
    p.summary.paid_gates++;
    p.summary.paid_total++;
  }
  if(p.records.at(-1).pivot===999999){
    const last=p.records.at(-1);last.pivot=-last.pivot;last.parents.reverse();
  }
  assert.ok(core(p).accept,'repaired mathematical core rejected');
  return p;
}
const base=buildK4();
assert.equal(base.summary.live_records,49);assert.equal(base.summary.resolution,32);
const oneOwner=clone(base);oneOwner.gate_defs=[[0,8,1,2]];
oneOwner.summary.paid_gates=1;oneOwner.summary.paid_total++;
const sentinel=clone(base);sentinel.spec.guard=999999;
for(const r of sentinel.records){
  r.c=key(r.c.map(x=>x===7?999999:x===-7?-999999:x));
  if(r.kind==='RES'&&Math.abs(r.pivot)===7)r.pivot=Math.sign(r.pivot)*999999;
}
assert.equal(sentinel.records.at(-1).pivot,999999);
const asObject=(p,length)=>{const q=clone(p);q.records=Object.assign(Object.fromEntries(q.records.map((r,i)=>[String(i),r])),{length});return q;};
const cases=[
  ['array_zero_owner',base],
  ['array_one_owner',oneOwner],
  ['array_sentinel_zero_owner',sentinel],
  ['object_string_length_sentinel',asObject(sentinel,String(sentinel.records.length))],
  ['object_fractional_length_sentinel',asObject(sentinel,sentinel.records.length-0.5)],
  ['object_one_owner',asObject(oneOwner,oneOwner.records.length)]
];
const badSource=clone(base);badSource.records[0].c=[123456];
const badParent=clone(base);badParent.records.at(-1).parents[0]=999;
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-lspv1-578-'));
const rows=[];
try{
  function cli(name,p){
    const file=path.join(dir,name+'.json');fs.writeFileSync(file,JSON.stringify(p)+'\n');
    const r=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',timeout:8000,maxBuffer:2*1024*1024});
    return {accept:r.status===0&&!r.error,status:r.status,
      result:r.status===0?JSON.parse(r.stdout):null,
      error:r.status!==0?(r.stderr.match(/Error: [^\n]+|TypeError: [^\n]+/)||['unknown'])[0]:null,
      sha256:sha(fs.readFileSync(file))};
  }
  for(const [name,p] of cases){
    const before=core(p);assert.ok(before.accept,name+' core');
    const initial=cli(name+'-before',p);
    const fixed=repair(JSON.stringify(p));
    const after=cli(name+'-after',fixed);
    assert.ok(after.accept,name+' post-repair CLI');
    assert.equal(after.result.paid,p.summary.paid_total+(p.gate_defs.length===0?1:0));
    assert.equal(after.result.res,p.summary.resolution);
    assert.equal(after.result.sources,17);
    assert.equal(after.result.negativeTests,11);
    assert.equal(fixed.records.length,p.summary.live_records);
    assert.equal(fixed.records.at(-1).c.length,0);
    rows.push({name,core_before:before.accept,cli_before:initial.accept,
      before_error:initial.error,original_records_array:Array.isArray(p.records),
      original_length:p.records.length,original_owners:p.gate_defs.length,
      original_pivot:p.records[p.summary.live_records-1].pivot,
      W_core:p.summary.paid_total,W_cli:after.result.paid,W_increment:after.result.paid-p.summary.paid_total,
      post_pivot:fixed.records.at(-1).pivot,sha256_before:initial.sha256,
      sha256_after:after.sha256,cli_assertions:after.result.assertions});
  }
  for(const [name,p] of [['forged_source',badSource],['future_parent',badParent]]){
    const before=core(p);assert.equal(before.accept,false,name+' core');
    assert.throws(()=>repair(JSON.stringify(p)),/not core accepted/);
    const native=cli('negative-'+name,p);assert.equal(native.accept,false);
    rows.push({name,core_before:before.accept,cli_before:native.accept,repaired:false,error:before.error});
  }
}finally{fs.rmSync(dir,{recursive:true,force:true});}
const result={marker:'LSPV1_578_RAW_CORE_TO_CLI_CLOSURE',date:'2026-11-11',
  original_checker_git_blob:pinnedBlob,original_checker_sha256:pinnedSHA256,
  node:process.version,method:'deterministic K4 DP, real unchanged-original checker OS subprocess, independently extracted original core',
  no_randomness:true,seed:0,original_k4:{h:4,E:6,source:17,resolution:32,records:49},
  cases:rows,positive:6,negative:2,
  outcome:'PASS: every original core-accepted raw JSON specimen admits a same-source native full-CLI proof with delta W in {0,1}; not a full R_mix341 claim'};
const out=JSON.stringify(result,null,2)+'\n';
if(process.argv[2])fs.writeFileSync(process.argv[2],out);
process.stdout.write(out);
