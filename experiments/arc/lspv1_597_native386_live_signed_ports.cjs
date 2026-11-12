#!/usr/bin/env node
'use strict';
// LSPV-1/597: run from the j15marti/pnp repository root.
// node experiments/arc/lspv1_597_native386_live_signed_ports.cjs [raw.json]
// Authenticates original archived /386, not full historical R_mix341.
const assert=require('node:assert/strict'),fs=require('node:fs'),
 os=require('node:os'),path=require('node:path'),cp=require('node:child_process'),
 crypto=require('node:crypto');
const root=path.resolve(__dirname,'../..');
const paths={
 checker:'experiments/arc/lspv2_386_independent_verify.js',
 seed:'results/raw/arc/2026-11-12_0424_LSPV3_587_NATIVE_CONSTANT_FACET_ACCEPTED_PACKET.json',
 k4:'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json',
 witness:'results/raw/arc/2026-11-12_1100_LSPV1_597_NATIVE386_LIVE16_W44_ACCEPTED.json'
};
const pins={
 checker:'338305c0ce101704205e57543756b8127074a986',
 seed:'4177ec15a0c7253378d5652a6b13b7152601d300',
 k4:'fe27fe1011d0021e721ccaeb747ed58da65d7464',
 witness:'a9514ed6d28d19403d745a583c3096d36cd1a399'
};
const gitBlob=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
for(const [k,f] of Object.entries(paths))
 assert.equal(gitBlob(fs.readFileSync(path.join(root,f))),pins[k],'pin '+k);
const read=k=>JSON.parse(fs.readFileSync(path.join(root,paths[k]),'utf8'));
const clone=x=>JSON.parse(JSON.stringify(x));
const seed=read('seed'),guard=seed.spec.guard;
const K4=read('k4').fixtures.find(f=>f.graph.name==='K4');
const sig=c=>c.slice().sort((a,b)=>a-b).join(',');
const exact=new Set(K4.clauses.map(c=>sig(c.literals)));
const sources=seed.records.map((r,i)=>({r,i})).filter(x=>x.r.kind==='SOURCE'&&x.r.source!==-1);
const unit=seed.records.findIndex(r=>r.kind==='SOURCE'&&r.source===-1);
assert.equal(unit,17);assert.equal(sources.length,16);assert.equal(exact.size,16);
const ports=sources.map(({r,i})=>({kind:'RES',c:r.c.filter(x=>x!==-guard),parents:[unit,i],pivot:guard}));
for(const p of ports)assert(exact.has(sig(p.c)),'signed K4 source mismatch');
const packet=clone(seed);packet.records=clone(seed.records.slice(0,18)).concat(ports);
const map=new Map(sources.map(({i},j)=>[i,18+j]));
for(let i=18;i<=44;i++)map.set(i,i+16);
for(let i=18;i<=44;i++){
 const r=seed.records[i];
 assert.equal(r.kind,'RES');
 assert(r.c.includes(-guard)&&r.pivot!==guard,'guarded proof-cone precondition');
 packet.records.push({...r,c:r.c.filter(x=>x!==-guard),
  parents:r.parents.map(j=>map.has(j)?map.get(j):j)});
}
packet.summary={...seed.summary,resolution:43,paid_total:44,live_records:61};
assert.deepEqual(packet,read('witness'));
assert.equal(packet.records.length,61);
assert.deepEqual(packet.records.at(-1).c,[]);
const ancestor=new Set();
function visit(i){if(ancestor.has(i))return;ancestor.add(i);
 for(const j of packet.records[i].parents){assert(j>=0&&j<i);visit(j)}}
visit(60);assert.equal(ancestor.size,60);
for(let i=18;i<34;i++)assert(ancestor.has(i),'paid port not terminal live');
let sat=0;for(let mask=0;mask<64;mask++){
 const v=lit=>Boolean((mask>>(Math.abs(lit)-1))&1)===(lit>0);
 if(K4.clauses.every(c=>c.literals.some(v)))sat++;
}assert.equal(sat,0);
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv1-597-')),tests=[];
function native(name,data,expect,cost){
 const fn=path.join(dir,'packet.json');fs.writeFileSync(fn,JSON.stringify(data)+'\n');
 const r=cp.spawnSync(process.execPath,[path.join(root,paths.checker),fn],
  {encoding:'utf8',timeout:30000,maxBuffer:32*1024*1024});
 if(r.error)throw r.error;
 const yes=r.status===0;assert.equal(yes,expect,name+' native verdict: '+r.stderr.slice(-250));
 const row={name,accepted:yes};
 if(yes){const x=JSON.parse(r.stdout);assert.equal(x.paid,cost);
  assert.equal(x.negativeTests,11);
  Object.assign(row,{paid:x.paid,RES:x.res,owners:x.def,records:x.records,
   assertions:x.assertions,oddModels:x.oddModels,evenModels:x.evenModels});
 }else row.error=r.stderr.trim().slice(-150);
 tests.push(row);
}
try{
 native('live16-W44',packet,true,44);
 let x=clone(packet);x.records[18].c[0]*=-1;native('bad-port-sign',x,false);
 x=clone(packet);x.records[18].pivot=1;native('bad-port-pivot',x,false);
 x=clone(packet);x.records[18].parents.reverse();native('bad-parent-orientation',x,false);
 x=clone(packet);x.records[18].parents[1]=x.records[19].parents[1];native('bad-source-parent',x,false);
 x=clone(packet);x.records[34].parents[0]=1;native('bad-live-consumer',x,false);
 x=clone(packet);x.records[60].c=[-guard];native('bad-terminal',x,false);
 x=clone(packet);x.summary.paid_total=43;native('underpay',x,false);
 x=clone(packet);x.spec.charge[0]^=1;native('forged-charge',x,false);
 x=clone(packet);x.records[1].c=[1,2,4,-guard];native('forged-source',x,false);
}finally{fs.rmSync(dir,{recursive:true,force:true})}
const raw={id:'LSPV-1/597',scope:'exact original archived /386 SOURCE/DEF/RES; NOT full R_mix341',
 mode:'OS Node unchanged original checker',status:'PASS',node_version:process.version,
 pins,certificate:{original_source_clauses:17,new_live_ports:16,ancestor_nodes:60,
 paid_RES:43,paid_owner:1,paid_W:44,records:61,K4_sat_models:sat},tests,
 limitations:['finite W44 is a legal upper witness, not optimality',
 'dead paid owner is retained for archived CLI sentinel',
 'no original mixed RES to AND3 consumer; P versus NP OPEN']};
if(process.argv[2])fs.writeFileSync(path.resolve(process.argv[2]),JSON.stringify(raw,null,2)+'\n');
console.log(JSON.stringify(raw,null,2));
