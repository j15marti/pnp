#!/usr/bin/env node
'use strict';
/*
 LSPV-3/589: a SEPARATE strict mathematical/source-binding gate for the
 archived /341 SOURCE/AND3/XOR packet format.
 It is NOT the historical native checker, NOT the missing full R_mix341 parser,
 and its stricter acceptance policy must NEVER substitute for native acceptance.
 Run on a fresh checkout: node experiments/arc/lspv3_589_source_bound_gate.cjs
 Existing original checker is executed unmodified in a Node subprocess.
*/
const fs=require('node:fs');
const path=require('node:path');
const os=require('node:os');
const cp=require('node:child_process');
const crypto=require('node:crypto');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../..');
const paths={
 checker:'experiments/arc/lspv2_341_independent_verify.js',
 original:'results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json',
 fake582:'results/raw/arc/2026-11-11_1824_LSPV3_582_STRING_CHARGE_SAT_ACCEPTED_PACKET.json',
 fake583:'results/raw/arc/2026-11-11_1924_LSPV3_583_ROTATED_SUPPORT_SAT_ACCEPTED_PACKET.json',
 hybrid500:'results/raw/review/2026-11-11_1948_LSPV5_500_HYBRID_ALIAS_SAT_ACCEPTED.json'
};
const pinned={
 checker:'fcb7d4ced8f922de14c0bda16263a8cc7853e8e0',
 original:'fe27fe1011d0021e721ccaeb747ed58da65d7464',
 fake582:'6cf9b0fe1e5a9419e8967d836c707c385418b810',
 fake583:'5d78d8f6eb5934bf805ee90736b1f88d4acd2729',
 hybrid500:'e083e684f67a5520d6404788693a40d2dd4870b8'
};
function blob(b){return crypto.createHash('sha1').update('blob '+b.length+'\0').update(b).digest('hex');}
function sha256(b){return crypto.createHash('sha256').update(b).digest('hex');}
const sources={};
for(const [k,p] of Object.entries(paths)){
 const bytes=fs.readFileSync(path.join(root,p));
 assert.equal(blob(bytes),pinned[k],'mismatched Git blob '+k);
 sources[k]={bytes,sha256:sha256(bytes),path:p,gitBlob:pinned[k]};
}
const packet={};
for(const k of ['original','fake582','fake583','hybrid500'])packet[k]=JSON.parse(sources[k].bytes);
function reject(name){throw Error(name);}
function need(cond,name){if(!cond)reject(name);}
function idKey(id){
 if(typeof id==='number'&&Number.isSafeInteger(id)&&id>=0)return 'n:'+id;
 if(typeof id==='string'&&/^[A-Za-z][A-Za-z0-9._:-]*$/.test(id))return 's:'+id;
 reject('ID_TYPE');
}
function rowCheck(r,E){
 need(r&&typeof r.mask==='string'&&/^0x(?:0|[1-9a-f][0-9a-f]*)$/.test(r.mask),'ROW_LEXICAL');
 need(r.rhs===0||r.rhs===1,'ROW_RHS_TYPE');
 let m=BigInt(r.mask);
 need(m>=0n&&m<(1n<<BigInt(E)),'ROW_RANGE');
 return {mask:m,rhs:r.rhs};
}
function tableBit(v,bits){
 let ix=0;for(let j=0;j<v.support.length;j++)ix|=bits[v.support[j]]<<j;
 return (v.table>>ix)&1;
}
function signedSource(f){return f.clauses.map(c=>[...c.literals]);}
/* Original source must be supplied by the verifier independently of the
 candidate packet. Exact ORDERED signed-clause equality here is deliberately
 stronger than multiset equality and does not assert historical byte grammar.
 Validity of the extra strict gate implies mathematical UNSAT by induction;
 its acceptance is only a subset of all native accepted packets. */
function strictAudit(f,external){
 need(Array.isArray(external)&&Array.isArray(f.clauses),'SOURCE_TYPE');
 need(f.clauses.length===external.length&&
    f.clauses.every((c,i)=>JSON.stringify(c.literals)===JSON.stringify(external[i])),'SOURCE_MISMATCH');
 const g=f.graph,V=g.n,E=g.edges.length;
 need(Number.isSafeInteger(V)&&V>=4&&Array.isArray(g.edges)&&E*2===3*V,'GRAPH_DIM');
 need(Array.isArray(f.charges)&&f.charges.length===V&&f.charges.every(x=>x===0||x===1),'CHARGE_TYPE');
 need(f.charges.reduce((a,b)=>a^b,0)===1,'CHARGE_PARITY');
 const incidence=Array.from({length:V},()=>[]),degree=Array(V).fill(0),edges=new Set();
 g.edges.forEach((edge,i)=>{
  need(Array.isArray(edge)&&edge.length===2&&edge.every(x=>Number.isSafeInteger(x)&&x>=0&&x<V)&&edge[0]!==edge[1],'EDGE_TYPE');
  let [u,v]=edge,k=[Math.min(u,v),Math.max(u,v)].join(':');
  need(!edges.has(k),'EDGE_DUPLICATE');edges.add(k);
  incidence[u].push(i);incidence[v].push(i);degree[u]++;degree[v]++;
 });
 need(degree.every(d=>d===3),'GRAPH_DEGREE');
 need(f.clauses.length===4*V,'SOURCE_COUNT');
 const byID=new Map(),parents=new Map(),patterns=Array.from({length:V},()=>new Set());
 for(const c of f.clauses){
  const id=idKey(c.id);need(!byID.has(id),'DUPLICATE_ID');
  need(Number.isSafeInteger(c.vertex)&&c.vertex>=0&&c.vertex<V,'SOURCE_VERTEX');
  const support=incidence[c.vertex],lits=c.literals;
  need(Array.isArray(lits)&&lits.length===3&&lits.every(x=>Number.isSafeInteger(x)&&x!==0)&&
   JSON.stringify(lits.map(x=>Math.abs(x)-1).sort((a,b)=>a-b))===
   JSON.stringify([...support].sort((a,b)=>a-b)),'SOURCE_INCIDENCE');
  const sign=lits.map(x=>x<0?1:0),parity=sign.reduce((a,b)=>a^b,0);
  need(parity!==f.charges[c.vertex],'SOURCE_SIGN_PARITY');
  const pattern=support.map(e=>lits.find(x=>Math.abs(x)-1===e)<0?1:0).join('');
  need(!patterns[c.vertex].has(pattern),'SOURCE_SIGN_DUP');patterns[c.vertex].add(pattern);
  let table=0;
  for(let m=0;m<8;m++){
   const bits=Array(E).fill(0);
   for(let j=0;j<3;j++)bits[support[j]]=(m>>j)&1;
   if(lits.some(x=>x>0?bits[x-1]===1:bits[-x-1]===0))table|=1<<m;
  }
  byID.set(id,{kind:'factor',support:[...support],table});parents.set(id,[]);
 }
 need(patterns.every(v=>v.size===4),'SOURCE_MISSING_PATTERN');
 need(Array.isArray(f.proof)&&f.proof.length===4*V-1,'PROOF_COUNT');
 for(const p of f.proof){
  const id=idKey(p.id);need(!byID.has(id),'INFERENCE_ID_FRESH');
  need(Array.isArray(p.parents)&&p.parents.length===2&&idKey(p.parents[0])!==idKey(p.parents[1]),'PARENT_ARITY');
  const pp=p.parents.map(idKey);need(pp.every(k=>byID.has(k)),'PARENT_MISSING');
  const [a,b]=pp.map(k=>byID.get(k));
  if(p.rule==='AND3'){
   need(a.kind==='factor'&&b.kind==='factor'&&p.kind==='factor','AND3_PARENT_TYPE');
   const sup=[...new Set([...a.support,...b.support])].sort((x,y)=>x-y);
   need(sup.length<=3,'AND3_ARITY');
   need(Array.isArray(p.support)&&p.support.length===sup.length&&
    p.support.every(x=>Number.isSafeInteger(x)&&sup.includes(x))&&
    new Set(p.support).size===sup.length,'AND3_SUPPORT_TYPE');
   need(Number.isInteger(p.table)&&p.table>=0&&p.table<256,'AND3_TABLE_TYPE');
   let tab=0;
   for(let m=0;m<(1<<sup.length);m++){
    const bits=Array(E).fill(0);
    for(let j=0;j<sup.length;j++)bits[sup[j]]=(m>>j)&1;
    if(tableBit(a,bits)&&tableBit(b,bits)){
     let ix=0;for(let j=0;j<p.support.length;j++)ix|=bits[p.support[j]]<<j;
     tab|=1<<ix;
    }
   }
   need(tab===p.table,'AND3_TABLE');
   const out={kind:'factor',support:[...p.support],table:tab};
   if(p.row){
    const row=rowCheck(p.row,E);
    for(let e=0;e<E;e++)if(((row.mask>>BigInt(e))&1n)===1n)need(sup.includes(e),'AFFINE_SCOPE');
    for(let m=0;m<(1<<p.support.length);m++){
     let lhs=0;
     for(let e=0;e<E;e++)if((row.mask>>BigInt(e))&1n)
      lhs^=p.support.includes(e)?((m>>p.support.indexOf(e))&1):0;
     need(((tab>>m)&1)===(lhs===row.rhs?1:0),'AFFINE_ALIAS');
    }
    out.row=row;
   }
   byID.set(id,out);
  }else if(p.rule==='XOR'){
   need(a.row&&b.row&&p.row&&p.kind==='affine','XOR_PARENT_TYPE');
   const row=rowCheck(p.row,E);
   need(row.mask===(a.row.mask^b.row.mask)&&row.rhs===(a.row.rhs^b.row.rhs),'XOR_EQUATION');
   byID.set(id,{kind:'affine',row});
  }else reject('UNKNOWN_RULE');
  parents.set(id,pp);
 }
 const terminal=byID.get(idKey(f.proof.at(-1).id));
 need(terminal.kind==='affine'&&terminal.row.mask===0n&&terminal.row.rhs===1,'TERMINAL_CONTRADICTION');
 const live=new Set();
 function visit(k){if(live.has(k))return;live.add(k);for(const parent of parents.get(k)||[])visit(parent);}
 visit(idKey(f.proof.at(-1).id));
 need(f.clauses.every(c=>live.has(idKey(c.id))),'SOURCE_NOT_LIVE');
 return {accept:true,source:f.clauses.length,paid:f.proof.length,ancestry:live.size,vertices:V,variables:E};
}
const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'lspv3-589-'));
function native(name,object){
 const p=path.join(tmp,name+'.json');
 fs.writeFileSync(p,JSON.stringify(object)+'\n');
 const r=cp.spawnSync(process.execPath,[path.join(root,paths.checker),p],{encoding:'utf8',timeout:30000});
 return {accepted:r.status===0,status:r.status,stderr:r.stderr.trim().slice(0,500),
    checks:r.status===0?JSON.parse(r.stdout).checks:null};
}
const copy=x=>JSON.parse(JSON.stringify(x));
const cases=[];
function test(name,f,external,expect){
 let got='OK',metadata=null;
 try{metadata=strictAudit(f,external);}catch(e){got=e.message;}
 cases.push({name,expected:expect,observed:got,pass:got===expect,metadata});
 assert.equal(got,expect,name);
}
for(const f of packet.original.fixtures)test('original_'+f.graph.name,f,signedSource(f),'OK');
for(const k of ['fake582','fake583','hybrid500'])
 test('native_accepted_SAT_'+k,packet[k].fixtures[0],signedSource(packet[k].fixtures[0]),'CHARGE_TYPE');
const baseline=packet.original.fixtures[0],external=signedSource(baseline);
let f=copy(baseline);f.clauses[0].literals[0]*=-1;
test('changed_signed_original_clause',f,external,'SOURCE_MISMATCH');
f=copy(baseline);let externalChanged=copy(external);externalChanged[0][0]*=-1;
test('changed_out_of_band_source_only',f,externalChanged,'SOURCE_MISMATCH');
f=copy(baseline);f.charges[0]='1';test('string_charge',f,external,'CHARGE_TYPE');
f=copy(baseline);f.proof[0].table^=1;test('bad_and3_table',f,external,'AND3_TABLE');
f=copy(baseline);f.proof[0].support='012';test('string_support',f,external,'AND3_SUPPORT_TYPE');
f=copy(baseline);f.proof[11].row.rhs^=1;test('false_affine_alias',f,external,'AFFINE_ALIAS');
f=copy(baseline);f.proof[0].parents[0]='unknown';test('missing_parent',f,external,'PARENT_MISSING');
f=copy(baseline);f.proof.at(-1).row.rhs=0;test('invalid_terminal',f,external,'XOR_EQUATION');
f=copy(baseline);f.proof.find(x=>x.row).row.mask='0x100000000';test('out_of_range_row',f,external,'ROW_RANGE');
const nativeTests=[
 {name:'original_unmodified_seven',packet:packet.original,expected:true},
 ...['fake582','fake583','hybrid500'].map(k=>({name:k,packet:packet[k],expected:true}))
].map(x=>({...native(x.name,x.packet),name:x.name,expected:x.expected}));
for(const x of nativeTests)assert.equal(x.accepted,x.expected,'original checker '+x.name);
const out={
 id:'LSPV-3/589',date:'2026-11-12 06:24 PST',
 scope:'Separate mathematically sound gate for archived /341 SOURCE/AND3/XOR, NOT historical full R_mix341',
 source_binding:'Exact signed ordered clause equality to independently pinned original fixture, plus global out-of-band trusted source requirement',
 pins:Object.fromEntries(Object.entries(sources).map(([k,v])=>[k,{path:v.path,git_blob:v.gitBlob,sha256:v.sha256}])),
 nativeTests,cases,summary:{strict_pass:cases.filter(c=>c.pass).length,strict_total:cases.length,native_accepted:nativeTests.filter(c=>c.accepted).length},
 theorem_scope:'If an independently trusted original signed source is supplied, strictAudit acceptance proves the clause conjunction unsatisfiable. No equivalence to historical acceptance is asserted.',
 limitations:['This strict auditor is a proposed REPAIR and independent implementation, never the historical checker','A malicious source file cannot be trusted merely because the packet itself supplied it','No external full mixed rule grammar authenticated','No superpolynomial bound or arbitrary-SAT transfer']
};
const target=path.join(root,'results/raw/arc/2026-11-12_0624_LSPV3_589_SOURCE_BOUND_SEMANTIC_GATE_NODE_RAW.json');
fs.mkdirSync(path.dirname(target),{recursive:true});
fs.writeFileSync(target,JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify({id:out.id,strict:out.summary,native:nativeTests.map(x=>({name:x.name,accepted:x.accepted,checks:x.checks})),output:path.relative(root,target)},null,2));
fs.rmSync(tmp,{recursive:true,force:true});
