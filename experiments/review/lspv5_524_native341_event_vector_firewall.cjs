'use strict';
// LSPV-5/524: independent event-vector audit of LSPV-4/582.
// Usage: node experiments/review/lspv5_524_native341_event_vector_firewall.cjs --out FILE
const fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const crypto=require('node:crypto'),cp=require('node:child_process'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const packetPath=path.join(root,'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json');
const checkerPath=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const pin={packet:'fe27fe1011d0021e721ccaeb747ed58da65d7464',checker:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0'};
const gitBlob=b=>crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');
const packetBytes=fs.readFileSync(packetPath),checkerBytes=fs.readFileSync(checkerPath);
assert.equal(gitBlob(packetBytes),pin.packet);assert.equal(gitBlob(checkerBytes),pin.checker);
const packet=JSON.parse(packetBytes),clone=x=>JSON.parse(JSON.stringify(x));

function perms(a){return [[a[0],a[1],a[2]],[a[0],a[2],a[1]],[a[1],a[0],a[2]],
 [a[1],a[2],a[0]],[a[2],a[0],a[1]],[a[2],a[1],a[0]]];}
function litTrue(lit,bits){return lit>0?Number(bits[lit-1])===1:Number(bits[-lit-1])===0;}
function shortCircuitProbes(lits,bits){let n=0;for(const lit of lits){n++;if(litTrue(lit,bits))break;}return n;}
function builtinSortComparisons(lits){const a=lits.map(x=>Math.abs(x)-1);let n=0;a.sort((u,v)=>(n++,u-v));return n;}
function insertionSortComparisons(lits){const a=lits.map(x=>Math.abs(x)-1);let n=0;
 for(let i=1;i<a.length;i++){const x=a[i];let j=i-1;while(j>=0){n++;if(a[j]<=x)break;a[j+1]=a[j--];}a[j+1]=x;}return n;}
function networkSortComparisons(lits){const a=lits.map(x=>Math.abs(x)-1);let n=0;
 function cs(i,j){n++;if(a[i]>a[j])[a[i],a[j]]=[a[j],a[i]];}cs(0,1);cs(1,2);cs(0,1);return n;}
function witnesses(f){return f.deleted.filter(d=>d.assignment!==null).map(d=>d.assignment);}
function incidence(f,v){const out=[];for(let i=0;i<f.graph.edges.length;i++){const [a,b]=f.graph.edges[i];if(a===v||b===v)out.push(i);}return out;}
function runNative(bytes,label){const tmp=path.join(os.tmpdir(),`lspv5_524_${process.pid}_${label}.json`);fs.writeFileSync(tmp,bytes);
 const r=cp.spawnSync(process.execPath,[checkerPath,tmp],{encoding:'utf8',maxBuffer:16*1024*1024});fs.unlinkSync(tmp);
 assert.equal(r.status,0,`${label}: ${r.stderr.slice(0,500)}`);const obj=JSON.parse(r.stdout);assert.equal(obj.checks,30714);
 return {accepted:true,checks:obj.checks};}

const models={v8_builtin:builtinSortComparisons,insertion:insertionSortComparisons,network3:networkSortComparisons};
const stats={};for(const name of Object.keys(models))stats[name]={literalSort:{canonical:0,mean6:0,min:0,max:0},joint:{canonical:0,mean6:0,min:0,max:0,varianceNumerator36:0}};
let sourceClauses=0,vertexWitnessPairs=0,witnessCanonical=0,witnessMean6=0,witnessMin=0,witnessMax=0,witnessVar36=0;
let sourceTableLiteralProbes=0,findPredicateEvaluations=0,incidenceSortComparisonsV8=0;
const minPacket=clone(packet),maxPacket=clone(packet);
for(let fi=0;fi<packet.fixtures.length;fi++){
 const f=packet.fixtures[fi],ws=witnesses(f);vertexWitnessPairs+=f.graph.n*ws.length;
 for(let ci=0;ci<f.clauses.length;ci++){
  const c=f.clauses[ci],options=perms(c.literals).map(lits=>({lits,w:ws.reduce((s,b)=>s+shortCircuitProbes(lits,b),0)}));
  const canonicalW=ws.reduce((s,b)=>s+shortCircuitProbes(c.literals,b),0);
  const sw=options.reduce((s,o)=>s+o.w,0),sw2=options.reduce((s,o)=>s+o.w*o.w,0);
  witnessCanonical+=canonicalW;witnessMean6+=sw;witnessVar36+=6*sw2-sw*sw;
  witnessMin+=Math.min(...options.map(o=>o.w));witnessMax+=Math.max(...options.map(o=>o.w));
  for(const [name,cost] of Object.entries(models)){
   const xs=options.map(o=>({...o,cmp:cost(o.lits)})),canonicalCmp=cost(c.literals);
   const sj=xs.reduce((s,o)=>s+o.w+o.cmp,0),sj2=xs.reduce((s,o)=>s+(o.w+o.cmp)**2,0);
   stats[name].literalSort.canonical+=canonicalCmp;stats[name].literalSort.mean6+=xs.reduce((s,o)=>s+o.cmp,0);
   stats[name].literalSort.min+=Math.min(...xs.map(o=>o.cmp));stats[name].literalSort.max+=Math.max(...xs.map(o=>o.cmp));
   stats[name].joint.canonical+=canonicalW+canonicalCmp;stats[name].joint.mean6+=sj;
   stats[name].joint.min+=Math.min(...xs.map(o=>o.w+o.cmp));stats[name].joint.max+=Math.max(...xs.map(o=>o.w+o.cmp));
   stats[name].joint.varianceNumerator36+=6*sj2-sj*sj;
  }
  const v8=options.map(o=>({...o,cmp:builtinSortComparisons(o.lits)}));
  v8.sort((a,b)=>(a.w+a.cmp)-(b.w+b.cmp)||a.lits.join(',').localeCompare(b.lits.join(',')));
  minPacket.fixtures[fi].clauses[ci].literals=v8[0].lits;maxPacket.fixtures[fi].clauses[ci].literals=v8.at(-1).lits;
  const inc=incidence(f,c.vertex);assert.equal(inc.length,3);incidenceSortComparisonsV8+=builtinSortComparisons(inc.map(x=>x+1));
  findPredicateEvaluations+=6;
  for(let m=0;m<8;m++){const bits=Array(f.graph.edges.length).fill(0);inc.forEach((e,j)=>bits[e]=(m>>j)&1);sourceTableLiteralProbes+=shortCircuitProbes(c.literals,bits);}
  sourceClauses++;
 }
}
assert.equal(sourceClauses,328);assert.equal(vertexWitnessPairs,5896);
assert.equal(witnessCanonical,41272);assert.equal(witnessMean6,247632);assert.equal(witnessVar36,17409088);
assert.equal(witnessMin,29238);assert.equal(witnessMax,53310);assert.equal(sourceTableLiteralProbes,4592);
assert.equal(findPredicateEvaluations,1968);assert.equal(incidenceSortComparisonsV8,656);
assert.equal(stats.v8_builtin.joint.canonical,41928);
for(const s of Object.values(stats)){
 s.literalSort.mean=s.literalSort.mean6/6;s.joint.mean=s.joint.mean6/6;s.joint.variance=s.joint.varianceNumerator36/36;
}
const omittedConstant={incidenceSortComparisonsV8,findPredicateEvaluations,sourceTableLiteralProbes,
 total:incidenceSortComparisonsV8+findPredicateEvaluations+sourceTableLiteralProbes};
for(const s of Object.values(stats))s.augmentedSelected={canonical:s.joint.canonical+omittedConstant.total,
 mean:s.joint.mean+omittedConstant.total,min:s.joint.min+omittedConstant.total,max:s.joint.max+omittedConstant.total};
const minBytes=Buffer.from(JSON.stringify(minPacket,null,2)+'\n'),maxBytes=Buffer.from(JSON.stringify(maxPacket,null,2)+'\n');
assert.equal(minBytes.length,packetBytes.length);assert.equal(maxBytes.length,packetBytes.length);
const native={original:runNative(packetBytes,'original'),v8Min:runNative(minBytes,'v8min'),v8Max:runNative(maxBytes,'v8max')};
const result={schema:'LSPV5_524_NATIVE341_EVENT_VECTOR_FIREWALL/v1',timestamp:new Date().toISOString(),runtime:{node:process.version,v8:process.versions.v8,platform:process.platform,arch:process.arch},
 authority:{checkerPath:path.relative(root,checkerPath),checkerBlob:pin.checker,packetPath:path.relative(root,packetPath),packetBlob:pin.packet,packetBytes:packetBytes.length},
 portable:{sourceClauses,vertexWitnessPairs,witnessLiteralProbes:{canonical:witnessCanonical,mean:witnessMean6/6,variance:witnessVar36/36,min:witnessMin,max:witnessMax},sourceTableLiteralProbes,findPredicateEvaluations},
 sortModels:stats,omittedFromLSPV4_582_joint:omittedConstant,native,
 extremaPackets:{v8MinBlob:gitBlob(minBytes),v8MaxBlob:gitBlob(maxBytes),bytes:minBytes.length},
 conclusions:[
  'The unchanged checker accepts the V8-minimum and V8-maximum literal-order packets with 30,714 assertion groups.',
  'The 41,272 witness-probe result and its exact moments reproduce and are portable over the six-order product class.',
  'The quantity named joint in LSPV-4/582 is witness probes plus one engine-specific literal-array sort comparator count; it omits at least the separately reported find scans, source-table probes, and the incidence-array sort comparisons executed by the same checker.',
  'ECMAScript permits an implementation-defined sequence of comparator calls, and the insertion/network controls give different scalar totals while preserving sorted results. Thus joint is not a historical R_mix341 weight or complete verifier cost.',
  'A sound statement is the nonnegative partial-event lower envelope, together with a vector ledger and a pinned runtime for any engine-event coordinate.'
 ],scope:['P2-D1 accepted-operation/cost authentication only','does not falsify the portable witness-moment theorem','does not establish P2-C3 or P2-B1','P2-B2/B3 remain separate','P versus NP remains OPEN']};
const oi=process.argv.indexOf('--out');if(oi>=0){assert(process.argv[oi+1]);fs.writeFileSync(process.argv[oi+1],JSON.stringify(result,null,2)+'\n');}
console.log(JSON.stringify(result,null,2));
