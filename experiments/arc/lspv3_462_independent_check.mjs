#!/usr/bin/env node
'use strict';
/* Independently reconstructed LSPV-3/462 finite checker.
 * Usage: node script.mjs fixture_r1_d7.json fixture_r2_d5.json fixture_r3_d4.json
 * This is not the authoritative historical R_mix341 checker. */
import fs from 'node:fs'; import crypto from 'node:crypto'; import assert from 'node:assert';
let checks=0, rejected=0;
function ok(v,s){assert(v,s);checks++;}
function canonical(v){if(Array.isArray(v))return '['+v.map(canonical).join(',')+']';
 if(v!==null && typeof v==='object')return '{'+Object.keys(v).sort().map(k=>JSON.stringify(k)+':'+canonical(v[k])).join(',')+'}';
 return JSON.stringify(v);}
const h=s=>crypto.createHash('sha256').update(s).digest('hex');
const xor=bs=>bs.reduce((a,b)=>a^b,0);
const normalized=c=>[...c].sort((a,b)=>Math.abs(a)-Math.abs(b)||b-a);
const sat=(c,a)=>c.some(l=>l>0 ? a[l-1]===1:a[-l-1]===0);
const bitseq=n=>Array.from({length:(1<<n)},(_,j)=>Array.from({length:n},(_,k)=>(j>>k)&1));
function forb(vars,bits){return normalized(vars.map((v,k)=>bits[k]?-v:v));}
function eq(x,y){return canonical(x)===canonical(y);}
function eqMulti(x,y){return x.length===y.length && x.map(canonical).sort().join('|')===y.map(canonical).sort().join('|');}
function reconstruct(r,d,rhs){
 const flat=[],strict=[],gates=[];let next=r*d+1;
 for(let j=0;j<r;j++){
   const orig=Array.from({length:d},(_,k)=>j*d+k+1);
   for(const a of bitseq(d))if(xor(a)!==rhs[j])flat.push(forb(orig,a));
   let chain=[...orig];
   for(let t=0;t<d-3;t++){
     const [x,y]=chain,z=next++;
     gates.push({out:z,inputs:[x,y],block:j});
     for(const a of bitseq(3))if(a[2] !== (a[0]^a[1]))strict.push(forb([x,y,z],a));
     chain=[z,...chain.slice(2)];
   }
   for(const a of bitseq(3))if(xor(a)!==rhs[j])strict.push(forb(chain,a));
 }
 return {flat,strict,gates,vars:next-1};
}
function verify(doc){
 const {r,d,rhs}=doc;
 ok(Number.isInteger(r)&&r>0&&r<=3,'r');ok(Number.isInteger(d)&&d>=3&&d<=9,'d');
 ok(rhs.length===r&&rhs.every(x=>x===0||x===1),'rhs');
 const x=reconstruct(r,d,rhs);
 ok(eqMulti(doc.flat_clauses,x.flat),'all flat clauses from original bit truth tables');
 ok(eqMulti(doc.strict3_clauses,x.strict),'all compact strict3 clauses from XOR truth tables');
 ok(eq(doc.gates,x.gates),'fresh XOR defs');
 ok(doc.original_variables===r*d,'original count');
 ok(doc.total_compact_variables===x.vars,'fresh auxiliary count');
 ok(doc.flat_clause_count===r*(1<<(d-1)),'flat count');
 ok(doc.strict3_clause_count===4*r*(d-2),'compact count');
 ok(doc.gate_count===r*(d-3),'aux count');
 ok(doc.strict3_clauses.every(c=>c.length===3 && c.every(x=>x!==0) && new Set(c.map(Math.abs)).size===3),'proper width3');
 const canon=canonical({r,d,rhs,flat:doc.flat_clauses,strict3:doc.strict3_clauses,gates:doc.gates});
 ok(doc.source_sha256===h(canon),'source hash');
 let correct=0;
 for(const a of bitseq(r*d)){
   const want=Array.from({length:r},(_,j)=>xor(a.slice(j*d,(j+1)*d))===rhs[j]).every(Boolean);
   const ac=[...a];for(const g of doc.gates){let [u,v]=g.inputs;ac[g.out-1]=ac[u-1]^ac[v-1];}
   ok(doc.flat_clauses.every(c=>sat(c,a))===want,'flat exact equivalence');
   ok(doc.strict3_clauses.every(c=>sat(c,ac))===want,'compact unique-extension exact equivalence');
   if(want)correct++;
 }
 ok(correct===(1<<(r*(d-1))),'sat count');
 for(let t=0;t<doc.flat_clauses.length;t++){
   const c=doc.flat_clauses[t], v=Array(r*d).fill(0);
   for(let j=0;j<r;j++){const start=j*d;v[start+d-1]=rhs[j];}
   const j=Math.floor((Math.abs(c[0])-1)/d);
   for(const lit of c)v[Math.abs(lit)-1]=lit>0?0:1;
   ok(!sat(c,v),'witness falsifies own clause');
   ok(doc.flat_clauses.every((cl,k)=>k===t||sat(cl,v)),'all other canonical clauses true');
 }
 return {r,d,checks,flat:doc.flat_clause_count,compact:doc.strict3_clause_count};
}
const paths=process.argv.slice(2);ok(paths.length>0,'fixture files');
let outputs=[];
for(const path of paths){const orig=JSON.parse(fs.readFileSync(path,'utf8'));outputs.push(verify(orig));
 for(const name of ['flip','missing','reuse','hash','rhs']){
   const d=JSON.parse(JSON.stringify(orig));
   if(name==='flip')d.flat_clauses[0][0]*=-1;
   else if(name==='missing')d.strict3_clauses.pop();
   else if(name==='reuse')d.gates.length?d.gates[0].out=d.gates[0].inputs[0]:d.total_compact_variables++;
   else if(name==='hash')d.source_sha256='00'.repeat(32);
   else d.rhs[0]^=1;
   try {verify(d);throw Error('failed rejection '+name)}
   catch(e){if(String(e.message).includes('failed rejection'))throw e;rejected++;}
 }
}
console.log(JSON.stringify({schema:'LSPV3/462/independent-v1',cases:outputs,assertions:checks,
 negative_controls_rejected:rejected,status:'COMPUTATIONAL; not authoritative historical R_mix341 checker'},null,2));
