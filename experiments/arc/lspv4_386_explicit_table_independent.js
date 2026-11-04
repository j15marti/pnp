'use strict';
// LSPV-4/386 independent, no-dependency TABLE evidence referee (Node 18+).
// A certificate is an ordered list of source-clause indices, one per assignment.
const assert = require('node:assert/strict');
function legal(F){
  if(!Array.isArray(F)) return false;
  let seen=new Set();
  for(const c of F){
    if(!Array.isArray(c))return false;
    for(const lit of c){
      if(!Number.isSafeInteger(lit)||lit===0)return false;
      seen.add(Math.abs(lit));
    }
  }
  for(let i=1;i<=seen.size;i++)if(!seen.has(i))return false;
  return true;
}
function satclause(c,a){
  return c.some(lit=>((a>>(Math.abs(lit)-1))&1)===(lit>0?1:0));
}
function verify(F,row){
  if(!legal(F)||!Array.isArray(row))return false;
  const n=new Set(F.flat().map(Math.abs)).size;
  if(row.length!==2**n)return false;
  return row.every((j,a)=>
    Number.isSafeInteger(j)&&j>=0&&j<F.length&&!satclause(F[j],a));
}
let checks=0,counts=[];
for(let n=1;n<=12;n++){
  const f=[[1],[-1]];
  for(let j=2;j<=n;j++)f.push([j]);
  const rows=[];
  for(let a=0;a<2**n;a++){
    const idx=f.findIndex(c=>!satclause(c,a));
    assert(idx>=0); rows.push(idx);checks++;
  }
  assert(verify(f,rows));checks++;
  assert(!verify(f,rows.slice(1)));checks++;
  assert(!verify(f,[f.length,...rows.slice(1)]));checks++;
  const sat=f.filter((_,j)=>j!==1);
  assert(sat.every(c=>satclause(c,2**n-1)));checks++;
  assert(!verify(sat,rows));checks++;
  counts.push([n,rows.length]);
}
assert(!verify([[2]], [0,0,0,0]));checks++;
assert(verify([[]],[0]));checks++;
assert(!verify([], [0]));checks++;
assert(!verify([[0]],[0]));checks++;
assert(!verify([[true]],[0]));checks++;
console.log(JSON.stringify({status:'COMPUTATIONAL',source:'independent JS',checks,failed:0,counts}));
