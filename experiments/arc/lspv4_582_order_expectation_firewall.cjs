'use strict';
// LSPV-4/582: accepted literal-order proof-verifier resource moments.
// Run: node experiments/arc/lspv4_582_order_expectation_firewall.cjs [--native] [--out /tmp/lspv4_582.json]
// Requires a local j15marti/pnp checkout, Node >=18.
// --native runs the exact pinned original checker on original, min and max alias packets.
// Statistics can be audited without --native and do not infer physical RAM or SAT hardness.
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const crypto=require('node:crypto'),cp=require('node:child_process'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const file=path.join(root,'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json');
const checker=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const pin={packet:'fe27fe1011d0021e721ccaeb747ed58da65d7464',
 checker:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0'};
const blob=b=>crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');
const originalBytes=fs.readFileSync(file),checkerBytes=fs.readFileSync(checker);
assert.equal(blob(originalBytes),pin.packet); assert.equal(blob(checkerBytes),pin.checker);
const data=JSON.parse(originalBytes),clone=x=>JSON.parse(JSON.stringify(x));
function permutations(a){return [[a[0],a[1],a[2]],[a[0],a[2],a[1]],[a[1],a[0],a[2]],
 [a[1],a[2],a[0]],[a[2],a[0],a[1]],[a[2],a[1],a[0]]];}
function literalTrue(lit,bits){return lit>0 ? bits[lit-1]==='1':bits[-lit-1]==='0';}
function probes(lits,bits){let n=0;for(const lit of lits){n++;if(literalTrue(lit,bits))break;}return n;}
function sorterComparisons(lits){const a=lits.map(l=>Math.abs(l)-1);let n=0;
 a.sort((u,v)=>(n++,u-v));return n;}
function parityTripleTest(f,witness){
 const byVertex=Array.from({length:f.graph.n},()=>[]);
 for(const clause of f.clauses)byVertex[clause.vertex].push(clause);
 for(const block of byVertex){assert.equal(block.length,4);
  const ts=block.map(c=>c.literals.reduce((s,l)=>s+(literalTrue(l,witness)?1:0),0)).sort((a,b)=>a-b);
  assert(['0,2,2,2','1,1,1,3'].includes(ts.join(',')),'invalid signed source parity block');
 }
}
function verifyEightLocalPatterns(){
 for(let charge=0;charge<=1;charge++)for(let x=0;x<8;x++){
  const bits=Array.from({length:3},(_,i)=>(x>>i)&1).join('');
  const signed=[];
  for(let mask=0;mask<8;mask++)if(([0,1,2].reduce((s,i)=>s^((mask>>i)&1),0))!==charge)
   signed.push([0,1,2].map(i=>((mask>>i)&1)?-(i+1):(i+1)));
  assert.equal(signed.length,4);let mean6=0;
  for(const c of signed)for(const a of permutations(c))mean6+=probes(a,bits);
  assert.equal(mean6,42,'local uniform permutation mean is not seven');
 }
}
verifyEightLocalPatterns();
let minData=clone(data),maxData=clone(data);
const stat={schema:'LSPV4_582_ORDER_EXPECTATION_FIREWALL/v1',model:'original /341 checker; 6 independent token permutations per original signed ternary SOURCE clause',pins:pin,originalPacketBytes:originalBytes.length,
 fullCheckerOSReplay:'not run unless --native; independent LSPV5/523 published prior OS acceptance',
 clauses:0,vertexWitnessPairs:0,witnesses:0,positiveLocalControls:16,
 witness:{canonical:0,mean6:0,varianceNumerator36:0,min:0,max:0},
 compare:{canonical:0,mean6:0},
 joint:{canonical:0,mean6:0,varianceNumerator36:0,min:0,max:0},
 sourceTableLiteralProbes:0,findScanProbes:0,fixture:[]};
for(let fi=0;fi<data.fixtures.length;fi++){
 const f=data.fixtures[fi],ws=f.deleted.filter(d=>d.assignment!==null).map(d=>d.assignment);
 const t={name:f.graph.name,vertices:f.graph.n,sourceClauses:f.clauses.length,witnesses:ws.length,
  witness:{canonical:0,mean6:0,varianceNumerator36:0,min:0,max:0},
  compare:{canonical:0,mean6:0},
  joint:{canonical:0,mean6:0,varianceNumerator36:0,min:0,max:0}};
 assert.equal(f.clauses.length,4*f.graph.n);
 for(const w of ws){assert.equal(w.length,f.graph.edges.length);parityTripleTest(f,w);}
 stat.vertexWitnessPairs+=f.graph.n*ws.length;stat.witnesses+=ws.length;
 for(let ci=0;ci<f.clauses.length;ci++){
  const c=f.clauses[ci];assert.equal(c.literals.length,3);
  assert.equal(new Set(c.literals.map(Math.abs)).size,3);
  const options=permutations(c.literals).map(lits=>({
   lits,w:ws.reduce((s,b)=>s+probes(lits,b),0),cmp:sorterComparisons(lits)
  }));
  const sw=options.reduce((s,x)=>s+x.w,0),sw2=options.reduce((s,x)=>s+x.w*x.w,0);
  const sj=options.reduce((s,x)=>s+x.w+x.cmp,0);
  const sj2=options.reduce((s,x)=>s+(x.w+x.cmp)**2,0);
  const cmpSum=options.reduce((s,x)=>s+x.cmp,0);
  const lowest=options.slice().sort((a,b)=>(a.w+a.cmp)-(b.w+b.cmp)||a.lits.join(',').localeCompare(b.lits.join(',')))[0];
  const highest=options.slice().sort((a,b)=>(b.w+b.cmp)-(a.w+a.cmp)||a.lits.join(',').localeCompare(b.lits.join(',')))[0];
  for(const z of [stat,t]){
   z.witness.canonical+=options[0].w;z.witness.mean6+=sw;
   z.witness.varianceNumerator36+=6*sw2-sw*sw;
   z.witness.min+=Math.min(...options.map(o=>o.w));z.witness.max+=Math.max(...options.map(o=>o.w));
   z.compare.canonical+=options[0].cmp;z.compare.mean6+=cmpSum;
   z.joint.canonical+=options[0].w+options[0].cmp;z.joint.mean6+=sj;
   z.joint.varianceNumerator36+=6*sj2-sj*sj;
   z.joint.min+=lowest.w+lowest.cmp;z.joint.max+=highest.w+highest.cmp;
  }
  minData.fixtures[fi].clauses[ci].literals=lowest.lits;
  maxData.fixtures[fi].clauses[ci].literals=highest.lits;
  stat.clauses++;stat.findScanProbes+=6;stat.sourceTableLiteralProbes+=14;
 }
 stat.fixture.push(t);
}
assert.equal(stat.vertexWitnessPairs,5896);assert.equal(stat.clauses,328);
assert.equal(stat.witness.canonical,41272);
assert.equal(stat.witness.mean6,6*7*stat.vertexWitnessPairs);
assert.equal(stat.witness.varianceNumerator36,17409088);
assert.equal(stat.witness.min,29238);assert.equal(stat.witness.max,53310);
assert.equal(stat.joint.canonical,41928);
// Comparator invocation counts depend on the actual ECMAScript engine/version, not the native /341 logical tariff.
stat.comparatorEngine={node:process.version,v8:process.versions.v8};
if(process.versions.v8==='12.4.254.21-node.26'){
 assert.equal(stat.joint.min,30133);assert.equal(stat.joint.max,54281);
 assert.equal(stat.joint.varianceNumerator36,17418600);
}
assert.equal(stat.findScanProbes,1968);assert.equal(stat.sourceTableLiteralProbes,4592);
stat.witness.mean=stat.witness.mean6/6;stat.witness.variance=stat.witness.varianceNumerator36/36;
stat.joint.mean=stat.joint.mean6/6;stat.joint.variance=stat.joint.varianceNumerator36/36;
stat.joint.sd=Math.sqrt(stat.joint.variance);
stat.witness.sd=Math.sqrt(stat.witness.variance);
stat.rangeSameBytesAndPaidWork=true;
const minBytes=Buffer.from(JSON.stringify(minData,null,2)+'\n');
const maxBytes=Buffer.from(JSON.stringify(maxData,null,2)+'\n');
stat.extrema={minPacketBytes:minBytes.length,maxPacketBytes:maxBytes.length,
 minPacketBlob:blob(minBytes),maxPacketBlob:blob(maxBytes)};
assert.equal(minBytes.length,originalBytes.length);assert.equal(maxBytes.length,originalBytes.length);
if(process.argv.includes('--native')){
 function runNative(bytes,label){const tmp=path.join(os.tmpdir(),'lspv4_582_'+process.pid+'_'+label+'.json');
  fs.writeFileSync(tmp,bytes);
  const run=cp.spawnSync(process.execPath,[checker,tmp],{encoding:'utf8',maxBuffer:16*1024*1024});
  fs.unlinkSync(tmp);assert.equal(run.status,0,'native '+label+': '+run.stderr.slice(0,600));
  const obj=JSON.parse(run.stdout);assert.equal(obj.checks,30714);return {accepted:true,checks:obj.checks};
 }
 stat.native={original:runNative(originalBytes,'canonical'),min:runNative(minBytes,'min'),
  max:runNative(maxBytes,'max')};
}
const oi=process.argv.indexOf('--out');
if(oi>=0){assert(process.argv[oi+1]);fs.writeFileSync(process.argv[oi+1],JSON.stringify(stat,null,2)+'\n');}
console.log(JSON.stringify(stat,null,2));
