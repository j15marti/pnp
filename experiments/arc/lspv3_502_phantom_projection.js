#!/usr/bin/env node
'use strict';
// LSPV-3/502. Original SOURCE/AND3/XOR checker replay.
// Raw proof MUST pass native validation BEFORE any affine projection.
// Does not implement historical RES, DEF, LOCAL-CONVERT or branching.
const fs=require('fs'),os=require('os'),path=require('path'),cp=require('child_process'),crypto=require('crypto'),assert=require('assert').strict;
const root=path.resolve(__dirname,'../..');
const checker=path.join(__dirname,'lspv2_341_independent_verify.js');
const packetPath=path.join(root,'results/raw/arc/2026-11-07_2224_LSPV3_491_BALANCED_341_PACKET.json');
const binderPath=path.join(__dirname,'lspv3_490_external_source_bind.cjs');
const sha=f=>{const b=fs.readFileSync(f);return crypto.createHash('sha1').update('blob '+b.length+'\\0').update(b).digest('hex')};
assert.equal(sha(checker),'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0');
assert.equal(sha(packetPath),'481423a2f5271ab600bbc2f9a526fe62523239a9');
assert.equal(sha(binderPath),'b113119b7b87dac7510603804d91918e80f301b0');
const binder=require(binderPath),base=JSON.parse(fs.readFileSync(packetPath,'utf8'));
const copy=x=>JSON.parse(JSON.stringify(x));
function run(packet){
 const d=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-502-')),p=path.join(d,'p.json');
 try{fs.writeFileSync(p,JSON.stringify(packet));
   const r=cp.spawnSync(process.execPath,[checker,p],{encoding:'utf8',maxBuffer:32*1024*1024});
   return {ok:r.status===0,result:r.status===0?JSON.parse(r.stdout):r.stderr.slice(0,250)};
 }finally{fs.rmSync(d,{recursive:true,force:true})}
}
function pair(f){
 const m=new Map(f.proof.map(p=>[p.id,p]));
 const x=f.proof.find(p=>p.rule==='XOR'&&p.parents.every(id=>m.get(id)?.rule==='AND3'&&m.get(id)?.row));
 assert.ok(x,'two row join');return x.parents.map(id=>m.get(id));
}
function inject(p,which){for(const f of p.fixtures){
 const e=f.graph.edges.length,hi=1n<<BigInt(e+13),q=1n<<BigInt(e);
 for(const n of pair(f)){const m=BigInt(n.row.mask);assert.ok(m>=0n&&m<q);n.row.mask=(which==='hi'?(m^hi):(m-q)).toString()}
}return p}
function project(p){const q=copy(p);let rows=0;for(const f of q.fixtures){
 const mask=(1n<<BigInt(f.graph.edges.length))-1n;
 for(const n of f.proof)if(n.row){n.row.mask=(BigInt(n.row.mask)&mask).toString();rows++}
}return {q,rows}}
const start=Date.now(),rss0=process.memoryUsage().rss;
assert.equal(run(base).result.checks,30714);
let native=0,normalized=0;
for(const mode of ['hi','negative']){
 const p=inject(copy(base),mode);assert.ok(run(p).ok);native++;
 const r=project(p);assert.equal(r.rows,157);assert.ok(run(r.q).ok);normalized++;
}
const corrupt=copy(base),f=corrupt.fixtures[0];
pair(f)[0].row.mask=(BigInt(pair(f)[0].row.mask)^(1n<<BigInt(f.graph.edges.length+13))).toString();
assert.equal(run(corrupt).ok,false,'raw corrupted proof must be rejected');
assert.ok(run(project(corrupt).q).ok,'counterexample: premature projection launders invalid native step');
const badSource=copy(base);badSource.fixtures[0].clauses[0].literals[0]=999;
assert.equal(run(badSource).ok,false);
for(const f of base.fixtures)assert.equal(binder.bind(f,binder.serialize(f)).clauses,f.clauses.length);
const first=base.fixtures[0],l=first.clauses[0].literals;
const t=[Math.abs(l[0]),-Math.abs(l[0]),Math.abs(l[1])];
const mutant=binder.serialize(first,0,t);
assert.equal(mutant.length,binder.serialize(first).length);
assert.throws(()=>binder.bind(first,mutant));
console.log(JSON.stringify({
 status:'PASS',nativeOriginalAssertions:30714,fixtures:base.fixtures.length,
 originalClauses:base.fixtures.map(f=>f.clauses.length),
 originalVars:base.fixtures.map(f=>f.graph.edges.length),
 rowAnnotations:157,acceptedPhantomPairs:native,acceptedNegativePairs:native,
 acceptedProjections:normalized,invalidRawSinglePhantomRejected:true,
 invalidRawCanBeLaunderedByUnsafePrematureProjection:true,
 invalidSourceRejected:true,externalSameLengthSATMutationRejected:true,
 wallMs:Date.now()-start,rssBefore:rss0,rssAfter:process.memoryUsage().rss,
 scope:'Recovered SOURCE/AND3/XOR only. Raw native acceptance required before projection.'
},null,2));
