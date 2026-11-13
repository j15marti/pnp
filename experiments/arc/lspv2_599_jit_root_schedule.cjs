#!/usr/bin/env node
'use strict';
/* LSPV-2/599: Exact source/DEF-root just-in-time normalization for the archived /386
   SOURCE/DEF/RES checker. This script is an independent generator/auditor, NOT the
   historical checker and NOT an R_mix341 full-calculus parser.
   Usage: node lspv2_599_jit_root_schedule.cjs checker386.js source.cnf output-dir seedA.json [seedB.json ...]
 */
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process'),assert=require('node:assert/strict');
const [checkerPath,sourcePath,outDir,...packetPaths]=process.argv.slice(2);
if(!checkerPath||!sourcePath||!outDir||!packetPaths.length)throw Error('Usage: <checker386> <source.cnf> <output-dir> <packet.json>...');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const blob=b=>{const head=Buffer.from(`blob ${Buffer.byteLength(b)}\0`);return crypto.createHash('sha1').update(Buffer.concat([head,Buffer.from(b)])).digest('hex')};
const checker=fs.readFileSync(checkerPath);assert.equal(blob(checker),'338305c0ce101704205e57543756b8127074a986','not original /386 checker');
const source=fs.readFileSync(sourcePath);const cnfText=source.toString('utf8');
function canon(c){return JSON.stringify([...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b));}
function sourceMap(src){const arr=src.trim().split(/\s+/);assert.equal(arr[0],'p');assert.equal(arr[1],'cnf');const n=Number(arr[2]),m=Number(arr[3]);let c=[],out=[];
 for(const v of arr.slice(4)){assert.match(v,/^-?\d+$/);const x=Number(v);assert(Number.isSafeInteger(x));if(x===0){out.push(c);c=[]}else{assert(Math.abs(x)<=n);c.push(x)}}
 assert.equal(c.length,0);assert.equal(out.length,m);let counts=new Map();for(const row of out){let key=canon(row);counts.set(key,(counts.get(key)||0)+1)}return counts;
}
const expected=sourceMap(cnfText);fs.mkdirSync(outDir,{recursive:true});
function bind(d){const seen=new Map();for(const r of d.records)if(r.kind==='SOURCE'){const k=canon(r.c);seen.set(k,(seen.get(k)||0)+1)}
 assert.deepEqual([...seen].sort(),[...expected].sort(),'external SOURCE mismatch');}
function validate(d){assert(d.records.length===d.summary.live_records);assert.equal(d.records.at(-1).kind,'RES');assert.equal(d.records.at(-1).c.length,0);for(let i=0;i<d.records.length;i++){
 let r=d.records[i];assert(['SOURCE','DEF','RES'].includes(r.kind));assert(r.parents.every(p=>Number.isInteger(p)&&p<i&&p>=0));if(r.kind==='RES')assert.equal(r.parents.length,2);else assert.equal(r.parents.length,0);
 }bind(d);}
function canonicalSignature(d){const r=d.records,derived=r.map((v,i)=>({i,v})).filter(x=>x.v.kind==='RES');const ix=new Map(derived.map((x,i)=>[x.i,i]));const rootMap=new Map(r.map((v,i)=>[i,`${v.kind}:${v.kind==='SOURCE'?v.source:v.gate}:${canon(v.c)}`]));
 return derived.map(({i,v})=>({c:canon(v.c),pivot:v.pivot,parents:v.parents.map(p=>r[p].kind==='RES'?`R${ix.get(p)}`:rootMap.get(p))}));}
function jit(d){const r=d.records;const rootIndices=r.map((v,i)=>({v,i})).filter(({v})=>v.kind!=='RES').map(x=>x.i);const referenced=new Set(r.filter(x=>x.kind==='RES').flatMap(x=>x.parents));const unused=rootIndices.filter(i=>!referenced.has(i));const out=[],old2new=new Map();
 function emit(i){if(old2new.has(i))return;const x=structuredClone(r[i]);x.parents=x.parents.map(p=>{assert(old2new.has(p),'future parent '+p);return old2new.get(p)});old2new.set(i,out.length);out.push(x)}
 // Emit strictly unused roots in the lowest-live RES epoch. Their payload can be
 // immediately reclaimed by the abstract liveness model; the original CLI keeps known[].
 unused.forEach(emit);
 for(let i=0;i<r.length;i++)if(r[i].kind==='RES'){
  for(const p of r[i].parents)if(r[p].kind!=='RES'&&!old2new.has(p))emit(p);
  emit(i);
 }
 assert.equal(out.length,r.length);assert.equal(out.at(-1).kind,'RES');
 const result=structuredClone(d);result.records=out;return result;
}
function sourceFirst(d){const r=d.records,arr=r.map((v,i)=>({v,i}));arr.sort((a,b)=>Number(a.v.kind==='RES')-Number(b.v.kind==='RES')||a.i-b.i);const m=new Map(arr.map((e,i)=>[e.i,i]));const result=structuredClone(d);result.records=arr.map(e=>({...structuredClone(e.v),parents:e.v.parents.map(i=>m.get(i))}));validate(result);return result;}
function rootLiveLowerCurve(d){
 const records=d.records,roots=records.map((v,i)=>({v,i})).filter(x=>x.v.kind!=='RES');
 const res=records.map((v,i)=>({v,i})).filter(x=>x.v.kind==='RES');
 const firstLast=roots.map(x=>{
   let positions=[];res.forEach((r,j)=>{if(r.v.parents.includes(x.i))positions.push(j)});
   return positions.length?[Math.min(...positions),Math.max(...positions)]:null;
 });
 return res.map((_,j)=>firstLast.filter(bounds=>bounds&&bounds[0]<=j&&bounds[1]>=j).length);
}
function stats(d){const r=d.records,n=r.length,last=r.map((_,i)=>i),res=r.map((e,i)=>({e,i})).filter(v=>v.e.kind==='RES');r.forEach((e,i)=>e.parents.forEach(j=>last[j]=Math.max(last[j],i)));
 const span=Array(n).fill(0);let resNo=0,peak=0,rootPeak=0,area=0,peakPayload=0,rootArea=0,checks=[];
 for(let i=0;i<n;i++){const e=r[i];if(e.kind==='RES'){resNo++;span[i]=1+Math.max(...e.parents.map(p=>span[p]));let live=[];
 for(let k=0;k<i;k++)if(last[k]>=i)live.push(k);
 const roots=live.filter(k=>r[k].kind!=='RES').length;const payload=live.reduce((z,k)=>z+Buffer.byteLength(JSON.stringify(r[k].c)),0);
 const metric={resOrdinal:resNo,liveTotal:live.length,liveRoot:roots,liveRES:live.length-roots,liveClausePayloadBytes:payload};checks.push(metric);peak=Math.max(peak,live.length);rootPeak=Math.max(rootPeak,roots);area+=live.length;rootArea+=roots;peakPayload=Math.max(peakPayload,payload);
 }}
 return {res:resNo,span:span.at(-1),peakBeforeRES:peak,peakRootBeforeRES:rootPeak,totalLiveAtRES:area,totalRootLiveAtRES:rootArea,peakClausePayloadBeforeRES:peakPayload,atRES:checks};}
function run(file){const p=cp.spawnSync(process.execPath,[checkerPath,file],{encoding:'utf8',timeout:20000});let parsed=null;try{parsed=JSON.parse(p.stdout.trim().split('\n').at(-1))}catch{}return {accept:p.status===0,exit:p.status,signal:p.signal,assertions:parsed?.assertions||null,paid:parsed?.paid||null,error:(p.stderr||'').trim().split('\n')[0]||null};}
const raw={run:'LSPV-2/599',date:'2026-11-13',scope:'original archived /386 only; fixed RES order; ideal last-use reclamation memory (not Node RSS)',checker_git_blob:blob(checker),checker_sha256:sha(checker),source_sha256:sha(source),node:process.version,seeds:[],hostile:[]};
for(const file of packetPaths){const base=path.basename(file,'.json');const original=JSON.parse(fs.readFileSync(file,'utf8'));validate(original);const variants=[['input',original],['source-first',sourceFirst(original)],['jit',jit(original)]];
 const signature=canonicalSignature(original),rootLB=rootLiveLowerCurve(original);const row={seed:base,variants:{},root_lower_bound:{area:rootLB.reduce((a,b)=>a+b,0),peak:Math.max(...rootLB)}};let refStats=null;
 for(const [name,d] of variants){validate(d);assert.deepEqual(canonicalSignature(d),signature,'changed RES DAG');assert.equal(d.summary.paid_total,original.summary.paid_total,'changed W');const out=path.join(outDir,base+'_'+name+'.json'),bytes=JSON.stringify(d)+'\n';fs.writeFileSync(out,bytes);const v=run(out);assert(v.accept,base+':'+name+' original-CLI rejected '+JSON.stringify(v));const s=stats(d);assert(s.atRES.every((z,i)=>z.liveRoot>=rootLB[i]),'source-optimum lower envelope violated');if(name==='jit')assert(s.atRES.every((z,i)=>z.liveRoot===rootLB[i]),'JIT not pointwise root-optimal');if(refStats)assert.equal(s.span,refStats.span,'changed span');else refStats=s;
 row.variants[name]={file:path.basename(out),sha256:sha(Buffer.from(bytes)),bytes:Buffer.byteLength(bytes),...v,metrics:{...s,atRES:undefined}};
 if(name==='jit'){
 const baseline=stats(original);assert(s.atRES.every((z,i)=>z.liveRoot<=baseline.atRES[i].liveRoot),'JIT root domination violation');
 const sf=stats(variants[1][1]);assert(s.atRES.every((z,i)=>z.liveRoot<=sf.atRES[i].liveRoot),'source-first dominance failure');
 row.jit_checkpoint_strict_improvement_vs_input=s.atRES.filter((z,i)=>z.liveRoot<baseline.atRES[i].liveRoot).length;
 row.jit_checkpoint_strict_improvement_vs_sourcefirst=s.atRES.filter((z,i)=>z.liveRoot<sf.atRES[i].liveRoot).length;
 }
 }
 raw.seeds.push(row);
}
// Fixed original-CLI hostile controls are not reimplementations of the original checker.
const d=JSON.parse(fs.readFileSync(path.join(outDir,raw.seeds[0].variants.jit.file),'utf8'));
const mutations=[['source-forgery',x=>x.records.find(r=>r.kind==='SOURCE').c[0]*=-1],
 ['future-parent',x=>{const r=x.records.find(r=>r.kind==='RES');r.parents[0]=x.records.length+1}],
 ['false-payment',x=>x.summary.paid_total--],
 ['unsupported-AND3',x=>x.records.find(r=>r.kind==='RES').kind='AND3']];
for(const [tag,mutate] of mutations){let p=structuredClone(d);mutate(p);const filepath=path.join(outDir,'reject_'+tag+'.json'),txt=JSON.stringify(p)+'\n';fs.writeFileSync(filepath,txt);let result=run(filepath);assert(!result.accept,'original CLI accepted mutation '+tag);raw.hostile.push({name:tag,file:path.basename(filepath),sha256:sha(Buffer.from(txt)),...result});}
raw.total_native_accepts=raw.seeds.reduce((sum,x)=>sum+Object.values(x.variants).filter(v=>v.accept).length,0);raw.total_native_rejects=raw.hostile.length;
const resultFile=path.join(outDir,'LSPV2_599_JIT_ROOT_SCHEDULING_RAW.json');fs.writeFileSync(resultFile,JSON.stringify(raw,null,2)+'\n');console.log(JSON.stringify({raw:resultFile,accepted:raw.total_native_accepts,rejected:raw.total_native_rejects,seeds:raw.seeds.map(x=>({seed:x.seed,metrics:Object.fromEntries(Object.entries(x.variants).map(([k,v])=>[k,v.metrics])),jit_improvements:[x.jit_checkpoint_strict_improvement_vs_input,x.jit_checkpoint_strict_improvement_vs_sourcefirst]}))},null,2));