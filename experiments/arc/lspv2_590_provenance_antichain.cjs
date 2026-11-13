#!/usr/bin/env node
'use strict';
/* LSPV-2/590: exact source-provenance antichain for the signed [-guard]
   clause in a fixed guarded disjoint odd-K4 source. Only the unchanged
   archived /386 checker is operationally authoritative for ACCEPT/REJECT.
   This program is a separate REFERENCE producer and audit, not R_mix341. */
const fs=require('fs'),cp=require('child_process'),crypto=require('crypto'),path=require('path'),os=require('os');
const assert=require('assert/strict');
const p=process.argv;
const checker=p[2]||path.join(__dirname,'original_native386_checker.js');
const seedfile=p[3]||path.join(__dirname,'baseline_W29.json');
const sourcefile=p[4]||path.join(__dirname,'SOURCE.cnf');
const out=p[5]||path.join(__dirname,'590_raw.json');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const cb=fs.readFileSync(checker),sb=fs.readFileSync(seedfile),source=fs.readFileSync(sourcefile);
assert.equal(sha(cb),'22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113','immutable checker mismatch');
assert.equal(sha(sb),'0d8b1894f91d00c554727a92fed35b2bb58f2b1602f2a3cfcb949effda43ceb0','seed mismatch');
assert.equal(sha(source),'3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c','source mismatch');
const seed=JSON.parse(sb),sr=seed.records.filter(r=>r.kind==='SOURCE'),rs=seed.records.filter(r=>r.kind==='RES');
assert.equal(sr.length,17);assert.equal(rs.length,28);
const norm=xs=>[...new Set(xs)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
function build(k,j){
 assert(k>=3&&k%2===1&&j>=0&&j<k);
 const E=6*k,g=E+1,z=E+2;
 const edges=[],charge=[];
 for(let h=0;h<k;h++){
   for(const [a,b] of seed.spec.edges)edges.push([a+4*h,b+4*h]);
   charge.push(1,0,0,0);
 }
 const records=[];
 const lit=(x,h)=>Math.sign(x)*(Math.abs(x)===7?g:Math.abs(x)+6*h);
 for(let h=0;h<k;h++)for(let t=0;t<16;t++){
   const r=sr[t];records.push({kind:'SOURCE',c:norm(r.c.map(x=>lit(x,h))),parents:[],source:r.source+4*h});
 }
 records.push({kind:'SOURCE',c:[g],parents:[],source:-1});
 const offset=records.length;
 const index=i=>i===16?16*k:i<16?16*j+i:offset+(i-17);
 for(const r of rs)records.push({kind:'RES',c:norm(r.c.map(x=>lit(x,j))),parents:r.parents.map(index),pivot:lit(r.pivot,j)});
 return {spec:{h:4*k,edges,charge,guard:g},gate_defs:[[0,z,1,4]],records,
 summary:{source:16*k+1,def_views:0,resolution:28,paid_gates:1,paid_total:29,live_records:records.length}};
}
function bits(x){const a=[];let i=0;while(x){if(x&1n)a.push(i);x>>=1n;i++;}return a;}
function lineage(d){const rows=[],resAnc=[];
 for(let i=0;i<d.records.length;i++){
  const r=d.records[i];
  if(r.kind==='SOURCE'){rows.push(1n<<BigInt(i));resAnc.push(0n);}
  else if(r.kind==='DEF'){rows.push(0n);resAnc.push(0n);}
  else if(r.kind==='RES'){
    const [a,b]=r.parents;
    assert(a<i&&b<i,'forward parent');
    rows.push(rows[a]|rows[b]);
    resAnc.push(resAnc[a]|resAnc[b]|(1n<<BigInt(i)));
  }else throw Error('unknown rule in reference replay');
 }
 return {rows,resAnc};
}
function minimalSupports(k){return Array.from({length:k},(_,j)=>Array.from({length:16},(_,i)=>16*j+i));}
function inUpperClosure(s,k){const S=new Set(s);return minimalSupports(k).some(core=>core.every(i=>S.has(i)));}
function independentSatModels(component,removed){
 const d=build(3,0),cs=d.records.slice(component*16,component*16+16);
 let models=0;for(let a=0;a<64;a++){
  let ok=true;
  for(let i=0;i<16;i++){
   if(i===removed)continue;
   if(!cs[i].c.some(l=>Math.abs(l)===19?false:((l>0)===Boolean((a>>(Math.abs(l)-1-6*component))&1)))){ok=false;break;}
  }
  if(ok)models++;
 }
 return models;
}
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv2-590-'));const cases=[];let checks=0;
function ck(cond,msg){checks++;assert(cond,msg);}
function replay(label,d,want){
 const bytes=Buffer.from(JSON.stringify(d)+'\n'),filename=path.join(tmp,`p${cases.length}.json`);
 fs.writeFileSync(filename,bytes);
 const r=cp.spawnSync(process.execPath,[checker,filename],{encoding:'utf8',timeout:30000,maxBuffer:5e6});
 fs.unlinkSync(filename);if(r.error)throw r.error;
 const accepted=r.status===0;ck(accepted===want,`native mismatch ${label}: ${r.stderr}`);
 const result=accepted?JSON.parse(r.stdout.trim()):null;
 const row={name:label,accepted,bytes:bytes.length,sha256:sha(bytes),paid:d.summary.paid_total,
  checkerAssertions:result?.assertions??null,originalNegativeControls:result?.negativeTests??null,
  nativeError:accepted?null:(r.stderr||'').split('\n').find(x=>x.includes('Error:'))?.slice(0,180)};
 cases.push(row);return row;
}
try{
 const families={};
 for(const k of [3,5]){
  const choices=[];
  for(let j=0;j<k;j++){
   const d=build(k,j),a=lineage(d),last=d.records.length-1,penult=last-1;
   ck(JSON.stringify(d.records[penult].c)===JSON.stringify([-d.spec.guard]),'penultimate signed clause');
   ck(d.records[last].c.length===0,'empty sink');
   const support=bits(a.rows[penult]),sinkSupport=bits(a.rows[last]);
   const expected=minimalSupports(k)[j];
   ck(JSON.stringify(support)===JSON.stringify(expected),'incorrect [-g] provenance');
   ck(JSON.stringify(sinkSupport)===JSON.stringify([...expected,16*k]),'incorrect empty ancestry');
   ck(inUpperClosure(support,k),'provenance missing necessary core');
   const resCount=bits(a.resAnc[penult]).length;
   ck(resCount===27,'noncanonical number of paid RES in [-g] cone');
   const v=replay(`k${k}_choice${j}_W29`,d,true);
   choices.push({selection:j,support,terminalSupport:sinkSupport,resAncestorsToMinusGuard:resCount,
      lastClause:[-d.spec.guard],certificateSHA256:v.sha256,checkerAccepted:true});
  }
  const sup=choices.map(x=>x.support.join(','));ck(new Set(sup).size===k,'provenance alternatives collapsed');
  let intersect=choices[0].support.filter(i=>choices.every(z=>z.support.includes(i)));
  ck(intersect.length===0,'[-g] alternative cores must have empty intersection');
  let union=new Set(choices.flatMap(x=>x.support));ck(union.size===16*k,'all component SOURCEs should occur in OR alternatives');
  families[k]={sourceRecords:16*k+1,minusGuard:[-(6*k+1)],provenanceAntichain:choices,
   antichainSize:k,intersection:intersect,unionSize:union.size,originallyCompulsorySources:16*k+1,
   originalCheckerWork:29};
 }
 const local={all16:independentSatModels(0,-1),singleDeletions:Array.from({length:16},(_,i)=>independentSatModels(0,i))};
 ck(local.all16===0,'original local parity source SAT');ck(local.singleDeletions.every(n=>n>0),'one original clause removable without SAT');
 const abstractHostiles=[
  {name:'guard_only_implies_minus_guard',claimedSupport:[48]},
  {name:'one_component_missing_one_SOURCE',claimedSupport:[...Array(15).keys()]},
  {name:'one_clause_from_every_component',claimedSupport:[0,16,32]},
  {name:'empty_support',claimedSupport:[]}
 ];
 for(const q of abstractHostiles){q.refinedAdmitted=inUpperClosure(q.claimedSupport,3);ck(!q.refinedAdmitted,'spurious source-support admitted');}
 const genuine=[minimalSupports(3)[0],minimalSupports(3)[1],
  [...minimalSupports(3)[0],...minimalSupports(3)[1]],
  [...minimalSupports(3)[2],48]];
 genuine.forEach(s=>ck(inUpperClosure(s,3),'legal stronger support removed'));
 const nativeHostiles=[
  ['forged_penultimate_guard',d=>{d.records[d.records.length-2].c=[d.spec.guard]}],
  ['forged_pivot',d=>{d.records.at(-1).pivot=0}],
  ['cross_component_signed_parent',d=>{d.records[49].parents[0]=16}],
  ['forged_source',d=>{d.records[0].c=[-d.spec.guard]}],
  ['unsupported_AND3',d=>{d.records.at(-1).kind='AND3'}],
  ['underpay',d=>{d.summary.paid_total--}]
 ];
 for(const [name,mut] of nativeHostiles){const d=build(3,0);mut(d);replay(name,d,false);}
 const naiveSingleSupport=families[3].provenanceAntichain[0].support;
 const falselyExcluded=families[3].provenanceAntichain.filter(x=>x.support.join(',')!==naiveSingleSupport.join(',')).map(x=>x.selection);
 ck(falselyExcluded.length===2,'single exact provenance did not lose legal choices');
 const result={schema:'LSPV2-590-EXACT-MINUS-GUARD-PROVENANCE-ANTICHAIN/v1',
  timestamp:'2026-11-12 21:12 PST',status:'PROVED/RESTRICTED exact semantic antichain + COMPUTATIONAL archived original /386 OS',
  checker_sha256:sha(cb),seed_sha256:sha(sb),externalSource_sha256:sha(source),node:process.version,
  family:'k disjoint odd-charge guarded K4 components, k odd >=3',
  theorem:'Every minimal original SOURCE support entailing [-g] is exactly one full 16-clause component. Thus k incomparable alternatives, with empty intersection and union size 16k; each witnessed by original checker accepted W29 certificate with 27 RES ancestors of [-g]. A single exact-support record for clause [-g] loses valid alternatives.',
  alpha_gamma:'On clause [-g], alpha retains antichain of minimal source supports; gamma admits supports containing at least one antichain member. This is semantically exact for this fixed family only; general full-calculus alpha/gamma remains OPEN.',
  families,localSourceDeletionEnumeration:local,spuriousAbstractPaths:abstractHostiles,
  retainedLegalSupersets:genuine,firstSupportOnlyWouldExcludeChoices:falselyExcluded,
  cases,totals:{checks,accepts:cases.filter(x=>x.accepted).length,rejects:cases.filter(x=>!x.accepted).length,
   originalAcceptedAssertions:cases.reduce((s,x)=>s+(x.checkerAssertions||0),0),
   originalBuiltInNegativeControls:cases.reduce((s,x)=>s+(x.originalNegativeControls||0),0)},
  limitations:['Only semantic [-g] SOURCE consequence and the separate archived /386 fragment, NOT full historical R_mix341',
  'A MAY abstraction can conservatively union or forget supports but then loses source-provenance precision; no universal memory lower bound is claimed',
  'The k displayed W29 refutations are not claimed optimal paid-work proofs',
  'Cost count is fixed globally once paid /386 RES and declared gate owners; certificate bytes, construction, span and peak space are independent',
  'No lower bound for unrestricted 3-SAT or P != NP, and no noncircular B3 bridge']};
 fs.writeFileSync(out,JSON.stringify(result,null,2)+'\n');
 console.log(JSON.stringify({pass:true,out,totals:result.totals,antichainSizes:[families[3].antichainSize,families[5].antichainSize],
  nativeVerdicts:cases.map(x=>[x.name,x.accepted])}));
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
