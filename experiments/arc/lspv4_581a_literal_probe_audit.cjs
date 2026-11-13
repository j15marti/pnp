'use strict';
// LSPV-4/581A: exact 7-fixture /341 essential-witness literal-probe auditor.
// node experiments/arc/lspv4_581a_literal_probe_audit.cjs --out /tmp/lspv4_581a.json
// node experiments/arc/lspv4_581a_literal_probe_audit.cjs --native
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const assert=require('node:assert/strict'),cp=require('node:child_process');
const root=path.resolve(__dirname,'../..');
const cpPath='experiments/arc/lspv2_341_independent_verify.js';
const dataPath='results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json';
const expectedChecker='fcb7d4ced8f922de14c0bda16263a8cc7853e8e0';
const expectedPacket='fe27fe1011d0021e721ccaeb747ed58da65d7464';
const blob=b=>crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');
const checker=fs.readFileSync(path.join(root,cpPath));
const packet=fs.readFileSync(path.join(root,dataPath));
assert.equal(blob(checker),expectedChecker,'original checker hash');
assert.equal(blob(packet),expectedPacket,'original packet hash');
const data=JSON.parse(packet.toString('utf8'));
function satWithProbes(lits,bits) {
 let probes=0;
 for(const lit of lits) {
  probes++;
  if((lit>0&&bits[lit-1]===1)||(lit<0&&bits[-lit-1]===0))
   return {sat:true,probes};
 }
 return {sat:false,probes};
}
const rows=[];
for(const f of data.fixtures) {
 const V=f.graph.n,E=f.graph.edges.length,M=f.clauses.length;
 assert.equal(E*2,3*V,'cubic E');
 assert.equal(M,4*V,'four local SOURCE clauses');
 assert.equal(f.proof.length,4*V-1,'paid record count');
 assert.equal(f.deleted.length,M,'source witness count');
 const groups=Array.from({length:V},(_,v)=>f.clauses.filter(c=>c.vertex===v));
 for(const g of groups) {
  assert.equal(g.length,4);
  const order=g[0].literals.map(x=>Math.abs(x)).join(',');
  assert(g.every(c=>c.literals.map(x=>Math.abs(x)).join(',')===order),'source literal ordering differs');
  const patterns=g.map(c=>c.literals.map(x=>x<0?1:0));
  assert.equal(new Set(patterns.map(x=>x.join(''))).size,4,'source patterns duplicate');
  assert.equal(new Set(patterns.map(x=>x.reduce((a,b)=>a^b,0))).size,1,'not a parity block');
 }
 let sourceCalls=0,sourceProbes=0,sourceFalse=0;
 for(const c of f.clauses) {
  const incident=f.graph.edges.flatMap(([u,v],i)=>u===c.vertex||v===c.vertex?[i]:[]);
  assert.equal(incident.length,3);
  for(let mask=0;mask<8;mask++) {
   const bits=Array(E).fill(0);
   incident.forEach((edge,j)=>{bits[edge]=(mask>>j)&1;});
   const q=satWithProbes(c.literals,bits);
   sourceCalls++;sourceProbes+=q.probes;
   if(!q.sat)sourceFalse++;
  }
 }
 let essential=0,witnessDigits=0,witnessCalls=0,witnessProbes=0;
 for(let i=0;i<M;i++) {
  const d=f.deleted[i],c=f.clauses[i];
  assert.equal(d.sourceId,c.id,'same indexed SOURCE');
  if(d.assignment===null)continue;
  const s=d.assignment;
  assert.equal(s.length,E,'assignment length');
  assert(/^[01]+$/.test(s),'binary digits');
  const bits=Array.from(s,Number);
  essential++;witnessDigits+=s.length;
  for(let j=0;j<M;j++) {
   const q=satWithProbes(f.clauses[j].literals,bits);
   witnessCalls++;witnessProbes+=q.probes;
   assert.equal(q.sat,j!==i,'deletion witness does not isolate exactly one original clause');
  }
 }
 assert.equal(essential,f.properties.essential,'accepted essential count');
 assert.equal(witnessDigits,essential*E);
 assert.equal(witnessCalls,essential*M);
 assert.equal(witnessProbes,7*V*essential,'canonical parity-block seven-probe invariant');
 assert.equal(sourceCalls,8*M);
 assert.equal(sourceProbes,14*M,'full local-source table fourteen-probe invariant');
 assert.equal(sourceFalse,M,'one forbidden source assignment per clause');
 const row={fixture:f.graph.name,V,E,sourceClauses:M,paid:f.proof.length,essential,
  nullWitnesses:M-essential,witnessDigitChars:witnessDigits,
  witnessClauseCalls:witnessCalls,witnessLiteralProbes:witnessProbes,
  sourceTableClauseCalls:sourceCalls,sourceTableLiteralProbes:sourceProbes};
 rows.push(row);
}
const names=rows.map(x=>x.fixture);
assert.deepEqual(names,['K4','K33','CUBE','PETERSEN','PRISM6','PRISM16','BRIDGE_K4x2']);
assert.equal(rows.at(-1).essential,36,'bridged e');
const sumKey=k=>rows.reduce((n,r)=>n+r[k],0);
const totals={independentFixtures:rows.length,paid:sumKey('paid'),sourceClauses:sumKey('sourceClauses'),
 essential:sumKey('essential'),nullWitnesses:sumKey('nullWitnesses'),
 witnessDigitChars:sumKey('witnessDigitChars'),witnessClauseCalls:sumKey('witnessClauseCalls'),
 witnessLiteralProbes:sumKey('witnessLiteralProbes'),
 sourceTableClauseCalls:sumKey('sourceTableClauseCalls'),
 sourceTableLiteralProbes:sumKey('sourceTableLiteralProbes')};
assert.deepEqual(totals,{independentFixtures:7,paid:321,sourceClauses:328,essential:324,
 nullWitnesses:4,witnessDigitChars:8844,witnessClauseCalls:23584,witnessLiteralProbes:41272,
 sourceTableClauseCalls:2624,sourceTableLiteralProbes:4592});
let osNative=null;
if(process.argv.includes('--native')) {
 const run=cp.spawnSync(process.execPath,[path.join(root,cpPath),path.join(root,dataPath)],
   {encoding:'utf8',maxBuffer:16*1024*1024});
 assert.equal(run.status,0,'original checker failed: '+run.stderr.slice(0,300));
 osNative={checkerAccepted:true,assertionGroups:JSON.parse(run.stdout).checks};
 assert.equal(osNative.assertionGroups,30714);
}
const result={schema:'LSPV4_581A_ORIGINAL341_LITERAL_PROBES/v1',
 original_checker_blob:expectedChecker,original_packet_blob:expectedPacket,
 theorem:'For 4 source clauses per vertex in fixed common variable order forbidding one parity class, exactly 7 literal iterations per vertex occur on any complete assignment. For e valid deletion witnesses, Q_lit=7Ve; source truth tables use 14 iterations per clause.',
 method:'Independent JavaScript clause evaluation of all actual 324 nonnull original packet deletion witnesses against all 328 indexed signed original SOURCE clauses, and all 328 full three-bit source tables. No RNG.',
 rows,totals,osOriginalChecker:osNative,
 limitations:['seven independent proofs, not one combined proof','original /341 SOURCE/AND3/XOR accepted sublanguage only','not historical unified R_mix341 or proof verifier time/RAM lower bound',
 'OS original-checker replay only if --native']};
const out=process.argv.indexOf('--out');
if(out>=0){assert(process.argv[out+1]);fs.writeFileSync(process.argv[out+1],JSON.stringify(result,null,2)+'\n');}
console.log(JSON.stringify({result:'PASS',rows:rows.length,essential:totals.essential,
 witnessLiteralProbes:totals.witnessLiteralProbes,sourceLiteralProbes:totals.sourceTableLiteralProbes,
 native:!!osNative},null,2));
