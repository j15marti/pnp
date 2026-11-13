#!/usr/bin/env node
'use strict';
// LSPV-3/608 pinned recovered-original-checker audit (NOT full R_mix341).
// Mathematical checker source is unmodified. Hosted I/O and 386 digest-display stub only.
const files={
 c341:'experiments/arc/lspv2_341_independent_verify.js',
 c386:'experiments/arc/lspv2_386_independent_verify.js',
 original341:'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json',
 sat341:'results/raw/arc/2026-11-12_2219_LSPV3_606_X10_NATIVE341_ACCEPTED.json',
 facet386:'results/raw/arc/2026-11-11_0407_LSPV2_555_ACCEPTED_LIVE_DEF_RES_K1.json',
 res386:'results/raw/arc/574_k03_W29.json',
 external386:'results/raw/arc/574_k03_SIGNED_SOURCE.cnf'
};
const pins={
 c341:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
 c386:'338305c0ce101704205e57543756b8127074a986',
 original341:'fe27fe1011d0021e721ccaeb747ed58da65d7464',
 sat341:'1e19a9d2b84daa1fc8c29468873ad62e0d67e105',
 facet386:'aeeb555c4dcf7f510a9a501c8afc609b629a9298',
 res386:'22c18da85aaf28948796d5cc08944f4edac49668',
 external386:'5cb446fd490be5f8e86aeda879f537c0fd67dcab'
};
const tags=['SOURCE','RES','Resolution','DEF','AND3','XOR','GF(2)',
 'GF2','LOCAL-CONVERT','LOCAL_CONVERT','CASE','BRANCH','WEAKEN',
 'DISCHARGE','RECONVERGE','JOIN','DELETE','LEARN','EXPORT','PRIVATE'];
const clone=x=>JSON.parse(JSON.stringify(x));
function check(b,m){if(!b)throw Error(m)}
function runOriginal(js,data,is386){
 let output;
 try{
  const req=k=>{
   if(k==='fs')return {readFileSync:()=>JSON.stringify(data)};
   if(k==='assert')return (b,m)=>check(b,m);
   if(k==='crypto')return {createHash:()=>({update:()=>({digest:()=>'NOT_A_REAL_SHA256'})})};
   throw Error('unexpected module '+k)
  };
  new Function('require','process','console','structuredClone',js)(
    req,{argv:['node','original','packet.json']},{log:x=>output=x},clone);
  let v=JSON.parse(output);
  if(is386){check(v.sha256==='NOT_A_REAL_SHA256','printed digest');delete v.sha256;delete v.file}
  return {accept:true,info:is386?v:{checks:v.checks,
    cases:v.cases.map(x=>({name:x.name,paid:x.proofNodes,essential:x.essential}))}}
 }catch(e){return {accept:false,error:String(e)}}
}
function bindSource(s,p){
 const t=s.trim().split(/\s+/),n=+t[2],m=+t[3],cls=[];let c=[];
 check(t[0]==='p'&&t[1]==='cnf','external source header');
 for(const token of t.slice(4)){const v=+token;check(Number.isSafeInteger(v),'external literal');
   if(v===0){cls.push(c);c=[]}else{check(Math.abs(v)<=n,'literal range');c.push(v)}}
 check(c.length===0&&cls.length===m,'external clause count');
 const norm=c=>c.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(',');
 const key=x=>x.map(norm).sort().join('|');
 check(key(cls)===key(p.records.filter(x=>x.kind==='SOURCE').map(x=>x.c)),'source multiset');
 return {variables:n,clauses:m,exactExternalSignedMultiset:true,
   originalVerifierLoadsExternalFile:false}
}
function audit(inp){
 for(const k of Object.keys(files))check(typeof inp[k]==='string','missing '+k);
 const c341=inp.c341,c386=inp.c386,
  orig=JSON.parse(inp.original341),sat=JSON.parse(inp.sat341),
  live=JSON.parse(inp.facet386),other=JSON.parse(inp.res386);
 check(c341.includes('p.rule==="AND3"')&&c341.includes('p.rule==="XOR"')
   &&c341.includes('unknown rule'),'341 dispatcher changed');
 check(c386.includes("['SOURCE','DEF','RES'].includes(r.kind)"),'386 dispatcher changed');
 const k4={fixtures:[orig.fixtures[0]],summary:[orig.summary[0]]},
  positives=[],negatives=[];
 function go(label,engine,packet,expected){
  const result=runOriginal(engine==='341'?c341:c386,packet,engine==='386');
  check(result.accept===expected,'verdict mismatch: '+label+' '+JSON.stringify(result));
  (expected?positives:negatives).push({label,engine,...result})
 }
 go('all-seven-341-fixtures','341',orig,true);
 orig.fixtures.forEach((f,i)=>go('341-'+f.graph.name,'341',
   {fixtures:[f],summary:[orig.summary[i]]},true));
 go('341-known-accepted-SAT-source','341',sat,true);
 go('386-live-facets-RES','386',live,true);
 go('386-externally-compared-source','386',other,true);
 for(const tag of tags){
  if(tag!=='AND3'){const p=clone(k4);p.fixtures[0].proof[0].rule=tag;go('341-AND3-as-'+tag,'341',p,false)}
  if(tag!=='XOR'){const p=clone(k4);p.fixtures[0].proof.find(x=>x.rule==='XOR').rule=tag;go('341-XOR-as-'+tag,'341',p,false)}
  if(tag!=='RES'){const p=clone(live);p.records.find(x=>x.kind==='RES').kind=tag;go('386-RES-as-'+tag,'386',p,false)}
  if(tag!=='DEF'){const p=clone(live);p.records[0].kind=tag;go('386-DEF-as-'+tag,'386',p,false)}
 }
 for(const [label,value] of [['null',null],['numeric',0],['object',{}],['array',[]]]){
  let p=clone(k4);p.fixtures[0].proof[0].rule=value;go('341-tag-'+label,'341',p,false);
  p=clone(live);p.records.find(x=>x.kind==='RES').kind=value;go('386-tag-'+label,'386',p,false)
 }
 const hostile=[
  ['341-source','341',()=>{let p=clone(k4);p.fixtures[0].clauses[0].literals[0]=999;return p}],
  ['341-parent','341',()=>{let p=clone(k4);p.fixtures[0].proof[0].parents[0]='fake';return p}],
  ['341-sink','341',()=>{let p=clone(k4);p.fixtures[0].proof.at(-1).row.rhs=0;return p}],
  ['341-SAT-correct-charge','341',()=>{let p=clone(sat);p.fixtures[0].charges[5]=0;return p}],
  ['341-SAT-correct-support','341',()=>{let p=clone(sat);p.fixtures[0].proof[17].support=[0,1,10];return p}],
  ['386-facet','386',()=>{let p=clone(live);p.records[0].c=[-8];return p}],
  ['386-owner','386',()=>{let p=clone(live);p.gate_defs[1][0]=0;return p}],
  ['386-paid-total','386',()=>{let p=clone(live);p.summary.paid_total--;return p}],
  ['386-parent','386',()=>{let p=clone(live);p.records.at(-1).parents[0]=10000;return p}],
  ['386-source','386',()=>{let p=clone(live);p.records.find(x=>x.kind==='SOURCE').c=[-7];return p}]
 ];
 for(const [label,engine,mut] of hostile)go(label,engine,mut(),false);
 const external=bindSource(inp.external386,other),f=sat.fixtures[0],
    witness='000000010010000001';
 check(f.graph.edges.length===witness.length&&f.clauses.every(c=>
    c.literals.some(l=>witness[Math.abs(l)-1]===(l>0?'1':'0'))),'SAT witness');
 const nSource=orig.fixtures.reduce((a,f)=>a+f.clauses.length,0),
       nPaid=orig.fixtures.reduce((a,f)=>a+f.proof.length,0);
 check(nSource===328&&nPaid===321,'341 cost inventory');
 check(live.summary.def_views===4&&live.summary.paid_gates===3&&
    live.summary.paid_total===live.summary.paid_gates+live.summary.resolution,
    '386 paid-once count');
 return {run:'LSPV-3/608',status:'PASS',
  authority:'TWO_DISTINCT_ORIGINAL_RECOVERED_DISPATCHERS',
  execution:'UNCHANGED ORIGINAL MATHEMATICAL CHECKERS IN HOSTED V8, WITH IO/DISPLAY ADAPTER',
  checkerOSProcessExecuted:false,pins,files,
  341:{originalSourceOccurrences:nSource,originalPaidNodes:nPaid,
    acceptedOpcodeNames:['AND3','XOR'],externalSourceAuthenticated:false},
  386:{acceptedRecordKinds:['SOURCE','DEF','RES'],liveFacetRecords:4,
    distinctPaidOwners:3,paidResolution:live.summary.resolution,
    paidTotal:live.summary.paid_total,external},
  knownAcceptedSATSource:{clauses:48,satisfyingAssignment:witness,
    acceptedByChecker:true,mathematicallyValidUNSATProof:false},
  positiveCount:positives.length,negativeCount:negatives.length,
  positives,negatives,allHostilesRejected:true,
  P2_D1:'OPEN',P2_C3:'OPEN',P2_B1:'OPEN',P2_B2:'OPEN',P2_B3:'OPEN',
  P_versus_NP:'OPEN',
  limitation:'No original unified R_mix341 mixed-rule checker; absent operations unknown in full historical grammar, not deemed illegal.'};
}
if(typeof module!=='undefined')module.exports={audit,files,pins};
if(typeof require!=='undefined'&&typeof module!=='undefined'&&require.main===module){
 const fs=require('fs'),path=require('path'),crypto=require('crypto'),
  root=path.resolve(__dirname,'../..'),inp={};
 for(const [k,p] of Object.entries(files)){
  const b=fs.readFileSync(path.join(root,p));
  const sha=crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');
  check(sha===pins[k],'Git blob mismatch: '+p);inp[k]=b.toString('utf8')
 }
 const output=JSON.stringify(audit(inp),null,2)+'\n';
 if(process.argv[2])fs.writeFileSync(process.argv[2],output);
 process.stdout.write(output);
}
