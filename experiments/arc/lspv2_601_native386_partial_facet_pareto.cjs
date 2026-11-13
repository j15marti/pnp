#!/usr/bin/env node
'use strict';
// LSPV-2/601. Exact original /386 restricted checker OS driver.
// NOT an R_mix341 checker. Usage: node experiments/arc/lspv2_601_native386_partial_facet_pareto.cjs [output_dir]
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),cp=require('node:child_process'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..'),out=path.resolve(process.argv[2]||path.join(os.tmpdir(),'lspv2_601'));
fs.mkdirSync(out,{recursive:true});
const read=p=>fs.readFileSync(path.join(root,p)),SHA=b=>crypto.createHash('sha256').update(b).digest('hex'),clone=x=>JSON.parse(JSON.stringify(x));
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedBytes=read('results/raw/arc/2026-11-13_0812_LSPV2_601_W32_NATIVE386_SEED.json');
const source=read('results/raw/arc/574_k01_SIGNED_SOURCE.cnf');
assert.equal(SHA(fs.readFileSync(checker)),'22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113');
assert.equal(SHA(seedBytes),'56222417e011357a9f7d141221b9e10b0e4eb230a05ebf6365e00b95ec9be238');
assert.equal(SHA(source),'3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c');
const seed=JSON.parse(seedBytes);assert.equal(seed.summary.paid_total,32);
assert.equal(seed.records.length,50);assert(seed.records.slice(0,17).every(r=>r.kind==='SOURCE'));
assert(seed.records.slice(17,19).every(r=>r.kind==='DEF'));
assert(seed.records.slice(19).every(r=>r.kind==='RES'));
const tokens=source.toString('utf8').trim().split(/\s+/);
assert.deepEqual(tokens.slice(0,4),['p','cnf','7','17']);
let external=[],partial=[];
for(const t of tokens.slice(4)){
 const n=Number(t);assert(Number.isSafeInteger(n)&&Math.abs(n)<=7);
 if(n===0){external.push(partial);partial=[];}else partial.push(n);
}
assert.equal(partial.length,0);assert.equal(external.length,17);
const signatures=rows=>rows.map(r=>JSON.stringify(r)).sort();
assert.deepEqual(signatures(seed.records.slice(0,17).map(r=>r.c)),signatures(external));
function construct(M,groupA,groupB){
 assert.equal(groupA.length,M);assert.equal(groupB.length,M);
 const d=clone(seed);d.records=clone(seed.records.slice(0,17));
 const views=[new Map(),new Map()];
 for(let b=0;b<M;b++){
  const mapped=new Map(Array.from({length:17},(_,i)=>[i,i]));
  for(let i=19;i<50;i++){
   const r=clone(seed.records[i]);
   r.parents=r.parents.map(p=>{
    if(p<17)return p;
    if(p<19){
     const j=p-17,key=(j===0?groupA:groupB)[b];
     if(!views[j].has(key)){views[j].set(key,d.records.length);d.records.push(clone(seed.records[p]));}
     return views[j].get(key);
    }
    assert(mapped.has(p));return mapped.get(p);
   });
   const current=d.records.length;d.records.push(r);mapped.set(i,current);
  }
 }
 d.summary={source:17,def_views:views[0].size+views[1].size,resolution:31*M,
  paid_gates:1,paid_total:31*M+1,live_records:d.records.length};
 return d;
}
function profile(d){
 let step=0;const uses=new Map();
 d.records.forEach((r,i)=>{
  if(r.kind==='DEF')uses.set(i,[]);
  if(r.kind==='RES'){step++;for(const p of r.parents)if(uses.has(p))uses.get(p).push(step);}
 });
 const live=[...uses.values()].filter(u=>u.length);
 const counts=Array.from({length:step},(_,x)=>live.filter(u=>u[0]<=x+1&&x+1<=u.at(-1)).length);
 return {emissions:uses.size,clones:live.length,area:counts.reduce((a,b)=>a+b,0),peak:Math.max(...counts)};
}
const cases=[],measure=[],family=[];let assertions=0;
function run(name,data,expected=true){
 const bytes=Buffer.from(JSON.stringify(data)+'\n'),file=path.join(out,name+'.json');
 fs.writeFileSync(file,bytes);
 const r=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',maxBuffer:3e6,timeout:25000});
 assert.equal(r.status===0,expected,name+': '+r.stderr.slice(0,200));
 const count=expected?JSON.parse(r.stdout.trim()).assertions:0;assertions+=count;
 const item={name,verdict:expected?'ACCEPT':'REJECT',bytes:bytes.length,sha256:SHA(bytes),assertions:count};
 cases.push(item);return item;
}
const evenly=(M,c)=>Array.from({length:M},(_,b)=>Math.min(c-1,Math.floor(b*c/M)));
for(let v=2;v<=16;v++){
 const a=Math.min(8,Math.ceil(v/2)),b=v-a;
 const d=construct(8,evenly(8,a),evenly(8,b)),p=profile(d);
 assert.equal(p.clones,v);assert.equal(p.area,496-30*v);assert.equal(p.peak,v===16?1:2);
 const z=run('M8_v'+v,d);measure.push({views:v,split:[a,b],area:p.area,peak:p.peak,bytes:z.bytes,sha256:z.sha256});
}
let d=construct(8,Array.from({length:8},(_,b)=>b%2),evenly(8,8));
let p=profile(d);assert.equal(p.area,382);assert.equal(p.peak,3);run('M8_interleave_A2_B8',d);
d=construct(8,Array.from({length:8},(_,b)=>b%4),Array.from({length:8},(_,b)=>b%4));
p=profile(d);assert.equal(p.area,1000);assert.equal(p.peak,8);run('M8_midpoint_interleave_A4_B4',d);
for(const k of [2,3,4,5]){
 const M=2*k,contig=Array.from({length:M},(_,b)=>Math.floor(b/2)),inter=Array.from({length:M},(_,b)=>b%k);
 const good=construct(M,contig,contig),bad=construct(M,inter,inter);
 const gp=profile(good),bp=profile(bad);
 assert.equal(gp.area,64*k);assert.equal(bp.area,2*k*(31*k+1));
 assert.equal(gp.peak,2);assert.equal(bp.peak,2*k);
 const a=run('k'+k+'_contiguous',good),b=run('k'+k+'_interleaved',bad);
 family.push({k,W:62*k+1,views:2*k,contiguous:{area:gp.area,peak:gp.peak,bytes:a.bytes},interleaved:{area:bp.area,peak:bp.peak,bytes:b.bytes}});
}
const basis=construct(8,evenly(8,4),evenly(8,4));
for(const [name,f] of [
 ['bad_source',d=>{d.records.find(r=>r.kind==='SOURCE').c=[-d.spec.guard]}],
 ['bad_facet',d=>{d.records.find(r=>r.kind==='DEF').c=[9999999]}],
 ['bad_owner',d=>{d.records.find(r=>r.kind==='DEF').gate=98765}],
 ['bad_pivot',d=>{d.records.at(-1).pivot=98765}],
 ['future_parent',d=>{d.records.at(-1).parents[0]=d.records.length+1}],
 ['underpayment',d=>{d.summary.paid_total--}],
 ['unknown_AND3',d=>{d.records.find(r=>r.kind==='DEF').kind='AND3'}]
]){const x=clone(basis);f(x);run(name,x,false);}
const output={id:'LSPV2-601',scope:'exact original /386 SOURCE/DEF/RES only, not R_mix341',
 checker_sha256:SHA(fs.readFileSync(checker)),source_sha256:SHA(source),seed_sha256:SHA(seedBytes),
 theorem:'for two facet values used once per 31-RES block, A_min(M,v)=62M-30v for 2<=v<=2M; W=31M+1',
 counters:'same v=2k, M=2k: consecutive area 64k, peak 2; b mod k interleaved area 2k(31k+1), peak 2k',
 totals:{accepts:cases.filter(x=>x.verdict==='ACCEPT').length,rejects:cases.filter(x=>x.verdict==='REJECT').length,assertions},
 cases,measure,family};
fs.writeFileSync(path.join(out,'LSPV2_601_NATIVE386_PARTIAL_VIEW_RAW.json'),JSON.stringify(output,null,2)+'\n');
console.log(JSON.stringify({pass:true,totals:output.totals,family},null,2));
