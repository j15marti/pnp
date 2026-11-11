'use strict';
/* LSPV-3/579. Original /386 checker OS CLI reproducer; no surrogate calculus. */
const fs=require('fs'),path=require('path'),os=require('os'),cp=require('child_process');
const crypto=require('crypto'),assert=require('assert/strict');
const root=path.resolve(__dirname,'../..');
const seedFile=path.join(root,'results/raw/arc/2026-11-11_1324_LSPV3_577_LIVE_COMPLEMENTARY_NATIVE386_PACKET.json');
const checkerFile=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const PINS={seed:'5edeac8fbbe39764cfd3d075acd3c6ce7b5c87fe',checker:'338305c0ce101704205e57543756b8127074a986'};
function gitBlob(buf){return crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+buf.length+'\0'),buf])).digest('hex');}
const seedBytes=fs.readFileSync(seedFile),checkerBytes=fs.readFileSync(checkerFile);
assert.equal(gitBlob(seedBytes),PINS.seed);assert.equal(gitBlob(checkerBytes),PINS.checker);
const seed=JSON.parse(seedBytes),copy=x=>JSON.parse(JSON.stringify(x));
function key(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);}
function build(m){
  assert(Number.isInteger(m)&&m>=1&&m<=4);
  const d=copy(seed),cut=25,selected=[3,5,6].slice(0,m-1),extra=[],targets={};
  for(const s of selected){
    const C=seed.records[s].c;assert(C.includes(1));const D=C.filter(x=>x!==1);
    const a=cut+extra.length;
    extra.push({kind:'RES',c:key([...D,21,22]),parents:[s,20],pivot:1},
      {kind:'RES',c:key([...D,22]),parents:[a,19],pivot:21},
      {kind:'RES',c:key(C),parents:[a+1,21],pivot:22});
    targets[s]=a+2;
  }
  const oldTail=seed.records.slice(cut).map(o=>({
    ...o,parents:o.parents.map(p=>Object.hasOwn(targets,p)?targets[p]:(p>=cut?p+extra.length:p))
  }));
  d.records=[...seed.records.slice(0,cut),...extra,...oldTail];
  d.summary.resolution+=extra.length;d.summary.paid_total+=extra.length;
  d.summary.live_records+=extra.length;
  return d;
}
function ancestors(d){const seen=new Set(),q=[d.records.length-1];while(q.length){
  const k=q.pop();if(seen.has(k))continue;seen.add(k);
  for(const parent of d.records[k].parents)q.push(parent);
}return seen;}
function runOriginal(d){
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-579-'));
  try{
    const p=path.join(dir,'candidate.json');fs.writeFileSync(p,JSON.stringify(d)+'\n');
    const out=cp.spawnSync(process.execPath,[checkerFile,p],{encoding:'utf8',timeout:25000});
    if(out.error)throw out.error;
    return {accept:out.status===0,stdout:out.stdout,stderr:out.stderr,status:out.status};
  }finally{fs.rmSync(dir,{recursive:true,force:true});}
}
const positives=[];
for(let m=1;m<=4;m++){
  const d=build(m),r=runOriginal(d),anc=ancestors(d);
  const live=[17,18,19,20,21,22,23,24,...Array.from({length:3*(m-1)},(_,i)=>25+i)];
  assert(r.accept,'original checker rejected m='+m+': '+r.stderr);
  const v=JSON.parse(r.stdout.trim());
  assert.equal(v.negativeTests,11);assert.equal(v.paid,32+3*m);
  assert(live.every(i=>anc.has(i)));
  assert.deepEqual(d.records.filter(x=>x.kind==='SOURCE'),seed.records.filter(x=>x.kind==='SOURCE'));
  positives.push({m,paid:v.paid,records:d.records.length,original_assertions:v.assertions,
    live_macro_records:live.length,utf8_bytes:Buffer.byteLength(JSON.stringify(d)+'\n')});
}
const attacks=[
 ['wrong_first_pivot',d=>{d.records[25].pivot=2}],
 ['pivot_orientation',d=>{d.records[25].parents=[20,3]}],
 ['forged_original_source',d=>{d.records[3].c[0]=-1}],
 ['bad_def_facet',d=>{d.records[20].c=[-1,21,-22]}],
 ['future_parent',d=>{d.records[25].parents[0]=60}],
 ['underpaid_shared_work',d=>{d.summary.paid_total--}],
 ['wrong_copied_clause',d=>{d.records[27].c=d.records[27].c.filter(x=>x!==-19)}],
 ['wrong_shared_false_unit',d=>{d.records[19].c=[21]}],
 ['invalid_facet_owner',d=>{d.records[20].gate=999}]
];
const negative=[];
for(const [name,mutate] of attacks){const d=build(4);mutate(d);
  const r=runOriginal(d);assert(!r.accept,'original checker accepted hostile '+name);
  negative.push({name,rejected:true});
}
console.log(JSON.stringify({status:'PASS',checker_blob:PINS.checker,seed_blob:PINS.seed,
  original_checker_OS_execution:true,positives,negative,logical_cost_model:'count-once owners plus paid RES, not CPU time'},null,2));