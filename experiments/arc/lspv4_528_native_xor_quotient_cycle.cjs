#!/usr/bin/env node
'use strict';
/* LSPV-4/528. Run from a j15marti/pnp checkout:
   node experiments/arc/lspv4_528_native_xor_quotient_cycle.cjs [output.json]
   Checks pinned recovered original fixture versus separately typed /539.
   Neither is the complete historical R_mix341 accepted-byte verifier. */
const fs=require('fs'),path=require('path'),vm=require('vm'),crypto=require('crypto'),assert=require('assert');
const root=path.resolve(__dirname,'../..');
const files=[
 ['experiments/arc/lspv2_341_mixed_tseitin_min_dag.js','4081022e8a3841d79f751a3d3a7a10decbb026da'],
 ['experiments/arc/lspv2_341_independent_verify.js','fcb7d4ced8f922de14c0bda16263a8cc7853e8e0'],
 ['experiments/arc/lspv2_539_strict_fragment_reference.cjs','fc91a6f33d0d010d6225365a3d9ce72a090af21f']
];
const blobSHA=s=>{const b=Buffer.from(s);return crypto.createHash('sha1').update(Buffer.from('blob '+b.length+'\0')).update(b).digest('hex')};
const bodies=files.map(([f,sha])=>{const s=fs.readFileSync(path.join(root,f),'utf8');assert.strictEqual(blobSHA(s),sha,'original body changed: '+f);return s});
let output='';
vm.runInNewContext(bodies[0],{console:{log:x=>output=x}},{timeout:30000});
const produced=JSON.parse(output),base=produced.fixtures.find(f=>f.graph.name==='K4');
assert(base);
const originalSource='p cnf '+base.graph.edges.length+' '+base.clauses.length+'\n'+base.clauses.map(c=>c.literals.join(' ')+' 0').join('\n')+'\n';
assert.strictEqual(Buffer.byteLength(originalSource),163);
const typed=require(path.join(root,files[2][0]));
function packet(f){return JSON.stringify({version:produced.version,fixtures:[f],summary:[produced.summary[0]]})}
function xor(a,b){return {mask:'0x'+(BigInt(a.mask)^BigInt(b.mask)).toString(16),rhs:a.rhs^b.rhs}}
function extend(k){
 const f=JSON.parse(JSON.stringify(base)),anchor=f.proof.find(n=>n.id==='d12');assert(anchor&&anchor.row);
 let z=f.proof.at(-1);
 for(let i=0;i<k;i++){
  const u={id:'d'+(15+2*i),kind:'affine',rule:'XOR',parents:[z.id,anchor.id],row:xor(z.row,anchor.row)};
  const v={id:'d'+(16+2*i),kind:'affine',rule:'XOR',parents:[u.id,anchor.id],row:xor(u.row,anchor.row)};
  f.proof.push(u,v);z=v;
 }
 return f;
}
function cyclic(edges){
 const adj=new Map(),v=new Set();
 for(const [a,b] of edges){v.add(a);v.add(b);adj.set(a,(adj.get(a)||[]).concat(b))}
 const visiting=new Set(),done=new Set();
 function dfs(x){if(visiting.has(x))return true;if(done.has(x))return false;visiting.add(x);for(const y of adj.get(x)||[])if(dfs(y))return true;visiting.delete(x);done.add(x);return false}
 return [...v].some(x=>dfs(x));
}
function native(p){
 let out='';
 try {
  vm.runInNewContext(bodies[1],{require:n=>{assert.strictEqual(n,'fs');return {readFileSync:()=>p}},
     process:{argv:['node','verify','packet.json']},console:{log:x=>out=x}},{timeout:30000});
  return {accepted:true,output:JSON.parse(out)};
 }catch(e){return {accepted:false,diagnostic:String(e.message)}}
}
function key(x){
 if(x.row)return 'affine:'+BigInt(x.row.mask).toString()+':'+x.row.rhs;
 if(x.kind==='source')return 'source:'+x.id;
 return 'factor:'+x.support.join(',')+':'+x.table;
}
const cases=[];
for(const k of [0,1,2,4,8,16]){
 const f=extend(k),p=packet(f),r=typed.tryAudit(originalSource,p),n=native(p);
 assert(r.accepted,'typed checker rejected '+k+': '+r.diagnostic);
 assert.strictEqual(n.accepted,k===0,'original fixture checker mismatch');
 const nodes=new Map([...f.clauses.map(c=>[c.id,{...c,kind:'source'}]),...f.proof.map(q=>[q.id,q])]);
 const edges=f.proof.flatMap(q=>q.parents.map(par=>[par,q.id]));
 const qedges=edges.map(([u,v])=>[key(nodes.get(u)),key(nodes.get(v))]);
 assert.strictEqual(cyclic(edges),false,'original dependency cycle');
 assert.strictEqual(cyclic(qedges),k>0,'semantic quotient cycle mismatch');
 const labels=new Set([...nodes.values()].map(key));
 assert.strictEqual(labels.size,k?32:31);
 assert.strictEqual(r.result.logicalWeight,15+2*k);
 assert.strictEqual(r.result.referenceCount,30+4*k);
 assert.strictEqual(r.result.maxDependencySpan,6+2*k);
 if(k){assert.strictEqual(key(nodes.get('d14')),key(nodes.get('d16')));assert.notStrictEqual(key(nodes.get('d15')),key(nodes.get('d16')))}
 cases.push({k,paidDistinct:r.result.logicalWeight,references:r.result.referenceCount,
    spanUnitDependency:r.result.maxDependencySpan,semanticLabels:labels.size,
    semanticQuotientCycle:cyclic(qedges),eventDagCycle:cyclic(edges),
    sourceBytes:Buffer.byteLength(originalSource),packetBytes:Buffer.byteLength(p),
    typedReference:'ACCEPT',originalFixture:n.accepted?'ACCEPT':'REJECT_LENGTH_GUARD'});
}
const hostile={};
for(const kind of ['wrong_sink_rhs','missing_parent','source_sign','false_AND3','duplicate_ID']){
 const f=extend(1);
 if(kind==='wrong_sink_rhs')f.proof.at(-1).row.rhs=0;
 if(kind==='missing_parent')f.proof.at(-1).parents[0]='no-parent';
 if(kind==='source_sign')f.clauses[0].literals[0]*=-1;
 if(kind==='false_AND3')f.proof[0].table^=1;
 if(kind==='duplicate_ID')f.proof.at(-1).id='d12';
 assert(!typed.tryAudit(originalSource,packet(f)).accepted,'bad packet accepted: '+kind);
 hostile[kind]='REJECT';
}
const result={role:'LSPV-4',run:528,status:'PROVED/RESTRICTED + COMPUTATIONAL',cases,hostile,
  limitation:'Recovered original /341 checker rejects k>0 by fixed count; /539 separately typed reference accepts. No complete historical checker.',
  provenance:files,precursor:'LSPV-5/464 generic DAG-label quotient cycle and history-separation theorem; here a concrete pinned SOURCE/AND3/XOR source-bound specialization'};
const out=JSON.stringify(result,null,2)+'\n';
if(process.argv[2])fs.writeFileSync(process.argv[2],out);process.stdout.write(out);
