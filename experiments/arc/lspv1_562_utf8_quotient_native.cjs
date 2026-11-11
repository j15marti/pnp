#!/usr/bin/env node
'use strict';
/*
 LSPV-1/562. Execute in an ORIGINAL j15marti/pnp checkout using Node >= 18.
 Explicitly validates pinned Git blobs, launches the ORIGINAL producer and
 ORIGINAL recovered /341 fixture checker as unmodified OS Node subprocesses.
 This program is NEW and is not itself an authoritative R_mix341 full checker.
 Usage: node experiments/arc/lspv1_562_utf8_quotient_native.cjs [output.json]
 No dependencies beyond Node core.
*/
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const assert=require('node:assert/strict'),crypto=require('node:crypto');
const {spawnSync}=require('node:child_process');
const {TextDecoder}=require('node:util');
const root=path.resolve(__dirname,'../..');
const producer=path.join(root,'experiments/arc/lspv2_341_mixed_tseitin_min_dag.js');
const checker=path.join(root,'experiments/arc/lspv2_341_independent_verify.js');
const pinned={
 producer:'4081022e8a3841d79f751a3d3a7a10decbb026da',
 checker:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0'
};
function gitBlobSha(data){
 const b=Buffer.isBuffer(data)?data:Buffer.from(data);
 return crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
}
assert.equal(gitBlobSha(fs.readFileSync(producer)),pinned.producer,'original producer mismatch');
assert.equal(gitBlobSha(fs.readFileSync(checker)),pinned.checker,'original checker mismatch');
const generated=spawnSync(process.execPath,[producer],{encoding:'utf8',maxBuffer:16*1024*1024,timeout:30000});
assert.equal(generated.status,0,generated.stderr||'producer failure');
const data=JSON.parse(generated.stdout);
assert.equal(data.fixtures.length,7);
const k4=data.fixtures[0];
assert.equal(k4.clauses.length,16);
assert.equal(k4.proof.length,15);
let models=0;for(let m=0;m<64;m++)if(k4.clauses.every(c=>c.literals.some(l=>((m>>(Math.abs(l)-1))&1)==(l>0?1:0))))models++;
assert.equal(models,0,'original K4 must be UNSAT');
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp-lspv1-562-'));
const accepted={};
function check(name,b){
 const f=path.join(tmp,'packet.json'); fs.writeFileSync(f,b);
 const p=spawnSync(process.execPath,[checker,f],{encoding:'utf8',maxBuffer:16*1024*1024,timeout:30000});
 if(p.error)throw p.error;
 const good=p.status===0;
 let checks=0; if(good){const v=JSON.parse(p.stdout);checks=v.checks}
 accepted[name]={accepted:good,checks,bytes:b.length,stderr:good?'':(p.stderr||'').slice(0,220)};
 return good;
}
const base=Buffer.from(JSON.stringify(data),'utf8');
function replaceToken(src,needle,replacements){
 const chunks=[],a=Buffer.from(needle),positions=[];
 for(let start=0;;){const j=src.indexOf(a,start);if(j<0)break;positions.push(j);start=j+a.length}
 assert.equal(positions.length,replacements.length,'source ID occurrence count changed');
 let off=0;for(let i=0;i<positions.length;i++){
  chunks.push(src.subarray(off,positions[i]),replacements[i]);
  off=positions[i]+a.length;
 }
 chunks.push(src.subarray(off));
 return Buffer.concat(chunks);
}
const token=Buffer.from('"s0"');
const n=(base.toString('utf8').match(/"s0"/g)||[]).length;
assert.ok(n>=2,'expected live shared source identities');
const invalid80=replaceToken(base,'"s0"',Array.from({length:n},()=>Buffer.from([34,0x80,34])));
const invalid81=replaceToken(base,'"s0"',Array.from({length:n},()=>Buffer.from([34,0x81,34])));
const mixed=replaceToken(base,'"s0"',Array.from({length:n},(_,i)=>Buffer.from([34,i%2?0x81:0x80,34])));
const canonical=b=>Buffer.from(b.toString('utf8'),'utf8');
const strict=new TextDecoder('utf-8',{fatal:true,ignoreBOM:true});
function validStrict(b){try{strict.decode(b);return true}catch(e){return false}}
assert.equal(validStrict(invalid80),false);
assert.equal(validStrict(invalid81),false);
assert.equal(validStrict(canonical(invalid80)),true);
assert.equal(invalid80.equals(invalid81),false);
assert.ok(canonical(invalid80).equals(canonical(invalid81)));
assert.ok(canonical(invalid80).equals(canonical(mixed)));
assert.ok(check('original_all_7',base));
for(const [nm,b] of [['invalid_80',invalid80],['invalid_81',invalid81],['mixed_invalid',mixed],['canonical80',canonical(invalid80)],['canonical81',canonical(invalid81)]])
 assert.ok(check(nm,b),nm);
const bom=Buffer.concat([Buffer.from([0xef,0xbb,0xbf]),base]);
assert.equal(check('leading_BOM_rejected',bom),false);
assert.equal(check('canonical_BOM_rejected',canonical(bom)),false);
const escapedBOM=replaceToken(base,'"s0"',Array.from({length:n},()=>Buffer.from('"\ufeff"','utf8')));
assert.ok(check('live_UFEFF_source_id',escapedBOM));
const wrong=JSON.parse(JSON.stringify(data));
wrong.fixtures[0].proof[0].rule='DEF';
assert.equal(check('unsupported_DEF_rule',Buffer.from(JSON.stringify(wrong))),false);
const broken=replaceToken(base,'"s0"',Array.from({length:n},(_,i)=>i===0?Buffer.from([34,0x80,34]):token));
assert.equal(check('broken_live_id_reference',broken),false);
const sample=[
 ['empty',Buffer.alloc(0)],['invalid80',Buffer.from([34,0x80,34])],
 ['invalid81',Buffer.from([34,0x81,34])],['incompleteE2',Buffer.from([34,0xe2,34])],
 ['overlongC0',Buffer.from([34,0xc0,0xaf,34])],
 ['leadingBOM',Buffer.from([0xef,0xbb,0xbf,0x7b,0x7d])],
 ['BOMinId',Buffer.from('{"\ufeff":7}','utf8')],
 ['loneSurrogateEscape',Buffer.from('{"key":"\\ud800"}','utf8')],
 ['dupKeys',Buffer.from('{"a":1,"a":2}','utf8')],
 ['malformed',Buffer.from('not_json','utf8')],
 ['highValid',Buffer.from('{"😃":"�"}','utf8')]
];
for(let i=0;i<4096;i++){const h=crypto.createHash('sha256').update('PNP-562-BYTE-'+i).digest();sample.push(['sha256_'+i,Buffer.from(h.subarray(0,(i%80)%33))])}
let grows=0,shrinks=0,same=0,parseRejects=0;
for(const [name,b] of sample){
 const x=b.toString('utf8'),q=canonical(b),y=q.toString('utf8');
 assert.equal(x,y,name+':decode-encode-decode');
 assert.deepEqual(q,canonical(q),name+':idempotence');
 let p1,p2,e1=false,e2=false;try{p1=JSON.parse(x)}catch(e){e1=true}
 try{p2=JSON.parse(y)}catch(e){e2=true}
 assert.equal(e1,e2,name+':JSON-accept-equivalence');
 if(!e1)assert.deepEqual(p1,p2,name+':JSON-object');
 else parseRejects++;
 if(q.length>b.length)grows++;else if(q.length<b.length)shrinks++;else same++;
}
const result={run:'PNP-LSPV1-562',nodeVersion:process.version,
 pinned,source:{K4Variables:6,K4SourceClauses:16,K4Models:models,K4Paid:15,fixtures:7},
 liveSourceIdOccurrences:n,subprocessOriginalChecker:accepted,
 nativeDecoder:{cases:sample.length,decoderStable:sample.length,idempotent:sample.length,jsonEquivalence:sample.length,parserRejected:parseRejects,grows,shrinks,same},
 theorem:'Every raw packet accepted by this exact recovered fixture checker has a strictly valid UTF-8 representative with identical decoded JSON, native acceptance and distinct paid-node cost. Raw byte size and raw SHA source identity may change.',
 boundaries:['No complete historical R_mix341 grammar','No external raw-byte source-hash preservation','No proof that evidence bytes or peak space are nonincreasing','P versus NP OPEN']};
try{if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+'\n');
 console.log(JSON.stringify(result,null,2));}
finally{fs.rmSync(tmp,{recursive:true,force:true})}
