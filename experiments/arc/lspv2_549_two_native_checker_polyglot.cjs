'use strict';
// LSPV-2/549. Reproduce a checker-language polyglot using *unchanged*
// archived /341 and /386 original checkers as independent OS Node processes.
// The intersection of accepted JSON does not establish a shared inference calculus.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),
      crypto=require('node:crypto'),cp=require('node:child_process'),
      assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const f341='experiments/arc/lspv2_341_mixed_tseitin_min_dag.js';
const c341='experiments/arc/lspv2_341_independent_verify.js';
const c386='experiments/arc/lspv2_386_independent_verify.js';
const archived='results/raw/arc/2026-11-10_2124_LSPV3_561_ARCHIVED_386_NATIVE_PACKET.json';
const pin={
 [f341]:'4081022e8a3841d79f751a3d3a7a10decbb026da',
 [c341]:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
 [c386]:'338305c0ce101704205e57543756b8127074a986',
 [archived]:'d0fa96a155672f8f6a6a3428eacafa15e79b9e88'
};
const sha256=b=>crypto.createHash('sha256').update(b).digest('hex');
const blob=b=>crypto.createHash('sha1').update(
 Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex');
for(const [p,expected] of Object.entries(pin)){
 const b=fs.readFileSync(path.join(root,p));
 assert.equal(blob(b),expected,'historical source changed: '+p);
}
const prod=cp.spawnSync(process.execPath,[path.join(root,f341)],{
 encoding:'utf8',maxBuffer:32000000,timeout:30000});
assert.equal(prod.status,0,'original producer '+prod.stderr);
const f=JSON.parse(prod.stdout).fixtures[0];
assert.equal(f.graph.name,'K4');
assert.equal(f.clauses.length,16);
assert.equal(f.proof.length,15);
const a=JSON.parse(fs.readFileSync(path.join(root,archived),'utf8'));
assert.equal(a.summary.paid_total,50);
assert.equal(a.records.length,69);
const dual={fixtures:[f],spec:a.spec,gate_defs:a.gate_defs,
 records:a.records,summary:{length:1,...a.summary}};
const packet=Buffer.from(JSON.stringify(dual)+'\n');
assert.equal(packet.length,7533,'canonical packet has changed');
const packetPath='results/raw/arc/2026-11-10_2212_LSPV2_549_DUAL_NATIVE_POLYGLOT_PACKET.json';
fs.writeFileSync(path.join(root,packetPath),packet);
const scratch=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2-549-'));
function check(name,data){
 const filepath=path.join(scratch,'test.json');
 fs.writeFileSync(filepath,JSON.stringify(data)+'\n');
 const r=cp.spawnSync(process.execPath,[path.join(root,name),filepath],{
 encoding:'utf8',maxBuffer:32000000,timeout:30000});
 if(r.error)throw r.error;
 if(r.status!==0)return {accepted:false,diagnostic:r.stderr.slice(0,180)};
 const output=JSON.parse(r.stdout);
 return {accepted:true,checks:name===c341?output.checks:output.assertions,
 paid:name===c341?output.cases[0].proofNodes:output.paid};
}
const clone=x=>JSON.parse(JSON.stringify(x));
const cases=[
 ['dual',x=>x,true,true],
 ['wrong_341_AND3',x=>{x.fixtures[0].proof[0].table^=1;return x},false,true],
 ['wrong_386_RES_pivot',x=>{x.records[20].pivot=999;return x},true,false],
 ['missing_341_fixtures',x=>{delete x.fixtures;return x},false,true],
 ['missing_386_records',x=>{delete x.records;return x},true,false],
 ['341_summary_array',x=>{x.summary=[null];return x},true,false],
 ['386_summary_without_length',x=>{delete x.summary.length;return x},false,true],
 ['wrong_341_source',x=>{x.fixtures[0].clauses[0].literals[0]*=-1;return x},false,true],
 ['wrong_386_source',x=>{x.records[0].c=[-7];return x},true,false]
];
try{
 const rows=[];
 for(const [name,mutate,expected341,expected386] of cases){
  const d=mutate(clone(dual)),out341=check(c341,d),out386=check(c386,d);
  assert.equal(out341.accepted,expected341,'341 mismatch: '+name);
  assert.equal(out386.accepted,expected386,'386 mismatch: '+name);
  rows.push({name,out341,out386});
 }
 const raw={id:'LSPV-2/549',status:'COMPUTATIONAL',
  authority:'Two unchanged distinct ORIGINAL archived checkers via OS Node subprocess; NOT a full R_mix341 checker',
  original_blobs:pin,packet_sha256:sha256(packet),packet_bytes:packet.length,
  packet_path:packetPath,cases:rows,
  note:'Common accepted JSON envelope does not mean one checker validates a RES/AND3 cross-inference. Source formulas and node semantics remain independently checked.',
  cost_units:{checker_341_AND3_XOR_nodes:15,checker_386_RES_nodes:49,
   checker_386_paid_gate_owners:1,
   no_composable_joint_cost_justified:true},
  open:['P2-D1','P2-C3','P2-B1','P2-B2/B3']};
 const resultPath='results/raw/arc/2026-11-10_2212_LSPV2_549_DUAL_NATIVE_NODE_REPLAY_RAW.json';
 fs.writeFileSync(path.join(root,resultPath),JSON.stringify(raw,null,2)+'\n');
 console.log(JSON.stringify(raw,null,2));
}finally{fs.rmSync(scratch,{recursive:true,force:true});}
