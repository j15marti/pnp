'use strict';
// LSPV-3/609: direct native /341 CLI replay and SAT-goal counterexample.
// Usage from repository root: node experiments/arc/lspv3_609_goal_soundness_no_go.cjs
// No dependencies beyond Node.js 18+ standard library. Does not modify original checker.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const os=require('node:os');
const cp=require('node:child_process');
const crypto=require('node:crypto');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const packet=path.join(root,'results/raw/arc/2026-11-12_2219_LSPV3_606_X10_NATIVE341_ACCEPTED.json');
const signed=path.join(root,'results/raw/arc/2026-11-13_0124_LSPV3_609_SAT_SIGNED_SOURCE.cnf');
function gitBlobHash(buf) {return crypto.createHash('sha1').update('blob '+buf.length+'\0').update(buf).digest('hex');}
assert.equal(gitBlobHash(fs.readFileSync(checker)),'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0');
assert.equal(gitBlobHash(fs.readFileSync(packet)),'1e19a9d2b84daa1fc8c29468873ad62e0d67e105');
const bytes=fs.readFileSync(packet,'utf8'), data=JSON.parse(bytes), f=data.fixtures[0];
assert.equal(f.clauses.length,48);
assert.equal(f.proof.length,47);
assert.equal(f.charges[5],'0');
const dimacs='p cnf 18 48\n'+f.clauses.map(c=>c.literals.join(' ')+' 0').join('\n')+'\n';
assert.equal(fs.readFileSync(signed,'utf8'),dimacs,'signed source extraction changed');
const sat=(c,assignment)=>c.literals.some(l=>((assignment[Math.abs(l)-1]===1)===(l>0)));
const bits='000000010010000001'.split('').map(Number);
assert.equal(bits.length,18);
assert.equal(f.clauses.filter(c=>sat(c,bits)).length,48);
let models=0;
for(let mask=0;mask<2**18;mask++){
  let pass=true;
  for(const c of f.clauses){
    let yes=false;
    for(const l of c.literals){
      const bit=(mask >>> (Math.abs(l)-1)) & 1;
      if((l>0&&bit===1)||(l<0&&bit===0)){yes=true;break;}
    }
    if(!yes){pass=false;break;}
  }
  if(pass) models++;
}
assert.equal(models,64);
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-609-'));
function call(label,doc){
  const file=path.join(dir,label+'.json');
  fs.writeFileSync(file,doc);
  const z=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',timeout:120000});
  if(z.error) throw z.error;
  return {accept:z.status===0,status:z.status,stdout:z.stdout,stderr:z.stderr};
}
const cases={};
try{
  const original=call('baseline',bytes);
  assert.equal(original.accept,true,'original checker must accept exact raw packet');
  const o=JSON.parse(original.stdout);
  assert.equal(o.checks,5155);
  assert.equal(o.cases.length,1);
  assert.equal(o.cases[0].proofNodes,47);
  cases.baseline={accept:true,checks:o.checks,paid:o.cases[0].proofNodes};
  for(const [label,modify,needle] of [
    ['charge_type_repair',x=>{x.fixtures[0].charges[5]=0;},'source forbidden pattern parity'],
    ['signed_source_corruption',x=>{x.fixtures[0].clauses[0].literals[0]=999;},'signed incidence mismatch'],
    ['sink_corruption',x=>{x.fixtures[0].proof.at(-1).row.rhs=0;},'bad GF2 elimination']
  ]){
    const x=JSON.parse(bytes);modify(x);
    const observed=call(label,JSON.stringify(x));
    assert.equal(observed.accept,false,label+' was incorrectly accepted');
    assert(observed.stderr.includes(needle),label+' rejected for unexpected reason: '+observed.stderr);
    cases[label]={accept:false,reason:needle};
  }
}finally{fs.rmSync(dir,{recursive:true,force:true});}
const result={
  status:'PASS',role:'LSPV-3/609',checkerBlob:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
  packetBlob:'1e19a9d2b84daa1fc8c29468873ad62e0d67e105',
  sourceDerivedFromPacket:true,externallyTrustedHistoricalSource:false,
  sourceClauses:48,variables:18,actualSATModels:models,
  satisfyingWitness:'000000010010000001',paidInferenceRecords:47,
  originalCheckerExecution:'unchanged OS Node subprocess',cases,
  implication:'An acceptance-preserving overapproximation of this recovered /341 checker cannot also treat every abstract accepted goal as genuine UNSAT.',
  fullHistoricalRmix341Authenticated:false,p2d1:'OPEN',p2c3:'OPEN',p2b1:'OPEN',PversusNP:'OPEN'
};
console.log(JSON.stringify(result,null,2));
