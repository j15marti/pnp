#!/usr/bin/env node
'use strict';
// LSPV-3/556: counterfactual accepted-byte grammars, NOT historical R_mix341 checkers.
// The two grammars share the same mathematical Resolution rule and tariff.
const crypto = require('node:crypto');
const fs = require('node:fs');
const assert = (v,m) => { if(!v) throw Error(m || 'assertion failed'); };
let checks=0;
const ok=(v,m)=>{checks++;assert(v,m)};
const sha=(v)=>crypto.createHash('sha256').update(v).digest('hex');
const canonical=(a)=>{
  ok(Array.isArray(a),'clause not array');
  let z=[...new Set(a)];
  ok(z.length===a.length,'repeated literal');
  for(let q of z)ok(Number.isSafeInteger(q)&&q!==0,'bad literal');
  z.sort((a,b)=>Math.abs(a)-Math.abs(b)||b-a);
  ok(!z.some(x=>z.includes(-x)),'tautological clause');
  return z;
};
function parseDIMACS(src){
  ok(typeof src==='string','nonstring source');
  let lines=src.split(/\r?\n/).map(x=>x.trim()).filter(x=>x&&!x.startsWith('c'));
  ok(lines.length>0,'missing header');
  let header=lines.shift().split(/\s+/);
  ok(header.length===4&&header[0]==='p'&&header[1]==='cnf','header syntax');
  ok(header.slice(2).every(x=>/^(0|[1-9][0-9]*)$/.test(x)),'header numerics');
  const nv=Number(header[2]),nc=Number(header[3]);
  ok(Number.isSafeInteger(nv)&&Number.isSafeInteger(nc),'header bounds');
  let clauses=[],pending=[];
  for(let t of lines.join(' ').split(/\s+/).filter(Boolean)){
    ok(/^(0|-?[1-9][0-9]*)$/.test(t),'literal spelling');
    let x=Number(t);ok(Number.isSafeInteger(x)&&Math.abs(x)<=nv,'literal bound');
    if(x===0){clauses.push(canonical(pending));pending=[];}else pending.push(x);
  }
  ok(pending.length===0,'unterminated clause');
  ok(clauses.length===nc,'clause count');
  return {nv,nc,clauses};
}
const key=c=>JSON.stringify(canonical(c));
const resolve=(left,right,pivot)=>{
  ok(Number.isSafeInteger(pivot)&&pivot>0,'invalid pivot');
  const l=canonical(left),r=canonical(right);
  ok((l.includes(pivot)&&r.includes(-pivot))||(l.includes(-pivot)&&r.includes(pivot)),'not complementary');
  return canonical([...new Set([...l,...r].filter(x=>Math.abs(x)!==pivot))]);
};
function check(src,cert,opcode){
  const f=parseDIMACS(src);
  ok(cert&&typeof cert==='object'&&!Array.isArray(cert),'certificate type');
  ok(cert.source_sha256===sha(src),'original bytes not bound');
  ok(cert.source_length===Buffer.byteLength(src),'source length not bound');
  ok(Array.isArray(cert.nodes)&&cert.nodes.length>0,'proof nodes');
  const m=new Map(f.clauses.map((c,i)=>['s'+i,c]));
  let paid=new Set();
  for(const p of cert.nodes){
    ok(p.rule===opcode,'byte grammar rule mismatch');
    ok(typeof p.id==='string'&&/^d[0-9]+$/.test(p.id)&&!m.has(p.id),'fresh id');
    ok(typeof p.left==='string'&&typeof p.right==='string','parent type');
    ok(p.left!==p.right&&m.has(p.left)&&m.has(p.right),'missing/identical parent');
    ok(Array.isArray(p.clause),'derived conclusion');
    const actual=resolve(m.get(p.left),m.get(p.right),p.pivot);
    ok(key(actual)===key(p.clause),'wrong derived clause');
    m.set(p.id,actual);paid.add(p.id);
  }
  ok(cert.terminal===cert.nodes.at(-1).id,'terminal ref');
  ok(m.get(cert.terminal).length===0,'terminal not empty');
  return {accepted:true,paid_nodes:paid.size,original_source_count:f.nc};
}
function make(){
  const source=[];
  for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let c=0;c<2;c++)source.push([a?-1:1,b?-2:2,c?-3:3]);
  const dimacs='p cnf 3 8\n'+source.map(v=>v.join(' ')+' 0\n').join('');
  const m=new Map(source.map((c,i)=>['s'+i,canonical(c)]));
  const nodes=[];
  function add(left,right,pivot){const clause=resolve(m.get(left),m.get(right),pivot);const id='d'+nodes.length;nodes.push({id,rule:'RES',left,right,pivot,clause});m.set(id,clause);return id;}
  let mids=[];
  for(let i=0;i<4;i++)mids.push(add('s'+(2*i),'s'+(2*i+1),3));
  let lo=add(mids[0],mids[1],2),hi=add(mids[2],mids[3],2);
  const terminal=add(lo,hi,1);
  return {source:dimacs,proof:{source_sha256:sha(dimacs),source_length:Buffer.byteLength(dimacs),nodes,terminal}};
}
function run(){
  const {source,proof}=make();
  const A=structuredClone(proof),B=structuredClone(proof);
  B.nodes.forEach(n=>n.rule='R2');
  const a=check(source,A,'RES'),b=check(source,B,'R2');
  const negatives=[];
  function reject(label,src,p,op){let accepted=false;try{check(src,p,op);accepted=true;}catch(e){negatives.push({label,rejected:true,reason:String(e.message)});}ok(!accepted,'failed reject '+label)}
  reject('A packet in B grammar',source,A,'R2');
  reject('B packet in A grammar',source,B,'RES');
  const SAT=source.replace('p cnf 3 8','p cnf 3 7').replace('1 2 3 0\n','');
  reject('same proof against different independently supplied SAT source',SAT,A,'RES');
  let mutate=(fn)=>{let q=structuredClone(A);fn(q);return q};
  reject('forged source digest',source,mutate(p=>p.source_sha256='0'.repeat(64)),'RES');
  reject('false sink',source,mutate(p=>p.nodes.at(-1).clause=[1]),'RES');
  reject('wrong pivot',source,mutate(p=>p.nodes[0].pivot=1),'RES');
  reject('missing parent',source,mutate(p=>p.nodes[0].left='s999'),'RES');
  reject('reused paid identity',source,mutate(p=>p.nodes[1].id=p.nodes[0].id),'RES');
  reject('wrong result',source,mutate(p=>p.nodes[1].clause=[1]),'RES');
  reject('missing terminal',source,mutate(p=>p.terminal='d999'),'RES');
  reject('invalid source literal',source.replace('1 2 3 0','0 2 3 0'),A,'RES');
  let count=0;
  for(let val=0;val<8;val++)if(source.split('\n').slice(1).filter(Boolean).every(line=>line.split(' ').slice(0,3).some(l=>{let v=Number(l);return ((val>>(Math.abs(v)-1))&1)===(v>0?1:0)})))count++;
  ok(count===0,'original source should be UNSAT');
  const result={run:'LSPV-3/556',status:'PROVED/RESTRICTED conditional-grammar underdetermination + COMPUTATIONAL',date_pst:'2026-11-10 16:24 PST',source_sha256:sha(source),source_bytes:Buffer.byteLength(source),base_unsat_models:count,source_clauses:8,paid_nodes:a.paid_nodes,grammar_A:{opcode:'RES',accepted:true},grammar_B:{opcode:'R2',accepted:true},cross_grammar_rejections:2,negative_cases:negatives,assertions:checks,limitation:'Both languages are counterfactual, sound, source-bound interpretations of historically unspecified RES byte serialization; neither identifies the historical R_mix341 accepted-byte grammar.'};
  return {source,A,B,result};
}
const out=run();
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(out,null,2)+'\n');
console.log(JSON.stringify(out.result,null,2));
