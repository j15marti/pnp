#!/usr/bin/env node
'use strict';
// LSPV-3/593A. Run from a complete j15marti/pnp checkout:
// node experiments/arc/lspv3_593a_native386_source_port_replay.cjs [raw.json]
// Executes the UNCHANGED original archived /386 checker in OS Node.
// Neither this script nor the checker authenticates full R_mix341.
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const crypto=require('node:crypto'),cp=require('node:child_process');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const files={
 checker:'experiments/arc/lspv2_386_independent_verify.js',
 original:'results/raw/arc/2026-11-12_0424_LSPV3_587_NATIVE_CONSTANT_FACET_ACCEPTED_PACKET.json',
 k4:'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json',
 single:'results/raw/arc/2026-11-12_1024_LSPV3_593A_NATIVE386_SINGLE_SOURCE_PORT_W30_ACCEPTED.json',
 all:'results/raw/arc/2026-11-12_1024_LSPV3_593A_NATIVE386_ALL16_SOURCE_PORTS_W45_ACCEPTED.json'
};
const pins={
 checker:'338305c0ce101704205e57543756b8127074a986',
 original:'4177ec15a0c7253378d5652a6b13b7152601d300',
 k4:'fe27fe1011d0021e721ccaeb747ed58da65d7464',
 single:'ea831cad5138c921f90ec28efa5e62a6ff6ec98a',
 all:'c349e037c31ee4aa5293c89d0f5696bf1253dad5'
};
const blob=b=>crypto.createHash('sha1')
 .update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
for(const [key,name] of Object.entries(files))
 assert.equal(blob(fs.readFileSync(path.join(root,name))),pins[key],key+' Git blob');
const read=k=>JSON.parse(fs.readFileSync(path.join(root,files[k]),'utf8'));
const p=read('original'),single=read('single'),all=read('all');
const clone=x=>JSON.parse(JSON.stringify(x));
const sign=c=>c.slice().sort((a,b)=>a-b).join(',');
const k4=new Set(read('k4').fixtures.find(f=>f.graph.name==='K4')
 .clauses.map(c=>sign(c.literals)));
const guard=p.spec.guard,gi=p.records.findIndex(r=>r.kind==='SOURCE'&&r.source===-1);
const source=p.records.map((r,i)=>({...r,index:i}))
 .filter(r=>r.kind==='SOURCE'&&r.source!==-1);
assert.equal(gi,17);assert.equal(source.length,16);assert.equal(k4.size,16);
const port=source.map(r=>({kind:'RES',c:r.c.filter(x=>x!==-guard),
 parents:[gi,r.index],pivot:guard}));
assert.deepEqual(new Set(port.map(r=>sign(r.c))),k4);
const insert=xs=>{
 const out=clone(p);
 out.records.splice(out.records.length-1,0,...xs);
 out.summary.resolution+=xs.length;out.summary.paid_total+=xs.length;
 out.summary.live_records+=xs.length;
 return out;
};
assert.deepEqual(single,insert([port[0]]));
assert.deepEqual(all,insert(port));
const scenarios=[
 ['baseline',p,true,29],
 ['one-guard-port',single,true,30],
 ['all-16-guard-ports',all,true,45],
 ['bad-parent-order',(()=>{let x=clone(single);x.records.at(-2).parents.reverse();return x})(),false],
 ['bad-resolvent',(()=>{let x=clone(single);x.records.at(-2).c=[1,2,-3];return x})(),false],
 ['bad-pivot',(()=>{let x=clone(single);x.records.at(-2).pivot=6;return x})(),false],
 ['underpayment',(()=>{let x=clone(all);x.summary.paid_total--;return x})(),false],
 ['forged-original',(()=>{let x=clone(all);x.records[1].c=[1,2,4,-7];return x})(),false]
];
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-593a-'));
function check(packet){
 const f=path.join(dir,'packet.json');fs.writeFileSync(f,JSON.stringify(packet)+'\n');
 const x=cp.spawnSync(process.execPath,[path.join(root,files.checker),f],
  {encoding:'utf8',timeout:30000,maxBuffer:32000000});
 if(x.error)throw x.error;
 if(x.status!==0)return {accepted:false,diagnostic:x.stderr.slice(-180)};
 const o=JSON.parse(x.stdout);
 return {accepted:true,assertions:o.assertions,paid:o.paid,res:o.res,
   records:o.records,negativeTests:o.negativeTests};
}
let results;
try {
 results=scenarios.map(([name,packet,expected,cost])=>{
   const out=check(packet);assert.equal(out.accepted,expected,name);
   if(expected)assert.equal(out.paid,cost,'exact cost '+name);
   return {name,...out};
 });
}finally{fs.rmSync(dir,{recursive:true,force:true})}
assert.equal(results[1].assertions,3185);
assert.equal(results[2].assertions,4085);
const raw={id:'LSPV-3/593A',mode:'DIRECT OS NODE ORIGINAL ARCHIVED 386',
 status:'PASS; native source-port Resolution only',signed_source_match:16,
 checker_blob:pins.checker,results,
 limit:'No authentic cross-checker RES-to-AND3 or full R_mix341 step'};
if(process.argv[2])fs.writeFileSync(path.resolve(process.argv[2]),
 JSON.stringify(raw,null,2)+'\n');
console.log(JSON.stringify(raw,null,2));
