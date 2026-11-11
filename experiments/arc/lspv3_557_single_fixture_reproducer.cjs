'use strict';
// LSPV-3/557. Reconstruct a *single-fixture* SAT-source packet for the
// pinned, unsound /341 SOURCE/AND3/XOR fixture checker.
// NOT the full historical R_mix341 parser or an intended-sound proof.
const fs=require('node:fs'),cp=require('node:child_process'),os=require('node:os'),
path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const oldPath='results/raw/arc/2026-11-10_1224_LSPV3_551_ACCEPTED_SAT_PACKET.json';
const checkerPath='experiments/arc/lspv2_341_independent_verify.js';
function gitBlob(text){return crypto.createHash('sha1').update('blob '+Buffer.byteLength(text)+'\0'+text).digest('hex');}
const previous=fs.readFileSync(oldPath,'utf8'),historical=fs.readFileSync(checkerPath,'utf8');
assert.equal(gitBlob(previous),'706947c767361e7c979b8208677eb983d33838f4');
assert.equal(gitBlob(historical),'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0');
const source=JSON.parse(previous).fixtures[1],E=source.graph.edges.length;
assert.equal(E,18);assert.equal(source.clauses.length,48);assert.equal(source.proof.length,47);
const ids=new Map();
source.clauses.forEach((c,i)=>ids.set(c.id,i));
source.proof.forEach((p,i)=>ids.set(p.id,48+i));
const f={
 graph:{n:12,edges:source.graph.edges}, charges:source.charges,
 clauses:source.clauses.map(c=>({id:ids.get(c.id),vertex:c.vertex,literals:c.literals})),
 proof:source.proof.map(p=>({
  id:ids.get(p.id),rule:p.rule,kind:p.kind,parents:p.parents.map(x=>ids.get(x)),
  ...(p.support!==undefined?{support:p.support,table:p.table}:{}),
  ...(p.row?{row:p.row}:{})
 })),
 deleted:source.deleted.map(d=>({sourceId:ids.get(d.sourceId),
 assignment:d.sourceId==='s0'?'0'.repeat(E):null})),
 evenWitness:source.evenWitness,properties:{essential:1}
};
const pkt={fixtures:[f],summary:[0]},raw=JSON.stringify(pkt);
assert.equal(Buffer.byteLength(raw),8573);
const sat=(c,a)=>c.literals.some(l=>a[Math.abs(l)-1]===(l>0?1:0));
const w=Array(E).fill(0);for(const i of [0,2,5,12])w[i]=1;
assert.equal(f.clauses.filter(c=>sat(c,w)).length,48);
const zero=Array(E).fill(0);
assert.equal(f.clauses.filter(c=>!sat(c,zero)).length,1);
assert.equal(sat(f.clauses[0],zero),false);
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-557-'));
function native(o){
 const file=path.join(temp,'pkt.json');fs.writeFileSync(file,JSON.stringify(o));
 const run=cp.spawnSync(process.execPath,[checkerPath,file],{encoding:'utf8',maxBuffer:10_000_000});
 if(run.error)throw run.error;
 if(run.status===0)return{accepted:true,checks:JSON.parse(run.stdout).checks};
 return{accepted:false,error:(run.stderr||run.stdout).split('\n').filter(Boolean).at(-1)};
}
let ok,controls;
try{
 ok=native(pkt);assert.deepEqual(ok,{accepted:true,checks:3273});
 controls=[
 ['numeric_charge',o=>o.fixtures[0].charges[0]=1],
 ['typed_support',o=>o.fixtures[0].proof[2].support=[0,1,12]],
 ['corrupt_table',o=>o.fixtures[0].proof[2].table^=1],
 ['corrupt_sink',o=>o.fixtures[0].proof.at(-1).row.rhs^=1],
 ['invalid_parent',o=>o.fixtures[0].proof[0].parents[0]=999],
 ['invalid_source_literal',o=>o.fixtures[0].clauses[0].literals[0]=999],
 ['corrupt_deletion_witness',o=>o.fixtures[0].deleted[0].assignment='1'+'0'.repeat(17)],
 ['corrupt_even_witness',o=>o.fixtures[0].evenWitness='1'+'0'.repeat(17)],
 ['invalid_arity',o=>o.fixtures[0].proof[0].parents=[0]],
 ['missing_source_clause',o=>o.fixtures[0].clauses.pop()]
 ].map(([name,fn])=>{const x=JSON.parse(raw);fn(x);return{name,...native(x)}});
 assert(controls.every(x=>!x.accepted));
}finally{fs.rmSync(temp,{force:true,recursive:true});}
if(process.argv[2])fs.writeFileSync(process.argv[2],raw+'\n');
console.log(JSON.stringify({scope:'recovered restricted /341 fixture checker only',
sat_source:true,source_witness:w.join(''),clauses_satisfied:48,
accepted:ok,packet_bytes:Buffer.byteLength(raw),paid_steps:47,
negative_controls:controls},null,2));
