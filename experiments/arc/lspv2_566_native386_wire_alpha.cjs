#!/usr/bin/env node
'use strict';
// LSPV-2/566: separately labeled REFERENCE renaming transformer and OS original-checker differential.
// NOT the original /386 checker; NOT a parser for historical full R_mix341.
const fs=require('node:fs'), path=require('node:path'), os=require('node:os');
const crypto=require('node:crypto'), cp=require('node:child_process'), assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checker='experiments/arc/lspv2_386_independent_verify.js';
const seed='results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json';
const external='results/raw/arc/2026-11-11_0812_LSPV2_559_EXTERNAL_K4_SIGNED_SOURCE.cnf';
const blobs={
 [checker]:'338305c0ce101704205e57543756b8127074a986',
 [seed]:'318c52d99977ea4e91bc8554051138a700c1dc94',
 [external]:'e8bc4300f1f4518cb447edaf3f699bcee4839803'
};
const digest=b=>crypto.createHash('sha256').update(b).digest('hex');
const gitblob=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
function pinned(p){let b=fs.readFileSync(path.join(root,p));assert.equal(gitblob(b),blobs[p]);return b;}
const copy=x=>structuredClone(x), encode=p=>Buffer.from(JSON.stringify(p)+'\n');
function tally(p){let count=k=>p.records.filter(x=>x.kind===k).length;
 p.summary={source:count('SOURCE'),def_views:count('DEF'),resolution:count('RES'),
 paid_gates:p.gate_defs.length,paid_total:p.gate_defs.length+count('RES'),live_records:p.records.length};return p;}
function splice(seedPacket){
 let p=copy(seedPacket),front=[
  {kind:'DEF',gate:0,c:[1,-8],parents:[]},
  {kind:'DEF',gate:0,c:[-1,-4,8],parents:[]}];
 let sources=p.records.slice(0,17).map(copy),res=p.records.slice(17).map(copy);
 let detour=[{kind:'RES',c:[-4,-5,-7,-8],parents:[0,9],pivot:1},
             {kind:'RES',c:[-1,-4,-5,-7],parents:[19,1],pivot:-8}];
 let remap=j=>j<17?j+2:j+4;
 res.forEach((r,k)=>{r.parents=r.parents.map(remap);
  if(k===3){assert.deepEqual(r.parents,[5,9]);r.parents[1]=20;}
 });
 p.records=[...front,...sources,...detour,...res];return tally(p);
}
// Maps only globally declared fresh gate outputs, never source variables or guard.
// Owner IDs and signed uses are renamed simultaneously. Mapping must be injective.
function rename(p,wireMap,idMap){let q=copy(p),a=new Map(Object.entries(wireMap).map(([x,y])=>[Number(x),y]));
 let d=new Map(Object.entries(idMap).map(([x,y])=>[Number(x),y]));
 assert.equal(a.size,p.gate_defs.length);assert.equal(d.size,p.gate_defs.length);
 assert.equal(new Set([...a.values()]).size,a.size);assert.equal(new Set([...d.values()]).size,d.size);
 const names=new Set(p.gate_defs.map(g=>g[1]));assert.deepEqual(names,new Set(a.keys()));
 const ids=new Set(p.gate_defs.map(g=>g[0]));assert.deepEqual(ids,new Set(d.keys()));
 let guard=p.spec.guard,n=p.spec.edges.length;
 for(const z of a.values())assert(Number.isSafeInteger(z)&&z>n&&z!==guard);
 for(const id of d.values())assert(Number.isSafeInteger(id)&&id>=0);
 const lit=x=>names.has(Math.abs(x))?(x<0?-1:1)*a.get(Math.abs(x)):x;
 const key=c=>[...new Set(c)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
 q.gate_defs=q.gate_defs.map(([id,z,x,y])=>[d.get(id),a.get(z),lit(x),lit(y)]);
 q.records=q.records.map(r=>{let t=copy(r);if(t.kind==='DEF')t.gate=d.get(t.gate);
  t.c=key(t.c.map(lit));if(t.kind==='RES')t.pivot=lit(t.pivot);return t;});
 assert.notEqual(q.records.at(-1).pivot,999999,'original CLI synthetic terminal-pivot negative-test collision');
 return q;
}
function normal(p){let wires={},ids={};let next=p.spec.edges.length+1;
 for(let i=0;i<p.gate_defs.length;i++){
  while(next===p.spec.guard)next++;
  assert(Number.isSafeInteger(next),'exhausted safe fresh wire namespace');
  const [id,z]=p.gate_defs[i];wires[z]=next++;ids[id]=i;
 }return rename(p,wires,ids);
}
function sourceHashBound(p,raw){let lines=raw.toString().trim().split(/\n/),head=lines.shift();
 assert.equal(head,'p cnf '+p.spec.guard+' '+p.summary.source);
 const cv=x=>JSON.stringify([...new Set(x)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b));
 const clauses=lines.map(line=>{let ns=line.split(' ').map(Number);assert.equal(ns.pop(),0);return cv(ns)});
 const source=p.records.filter(r=>r.kind==='SOURCE').map(r=>cv(r.c));
 const multi=xs=>JSON.stringify([...xs].sort());assert.equal(multi(clauses),multi(source));
 return digest(raw);
}
function checkOS(p,scratch,label){const buf=encode(p),file=path.join(scratch,label+'.json');fs.writeFileSync(file,buf);
 const t=process.hrtime.bigint();let r=cp.spawnSync(process.execPath,[path.join(root,checker),file],
  {encoding:'utf8',maxBuffer:1024*1024,timeout:20000});
 assert(!r.error);let ok=r.status===0;let detail=null;
 if(ok){detail=JSON.parse(r.stdout.trim().split(/\r?\n/).at(-1));assert.equal(detail.negativeTests,11)}
 return {label,accept:ok,exit:r.status,sha256:digest(buf),bytes:buf.length,
  paid:p.summary.paid_total,gate_owners:p.gate_defs.map(x=>x[0]),
  wires:p.gate_defs.map(x=>x[1]),records:p.records.length,
  assertions:detail?.assertions||0,run_ns:Number(process.hrtime.bigint()-t),
  error:ok?null:(r.stderr||'').trim().slice(0,1000),bytes_base64:buf.toString('base64')};
}
function main(){pinned(checker);let original=JSON.parse(pinned(seed));let source=pinned(external);
 let live=splice(original);let large=rename(live,{8:9007199254740991},{0:9007199254740991});
 let small=rename(live,{8:126},{0:71});let restored=normal(large);
 assert.deepEqual(restored,live);assert.deepEqual(normal(small),live);
 let nested=copy(live);nested.gate_defs.push([1,9,8,2]);nested.records.unshift({kind:'DEF',gate:1,c:[8,-9],parents:[]});
 nested.records.slice(1).forEach(r=>{r.parents=r.parents.map(j=>j+1)});tally(nested);
 let nestedLarge=rename(nested,{8:10001,9:9007199254740991},{0:77,1:700001});
 assert.deepEqual(normal(nestedLarge),nested);
 let swappedNested=rename(nested,{8:9007199254740991,9:10001},{0:99,1:56});
 assert.deepEqual(normal(swappedNested),nested);
 let unsortedNested=copy(swappedNested);unsortedNested.records[0].c.reverse();
 let normId=copy(live),wrongFacet=copy(large),badPivot=copy(large);
 let collide=copy(large),unsafe=copy(large),collisionId=copy(nestedLarge);
 collide.gate_defs[0][1]=7;
 unsafe.gate_defs[0][1]=9007199254740992;
 wrongFacet.records[0].c=[1,-8];
 badPivot.records[20].pivot=-8;
 collisionId.gate_defs[1][0]=collisionId.gate_defs[0][0];
 let underpay=copy(large);underpay.summary.paid_total--;
 let forgedSource=copy(large);forgedSource.records[2].c=[-1,2,3,-7];
 let staleDef=copy(large);staleDef.records[1].gate=0;
 let staleRes=copy(large);staleRes.records[19].c=[-4,-5,-7,-8];
 const cases=[
  ['canonical_live_splice',live,true],['max_safe_wire_owner',large,true],
  ['noncanonical_names',small,true],['alpha_normalized',restored,true],
  ['nested_gate_positive',nested,true],['nested_relabel_high',nestedLarge,true],
  ['nested_restored',normal(nestedLarge),true],
  ['nested_swapped_wires_canonicalized',swappedNested,true],
  ['nested_swapped_unsorted_facet',unsortedNested,false],
  ['wire_collides_guard',collide,false],['wire_outside_safe_integer',unsafe,false],
  ['stale_facet_literal',wrongFacet,false],['stale_RES_pivot',badPivot,false],
  ['duplicate_paid_owner_id',collisionId,false],['underpaid',underpay,false],
  ['forged_source_sign',forgedSource,false],['stale_facet_owner',staleDef,false],
  ['stale_RES_clause',staleRes,false]
 ];
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2-566-'));
 let results=[];try{for(let [name,p,expected] of cases){const r=checkOS(p,tmp,name);
  if(r.accept!==expected)console.error(name,r.error);assert.equal(r.accept,expected,name+': original archived checker differential mismatch');
  if(r.accept){assert.equal(r.paid,p.summary.paid_total);assert.equal(sourceHashBound(p,source),digest(source));}
  results.push({...r,expected});
 }}finally{fs.rmSync(tmp,{recursive:true,force:true})}
 const positives=results.filter(x=>x.accept);let summary={run:'LSPV-2/566',model:'original /386 CLI source/DEF/RES only',
 authority:'unchanged original OS Node checker; separate reference alpha-renamer',
 checker_git_blob:blobs[checker],seed_git_blob:blobs[seed],external_git_blob:blobs[external],
 source_sha256:digest(source),case_count:results.length,positives:positives.length,
 negatives:results.length-positives.length,positive_assertions:positives.reduce((s,x)=>s+x.assertions,0),
 baseline_work:live.summary.paid_total,high_name_work:large.summary.paid_total,
 baseline_bytes:encode(live).length,high_name_bytes:encode(large).length,
 restored_exact_bytes:encode(restored).equals(encode(live)),
 nested_restored_exact_bytes:encode(normal(nestedLarge)).equals(encode(nested)),
 swapped_nested_restored_exact_bytes:encode(normal(swappedNested)).equals(encode(nested)),
 full_R_mix341_authenticated:false,proof_P_vs_NP:'OPEN',
 checks:results};
 const out=path.join(root,'results/raw/arc');fs.mkdirSync(out,{recursive:true});
 fs.writeFileSync(path.join(out,'2026-11-11_1512_LSPV2_566_NATIVE_WIRE_ALPHA_RAW.json'),JSON.stringify(summary,null,2)+'\n');
 fs.writeFileSync(path.join(out,'2026-11-11_1512_LSPV2_566_ACCEPTED_HIGH_WIRE.json'),encode(large));
 fs.writeFileSync(path.join(out,'2026-11-11_1512_LSPV2_566_ACCEPTED_NESTED_HIGH_WIRES.json'),encode(nestedLarge));
 console.log(JSON.stringify({count:summary.case_count,positives:summary.positives,
  negatives:summary.negatives,assertions:summary.positive_assertions,
  baseline_bytes:summary.baseline_bytes,high_name_bytes:summary.high_name_bytes,
  restored:summary.restored_exact_bytes}));
}
main();
