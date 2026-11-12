#!/usr/bin/env node
'use strict';
/* LSPV-2/581: A CONSTRUCTOR/REFERENCE NORMALIZER, NOT THE AUTHORITATIVE CHECKER.
 * Uses the archived, unmodified original /386 checker as a separate Node OS process.
 * Usage: node experiments/arc/lspv2_581_parametric_congruence_gap.cjs
 * Optional: PNP581_ROOT=/path/to/repository PNP581_OUT=/path/to/output.
 */
const fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process');
const crypto=require('node:crypto'),assert=require('node:assert/strict');
const {performance}=require('node:perf_hooks');
const root=process.env.PNP581_ROOT||process.cwd();
const checker=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const seedFile=path.join(root,'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json');
const sourceFile=path.join(root,'results/raw/arc/574_k01_SIGNED_SOURCE.cnf');
const out=process.env.PNP581_OUT||path.join(root,'results/raw/arc/581_parametric_cases');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const clone=o=>JSON.parse(JSON.stringify(o));
function summary(d){
 let source=0,def_views=0,resolution=0;
 for(const r of d.records){if(r.kind==='SOURCE')source++;else if(r.kind==='DEF')def_views++;else if(r.kind==='RES')resolution++;else throw Error('unknown kind')}
 d.summary={source,def_views,resolution,paid_gates:d.gate_defs.length,paid_total:resolution+d.gate_defs.length,live_records:d.records.length};
 return d;
}
function parseOriginalSource(d){
 const b=fs.readFileSync(sourceFile),digest=sha(b);
 assert.equal(digest,'3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c');
 const tok=b.toString('utf8').trim().split(/\s+/);assert.deepEqual(tok.slice(0,4),['p','cnf','7','17']);
 const norm=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
 let cs=[],row=[];
 for(const s of tok.slice(4)){assert.match(s,/^-?\d+$/);const v=Number(s);if(v===0){cs.push(norm(row));row=[];}else row.push(v)}
 assert.equal(row.length,0);assert.equal(cs.length,17);
 const fromPacket=d.records.filter(r=>r.kind==='SOURCE').map(r=>r.c);
 assert.deepEqual(cs.map(JSON.stringify).sort(),fromPacket.map(JSON.stringify).sort());
 return {sha256:digest,bytes:b.length,sourceClauses:cs.length};
}
/* Each stage has TWO independent live length-2 derivations of the already-known
 * source clause C=[-1,-4,-5,-7]. Their signed premises are genuine AND2 facets.
 * The live terminal cone traverses both chains at every stage.
 */
function construct(seed,k){
 assert(Number.isInteger(k)&&k>=1);assert.equal(seed.summary.paid_total,29);
 assert.equal(seed.records.length,45);assert.deepEqual(seed.gate_defs,[[0,8,1,4]]);
 assert.deepEqual(seed.records[7].c,[-1,-4,-5,-7]);
 const prefix=clone(seed.records.slice(0,17));
 const extra=[{kind:'DEF',c:[1,-8],parents:[],gate:0},{kind:'DEF',c:[-1,-4,8],parents:[],gate:0}];
 let pair=[7,7],layers=[];
 for(let j=0;j<k;j++){
  const t=[],c=[];
  for(let side=0;side<2;side++){
   t.push(prefix.length+extra.length);
   extra.push({kind:'RES',c:[-4,-5,-7,-8],parents:[pair[side],17],pivot:-1});
  }
  for(let side=0;side<2;side++){
   c.push(prefix.length+extra.length);
   extra.push({kind:'RES',c:[-1,-4,-5,-7],parents:[t[side],18],pivot:-8});
  }
  layers.push({stage:j+1,inputs:pair,first:t,outputs:c});pair=c;
 }
 let uses=0;
 const tail=seed.records.slice(17).map(r=>{
  const q=clone(r);q.parents=q.parents.map(p=>{
   if(p===7){uses++;return pair[uses-1]}
   return p>=17?p+extra.length:p;
  });return q;
 });
 assert.equal(uses,2,'seed must use SOURCE7 twice');
 const packet=clone(seed);packet.records=[...prefix,...extra,...tail];summary(packet);
 assert.equal(packet.summary.paid_total,29+4*k);
 const anc=ancestors(packet);for(const layer of layers)for(const id of [...layer.first,...layer.outputs])assert(anc.has(id),'stage dead '+id);
 assert(anc.has(17)&&anc.has(18),'facets must be terminal live');
 return {packet,layers,liveAdded:4*k+2};
}
function ancestors(d){const used=new Set(),stack=[d.records.length-1];while(stack.length){const i=stack.pop();if(used.has(i))continue;used.add(i);for(const p of d.records[i].parents)stack.push(p)}return used}
function quotient(d,mode){
 assert(['structural','value'].includes(mode));
 const out=clone(d);out.records=[];
 const seenDEF=new Map(),seenRES=new Map(),seenValue=new Map(),oldToNew=[],deleted=[];
 for(let i=0;i<d.records.length;i++){
  const r=clone(d.records[i]);r.parents=r.parents.map(j=>{assert(Number.isInteger(j)&&0<=j&&j<i&&oldToNew[j]!==undefined);return oldToNew[j]});
  const val=JSON.stringify(r.c),isTerminal=(i===d.records.length-1);
  let key=null,representative;
  if(r.kind==='DEF'){
   key=JSON.stringify([r.gate,r.c]);representative=seenDEF.get(key);
  }else if(r.kind==='RES'&&!isTerminal){
   if(mode==='structural'){key=JSON.stringify([r.parents,r.pivot,r.c]);representative=seenRES.get(key)}
   else representative=seenValue.get(val);
  }
  if(representative!==undefined){oldToNew[i]=representative;deleted.push({old:i,representative,kind:r.kind,clause:r.c});continue}
  const index=out.records.length;oldToNew[i]=index;out.records.push(r);
  if(r.kind==='DEF')seenDEF.set(key,index);
  if(r.kind==='RES'&&mode==='structural'&&!isTerminal)seenRES.set(key,index);
  if(!seenValue.has(val))seenValue.set(val,index);
 }
 return {packet:summary(out),deleted};
}
function prune(d){
 const live=ancestors(d),copy=clone(d);copy.records=[];const remap=[];
 for(let i=0;i<d.records.length;i++){
  const r=clone(d.records[i]);if(r.kind!=='SOURCE'&&!live.has(i))continue;
  remap[i]=copy.records.length;copy.records.push(r);
 }
 for(const r of copy.records)r.parents=r.parents.map(i=>{assert(remap[i]!==undefined,'pruned live parent');return remap[i]});
 return summary(copy);
}
function depth(d){let dep=[];for(const r of d.records){dep.push(r.kind==='RES'?1+Math.max(...r.parents.map(i=>dep[i])):0)}return Math.max(...dep)}
function replay(d,label,expected=true){
 const b=Buffer.from(JSON.stringify(d)+'\n');const f=path.join(out,label+'.json');fs.writeFileSync(f,b);
 const start=performance.now(),run=cp.spawnSync(process.execPath,[checker,f],{encoding:'utf8',timeout:25000,maxBuffer:2000000});
 const ms=performance.now()-start,accepted=run.status===0&&!run.error;
 assert.equal(accepted,expected,label+': unexpected native result: '+String(run.stderr).slice(-500));
 let res=accepted?JSON.parse(run.stdout.trim()):null;
 return {label,accepted,paid:d.summary.paid_total,paid_resolution:d.summary.resolution,paid_owners:d.summary.paid_gates,
  signed_SOURCE:d.summary.source,free_DEF:d.summary.def_views,records:d.records.length,bytes:b.length,sha256:sha(b),res_depth:depth(d),
  native_assertions:res?.assertions??null,native_negative_tests:res?.negativeTests??null,checker_wall_ms:Math.round(ms*1000)/1000,
  rejection:accepted?undefined:String(run.stderr||'').slice(-240)};
}
function run(){
 fs.mkdirSync(out,{recursive:true});const seed=JSON.parse(fs.readFileSync(seedFile,'utf8'));
 const provenance=parseOriginalSource(seed);
 const cases=[],results=[],summaries=[],kvals=[1,2,3,4,8,16];
 cases.push(replay(seed,'581_seed_W29'));
 for(const k of kvals){
  const start=performance.now(),{packet,layers}=construct(seed,k);
  const si=quotient(packet,'structural'),sf=quotient(si.packet,'structural');
  assert.deepEqual(sf.packet,si.packet,'fixed point after structural sweep');
  const val=quotient(packet,'value'),pr=prune(val.packet);
  const vp=quotient(si.packet,'value'),pr2=prune(vp.packet);
  assert.equal(si.packet.summary.paid_total,29+2*k,'structural gap exact');
  assert.equal(packet.summary.paid_total,29+4*k,'all duplicated paid nodes must be charged');
  assert.equal(pr.summary.paid_total,29,'value quotient + cone restores seed W29');
  assert.equal(pr2.summary.paid_total,29,'same from structural normal form');
  assert.deepEqual(pr,pr2,'value result is independent of initial syntactic quotient here');
  assert.deepEqual(pr,seed,'value-plus-cone should reconstruct original seed bytes exactly');
  const buildMs=performance.now()-start;
  const originals=[['expanded',packet],['syntactic_fixed',si.packet],['value_pruned',pr]];
  for(const [suffix,d] of originals)cases.push(replay(d,'581_k'+String(k).padStart(2,'0')+'_'+suffix));
  summaries.push({k,generated_paid:packet.summary.paid_total,syntactic_paid:si.packet.summary.paid_total,value_cone_paid:pr.summary.paid_total,
    gap:si.packet.summary.paid_total-pr.summary.paid_total,all_added_terminal_live:layers.every(l=>l.outputs.every(i=>ancestors(packet).has(i))),
    generation_transform_ms:Math.round(buildMs*1000)/1000});
  results.push({k,layers});
 }
 const base=construct(seed,2).packet;
 const mutation=[
  ['bad_facet',x=>{x.records[17].c=[-1,-8]}],
  ['underpaid',x=>{x.summary.paid_total--}],
  ['future_parent',x=>{x.records[19].parents[0]=x.records.length+2}],
  ['signed_pivot',x=>{x.records[19].pivot=1}],
  ['source_forgery',x=>{x.records[7].c=[1,-4,-5,-7]}],
  ['unknown_AND3',x=>{x.records[19].kind='AND3'}]
 ];
 for(const [name,fn] of mutation){const x=clone(base);fn(x);cases.push(replay(x,'581_negative_'+name,false))}
 const answer={run:'LSPV-2/581',status:'PROVED/RESTRICTED symbolic family; COMPUTATIONAL original-OS /386 replay',
  candidate:'Unbounded terminal-live separation between saturated structural DEF/RES congruence and original-checker legal same-clause reuse',
  source:provenance,checker_sha256:sha(fs.readFileSync(checker)),checker_original_body_unchanged:true,
  seed_sha256:sha(fs.readFileSync(seedFile)),seed_bytes:fs.statSync(seedFile).size,
  formulas:{expanded:'W=29+4k',structural_fixed:'W=29+2k',value_plus_terminal_cone:'W=29',gap:'2k'},
  interpretation:'SOURCE identities and paid owner retained. No inference, bound or bridge for full R_mix341. Structural congruence is a subset of semantic clause-value reuse only in this context-free /386 calculus.',
  tests:cases,groups:summaries,
  totals:{accepted:cases.filter(t=>t.accepted).length,rejected:cases.filter(t=>!t.accepted).length,
   checker_assertions:cases.reduce((x,c)=>x+(c.native_assertions||0),0),checker_negative_tests:cases.reduce((x,c)=>x+(c.native_negative_tests||0),0)},
  other_resources:'The measured proof bytes, inference-depth span, script build milliseconds and checker wall milliseconds are NOT paid W. Native peak-space and deterministic machine bit-complexity not measured. The test does not authenticate cross-rule, branching or context operations.'};
 fs.writeFileSync(path.join(out,'581_manifest.json'),JSON.stringify(answer,null,2)+'\n');
 console.log(JSON.stringify({totals:answer.totals,groups:summaries,sha_of_source:provenance.sha256,checker_sha256:answer.checker_sha256}));
}
run();
