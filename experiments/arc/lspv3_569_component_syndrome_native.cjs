#!/usr/bin/env node
'use strict';
// LSPV-3/569. A source-exact disconnected /386 gauge-orbit differential.
// Run in full j15marti/pnp checkout:
//   node experiments/arc/lspv3_569_component_syndrome_native.cjs
// This invokes the unchanged ORIGINAL archived /386 checker via OS Node.
// Does NOT authenticate the missing full R_mix341 grammar.
const fs=require('node:fs'), path=require('node:path'), os=require('node:os');
const crypto=require('node:crypto'), cp=require('node:child_process');
const assert=require('node:assert/strict');
const ROOT=path.resolve(__dirname,'../..');
const CK=path.join(ROOT,'experiments/arc/lspv2_386_independent_verify.js');
const SEED=path.join(ROOT,'results/raw/arc/2026-11-11_0224_LSPV3_566_K4x3_CLI_ACCEPTED_PACKET.json');
const EXPECT={checker:'338305c0ce101704205e57543756b8127074a986',seed:'4656b801feba72b84133bacad5ae18692a83fe03'};
const gitBlob=buf=>crypto.createHash('sha1').update(Buffer.concat([Buffer.from('blob '+buf.length+'\0'),buf])).digest('hex');
assert.equal(gitBlob(fs.readFileSync(CK)),EXPECT.checker);
const input=fs.readFileSync(SEED);
assert.equal(gitBlob(input),EXPECT.seed);
const seed=JSON.parse(input),clone=x=>JSON.parse(JSON.stringify(x));
const canonical=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
assert.equal(seed.spec.h,12);assert.equal(seed.spec.edges.length,18);
assert.equal(seed.summary.paid_total,29);assert.equal(seed.records.length,77);
function componentSwap(q,j){
 const d=clone(q),vs=x=>{const a=Math.floor(x/4),i=x%4;return a===0?4*j+i:a===j?i:x};
 const es=x=>{const a=Math.floor((x-1)/6),i=(x-1)%6;return a===0?6*j+i+1:a===j?i+1:x};
 const ls=x=>Math.abs(x)<=18?Math.sign(x)*es(Math.abs(x)):x;
 d.spec.charge=Array(q.spec.h).fill(0);
 q.spec.charge.forEach((z,i)=>{d.spec.charge[vs(i)]=z});
 d.spec.edges=Array(q.spec.edges.length).fill(null);
 q.spec.edges.forEach(([a,b],i)=>{d.spec.edges[es(i+1)-1]=[vs(a),vs(b)].sort((x,y)=>x-y)});
 assert.deepEqual(d.spec.edges,seed.spec.edges,'fixed labeled source graph');
 d.records.forEach(r=>{
   r.c=canonical(r.c.map(ls));
   if(r.source>=0)r.source=vs(r.source);
   if(r.kind==='RES')r.pivot=ls(r.pivot);
 });
 d.gate_defs=d.gate_defs.map(([id,z,a,b])=>[id,z,ls(a),ls(b)]);
 return d;
}
function flipChargeWithSource(d,v){
 d.spec.charge[v]^=1;
 const inc=[];
 d.spec.edges.forEach(([a,b],i)=>{if(a===v||b===v)inc.push(i+1)});
 assert.equal(inc.length,3);
 const expected=[];
 for(let p=0;p<8;p++){
   const bits=[p&1,(p>>1)&1,(p>>2)&1];
   if((bits[0]^bits[1]^bits[2])!==d.spec.charge[v])
     expected.push(canonical([...inc.map((e,i)=>bits[i]?-e:e),-d.spec.guard]));
 }
 const rows=d.records.filter(r=>r.kind==='SOURCE'&&r.source===v);
 assert.equal(rows.length,4);assert.equal(expected.length,4);
 rows.forEach((r,i)=>{r.c=expected[i]});
}
function components(d){
 const adj=Array.from({length:d.spec.h},()=>[]);
 d.spec.edges.forEach(([a,b])=>{adj[a].push(b);adj[b].push(a)});
 const seen=new Set(),blocks=[];
 for(let v=0;v<d.spec.h;v++)if(!seen.has(v)){
  const stack=[v],block=[];seen.add(v);
  while(stack.length){const u=stack.pop();block.push(u);for(const w of adj[u])if(!seen.has(w)){seen.add(w);stack.push(w)}}
  blocks.push(block.sort((a,b)=>a-b));
 }
 return blocks.sort((a,b)=>a[0]-b[0]);
}
function syndrome(d){
 return components(d).map(block=>block.reduce((a,v)=>a^d.spec.charge[v],0));
}
function validateSource(d){
 const expected=new Set(),G=d.spec.guard,edges=d.spec.edges;
 const blocks=components(d);
 assert.equal(blocks.length,3);assert(blocks.every(a=>a.length===4));
 assert.deepEqual(edges,seed.spec.edges);
 expected.add('-1:'+JSON.stringify([G]));
 for(let v=0;v<d.spec.h;v++){
   let inc=[];edges.forEach(([a,b],i)=>{if(a===v||b===v)inc.push(i+1)});
   assert.equal(inc.length,3);
   for(let p=0;p<8;p++){
     const bits=[p&1,p>>1&1,p>>2&1];
     if((bits[0]^bits[1]^bits[2])!==d.spec.charge[v])
       expected.add(v+':'+JSON.stringify(canonical([...inc.map((e,i)=>bits[i]?-e:e),-G])));
   }
 }
 const actual=d.records.filter(r=>r.kind==='SOURCE').map(r=>r.source+':'+JSON.stringify(r.c));
 assert.equal(actual.length,49);assert.equal(expected.size,49);
 assert.equal(new Set(actual).size,49);
 actual.forEach(x=>assert(expected.has(x),'source mismatch'));
 return true;
}
function incidenceRank(d){
 const h=d.spec.h,E=d.spec.edges.length,rows=Array(h).fill(0n);
 d.spec.edges.forEach(([a,b],e)=>{rows[a]^=1n<<BigInt(e);rows[b]^=1n<<BigInt(e)});
 let rank=0;
 for(let k=0;k<E;k++){
  const pivot=rows.findIndex((r,i)=>i>=rank&&((r>>BigInt(k))&1n)===1n);
  if(pivot<0)continue;
  [rows[pivot],rows[rank]]=[rows[rank],rows[pivot]];
  for(let i=0;i<h;i++)if(i!==rank&&((rows[i]>>BigInt(k))&1n)===1n)rows[i]^=rows[rank];
  rank++;
 }
 return rank;
}
function originalCLI(d){
 const bytes=Buffer.from(JSON.stringify(d)+'\n');
 const dir=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-569-'));
 try {
  const pth=path.join(dir,'packet.json');fs.writeFileSync(pth,bytes);
  const p=cp.spawnSync(process.execPath,[CK,pth],{encoding:'utf8',timeout:30000,maxBuffer:1<<20});
  if(p.error)throw p.error;
  if(p.status!==0)return {accepted:false,bytes:bytes.length,sha256:crypto.createHash('sha256').update(bytes).digest('hex'),error:p.stderr.trim().split('\n').slice(0,2).join(' | ')};
  const out=JSON.parse(p.stdout.trim().split('\n').at(-1));
  assert.equal(out.paid,29);assert.equal(out.sources,49);assert.equal(out.res,28);
  assert.equal(out.def,1);assert.equal(out.negativeTests,11);
  return {accepted:true,bytes:bytes.length,sha256:crypto.createHash('sha256').update(bytes).digest('hex'),original_assertions:out.assertions,original_negative_tests:out.negativeTests,paid:out.paid};
 }finally{fs.rmSync(dir,{recursive:true,force:true})}
}
const sourceCases=[
 ['100',clone(seed)],['010',componentSwap(seed,1)],['001',componentSwap(seed,2)]
];
const allOdd=clone(seed);flipChargeWithSource(allOdd,4);flipChargeWithSource(allOdd,8);
sourceCases.push(['111',allOdd]);
const positives=[];
for(const [name,d] of sourceCases){
 assert.equal(validateSource(d),true);
 assert.equal(syndrome(d).join(''),name);
 assert.equal(incidenceRank(d),9);
 const result=originalCLI(d);assert(result.accepted,name+' original checker reject');
 positives.push({componentParity:name,source:49,paidOwners:1,paidResolution:28,logicalWork:29,records:77,sourceGraphFixed:true,...result});
}
const negatives=[];
function negative(name,original,mutate){
 const d=clone(original);mutate(d);
 const result=originalCLI(d);assert(!result.accepted,name+' unexpectedly accepted');
 negatives.push({name,...result});
}
negative('same_odd_global_parity_but_mismatched_source',allOdd,d=>{d.spec.charge[4]^=1;d.spec.charge[5]^=1});
negative('even_total_component_charge',allOdd,d=>flipChargeWithSource(d,8));
negative('underpaid_owner',sourceCases[1][1],d=>d.summary.paid_total--);
negative('forged_source_id',sourceCases[1][1],d=>d.records.find(r=>r.source===4).source=999);
negative('undefined_gate_input',sourceCases[1][1],d=>d.gate_defs[0][2]=0);
negative('wrong_signed_source',sourceCases[0][1],d=>{d.records.find(r=>r.source===8).c[0]*=-1});
const sourceParityVectors=positives.map(x=>x.componentParity);
assert.equal(new Set(sourceParityVectors).size,4);
const result={run:'LSPV-3/569',timestamp:'2026-11-11 05:24 PST',
 status:'PROVED/RESTRICTED linear-algebra orbit theorem + COMPUTATIONAL actual original archived /386 OS Node checker',
 checker_git_blob:EXPECT.checker,seed_git_blob:EXPECT.seed,
 graph:'3 disjoint K4, fixed 12 vertices, 18 edges, 3 connected components',
 incidence_rank:9,global_odd_component_orbits:4,positive_count:positives.length,negative_count:negatives.length,
 positives,negatives,known_full_historical_R_mix341_parser:false,
 proof_chain:{'P2-D1':'OPEN','P2-C3':'OPEN','P2-B1':'OPEN','P2-B2/B3':'OPEN'},
 caveat:'Archived /386 only, not a mixed-rule checker. OS tests must be executed in full checkout to assert OS provenance.'};
console.log(JSON.stringify(result,null,2));
