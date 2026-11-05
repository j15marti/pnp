#!/usr/bin/env node
// Independent finite oracle for LSPV4/413. NOT an implementation of a logspace TM.
import fs from 'node:fs';
import crypto from 'node:crypto';
let x=JSON.parse(fs.readFileSync(process.argv[2]||'results/raw/arc/2026-11-05_0540_LSPV4_413_LOGSPACE_PADDING.json','utf8'));
let checks=0,mutations=0;
function canon(v) {
 if(Array.isArray(v))return '['+v.map(canon).join(',')+']';
 if(v!==null&&typeof v==='object')return '{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+canon(v[k])).join(',')+'}';
 return JSON.stringify(v);
}
let src={nvars:1,clauses:[[1],[-1]]};
let doc={format:'Rmix341-CANON2',source:src,
 source_sha256:crypto.createHash('sha256').update(canon(src)).digest('hex'),
 nodes:[{id:0,rule:'RES',left:{src:0,view:'clause'},right:{src:1,view:'clause'},pivot:1,clause:[]}],
 final:{node:0,view:'clause'}};
function resolvents(a,b,p) {
 let out=[];
 for(let v of [p,-p])if(a.includes(v)&&b.includes(-v)){
  let t=[...new Set([...a.filter(y=>y!==v),...b.filter(y=>y!==-v)])].sort((u,w)=>Math.abs(u)-Math.abs(w)||Number(u<0)-Number(w<0));
  if(!out.some(k=>JSON.stringify(k)===JSON.stringify(t)))out.push(t);
 }
 return out;
}
function valid(d) {
 if(d.format!=='Rmix341-CANON2'||canon(d.source)!==canon(src))return false;
 if(d.source_sha256!==crypto.createHash('sha256').update(canon(src)).digest('hex'))return false;
 if(d.nodes.length!==1||d.final.node!==0||d.final.view!=='clause')return false;
 let r=d.nodes[0];
 return r.id===0&&r.rule==='RES'&&r.pivot===1&&r.left.src===0&&r.right.src===1&&r.clause.length===0&&resolvents([1],[-1],1).some(k=>k.length===0);
}
let base=canon(doc);
if(base.length!==x.canonical_proof_bytes)throw Error('base length');checks++;
for(let row of x.padding_cases){
 let raw=base.slice(0,-1)+' '.repeat(row.padding)+'}';
 if(raw.length!==row.raw_bytes||!valid(JSON.parse(raw)))throw Error('valid case');checks++;
 for(let j=0;j<row.padding;j++){
  let pos=base.length-1+j,bad=raw.slice(0,pos)+'#'+raw.slice(pos+1);
  let rejected=false;try{JSON.parse(bad)}catch(e){rejected=true}
  if(!rejected)throw Error('corrupt byte missed');checks++;mutations++;
 }
}
if(JSON.stringify(resolvents([1,-1,-2],[1],1))!==JSON.stringify([[1,-2]]))throw Error('RES1');checks++;
if(JSON.stringify(resolvents([1,-1,2],[1],1))!==JSON.stringify([[1,2]]))throw Error('RES2');checks++;
if(valid({...doc,source:{nvars:1,clauses:[[1]]}}))throw Error('source forgery');checks++;
if(valid({...doc,source_sha256:'0'.repeat(64)}))throw Error('hash forgery');checks++;
if(mutations!==x.mutation_rejections)throw Error('mutations');checks++;
function next(s){
 let a=s.split(''),i=a.length-1,carry=1;
 while(i>=0&&carry){let z=a[i].charCodeAt(0)-48+carry;a[i]=String(z%10);carry=Math.floor(z/10);i--}
 if(carry)a.unshift('1');return a.join('');
}
if(next('9'.repeat(20000))!=='1'+'0'.repeat(20000))throw Error('large ID');checks++;
for(let i=1;i<=500;i++){if(BigInt(next(String(i)))!==BigInt(i)+1n)throw Error('ID+1');checks++}
console.log(JSON.stringify({PASS:true,checks,mutations,source_bytes:canon(src).length,base_bytes:base.length,
 caveat:'Node JSON buffers certificate; no FLMV or logspace measurement'}));
