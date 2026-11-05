#!/usr/bin/env node
// LSPV-4/414 finite independent valid-source-byte read-sensitivity controls.
// Node v18+, no dependencies, seed-free exhaustive comment-byte mutations.
// This tests the exact-source condition, NOT the full native Rmix341 checker.
const assert=require('assert'),crypto=require('crypto');
let checks=0;const check=x=>{assert(x);checks++};
const parse=s=>{
 const lines=s.split(/\r\n|\n|\r/).map(x=>x.trim()).filter(Boolean);
 let h=null,c=[];
 for(const l of lines){
  if(l==='c'||/^c\s/.test(l))continue;
  const w=l.split(/\s+/);
  if(!h){if(w[0]!=='p'||w[1]!=='cnf'||w.length!==4)throw Error('header');h=[+w[2],+w[3]];continue}
  if(w.at(-1)!=='0'||w.slice(0,-1).includes('0'))throw Error('terminator');
  let a=w.slice(0,-1).map(Number);
  if(a.some(x=>!Number.isInteger(x)||x===0||Math.abs(x)>h[0]))throw Error('literal');
  c.push([...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||(x<0?1:0)-(y<0?1:0)));
 }
 if(!h||c.length!==h[1])throw Error('count');
 return JSON.stringify({nvars:h[0],clauses:c});
};
function exact(original,wrapper){
 return Buffer.from(wrapper.raw,'base64').toString('base64')===wrapper.raw
  &&Buffer.from(wrapper.raw,'base64').equals(Buffer.from(original))
  &&crypto.createHash('sha256').update(original).digest('hex')===wrapper.hash
  &&parse(original)===wrapper.parsed;
}
for(const m of [1,8,64,256]){
 const tail='\np cnf 1 2\n1 0\n-1 0\n';
 const original='c '+'a'.repeat(m)+tail;
 const wrapper={raw:Buffer.from(original).toString('base64'),
 hash:crypto.createHash('sha256').update(original).digest('hex'),parsed:parse(original)};
 check(exact(original,wrapper));
 for(let j=0;j<m;j++){
  const other='c '+'a'.repeat(j)+'b'+'a'.repeat(m-j-1)+tail;
  check(parse(other)===wrapper.parsed);
  check(!exact(other,wrapper));
 }
}
const a='p cnf 2 3\n2 1 0\n1 0\n-1 0\n',b='c other comment\np cnf 2 3\n1 2 0\n1 0\n-1 0\n';
check(parse(a)===parse(b));check(a!==b);
const code='eA==',alias='eB==';check(Buffer.from(code,'base64').equals(Buffer.from(alias,'base64')));check(Buffer.from(alias,'base64').toString('base64')!==alias);
console.log(JSON.stringify({PASS:true,checks,comment_mutations:329,scope:'raw-source-auth-only',B3:'OPEN'}));
