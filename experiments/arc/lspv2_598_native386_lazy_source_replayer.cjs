#!/usr/bin/env node
'use strict';
/* LSPV-2/598: external signed SOURCE-bound scheduling regression for the
 * UNMODIFIED original archived /386 sibling checker. This program is an
 * independently labeled replayer/packet editor, not an R_mix341 checker. */
const fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process');
const crypto=require('node:crypto'),assert=require('node:assert/strict');
const base=__dirname,out=path.join(base,'packets');fs.mkdirSync(out,{recursive:true});
const pin={checker:'22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113',W29:'0d8b1894f91d00c554727a92fed35b2bb58f2b1602f2a3cfcb949effda43ceb0',W32:'56222417e011357a9f7d141221b9e10b0e4eb230a05ebf6365e00b95ec9be238'};
const hash=x=>crypto.createHash('sha256').update(x).digest('hex');
const load=(n,h)=>{let b=fs.readFileSync(path.join(base,n));assert.equal(hash(b),h,`pinned input ${n}`);return b};
const checker=path.join(base,'checker386.js');load('checker386.js',pin.checker);
const source=load('SOURCE.cnf','3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c');
const sn=source.toString('utf8').trim().split(/\s+/);assert.deepEqual(sn.slice(0,2),['p','cnf']);
const nv=Number(sn[2]),nc=Number(sn[3]);const sourceRows=[];let row=[];for(let i=4;i<sn.length;i++){const n=Number(sn[i]);assert(Number.isSafeInteger(n));if(n===0){sourceRows.push(row);row=[]}else {assert(Math.abs(n)<=nv);row.push(n)}}
assert.equal(row.length,0);assert.equal(sourceRows.length,nc);const sort=a=>a.map(JSON.stringify).sort();
const packets=[];let positive=0,negative=0,originalAssertions=0;
function replay(o,mode){const old=o.records,m=o.records.length,terminal=m-1;assert.deepEqual(old[terminal].c,[]);const mapping=new Map(),newRecords=[];
 function emit(i){if(mapping.has(i))return;assert(Number.isSafeInteger(i)&&i>=0&&i<m);const rec=old[i];for(const p of rec.parents)emit(p);const parents=rec.parents.map(p=>mapping.get(p));mapping.set(i,newRecords.length);newRecords.push({...rec,parents});}
 const ancestors=new Set();function ancestry(i){if(ancestors.has(i))return;ancestors.add(i);for(let p of old[i].parents)ancestry(p)}ancestry(terminal);
 if(mode==='lazy'){
   for(let i=0;i<terminal;i++)if(old[i].kind==='RES')emit(i);
   for(let i=0;i<terminal;i++)if(!mapping.has(i))emit(i);
 }else if(mode==='ancestry-first'){
   for(let i=0;i<terminal;i++)if(ancestors.has(i))emit(i);
   for(let i=0;i<terminal;i++)emit(i);
 }else if(mode==='reverse-source'){
   for(let i=terminal-1;i>=0;i--)if(old[i].kind==='SOURCE')emit(i);
   for(let i=0;i<terminal;i++)if(old[i].kind==='RES')emit(i);
   for(let i=0;i<terminal;i++)emit(i);
 }else if(mode==='source-first'){
   for(let i=0;i<terminal;i++)emit(i);
 }else throw Error('bad mode');
 emit(terminal);assert.equal(mapping.size,m);const d={...o,records:newRecords};
 assert.deepEqual(sort(o.records.filter(r=>r.kind==='SOURCE').map(r=>r.c)),sort(d.records.filter(r=>r.kind==='SOURCE').map(r=>r.c)));
 assert.deepEqual(sort(sourceRows),sort(d.records.filter(r=>r.kind==='SOURCE').map(r=>r.c)),'independent external SOURCE mismatch');
 assert.equal(d.summary.paid_total,o.summary.paid_total);return {packet:d,mapping,ancestry};}
function measurements(d){let firstRES=d.records.findIndex(r=>r.kind==='RES'),lastSOURCE=d.records.map(r=>r.kind).lastIndexOf('SOURCE'),firstDEF=d.records.findIndex(r=>r.kind==='DEF');let lateSource=d.records.filter((r,i)=>r.kind==='SOURCE'&&i>firstRES).length,lateDef=d.records.filter((r,i)=>r.kind==='DEF'&&i>firstRES).length;
 let depth=[];for(let i=0;i<d.records.length;i++){const r=d.records[i];depth[i]=r.kind==='RES'?1+Math.max(...r.parents.map(j=>depth[j])):0}
 const anc=new Set();function visit(i){if(anc.has(i))return;anc.add(i);for(let p of d.records[i].parents)visit(p)}visit(d.records.length-1);
 const sourceAnc=[...anc].filter(i=>d.records[i].kind==='SOURCE').map(i=>JSON.stringify(d.records[i].c)).sort();
 const facetAnc=[...anc].filter(i=>d.records[i].kind==='DEF').map(i=>JSON.stringify(d.records[i].c)).sort();
 return {first_paid_index:firstRES,last_source_index:lastSOURCE,first_DEF_index:firstDEF,source_after_first_RES:lateSource,DEF_after_first_RES:lateDef,source_ancestry:sourceAnc,facet_ancestry:facetAnc,span:depth.at(-1),work:d.summary.paid_total,serialized_bytes:Buffer.byteLength(JSON.stringify(d)+'\n')};}
function run(name,d,want){const bytes=Buffer.from(JSON.stringify(d)+'\n'),file=path.join(out,name+'.json');fs.writeFileSync(file,bytes);const proc=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',timeout:10000});const ok=proc.status===0;if(ok!==want)throw Error(`${name} expected ${want} got ${ok}: ${proc.stderr.slice(0,500)}`);if(ok){const result=JSON.parse(proc.stdout.trim());originalAssertions+=result.assertions;positive++}else negative++;
 const m=ok?measurements(d):null;const z={name,verdict:ok?'ACCEPT':'REJECT',sha256:hash(bytes),bytes:bytes.length,original_assertions:ok?JSON.parse(proc.stdout.trim()).assertions:0,...m};packets.push(z);return z;}
for(const [label,file,pinhash] of [['W29','native_W29.json',pin.W29],['W32','native_W32.json',pin.W32]]){
 const b=JSON.parse(load(file,pinhash));const baseline=measurements(b);
 for(const mode of ['source-first','lazy','ancestry-first','reverse-source']){
  const {packet}=replay(b,mode);const x=run(label+'_'+mode,packet,true);assert.deepEqual(x.source_ancestry,baseline.source_ancestry);assert.deepEqual(x.facet_ancestry,baseline.facet_ancestry);assert.equal(x.span,baseline.span);
 }
 const {packet}=replay(b,'lazy');
 // Four independent falsifiers: future SOURCE/DEF parent, signed SOURCE,
 // a wrong facet/RES pivot, and incorrect paid work.
 if(label==='W29'){
  const badFuture=structuredClone(packet);const j=badFuture.records.findIndex(r=>r.kind==='RES');badFuture.records[j].parents[0]=badFuture.records.length;run('reject_future_SOURCE_parent',badFuture,false);
  const badSrc=structuredClone(packet);const k=badSrc.records.findIndex(r=>r.kind==='SOURCE');badSrc.records[k].c=[-badSrc.spec.guard];run('reject_wrong_signed_SOURCE',badSrc,false);
  const badPay=structuredClone(packet);badPay.summary.paid_total--;run('reject_paid_owner_undercharge',badPay,false);
 }else{
  const badFacet=structuredClone(packet);const j=badFacet.records.findIndex(r=>r.kind==='DEF');badFacet.records[j].c=[-badFacet.spec.guard];run('reject_wrong_DEF_facet',badFacet,false);
  const badPivot=structuredClone(packet);badPivot.records.at(-1).pivot=999999;run('reject_invalid_RES_pivot',badPivot,false);
  const badOpcode=structuredClone(packet);badOpcode.records.at(-1).kind='AND3';run('reject_unimplemented_AND3',badOpcode,false);
 }
}
const ledger={schema:'LSPV2/598/native386-lazy-source-interleaving/v1',scope:'unchanged archived /386 checker ONLY; external-source binder is independent; NOT R_mix341',checker_git_blob:'338305c0ce101704205e57543756b8127074a986',checker_sha256:pin.checker,source_sha256:hash(source),source_rows:sourceRows.length,pins:pin,totals:{cases:packets.length,positive,negative,original_assertions:originalAssertions},packets};
fs.writeFileSync(path.join(base,'LSPV2_598_native386_lazy_source_raw.json'),JSON.stringify(ledger,null,2)+'\n');console.log(JSON.stringify({totals:ledger.totals,sourceSHA:ledger.source_sha256,positives:packets.filter(x=>x.verdict==='ACCEPT').map(x=>({name:x.name,lateSource:x.source_after_first_RES,lateDEF:x.DEF_after_first_RES,span:x.span,bytes:x.bytes,work:x.work}))},null,2));
