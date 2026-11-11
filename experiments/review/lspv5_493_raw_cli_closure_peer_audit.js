#!/usr/bin/env node
'use strict';
/*
 * LSPV-5/493 independent red-team audit of archived /386 raw-core -> CLI closure.
 * Runs exact published peer programs in temporary mirrors, invokes the pinned
 * historical checker as OS subprocess, and independently challenges JSON
 * container/length shapes plus all eleven wrapper mutations.
 */
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const cp=require('node:child_process'),crypto=require('node:crypto'),vm=require('node:vm');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const wallStart=process.hrtime.bigint();
const sha256=b=>crypto.createHash('sha256').update(b).digest('hex');
const gitblob=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
const clone=x=>JSON.parse(JSON.stringify(x));
function pinned(rel,sha){
  let b=fs.readFileSync(path.join(root,rel));
  if(gitblob(b)!==sha && b.length && b.at(-1)===10 && gitblob(b.subarray(0,-1))===sha)b=b.subarray(0,-1);
  assert.equal(gitblob(b),sha,'pinned blob mismatch '+rel);return b;
}
const files={
 checker:['experiments/arc/lspv2_386_independent_verify.js','338305c0ce101704205e57543756b8127074a986'],
 packet575:['results/raw/arc/2026-11-11_0900_LSPV1_575_BRIDGE_GUARDED_DP_NATIVE_ACCEPTED.json','d5de0f477cd736ec5fd7b01be18350f9cb594fd2'],
 seed561:['results/raw/arc/2026-11-11_1012_LSPV2_561_ACCEPTED_LIVE_PAID_RES_FANOUT.json','bf7cd9851e881fef47e617eb99f0c3b2e83bb0a0'],
 seed563:['results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json','08aa169b5db49b2ddd1cb5a9b6890fcc3b790916'],
 seed546:['results/raw/arc/2026-11-11_0936_LSPV4_546_AREA_SCHEDULE_ACCEPTED.json','0a428dc5afa7154cad3ae9a1f7816eb285d7a6b9'],
 packet548:['results/raw/arc/2026-11-11_1136_LSPV4_548_INPLACE_BYTE_SAFE_ACCEPTED.json','72f4430fb36ee58100ec6d81d89de95e93bee0f8']
};
function runMirror(scriptRel,scriptSha,requirements,args=[],opts={}){
  const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv5-493-mirror-'));
  try{
    let script=pinned(scriptRel,scriptSha);if(opts.transform)script=Buffer.from(opts.transform(script.toString('utf8')));
    const target=path.join(tmp,scriptRel);
    fs.mkdirSync(path.dirname(target),{recursive:true});fs.writeFileSync(target,script);
    for(const k of requirements){
      const [rel,sha]=files[k],out=path.join(tmp,rel);
      fs.mkdirSync(path.dirname(out),{recursive:true});fs.writeFileSync(out,pinned(rel,sha));
    }
    const r=cp.spawnSync(process.execPath,[target,...args],{cwd:tmp,encoding:'utf8',timeout:120000,maxBuffer:32*1024*1024});
    assert.equal(r.error,undefined,scriptRel+' launch');
    if(opts.allowFailure)return {status:r.status,stdout:r.stdout,stderr:r.stderr};
    assert.equal(r.status,0,scriptRel+'\n'+r.stderr);
    return JSON.parse(r.stdout);
  }finally{fs.rmSync(tmp,{recursive:true,force:true});}
}
const peer577=runMirror('experiments/arc/lspv1_577_386_cli_arraylike_counterexample.cjs',
  '52d8cdf6a8fe6ffe90a8c2d24908aa8c2c911df8',['checker','packet575']);
const peer578=runMirror('experiments/arc/lspv1_578_raw_core_cli_closure.cjs',
  '62e1ebda21d7e24081e4eba8f376be63ffea9cd7',['checker']);
const peer562=runMirror('experiments/arc/lspv2_562_native386_cli_safe_quotient.cjs',
  '26a9a42b1cf5234cc06c07d374d8050d3b93648a',['checker','seed561']);
const peer575Failure=runMirror('experiments/arc/lspv3_575_charge_compensated_source_symmetry.cjs',
  '713e6e7ec80972f43b11b8f5eff281f198d27670',['checker','seed563'],[],{allowFailure:true});
assert.equal(peer575Failure.status,1);assert.match(peer575Failure.stderr,/x\.s\[0\]/);
const peer575=runMirror('experiments/arc/lspv3_575_charge_compensated_source_symmetry.cjs',
  '713e6e7ec80972f43b11b8f5eff281f198d27670',['checker','seed563'],[],{
    transform:s=>s.replace('rows.filter(x=>x.s[0]!==0)','rows.filter(x=>x.sigma[0]!==0)')
  });
const peer548=runMirror('experiments/arc/lspv4_548_inplace_register_exact.cjs',
  'e3b3ebbf5adffc2ba5a153b6bd6afe6af034e11b',['checker','seed546','packet548']);

const checkerBytes=pinned(...files.checker),checkerText=checkerBytes.toString('utf8');
const originalCore=vm.runInNewContext(checkerText+'\ncheckProof;',{
  require,process:{argv:['node','checker']},console,structuredClone
},{timeout:3000});
function core(p){try{return {accept:true,result:originalCore(p,{control:true})}}catch(e){return {accept:false,error:e.message}}}
function cli(p,name,tmp){
  const f=path.join(tmp,name+'.json');fs.writeFileSync(f,JSON.stringify(p)+'\n');
  const r=cp.spawnSync(process.execPath,[path.join(root,files.checker[0]),f],{encoding:'utf8',timeout:30000,maxBuffer:2e6});
  return {accept:r.status===0,status:r.status,error:r.status===0?null:(r.stderr||'').split(/\r?\n/).find(x=>/Error|TypeError/.test(x))||'reject'};
}
function repair(p){
  p=clone(p);assert(core(p).accept);
  const n=p.summary.live_records;
  assert(Number.isSafeInteger(n)&&n>0);
  if(!Array.isArray(p.records))p.records=Array.from({length:n},(_,i)=>p.records[i]);
  if(p.gate_defs.length===0){
    const E=p.spec.edges.length,z=E+1===p.spec.guard?E+2:E+1;
    p.gate_defs.push([0,z,1,2]);p.summary.paid_gates++;p.summary.paid_total++;
  }
  if(p.records.at(-1).pivot===999999){p.records.at(-1).pivot=-999999;p.records.at(-1).parents.reverse()}
  assert(core(p).accept);return p;
}
const base=JSON.parse(pinned(...files.packet575).toString('utf8'));
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv5-493-hostile-'));
const lengthShapes=[],gateShapes=[];
try{
  for(const length of [103,'103','103.0','1.03e2',102.5,102.00000000000001]){
    const p=clone(base);p.records=Object.assign(Object.fromEntries(p.records.map((r,i)=>[String(i),r])),{length});
    const before=core(p),native=cli(p,'len-'+lengthShapes.length,tmp),fixed=repair(p),after=cli(fixed,'fixed-'+lengthShapes.length,tmp);
    assert(before.accept);assert(!native.accept);assert(after.accept);
    lengthShapes.push({length,decoded_type:typeof length,core:true,cli_before:false,cli_after:true,W_before:p.summary.paid_total,W_after:fixed.summary.paid_total});
  }
  for(const [name,value] of [
    ['numeric_object',{'0':base.gate_defs[0],length:1}],
    ['nonempty_string','[0,17,1,2]'],['number',1],['true',true]
  ]){
    const p=clone(base);p.gate_defs=value;const c=core(p),n=cli(p,'gate-'+name,tmp);
    assert(!c.accept);assert(!n.accept);gateShapes.push({name,core:false,cli:false,error:c.error});
  }
}finally{fs.rmSync(tmp,{recursive:true,force:true})}

const mutations=[
 ['terminal_pivot',o=>{o.records.at(-1).pivot=999999}],
 ['terminal_clause',o=>{o.records.at(-1).c=[123456]}],
 ['first_source',o=>{o.records[0].c=[-o.spec.guard]}],
 ['owner_shift',o=>{o.gate_defs.shift()}],
 ['future_parent',o=>{o.records.at(-1).parents[0]=o.records.length+1}],
 ['underpay',o=>{o.summary.paid_total--}],
 ['charge_flip',o=>{o.spec.charge[0]^=1}],
 ['terminal_kind',o=>{o.records.at(-1).kind='SOURCE'}],
 ['duplicate_edge',o=>{o.spec.edges[0]=o.spec.edges[1].slice()}],
 ['zero_literal',o=>{o.records[0].c=[0]}],
 ['guard_floor',o=>{o.spec.guard=o.spec.edges.length}]
];
const mutationRows=mutations.map(([name,fn])=>{const p=clone(base),before=JSON.stringify(p);fn(p);const c=core(p);
  assert.notEqual(JSON.stringify(p),before,name+' unexpectedly no-op on positive control');assert(!c.accept,name+' core accepted');
  return {name,rejected:true,error:c.error}});

assert.equal(peer577.cases.length,7);assert.equal(peer578.positive,6);assert.equal(peer578.negative,2);
assert.deepEqual(peer562.results.filter(x=>x.accepted).map(x=>x.paid),[32,30,29]);
assert.equal(peer575.accepted,192);assert.equal(peer575.charge_moving,144);assert.equal(peer575.negative_rejections,6);
assert.equal(peer548.certifiedNoFiveAnyReuse.visited,185340);assert.equal(peer548.reordered.byteSafe,6);
const out={
 marker:'LSPV5_493_RAW_CLI_CLOSURE_PEER_AUDIT',date_pst:'2026-11-11 11:48 PST',
 checker_git_blob:files.checker[1],checker_sha256:sha256(checkerBytes),
 target:'Theorem /578.1 and corrected /577 full-CLI iff for archived /386 only',
 independent_hostiles:{coercive_length_shapes:lengthShapes,nonarray_gate_defs:gateShapes,all_cli_mutations:mutationRows},
 exact_peer_replays:{
  lspv1_577:{cases:peer577.cases.length,core_accepts:peer577.cases.filter(x=>x.core_accept).length,cli_accepts:peer577.cases.filter(x=>x.cli_accept).length},
  lspv1_578:{positive:peer578.positive,negative:peer578.negative,rows:peer578.cases.length},
  lspv2_562:{accepted:peer562.results.filter(x=>x.accepted).length,rejected:peer562.results.filter(x=>!x.accepted).length,paid:peer562.results.filter(x=>x.accepted).map(x=>x.paid)},
  lspv3_575:{published_runner_exit:peer575Failure.status,published_runner_error:'TypeError: x.s is undefined in final charge_moving summary',diagnostic_one_token_repair:true,accepted:peer575.accepted,charge_moving:peer575.charge_moving,composition_checks:peer575.group_composition,hostile_rejections:peer575.negative_rejections},
  lspv4_548:{cap5:peer548.certifiedNoFiveAnyReuse,reordered:peer548.reordered,checker_paid:peer548.originalCheckerOS[0].paid}
 },
 resource_accounting:{
  parent_wall_seconds:Number(process.hrtime.bigint()-wallStart)/1e9,
  parent_cpu:process.resourceUsage(),
  parent_memory_at_finish:process.memoryUsage(),
  child_peak_rss:'not observed; Node subprocess exit/output and logical checker counts only',
  phases:['pin/read inputs','mirror exact peer runners','OS checker subprocesses','hostile container replay','eleven-mutation core replay','JSON output']
 },
 result:'VALIDATED/RESTRICTED theorem; REPRODUCIBILITY FALSIFIER: published LSPV-3/575 runner exits 1 after its checker work because final summary reads x.s instead of stored x.sigma. Core acceptance implies gate_defs is an Array; records Array is not implied. Reification plus optional paid owner and signed terminal-pivot repair closes the exact archived /386 core-to-CLI gap at delta W in {0,1}.',
 firewall:'Not complete historical R_mix341; no P2-D1/P2-C3/P2-B1 closure; no memory or P-versus-NP lower bound.'
};
const dest=process.argv[2];if(dest)fs.writeFileSync(dest,JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify(out,null,2));
