'use strict';
// LSPV-4/581, original /341 witness-vs-paid-work resource firewall.
// Reproduce symbolic ledger: node experiments/arc/lspv4_581_witness_verifier_ledger.cjs
// Replay original source in a complete checkout:
// node experiments/arc/lspv4_581_witness_verifier_ledger.cjs --native
// node experiments/arc/lspv4_581_witness_verifier_ledger.cjs --native --out /tmp/audit581.json
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const assert=require('node:assert/strict');
const vm=require('node:vm'),cp=require('node:child_process');
const ROOT=path.resolve(__dirname,'../..');
const CHECKER='experiments/arc/lspv2_341_independent_verify.js';
const PACKET='results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json';
const EXPECT_CHECKER='fcb7d4ced8f922de14c0bda16263a8cc7853e8e0';
const EXPECT_PACKET='fe27fe1011d0021e721ccaeb747ed58da65d7464';
const sha=b=>crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');
function ledger(V,essential) {
 assert(Number.isInteger(V)&&V>=4&&V%2===0);
 assert(Number.isInteger(essential)&&essential>=0&&essential<=4*V);
 const E=3*V/2, M=4*V, W=M-1;
 return {V,E,clauses:M,paid:W,parent_applications:2*W,
         essential,witness_payload_characters:essential*E,
         witness_phase_clauseSat_calls:essential*M,
         source_table_clauseSat_calls:8*M,
         witness_phase_asserts_per_witness:M+1};
}
const observedBridgeless=[
 ['K4',4],['K33',6],['CUBE',8],['PETERSEN',10],
 ['PRISM6',12],['PRISM16',32]
].map(([fixture,V])=>({fixture,...ledger(V,4*V)}));
for(const x of observedBridgeless) {
 assert.equal(x.witness_payload_characters,6*x.V*x.V);
 assert.equal(x.witness_phase_clauseSat_calls,16*x.V*x.V);
 assert.equal(x.paid,4*x.V-1);
 assert.equal(x.source_table_clauseSat_calls,32*x.V);
}
const bridgeBounds={fixture:'BRIDGE_K4x2',V:10,
  essential:'e in [0,39], exact e requires original packet replay',
  witness_payload:'15*e',witness_clause_calls:'40*e',
  source_table_clause_calls:320,paid:39};
const audit={status:'PROVED/RESTRICTED by original-checker code inspection; finite arithmetic COMPUTATIONAL',
  source:{checker:CHECKER,checker_blob:EXPECT_CHECKER,packet:PACKET,packet_blob:EXPECT_PACKET},
  theorem:'For an accepted bridgeless cubic /341 fixture with V vertices and all 4V essential deletion witnesses, raw witness digit payload=6V^2, witness validation clauseSat calls=16V^2, source table clauseSat calls=32V, paid inference records=4V-1.',
  models:'Unchanged /341 verifier implementation only; no bound for minimal verifier, arbitrary R_mix341, SAT solver or shared calculus.',
  controls:['bridged fixture has e<4V','zero-essential synthetic e=0','compact alternate witness encoding is not part of pinned checker','shared reference work and native logical W counted separately'],
  bridgeless:observedBridgeless,bridge:bridgeBounds,
  native_replay:'not run'};
assert.equal(observedBridgeless.reduce((n,x)=>n+x.paid,0),282);
assert.equal(observedBridgeless.reduce((n,x)=>n+x.witness_payload_characters,0),8304);
assert.equal(observedBridgeless.reduce((n,x)=>n+x.witness_phase_clauseSat_calls,0),22144);
assert.equal(ledger(10,0).witness_phase_clauseSat_calls,0);
assert.equal(ledger(10,39).witness_phase_clauseSat_calls,1560);
function originalRun(buf,checkerBuf) {
 const packet=JSON.parse(buf.toString('utf8'));
 const auditCounters={phase:null,sourceCalls:0,witnessCalls:0};
 let src=checkerBuf.toString('utf8');
 function replaceOne(before,after) {
  assert(src.includes(before),'checker instrumentation anchor absent: '+before.slice(0,25));
  assert.equal(src.split(before).length,2,'nonunique source anchor');
  src=src.replace(before,after);
 }
 replaceOne('function clauseSat(c,bits){',
  "function clauseSat(c,bits){ if(globalThis.__lspvAudit.phase==='source') globalThis.__lspvAudit.sourceCalls++; if(globalThis.__lspvAudit.phase==='witness') globalThis.__lspvAudit.witnessCalls++;");
 replaceOne('  const sup=incid[v].slice(),tab=Array.from',
  "  globalThis.__lspvAudit.phase='source';\n  const sup=incid[v].slice(),tab=Array.from");
 replaceOne('  src.set(c.id,{kind:"factor",support:sup,table:tab});',
  '  src.set(c.id,{kind:"factor",support:sup,table:tab});globalThis.__lspvAudit.phase=null;');
 replaceOne(' let essential=0;',
  " let essential=0;globalThis.__lspvAudit.phase='witness';");
 replaceOne(' assert(essential===f.properties.essential,"essential count");',
  ' globalThis.__lspvAudit.phase=null;assert(essential===f.properties.essential,"essential count");');
 let output='';
 vm.runInNewContext(src,{
  __lspvAudit:auditCounters,require:n=>{
   assert.equal(n,'fs');
   return {readFileSync:()=>buf.toString('utf8')};
  },process:{argv:['node',CHECKER,PACKET]},
  console:{log:x=>{output+=x;}}
 },{filename:CHECKER,timeout:30000});
 const checker=JSON.parse(output);
 assert.equal(checker.checks,30714);
 const rows=packet.fixtures.map(f=>{
  const V=f.graph.n,e=f.deleted.filter(d=>d.assignment!==null).length;
  assert.equal(f.clauses.length,4*V);
  assert.equal(f.graph.edges.length,3*V/2);
  assert.equal(f.proof.length,4*V-1);
  for(const d of f.deleted)if(d.assignment!==null)assert.equal(d.assignment.length,3*V/2);
  return {fixture:f.graph.name,...ledger(V,e),graph_bridgeless:checker.cases.find(c=>c.name===f.graph.name).bridgeless};
 });
 assert.equal(auditCounters.sourceCalls,rows.reduce((n,r)=>n+r.source_table_clauseSat_calls,0));
 assert.equal(auditCounters.witnessCalls,rows.reduce((n,r)=>n+r.witness_phase_clauseSat_calls,0));
 for(const r of rows)if(r.graph_bridgeless)assert.equal(r.essential,4*r.V);
 return {rows,observed_source_clauseSat_calls:auditCounters.sourceCalls,
  observed_witness_clauseSat_calls:auditCounters.witnessCalls,
  original_checker_assertion_groups:checker.checks};
}
if(process.argv.includes('--native')) {
 const C=fs.readFileSync(path.join(ROOT,CHECKER));
 const P=fs.readFileSync(path.join(ROOT,PACKET));
 assert.equal(sha(C),EXPECT_CHECKER);assert.equal(sha(P),EXPECT_PACKET);
 const instrumented=originalRun(P,C);
 const os=cp.spawnSync(process.execPath,[path.join(ROOT,CHECKER),path.join(ROOT,PACKET)],
   {encoding:'utf8',maxBuffer:16*1024*1024});
 assert.equal(os.status,0,'original OS checker rejected: '+os.stderr.slice(0,300));
 assert.equal(JSON.parse(os.stdout).checks,30714);
 audit.native_replay={mode:'actual node subprocess original checker plus source-hooked VM',
  original_os_checker_accepted:true,...instrumented};
}
const outIndex=process.argv.indexOf('--out');
if(outIndex!==-1){assert(process.argv[outIndex+1]);fs.writeFileSync(process.argv[outIndex+1],JSON.stringify(audit,null,2)+'\n');}
console.log(JSON.stringify({result:'PASS',bridgeless_fixtures:6,
  six_witness_payload_chars:8304,six_witness_clausesat_calls:22144,
  prism16_calls:16384,native:!!(audit.native_replay&&audit.native_replay!=='not run')},null,2));
