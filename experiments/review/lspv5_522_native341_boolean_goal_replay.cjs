'use strict';
/*
 LSPV-5/522: independent OS replay of LSPV-1/613 and exact-artifact
 validation of LSPV-3/609.

 Run from repository root:
   node experiments/review/lspv5_522_native341_boolean_goal_replay.cjs [raw-output.json]

 Standard-library only. The archived checker is executed unchanged in fresh
 Node subprocesses. No replacement verifier is used for native verdicts.
*/
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const os=require('node:os');
const cp=require('node:child_process');
const crypto=require('node:crypto');

const root=path.resolve(__dirname,'../..');
const rel={
 checker:'experiments/arc/lspv2_341_independent_verify.js',
 packet:'results/raw/arc/2026-11-13_0102_LSPV1_613_ALL_BOOLEAN_SAT_ACCEPTED.json',
 signed:'results/raw/arc/2026-11-13_0124_LSPV3_609_SAT_SIGNED_SOURCE.cnf'
};
for(const k of Object.keys(rel)) rel[k]=path.join(root,rel[k]);
const gitBlob=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
const sha256=b=>crypto.createHash('sha256').update(b).digest('hex');
const checkerBytes=fs.readFileSync(rel.checker);
const packetBytes=fs.readFileSync(rel.packet);
const signedBytes=fs.readFileSync(rel.signed);
assert.equal(gitBlob(checkerBytes),'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0');
assert.equal(gitBlob(packetBytes),'475be36cd9209e32050295192f0452836eb864e3');
assert.equal(gitBlob(signedBytes),'fe1fbde1c74ec1caf052fe009bf96c14ab229303');

const parsed=JSON.parse(packetBytes);
const fixture=parsed.fixtures[0];
assert.equal(fixture.clauses.length,48);
assert.equal(fixture.proof.length,47);
assert.equal(fixture.charges.length,12);
assert(fixture.charges.every(x=>typeof x==='boolean'));
assert.equal(fixture.charges.filter(Boolean).length,1);
assert.equal(fixture.charges[0],true);
assert.equal(typeof fixture.proof.find(x=>x.id==='d17').support,'string');

const dimacs='p cnf 18 48\n'+fixture.clauses.map(c=>c.literals.join(' ')+' 0').join('\n')+'\n';
assert.equal(signedBytes.toString('utf8'),dimacs,'remote /609 signed artifact differs from exact packet extraction');

const sat=(c,a)=>c.literals.some(l=>((a[Math.abs(l)-1]===1)===(l>0)));
const witness='000000010010000001'.split('').map(Number);
assert.equal(fixture.clauses.filter(c=>sat(c,witness)).length,48);
let models=0;
for(let mask=0;mask<2**18;mask++){
 let ok=true;
 for(const c of fixture.clauses){
  let yes=false;
  for(const l of c.literals){
   const bit=(mask >>> (Math.abs(l)-1))&1;
   if((l>0&&bit===1)||(l<0&&bit===0)){yes=true;break}
  }
  if(!yes){ok=false;break}
 }
 if(ok) models++;
}
assert.equal(models,64);

const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv5-522-'));
function runFile(label,file){
 const z=cp.spawnSync(process.execPath,[rel.checker,file],{
  encoding:'utf8',timeout:15000,maxBuffer:4e6
 });
 if(z.error) throw z.error;
 let positive=null;
 if(z.status===0) positive=JSON.parse(z.stdout);
 const reason=(z.stderr.match(/Error: Verifier: ([^\n]+)/)||[])[1]||null;
 return {label,accepted:z.status===0,status:z.status,checks:positive&&positive.checks,
  paid:positive&&positive.cases&&positive.cases[0]&&positive.cases[0].proofNodes,reason};
}
function runMutation(label,mutate){
 const d=JSON.parse(packetBytes);
 mutate(d.fixtures[0]);
 const file=path.join(tmp,label+'.json');
 fs.writeFileSync(file,JSON.stringify(d)+'\n');
 return runFile(label,file);
}

const cases=[];
cases.push(runFile('exact_remote_all_boolean_packet',rel.packet));
cases.push(runMutation('charge_5_integer_zero',f=>{f.charges[5]=0}));
cases.push(runMutation('all_false_charges',f=>{f.charges=f.charges.map(()=>false)}));
cases.push(runMutation('forged_first_source_literal',f=>{f.clauses[0].literals[0]=999}));
cases.push(runMutation('corrupt_d0_table',f=>{f.proof.find(x=>x.id==='d0').table^=1}));
cases.push(runMutation('corrupt_terminal_rhs',f=>{f.proof.at(-1).row.rhs=0}));
assert.deepEqual(cases.map(x=>x.accepted),[true,false,false,false,false,false]);
assert.equal(cases[0].checks,5155);
assert.equal(cases[0].paid,47);

const output={
 schema:'LSPV5-522-NATIVE341-BOOLEAN-GOAL-REPLAY/v1',
 timestamp_pst:'2026-11-13T01:48:00-08:00',
 status:'COMPUTATIONAL independent original-OS validation plus PROVED/RESTRICTED acceptance-vs-goal corollary',
 scope:'Pinned archived /341 SOURCE/AND3/XOR fixture checker only; not full historical R_mix341',
 pins:{
  checker:{git_blob:gitBlob(checkerBytes),sha256:sha256(checkerBytes),bytes:checkerBytes.length},
  packet:{git_blob:gitBlob(packetBytes),sha256:sha256(packetBytes),bytes:packetBytes.length},
  signed:{git_blob:gitBlob(signedBytes),sha256:sha256(signedBytes),bytes:signedBytes.length}
 },
 source:{clauses:48,variables:18,models,witness:'000000010010000001',witness_satisfies:48},
 packet:{all_boolean_charges:true,true_count:1,paid_records:47,string_supports:fixture.proof.filter(x=>typeof x.support==='string').map(x=>x.id)},
 exact_artifact_validation:{
  lspv3_609_signed_file_equals_packet_extraction:true,
  local_sync_extra_newline_hypothesis:'FALSIFIED/RETIRED; exact 540-byte Git blob is correct'
 },
 native_execution:'unchanged checker in fresh OS Node subprocesses',
 cases,
 cegar:'The positive byte path genuinely accepts and must not be refined away. It is an operational goal, not a sound UNSAT goal.',
 theorem:'Any abstraction covering every accepted execution of this checker cannot soundly map every accepted goal to UNSAT of the in-packet source, because this exact accepted packet has 64 models.',
 affected:['P2-D1 OPEN','P2-C3 OPEN','P2-B1 OPEN','P2-B2/B3 separate OPEN'],
 nonclaims:['No complete historical mixed dispatcher','No general proof-cost lower bound','No SAT decision lower bound','No P versus NP result']
};
fs.rmSync(tmp,{recursive:true,force:true});
const out=JSON.stringify(output,null,2)+'\n';
if(process.argv[2]) fs.writeFileSync(process.argv[2],out);
process.stdout.write(out);
