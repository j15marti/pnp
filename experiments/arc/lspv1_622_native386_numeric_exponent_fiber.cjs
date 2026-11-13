'use strict';
// LSPV-1/622: original /386 native-checker accepted lexical exponent fiber.
// Run: node experiments/arc/lspv1_622_native386_numeric_exponent_fiber.cjs [REPO_ROOT] [RAW_OUTPUT]
// Requires Node >=18, standard library only. Original checker is executed unchanged as a child.
const fs=require('node:fs'),cp=require('node:child_process'),path=require('node:path');
const os=require('node:os'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(process.argv[2]||'.');
const checkerFile=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedFile=path.join(root,'results/raw/arc/2026-11-13_0812_LSPV2_601_W32_NATIVE386_SEED.json');
const output=path.resolve(process.argv[3]||path.join(root,'results/raw/arc/2026-11-13_0900_LSPV1_622_NATIVE386_EXPONENT_FIBER_RAW.json'));
const hash=x=>crypto.createHash('sha256').update(x).digest('hex');
const gitHash=x=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+x.length+'\0'),x])).digest('hex');
const checker=fs.readFileSync(checkerFile),seed=fs.readFileSync(seedFile),canonical=seed.toString('utf8');
assert.equal(hash(checker),'22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113');
assert.equal(gitHash(seed),'3a2f40d09b03089e8c86ce2ff2619ad83fbb8e5e');
const needle='"charge":[1,0,0,0]';
assert.equal(canonical.split(needle).length,2,'seed token must occur exactly once');
const parsed=JSON.parse(canonical);assert.equal(parsed.summary.paid_total,32);
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp622-'));
function mutate(token){return canonical.replace(needle,'"charge":['+token+',0,0,0]');}
const cases=[];
function execute(name,raw,expected){
  const file=path.join(temp,name+'.json');fs.writeFileSync(file,raw);
  const cmd=cp.spawnSync(process.execPath,[checkerFile,file],{encoding:'utf8',timeout:20000,maxBuffer:2*1024*1024});
  const accepted=cmd.status===0;
  assert.equal(accepted,expected,name+' unexpected verdict '+cmd.status+' '+cmd.stderr);
  const out=accepted?JSON.parse(cmd.stdout.trim()):null;
  const rec={case:name,expected_accept:expected,accepted,bytes:Buffer.byteLength(raw),sha256:hash(raw),
    paid:out?.paid??null,records:out?.records??null,assertions:out?.assertions??null,
    internal_hostile_tests:out?.negativeTests??null};
  if(accepted){
    assert.equal(out.paid,32);assert.equal(out.records,50);
    assert.equal(out.negativeTests,11);
    assert.deepEqual(JSON.parse(raw),parsed,'parsed packet changed');
  }
  cases.push(rec);return rec;
}
try{
 const ks=[0,1,2,4,8,16,32,64,128,256,1024,4096,16384,65536];
 for(const k of ks)execute('valid_k'+k,mutate('1e+'+'0'.repeat(k+1)),true);
 const negatives=[
  ['bad_exponent','1e+'],['bad_leading_zero','01'],['bad_string','"1e+000"'],
  ['bad_infinite','1e+309'],['bad_minus_one','-1e+000'],
  ['bad_even','0e+000'],['bad_exponent_suffix','1e+000a']];
 for(const [name,tok] of negatives)execute(name,mutate(tok),false);
 const raw={id:'LSPV1-622',checker_git_blob:'338305c0ce101704205e57543756b8127074a986',
  checker_sha256:hash(checker),seed_git_blob:gitHash(seed),seed_sha256:hash(seed),
  status:'PROVED/RESTRICTED (source argument) and COMPUTATIONAL (OS Node finite corpus)',
  k_values:ks,positive:ks.length,negative:negatives.length,base_bytes:seed.length,
  original_source_reused:true,original_checker_unchanged:true,scope:'archived /386 SOURCE/DEF/RES only',
  empirical_caveat:'ECMAScript implementations have finite memory and maximum-string limits; all-k ideal grammar claim is qualified.',
  cases};
 fs.mkdirSync(path.dirname(output),{recursive:true});
 fs.writeFileSync(output,JSON.stringify(raw,null,2)+'\n');
 console.log(JSON.stringify({id:raw.id,positive:raw.positive,negative:raw.negative,paid:32,pass:true,output}));
}finally{fs.rmSync(temp,{recursive:true,force:true});}
