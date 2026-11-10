#!/usr/bin/env node
'use strict';
/* LSPV-2/539 executable differential runner. Requires original repo files.
   Executes *unmodified* /341 producer and verifier logic, replacing I/O only.
   The strict auditor is a separate, non-authoritative reference parser. */
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const audit=require('./lspv2_539_strict_fragment_reference.cjs');
const ROOT=path.resolve(__dirname,'../..');
const originProducer='experiments/arc/lspv2_341_mixed_tseitin_min_dag.js';
const originVerifier='experiments/arc/lspv2_341_independent_verify.js';
const satPacket='results/raw/arc/2026-11-10_1224_LSPV3_551_ACCEPTED_SAT_PACKET.json';
const pins={producer:'4081022e8a3841d79f751a3d3a7a10decbb026da',verifier:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',SAT:'706947c767361e7c979b8208677eb983d33838f4'};
function blob(s){return crypto.createHash('sha1').update(Buffer.from('blob '+Buffer.byteLength(s)+'\0'+s)).digest('hex')}
const producer=fs.readFileSync(path.join(ROOT,originProducer),'utf8'),checker=fs.readFileSync(path.join(ROOT,originVerifier),'utf8'),sProof=fs.readFileSync(path.join(ROOT,satPacket),'utf8');
if(blob(producer)!==pins.producer||blob(checker)!==pins.verifier||blob(sProof)!==pins.SAT)throw Error('pinned primary-source drift');
let out=[];new Function('console',producer)({log:x=>out.push(x)});
const data=JSON.parse(out[0]);let checks=0,nativeChecks=0,passed=0,rejected=0;
function check(b,why){checks++;if(!b)throw Error(why)}
function ext(f){return 'p cnf '+f.graph.edges.length+' '+f.clauses.length+'\n'+f.clauses.map(x=>x.literals.join(' ')+' 0').join('\n')+'\n'}
function ref(src,f){return audit.tryAudit(src,JSON.stringify({fixtures:[f],summary:[null]}))}
function native(pkt){
  let log=[];try{new Function('require','process','console',checker)(
    ()=>({readFileSync:()=>JSON.stringify(pkt)}),{argv:['node','original','packet.json']},{log:x=>log.push(x)});
    return {accepted:true,checks:JSON.parse(log[0]).checks};}
  catch(e){return {accepted:false,error:String(e).slice(0,180)}}
}
let packetCounts=[];
for(const f of data.fixtures){
  const r=ref(ext(f),f);check(r.accepted,'original fixture rejected: '+f.graph.name+' '+r.diagnostic);
  check(r.result.paidDistinct===4*f.graph.n-1,'wrong distinct paid');
  passed++;packetCounts.push({graph:f.graph.name,source:crypto.createHash('sha256').update(ext(f)).digest('hex'),paid:r.result.paidDistinct});
}
const base=native(data);check(base.accepted&&base.checks===30714,'original seven-fixture checker regression');nativeChecks+=base.checks;
let p=JSON.parse(sProof),sf=p.fixtures[1];
let origSat=native(p);check(origSat.accepted&&origSat.checks===2273,'pinned SAT-source counterexample did not replay');
nativeChecks+=origSat.checks;
const satRef=ref(ext(sf),sf);check(!satRef.accepted,'reference falsely accepts SAT source');rejected++;
const witness='101001000000100000'.split('').map(Number);
check(sf.clauses.every(x=>x.literals.some(l=>witness[Math.abs(l)-1]===(l>0?1:0))),'SAT source witness invalid');
let k4=data.fixtures[0],copy=x=>JSON.parse(JSON.stringify(x));
let c=copy(k4);c.proof[0].support='012';check(!ref(ext(c),c).accepted,'type coercion accepted');rejected++;
c=copy(k4);c.clauses[0].literals[0]=String(c.clauses[0].literals[0]);check(!ref(ext(c),c).accepted,'source string accepted');rejected++;
c=copy(k4);c.proof.at(-1).row.mask='0x100000';check(!ref(ext(c),c).accepted,'ghost index accepted');rejected++;
c=copy(k4);c.proof[0].table^=1;check(!ref(ext(c),c).accepted,'false AND3 accepted');rejected++;
c=copy(k4);c.proof[0].rule='RES';check(!ref(ext(c),c).accepted,'unauthenticated native RES wrongly admitted');rejected++;
c=copy(k4);c.proof.at(-1).row.rhs=0;check(!ref(ext(c),c).accepted,'wrong sink admitted');rejected++;
let altered=ext(k4).replace('1 2 3 0','-1 2 3 0');
check(!ref(altered,k4).accepted,'different authenticated source accepted');rejected++;
c=copy(k4);let extra=copy(c.proof[0]);extra.id='extra';c.proof.splice(1,0,extra);
let pr=ref(ext(c),c);check(pr.accepted&&pr.result.paidDistinct===16,'valid distinct paid node excluded from reference');passed++;
let nr=native({fixtures:[c],summary:[null]});check(!nr.accepted&&nr.error.includes('proof candidate length'),'native length guard not observed');rejected++;
const raw={id:'LSPV2-539-SOURCE-BOUND-STRICT-REFERENCE',status:'COMPUTATIONAL / separate sound semantic fragment',checkedOriginalBlobs:pins,source:'original project files, original signed CNF and legacy fixture',nativeSeven:base,nativeSAT:origSat,referenceOriginalPass:7,referenceRejectedSAT:1,strictAccepted:passed,strictRejectedControls:rejected,assertions:checks,nativeAssertionGroups:nativeChecks,originalPackets:packetCounts,validPadding:{strictReference:true,originalNative:false},boundaries:'NOT full R_mix341; neither RES/DEF/LOCAL/branch authenticated, no all-rule proof minimum or RAM cost',open:['P2-D1','P2-C3','P2-B1','P2-B2']};
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(raw,null,2)+'\n');
console.log(JSON.stringify(raw,null,2));
