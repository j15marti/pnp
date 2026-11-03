'use strict';
// Complete finite 2-variable CNF atlas, using the ALREADY PROVED
// LSPV-2 LOW-SUPPORT343 fact W_Rmix341(F)=mu(F)-1.
// This script is not a proof-search optimizer for arbitrary Rmix proofs.
const assert=require('assert');
const CLAUSES=[];
for(const a of [-1,0,1])for(const b of [-1,0,1]){
  const clause=[];if(a)clause.push(a);if(b)clause.push(2*b);
  CLAUSES.push(clause);
}
const sat=F=>{
  for(let a=0;a<4;a++)
    if(F.every(C=>C.some(x=>Boolean(a&(1<<(Math.abs(x)-1)))===(x>0))))
      return true;
  return false;
};
function minimumCore(F){
  for(let k=1;k<=F.length;k++){
    const selected=[];
    function find(start){
      if(selected.length===k)return !sat(selected)?selected.slice():null;
      for(let i=start;i<=F.length-(k-selected.length);i++){
        selected.push(F[i]);
        const ans=find(i+1);selected.pop();
        if(ans)return ans;
      }
      return null;
    }
    const found=find(0);if(found)return found;
  }
  return null;
}
const enc=F=>{
  const vars=Math.max(0,...F.flat().map(Math.abs));
  return 'p cnf '+vars+' '+F.length+'\n'+F.map(C=>C.join(' ')+(C.length?' ':'')+'0\n').join('');
};
const all=[],mus=[],hist={};let checks=0,satCount=0;
for(let mask=0;mask<512;mask++){
  const F=CLAUSES.filter((c,i)=>Boolean(mask&(1<<i)));
  if(sat(F)){satCount++;continue;}
  const U=minimumCore(F);
  assert(U && !sat(U));checks++;
  assert(U.every((_,i)=>sat(U.filter((_,j)=>j!==i))));checks++;
  const isMUS=F.every((_,i)=>sat(F.filter((_,j)=>i!==j)));
  const N=Buffer.byteLength(enc(F)),w=U.length-1;
  assert(Buffer.byteLength(enc(U))<=N);checks++;
  assert(w<=3**Math.max(0,U.length-1));checks++;
  all.push([N,w]);if(isMUS)mus.push([N,w]);
  hist[U.length]=(hist[U.length]||0)+1;
}
const maxbytes=Math.max(...all.map(x=>x[0]));
for(let N=0;N<=maxbytes;N++){
  const maxW=rows=>Math.max(0,...rows.filter(row=>row[0]<=N).map(row=>row[1]));
  assert.equal(maxW(all),maxW(mus));checks++;
}
assert.equal(CLAUSES.length,9);
assert.equal(all.length,417);assert.equal(satCount,95);
assert.equal(mus.length,12);assert.equal(maxbytes,58);
assert.deepStrictEqual(hist,{'1':256,'2':112,'3':48,'4':1});
assert(sat([[1]]));assert(!sat([[1],[-1]]));
assert(sat([[1],[1]]));assert(!sat([[]]));
checks+=4;
const strict=s=>{
  const L=s.split('\n').filter((x,i,a)=>i<a.length-1||x!=='');
  if(!L.length)return false;
  const H=L[0].trim().split(/\s+/);
  if(H.length!==4||H[0]!=='p'||H[1]!=='cnf')return false;
  const n=Number(H[2]),m=Number(H[3]);
  if(!Number.isSafeInteger(n)||n<0||!Number.isSafeInteger(m)||m!==L.length-1)return false;
  for(const row of L.slice(1)){
    const toks=row.trim().split(/\s+/).map(Number);
    if(toks.some(x=>!Number.isSafeInteger(x))||toks[toks.length-1]!==0
        ||toks.slice(0,-1).includes(0)||toks.slice(0,-1).some(x=>Math.abs(x)>n))return false;
  }
  return true;
};
const malformed=['p cnf 2 1\n1 -2\n','p cnf 2 2\n1 0\n',
                 'p cnf 2 1\n3 0\n','p cnf 2 1\n0 0\n'];
assert(malformed.every(x=>!strict(x)));
assert(strict('p cnf 1 2\n1 0\n-1 0\n'));
console.log(JSON.stringify({status:'PASS',all_sources:512,sat:satCount,unsat:all.length,
  mus:mus.length,mu_histogram:hist,max_W:Math.max(...all.map(x=>x[1])),
  max_source_bytes:maxbytes,budgets:maxbytes+1,assertions:checks,
  malformed_rejections:malformed.length},null,2));
