'use strict';
// LSPV-3/599, 2026-11-12 16:28 PST.  Original /341 checker body is run verbatim
// via vm with fs/process/console adapters; this is NOT a reimplemented checker.
// Run at repository root:
// node experiments/arc/lspv3_599_native341_deletion_object_domain.cjs [output.json]
const fs=require('fs'),crypto=require('crypto'),vm=require('vm'),assert=require('assert');
const REPO='j15marti/pnp';
const sourcePath='experiments/arc/lspv2_341_independent_verify.js';
const packetPath='results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json';
const expectedSource='fcb7d4ced8f922de14c0bda16263a8cc7853e8e0';
const expectedPacket='fe27fe1011d0021e721ccaeb747ed58da65d7464';
const blob=x=>crypto.createHash('sha1').update('blob '+Buffer.byteLength(x)+'\0').update(x).digest('hex');
const script=fs.readFileSync(sourcePath,'utf8'),raw=fs.readFileSync(packetPath,'utf8');
assert.strictEqual(blob(script),expectedSource,'historical checker changed');
assert.strictEqual(blob(raw),expectedPacket,'historical packet changed');
const baseline=JSON.parse(raw),clone=x=>JSON.parse(JSON.stringify(x));
function run(data){
 let returned=null;
 try{
  vm.runInNewContext(script,{
   require:mod=>{if(mod!=='fs')throw Error('checker unexpectedly loaded '+mod);
      return {readFileSync:()=>JSON.stringify(data)};},
   process:{argv:['node',sourcePath,'virtual_input.json']},
   console:{log:s=>returned=JSON.parse(s)}
  },{timeout:300000,filename:sourcePath});
  if(!returned||!Number.isInteger(returned.checks))throw Error('missing native result');
  return {accepted:true,assertions:returned.checks,cases:returned.cases.length};
 }catch(e){return {accepted:false,error:String(e).slice(0,200)};}
}
function changeDeleted(f,{reverse=false,extra=false}={}){
 const items=f.deleted,keys=Array.from(items.keys());
 if(reverse)keys.reverse();
 const indexable={length:items.length};
 for(const i of keys)indexable[String(i)]=items[i];
 if(extra)indexable.outside={fake:'not a checked witness'};
 f.deleted=indexable;
}
function oneFixture(i){
 const d=clone(baseline);
 d.fixtures=[d.fixtures[i]];
 d.summary=[d.summary[i]];
 return d;
}
const reference=run(baseline);assert(reference.accepted);
const full=clone(baseline);full.fixtures.forEach(f=>changeDeleted(f));
const fullResult=run(full);assert(fullResult.accepted&&fullResult.assertions===reference.assertions);
const perFixture=baseline.fixtures.map((f,i)=>{
 const x=oneFixture(i);changeDeleted(x.fixtures[0]);
 const result=run(x);assert(result.accepted,'native fixture '+i);
 return {index:i,graph:f.graph.name,sources:f.clauses.length,paid:f.proof.length,
         deletedSlots:f.deleted.length,...result};
});
const altered=oneFixture(0);changeDeleted(altered.fixtures[0],{reverse:true,extra:true});
const extra=run(altered);assert(extra.accepted&&extra.assertions===perFixture[0].assertions);
const controls=[
 ['missing_first',x=>delete x.fixtures[0].deleted['0']],
 ['missing_last',x=>delete x.fixtures[0].deleted['15']],
 ['wrong_source',x=>x.fixtures[0].deleted['0'].sourceId='FORGED'],
 ['wrong_length_minus',x=>x.fixtures[0].deleted.length--],
 ['wrong_length_string',x=>x.fixtures[0].deleted.length='16'],
 ['null_container',x=>x.fixtures[0].deleted=null],
 ['arrayless_container',x=>x.fixtures[0].deleted={length:16}],
 ['wrong_source_index_swap',x=>{
   const v=x.fixtures[0].deleted[0];
   x.fixtures[0].deleted[0]=x.fixtures[0].deleted[1];
   x.fixtures[0].deleted[1]=v;
 }],
 ['wrong_witness_size',x=>{
   const k=Object.keys(x.fixtures[0].deleted).find(
     k=>k!=='length'&&x.fixtures[0].deleted[k]&&x.fixtures[0].deleted[k].assignment!==null);
   x.fixtures[0].deleted[k].assignment='101';
 }],
 ['not_object_slot',x=>x.fixtures[0].deleted['0']=0]
];
const negatives=controls.map(([name,fn])=>{
 const d=clone(altered);fn(d);const r=run(d);
 assert(!r.accepted,'hostile case accepted: '+name);
 return {name,...r};
});
const positives=[fullResult,...perFixture,extra];
const result={
 provenance:{sourcePath,sourceBlob:blob(script),packetPath,packetBlob:blob(raw),
   executed:'UNCHANGED archived checker in Node vm with input/output adapters',
   version:process.version,originalNativeRuleSet:'SOURCE/AND3/XOR only'},
 theorem:'Any accepted fixture with deletion array accepts its length-preserving JSON index-object re-encoding; checked deletion evidence remains source-indexed.',
 baseline:reference,wholeObject:fullResult,perFixture,reverseAndExtra:extra,negatives,
 totals:{positivePackets:positives.length,positiveOriginalAssertionGroups:positives.reduce((s,a)=>s+a.assertions,0),
    hostileRejected:negatives.length,fixtures:baseline.fixtures.length,
    separatePaidNodes:baseline.fixtures.reduce((s,f)=>s+f.proof.length,0)},
 scope:'Restricted /341 accepted-byte rule; NOT complete historical R_mix341; P2-D1/C3/B1 OPEN; P!=NP OPEN'
};
const target=process.argv[2];
if(target)fs.writeFileSync(target,JSON.stringify(result,null,2)+'\n');
process.stdout.write(JSON.stringify(result,null,2)+'\n');
