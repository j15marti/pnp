#!/usr/bin/env node
'use strict';
/* LSPV-5/498 independent red-team audit.
   This isolates the distinction between (a) a sound SOURCE/RES proof relative
   to the source embedded in a packet and (b) a verifier for a caller-supplied
   SAT instance. It also OS-replays the current LSPV-1/583 reference checker
   and the unchanged archived /386 checker on the newest LSPV-3/580 and
   LSPV-4/553 accepted packets. */
const assert=require('node:assert/strict');
const cp=require('node:child_process');
const crypto=require('node:crypto');
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'../..');
const sha256=b=>crypto.createHash('sha256').update(b).digest('hex');
const stable=x=>JSON.stringify(x);
const sortClause=v=>{
  assert(Array.isArray(v));
  assert(v.every(x=>Number.isSafeInteger(x)&&x!==0));
  assert.equal(new Set(v).size,v.length);
  assert(!v.some(x=>v.includes(-x)));
  return [...v].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
};
const canonRoot=src=>src.map(s=>{
  assert.equal(typeof s.id,'string');
  assert.deepEqual(sortClause(s.clause),s.clause);
  return {id:s.id,clause:[...s.clause]};
});
const models=(src,n)=>{
  let count=0;
  for(let a=0;a<2**n;a++) if(src.every(s=>s.clause.some(l=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0)))) count++;
  return count;
};
const resolve=(a,b,p)=>{
  assert(Number.isSafeInteger(p)&&p!==0);
  assert(a.includes(p)&&b.includes(-p));
  return sortClause([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
};
function verifyEmbedded(pkt){
  const source=new Map();
  for(const s of canonRoot(pkt.external)){
    assert(!source.has(s.id)); source.set(s.id,s.clause);
  }
  const all=new Map(); let paid=0;
  for(const c of pkt.components){
    assert.equal(new Set(c.source_view).size,c.source_view.length);
    c.source_view.forEach(id=>assert(source.has(id)));
    for(const r of c.records){
      assert(!all.has(r.id)); assert(!r.ctx||r.ctx.length===0);
      if(r.kind==='SOURCE'){
        assert(c.source_view.includes(r.source_id));
        assert.deepEqual(r.clause,source.get(r.source_id));
      }else if(r.kind==='RES'){
        assert.equal(r.parents.length,2); r.parents.forEach(id=>assert(all.has(id)));
        assert.deepEqual(r.clause,resolve(all.get(r.parents[0]),all.get(r.parents[1]),r.pivot)); paid++;
      }else assert.fail('unsupported component opcode');
      all.set(r.id,r.clause);
    }
  }
  for(const r of pkt.joins){
    assert(!all.has(r.id)); assert.equal(r.kind,'RES'); assert.equal(r.parents.length,2);
    r.parents.forEach(id=>assert(all.has(id)));
    assert.deepEqual(r.clause,resolve(all.get(r.parents[0]),all.get(r.parents[1]),r.pivot));
    all.set(r.id,r.clause); paid++;
  }
  assert(pkt.joins.length>0); assert.deepEqual(all.get(pkt.joins.at(-1).id),[]);
  return {accepted:true,paid};
}
function verifyForTarget(target,pkt){
  assert.equal(stable(canonRoot(target)),stable(canonRoot(pkt.external)),'caller target / packet source mismatch');
  return verifyEmbedded(pkt);
}
const packet={
  external:[{id:'s0',clause:[1,2]},{id:'s1',clause:[-2]},{id:'s2',clause:[-1]}],
  components:[
    {source_view:['s0','s1'],records:[
      {id:'a0',kind:'SOURCE',source_id:'s0',clause:[1,2]},
      {id:'a1',kind:'SOURCE',source_id:'s1',clause:[-2]},
      {id:'a2',kind:'RES',parents:['a0','a1'],pivot:2,clause:[1]}]},
    {source_view:['s2'],records:[{id:'b0',kind:'SOURCE',source_id:'s2',clause:[-1]}]}
  ],
  joins:[{id:'j0',kind:'RES',parents:['a2','b0'],pivot:1,clause:[]}]
};
const satTarget=[{id:'t0',clause:[1]}];
const embedded=verifyEmbedded(packet);
assert.equal(models(packet.external,2),0);
assert.equal(models(satTarget,1),1);
let mismatch=null;
try{verifyForTarget(satTarget,packet);}catch(e){mismatch=e.message;}
assert.match(mismatch,/caller target \/ packet source mismatch/);
assert.deepEqual(verifyForTarget(packet.external,packet),embedded);

function run(rel,args=[]){
  const p=path.join(root,rel);
  const out=cp.spawnSync(process.execPath,[p,...args],{cwd:root,encoding:'utf8',timeout:15000,maxBuffer:2**20});
  return {rel,status:out.status,signal:out.signal,stdout:out.stdout,stderr:out.stderr};
}
const replay583=run('experiments/arc/lspv1_583_source_view_join.cjs');
assert.equal(replay583.status,0,replay583.stderr); const parsed583=JSON.parse(replay583.stdout); assert.equal(parsed583.all_passed,true);
const checker='experiments/arc/lspv2_386_independent_verify.js';
const p580='results/raw/arc/2026-11-11_1624_LSPV3_580_TERMINAL_LIVE_IDEMPOTENT_BATCH_PACKET.json';
const p553='results/raw/arc/2026-11-11_1636_LSPV4_553_PRUNED_SHARED_NATIVE_W43.json';
const p567ok='results/raw/arc/2026-11-11_1608_LSPV2_567_ACCEPTED_GAUGE_M8_W32.json';
const p567no='results/raw/arc/2026-11-11_1608_LSPV2_567_CLI_REJECTED_CORE_ACCEPTED_GAUGE_M1_W32.json';
const replay567ok=run(checker,[p567ok]); assert.equal(replay567ok.status,0,replay567ok.stderr); const parsed567ok=JSON.parse(replay567ok.stdout);
const replay567no=run(checker,[p567no]); assert.notEqual(replay567no.status,0); assert(replay567no.stderr.includes('even mismatch'));
const replay580=run(checker,[p580]); assert.equal(replay580.status,0,replay580.stderr); const parsed580=JSON.parse(replay580.stdout);
const replay553=run(checker,[p553]); assert.equal(replay553.status,0,replay553.stderr); const parsed553=JSON.parse(replay553.stdout);
const out={
  id:'LSPV5-498',status:'PROVED/RESTRICTED repaired source-binding lemma; COMPUTATIONAL exact OS replay',
  target_binding_counterexample:{caller_target_models:models(satTarget,1),embedded_root_models:models(packet.external,2),embedded_verifier_accepts:embedded.accepted,naive_wrapper_would_misattribute_unsat:true,bound_wrapper_rejection:mismatch},
  repaired_condition:'canonical caller source bytes must equal canonical packet.external bytes before embedded proof verification; thereafter unequal component subsets are sound when every SOURCE occurrence and every cross-edge is checked',
  os_replays:{
    lspv1_583:{exit:replay583.status,stdout_bytes:Buffer.byteLength(replay583.stdout),stdout_sha256:sha256(Buffer.from(replay583.stdout)),all_passed:parsed583.all_passed,total_extensions:parsed583.total_source_extensions_checked},
    lspv2_567:{mask8_exit:replay567ok.status,mask8_paid:parsed567ok.paid,mask8_assertions:parsed567ok.assertions,mask1_exit:replay567no.status,mask1_diagnostic:'even mismatch'},
    lspv3_580:{exit:replay580.status,paid:parsed580.paid,records:parsed580.records,assertions:parsed580.assertions,negative_tests:parsed580.negativeTests},
    lspv4_553:{exit:replay553.status,paid:parsed553.paid,records:parsed553.records,assertions:parsed553.assertions,negative_tests:parsed553.negativeTests}
  },
  scope:{historical_full_R_mix341_authenticated:false,p2_d1:'OPEN',p2_c3:'OPEN',p2_b1:'OPEN',p2_b2_b3:'OPEN separately',p_vs_np:'OPEN'}
};
console.log(JSON.stringify(out,null,2));
