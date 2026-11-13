'use strict';
// LSPV-3/619. Run in j15marti/pnp checkout:
// node experiments/arc/lspv3_619_dead_owner_charge_family.cjs [output.json]
// This executes the unchanged original /386 CLI as actual Node subprocesses.
// It is not the missing complete R_mix341 checker.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const cp=require('node:child_process'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const ROOT=path.resolve(__dirname,'../..');
const checker='experiments/arc/lspv2_386_independent_verify.js';
const seed='results/raw/arc/2026-11-11_0407_LSPV2_555_ACCEPTED_LIVE_DEF_RES_K1.json';
const PIN={checker:'338305c0ce101704205e57543756b8127074a986',seed:'aeeb555c4dcf7f510a9a501c8afc609b629a9298'};
const buf=p=>fs.readFileSync(path.join(ROOT,p));
const blobSha=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
assert.equal(blobSha(buf(checker)),PIN.checker,'Original checker Git blob changed');
assert.equal(blobSha(buf(seed)),PIN.seed,'Original seed Git blob changed');
const base=JSON.parse(buf(seed).toString('utf8'));
assert.equal(base.summary.paid_total,33);assert.equal(base.summary.paid_gates,3);
assert.equal(base.summary.resolution,30);assert.equal(base.summary.live_records,51);
const clone=o=>JSON.parse(JSON.stringify(o));
const addDead=k=>{
 const d=clone(base);
 for(let j=0;j<k;j++)d.gate_defs.push([3+j,11+j,1,2]);
 d.summary.paid_gates+=k;d.summary.paid_total+=k;
 assert.equal(JSON.stringify(d.records),JSON.stringify(base.records),'Proof records changed');
 assert.equal(JSON.stringify(d.spec),JSON.stringify(base.spec),'Source spec changed');
 return d;
};
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-lspv3-619-'));
let attempts=0;
function native(d,label){
 const f=path.join(dir,label+'.json');fs.writeFileSync(f,JSON.stringify(d));
 const child=cp.spawnSync(process.execPath,[path.join(ROOT,checker),f],{
  encoding:'utf8',timeout:30000,maxBuffer:4*1024*1024});
 attempts++;
 return {accepted:child.status===0&&!child.error,status:child.status,
  info:child.status===0?JSON.parse(child.stdout):null,
  error:String(child.stderr||child.error||'').trim().slice(0,500)};
}
let positives=[],negatives=[];
try {
 for(const k of [0,1,2,8,32]){
  const p=native(addDead(k),'positive-'+k);
  assert(p.accepted,'Native checker rejected k='+k+': '+p.error);
  assert.equal(p.info.paid,33+k);assert.equal(p.info.def,3+k);
  assert.equal(p.info.res,30);assert.equal(p.info.records,51);
  assert.equal(p.info.sources,17);assert.equal(p.info.negativeTests,11);
  positives.push({k,paid:p.info.paid,gates:p.info.def,resolution:p.info.res,
   source:p.info.sources,records:p.info.records,assertions:p.info.assertions,accepted:true});
 }
 const bad=[
  ['underpaid total',d=>d.summary.paid_total--],
  ['underreported gates',d=>d.summary.paid_gates--],
  ['duplicate owner ID',d=>d.gate_defs.at(-1)[0]=d.gate_defs.at(-2)[0]],
  ['duplicate owner output',d=>d.gate_defs.at(-1)[1]=d.gate_defs.at(-2)[1]],
  ['guard reused as output',d=>d.gate_defs.at(-1)[1]=d.spec.guard],
  ['forward gate input',d=>d.gate_defs.at(-2)[2]=12],
  ['guard reused as input',d=>d.gate_defs.at(-1)[2]=d.spec.guard],
  ['string owner ID',d=>d.gate_defs.at(-1)[0]='4']
 ];
 for(let j=0;j<bad.length;j++){
  const [label,mutate]=bad[j],d=addDead(2);mutate(d);
  const result=native(d,'negative-'+j);
  assert(!result.accepted,'Malformed '+label+' accepted');
  negatives.push({label,accepted:false,rejection:result.error});
 }
}finally {fs.rmSync(dir,{recursive:true,force:true});}
const result={schema:'LSPV3-619-NATIVE386-DEAD-OWNER-FAMILY/v1',
 date_pst:'2026-11-13 10:24 PST',authority:'UNCHANGED_ORIGINAL_386_NODE_OS',
 checker_git_blob:PIN.checker,seed_git_blob:PIN.seed,
 theorem:'For every representable nonnegative k, append k fresh unused paid gate declarations; source, records and terminal DAG unchanged, accepted W=33+k.',
 fixture:{source:17,free_def:4,resolution:30,records:51,baseline_gates:3,baseline_work:33},
 positives,negatives,attempts,all_pass:true,
 scope:'The archived /386 SOURCE/DEF/RES sibling only. Node OS runner, not executed in hosted original-body run. W is logical paid work, not bytes, time, span or peak space. Not an optimal-work lower bound.'};
const json=JSON.stringify(result,null,2)+'\n';
if(process.argv[2])fs.writeFileSync(process.argv[2],json);
process.stdout.write(json);
