#!/usr/bin/env node
'use strict';
/* LSPV-2/542 source-permutation transporter. SEPARATE typed reference fragment.
   Does not define historical R_mix341 grammar. Unknown opcodes yield MAY. */
const fs=require('fs'),crypto=require('crypto');
const ref=require('./lspv2_539_strict_fragment_reference.cjs');
const die=s=>{throw Error('TRANSPORT542: '+s)};
function sig(row,n){
 if(!Array.isArray(row)||row.length!==3)die('width');
 const ids=new Set();
 for(const x of row){if(!Number.isSafeInteger(x)||x===0||Math.abs(x)>n||ids.has(Math.abs(x)))die('signed variable');ids.add(Math.abs(x))}
 return row.slice().sort((a,b)=>a-b).join(',');
}
function transport(source,packet){
 const F=ref.parseDimacs(source),p=JSON.parse(packet);
 if(!p||!Array.isArray(p.fixtures)||p.fixtures.length!==1)die('one fixture');
 const f=p.fixtures[0];if(!f||!Array.isArray(f.clauses)||f.clauses.length!==F.nc)die('source count');
 const buckets=new Map();
 F.clauses.forEach((c,i)=>{const k=sig(c,F.nv);if(!buckets.has(k))buckets.set(k,[]);buckets.get(k).push(i)});
 const mapping=[],ids=new Set();
 for(const c of f.clauses){
  if(!c||typeof c.id!=='string'||ids.has(c.id))die('SOURCE identity');
  ids.add(c.id);const k=sig(c.literals,F.nv),q=buckets.get(k);
  if(!q||!q.length)die('signed source multiset');
  mapping.push({sourceId:c.id,externalOccurrence:q.shift()});
 }
 if([...buckets.values()].some(q=>q.length))die('extra source occurrence');
 const h=x=>crypto.createHash('sha256').update(x).digest('hex');
 // Internal text only for REF-539 semantic replay; NEVER rewrite native packet.
 const internal='p cnf '+F.nv+' '+F.nc+'\n'+f.clauses.map(c=>c.literals.join(' ')+' 0').join('\n')+'\n';
 let r;
 try{r=ref.auditCertificate(internal,packet)}
 catch(e){let reason=String(e.message||e);return {status:reason.includes('UNAUTHENTICATED NATIVE OPCODE')?'UNAUTHENTICATED_MAY':'REFERENCE_REJECT',abstractMinCost:0,reason,sourceSHA256:h(source),packetSHA256:h(packet)}}
 return {status:'VERIFIED_SEPARATE_FRAGMENT',sourceSHA256:h(source),packetSHA256:h(packet),sourceBytes:Buffer.byteLength(source),packetBytes:Buffer.byteLength(packet),mapping,paidDistinct:r.paidDistinct,logicalWeight:r.logicalWeight,referenceCount:r.referenceCount,maxDependencySpan:r.maxDependencySpan,scope:'SOURCE/AND3/XOR only; no historical rule closure'};
}
module.exports={transport};
if(require.main===module){if(process.argv.length!==4)throw Error('usage: transporter.cjs source.cnf cert.json');const r=transport(fs.readFileSync(process.argv[2],'utf8'),fs.readFileSync(process.argv[3],'utf8'));console.log(JSON.stringify(r,null,2));if(r.status==='REFERENCE_REJECT')process.exitCode=1}