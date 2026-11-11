#!/usr/bin/env node
'use strict';
// LSPV-2/545: differential audit of PINNED /341 fixture checker, not full R_mix341.
// Usage: node experiments/arc/lspv2_545_invalid_utf8_packet_audit.cjs [results.json]
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const crypto=require('node:crypto'),cp=require('node:child_process'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const sources={
 producer:['experiments/arc/lspv2_341_mixed_tseitin_min_dag.js','4081022e8a3841d79f751a3d3a7a10decbb026da'],
 checker:['experiments/arc/lspv2_341_independent_verify.js','fcb7d4ced8f922de14c0bda16263a8cc7853e8e0']
};
const sha256=b=>crypto.createHash('sha256').update(b).digest('hex');
const gitsha=b=>crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');
for(const [role,[p,h]] of Object.entries(sources))
 assert.equal(gitsha(fs.readFileSync(path.join(root,p))),h,'pinned '+role+' changed');
function splice(bytes,token,replacement,firstOnly=false) {
 const chunks=[];let pos=0,count=0;
 while(true) {
  const i=bytes.indexOf(token,pos);if(i<0)break;
  chunks.push(bytes.subarray(pos,i),replacement);pos=i+token.length;count++;
  if(firstOnly)break;
 }
 assert(count>0,'no source token');chunks.push(bytes.subarray(pos));
 return {bytes:Buffer.concat(chunks),count};
}
const q=s=>Buffer.from('"'+s+'"','ascii'),bad=n=>Buffer.from([34,n,34]);
const producer=cp.spawnSync(process.execPath,[path.join(root,sources.producer[0])],
 {encoding:'utf8',maxBuffer:16*1024*1024,timeout:20000});
assert.equal(producer.status,0,producer.stderr);
const all=JSON.parse(producer.stdout),f=all.fixtures.find(x=>x.graph.name==='K4');
assert(f&&f.clauses.length===16&&f.proof.length===15);
const base=Buffer.from(JSON.stringify({fixtures:[f],summary:[all.summary.find(x=>x.name==='K4')]}));
const a=splice(base,q('s0'),bad(0x80)),b=splice(base,q('s0'),bad(0x81));
assert.equal(a.count,3);assert.equal(b.count,3);
assert(!a.bytes.equals(b.bytes)&&a.bytes.toString('utf8')===b.bytes.toString('utf8'));
const one=splice(base,q('s0'),bad(0x80),true);
const opcode=splice(base,q('AND3'),bad(0x80),true);
const collision=splice(a.bytes,q('s1'),bad(0x81));
assert.equal(collision.count,2);
const graph=splice(base,q('K4'),bad(0x80),true);
const cases=[['baseline',base,true],['invalid80_all_source_refs',a.bytes,true],
 ['invalid81_all_source_refs',b.bytes,true],['invalid80_one_source_ref',one.bytes,false],
 ['invalid80_rule_opcode',opcode.bytes,false],
 ['invalid80_81_two_source_ids_collide',collision.bytes,false],
 ['invalid80_graph_display',graph.bytes,true]];
let models=0;
for(let x=0;x<64;x++) if(f.clauses.every(c=>c.literals.some(l=>
 l>0?((x>>(l-1))&1)===1:((x>>(-l-1))&1)===0)))models++;
assert.equal(models,0);
const dimacs=Buffer.from('p cnf 6 16\n'+f.clauses.map(c=>c.literals.join(' ')+' 0').join('\n')+'\n','ascii');
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'pnp545-')),rows=[];
try{
 for(const [name,raw,expected] of cases) {
  const file=path.join(tmp,name+'.json');fs.writeFileSync(file,raw);
  const r=cp.spawnSync(process.execPath,[path.join(root,sources.checker[0]),file],
   {encoding:'utf8',maxBuffer:16*1024*1024,timeout:20000});
  let parsed;try{parsed=JSON.parse(r.stdout);}catch{}
  const accepted=r.status===0&&!!parsed;
  assert.equal(accepted,expected,name+': '+r.stderr);
  if(accepted){assert.equal(parsed.checks,1401);assert.equal(parsed.cases[0].proofNodes,15);}
  let strictUTF8=true;
  try{new TextDecoder('utf-8',{fatal:true}).decode(raw);}catch{strictUTF8=false;}
  rows.push({name,expected,accepted,bytes:raw.length,sha256:sha256(raw),
    strictUTF8,replacements:(raw.toString('utf8').match(/\ufffd/g)||[]).length,
    assertionGroups:parsed?.checks??null,diagnostic:accepted?'':r.stderr.slice(0,240)});
 }
}finally{fs.rmSync(tmp,{recursive:true,force:true});}
assert.equal(rows.filter(r=>r.accepted).length,4);
assert.equal(rows.filter(r=>!r.accepted).length,3);
assert.equal(JSON.stringify(JSON.parse(a.bytes.toString('utf8'))),
 JSON.stringify(JSON.parse(b.bytes.toString('utf8'))));
const result={experiment:'LSPV-2/545',sources,node:process.version,
 scope:'Original /341 SOURCE/AND3/XOR fixture checker only. Full R_mix341 not authenticated.',
 generatedK4:{dimacsSHA256:sha256(dimacs),dimacsBytes:dimacs.length,variables:6,
 clauses:16,modelsOf64:models,distinctPaidNodes:15},rows,accepted:4,rejected:3,
 originalCheckerAssertions:5604,byteLevelEqualityOfDecodedVariants:true,
 status:'PROVED/RESTRICTED + COMPUTATIONAL; P2-D1 P2-C3 P2-B1 B3 OPEN'};
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
