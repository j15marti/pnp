#!/usr/bin/env node
'use strict';
/*
 LSPV-2/541. Original recovered /341 fixture verifier differential corpus.
 It is NOT the complete historical R_mix341 checker.
 Run from j15marti/pnp repository root:
   node experiments/arc/lspv2_541_nonfinite_identity_replayer.cjs results/raw/arc/lspv2_541_local.json
 The original producer and checker files are read without modifying their bodies.
*/
const fs=require('fs'),crypto=require('crypto');
const paths={
 producer:'experiments/arc/lspv2_341_mixed_tseitin_min_dag.js',
 checker:'experiments/arc/lspv2_341_independent_verify.js'};
const pins={
 producer:'4081022e8a3841d79f751a3d3a7a10decbb026da',
 checker:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0'};
function need(p,msg){if(!p)throw Error('LSPV2-541: '+msg);}
function hash(data,algo){return crypto.createHash(algo||'sha256').update(data,'utf8').digest('hex');}
function blob(data){return hash('blob '+Buffer.byteLength(data,'utf8')+'\0'+data,'sha1');}
function originalCheck(checker,packet){
 const stdout=[];
 try {
   new Function('require','process','console',checker)(
     ()=>({readFileSync:()=>packet}),
     {argv:['node','historical-verifier.js','candidate.json']},
     {log:s=>stdout.push(s)});
   need(stdout.length===1,'missing original verifier result');
   return {accepted:true,checks:JSON.parse(stdout[0]).checks};
 }catch(e){return {accepted:false,diagnostic:String(e).slice(0,170)};}
}
function produce(producer){
 const logs=[];
 new Function('console',producer)({log:s=>logs.push(s)});
 need(logs.length===1,'producer output');
 return JSON.parse(logs[0]);
}
function renameIds(packet,a,b,sa,sb){
 need(packet.includes('"'+a+'"')&&packet.includes('"'+b+'"'),'missing ID strings');
 return packet.replaceAll('"'+a+'"',sa).replaceAll('"'+b+'"',sb);
}
function singleId(packet,id,raw){
 need(packet.includes('"'+id+'"'),'missing ID');
 return packet.replaceAll('"'+id+'"',raw);
}
function caseData(id,packet,expected,checker,opts){
 const parsed=JSON.parse(packet),roundtrip=JSON.stringify(parsed);
 const observed=originalCheck(checker,packet);
 const after=originalCheck(checker,roundtrip);
 need(observed.accepted===expected,'original verdict mismatch '+id);
 const record={id,expected,rawBytes:Buffer.byteLength(packet,'utf8'),
   roundtripBytes:Buffer.byteLength(roundtrip,'utf8'),rawCheck:observed,
   roundtripCheck:after,
   parsedProofCount:parsed.fixtures[0].proof.length,
   parsedSourceCount:parsed.fixtures[0].clauses.length};
 if(!opts.skipDigest){record.rawSHA256=hash(packet);record.roundtripSHA256=hash(roundtrip);}
 if(opts.retainBytes || ['PAID_NONFINITE_PAIR','SOURCE_NONFINITE_PAIR','CHARGE_SMALL_EXP'].includes(id)){
   record.rawPacket=packet;
   record.roundtripPacket=roundtrip;
 }
 if(id==='PAID_NONFINITE_PAIR'){
   const pre=parsed.fixtures[0].proof.slice(0,2).map(x=>x.id);
   const post=JSON.parse(roundtrip).fixtures[0].proof.slice(0,2).map(x=>x.id);
   need(pre[0]===Infinity&&pre[1]===-Infinity,'nonfinite paid identities lost');
   need(post[0]===null&&post[1]===null,'paid collision missing');
   need(!after.accepted&&after.diagnostic.includes('fresh inference ID'),'paid roundtrip should fail freshness');
   record.identityBefore=pre.map(String);record.identityAfter=post;
 }else if(id==='SOURCE_NONFINITE_PAIR'){
   const pre=parsed.fixtures[0].clauses.slice(0,2).map(x=>x.id);
   const post=JSON.parse(roundtrip).fixtures[0].clauses.slice(0,2).map(x=>x.id);
   need(pre[0]===Infinity&&pre[1]===-Infinity,'nonfinite source IDs lost');
   need(post[0]===null&&post[1]===null,'source collision missing');
   need(!after.accepted&&after.diagnostic.includes('unique source id'),'source roundtrip should fail freshness');
   record.identityBefore=pre.map(String);record.identityAfter=post;
 }else if(id==='CHARGE_SMALL_EXP'){
   need(after.accepted&&roundtrip.length>packet.length,'monotonic byte-cost falsifier missing');
   need(parsed.fixtures[0].charges[1]===1e-6,'small source charge parsing wrong');
   record.byteExpansion=roundtrip.length-packet.length;
 }else if(id==='CHARGE_NONFINITE'){
   need(parsed.fixtures[0].charges[1]===Infinity,'Infinity charge parse missing');
   need(JSON.parse(roundtrip).fixtures[0].charges[1]===null,'Infinity-null charge change missing');
   need(after.accepted,'charge roundtrip should still pass this fixture');
 }
 return record;
}
function audit(producer,checker,opts={}){
 if(!opts.skipPin){
   need(blob(producer)===pins.producer,'producer blob mismatch');
   need(blob(checker)===pins.checker,'historical verifier blob mismatch');
 }
 const original=produce(producer),all=originalCheck(checker,JSON.stringify(original));
 need(all.accepted&&all.checks===30714,'original seven-fixture control');
 const f=original.fixtures[0],base=JSON.stringify({fixtures:[f],summary:[null]});
 need(originalCheck(checker,base).accepted,'K4 original failed');
 const paid=renameIds(base,'d0','d1','1e400','-1e400');
 const source=renameIds(base,'s0','s1','1e400','-1e400');
 const records=[
   caseData('BASE',base,true,checker,opts),
   caseData('PAID_NONFINITE_PAIR',paid,true,checker,opts),
   caseData('SOURCE_NONFINITE_PAIR',source,true,checker,opts),
   caseData('PAID_FINITE_PAIR',renameIds(base,'d0','d1','100','-100'),true,checker,opts),
   caseData('SOURCE_FINITE_PAIR',renameIds(base,'s0','s1','100','-100'),true,checker,opts),
   caseData('PAID_NONFINITE_SINGLE',singleId(base,'d0','1e400'),true,checker,opts),
   caseData('CHARGE_NONFINITE',base.replace('"charges":[1,0,0,0]','"charges":[1,1e400,0,0]'),true,checker,opts),
   caseData('CHARGE_SMALL_EXP',base.replace('"charges":[1,0,0,0]','"charges":[1,1e-6,0,0]'),true,checker,opts),
   caseData('CHARGE_BAD_ODD',base.replace('"charges":[1,0,0,0]','"charges":[1e400,0,0,0]'),false,checker,opts),
   caseData('DUPLICATED_PAID_INFINITY',renameIds(base,'d0','d1','1e400','1e400'),false,checker,opts),
   caseData('DUPLICATED_PAID_NULL',renameIds(base,'d0','d1','null','null'),false,checker,opts),
   caseData('PAID_DANGLING',base.replace('"id":"d0"','"id":1e400'),false,checker,opts)
 ];
 const malformed=paid.replace('1e400','1e400e0');
 need(!originalCheck(checker,malformed).accepted,'invalid JSON exponent accepted');
 const summaries={
  cases:records.length+1,originalAccepted:records.filter(x=>x.rawCheck.accepted).length,
  originalRejected:records.filter(x=>!x.rawCheck.accepted).length+1,
  acceptedRoundtripRejected:records.filter(x=>x.rawCheck.accepted&&!x.roundtripCheck.accepted).map(x=>x.id),
  malformedJSONRejected:true,allOriginalFixtureChecks:all.checks,
  validK4SourceClauses:f.clauses.length,validK4PaidNodes:f.proof.length};
 need(summaries.acceptedRoundtripRejected.join(',')==='PAID_NONFINITE_PAIR,SOURCE_NONFINITE_PAIR',
  'unexpected acceptance-status roundtrip gap');
 const dimacs='p cnf '+f.graph.edges.length+' '+f.clauses.length+'\n'+
     f.clauses.map(c=>c.literals.join(' ')+' 0').join('\n')+'\n';
 return {id:'LSPV2-541-NONFINITE-ID-ROUNDTRIP',date:'2026-11-10 PST',
  status:'COMPUTATIONAL; recovered historical fixture checker only',
  pins,originalSourceDIMACS:dimacs,
  originalSourceSHA256:opts.skipDigest?null:hash(dimacs),
  assertionCountNote:'Verifier check count includes its internal fixed malformed/negative controls; not a direct execution-time measurement.',
  totals:summaries,records,
  malformed:{id:'INVALID_JSON_EXPONENT',rawPacket:malformed,
    diagnostic:originalCheck(checker,malformed).diagnostic},
  conclusion:'Two distinct non-finite JSON numeric paid IDs or source IDs pass original JS Map freshness checks, but JSON.stringify(JSON.parse(packet)) maps both to null, causing the same original checker to REJECT the reserialized certificate. Canonicalization is not an acceptance-preserving native byte normalization. Source-charge exponent 1e-6 demonstrates byte-cost expansion.',
  limitations:'Original checker is only SOURCE/AND3/XOR fixture verifier, not full historical R_mix341. No externally source-bound full-rule proof or P-vs-NP lower bound is established.'};
}
module.exports={audit,originalCheck,produce,renameIds,pins};
if(require.main===module){
 const producer=fs.readFileSync(paths.producer,'utf8');
 const checker=fs.readFileSync(paths.checker,'utf8');
 const out=JSON.stringify(audit(producer,checker),null,2)+'\n';
 if(process.argv[2])fs.writeFileSync(process.argv[2],out,'utf8');
 else process.stdout.write(out);
}
