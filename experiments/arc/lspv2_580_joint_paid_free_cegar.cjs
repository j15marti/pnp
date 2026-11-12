#!/usr/bin/env node
'use strict';
/* LSPV-2/580: source-pinned original-/386 differential replay.
 * This program is a CONSTRUCTOR/NORMALIZER, NOT the authoritative checker.
 * Run from j15marti/pnp root, Node >=18. No dependencies.
 * Optional env: PNP_386_CHECKER, PNP_386_SEED, PNP_386_SOURCE, PNP580_OUT.
 */
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const cp=require('node:child_process'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=process.cwd(),checker=process.env.PNP_386_CHECKER||path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedPath=process.env.PNP_386_SEED||path.join(root,'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json');
const sourcePath=process.env.PNP_386_SOURCE||path.join(root,'results/raw/arc/574_k01_SIGNED_SOURCE.cnf');
const outDir=process.env.PNP580_OUT||path.join(root,'results/raw/arc/580_native_joint_quotient_cases');
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const clone=x=>JSON.parse(JSON.stringify(x));
const sort=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function sourceAudit(packet){
 const bytes=fs.readFileSync(sourcePath),actual=sha(bytes);
 assert.equal(actual,'3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c','external signed SOURCE SHA');
 const text=bytes.toString('utf8').trim().split(/\s+/),nv=Number(text[2]),m=Number(text[3]);
 assert.equal(text[0],'p');assert.equal(text[1],'cnf');assert.equal(nv,7);assert.equal(m,17);
 const clauses=[],cur=[];for(const word of text.slice(4)){
  assert.match(word,/^-?\d+$/);const v=Number(word);if(v===0){clauses.push(sort(cur));cur.length=0;}else{assert(v!==0&&Math.abs(v)<=nv);cur.push(v)}
 }
 assert.equal(cur.length,0);assert.equal(clauses.length,17);
 const native=packet.records.filter(r=>r.kind==='SOURCE').map(r=>r.c);
 assert.deepEqual(clauses.map(JSON.stringify).sort(),native.map(JSON.stringify).sort(),'signed occurrence multiset');
 return {sha256:actual,bytes:bytes.length,clauses:clauses.length};
}
function summary(d){const s={source:0,def_views:0,resolution:0,paid_gates:d.gate_defs.length,paid_total:0,live_records:d.records.length};
 for(const r of d.records){if(r.kind==='SOURCE')s.source++;else if(r.kind==='DEF')s.def_views++;else if(r.kind==='RES')s.resolution++;else throw Error('bad record kind')}
 s.paid_total=s.paid_gates+s.resolution;d.summary=s;return d;
}
function construct(base){
 assert.equal(base.summary.paid_total,29);assert.equal(base.records.length,45);assert.equal(base.records[7].kind,'SOURCE');
 assert.deepEqual(base.records[7].c,[-1,-4,-5,-7]);assert.deepEqual(base.gate_defs,[[0,8,1,4]]);
 const [s,..._] = base.records;void s;void _;
 const extra=[
  {kind:'DEF',c:[1,-8],parents:[],gate:0},
  {kind:'DEF',c:[1,-8],parents:[],gate:0},
  {kind:'DEF',c:[-1,-4,8],parents:[],gate:0},
  {kind:'RES',c:[-4,-5,-7,-8],parents:[7,17],pivot:-1},
  {kind:'RES',c:[-4,-5,-7,-8],parents:[7,18],pivot:-1},
  {kind:'RES',c:[-1,-4,-5,-7],parents:[20,19],pivot:-8},
  {kind:'RES',c:[-1,-4,-5,-7],parents:[21,19],pivot:-8}
 ];
 let uses=0;
 const rest=base.records.slice(17).map(r=>{
  const q=clone(r);q.parents=q.parents.map(p=>{
    if(p===7){uses++;return uses===1?22:23}
    return p>=17?p+extra.length:p;
  });return q;
 });
 assert.equal(uses,2,'two terminal-live source uses needed');
 const d=clone(base);d.records=[...base.records.slice(0,17),...extra,...rest];return summary(d);
}
function normalize(d,mode){
 const out=clone(d);out.records=[];const oldToNew=[],seen=new Map(),removed=[];
 for(let i=0;i<d.records.length;i++){
  const r=clone(d.records[i]);r.parents=r.parents.map(j=>{assert(j<i&&oldToNew[j]!==undefined);return oldToNew[j]});
  let key=null;
  if(mode==='DEF'&&r.kind==='DEF')key=JSON.stringify([r.gate,r.c]);
  if(mode==='RES'&&r.kind==='RES')key=JSON.stringify([r.parents,r.pivot,r.c]);
  if(key!==null&&seen.has(key)){
   oldToNew[i]=seen.get(key);removed.push({old:i,new:oldToNew[i],kind:r.kind});continue;
  }
  oldToNew[i]=out.records.length;out.records.push(r);if(key!==null)seen.set(key,oldToNew[i]);
 }
 summary(out);return {packet:out,removed};
}
function ancestors(d){const seen=new Set(),stack=[d.records.length-1];while(stack.length){const i=stack.pop();if(seen.has(i))continue;seen.add(i);for(const p of d.records[i].parents)stack.push(p)}return seen}
function replay(d,name,expected=true){
 const f=path.join(outDir,name+'.json'),bytes=Buffer.from(JSON.stringify(d)+'\n');fs.writeFileSync(f,bytes);
 const p=cp.spawnSync(process.execPath,[checker,f],{encoding:'utf8',timeout:12000,maxBuffer:1048576});
 const accepted=p.status===0&&!p.error;
 assert.equal(accepted,expected,name+' checker verdict '+p.stderr?.slice(-350));
 const obj=accepted?JSON.parse(p.stdout.trim()):null;
 return {name,accepted,paid:d.summary.paid_total,records:d.records.length,def_views:d.summary.def_views,
  resolution:d.summary.resolution,bytes:bytes.length,sha256:sha(bytes),native_assertions:obj?.assertions||null,
  native_negative_tests:obj?.negativeTests||null,terminal_pivot:d.records.at(-1).pivot,stderr:accepted?undefined:p.stderr.slice(-400)};
}
function run(){fs.mkdirSync(outDir,{recursive:true});
 const base=JSON.parse(fs.readFileSync(seedPath,'utf8'));const source=sourceAudit(base);
 const original=construct(base);const anc=ancestors(original);
 for(const i of [17,18,19,20,21,22,23])assert(anc.has(i),'inserted facet/paid node not terminal-live '+i);
 const before=normalize(original,'RES');assert.equal(before.removed.length,0,'RES-first must not merge');
 const reverse=normalize(before.packet,'DEF');assert.equal(reverse.removed.length,1);
 const first=normalize(original,'DEF');assert.equal(first.removed.length,1);
 const second=normalize(first.packet,'RES');assert.equal(second.removed.length,2);
 const fixed=normalize(normalize(second.packet,'DEF').packet,'RES');assert.deepEqual(fixed.packet,second.packet,'normal form idempotence');
 assert.equal(original.summary.paid_total,33);assert.equal(reverse.packet.summary.paid_total,33);assert.equal(second.packet.summary.paid_total,31);
 assert.equal(second.packet.records.at(-1).c.length,0);
 const cases=[];
 cases.push(replay(base,'580_seed_W29'));
 cases.push(replay(original,'580_live_two_paths_W33'));
 cases.push(replay(reverse.packet,'580_RES_then_DEF_W33'));
 cases.push(replay(first.packet,'580_DEF_only_W33'));
 cases.push(replay(second.packet,'580_DEF_then_RES_W31'));
 const mutations=[
  ['bad_facet',d=>{d.records[17].c=[-1,-8]}],
  ['underpaid',d=>{d.summary.paid_total--}],
  ['future_parent',d=>{d.records[20].parents[0]=21}],
  ['wrong_pivot',d=>{d.records[20].pivot=1}],
  ['source_forgery',d=>{d.records[7].c=[1,-4,-5,-7]}]
 ];
 for(const [name,change] of mutations){const d=clone(original);change(d);cases.push(replay(d,'580_invalid_'+name,false))}
 const raw={run:'LSPV-2/580',status:'PROVED/RESTRICTED normalization-order lemma + COMPUTATIONAL OS original-checker replay',
  source,checker_sha256:sha(fs.readFileSync(checker)),checker_original_body_unchanged:true,
  seed_sha256:sha(fs.readFileSync(seedPath)),
  candidate:'Live duplication of two paid RES nodes with distinct duplicate DEF parents; DEF-before-RES canonicalization creates two legal cost-saving merges',
  genuine_ancestry:[...anc].filter(i=>i>=17&&i<=23).sort((a,b)=>a-b),
  transformer:{res_first_removed:before.removed,def_after_res_removed:reverse.removed,
   def_first_removed:first.removed,res_after_def_removed:second.removed,
   reverse_paid:reverse.packet.summary.paid_total,forward_paid:second.packet.summary.paid_total},
  results:cases,counts:{accepted:cases.filter(c=>c.accepted).length,rejected:cases.filter(c=>!c.accepted).length,
   original_checker_assertions:cases.reduce((n,c)=>n+(c.native_assertions||0),0),negative_checks:cases.reduce((n,c)=>n+(c.native_negative_tests||0),0)},
  limitations:'Original /386 SOURCE/DEF/RES sibling only, no R_mix341 full checker or B3. The W31 normalized path is not a global minimum; source and full checker wrappers impose distinct resource costs. No optimization of real TM time/space is claimed.'};
 const rawFile=path.join(outDir,'580_raw_manifest.json');fs.writeFileSync(rawFile,JSON.stringify(raw,null,2)+'\n');
 console.log(JSON.stringify({source,counts:raw.counts,payments:{original:33,reverse:33,forward:31},sizes:cases.slice(0,5).map(x=>[x.name,x.bytes]),rawFile}));
}
run();
