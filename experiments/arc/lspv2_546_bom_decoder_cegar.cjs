#!/usr/bin/env node
'use strict';
// LSPV-2/546: pinned recovered /341 fixture checker BOM/UTF-8 CEGAR differential.
// This file is NOT an authoritative full R_mix341 checker.
// Execute from a checkout: node experiments/arc/lspv2_546_bom_decoder_cegar.cjs [out.json]
const fs=require('node:fs'),cp=require('node:child_process'),os=require('node:os'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const pinned=[
 ['experiments/arc/lspv2_341_mixed_tseitin_min_dag.js','4081022e8a3841d79f751a3d3a7a10decbb026da'],
 ['experiments/arc/lspv2_341_independent_verify.js','fcb7d4ced8f922de14c0bda16263a8cc7853e8e0']
];
function blobSHA(b){return crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\\0')).update(b).digest('hex')}
function digest(b){return crypto.createHash('sha256').update(b).digest('hex')}
for(const [file,sha] of pinned)assert.equal(blobSHA(fs.readFileSync(path.join(root,file))),sha,'PIN DRIFT '+file);
function replaceAllBuffer(b,needle,repl,first=false){
 const parts=[];let i=0,cnt=0;
 for(;;){let p=b.indexOf(needle,i);if(p<0)break;
  parts.push(b.subarray(i,p),repl);cnt++;i=p+needle.length;
  if(first)break;
 }parts.push(b.subarray(i));
 assert(cnt>0,'missing replacement target');return {bytes:Buffer.concat(parts),count:cnt};
}
function readJsonOutput(p,args=[]){
 const r=cp.spawnSync(process.execPath,[p,...args],{encoding:'utf8',timeout:25000,maxBuffer:32*1024*1024});
 assert.equal(r.status,0,r.stderr);return JSON.parse(r.stdout);
}
const original=readJsonOutput(path.join(root,pinned[0][0]));
const fixture=original.fixtures.find(f=>f.graph.name==='K4');
const summary=original.summary.find(s=>s.name==='K4');
assert.equal(fixture.clauses.length,16);assert.equal(fixture.proof.length,15);
let nmodels=0;
for(let bits=0;bits<64;bits++)
 if(fixture.clauses.every(c=>c.literals.some(l=>l>0 ? Boolean(bits&(1<<(l-1))):!Boolean(bits&(1<<(-l-1))))))nmodels++;
assert.equal(nmodels,0);
const baseline=Buffer.from(JSON.stringify({fixtures:[fixture],summary:[summary]}),'utf8');
const bom=Buffer.from([0xef,0xbb,0xbf]),zws=Buffer.from('\u200b','utf8');
const inside=replaceAllBuffer(baseline,Buffer.from('"name":"K4"'),Buffer.from('"name":"\ufeffK4"'));
const escaped=replaceAllBuffer(baseline,Buffer.from('"name":"K4"'),Buffer.from('"name":"\\uFEFFK4"'));
const idAll=replaceAllBuffer(baseline,Buffer.from('"s0"'),Buffer.from('"\ufeffs0"'));
assert.equal(idAll.count,3);
const idOnce=replaceAllBuffer(baseline,Buffer.from('"s0"'),Buffer.from('"\ufeffs0"'),true);
const invalid=replaceAllBuffer(baseline,Buffer.from('"s0"'),Buffer.from([34,0x80,34]));
assert.equal(invalid.count,3);
const packets=[
 ['baseline',baseline,true],
 ['leading_bom',Buffer.concat([bom,baseline]),false],
 ['leading_bom_after_whitespace',Buffer.concat([Buffer.from(' \\n'),bom,baseline]),false],
 ['double_leading_bom',Buffer.concat([bom,bom,baseline]),false],
 ['trailing_bom',Buffer.concat([baseline,bom]),false],
 ['leading_zwsp',Buffer.concat([zws,baseline]),false],
 ['legal_whitespace',Buffer.concat([Buffer.from(' \\n'),baseline]),true],
 ['graph_name_literal_bom',inside.bytes,true],
 ['graph_name_escaped_bom',escaped.bytes,true],
 ['source_id_all_bom',idAll.bytes,true],
 ['source_id_only_one_bom',idOnce.bytes,false],
 ['invalid_utf8_source_id_all',invalid.bytes,true]
];
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-546-'));
const checker=path.join(root,pinned[1][0]);
function invoke(bytes,name){
 const filename=path.join(dir,name+'.json');
 fs.writeFileSync(filename,bytes);
 const r=cp.spawnSync(process.execPath,[checker,filename],{encoding:'utf8',timeout:25000,maxBuffer:32*1024*1024});
 let result=null;try{result=JSON.parse(r.stdout)}catch{}
 return {accepted:r.status===0&&!!result,checks:result?.checks??null,
  error:r.status===0?'':r.stderr.slice(0,175)};
}
const cases=[];let checkCount=0;
try{
 for(const [name,bytes,expected] of packets){
  const native=invoke(bytes,name+'-native');
  assert.equal(native.accepted,expected,name+' native: '+native.error);
  if(native.accepted){assert.equal(native.checks,1401);checkCount+=native.checks;}
  const defaultDecoded=new TextDecoder('utf-8').decode(bytes);
  const defaultNormalized=Buffer.from(defaultDecoded,'utf8');
  const normalized=invoke(defaultNormalized,name+'-td');
  const preservesBOM=new TextDecoder('utf-8',{ignoreBOM:true}).decode(bytes);
  assert.equal(preservesBOM,bytes.toString('utf8'),'replacement-mode decode mismatch '+name);
  const exactDecoded=invoke(Buffer.from(preservesBOM,'utf8'),name+'-node-decoded');
  assert.equal(exactDecoded.accepted,native.accepted,'Node-compatible replacement-mode mismatch '+name);
  let fatalSuccess=true;
  try{new TextDecoder('utf-8',{fatal:true,ignoreBOM:true}).decode(bytes)}catch{fatalSuccess=false}
  cases.push({name,expected,native:native.accepted,nativeChecks:native.checks,
   byteLength:bytes.length,sha256:digest(bytes),byteHex:bytes.toString('hex'),
   defaultTextDecoderEquivalent:defaultNormalized.equals(bytes),
   defaultDecoderThenCheckerAccepts:normalized.accepted,
   nodeReplacementThenCheckerAccepts:exactDecoded.accepted,
   fatalUtf8Succeeds:fatalSuccess,leadingBOM:bytes.subarray(0,3).equals(bom),
   nativeDiagnostic:native.error.slice(0,120)});
 }
}finally{fs.rmSync(dir,{recursive:true,force:true})}
const led={
 id:'LSPV-2/546',date:'2026-11-10 19:12 PST',
 scope:'Only recovered original /341 SOURCE/AND3/XOR fixture checker. Not full R_mix341.',
 pinned,host:process.version,zeroOf64SatisfyingAssignments:nmodels,
 originalSignedK4:{variables:6,clauses:16,paid:15},
 cases,nativeAcceptanceCount:cases.filter(x=>x.native).length,
 nativeRejectionCount:cases.filter(x=>!x.native).length,
 nativeAssertionGroups:checkCount,
 spuriousPath:cases.find(x=>x.name==='leading_bom').defaultDecoderThenCheckerAccepts,
 realInvalidUTF8Path:cases.find(x=>x.name==='invalid_utf8_source_id_all').native,
 conclusion:'Native fs UTF8 read retains initial U+FEFF; default TextDecoder strips it, causing a spurious accepted proof. Fatal UTF8 excludes actual accepted invalid-source bytes. Node-compatible replacement decode+prefix ownership avoids both tested errors.',
 status:'COMPUTATIONAL; P2-D1 P2-C3 P2-B1 B3 and P versus NP OPEN'
};
assert.equal(led.nativeAcceptanceCount,6);assert.equal(led.nativeRejectionCount,6);
assert(led.spuriousPath&&led.realInvalidUTF8Path);
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(led,null,2)+'\n');
console.log(JSON.stringify({...led,cases:led.cases.map(({byteHex,...rest})=>rest)},null,2));
