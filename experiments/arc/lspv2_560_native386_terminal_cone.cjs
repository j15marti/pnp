#!/usr/bin/env node
'use strict';
// LSPV-2/560: restricted source-complete terminal-cone normalization.
// This is a REFERENCE transformer and differential harness, NOT the historical R_mix341 checker.
// Run: node experiments/arc/lspv2_560_native386_terminal_cone.cjs [raw-results.json]
function must(b,m){if(!b)throw Error(m)}
function normalize(p){
 must(p&&Array.isArray(p.records)&&Array.isArray(p.gate_defs)&&p.summary,'packet object');
 const rows=p.records,goal=rows.length-1;
 must(goal>=0&&Array.isArray(rows[goal].c)&&rows[goal].c.length===0,'terminal empty clause needed');
 const keep=new Set(),todo=[];
 const add=i=>{must(Number.isInteger(i)&&i>=0&&i<rows.length,'unknown row');if(!keep.has(i)){keep.add(i);todo.push(i)}};
 add(goal);
 // The actual archived /386 checker requires every original SOURCE occurrence,
 // including SOURCE records not in the terminal proof ancestry.
 for(let i=0;i<rows.length;i++)if(rows[i].kind==='SOURCE')add(i);
 while(todo.length){
  const i=todo.pop();
  must(Array.isArray(rows[i].parents),'missing parents');
  for(const q of rows[i].parents){must(q<i,'parent not earlier');add(q)}
 }
 const defsByZ=new Map(),defsById=new Map();
 for(const d of p.gate_defs){
  must(Array.isArray(d)&&d.length===4,'gate tuple');
  must(!defsByZ.has(d[1])&&!defsById.has(d[0]),'duplicate owners');
  defsByZ.set(d[1],d);defsById.set(d[0],d);
 }
 const usedZ=new Set(),gateTodo=[];
 const need=z=>{if(defsByZ.has(z)&&!usedZ.has(z)){usedZ.add(z);gateTodo.push(z)}};
 for(const i of keep){
  const r=rows[i];
  if(r.kind==='DEF'){
   const d=defsById.get(r.gate);must(d,'missing owner');need(d[1]);
  }
  for(const x of r.c)need(Math.abs(x));
 }
 // Owner dependency closure includes gates whose definitions feed another retained gate,
 // even if their outputs do not occur in any retained proof record.
 while(gateTodo.length){
  const d=defsByZ.get(gateTodo.pop());
  need(Math.abs(d[2]));need(Math.abs(d[3]));
 }
 const owners=p.gate_defs.filter(d=>usedZ.has(d[1]));
 const originalToTrim=new Map(),kept=[];
 for(let i=0;i<rows.length;i++)if(keep.has(i)){originalToTrim.set(i,kept.length);kept.push(i)}
 const records=kept.map(i=>{
  const r={...rows[i]};
  r.parents=r.parents.map(j=>{must(originalToTrim.has(j),'dangling parent');return originalToTrim.get(j)});
  return r;
 });
 const source=records.filter(r=>r.kind==='SOURCE').length;
 const facets=records.filter(r=>r.kind==='DEF').length;
 const res=records.filter(r=>r.kind==='RES').length;
 must(source===rows.filter(r=>r.kind==='SOURCE').length,'lost original source occurrence');
 const out={...p,gate_defs:owners,records,summary:{...p.summary,
  source,def_views:facets,resolution:res,paid_gates:owners.length,
  paid_total:owners.length+res,live_records:records.length}};
 const originalWork=p.gate_defs.length+rows.filter(r=>r.kind==='RES').length;
 const afterWork=owners.length+res;
 must(afterWork<=originalWork,'cost rose');
 const log={
  source_occurrences:source,original_records:rows.length,kept_records:records.length,
  original_owner_count:p.gate_defs.length,kept_owner_count:owners.length,
  original_res_count:rows.filter(r=>r.kind==='RES').length,kept_res_count:res,
  original_logical_work:originalWork,trimmed_logical_work:afterWork,
  freed_paid_nodes:originalWork-afterWork,
  old_to_new_record:kept.map((i,j)=>[i,j]),
  retained_owner_ids:owners.map(d=>d[0]),
  // This is a record upper bound, not physical peak-memory measurement.
  retained_record_storage_upper:records.length
 };
 return {packet:out,log};
}
function outputBytes(p){return JSON.stringify(p)+'\n'}
function selftest(root){
 const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process'),os=require('node:os');
 const at=x=>path.join(root,x),checker=at('experiments/arc/lspv2_386_independent_verify.js');
 const seed=at('results/raw/arc/2026-11-11_0407_LSPV2_555_ACCEPTED_LIVE_DEF_RES_K1.json');
 const digest=b=>crypto.createHash('sha256').update(b).digest('hex');
 const gitblob=b=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+b.length+'\0'),b])).digest('hex');
 must(gitblob(fs.readFileSync(checker))==='338305c0ce101704205e57543756b8127074a986','checker blob drift');
 must(gitblob(fs.readFileSync(seed))==='aeeb555c4dcf7f510a9a501c8afc609b629a9298','seed blob drift');
 const original=JSON.parse(fs.readFileSync(seed));
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-lspv2-560-'));
 let cases=[],nativeAsserts=0;
 function native(label,p,expected){
  const b=Buffer.from(outputBytes(p));const file=path.join(tmp,label+'.json');fs.writeFileSync(file,b);
  const child=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',timeout:30000,maxBuffer:1<<20});
  const accepted=child.status===0&&!child.error;
  must(accepted===expected,'original CLI wrong verdict '+label+': '+String(child.stderr||child.error).slice(0,240));
  let checked=null;
  if(accepted){
   checked=JSON.parse(child.stdout.trim());nativeAsserts+=checked.assertions;
   must(checked.negativeTests===11&&checked.paid===p.summary.paid_total,'original native accounting '+label);
  }
  cases.push({name:label,accepted,expected,bytes:b.length,sha256:digest(b),
   native_paid:checked?.paid??null,native_assertions:checked?.assertions??null});
 }
 try{
  native('original_seed',original,true);
  for(const k of [0,1,2,4]){
   let p=structuredClone(original);
   for(let j=0;j<k;j++)p.gate_defs.push([3+j,11+j,1,4]);
   p.summary.paid_gates+=k;p.summary.paid_total+=k;
   native('padded_owners_'+k,p,true);
   let trim=normalize(p);
   must(trim.log.trimmed_logical_work===31&&trim.log.kept_owner_count===1&&
        trim.log.kept_res_count===30&&trim.log.source_occurrences===17&&
        trim.log.kept_records===49,'restricted cone normal form drift at '+k);
   native('trimmed_owners_'+k,trim.packet,true);
  }
  const trim=normalize(original);
  let noOwner=structuredClone(trim.packet);noOwner.gate_defs=[];
  noOwner.summary.paid_gates=0;noOwner.summary.paid_total=30;
  native('missing_required_owner',noOwner,false);
  let badParent=structuredClone(trim.packet);
  badParent.records.at(-1).parents[0]=badParent.records.length+1;
  native('dangling_terminal_parent',badParent,false);
  let falseSource=structuredClone(trim.packet);
  const first=falseSource.records.find(r=>r.kind==='SOURCE');first.c=[12345];
  native('forged_original_source',falseSource,false);
  let badPayment=structuredClone(trim.packet);badPayment.summary.paid_total=30;
  native('underpaid_owner',badPayment,false);
  // Unsound naive pruning deletes all SOURCE records outside final ancestry,
  // violating the archived checker's compulsory source-occurrence coverage.
  const onlyAncestry=structuredClone(original);
  const work=[onlyAncestry.records.length-1],cone=new Set(work);
  while(work.length){let i=work.pop();for(const j of onlyAncestry.records[i].parents)if(!cone.has(j)){cone.add(j);work.push(j)}}
  const ids=[...cone].sort((a,b)=>a-b),ix=new Map(ids.map((j,i)=>[j,i]));
  onlyAncestry.records=ids.map(i=>({...original.records[i],parents:original.records[i].parents.map(j=>ix.get(j))}));
  onlyAncestry.summary.source=onlyAncestry.records.filter(r=>r.kind==='SOURCE').length;
  onlyAncestry.summary.def_views=onlyAncestry.records.filter(r=>r.kind==='DEF').length;
  onlyAncestry.summary.resolution=onlyAncestry.records.filter(r=>r.kind==='RES').length;
  onlyAncestry.summary.live_records=onlyAncestry.records.length;
  onlyAncestry.summary.paid_total=onlyAncestry.summary.resolution+original.gate_defs.length;
  must(onlyAncestry.summary.source<17,'example has no dead SOURCE rows');
  native('naive_goal_ancestry_only',onlyAncestry,false);
  must(cases.length===14,'case count');
  return {id:'LSPV-2/560',status:'PROVED/RESTRICTED normal-form theorem + COMPUTATIONAL original CLI',
   checker_scope:'archived /386 SOURCE paid-DEF facets RES only, NOT complete R_mix341',
   exact_original_checker_blob:'338305c0ce101704205e57543756b8127074a986',
   exact_seed_blob:'aeeb555c4dcf7f510a9a501c8afc609b629a9298',
   native_os:process.version,cases,native_assertions:nativeAsserts,
   normal_form:normalize(original).log,source_hash_or_external_binding:'source occurrences retained; external DIMACS binding requires the separate /559 wrapper',
   time_space:'native logical work excludes certificate serialization, construction, verification, span and peak memory; no physical lower bound',
   open:['P2-D1','P2-C3','P2-B1','P2-B2/B3']};
 }finally{fs.rmSync(tmp,{recursive:true,force:true})}
}
module.exports={normalize,outputBytes,selftest};
if(require.main===module){
 const path=require('node:path'),fs=require('node:fs');
 const result=selftest(path.resolve(__dirname,'../..'));
 if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+'\n');
 process.stdout.write(JSON.stringify(result,null,2)+'\n');
}