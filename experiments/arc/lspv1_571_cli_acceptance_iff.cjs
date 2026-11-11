#!/usr/bin/env node
'use strict';
// LSPV-1/571. Run from repository root:
// node experiments/arc/lspv1_571_cli_acceptance_iff.cjs
// Optionally: node experiments/arc/lspv1_571_cli_acceptance_iff.cjs --write /tmp/lspv1_571_os.json
// The original /386 checker runs unchanged in a real Node subprocess for CLI tests;
// its unchanged checkProof is called through node:vm for mathematical/core tests.
const fs=require('node:fs'), path=require('node:path'), os=require('node:os'),
      vm=require('node:vm'), cp=require('node:child_process'),
      crypto=require('node:crypto'), assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const cases=[
 ['core28','results/raw/arc/2026-11-11_0203_LSPV1_568_K4_DP_CORE28.json','c68eeaf67015416dae49a34ad5ce25432b839bee',true,false],
 ['cli29','results/raw/arc/2026-11-11_0203_LSPV1_568_K4_DP_CLI29.json','e3eb2a46857776089ab83f4ad50159ef622d2869',true,true],
 ['positive_sentinel','results/raw/arc/2026-11-11_0057_LSPV1_567_PIVOT999999_CORE_ONLY_PACKET.json','b2216a95f65d765028410ec3db9520dfcb104015',true,false],
 ['negative_sentinel','results/raw/arc/2026-11-11_0057_LSPV1_567_NEGATIVE_PIVOT_CLI_ACCEPT_PACKET.json','717970007a1988cda31b70ac5abce8fd81519f4c',true,true],
 ['relabel_even_control','results/raw/arc/2026-11-10_2303_LSPV1_565_ARCHIVED_386_RELABEL_CORE_ACCEPT_CLI_REJECT.json','5f8236b622fe340e1d485dd32be4b987cc158c84',false,false]
];
const blob=s=>crypto.createHash('sha1').update(Buffer.concat([
  Buffer.from('blob '+Buffer.byteLength(s)+'\0'),Buffer.from(s)])).digest('hex');
const original=fs.readFileSync(checker,'utf8');
assert.equal(blob(original),'338305c0ce101704205e57543756b8127074a986');
function coreAccept(payload){
 const context={require,structuredClone,console:{log(){}},process:{argv:[process.execPath,checker]},__payload:payload};
 try{
   vm.runInNewContext(original+'\nglobalThis.__verdict=checkProof(__payload,{control:true});',context,{timeout:10000});
   return {accept:true,paid:context.__verdict.paid};
 }catch(e){return {accept:false,error:String(e.message||e)};}
}
const workDir=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-571-'));
function nativeCli(raw){
 const file=path.join(workDir,'packet.json');fs.writeFileSync(file,raw);
 const z=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',timeout:10000,maxBuffer:20000000});
 if(z.error)throw z.error;
 if(z.status===0){const j=JSON.parse(z.stdout);return {accept:true,assertions:j.assertions,paid:j.paid};}
 const errors=(z.stderr||'').split('\n').filter(s=>s.includes('Error:'));
 return {accept:false,error:errors[0]||'nonzero exit '+z.status};
}
const deep=x=>JSON.parse(JSON.stringify(x)), test=[];
function run(name,p,raw,expectCore,expectCli,origin){
 const core=coreAccept(p),cli=nativeCli(raw);
 const predicted=core.accept&&Array.isArray(p.gate_defs)&&p.gate_defs.length>0&&p.records.at(-1).pivot!==999999;
 assert.equal(core.accept,expectCore,name+' core expectation');
 assert.equal(cli.accept,expectCli,name+' CLI expectation');
 assert.equal(cli.accept,predicted,name+' equivalence');
 test.push({name,origin,core,cli,predicted,paid_owners:p.gate_defs.length,
   final_pivot:p.records.at(-1).pivot,raw_bytes:Buffer.byteLength(raw)});
}
let seed;
try {
 for(const [name,filepath,expectedSHA,expectedCore,expectedCli] of cases){
  const raw=fs.readFileSync(path.join(root,filepath),'utf8');
  assert.equal(blob(raw),expectedSHA,filepath+' changed');
  const p=JSON.parse(raw);
  run(name,p,raw,expectedCore,expectedCli,filepath);
  if(name==='cli29')seed=p;
 }
 function altered(name,mutator,ec,el){
  const p=deep(seed);mutator(p);run(name,p,JSON.stringify(p),ec,el,'transformation of cli29');
 }
 altered('nested_unused_owner',p=>{p.gate_defs.push([1,9,8,2]);p.summary.paid_gates++;p.summary.paid_total++;},true,true);
 altered('safe_owner_id_999999',p=>{p.gate_defs[0][0]=999999;},true,true);
 altered('reverse_final_orientation',p=>{p.records.at(-1).parents.reverse();p.records.at(-1).pivot*=-1;},true,true);
 altered('underpaid_summary',p=>{p.summary.paid_total--;},false,false);
 altered('zero_source_literal',p=>{p.records[0].c=[0];},false,false);
 altered('invalid_final_pivot_999999',p=>{p.records.at(-1).pivot=999999;},false,false);
 altered('even_charge',p=>{p.spec.charge[0]=0;},false,false);
}finally{fs.rmSync(workDir,{recursive:true,force:true});}
const out={result:'LSPV1-571 full original /386 CLI acceptance iff controlled core AND positive owner count AND final pivot !=999999',
 model:'pinned archived /386 only; NOT full historical R_mix341',
 node_version:process.version,checker_blob:blob(original),case_count:test.length,all_conditions_match:true,
 accepted_cli:test.filter(x=>x.cli.accept).length, accepted_core:test.filter(x=>x.core.accept).length,
 counted_original_cli_assertions:test.reduce((a,b)=>a+(b.cli.assertions||0),0),tests:test,
 status:'PROVED/RESTRICTED theorem, COMPUTATIONAL native OS regression; P versus NP OPEN'};
const i=process.argv.indexOf('--write');if(i>=0){assert(process.argv[i+1],'--write needs path');fs.writeFileSync(process.argv[i+1],JSON.stringify(out,null,2)+'\n');}
console.log(JSON.stringify(out,null,2));
