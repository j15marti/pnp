#!/usr/bin/env node
'use strict';
// LSPV-5/499: exact-CLI accepted-byte audit for SOURCE-coordinate JSON lexemes.
const fs=require('node:fs');
const path=require('node:path');
const os=require('node:os');
const cp=require('node:child_process');
const crypto=require('node:crypto');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const checkerPath=path.join(root,'experiments/arc/lspv2_386_independent_verify.js');
const basePath=path.join(root,'results/raw/arc/2026-11-11_1734_LSPV4_554_W29_SOURCE_QUOTIENT_ACCEPTED.json');
const witnessPath=path.join(root,'results/raw/review/2026-11-11_1748_LSPV5_499_SOURCE_COORDINATE_LEXEME_ACCEPTED.json');
const rawPath=path.join(root,'results/raw/review/2026-11-11_1748_LSPV5_499_SOURCE_COORDINATE_LEXEME_RAW.json');
const gitBlob=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
const sha256=b=>crypto.createHash('sha256').update(b).digest('hex');
const checker=fs.readFileSync(checkerPath);
const base=fs.readFileSync(basePath);
assert.equal(gitBlob(checker),'338305c0ce101704205e57543756b8127074a986','checker drift');
assert.equal(gitBlob(base),'035d681e2d18e8b12191b984d59bcf870d3915d0','packet drift');
const baseText=base.toString('utf8');
const baseObj=JSON.parse(baseText);
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv5-499-'));
function run(name,text){
  const file=path.join(tmp,name+'.json');
  fs.writeFileSync(file,text);
  const x=cp.spawnSync(process.execPath,[checkerPath,file],{encoding:'utf8',timeout:25000,maxBuffer:2e6});
  let parsed=null;try{parsed=JSON.parse((x.stdout||'').trim())}catch(_e){}
  return {name,accept:x.status===0&&!!parsed,status:x.status,signal:x.signal,bytes:Buffer.byteLength(text),
    sha256:sha256(Buffer.from(text)),paid:parsed?.paid??null,records:parsed?.records??null,sources:parsed?.sources??null,
    negativeTests:parsed?.negativeTests??null,assertions:parsed?.assertions??null,
    stderr:(x.stderr||'').trim().slice(0,300)};
}
const sourcePattern=/"source":(-?\d+)/g;
const occurrences=[...baseText.matchAll(sourcePattern)];
assert.equal(occurrences.length,50,'expected 49 SOURCE coordinates plus summary source count');
const aliases=new Map([
  [0,'-0'],[1,'1.0'],[2,'2e0'],[3,'3.000'],[4,'4E+0'],[5,'5e00'],
  [6,'6.000e+000'],[7,'7E000'],[8,'8.0e0'],[9,'9.0000'],[10,'1e1'],[11,'11.00']
]);
let changed=0,seenCoordinate=0;
const aliasText=baseText.replace(sourcePattern,(m,d)=>{
  if(seenCoordinate++>=49)return m;
  const n=Number(d);
  if(n<0)return m;
  const lex=aliases.get(n);
  assert.ok(lex!==undefined,'missing alias '+n);
  assert.ok(Number(lex)===n,'alias value drift');
  changed++;
  return '"source":'+lex;
});
assert.equal(changed,48,'expected 48 non-guard source coordinates');
const aliasObj=JSON.parse(aliasText);
assert.equal(JSON.stringify(aliasObj),JSON.stringify(baseObj),'semantic parsed object changed');
assert.notEqual(aliasText,baseText,'raw bytes did not change');
const results=[];
results.push(run('baseline',baseText));
results.push(run('all_coordinate_aliases',aliasText));
assert.equal(results[0].accept,true);
assert.equal(results[1].accept,true);
assert.equal(results[0].paid,29);
assert.equal(results[1].paid,29);
for(const [name,lex] of [['zero_fraction','0.0'],['zero_exponent','0e0'],['zero_positive_exponent','0E+999999'],['negative_zero','-0']]){
  const t=baseText.replace('"source":0','"source":'+lex);
  const p=JSON.parse(t);assert.ok(p.records[0].source===0);
  const r=run(name,t);assert.equal(r.accept,true,name);results.push(r);
}
const controls=[
  ['string_coordinate',baseText.replace('"source":0','"source":"0"')],
  ['fractional_coordinate',baseText.replace('"source":0','"source":0.5')],
  ['out_of_range_coordinate',baseText.replace('"source":0','"source":12')],
  ['leading_zero_malformed',baseText.replace('"source":0','"source":00')],
  ['incomplete_exponent',baseText.replace('"source":0','"source":0e')],
  ['forged_source_clause',baseText.replace('"c":[1,2,3,-19]','"c":[-1,2,3,-19]')]
];
for(const [name,text] of controls){const r=run(name,text);assert.equal(r.accept,false,name);results.push(r)}
fs.mkdirSync(path.dirname(witnessPath),{recursive:true});
fs.writeFileSync(witnessPath,aliasText);
const raw={
  id:'LSPV-5/499',timestamp:'2026-11-11 17:48 PST',status:'PROVED/RESTRICTED + COMPUTATIONAL',
  checker:{path:path.relative(root,checkerPath),git_blob:gitBlob(checker),sha256:sha256(checker)},
  baseline:{path:path.relative(root,basePath),git_blob:gitBlob(base),sha256:sha256(base),bytes:base.length},
  acceptedWitness:{path:path.relative(root,witnessPath),sha256:sha256(Buffer.from(aliasText)),bytes:Buffer.byteLength(aliasText),
    parsedObjectCanonicalEquality:true,mutatedSourceCoordinateOccurrences:changed,distinctCoordinateValues:[...aliases.keys()]},
  results,
  summary:{accepted:results.filter(x=>x.accept).length,rejected:results.filter(x=>!x.accept).length,
    baselinePaid:results[0].paid,aliasPaid:results[1].paid,sourceCoordinates:49,
    claim:'The unchanged archived /386 CLI accepts noncanonical RFC-8259 numeric lexemes in authenticated SOURCE coordinate fields after JSON.parse collapses them to the same ECMAScript Number.',
    scope:'Accepted-byte syntax and source-coordinate identity only; no all-rule authentication, minimum cost, memory lower bound, or P!=NP conclusion.'}
};
fs.writeFileSync(rawPath,JSON.stringify(raw,null,2)+'\n');
console.log(JSON.stringify({raw:path.relative(root,rawPath),witness:path.relative(root,witnessPath),...raw.summary,
  rawSha256:sha256(fs.readFileSync(rawPath)),witnessSha256:sha256(fs.readFileSync(witnessPath))},null,2));
fs.rmSync(tmp,{recursive:true,force:true});
