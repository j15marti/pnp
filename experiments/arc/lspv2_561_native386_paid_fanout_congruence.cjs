#!/usr/bin/env node
'use strict';
/* LSPV-2/561: archived /386 ORIGINAL-checker differential runner and
 * REFERENCE-only exact-congruence transformer (not historical R_mix341).
 * Run from repo root: node experiments/arc/lspv2_561_native386_paid_fanout_congruence.cjs [outdir]
 */
const fs=require('node:fs'), path=require('node:path'), os=require('node:os');
const cp=require('node:child_process'), crypto=require('node:crypto'), assert=require('node:assert/strict');
const checker='experiments/arc/lspv2_386_independent_verify.js';
const seedFile='results/raw/arc/2026-11-11_0912_LSPV2_560_ACCEPTED_TRIMMED_NATIVE386_K4.json';
const checkerBlob='338305c0ce101704205e57543756b8127074a986';
const seedBlob='3843187f0ccccf8f04cc049e25a8de1df91ce194';
const copy=x=>JSON.parse(JSON.stringify(x));
const encoded=p=>Buffer.from(JSON.stringify(p)+'\n','utf8');
const sha256=b=>crypto.createHash('sha256').update(b).digest('hex');
const gitBlob=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
function pinned(path,sha){const b=fs.readFileSync(path);assert.equal(gitBlob(b),sha,path+' changed');return b}
function source(p){return JSON.stringify([p.spec,p.records.filter(r=>r.kind==='SOURCE')])}
function work(p){return p.gate_defs.length+p.records.filter(r=>r.kind==='RES').length}
function cone(p){const seen=new Set(),s=[p.records.length-1];
 while(s.length){let j=s.pop();assert.ok(j>=0&&j<p.records.length);
 if(seen.has(j))continue;seen.add(j);s.push(...p.records[j].parents)}return seen}
function depth(p){const d=[];for(const [i,r] of p.records.entries()){
 for(const j of r.parents)assert.ok(j<i);
 d[i]=r.kind==='RES'?1+Math.max(...r.parents.map(j=>d[j])):0}return d.at(-1)}
function split(seed){
 const p=copy(seed),j=20,uses=[];
 p.records.forEach((r,i)=>{if(r.parents.includes(j))uses.push(i)});
 assert.equal(p.records[j].kind,'RES');assert.deepEqual(uses,[22,24]);
 p.records.splice(j+1,0,copy(p.records[j]));
 for(let i=j+2;i<p.records.length;i++)
   p.records[i].parents=p.records[i].parents.map(x=>x>j?x+1:x);
 p.records[uses[1]+1].parents=p.records[uses[1]+1].parents.map(x=>x===j?j+1:x);
 p.summary.resolution++;p.summary.paid_total++;p.summary.live_records++;
 assert.equal(work(p),32);assert.equal(source(p),source(seed));
 assert.ok(cone(p).has(j)&&cone(p).has(j+1),'two distinct paid nodes must be live');
 assert.deepEqual(p.records[j],p.records[j+1]);
 return p
}
/* For nonterminal RES only, identify an inference by its remapped
 * parents, oriented pivot, conclusion, and rule. Never merge on
 * clause text alone. This is restricted to the actual /386 syntax:
 * it does NOT apply to unauthenticated contexts/branches/discharge.
 */
function coalesce(input){
 const p=copy(input),map=new Map(),seen=new Map(),keep=[];
 p.records.forEach((item,old)=>{
  const r=copy(item);
  r.parents=r.parents.map(j=>{assert.ok(map.has(j));return map.get(j)});
  if(r.kind==='RES'&&old!==p.records.length-1){
   const sig=JSON.stringify([r.kind,r.parents,r.pivot,r.c]);
   if(seen.has(sig)){map.set(old,seen.get(sig));return}
   seen.set(sig,keep.length);
  }
  map.set(old,keep.length);keep.push(r)
 });
 p.records=keep;
 p.summary.source=keep.filter(r=>r.kind==='SOURCE').length;
 p.summary.def_views=keep.filter(r=>r.kind==='DEF').length;
 p.summary.resolution=keep.filter(r=>r.kind==='RES').length;
 p.summary.paid_gates=p.gate_defs.length;
 p.summary.paid_total=work(p);
 p.summary.live_records=keep.length;
 assert.equal(source(p),source(input));
 assert.ok(work(p)<=work(input));
 return p
}
function buildCases(seed){
 const live=split(seed),trim=coalesce(live);
 assert.deepEqual(trim,seed);
 const rows=[['original_seed',seed,true],['two_live_paid_RES',live,true],['congruence_inverse',trim,true]];
 const bad=(name,fn)=>{const t=copy(live);fn(t);rows.push([name,t,false])};
 bad('underpaid_RES',t=>t.summary.paid_total--);
 bad('incorrect_RES_count',t=>t.summary.resolution--);
 bad('incorrect_record_count',t=>t.summary.live_records--);
 bad('bad_second_pivot',t=>t.records[21].pivot=1);
 bad('forged_second_clause',t=>t.records[21].c=[-1,-4,-7]);
 bad('future_parent',t=>t.records[25].parents[0]=25);
 bad('forged_SOURCE',t=>t.records[2].c=[-2]);
 bad('same_sign_parent_pair',t=>t.records[25].parents=[21,21]);
 return {rows,live,trim}
}
function originalCLI(buf,file){
 fs.writeFileSync(file,buf);
 const r=cp.spawnSync(process.execPath,[checker,file],{encoding:'utf8',timeout:20000,maxBuffer:1048576});
 assert.equal(r.error,undefined,'original checker subprocess did not start');
 const accept=r.status===0;
 return {accept,exit:r.status,
  original:accept?JSON.parse(r.stdout.trim().split(/\r?\n/).at(-1)):null,
  error:accept?null:(r.stderr||r.stdout).slice(0,250)}
}
function main(){
 const checkerBytes=pinned(checker,checkerBlob),seedBytes=pinned(seedFile,seedBlob);
 const seed=JSON.parse(seedBytes.toString('utf8')),{rows,live,trim}=buildCases(seed);
 assert.ok(encoded(trim).equals(seedBytes));assert.equal(depth(live),depth(seed));
 const outdir=process.argv[2];
 if(outdir)fs.mkdirSync(outdir,{recursive:true});
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2-561-'));
 try{
  const tests=rows.map(([name,p,expect])=>{
   const b=encoded(p),r=originalCLI(b,path.join(tmp,name+'.json'));
   assert.equal(r.accept,expect,'original /386 acceptance mismatch: '+name);
   if(r.accept){assert.equal(r.original.paid,work(p));assert.equal(r.original.negativeTests,11)}
   if(outdir)fs.writeFileSync(path.join(outdir,name+'.json'),b);
   return {name,expected:expect,accepted:r.accept,bytes:b.length,sha256:sha256(b),
    records:p.records.length,paid:work(p),depth:depth(p),...r}
  });
  const m={run:'LSPV-2/561',date_pst:'2026-11-11',
   checker:'unchanged archived /386 original Node operating-system subprocess',
   checker_blob:checkerBlob,checker_sha256:sha256(checkerBytes),
   seed_blob:seedBlob,seed_sha256:sha256(seedBytes),
   source_identical:source(seed)===source(live),
   both_paid_duplicate_nodes_terminal_live:cone(live).has(20)&&cone(live).has(21),
   identical_clause_sets:JSON.stringify([...new Set(seed.records.map(r=>JSON.stringify(r.c)))].sort())===
                        JSON.stringify([...new Set(live.records.map(r=>JSON.stringify(r.c)))].sort()),
   byte_exact_inverse:encoded(trim).equals(seedBytes),
   full_R_mix341_authenticated:false,
   resource_scope:'logical paid work, encoded bytes, logical depth; no physical time/space claims',
   cases:tests,positive:tests.filter(t=>t.accepted).length,
   negative:tests.filter(t=>!t.accepted).length};
  assert.equal(m.positive,3);assert.equal(m.negative,8);
  if(outdir)fs.writeFileSync(path.join(outdir,'manifest.json'),JSON.stringify(m,null,2)+'\n');
  console.log(JSON.stringify(m,null,2))
 }finally{fs.rmSync(tmp,{recursive:true,force:true})}
}
if(require.main===module)main();
module.exports={split,coalesce,buildCases,cone,depth};
