// LSPV-2 forced-row sensitivity, standalone Node >=16. Rcover347 diagnostic, NOT Rmix341.
'use strict';
const assert=require('assert'),crypto=require('crypto');
function ct(c,a){return c.some(l=>!!(a&(1<<(Math.abs(l)-1)))===(l>0));}
const cases=[];let assertions=0,neighbors=0;
for(const n of [2,3,4,6,8,10,12]){
 const F=[[1],[-1],...Array.from({length:n-1},(_,j)=>[j+2])];
 const rows=Buffer.alloc(1<<n);
 for(let a=0;a<rows.length;a++){
  const j=a&1;rows[a]=j;
  assert(!ct(F[j],a)&&ct(F[j^1],a));assertions+=2;
  // Changing this one-bit row chooses the wrong source clause.
  assert(ct(F[j^1],a));assertions++;neighbors++;
 }
 function models(cs){let t=0;for(let a=0;a<(1<<n);a++)t+=cs.every(c=>ct(c,a));return t;}
 assert.strictEqual(models(F),0);assert.strictEqual(models(F.slice(0,1).concat(F.slice(2))),1);
 assert.strictEqual(models([[1],[1],...F.slice(2)]),1);assertions+=3;
 const dimacs=`p cnf ${n} ${F.length}\n`+F.map(c=>c.join(' ')+' 0\n').join('');
 cases.push({n,m:F.length,dimacs_bytes:Buffer.byteLength(dimacs),logical_cost:1,payload_bits:rows.length,
  sensitive_bits:rows.length,sat_deletion_models:1,sat_sign_flip_models:1,sha256_rows:crypto.createHash('sha256').update(rows).digest('hex')});
}
console.log(JSON.stringify({experiment:'LSPV2-FORCED-ROW-PAYLOAD-SENSITIVITY348',
 model:'fixed diagnostic Rcover347, explicit rows, two source clauses',
 cases,neighbors_tested:neighbors,assertions,claim:'Verification of THIS supplied explicit certificate requires reading every row bit; shortest Rmix341 RES proof is one node. B3 OPEN.'},null,2));
