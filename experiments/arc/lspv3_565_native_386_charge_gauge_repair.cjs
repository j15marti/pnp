'use strict';
/*
 * LSPV-3/565, archived /386 source-charge gauge and full-CLI repair.
 * Run: node experiments/arc/lspv3_565_native_386_charge_gauge_repair.cjs
 * Uses the UNMODIFIED archived /386 checker as the sole acceptance oracle
 * for the restricted /386 system. Does not define historical R_mix341 syntax.
 */
const fs=require('fs');
const path=require('path');
const os=require('os');
const crypto=require('crypto');
const vm=require('vm');
const cp=require('child_process');
const assert=require('assert');
const root=path.resolve(__dirname,'../..');
const entries={
  checker:['experiments/arc/lspv2_386_independent_verify.js','338305c0ce101704205e57543756b8127074a986'],
  seed:['results/raw/arc/2026-11-10_2324_LSPV3_563_ARCHIVED_386_NESTED_OWNER_PACKET.json','08aa169b5db49b2ddd1cb5a9b6890fcc3b790916'],
  broken:['results/raw/arc/2026-11-10_2303_LSPV1_565_ARCHIVED_386_RELABEL_CORE_ACCEPT_CLI_REJECT.json','5f8236b622fe340e1d485dd32be4b987cc158c84']
};
function blobHash(data) {
  return crypto.createHash('sha1').update(Buffer.from('blob '+data.length+'\0')).update(data).digest('hex');
}
function load(name) {
  const [file,expected]=entries[name],data=fs.readFileSync(path.join(root,file));
  assert.strictEqual(blobHash(data),expected,'Git blob source changed: '+name);
  return name==='checker'?data.toString('utf8'):JSON.parse(data.toString('utf8'));
}
function clone(o){return JSON.parse(JSON.stringify(o))}
function key(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}
function gaugeTo(P,target){
  const Q=clone(P),h=P.spec.h,E=P.spec.edges.length;
  assert.strictEqual(target.length,h);
  assert(target.every(x=>x===0||x===1));
  assert.strictEqual(target.reduce((a,b)=>a^b,0),1);
  const boundary=P.spec.charge.map((x,i)=>x^target[i]);
  assert.strictEqual(boundary.reduce((a,b)=>a^b,0),0);
  const adj=Array.from({length:h},()=>[]);
  P.spec.edges.forEach(([u,v],e)=>{adj[u].push([v,e]);adj[v].push([u,e]);});
  const prev=Array(h).fill(-1),from=Array(h).fill(-1),q=[0];
  prev[0]=0;
  for(let k=0;k<q.length;k++){
    for(const [v,e] of adj[q[k]])if(prev[v]<0){prev[v]=q[k];from[v]=e;q.push(v);}
  }
  assert.strictEqual(q.length,h,'requires connected source graph');
  const flips=Array(E).fill(0);
  for(let v=1;v<h;v++)if(boundary[v])for(let w=v;w!==0;w=prev[w])flips[from[w]]^=1;
  const delta=Array(h).fill(0);
  P.spec.edges.forEach(([u,v],e)=>{delta[u]^=flips[e];delta[v]^=flips[e];});
  assert.deepStrictEqual(delta,boundary,'incidence solve');
  function lit(l){return Math.abs(l)<=E&&flips[Math.abs(l)-1]?-l:l;}
  Q.spec.charge=target.slice();
  Q.gate_defs=Q.gate_defs.map(([id,z,a,b])=>[id,z,lit(a),lit(b)]);
  Q.records=Q.records.map(r=>({...r,c:key(r.c.map(lit)),...(r.kind==='RES'?{pivot:lit(r.pivot)}:{})}));
  return {packet:Q,flips};
}
function nativeCore(checkerSource){
  // The archived original checker is evaluated WITHOUT any rule modification.
  // Only an export is appended, and no CLI input is supplied.
  const ctx={require,process:{argv:['node','original']},structuredClone:globalThis.structuredClone,console};
  vm.runInNewContext(checkerSource+'\nglobalThis.__native={checkProof};',ctx,{filename:'original_386.js'});
  return ctx.__native.checkProof;
}
function invokeCli(P,checkerFile){
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-565-'));
  const tmp=path.join(dir,'native_packet.json');
  try{
    fs.writeFileSync(tmp,JSON.stringify(P));
    const r=cp.spawnSync(process.execPath,[checkerFile,tmp],{encoding:'utf8',timeout:30000,maxBuffer:1024*1024});
    let output;
    if(r.status===0){output=JSON.parse(r.stdout.trim());assert.strictEqual(output.negativeTests,11);}
    return {accepted:r.status===0,status:r.status,output:output||null,reason:r.status===0?null:String(r.stderr||r.error).trim().slice(0,400)};
  }finally{fs.rmSync(dir,{recursive:true,force:true});}
}
function coreResult(checkProof,P,control){
  try{return {accepted:true,result:checkProof(P,{control})};}
  catch(e){return {accepted:false,reason:String(e.message)};}
}
function run(){
  const source=load('checker'),base=load('seed'),broken=load('broken');
  const checkerFile=path.join(root,entries.checker[0]),checkProof=nativeCore(source);
  const orbit=[];
  for(let bits=0;bits<16;bits++){
    const target=Array.from({length:4},(_,i)=>(bits>>i)&1);
    if(target.reduce((a,b)=>a^b,0)!==1)continue;
    const g=gaugeTo(base,target),c=coreResult(checkProof,g.packet,false),p=coreResult(checkProof,g.packet,true),cli=invokeCli(g.packet,checkerFile);
    assert(c.accepted,'all orbit instances must pass core');
    assert.strictEqual(c.result.paid,53);
    assert.strictEqual(p.accepted,Boolean(target[0]),'native checkProof control asymmetry');
    assert.strictEqual(cli.accepted,Boolean(target[0]),'native CLI orbit asymmetry');
    orbit.push({charge:target,flipped_edges:g.flips.flatMap((v,i)=>v?[i+1]:[]),
      core:c.accepted,control:p.accepted,cli:cli.accepted,
      paid:53,records:g.packet.records.length,bytes:JSON.stringify(g.packet).length,
      checker_assertions:cli.output&&cli.output.assertions||null,
      rejection:p.reason||null});
  }
  assert.strictEqual(orbit.length,8);
  const g=gaugeTo(broken,[1,0,0,0]),r=g.packet;
  const before=invokeCli(broken,checkerFile),after=invokeCli(r,checkerFile);
  assert(!before.accepted&&after.accepted,'old full CLI must fail; repaired CLI must pass');
  assert.strictEqual(after.output.paid,50);
  const controls=[
    ['wrong_source_charge',d=>{d.spec.charge[1]^=1}],
    ['forged_original_source',d=>{d.records.find(r=>r.kind==='SOURCE').c[0]*=-1}],
    ['unflipped_def_input',d=>{d.gate_defs[0][2]*=-1}],
    ['unflipped_res_pivot',d=>{d.records.find(r=>r.kind==='RES'&&Math.abs(r.pivot)===1).pivot*=-1}],
    ['unsorted_source',d=>{let c=d.records.find(r=>r.kind==='SOURCE').c;[c[0],c[1]]=[c[1],c[0]]}],
    ['underpaid_owner',d=>{d.summary.paid_total--}],
    ['forward_parent',d=>{let i=d.records.findIndex(r=>r.kind==='RES');d.records[i].parents[0]=d.records.length}],
    ['invalid_facet_owner',d=>{d.records.find(r=>r.kind==='DEF').gate=999}]
  ].map(([name,mutate])=>{
    const x=clone(r);mutate(x);const a=coreResult(checkProof,x,false);
    assert(!a.accepted,'hostile control accidentally accepted: '+name);
    return {name,rejected:true,reason:a.reason};
  });
  const out={
    scope:'ORIGINAL ARCHIVED /386 checker, NOT historical R_mix341',
    source_blob:entries.checker[1],seed_blob:entries.seed[1],charge0_blob:entries.broken[1],
    status:'PASS',orbit,cli_repair:{
      source_before:broken.spec.charge,source_after:r.spec.charge,flipped_edges:g.flips.flatMap((v,i)=>v?[i+1]:[]),
      core_before:coreResult(checkProof,broken,false),core_after:coreResult(checkProof,r,false),
      original_cli:before.accepted,repaired_cli:after.accepted,
      paid:r.summary.paid_total,records:r.records.length,bytes:JSON.stringify(r).length,
      original_assertions:after.output.assertions},
    hostiles:controls,independent_OS_subprocess:true,
    unchanged_native_checker:true,p_vs_np:'OPEN',full_R_mix341:'OPEN'
  };
  console.log(JSON.stringify(out,null,2));
}
run();
