'use strict';
/*
 * LSPV-3/563, 2026-11-10 23:24 America/Los_Angeles.
 * Exact guard-lift and original archived /386 SOURCE/RES acceptance experiment.
 * Standalone: node experiments/arc/lspv3_563_exact_guard_shift_archived_386.cjs
 * No dependencies beyond Node.js standard library and the pinned original checker in this repo.
 * This is NOT the complete historical /341 five-rule R_mix341 verifier.
 */
const PINNED_CHECKER_BLOB='338305c0ce101704205e57543756b8127074a986';
const CHECKER_PATH='experiments/arc/lspv2_386_independent_verify.js';
const PACKET_PATH='results/raw/arc/2026-11-10_2324_LSPV3_563_EXACT_GUARD_NATIVE_PACKET.json';
const RESULTS_PATH='results/raw/arc/2026-11-10_2324_LSPV3_563_EXACT_GUARD_NATIVE_REPLAY.json';
const deep=x=>JSON.parse(JSON.stringify(x));
function canonical(xs) {
 const out=[...new Set(xs)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
 return out.some(x=>out.includes(-x))?null:out;
}
const key=JSON.stringify;
function permutations(a) {
 return a.length<2?[a]:a.flatMap((v,i)=>permutations(a.filter((_,j)=>i!==j)).map(p=>[v,...p]));
}
function sourceData() {
 const spec={h:4,edges:[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],charge:[1,0,0,0],guard:7};
 const source=[];
 for(let v=0;v<4;v++) {
  const incident=spec.edges.map(([u,w],i)=>u===v||w===v?i+1:0).filter(Boolean);
  for(let bits=0;bits<8;bits++) {
   const a=[bits&1,(bits>>1)&1,(bits>>2)&1];
   if((a[0]^a[1]^a[2])!==spec.charge[v])
    source.push({kind:'SOURCE',c:canonical(incident.map((z,i)=>a[i]?-z:z).concat([-7])),parents:[],source:v});
  }
 }
 return {spec,source};
}
function buildOrder(order,spec,source) {
 const records=deep(source);
 records.push({kind:'SOURCE',c:[7],parents:[],source:-1});
 const known=new Map(records.map((r,i)=>[key(r.c),i]));
 const active=new Map(source.map((r,i)=>[key(r.c),i]));
 for(const v of order) {
  const plus=[...active.values()].filter(i=>records[i].c.includes(v));
  const minus=[...active.values()].filter(i=>records[i].c.includes(-v));
  const added=new Map();
  for(const a of plus)for(const b of minus) {
   const c=canonical(records[a].c.filter(x=>x!==v).concat(records[b].c.filter(x=>x!==-v)));
   if(c===null)continue;
   const k=key(c);let i=known.get(k);
   if(i===undefined){i=records.length;records.push({kind:'RES',c,parents:[a,b],pivot:v});known.set(k,i)}
   added.set(k,i);
  }
  for(const a of [...plus,...minus])active.delete(key(records[a].c));
  for(const [k,i] of added)active.set(k,i);
  if(known.has('[-7]'))break;
 }
 const terminal=known.get('[-7]');
 if(terminal===undefined)throw Error('guard sink absent');
 const ancestors=new Set();
 function mark(i){if(ancestors.has(i))return;ancestors.add(i);records[i].parents.forEach(mark)}
 mark(terminal);
 const pureResolution=[...ancestors].filter(i=>records[i].kind==='RES').length;
 const usedSources=[...ancestors].filter(i=>records[i].kind==='SOURCE').length;
 return {order,records,terminal,ancestors,pureResolution,usedSources};
}
function produce() {
 const {spec,source}=sourceData();
 if(source.length!==16)throw Error('source count');
 const all=permutations([1,2,3,4,5,6]).map(p=>buildOrder(p,spec,source));
 all.sort((a,b)=>a.pureResolution-b.pureResolution||a.order.join('').localeCompare(b.order.join('')));
 const best=all[0];
 const keep=new Set([...Array(17).keys(),...best.ancestors]);
 const oldToNew=new Map(),records=[];
 best.records.forEach((r,i)=>{if(keep.has(i)){oldToNew.set(i,records.length);records.push(r)}});
 records.forEach(r=>r.parents=r.parents.map(i=>oldToNew.get(i)));
 records.push({kind:'RES',c:[],parents:[16,oldToNew.get(best.terminal)],pivot:7});
 const nRes=records.filter(r=>r.kind==='RES').length;
 const packet={
  spec,gate_defs:[[0,8,1,2]],records,
  summary:{source:17,def_views:0,resolution:nRes,paid_gates:1,paid_total:nRes+1,live_records:records.length}
 };
 const histogram={};
 for(const c of all)histogram[c.pureResolution]=(histogram[c.pureResolution]||0)+1;
 return {packet,search:{ordersTested:all.length,minPureResolution:best.pureResolution,
          chosenEliminationOrder:best.order,originalSourcesInSinkAncestry:best.usedSources,
          proofRecords:records.length,chargedResolution:nRes,paidUnusedDefinition:1,
          histogramPureResolution:histogram}};
}
function independent(packet) {
 const R=packet.records;const original=R.filter(r=>r.kind==='SOURCE'&&r.source!==-1);
 if(original.length!==16||R.filter(r=>r.kind==='SOURCE').length!==17)throw Error('missing sources');
 const sourceRows=sourceData().source;
 const expected=sourceRows.map(x=>x.source+':'+key(x.c)).sort().join('|');
 const got=original.map(x=>x.source+':'+key(x.c)).sort().join('|');
 if(got!==expected)throw Error('signed-original-source mismatch');
 for(let i=0;i<R.length;i++) {
  const r=R[i];if(!r.parents.every(j=>Number.isInteger(j)&&j>=0&&j<i))throw Error('forward parent');
  if(r.kind==='RES') {
   const [a,b]=r.parents.map(j=>R[j].c),p=r.pivot;
   if(!(a.includes(p)&&b.includes(-p)))throw Error('bad signed pivot');
   const c=canonical(a.filter(x=>x!==p).concat(b.filter(x=>x!==-p)));
   if(c===null||key(c)!==key(r.c))throw Error('incorrect resolvent');
  }
 }
 if(R.at(-1).c.length!==0)throw Error('not a contradiction');
 let odd=0,guardFalse=0;
 for(let mask=0;mask<64;mask++) {
  const sat=original.every(r=>r.c.some(x=>x===-7||(x>0?((mask>>(x-1))&1)===1:((mask>>(-x-1))&1)===0)));
  // At guard=1 each original SOURCE reduces to its signed 3-clause.
  const satAtGuardOne=original.every(r=>r.c.some(x=>x!==-7&&(x>0?((mask>>(x-1))&1)===1:((mask>>(-x-1))&1)===0)));
  if(satAtGuardOne)odd++;
  if(sat)guardFalse++;
 }
 if(odd!==0||guardFalse!==64)throw Error('source model count');
 return {signedSources:original.length,oddModels:odd,guardFalseModels:guardFalse,
   paidResolution:R.filter(r=>r.kind==='RES').length,
   ownerCount:packet.gate_defs.length,source:packet.summary.source,terminal:R.at(-1).c};
}
function replayOriginalBody(originalSource, packet, realCrypto) {
 const logs=[];
 const fsShim={readFileSync:()=>JSON.stringify(packet)};
 const requireShim=name=>{
  if(name==='fs')return fsShim;
  if(name==='crypto')return realCrypto||{createHash:()=>({update:()=>({digest:()=> 'sha256-not-computed-hosted'})})};
  if(name==='assert')return {};
  throw Error('unexpected original checker module '+name);
 };
 try {
  // The fetched archived checker source is executed unchanged, not reimplemented.
  const execute=new Function('require','process','console','structuredClone',originalSource);
  execute(requireShim,{argv:['node',CHECKER_PATH,'certificate.json']},{log:x=>logs.push(x)},deep);
  return {accepted:true,log:logs};
 } catch(e){return {accepted:false,error:String(e),log:logs}}
}
function mutate(packet) {
 const m={
  original_source:p=>p.records[0].c=[-1],
  signed_pivot:p=>p.records.at(-1).pivot=3,
  invalid_fresh_owner:p=>p.gate_defs[0][1]=7,
  even_charge:p=>p.spec.charge[0]=0,
  forward_parent:p=>p.records.at(-1).parents[0]=9999,
  undercharged:p=>p.summary.paid_total--,
  wrong_sink:p=>p.records.at(-1).c=[1]
 };
 const cases={};
 for(const [name,f] of Object.entries(m)){const p=deep(packet);f(p);cases[name]=p}
 return cases;
}
function replayOriginalCore(originalSource,packet) {
 const modules=name=>name==='fs'?{}:name==='crypto'?{}:name==='assert'?{}:(()=>{throw Error(name)})();
 try {
  // The archived checkProof is obtained from the original file without changing its function body.
  // No fixture argv are supplied, so the checker CLI negative-test harness is not executed.
  const getCheck=new Function('require','process','console','structuredClone',originalSource+'\nreturn checkProof;');
  const check=getCheck(modules,{argv:['node',CHECKER_PATH]},{log:()=>{}},deep);
  return {accepted:true,outcome:check(packet,{control:true})};
 } catch(e){return {accepted:false,error:String(e)}}
}
function hostedAudit(originalSource,realCrypto) {
 const {packet,search}=produce(),independentResult=independent(packet),native=replayOriginalBody(originalSource,packet,realCrypto);
 if(!native.accepted)throw Error('archived checker REJECT: '+native.error);
 const noOwner=deep(packet);noOwner.gate_defs=[];noOwner.summary.paid_gates=0;noOwner.summary.paid_total--;
 const noOwnerCore=replayOriginalCore(originalSource,noOwner);
 const noOwnerFullCLI=replayOriginalBody(originalSource,noOwner,realCrypto);
 if(!noOwnerCore.accepted||noOwnerFullCLI.accepted)throw Error('core/CLI asymmetry falsifier failed');
 const hostile={};
 for(const [name,p] of Object.entries(mutate(packet))){
  const r=replayOriginalBody(originalSource,p,realCrypto);
  if(r.accepted)throw Error('hostile accepted: '+name);
  hostile[name]={rejected:true,error:r.error};
 }
 return {packet,raw:{run:'LSPV-3/563',timestamp:'2026-11-10 23:24 PST',
   model:'archived /386 checker; not full R_mix341 /341',
   originalVerifierGitBlob:PINNED_CHECKER_BLOB,search,independent:independentResult,
   originalChecker:{...native,hostile},noOwnerDifferential:{originalCore:noOwnerCore,originalCLI:noOwnerFullCLI},packetBytes:JSON.stringify(packet).length,
   provenanceNote:'Original archived checker body executed unchanged in V8; JS source SHA-256 from Node CLI only.'}};
}
if(typeof module==='object')module.exports={produce,independent,replayOriginalBody,replayOriginalCore,hostedAudit};
if(typeof require==='function'&&require.main===module) {
 const fs=require('fs'),crypto=require('crypto');
 const source=fs.readFileSync(CHECKER_PATH,'utf8');
 const originalBlob=crypto.createHash('sha1').update('blob '+Buffer.byteLength(source)+'\0'+source).digest('hex');
 if(originalBlob!==PINNED_CHECKER_BLOB)throw Error('original-checker blob mismatch: '+originalBlob);
 const report=hostedAudit(source,crypto);
 fs.mkdirSync('results/raw/arc',{recursive:true});
 fs.writeFileSync(PACKET_PATH,JSON.stringify(report.packet));
 report.raw.packetSha256=crypto.createHash('sha256').update(JSON.stringify(report.packet)).digest('hex');
 fs.writeFileSync(RESULTS_PATH,JSON.stringify(report.raw,null,2)+'\n');
 console.log(JSON.stringify(report.raw,null,2));
}