#!/usr/bin/env node
'use strict';
// LSPV-5/516 independent original-OS replay. This does not repair or replace
// the recovered checker and does not claim to be the full historical R_mix341.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const os=require('node:os');
const cp=require('node:child_process');
const crypto=require('node:crypto');

const root=path.resolve(__dirname,'../..');
const rel={
  checker:'experiments/arc/lspv2_341_independent_verify.js',
  original:'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json',
  sat:'results/raw/arc/2026-11-10_1224_LSPV3_551_ACCEPTED_SAT_PACKET.json',
  k4:'results/raw/arc/2026-11-12_1725_LSPV3_600_NATIVE341_K4_EDGE_SUFFIX_ACCEPTED.json',
  escaped:'results/raw/arc/2026-11-12_1905_LSPV3_603_K4_ESCAPED_WITNESSES_ACCEPTED.json',
  peer603:'experiments/arc/lspv3_603_native341_witness_escape_grammar.cjs'
};
const pins={checker:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
  original:'fe27fe1011d0021e721ccaeb747ed58da65d7464',
  sat:'706947c767361e7c979b8208677eb983d33838f4',
  k4:'393d13265192b4e43073c6f6559bc22b6a71ece5',
  escaped:'c024067e85053b6f25a06795f3c5da748850c8dd',
  peer603:'a18ae9760ffc20f51e08fb8537a4e25f8d88e2ad'};
const sha256=b=>crypto.createHash('sha256').update(b).digest('hex');
const gitBlob=b=>crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');
const bytes={};
for(const [k,p] of Object.entries(rel)){
  bytes[k]=fs.readFileSync(path.join(root,p));
  assert.equal(gitBlob(bytes[k]),pins[k],`pinned Git blob ${k}`);
}
const original=JSON.parse(bytes.original),satPacket=JSON.parse(bytes.sat);
const clone=x=>JSON.parse(JSON.stringify(x));
const fixture=satPacket.fixtures.find(f=>f.graph?.edges?.length===18);
assert(fixture&&fixture.clauses.length===48&&fixture.proof.length===47);
const witness=Array.from('101001000000100000',Number);
const clauseSat=(c,a)=>c.literals.some(l=>a[Math.abs(l)-1]===Number(l>0));
assert.equal(fixture.clauses.filter(c=>clauseSat(c,witness)).length,48);

// Independently prove that duplicating the first K4 AND3 with a fresh ID is
// a truth-table-exact, source-parented inference under the separately declared rule.
const k4=original.fixtures[0],first=k4.proof[0];
assert.equal(first.rule,'AND3');assert.equal(first.parents.length,2);
const sourceById=new Map(k4.clauses.map(c=>[c.id,c]));
function factorValue(parent,bits){
  const c=sourceById.get(parent);assert(c,`source parent ${parent}`);return clauseSat(c,bits)?1:0;
}
let reconstructed=0;
for(let m=0;m<(1<<first.support.length);m++){
  const bits=Array(k4.graph.edges.length).fill(0);
  first.support.forEach((e,i)=>bits[e]=(m>>i)&1);
  if(first.parents.every(p=>factorValue(p,bits)))reconstructed|=1<<m;
}
assert.equal(reconstructed,first.table);
const redundant=clone(original),copy=clone(redundant.fixtures[0].proof[0]);
copy.id='REDUNDANT_VALID_AND3_516';
redundant.fixtures[0].proof.splice(1,0,copy);
assert.equal(redundant.fixtures[0].proof.length,16);

// The general Resolution declaration has the one-step refutation (x),(-x) |- ().
function resolveUnit(a,b,pivot){
  assert(a.includes(pivot)&&b.includes(-pivot));
  return [...new Set([...a.filter(x=>x!==pivot),...b.filter(x=>x!==-pivot)])];
}
assert.deepEqual(resolveUnit([1],[-1],1),[]);

const acceptedClaim=clone(satPacket);
acceptedClaim.claimedExternalOriginalInput='p cnf 1 2\n1 0\n-1 0\n';
acceptedClaim.claimedExternalSourceSha256=sha256(Buffer.from(acceptedClaim.claimedExternalOriginalInput));
const badSource=clone(satPacket);badSource.fixtures[1].clauses[0].literals[0]=999;
const badParent=clone(satPacket);badParent.fixtures[1].proof[0].parents[0]='MISSING_PARENT';
const badSink=clone(satPacket);badSink.fixtures[1].proof.at(-1).row.rhs^=1;
const badRule=clone(original);badRule.fixtures[0].proof[0].rule='RES';

// Repair the /603 nested-edit test locally: the peer runner's edit function
// accepts only two parameters, so its third nested-base argument is ignored.
const peer603Text=bytes.peer603.toString('utf8');
assert(peer603Text.includes('function edit(field,token)'));
assert(peer603Text.includes('edit("deleted",slash+"u0030",edit("even",slash+"u0030"))'));
function editWitness(base,field,token){
  const pat=field==='even'?/("evenWitness":\s*")000000(")/:/("assignment":\s*")000000(")/;
  assert(pat.test(base));return base.replace(pat,(_,a,b)=>a+'00000'+token+b);
}
const k4Raw=bytes.k4.toString('utf8'),slash=String.fromCharCode(92);
const evenEscaped=editWitness(k4Raw,'even',slash+'u0030');
const deletedEscaped=editWitness(k4Raw,'deleted',slash+'u0030');
const bothEscaped=editWitness(editWitness(k4Raw,'even',slash+'u0030'),'deleted',slash+'u0030');
assert.notEqual(sha256(Buffer.from(bothEscaped)),sha256(Buffer.from(evenEscaped)));
assert.notEqual(sha256(Buffer.from(bothEscaped)),sha256(Buffer.from(deletedEscaped)));
assert.equal(bothEscaped,bytes.escaped.toString('utf8'));

const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv5-516-')),runs=[];
function run(name,body,expected,expectedError=null){
  const raw=Buffer.isBuffer(body)?body:Buffer.from(typeof body==='string'?body:JSON.stringify(body));
  const file=path.join(tmp,name+'.json');fs.writeFileSync(file,raw);
  const p=cp.spawnSync(process.execPath,[path.join(root,rel.checker),file],
    {encoding:'utf8',timeout:30000,maxBuffer:12*1024*1024});
  if(p.error)throw p.error;
  const accepted=p.status===0;assert.equal(accepted,expected,`${name}: ${p.stderr}`);
  let out=null;if(accepted)out=JSON.parse(p.stdout);
  const err=accepted?null:(p.stderr||p.stdout).trim().split('\n').find(x=>x.includes('Error:'))||'native rejection';
  if(expectedError)assert.match(err,expectedError,name);
  runs.push({name,accepted,exitStatus:p.status,bytes:raw.length,sha256:sha256(raw),
    checks:out?.checks??null,stdoutSha256:accepted?sha256(Buffer.from(p.stdout)):null,error:err});
}
try{
  run('seven_fixture_original',bytes.original,true);
  run('accepted_satisfiable_source',bytes.sat,true);
  run('accepted_ignored_external_unsat_claim',acceptedClaim,true);
  run('rejected_fresh_valid_redundant_AND3',redundant,false,/proof candidate length/);
  run('rejected_unknown_RES_opcode',badRule,false,/unknown rule/);
  run('rejected_forged_source',badSource,false,/signed incidence mismatch/);
  run('rejected_missing_parent',badParent,false,/missing antecedent/);
  run('rejected_bad_sink',badSink,false,/bad GF2 elimination|invalid sink/);
  run('k4_even_escape_only',evenEscaped,true);
  run('k4_deleted_escape_only',deletedEscaped,true);
  run('k4_actual_both_escaped',bothEscaped,true);
  run('k4_published_both_escaped',bytes.escaped,true);
  assert.equal(runs[0].checks,30714);assert.equal(runs[1].checks,2273);assert.equal(runs[2].checks,2273);
  assert.equal(runs[8].checks,1401);assert.equal(runs[9].checks,1401);assert.equal(runs[10].checks,1401);
  const acceptedPath=path.join(root,'results/raw/review/2026-11-12_1948_LSPV5_516_ACCEPTED_IGNORED_EXTERNAL_CLAIM.json');
  const rejectedPath=path.join(root,'results/raw/review/2026-11-12_1948_LSPV5_516_REJECTED_VALID_REDUNDANT_AND3.json');
  fs.mkdirSync(path.dirname(acceptedPath),{recursive:true});
  fs.writeFileSync(acceptedPath,JSON.stringify(acceptedClaim,null,2)+'\n');
  fs.writeFileSync(rejectedPath,JSON.stringify(redundant,null,2)+'\n');
  const result={schema:'LSPV5-516-native341-two-sided-membership-os/v1',
    timestamp:'2026-11-12T19:48:00-08:00',status:'COMPUTATIONAL original OS checker replay plus exact finite semantic checks',
    authority:{rel,pins,sha256:Object.fromEntries(Object.entries(bytes).map(([k,v])=>[k,sha256(v)]))},
    satSource:{assignment:'101001000000100000',variables:18,clauses:48,satisfied:48,paidNodes:47},
    declaredResolutionControl:{source:[[1],[-1]],pivot:1,resolvent:[],paidSteps:1},
    redundantAND3Control:{freshId:copy.id,parents:copy.parents,support:copy.support,table:copy.table,
      allAssignmentsChecked:1<<copy.support.length,semanticExact:true,originalPaid:15,mutatedPaid:16},
    peer603Repair:{bug:'peer edit(field,token) ignores the nested third base argument in its mislabeled both_escaped_ascii0 case',
      publishedExactBothEscaped:true,actualBothEscapedOsAccepted:true,
      actualBothSha256:sha256(Buffer.from(bothEscaped)),singleHashesDistinct:true},
    runs,totals:{runs:runs.length,accepted:runs.filter(x=>x.accepted).length,rejected:runs.filter(x=>!x.accepted).length,
      acceptedAssertions:runs.reduce((s,x)=>s+(x.checks||0),0)},
    affected:{P2_D1:'OPEN; recovered checker acceptance is neither sound nor complete for the separate declaration',
      P2_C3:'OPEN',P2_B1:'OPEN',P2_B2_B3:'OPEN separately',P_vs_NP:'OPEN'},
    scope:'Recovered SOURCE/AND3/XOR fixture checker only; not the authoritative full historical R_mix341 grammar'};
  const out=JSON.stringify(result,null,2)+'\n';
  const outPath=process.argv[2]||path.join(root,'results/raw/review/2026-11-12_1948_LSPV5_516_TWO_SIDED_MEMBERSHIP_OS_RAW.json');
  fs.writeFileSync(outPath,out);process.stdout.write(out);
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
