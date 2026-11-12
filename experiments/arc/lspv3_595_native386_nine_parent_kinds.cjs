'use strict';
// LSPV-3/595, original OS Node/CLI replay, no third-party dependencies.
// Run from any directory: node experiments/arc/lspv3_595_native386_nine_parent_kinds.cjs
// Uses ORIGINAL archived /386 checker, not an independent acceptance emulator.
const fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process');
const os=require('node:os'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const original=path.join(root,'results/raw/arc/2026-11-12_0424_LSPV3_587_NATIVE_CONSTANT_FACET_ACCEPTED_PACKET.json');
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const expected={seed:'4177ec15a0c7253378d5652a6b13b7152601d300',checker:'338305c0ce101704205e57543756b8127074a986'};
function gitBlob(b){return crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\\0'),b])).digest('hex');}
for(const [p,id] of [[original,expected.seed],[checker,expected.checker]]) assert.equal(gitBlob(fs.readFileSync(p)),id,'immutable upstream blob drift');
const base=JSON.parse(fs.readFileSync(original,'utf8'));
function canonical(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);}
function construct(base){
 const p=JSON.parse(JSON.stringify(base));const end=p.records.pop();
 p.records.push({kind:'DEF',gate:0,c:[-1,-8],parents:[]}); // new 45, authentic free facet
 function add(i,j,pivot){
  const A=p.records[i].c,B=p.records[j].c;
  assert(A.includes(pivot)&&B.includes(-pivot),'invalid signed pivot');
  const c=canonical([...A.filter(x=>x!==pivot),...B.filter(x=>x!==-pivot)]);
  assert(!c.some(x=>c.includes(-x)),'tautological resolvent');
  p.records.push({kind:'RES',parents:[i,j],pivot,c});return p.records.length-1;
 }
 assert.equal(add(2,10,-2),46);     // SOURCE/SOURCE, generator
 assert.equal(add(0,46,1),47);       // DEF/RES
 assert.equal(add(46,0,-1),48);      // RES/DEF
 assert.equal(add(0,45,1),49);       // DEF/DEF
 assert.equal(add(1,45,1),50);       // SOURCE/DEF
 assert.equal(add(0,2,1),51);        // DEF/SOURCE
 p.records.push(end);p.summary.def_views++;p.summary.resolution+=6;
 p.summary.paid_total+=6;p.summary.live_records+=7;
 return p;
}
function kindMatrix(p){
 const r={};
 for(const n of p.records)if(n.kind==='RES'){
  const k=p.records[n.parents[0]].kind+'/'+p.records[n.parents[1]].kind;
  r[k]=(r[k]||0)+1;
 }
 return r;
}
const packet=construct(base),matrix=kindMatrix(packet);
assert.equal(Object.keys(matrix).length,9);assert.equal(packet.summary.paid_total,35);
assert.equal(packet.records.length,53);
assert.deepEqual(packet.spec,base.spec);assert.deepEqual(packet.gate_defs,base.gate_defs);
assert.deepEqual(packet.records.filter(x=>x.kind==='SOURCE'),base.records.filter(x=>x.kind==='SOURCE'));
const dst=process.argv[2]||path.join(root,'results/raw/arc/2026-11-12_1230_LSPV3_595_NINE_KINDS_ACCEPTED.json');
const rawDst=process.argv[3]||path.join(root,'results/raw/arc/2026-11-12_1230_LSPV3_595_NINE_KINDS_OS_REPLAY.json');
fs.mkdirSync(path.dirname(dst),{recursive:true});
const blob=JSON.stringify(packet)+'\n';fs.writeFileSync(dst,blob);
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3_595_'));
const rows=[];let failures=0;
try{
 function run(name,obj,want){
  const f=path.join(tmp,name+'.json');fs.writeFileSync(f,JSON.stringify(obj)+'\n');
  const r=cp.spawnSync(process.execPath,[checker,f],{encoding:'utf8',timeout:25000,maxBuffer:2**22});
  const accepted=r.status===0;
  assert.equal(accepted,want,'original checker verdict for '+name+' '+r.stderr);
  let result=accepted?JSON.parse(r.stdout):null;
  if(accepted){assert.equal(result.negativeTests,11);if(name==='complete_nine_kind_W35')assert.equal(result.paid,35);}
  else failures++;
  rows.push({name,accepted,expected_accept:want,assertions:result?.assertions??null,
   rejection:accepted?null:r.stderr.slice(0,280),
   sha256:crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex')});
 }
 run('original_W29',base,true);run('complete_nine_kind_W35',packet,true);
 const corrupt=[
 ['bad_facet',p=>p.records[45].c=[-1,8]],
 ['bad_res_pivot',p=>p.records[47].pivot=-1],
 ['future_parent',p=>p.records[47].parents[1]=52],
 ['underpaid',p=>p.summary.paid_total--],
 ['forged_source',p=>p.records[1].c=[-1,2,3,-7]],
 ['false_terminal',p=>p.records.at(-1).c=[-7]]
 ];
 for(const [name,fn] of corrupt){const p=JSON.parse(JSON.stringify(packet));fn(p);run(name,p,false);}
 assert.equal(failures,6);
 const data={id:'LSPV-3/595',execution:'real OS Node subprocess original checker',
   checker_blob:expected.checker,seed_blob:expected.seed,matrix,rows,
   logical_paid_work:{original:29,extended:35},
   source_sha256:crypto.createHash('sha256').update(JSON.stringify(packet.records.filter(r=>r.kind==='SOURCE'))).digest('hex'),
   accepted_sha256:crypto.createHash('sha256').update(blob).digest('hex')};
 fs.mkdirSync(path.dirname(rawDst),{recursive:true});fs.writeFileSync(rawDst,JSON.stringify(data,null,2)+'\n');
 console.log(JSON.stringify({status:'PASS',positive:2,hostile_rejected:6,matrix_kinds:Object.keys(matrix).length,
  sha256:data.accepted_sha256,raw:rawDst}));
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
