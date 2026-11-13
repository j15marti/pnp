'use strict';
/*
 LSPV-4/580: original /341 two-register evidence-cost frontier.
 Run from j15marti/pnp root:
   node experiments/arc/lspv4_580_two_register_string_frontier.cjs
   node experiments/arc/lspv4_580_two_register_string_frontier.cjs --native
   node experiments/arc/lspv4_580_two_register_string_frontier.cjs --out /tmp/audit580.json
 Only SOURCE/AND3/XOR recovered /341 fixture checker, not R_mix341.
*/
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const vm=require('node:vm'),os=require('node:os'),cp=require('node:child_process');
const assert=require('node:assert/strict');
const ROOT=path.resolve(__dirname,'../..');
const CP='experiments/arc/lspv2_341_independent_verify.js';
const PP='results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json';
const C=fs.readFileSync(path.join(ROOT,CP)), P=fs.readFileSync(path.join(ROOT,PP));
const blob=b=>crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');
assert.equal(blob(C),'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0');
assert.equal(blob(P),'fe27fe1011d0021e721ccaeb747ed58da65d7464');
const orig=JSON.parse(P.toString('utf8')),clone=o=>JSON.parse(JSON.stringify(o));
const bytes=o=>Buffer.byteLength(JSON.stringify(o)+'\n','utf8');
function nativeVM(packet){
 let out='',src=C.toString('utf8');
 try {
  vm.runInNewContext(src,{
   require:name=>{assert.equal(name,'fs');return {readFileSync:()=>JSON.stringify(packet)+'\n'}},
   process:{argv:['node',CP,'in-memory.json']},console:{log:s=>{out+=s}}
  },{filename:CP,timeout:20000});
  return {accepted:true,checks:JSON.parse(out).checks};
 }catch(e){return {accepted:false,error:String(e).slice(0,250)}}
}
function sourceTerm(f,c) {
 const E=f.graph.edges.length,support=f.graph.edges.map((uv,i)=>uv.includes(c.vertex)?i:-1).filter(x=>x>=0);
 assert.equal(support.length,3);
 let table=0;
 for(let m=0;m<8;m++){
  const bits=Array(E).fill(0);
  support.forEach((e,j)=>bits[e]=(m>>j)&1);
  if(c.literals.some(l=>l>0?bits[l-1]===1:bits[-l-1]===0))table|=1<<m;
 }
 return {support,table};
}
function tableAt(t,bits){
 let m=0;
 for(let j=0;j<t.support.length;j++)m|=Number(bits[t.support[j]])<<j;
 return (t.table>>m)&1;
}
function rankAndOrder(f,reorder) {
 const map=new Map(f.proof.map(q=>[q.id,q])),memo=new Map(),seen=new Set(),order=[];
 function rank(id){
  if(!map.has(id))return 0;
  if(memo.has(id))return memo.get(id);
  const [a,b]=map.get(id).parents.map(rank);
  const result=a===b?a+1:Math.max(1,a,b);
  memo.set(id,result);return result;
 }
 function emit(id){
  if(!map.has(id)||seen.has(id))return;
  const p=map.get(id);
  const parents=p.parents.slice().sort((a,b)=>rank(b)-rank(a));
  parents.forEach(emit);seen.add(id);order.push(p);
 }
 const peak=rank(f.proof.at(-1).id);
 emit(f.proof.at(-1).id);
 assert.equal(order.length,f.proof.length,'complete tree');
 if(reorder)f.proof=order;
 const refUses=new Map(f.proof.map(q=>[q.id,0])),alive=new Set();
 for(const p of f.proof)for(const id of p.parents)if(refUses.has(id))refUses.set(id,refUses.get(id)+1);
 let livePeak=0;
 for(const p of f.proof){
  for(const id of p.parents)if(refUses.has(id)){
   assert(alive.has(id),'missing retained result '+id);
   refUses.set(id,refUses.get(id)-1);
   if(refUses.get(id)===0)alive.delete(id);
  }
  alive.add(p.id);
  livePeak=Math.max(livePeak,alive.size);
 }
 if(reorder)assert.equal(livePeak,peak,'optimal in-place schedule');
 return {minimum_registers:peak,actual_live_peak:livePeak,final_live:alive.size};
}
function transform(base,k){
 const data=clone(base);
 for(const f of data.fixtures.slice(0,2)){
  const V=f.graph.n,E=f.graph.edges.length;
  assert(E<=9,'single digit original edge IDs required');
  const by=new Map(f.clauses.map(c=>[c.id,sourceTerm(f,c)]));
  for(let v=0;v<Math.min(k,V);v++){
   const src=f.clauses.filter(c=>c.vertex===v).map(c=>c.id);
   assert.equal(src.length,4);
   const [a,b,c]=f.proof.slice(3*v,3*v+3);
   a.parents=src.slice(0,2);
   b.parents=src.slice(2,4);
   c.parents=[a.id,b.id];
  }
  for(let i=0;i<3*V;i++){
   const q=f.proof[i],v=Math.floor(i/3),j=i%3;
   const [a,b]=q.parents.map(x=>by.get(x));
   assert(a&&b,'topological AND3 parents');
   const supportUnion=[...new Set([...a.support,...b.support])];
   assert.equal(supportUnion.length,3);
   const digits=supportUnion.map(String).sort((a,b)=>Number(a)-Number(b));
   assert(digits.every(d=>/^[0-9]$/.test(d)));
   q.support=(v<k||j===2)?digits.join(''):supportUnion.slice();
   let table=0;
   for(let m=0;m<8;m++){
    const bits=Array(E).fill(0);
    for(let j=0;j<3;j++)bits[q.support[j]]=(m>>j)&1;
    if(tableAt(a,bits)&&tableAt(b,bits))table|=1<<m;
   }
   q.table=table;
   by.set(q.id,{support:q.support,table});
  }
  rankAndOrder(f,true);
 }
 return data;
}
function sourceModels(f){
 const E=f.graph.edges.length;let count=0;
 for(let a=0;a<(1<<E);a++){
  const bits=Array.from({length:E},(_,i)=>(a>>i)&1);
  if(f.clauses.every(c=>c.literals.some(l=>l>0?bits[l-1]===1:bits[-l-1]===0)))count++;
 }
 return {assignments:1<<E,models:count};
}
const cases=[],baseBytes=bytes(orig);
function check(name,packet,expected){
 const verdict=nativeVM(packet);
 assert.equal(verdict.accepted,expected,name+' '+verdict.error);
 if(expected)assert.equal(verdict.checks,30714);
 cases.push({name,bytes:bytes(packet),accepted:verdict.accepted,checks:verdict.checks||null,
  error:verdict.error||null});
 return verdict;
}
check('original',orig,true);
const summaries=[];
for(const k of [0,1,2,6]){
 const p=transform(orig,k);
 check('balanced_vertices_per_fixture_'+k,p,true);
 const resources=p.fixtures.slice(0,2).map(f=>({
  fixture:f.graph.name,vertices:f.graph.n,...rankAndOrder(f,false),source:sourceModels(f)
 }));
 assert(resources.every(x=>x.source.models===0));
 summaries.push({k,bytes:bytes(p),saved:baseBytes-bytes(p),resources});
}
assert.deepEqual(summaries.map(x=>x.saved),[20,28,36,60]);
assert.deepEqual(summaries.map(x=>x.resources.map(y=>y.minimum_registers)),[[2,2],[2,2],[3,3],[3,3]]);
const best=transform(orig,1);
const idChars=d=>d.fixtures.reduce((n,f)=>n+f.proof.reduce((m,q)=>m+q.parents.reduce((z,id)=>z+String(id).length,0),0),0);
const paid=d=>d.fixtures.reduce((n,f)=>n+f.proof.length,0),applies=d=>paid(d)*2;
assert.equal(paid(best),321);assert.equal(applies(best),642);
assert.equal(idChars(best),1840);
assert.deepEqual(best.fixtures.slice(0,2).map(f=>sourceModels(f).assignments),[64,512]);
assert.equal(bytes(best),77686);
assert.deepEqual(orig.fixtures.map(f=>f.clauses),best.fixtures.map(f=>f.clauses));
assert.deepEqual(orig.fixtures.map(f=>f.charges),best.fixtures.map(f=>f.charges));
let bad=clone(orig);bad.fixtures[0].proof[0].support='012';
check('left_deep_early_String',bad,false);
bad=clone(best);bad.fixtures[0].proof.find(q=>q.rule==='AND3').table^=1;
check('bad_internal_truth_table',bad,false);
bad=clone(best);bad.fixtures[0].clauses[0].literals[0]*=-1;
check('bad_signed_SOURCE',bad,false);
bad=clone(best);bad.fixtures[0].proof[0].parents[0]='missing_parent';
check('missing_parent',bad,false);
bad=clone(best);bad.fixtures[0].proof.at(-1).row.rhs^=1;
check('bad_terminal_GF2',bad,false);
let osCases=null;
if(process.argv.includes('--native')){
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv4_580_'));
 try{
  osCases=[];
  for(const [name,packet,expect] of [['original',orig,true],['best_peak2',best,true],
   ['two_balanced_peak3',transform(orig,2),true]]){
   const input=path.join(tmp,'packet.json');
   fs.writeFileSync(input,JSON.stringify(packet)+'\n');
   const run=cp.spawnSync(process.execPath,[path.join(ROOT,CP),input],{encoding:'utf8',maxBuffer:16*1024*1024});
   assert.equal(run.status===0,expect,name+' '+run.stderr.slice(0,500));
   const checks=run.status===0?JSON.parse(run.stdout).checks:null;
   if(run.status===0)assert.equal(checks,30714);
   osCases.push({name,accepted:run.status===0,checks});
  }
 }finally{fs.rmSync(tmp,{recursive:true,force:true});}
}
const manifest={schema:'LSPV4_580_TWO_REGISTER_STRING_FRONTIER/v1',
 timestamp:'2026-11-13 00:36 PST',
 status:'PROVED/RESTRICTED finite typed-tree frontier plus original checker computational replay',
 authority:{checker:CP,checker_git_blob:blob(C),packet:PP,packet_git_blob:blob(P)},
 scope:'two fixtures K4 and K33 of seven independent /341 proofs, numeric edge IDs 0..9, fixed source, four SOURCE leaves per vertex; eligible local parenthesizations and String/array supports; no recomputation, atomic last-use overwrite, read-only SOURCE',
 theorem:'For 2-register cap and within the stated typed-tree class, at most one 2+2 all-String vertex per fixture; maximal savings 2*(4+6)+4*2=28 bytes. Canonical minimum 77686 bytes versus original 77714. If peak3 permitted all 10 vertices balanced and all-String saves 60 bytes (77654).',
 counts:{paid:paid(best),parent_applications:applies(best),parent_id_chars:idChars(best),base_bytes:baseBytes,best_two_register_bytes:bytes(best)},
 summaries,cases,osCases,
 caveats:['not complete R_mix341 native calculus','hosted VM unchanged-checker-body replay; OS replay only if --native','no proof discovery, physical RAM, bit-machine verification or shared-DAG minimum theorem','legal GF2, DEF, branch, learning, compact rows and cross-rule shortcuts remain allowed']
};
const arg=process.argv.indexOf('--out');
if(arg>=0){assert(process.argv[arg+1]);fs.writeFileSync(process.argv[arg+1],JSON.stringify(manifest,null,2)+'\n');}
console.log(JSON.stringify({result:'PASS',saved_two_register_bytes:28,minimum_bytes_2:77686,checker_positives:cases.filter(c=>c.accepted).length,checker_negatives:cases.filter(c=>!c.accepted).length,OS:!!osCases},null,2));
