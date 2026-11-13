'use strict';
// LSPV-5/523: accepted-byte literal-order alias against the /581A 7Ve claim.
// Usage: node experiments/arc/lspv5_523_accepted_order_alias.cjs [--out FILE] [--emit FILE]
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),crypto=require('node:crypto');
const cp=require('node:child_process'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checkerPath=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const packetPath=path.join(root,'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json');
const checkerBlob='fcb7d4ced8f922de14c0bda16263a8cc7853e8e0';
const packetBlob='fe27fe1011d0021e721ccaeb747ed58da65d7464';
const gitBlob=b=>crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');
const C=fs.readFileSync(checkerPath),P=fs.readFileSync(packetPath);
assert.equal(gitBlob(C),checkerBlob); assert.equal(gitBlob(P),packetBlob);
const original=JSON.parse(P);
const clone=x=>JSON.parse(JSON.stringify(x));
function probes(lits,bits){let n=0;for(const lit of lits){n++;if((lit>0&&bits[lit-1]===1)||(lit<0&&bits[-lit-1]===0))return n;}return n;}
function perms(a){return [[a[0],a[1],a[2]],[a[0],a[2],a[1]],[a[1],a[0],a[2]],[a[1],a[2],a[0]],[a[2],a[0],a[1]],[a[2],a[1],a[0]]];}
function fixtureWitnessBits(f){return f.deleted.filter(d=>d.assignment!==null).map(d=>Array.from(d.assignment,Number));}
function witnessProbeTotal(data){let total=0;for(const f of data.fixtures){const ws=fixtureWitnessBits(f);for(const bits of ws)for(const c of f.clauses)total+=probes(c.literals,bits);}return total;}
function sourceProbeTotal(data){let total=0;for(const f of data.fixtures){const E=f.graph.edges.length;for(const c of f.clauses){const inc=f.graph.edges.flatMap(([u,v],i)=>u===c.vertex||v===c.vertex?[i]:[]);for(let m=0;m<8;m++){const bits=Array(E).fill(0);inc.forEach((e,j)=>bits[e]=(m>>j)&1);total+=probes(c.literals,bits);}}}return total;}
function runChecker(bytes,label){const file=path.join(os.tmpdir(),'lspv5_523_'+process.pid+'_'+label+'.json');fs.writeFileSync(file,bytes);const r=cp.spawnSync(process.execPath,[checkerPath,file],{encoding:'utf8',maxBuffer:16*1024*1024});fs.unlinkSync(file);return {accepted:r.status===0,status:r.status,checks:r.status===0?JSON.parse(r.stdout).checks:null,stderr:r.stderr.slice(0,400)};}
const baselineWitness=witnessProbeTotal(original),baselineSource=sourceProbeTotal(original);
assert.equal(baselineWitness,41272);assert.equal(baselineSource,4592);
let single=null;
outer:for(let fi=0;fi<original.fixtures.length;fi++)for(let ci=0;ci<original.fixtures[fi].clauses.length;ci++){
 const old=original.fixtures[fi].clauses[ci].literals,ws=fixtureWitnessBits(original.fixtures[fi]);
 const oldN=ws.reduce((n,b)=>n+probes(old,b),0);
 for(const q of perms(old)){
  const newN=ws.reduce((n,b)=>n+probes(q,b),0);
  if(newN!==oldN){single={fixtureIndex:fi,fixture:original.fixtures[fi].graph.name,clauseIndex:ci,sourceId:original.fixtures[fi].clauses[ci].id,oldLiterals:old,newLiterals:q,oldWitnessProbes:oldN,newWitnessProbes:newN,delta:newN-oldN};break outer;}
 }
}
assert(single,'no order-sensitive clause found');
const hostile=clone(original);hostile.fixtures[single.fixtureIndex].clauses[single.clauseIndex].literals=single.newLiterals;
const hostileBytes=Buffer.from(JSON.stringify(hostile,null,2)+'\n');
const hostileWitness=witnessProbeTotal(hostile),hostileSource=sourceProbeTotal(hostile);
assert.equal(hostileWitness,baselineWitness+single.delta);assert.equal(hostileSource,baselineSource);
const originalRun=runChecker(P,'original');const hostileRun=runChecker(hostileBytes,'single_alias');
assert(originalRun.accepted&&hostileRun.accepted);assert.equal(originalRun.checks,30714);assert.equal(hostileRun.checks,30714);
const minPacket=clone(original),maxPacket=clone(original);let minExpected=0,maxExpected=0;
for(let fi=0;fi<original.fixtures.length;fi++){
 const ws=fixtureWitnessBits(original.fixtures[fi]);
 for(let ci=0;ci<original.fixtures[fi].clauses.length;ci++){
  const p=perms(original.fixtures[fi].clauses[ci].literals).map(lits=>({lits,n:ws.reduce((s,b)=>s+probes(lits,b),0)}));
  p.sort((a,b)=>a.n-b.n||a.lits.join(',').localeCompare(b.lits.join(',')));
  minPacket.fixtures[fi].clauses[ci].literals=p[0].lits;maxPacket.fixtures[fi].clauses[ci].literals=p.at(-1).lits;minExpected+=p[0].n;maxExpected+=p.at(-1).n;
 }
}
assert.equal(witnessProbeTotal(minPacket),minExpected);assert.equal(witnessProbeTotal(maxPacket),maxExpected);
const minBytes=Buffer.from(JSON.stringify(minPacket,null,2)+'\n'),maxBytes=Buffer.from(JSON.stringify(maxPacket,null,2)+'\n');
const minRun=runChecker(minBytes,'min'),maxRun=runChecker(maxBytes,'max');assert(minRun.accepted&&maxRun.accepted);assert.equal(minRun.checks,30714);assert.equal(maxRun.checks,30714);
const orderIndependentLower=original.fixtures.reduce((n,f)=>n+f.properties.essential*(f.clauses.length+2),0);
const orderIndependentUpper=original.fixtures.reduce((n,f)=>n+3*f.properties.essential*f.clauses.length,0);
assert.equal(orderIndependentLower,24232);assert.equal(orderIndependentUpper,70752);
const result={schema:'LSPV5_523_ACCEPTED_ORDER_ALIAS/v1',checker:{path:path.relative(root,checkerPath),blob:checkerBlob},source_packet:{path:path.relative(root,packetPath),blob:packetBlob,bytes:P.length},claim_tested:'Whether 7Ve=41272 witness literal probes is enforced by the unchanged /341 accepted-byte grammar rather than only by the canonical archived clause order.',baseline:{accepted:originalRun.accepted,checks:originalRun.checks,witnessLiteralProbes:baselineWitness,sourceLiteralProbes:baselineSource},accepted_single_clause_alias:{mutation:single,packetBytes:hostileBytes.length,packetBlob:gitBlob(hostileBytes),accepted:hostileRun.accepted,checks:hostileRun.checks,witnessLiteralProbes:hostileWitness,sourceLiteralProbes:hostileSource},accepted_extrema:{minimum:{packetBlob:gitBlob(minBytes),accepted:minRun.accepted,checks:minRun.checks,witnessLiteralProbes:minExpected},maximum:{packetBlob:gitBlob(maxBytes),accepted:maxRun.accepted,checks:maxRun.checks,witnessLiteralProbes:maxExpected}},repaired_bounds:{orderIndependentCodeLower:orderIndependentLower,orderIndependentCodeUpper:orderIndependentUpper,exactAllWithinClausePermutationMinimum:minExpected,exactAllWithinClausePermutationMaximum:maxExpected,sourceTableProbesOrderIndependent:baselineSource},conclusion:'The exact canonical-packet count 41272 reproduces, but the unchanged historical checker accepts literal-order aliases with different short-circuit witness probe counts. Therefore 7Ve is not an accepted-byte invariant. The semantic source/proof is unchanged and the source-table total stays 4592.',scope:['P2-D1 grammar-authentication failure only','does not invalidate the parity-block theorem under its common-order premise','does not give a cheaper logical proof or settle P2-C3/P2-B1','P2-B2/B3 untouched','P versus NP remains OPEN']};
const oi=process.argv.indexOf('--out');if(oi>=0){assert(process.argv[oi+1]);fs.writeFileSync(process.argv[oi+1],JSON.stringify(result,null,2)+'\n');}
const ei=process.argv.indexOf('--emit');if(ei>=0){assert(process.argv[ei+1]);fs.writeFileSync(process.argv[ei+1],hostileBytes);}
console.log(JSON.stringify(result,null,2));
