#!/usr/bin/env node
'use strict';
/*
 * LSPV-3/582: OS-subprocess reproducer for the unchanged original archived /341
 * checker. Reference/independent computation is used ONLY for the SAT witness.
 * Run from the repository root:
 *   node experiments/arc/lspv3_582_string_charge_original341_os_replay.cjs
 * Optional second argument: JSON results output path.
 *
 * This script does NOT implement or repair R_mix341 and does not modify original files.
 */
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const cp=require('node:child_process'),crypto=require('node:crypto');
const assert=require('node:assert/strict');

const checker='experiments/arc/lspv2_341_independent_verify.js';
const seed='results/raw/arc/2026-11-11_0424_LSPV3_568_NUMERIC_WRAP32_SAT_ACCEPTED_PACKET.json';
const witness='results/raw/arc/2026-11-11_1824_LSPV3_582_STRING_CHARGE_SAT_ACCEPTED_PACKET.json';
const rawArchived='results/raw/arc/2026-11-11_1824_LSPV3_582_STRING_CHARGE_HOSTED_ORIGINAL341_RAW.json';
const expectedBlobs={
 [checker]:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
 [seed]:'adb4864906029ecf7b1cd1cf7a4bf513218a13a8',
 [witness]:'6cf9b0fe1e5a9419e8967d836c707c385418b810',
 [rawArchived]:'1b3fb2a385a3f66a0932625a447d2911eb9fb638'
};
const digest=b=>crypto.createHash('sha256').update(b).digest('hex');
function blob(b){const h=Buffer.from('blob '+b.length+'\0');return crypto.createHash('sha1').update(Buffer.concat([h,b])).digest('hex');}
for(const [f,id] of Object.entries(expectedBlobs)){
 const x=fs.readFileSync(f);assert.equal(blob(x),id,'original/published file drift: '+f);
}
const original=JSON.parse(fs.readFileSync(seed,'utf8'));
const pinnedPacket=fs.readFileSync(witness,'utf8');
const baseline=JSON.parse(pinnedPacket);
assert.equal(baseline.fixtures[0].charges[0],'1');
assert.equal(baseline.fixtures[0].clauses.length,48);
const clone=o=>JSON.parse(JSON.stringify(o));
function normalize(o){return JSON.stringify(o)+'\n';}
const simple=clone(original);simple.fixtures[0].charges[0]='1';
assert.equal(normalize(simple),pinnedPacket,'byte-exact packet not reproducible');

const assignment='101001000000100000';
function clauseSAT(c,a){return c.literals.some(l=>Number(a[Math.abs(l)-1])===(l>0?1:0));}
const satisfied=baseline.fixtures[0].clauses.filter(c=>clauseSAT(c,assignment)).length;
assert.equal(satisfied,48,'not an explicit SAT source');

const spec=[
 ['numeric_wrap_original',p=>{}],
 ['string_one',p=>p.fixtures[0].charges[0]='1'],
 ['boolean_true',p=>p.fixtures[0].charges[0]=true],
 ['array_one',p=>p.fixtures[0].charges[0]=[1]],
 ['all_string_charges',p=>p.fixtures[0].charges=p.fixtures[0].charges.map(x=>x===4294967297?'1':String(x))],
 ['string_zeroone',p=>p.fixtures[0].charges[0]='01'],
 ['hex_string_one',p=>p.fixtures[0].charges[0]='0x1'],
 ['numeric_one_reject',p=>p.fixtures[0].charges[0]=1],
 ['string_zero_reject',p=>p.fixtures[0].charges[0]='0'],
 ['boolean_false_reject',p=>p.fixtures[0].charges[0]=false],
 ['array_empty_reject',p=>p.fixtures[0].charges[0]=[]],
 ['null_reject',p=>p.fixtures[0].charges[0]=null],
 ['invalid_string_reject',p=>p.fixtures[0].charges[0]='non-number'],
 ['unknown_opcode_reject',p=>{p.fixtures[0].charges[0]='1';p.fixtures[0].proof[0].rule='LOCAL-CONVERT';}],
 ['missing_parent_reject',p=>{p.fixtures[0].charges[0]='1';p.fixtures[0].proof[0].parents[0]='nonexistent';}],
 ['forged_source_reject',p=>{p.fixtures[0].charges[0]='1';p.fixtures[0].clauses[0].literals[0]=999;}],
 ['forged_affine_reject',p=>{p.fixtures[0].charges[0]='1';p.fixtures[0].proof.find(y=>y.row).row.mask='0x0';}],
 ['forged_sink_reject',p=>{p.fixtures[0].charges[0]='1';p.fixtures[0].proof.at(-1).row.rhs=0;}]
];
const archived=JSON.parse(fs.readFileSync(rawArchived,'utf8')).variants;
assert.equal(spec.length,archived.length);
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-lspv3-582-'));
const cases=[];
try{
 for(let i=0;i<spec.length;i++){
  const [id,fun]=spec[i],candidate=clone(original);fun(candidate);
  const input=normalize(candidate),fp=path.join(temp,String(i)+'.json');
  fs.writeFileSync(fp,input,'utf8');
  const r=cp.spawnSync(process.execPath,[checker,fp],{encoding:'utf8',maxBuffer:16*1024*1024});
  assert.equal(r.error,undefined,'OS spawn failure');
  const accepted=r.status===0;
  const row={id,byteLength:Buffer.byteLength(input),sha256:digest(Buffer.from(input)),verdict:accepted?'ACCEPT':'REJECT'};
  if(accepted){
   const v=JSON.parse(r.stdout);row.originalAssertions=v.checks;
   assert.equal(v.checks,3273,'unexpected native checker assertion count: '+id);
  }else{
   row.error=(r.stderr||'').split('\n').filter(Boolean)[0]||'unknown';
  }
  assert.equal(row.verdict,archived[i].verdict,'hosted/original OS discrepancy '+id);
  assert.equal(row.byteLength,archived[i].byteLength,'byte count discrepancy '+id);
  cases.push(row);
 }
}finally{fs.rmSync(temp,{recursive:true,force:true});}
const outcome={
 run:'LSPV-3/582',execution:'OS Node subprocess ORIGINAL /341 checker; independent SAT oracle only',
 checkerBlob:expectedBlobs[checker],originalSatSeedBlob:expectedBlobs[seed],
 exactAcceptedPacketBlob:expectedBlobs[witness],positive:cases.filter(c=>c.verdict==='ACCEPT').length,
 negative:cases.filter(c=>c.verdict==='REJECT').length,sourceSAT:48,witness:assignment,cases
};
const output=JSON.stringify(outcome,null,2)+'\n';
if(process.argv[2])fs.writeFileSync(process.argv[2],output);
process.stdout.write(output);
