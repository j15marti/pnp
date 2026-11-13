#!/usr/bin/env node
'use strict';
// LSPV-2/600 original-/386 restricted reemission reproducer.
// Not an authoritative R_mix341 checker.
// Usage: node experiments/arc/lspv2_600_facet_reemission.cjs REPO_ROOT OUTPUT_DIR
const fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(process.argv[2]||'.'),out=path.resolve(process.argv[3]||'/tmp/lspv2_600');
fs.mkdirSync(out,{recursive:true});
const get=p=>fs.readFileSync(path.join(root,p));
const sum=b=>crypto.createHash('sha256').update(b).digest('hex'),copy=x=>JSON.parse(JSON.stringify(x));
const checker='experiments/arc/lspv2_386_independent_verify.js';
assert.equal(sum(get(checker)),'22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113');
const src=get('results/raw/arc/574_k01_SIGNED_SOURCE.cnf');
assert.equal(sum(src),'3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c');
const old=JSON.parse(get('results/raw/arc/2026-11-13_0612_LSPV2_599_W32_source-first_source-first.json').toString());
// If the /599 standalone packet is not published under this filename,
// copy the exact /599 archive file W32_source-first_source-first.json to that path.
assert.equal(old.summary.paid_total,32);
assert(old.records.slice(0,17).every(r=>r.kind==='SOURCE'));
assert(old.records.slice(17,19).every(r=>r.kind==='DEF'));
assert(old.records.slice(19).every(r=>r.kind==='RES'));
const external=src.toString().trim().split('\n').slice(1).map(x=>x.split(/\s+/).slice(0,-1).map(Number));
const norm=x=>x.map(y=>JSON.stringify(y)).sort();
assert.deepEqual(norm(old.records.slice(0,17).map(r=>r.c)),norm(external));
function build(M,reissue){
 const d=copy(old);d.records=copy(old.records.slice(0,17));
 const facets=new Map(),blocks=[];
 for(let b=0;b<M;b++){
  const rel=new Map(Array.from({length:17},(_,i)=>[i,i]));
  for(let i=19;i<50;i++){
   const r=copy(old.records[i]);r.parents=r.parents.map(p=>{
    if(p<17)return p;
    if(p<19){
     const id=reissue?b+':'+p:String(p);
     if(!facets.has(id)){facets.set(id,d.records.length);d.records.push(copy(old.records[p]));}
     return facets.get(id);
    }
    assert(rel.has(p));return rel.get(p);
   });
   const cur=d.records.length;d.records.push(r);rel.set(i,cur);
  }
  blocks.push(rel);
 }
 d.summary={source:17,def_views:2*(reissue?M:1),resolution:31*M,paid_gates:1,paid_total:31*M+1,live_records:d.records.length};
 const signatures=blocks.flatMap(rel=>Array.from({length:31},(_,z)=>{
  const i=z+19,r=d.records[rel.get(i)],o=old.records[i];
  assert.deepEqual(r.c,o.c);assert.equal(r.pivot,o.pivot);
  assert.deepEqual(r.parents.map(j=>d.records[j].c),o.parents.map(j=>old.records[j].c));
  return JSON.stringify([r.c,r.pivot,o.parents.map(j=>old.records[j].c)]);
 }));
 return {d,signatures};
}
function area(d){
 let j=0,occ=[];
 d.records.forEach((r,i)=>{
  if(r.kind==='DEF')occ.push({i,uses:[]});
  if(r.kind==='RES'){j++;for(const p of r.parents){const x=occ.find(x=>x.i===p);if(x)x.uses.push(j);}}
 });
 const profile=Array.from({length:j},(_,t)=>occ.filter(x=>x.uses.length&&x.uses[0]<=t+1&&x.uses.at(-1)>=t+1).length);
 return {peak:Math.max(...profile),area:profile.reduce((a,b)=>a+b,0),count:occ.length};
}
const cases=[],measure=[];
function run(name,d,expect){
 const bytes=Buffer.from(JSON.stringify(d)+'\n');const file=path.join(out,name+'.json');fs.writeFileSync(file,bytes);
 const res=cp.spawnSync(process.execPath,[path.join(root,checker),file],{encoding:'utf8',timeout:25000});
 assert.equal(res.status===0,expect,name+': '+res.stderr);
 cases.push({name,accept:expect,sha256:sum(bytes),bytes:bytes.length,original_assertions:expect?JSON.parse(res.stdout).assertions:0});
}
for(const M of [1,2,3,5,8]){
 const a=build(M,false),b=build(M,true);
 assert.deepEqual(a.signatures,b.signatures);
 const A=area(a.d),B=area(b.d);
 assert.equal(A.area,62*(M-1)+2);assert.equal(B.area,2*M);
 if(M>=2){assert.equal(A.peak,2);assert.equal(B.peak,1);}
 run('M'+M+'_shared',a.d,true);run('M'+M+'_reissued',b.d,true);
 measure.push({M,W:31*M+1,shared:A,reissued:B});
}
const baseline=build(3,true).d;
for(const [name,fn] of [
 ['bad_owner',d=>d.records.find(r=>r.kind==='DEF').gate=101],
 ['bad_facet',d=>d.records.find(r=>r.kind==='DEF').c=[999999]],
 ['forged_source',d=>d.records[0].c=[-d.spec.guard]],
 ['bad_pivot',d=>d.records.at(-1).pivot=3],
 ['future_parent',d=>d.records.at(-1).parents[0]=d.records.length],
 ['underpayment',d=>d.summary.paid_total--],
 ['unknown_DELETE',d=>d.records.find(r=>r.kind==='DEF').kind='DELETE']]){
 const d=copy(baseline);fn(d);run(name,d,false);
}
const raw={id:'LSPV2-600',checker_sha256:sum(get(checker)),source_sha256:sum(src),status:'PROVED/RESTRICTED + COMPUTATIONAL; full R_mix341 OPEN',measure,cases};
fs.writeFileSync(path.join(out,'LSPV2_600_RAW.json'),JSON.stringify(raw,null,2)+'\n');
console.log(JSON.stringify({pass:true,positive:10,negative:7,measure},null,2));
