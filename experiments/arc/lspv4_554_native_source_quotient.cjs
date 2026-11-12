'use strict';
// LSPV-4/554: independent OS reproduction of signed SOURCE-value bypass on /386.
// Run from a full j15marti/pnp checkout: node experiments/arc/lspv4_554_native_source_quotient.cjs
const fs=require('fs'),path=require('path'),os=require('os'),cp=require('child_process'),assert=require('assert'),vm=require('vm');
const root=path.resolve(__dirname,'../..');
const checkerPath=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const sourcePath=path.join(root,'results/raw/arc/2026-11-11_1636_LSPV4_553_PRUNED_SHARED_NATIVE_W43.json');
const checker=fs.readFileSync(checkerPath,'utf8');
const baseline=JSON.parse(fs.readFileSync(sourcePath,'utf8'));
const copy=o=>JSON.parse(JSON.stringify(o));
const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const aliases=new Map([[24,0],[27,3],[30,5],[33,6]]);
for (const [i,j] of aliases)assert(eq(baseline.records[i].c,baseline.records[j].c),'not identical signed source');
const keep=baseline.records.map((_,i)=>i).filter(i=>i<17||i>33);
const index=new Map(keep.map((old,now)=>[old,now]));
const records=keep.map(old=>{
  const r=copy(baseline.records[old]);
  r.parents=r.parents.map(p=>{
    const v=index.get(aliases.get(p)??p);
    assert(Number.isSafeInteger(v),'dangling parent '+p);
    return v;
  });
  return r;
});
function packet(n){
  const d=copy(baseline);
  d.records=records;
  d.gate_defs=d.gate_defs.slice(0,n);
  d.summary={source:49,def_views:0,resolution:28,paid_gates:n,paid_total:28+n,live_records:77};
  assert.strictEqual(d.records.filter(r=>r.kind==='SOURCE').length,49);
  assert.strictEqual(d.records.filter(r=>r.kind==='RES').length,28);
  return d;
}
const cases=[['original_W43',baseline,true],['two_owners_W30',packet(2),true],['one_owner_W29',packet(1),true],['zero_owners_W28_wrapper_reject',packet(0),false]];
function change(name,fn){const d=packet(1);fn(d);cases.push([name,d,false]);}
change('underpay',d=>{d.summary.paid_total=28});
change('forged_source',d=>{d.records[0].c=[-1,2,3,-19]});
change('bad_pivot',d=>{d.records.at(-1).pivot=999999});
change('dangling_parent',d=>{d.records.at(-1).parents[0]=9999});
change('wrong_terminal',d=>{d.records.at(-1).c=[21]});
change('duplicate_source',d=>{d.records[1].c=d.records[0].c.slice();d.records[1].source=d.records[0].source});
change('wrong_parent',d=>{const i=d.records.findIndex(r=>r.kind==='RES');d.records[i].parents[0]=16});
change('bad_gate',d=>{d.gate_defs[0][2]=19});
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-lspv4-554-'));
const results=[];
try {
 for (const [name,dat,want] of cases){
   const file=path.join(tmp,name+'.json');
   fs.writeFileSync(file,JSON.stringify(dat)+'\n','utf8');
   const x=cp.spawnSync(process.execPath,[checkerPath,file],{encoding:'utf8',timeout:25000});
   const accept=x.status===0;
   assert.strictEqual(accept,want,name+': '+x.stderr);
   results.push({name,accept,want,bytes:fs.statSync(file).size,stdout:x.stdout.trim(),stderr:accept?'':x.stderr.trim().slice(0,500)});
 }
 const code=checker.slice(0,checker.indexOf('function corrupt('));
 assert(code.includes('function checkProof('),'missing original core');
 const core=vm.runInNewContext(code+'\ncheckProof;', {require,console,structuredClone});
 assert.strictEqual(core(packet(0)).paid,28,'zero-owner mathematical core must accept');
 console.log(JSON.stringify({status:'PASS',checker:'experiments/arc/lspv2_386_independent_verify.js',source:'results/raw/arc/2026-11-11_1636_LSPV4_553_PRUNED_SHARED_NATIVE_W43.json',cases:results.length,results,core_W28_accept:true,source_aliases:[...aliases]},null,2));
} finally {fs.rmSync(tmp,{recursive:true,force:true})}
