'use strict';
// LSPV-4/572: run from the j15marti/pnp repository root with Node >=18.
// This is the original archived /341 SOURCE/AND3/XOR checker ONLY.
const fs=require('node:fs'),os=require('node:os'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process'),assert=require('node:assert/strict');
const BASE='results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json';
const CHECK='experiments/arc/lspv2_341_independent_verify.js';
const RAW='results/raw/arc/2026-11-12_1636_LSPV4_572_TWO_REGISTER_RETENTION_RAW.json';
const root=process.cwd();
function gitblob(b){return crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');}
function pinned(f,sha){const b=fs.readFileSync(path.join(root,f));assert.equal(gitblob(b),sha,f+' changed');return b.toString('utf8');}
pinned(CHECK,'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0');
const packet=JSON.parse(pinned(BASE,'fe27fe1011d0021e721ccaeb747ed58da65d7464'));
const golden=JSON.parse(fs.readFileSync(path.join(root,RAW),'utf8'));
const clone=v=>JSON.parse(JSON.stringify(v));
function auditFixture(f) {
 const by=new Map(f.proof.map(p=>[p.id,p]));
 assert.equal(by.size,f.proof.length);
 const leafIds=new Set(f.clauses.map(c=>c.id));
 assert.equal(leafIds.size,f.clauses.length);
 const fanout=new Map();
 for(const p of f.proof)for(const q of p.parents)fanout.set(q,(fanout.get(q)||0)+1);
 const terminal=f.proof.at(-1).id;
 assert(f.clauses.every(c=>fanout.get(c.id)===1));
 assert(f.proof.every(p=>p.id===terminal? !fanout.has(p.id):fanout.get(p.id)===1));
 const memo=new Map();
 function rank(id){if(!by.has(id)){assert(leafIds.has(id));return {reg:0,span:0};}
  if(memo.has(id))return memo.get(id);
  const [a,b]=by.get(id).parents.map(rank);
  const v={reg:a.reg===b.reg?a.reg+1:Math.max(a.reg,b.reg),span:1+Math.max(a.span,b.span)};memo.set(id,v);return v;
 }
 function build(id,seq){if(!by.has(id))return;const p=by.get(id),[a,b]=p.parents;const [A,B]=[rank(a),rank(b)]; if(B.reg>A.reg){build(b,seq);build(a,seq);}else{build(a,seq);build(b,seq);}seq.push(p);}
 const seq=[];build(terminal,seq);
 assert.equal(seq.length,f.proof.length);
 function simulate(list){
  let live=new Set(),peak=0,area=0;
  for(const p of list){
   const paid=p.parents.filter(x=>by.has(x));
   assert(paid.every(x=>live.has(x)),p.id+' parent not retained');
   // Read both parents, then destructively overwrite a dying paid parent.
   const temporary=live.size+(paid.length===0?1:0);
   peak=Math.max(peak,temporary);
   paid.forEach(x=>live.delete(x)); live.add(p.id);
   area+=live.size;
  }
  assert(live.size===1&&live.has(terminal));
  return {peak,retained_slot_steps:area};
 }
 const orig=simulate(f.proof),opt=simulate(seq),V=f.graph.n;
 assert.equal(f.clauses.length,4*V);assert.equal(f.proof.length,4*V-1);
 assert.equal(rank(terminal).reg,2);assert.equal(rank(terminal).span,V+2);
 assert.equal(orig.peak,V);assert.equal(orig.retained_slot_steps,2*V*V+V);
 assert.equal(opt.peak,2);assert.equal(opt.retained_slot_steps,7*V-4);
 return {graph:f.graph.name,vertices:V,source_records:f.clauses.length,paid_nodes:f.proof.length,
  source_applications:4*V,paid_result_applications:4*V-2,
  parent_applications:2*(4*V-1),paid_span:rank(terminal).span,register_lower_bound:2,
  producer:orig,two_register:opt,permuted_proof_ids:seq.map(x=>x.id)};
}
const results=packet.fixtures.map(auditFixture);
const optimized=clone(packet);
optimized.fixtures.forEach((f,i)=>{
 const dict=new Map(f.proof.map(p=>[p.id,p]));
 f.proof=results[i].permuted_proof_ids.map(id=>dict.get(id));
});
assert.equal(Buffer.byteLength(JSON.stringify(packet)+'\n'),77714);
assert.equal(Buffer.byteLength(JSON.stringify(packet)+'\n'),Buffer.byteLength(JSON.stringify(optimized)+'\n'));
assert.deepEqual(results,golden.fixtures);
function native(p){
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv4-572-'));
 const file=path.join(dir,'packet.json');fs.writeFileSync(file,JSON.stringify(p)+'\n');
 try {
  const o=cp.execFileSync(process.execPath,[path.join(root,CHECK),file],{encoding:'utf8',timeout:30000,maxBuffer:1<<20});
  return {accept:true,checks:JSON.parse(o).checks};
 }catch(e){return {accept:false,error:String(e.stderr||e.message).slice(0,200)};}
 finally{fs.rmSync(dir,{recursive:true,force:true});}
}
const control1=native(packet),control2=native(optimized);
assert(control1.accept&&control2.accept,'native checker rejected a legal reorder');
assert.equal(control1.checks,30714);assert.equal(control2.checks,30714);
const negatives=[];
let corrupted=clone(optimized);
[corrupted.fixtures[0].proof[0],corrupted.fixtures[0].proof[1]]=[corrupted.fixtures[0].proof[1],corrupted.fixtures[0].proof[0]];
negatives.push({name:'child_before_parent',...native(corrupted)});
corrupted=clone(optimized);corrupted.fixtures[0].proof[0].parents[0]='nonexistent';
negatives.push({name:'forged_parent',...native(corrupted)});
corrupted=clone(optimized);corrupted.fixtures[0].proof.at(-1).row.rhs^=1;
negatives.push({name:'bad_terminal_row',...native(corrupted)});
assert(negatives.every(v=>!v.accept));
const summary={tag:'LSPV-4/572',restriction:'seven separate /341 original SOURCE-AND3-XOR fixture trees',
 historical_full_R_mix341_authenticated:false,original_cli_positive:control1,optimized_cli_positive:control2,
 hostile_rejected:negatives.length,hostiles:negatives,matched_golden:true,
 total_paid:results.reduce((a,v)=>a+v.paid_nodes,0),
 total_parent_apps:results.reduce((a,v)=>a+v.parent_applications,0),
 original_compact_packet_bytes:77714,optimized_compact_packet_bytes:77714};
console.log(JSON.stringify(summary,null,2));
