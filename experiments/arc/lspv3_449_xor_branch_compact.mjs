// LSPV-3/449 compact source-authenticated affine branch discharge control.
// node experiments/arc/lspv3_449_xor_branch_compact.mjs
// Restricted declared semantic R_mix341 AND3/XOR subcalculus; NOT historical byte checker.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
const E=[[0,1],[0,2],[1,2],[2,3],[3,4],[3,5],[4,5]],chi=[1,0,0,0,0,0];
const bridge=4, rows=[],source=[];
let lines=['c LSPV3 449 original 6-vertex two-triangle bridge Tseitin CNF','p cnf 7 16'];
const table=(vars,fn)=>{let s=''; for(let k=0;k<1<<vars.length;k++){const a={};vars.forEach((v,j)=>a[v]=(k>>(vars.length-1-j))&1);s+=fn(a)?'1':'0';}return s;};
const parity=(vars,a)=>vars.reduce((x,v)=>x^a[v],0);
const clause=(lits,a)=>lits.some(l=>a[Math.abs(l)]===(l>0?1:0));
let andCount=0;
for(let v=0;v<6;v++){
 const vars=E.flatMap((e,i)=>e.includes(v)?[i+1]:[]);
 const factors=[];
 for(let k=0;k<1<<vars.length;k++){
  const bits=vars.map((_,j)=>(k>>(vars.length-1-j))&1);
  if(bits.reduce((x,b)=>x^b,0)!==chi[v]){
   const lits=vars.map((x,j)=>bits[j]?-x:x);
   factors.push(table(vars,a=>clause(lits,a)));
   source.push(lits); lines.push(lits.join(' ')+' 0');
  }
 }
 let out=factors[0];
 for(const f of factors.slice(1)){out=[...out].map((x,i)=>x==='1'&&f[i]==='1'?'1':'0').join('');andCount++;}
 assert.equal(out,table(vars,a=>parity(vars,a)===chi[v]));
 rows[v]={mask:vars.reduce((s,i)=>s|(1<<(i-1)),0),rhs:chi[v]};
}
const dimacs=lines.join('\n')+'\n',hash=createHash('sha256').update(dimacs).digest('hex');
assert.equal(hash,'a0df281786bdde3acd0d819c6814ef55597bf54c51a6fe946d184617747ec76e');
assert.equal(Buffer.byteLength(dimacs),205);assert.equal(source.length,16);assert.equal(andCount,10);
let nModels=0;for(let m=0;m<128;m++){const a={};for(let i=1;i<=7;i++)a[i]=(m>>(i-1))&1;if(source.every(s=>clause(s,a)))nModels++;}
assert.equal(nModels,0);
const xor=(a,b)=>({mask:a.mask^b.mask,rhs:a.rhs^b.rhs});
const arm=(indices,assume)=>{let r=xor(rows[indices[0]],rows[indices[1]]);r=xor(r,rows[indices[2]]);const before=r;r=xor(r,{mask:1<<(bridge-1),rhs:assume});assert.deepEqual(r,{mask:0,rhs:1});assert.deepEqual(before,{mask:1<<(bridge-1),rhs:1-assume});return before;};
const left=arm([0,1,2],0),right=arm([3,4,5],1);
assert.deepEqual(xor(left,right),{mask:0,rhs:1});
console.log(JSON.stringify({status:'accepted',source_sha256:hash,source_clauses:source.length,source_assignments:128,source_models:nModels,paid_AND3:10,paid_XOR:5,total_paid:15,concurrent_weighted_span:6,native_byte_checker:false}));
