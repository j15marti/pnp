#!/usr/bin/env node
'use strict';
/* LSPV-2/553. Byte-exact native /386 free-facet prefix. Generator ONLY.
 * Run from repository root:
 * node experiments/arc/lspv2_553_zero_paid_facet_prefix.cjs --emit=/tmp/lspv2_553 --out=/tmp/lspv2_553.json
 */
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const cp=require('node:child_process'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const checkerPath='experiments/arc/lspv2_386_independent_verify.js';
const seedPath='results/raw/arc/2026-11-11_0203_LSPV1_568_K4_DP_CLI29.json';
const checkerBlob='338305c0ce101704205e57543756b8127074a986';
const seedBlob='e3eb2a46857776089ab83f4ad50159ef622d2869';
const sha256=b=>crypto.createHash('sha256').update(b).digest('hex');
function gitBlob(b){return crypto.createHash('sha1')
  .update(Buffer.from('blob '+b.length+'\0','utf8')).update(b).digest('hex');}
function readPinned(p,sha){const b=fs.readFileSync(p);assert.equal(gitBlob(b),sha,
  'historical original blob changed: '+p);return b;}
const originalChecker=readPinned(checkerPath,checkerBlob);
const originalSeed=readPinned(seedPath,seedBlob);
const seed=JSON.parse(originalSeed.toString('utf8'));
assert.deepEqual(seed.summary,{source:17,def_views:0,resolution:28,
  paid_gates:1,paid_total:29,live_records:45});
assert.deepEqual(seed.gate_defs,[[0,8,1,4]]);
assert.equal(seed.records[0].kind,'SOURCE');
assert.equal(seed.records.at(-1).c.length,0);
const copy=obj=>JSON.parse(JSON.stringify(obj));
const sourceBinding=d=>JSON.stringify({spec:d.spec,
  source:d.records.filter(r=>r.kind==='SOURCE')});
const sourceSHA256=sha256(Buffer.from(sourceBinding(seed),'utf8'));
function prefix(k){
  assert.ok(Number.isSafeInteger(k)&&k>=0&&k<=100000);
  const d=copy(seed),f=()=>({kind:'DEF',gate:0,c:[1,-8],parents:[]});
  d.records=[...Array.from({length:k},f),
    ...d.records.map(r=>({...r,parents:r.parents.map(x=>x+k)}))];
  d.summary.def_views+=k;d.summary.live_records+=k;
  assert.equal(d.summary.paid_total,29);
  assert.equal(sourceBinding(d),sourceBinding(seed),'signed SOURCE changed');
  assert.equal(d.records.at(-1).c.length,0);
  assert.equal(d.records.length,45+k);
  return d;
}
const cases=[];
for(const k of [0,1,2,4,16,64])
  cases.push({label:'accept_k'+k,k,expected:true,packet:prefix(k)});
const hostile=(name,mutate)=>{
  const d=prefix(2);mutate(d);
  cases.push({label:'reject_'+name,k:2,expected:false,packet:d});
};
hostile('invalid_facet',d=>d.records[0].c=[1,8]);
hostile('undefined_gate',d=>d.records[0].gate=999);
hostile('wrong_parent_reindex',d=>d.records[19].parents[0]=0);
hostile('nonempty_facet_parents',d=>d.records[1].parents=[0]);
hostile('altered_signed_SOURCE',d=>d.records[2].c=[-7]);
hostile('incorrect_payment',d=>d.summary.paid_total=30);
hostile('wrong_facet_counter',d=>d.summary.def_views=1);
hostile('deleted_paid_owner',d=>d.gate_defs=[]);
hostile('wrong_terminal_clause',d=>d.records.at(-1).c=[1]);
hostile('wrong_record_counter',d=>d.summary.live_records=46);
function nativeCLI(packet,file){
  fs.writeFileSync(file,packet);
  const r=cp.spawnSync(process.execPath,[checkerPath,file],
    {encoding:'utf8',maxBuffer:1024*1024,timeout:15000});
  assert.equal(r.error,undefined,'OS Node subprocess did not start');
  let verdict=null;
  if(r.status===0)verdict=JSON.parse(r.stdout.trim().split(/\r?\n/).at(-1));
  return {ok:r.status===0,exitCode:r.status,verdict,
    error:r.status===0?null:(r.stderr||r.stdout).slice(0,320)};
}
const flags=process.argv.slice(2);
const emit=flags.find(s=>s.startsWith('--emit='))?.slice(7);
const outFile=flags.find(s=>s.startsWith('--out='))?.slice(6);
if(emit)fs.mkdirSync(emit,{recursive:true});
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-553-'));
try{
  const trials=cases.map(({label,k,expected,packet})=>{
    const bytes=Buffer.from(JSON.stringify(packet),'utf8');
    const result=nativeCLI(bytes,path.join(tmp,label+'.json'));
    assert.equal(result.ok,expected,'native full CLI mismatch '+label);
    if(result.ok){
      assert.equal(result.verdict.paid,29,'paid charge '+label);
      assert.equal(result.verdict.sources,17,'signed source '+label);
      assert.equal(result.verdict.res,28,'RES count '+label);
      assert.equal(result.verdict.records,45+k,'record count '+label);
      assert.equal(result.verdict.negativeTests,11,'native CLI tests '+label);
    }
    if(emit)fs.writeFileSync(path.join(emit,label+'.json'),bytes);
    return {label,k,expected,accepted:result.ok,bytes:bytes.length,
      sha256:sha256(bytes),records:packet.records.length,
      paid:packet.summary.paid_total,defViews:packet.summary.def_views,
      sourceSHA256:sha256(Buffer.from(sourceBinding(packet),'utf8')),native:result};
  });
  const summary={run:'LSPV-2/553',
    mode:'actual OS Node original archived /386 CLI',
    checkerBlob,seedBlob,checkerSHA256:sha256(originalChecker),
    seedSHA256:sha256(originalSeed),sourceSHA256,
    full_R_mix341_authenticated:false,
    positive:trials.filter(t=>t.accepted).length,
    negative:trials.filter(t=>!t.accepted).length,
    all16Expected:trials.every(t=>t.accepted===t.expected),trials};
  assert.equal(summary.positive,6);assert.equal(summary.negative,10);
  if(outFile){fs.mkdirSync(path.dirname(outFile),{recursive:true});
    fs.writeFileSync(outFile,JSON.stringify(summary,null,2)+'\n');}
  console.log(JSON.stringify(summary,null,2));
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
