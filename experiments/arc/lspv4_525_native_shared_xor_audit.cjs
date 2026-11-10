#!/usr/bin/env node
'use strict';
/* LSPV-4/525: honest SOURCE/AND3/XOR reconvergence control.
 * Run: node experiments/arc/lspv4_525_native_shared_xor_audit.cjs [out.json]
 * /341 original: limited fixture checker. /539: SEPARATE typed,
 * externally source-bound reference. Neither is full historical R_mix341.
 */
const fs=require('fs'),path=require('path'),vm=require('vm'),crypto=require('crypto'),assert=require('assert');
const root=path.resolve(__dirname,'../..');
const files=[
 ['experiments/arc/lspv2_341_mixed_tseitin_min_dag.js','4081022e8a3841d79f751a3d3a7a10decbb026da'],
 ['experiments/arc/lspv2_341_independent_verify.js','fcb7d4ced8f922de14c0bda16263a8cc7853e8e0'],
 ['experiments/arc/lspv2_539_strict_fragment_reference.cjs','fc91a6f33d0d010d6225365a3d9ce72a090af21f']
];
function blobSHA(s){const b=Buffer.from(s,'utf8');return crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex');}
const bodies=files.map(([p,sha])=>{const s=fs.readFileSync(path.join(root,p),'utf8');assert.strictEqual(blobSHA(s),sha,'pinned Git blob changed: '+p);return s;});
let out='';vm.runInNewContext(bodies[0],{console:{log:s=>{out=s;}}},{timeout:100000});
const original=JSON.parse(out),base=original.fixtures.find(f=>f.graph.name==='K4');assert(base,'K4 missing');
const ref=require(path.join(root,files[2][0]));
const source='p cnf '+base.graph.edges.length+' '+base.clauses.length+'\n'+base.clauses.map(c=>c.literals.join(' ')+' 0').join('\n')+'\n';
assert.strictEqual(Buffer.byteLength(source),163);
function native(packet){let result='';try{vm.runInNewContext(bodies[1],{require:name=>{assert.strictEqual(name,'fs');return {readFileSync:()=>packet}},process:{argv:['node','fixture','packet']},console:{log:x=>{result=x}}},{timeout:100000});return {accepted:true,result:JSON.parse(result)};}catch(e){return {accepted:false,diagnostic:String(e.message)}}}
function xor(a,b){return {mask:'0x'+(BigInt(a.mask)^BigInt(b.mask)).toString(16),rhs:a.rhs^b.rhs};}
function extend(k){const f=JSON.parse(JSON.stringify(base)),anchor=f.proof.find(v=>v.id==='d12');assert(anchor&&anchor.row);let z=f.proof.at(-1);for(let i=0;i<k;i++){const u={id:'d'+(15+2*i),kind:'affine',rule:'XOR',parents:[z.id,anchor.id],row:xor(z.row,anchor.row)},v={id:'d'+(16+2*i),kind:'affine',rule:'XOR',parents:[u.id,anchor.id],row:xor(u.row,anchor.row)};f.proof.push(u,v);z=v;}return f;}
function structural(f){const nodes=new Map([...f.clauses.map(c=>[c.id,{parents:[]}]),...f.proof.map(p=>[p.id,p])]),sink=f.proof.at(-1).id,used=new Set();
 function dfs(id){if(used.has(id))return;used.add(id);const n=nodes.get(id);assert(n,'bad parent');for(const p of n.parents)dfs(p);}dfs(sink);
 const outdeg=new Map([...nodes.keys()].map(id=>[id,0]));for(const n of f.proof)for(const p of n.parents)outdeg.set(p,outdeg.get(p)+1);
 const surplus=[...outdeg].filter(([id])=>id!==sink).reduce((s,[id,n])=>s+n-1,0),remaining=new Map(outdeg),live=new Set();let peak=0;
 for(const n of f.proof){for(const p of n.parents)if(p.startsWith('d'))assert(live.has(p),'not-live parent '+p);live.add(n.id);peak=Math.max(peak,live.size);for(const p of n.parents){remaining.set(p,remaining.get(p)-1);if(remaining.get(p)===0)live.delete(p)}}
 return {m:f.clauses.length,q:f.proof.length,allAncestor:used.size===nodes.size,surplus,anchorOutdegree:outdeg.get('d12'),derivedPeakOriginalOrder:peak};}
const packetOf=f=>JSON.stringify({version:original.version,fixtures:[f],summary:[original.summary[0]]});
let assertions=0;const cases=[];
for(const k of [0,1,2,4,8,16]){
 const f=extend(k),packet=packetOf(f),typed=ref.tryAudit(source,packet),old=native(packet),st=structural(f);
 assert(typed.accepted,typed.diagnostic);assert.strictEqual(st.q,15+2*k);assert.strictEqual(st.surplus,2*k);assert.strictEqual(st.anchorOutdegree,1+2*k);assert(st.allAncestor);assert.strictEqual(st.derivedPeakOriginalOrder,5);assert.strictEqual(typed.result.maxDependencySpan,6+2*k);assertions+=7;
 if(k===0)assert(old.accepted,'original K4 unexpectedly rejected');else{assert(!old.accepted,'original fixture accepted extra proof');assert(/proof candidate length/.test(old.diagnostic),old.diagnostic)}assertions+=k?2:1;
 let negative='n/a';if(k){const bad=JSON.parse(packet);bad.fixtures[0].proof.at(-1).row.rhs^=1;assert(!ref.tryAudit(source,JSON.stringify(bad)).accepted,'corrupt XOR accepted');negative='REJECT';assertions++;}
 cases.push({k,sourceBytes:Buffer.byteLength(source),packetBytes:Buffer.byteLength(packet),paidDistinct:typed.result.logicalWeight,referenceCount:typed.result.referenceCount,dependencySpan:typed.result.maxDependencySpan,reuseSurplus:st.surplus,anchorOutdegree:st.anchorOutdegree,derivedPeakOriginalOrder:st.derivedPeakOriginalOrder,reference:'ACCEPT',originalFixture:k===0?'ACCEPT':'REJECT_LENGTH_GUARD',corruptXor:negative});
}
const bad=extend(1);const sourceMut=source.replace('1 2 3 0','-1 2 3 0');assert(sourceMut!==source);assert(!ref.tryAudit(sourceMut,packetOf(bad)).accepted,'source mismatch');assertions++;
bad.proof.at(-1).parents[0]='missing';assert(!ref.tryAudit(source,packetOf(bad)).accepted,'missing parent');assertions++;
const result={run:'LSPV-4/525',scope:'SEPARATE typed SOURCE/AND3/XOR fragment; historical R_mix341 full byte language remains OPEN',pinnedGitBlobs:files,cases,hostile:{sourceMismatch:'REJECT',missingParent:'REJECT'},assertions,qualification:'logical unit-first-creation costs only; actual parser bytes and work/space separately charged; no native CASE, DEF, LOCAL-CONVERT or RES'};
const json=JSON.stringify(result,null,2)+'\n';if(process.argv[2])fs.writeFileSync(process.argv[2],json);process.stdout.write(json);
