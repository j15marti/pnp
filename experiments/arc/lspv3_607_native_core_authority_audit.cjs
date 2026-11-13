#!/usr/bin/env node
'use strict';
// LSPV-3/607 native-core authority audit.
// Run from j15marti/pnp repository root:
//   node experiments/arc/lspv3_607_native_core_authority_audit.cjs
// Optional output: node .../lspv3_607_native_core_authority_audit.cjs --out /tmp/607.json
// This invokes the two ORIGINAL recovered checker programs unchanged in Node OS.
// It does NOT authenticate or invent a combined historical R_mix341 dispatcher.
const fs=require('fs'),path=require('path'),os=require('os'),crypto=require('crypto');
const cp=require('child_process');
const ROOT=process.cwd();
const specs=[
 {label:'native341',checker:'experiments/arc/lspv2_341_independent_verify.js',
  checkerBlob:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
  cert:'results/raw/arc/2026-11-12_2219_LSPV3_606_X10_NATIVE341_ACCEPTED.json',
  certBlob:'1e19a9d2b84daa1fc8c29468873ad62e0d67e105'},
 {label:'native386',checker:'experiments/arc/lspv2_386_independent_verify.js',
  checkerBlob:'338305c0ce101704205e57543756b8127074a986',
  cert:'results/raw/arc/574_k03_W29.json',
  certBlob:'22c18da85aaf28948796d5cc08944f4edac49668'}];
const source='results/raw/arc/574_k03_SIGNED_SOURCE.cnf';
const sourceBlob='5cb446fd490be5f8e86aeda879f537c0fd67dcab';
function insist(b,m){if(!b)throw Error(m)}
function gitHash(b){return crypto.createHash('sha1')
  .update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex')}
function readPinned(p,sha){const b=fs.readFileSync(path.join(ROOT,p));
  insist(gitHash(b)===sha,'original git blob mismatch: '+p);
  return b}
function runOriginal(checker,file){let proc=cp.spawnSync(process.execPath,
  [path.join(ROOT,checker),file],{encoding:'utf8',timeout:30000,maxBuffer:8*1024*1024});
  return {accepted:proc.status===0&&!proc.error,exit:proc.status,
    stdout:proc.stdout,stderr:proc.stderr,error:proc.error&&String(proc.error)}}
function norm(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(',')}
function countSat(original){let f=original.fixtures[0],E=f.graph.edges.length;
  insist(E===18,'wrong externally audited SAT-source size');
  let models=0,violated=0;
  let bad=f.proof.find(p=>p.id==='d17');
  insist(bad&&bad.row&&BigInt(bad.row.mask)===0x403n,'missing d17');
  for(let a=0;a<2**E;a++){
    let valid=f.clauses.every(c=>c.literals.some(l=>{
      let z=((a>>(Math.abs(l)-1))&1);return l>0?z===1:z===0;}));
    if(!valid)continue;
    models++;
    let lhs=0;for(let e=0;e<E;e++)if((BigInt(bad.row.mask)>>BigInt(e))&1n)lhs^=(a>>e)&1;
    violated+=Number(lhs!==bad.row.rhs);
  }
  return {sourceModels:models,falseAffineModels:violated}}
function compareSource(cnf,packet){const lines=cnf.toString('utf8').trim().split(/\r?\n/);
  let header=lines[0].trim().split(/\s+/);
  insist(header[0]==='p'&&header[1]==='cnf','bad external source header');
  let cls=lines.slice(1).filter(Boolean).map(line=>{
    let a=line.trim().split(/\s+/).map(Number);
    insist(a.at(-1)===0,'bad external source terminator');
    return a.slice(0,-1)});
  let recs=packet.records.filter(x=>x.kind==='SOURCE');
  insist(cls.length===Number(header[3])&&cls.length===recs.length,'external source clause count');
  insist(cls.map(norm).sort().join('|')===recs.map(x=>norm(x.c)).sort().join('|'),
    'external source differs from checker SOURCE records');
  return {variables:Number(header[2]),clauses:cls.length,exactSignedSourceMultiset:true}}
function main(){
 const b341=readPinned(specs[0].checker,specs[0].checkerBlob).toString('utf8');
 const b386=readPinned(specs[1].checker,specs[1].checkerBlob).toString('utf8');
 insist(b341.includes('p.rule==="AND3"')&&b341.includes('p.rule==="XOR"')
   &&b341.includes('unknown rule'),'341 dispatcher changed');
 insist(b386.includes("['SOURCE','DEF','RES'].includes(r.kind)")&&
   !b386.includes('r.kind==="AND3"'),'386 dispatcher changed');
 const cnf=readPinned(source,sourceBlob);
 const docs=specs.map(s=>JSON.parse(readPinned(s.cert,s.certBlob).toString('utf8')));
 const external=compareSource(cnf,docs[1]);
 const sat=countSat(docs[0]);
 insist(sat.sourceModels===64&&sat.falseAffineModels===64,'SAT-source regression mismatch');
 const pristine=specs.map(s=>runOriginal(s.checker,path.join(ROOT,s.cert)));
 pristine.forEach((x,i)=>insist(x.accepted,'ORIGINAL '+specs[i].label+' rejected: '+x.stderr));
 let cases=[];
 const work=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-607-'));
 try{
   let bad341=structuredClone(docs[0]);bad341.fixtures[0].proof[0].rule='RES';
   let bad386=structuredClone(docs[1]);
   let first=bad386.records.findIndex(r=>r.kind==='RES');
   insist(first>=0,'386 RES not found');bad386.records[first].kind='AND3';
   for(const [lab,spec,bad] of [['341-RES-forgery',specs[0],bad341],
       ['386-AND3-forgery',specs[1],bad386]]){
     let f=path.join(work,lab+'.json');fs.writeFileSync(f,JSON.stringify(bad));
     let x=runOriginal(spec.checker,f);
     insist(!x.accepted,'forged cross-rule accepted by '+spec.label);
     cases.push({label:lab,accepted:false,stderr:x.stderr.trim().slice(0,600)});
   }
 } finally {fs.rmSync(work,{recursive:true,force:true})}
 const output={status:'PASS',authority:'TWO_SEPARATE_UNCHANGED_CHECKERS',
  noHistoricalUnifiedDispatcherAuthenticated:true,
  originalCheckers:specs.map((s,i)=>({checker:s.checker,checkerGitBlob:s.checkerBlob,
    certificate:s.cert,certificateGitBlob:s.certBlob,accepted:pristine[i].accepted,
    originalCheckerOutput:pristine[i].stdout.trim().slice(0,4000)})),
  external386:{file:source,gitBlob:sourceBlob,...external},
  recovered341SatCounterexample:sat,hostileCrossRuleControls:cases,
  acceptedNativePaidRuleSets:{native341:['AND3','XOR'],native386:['RES']},
  acceptedNativeRecordTypes:{native341:['SOURCE-via-clauses','AND3','XOR'],
    native386:['SOURCE','DEF-free-facet','RES','gate_defs-paid-owner']},
  fullRmix341:'OPEN',P2_D1:'OPEN',P2_C3:'OPEN',P2_B1:'OPEN',P2_B2_B3:'OPEN',
  knownExcludedFromAuthority:['LOCAL-CONVERT','CASE','WEAKEN','DISCHARGE','JOIN',
  'EXPORT','PRIVATE-WIRE-PORT','unified-RES-to-AND3','unified-DEF-facet-to-LOCAL-CONVERT']};
 const s=JSON.stringify(output,null,2)+'\n';
 if(process.argv[2]==='--out'){insist(Boolean(process.argv[3]),'--out requires path');
   fs.writeFileSync(process.argv[3],s)}
 process.stdout.write(s);
}
main();
