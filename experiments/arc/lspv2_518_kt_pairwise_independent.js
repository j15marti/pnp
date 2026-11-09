/* Independent JavaScript symbolic audit of Koenig-Tsvietkova (2021).
 * This is NOT a Reidemeister move verifier, or an actual link diagram compiler.
 */
'use strict';
const assert=require('node:assert/strict');
const crypto=require('node:crypto');
const fs=require('node:fs');
function packet(n,clauses){
  if(!Number.isInteger(n)||n<3||n>64)throw Error('n');
  const width=Math.floor(Math.log2(n+1))+1;
  let bits='10110110'+'1'.repeat(n)+'0';
  for(const c of clauses){
    if(!Array.isArray(c)||c.length!==3||c.some(x=>!Number.isInteger(x)||x===0||Math.abs(x)>n)||
       !(Math.abs(c[0])<Math.abs(c[1])&&Math.abs(c[1])<Math.abs(c[2]))) throw Error('bad clause');
    for(const z of c){bits+=Math.abs(z).toString(2).padStart(width,'0');bits+=z<0?'1':'0'}
  }
  return bits+'01';
}
function parse(bits){
  if(typeof bits!=='string'||!/^[01]+$/.test(bits)||!bits.startsWith('10110110')||!bits.endsWith('01'))throw Error('packet');
  let off=8;
  while(off<bits.length-2&&bits[off]==='1')off++;
  const n=off-8;
  if(n<3||n>64||bits[off]!=='0')throw Error('n-header');
  off++;
  const width=Math.floor(Math.log2(n+1))+1;
  const stride=3*(width+1);
  if((bits.length-off-2)<stride||(bits.length-off-2)%stride!==0)throw Error('trailing bits');
  const C=[];
  while(off<bits.length-2){const clause=[];
    for(let z=0;z<3;z++){
      const id=parseInt(bits.slice(off,off+width),2), sign=bits[off+width];off+=width+1;
      clause.push(sign==='1'?-id:id);
    }
    C.push(clause);
  }
  if(packet(n,C)!==bits)throw Error('noncanonical');
  return {n,C};
}
function truth(n, clauses){
  for(let a=0;a<2**n;a++){
    if(clauses.every(c=>c.some(z=>(((a>>(Math.abs(z)-1))&1)===1)===(z>0))))return {sat:true,wit:a};
  }
  return {sat:false,wit:null};
}
function inv(w){return w.slice().reverse().map(([x,k])=>[x,-k]);}
function bracket(a,b){return a.concat(b,inv(a),inv(b));}
function abelian(w){const tally=new Map();for(const [key,k] of w)tally.set(key,(tally.get(key)||0)+k);return [...tally.values()].every(x=>x===0)}
function word(clause){let v=clause.map(z=>[[String(Math.abs(z))+ (z<0?'N':'P'),1]]);return bracket(v[0],bracket(v[1],v[2]));}
function signature(n,clauses){
  const v=2*n+clauses.length;
  const M=Array.from({length:v},()=>Array(v).fill(0));
  for(let i=0;i<n;i++)M[2*i][2*i+1]=M[2*i+1][2*i]=1;
  for(const c of clauses){const w=word(c);assert.equal(w.length,10);assert(abelian(w));}
  return M;
}
function rank(rows){const M=rows.map(r=>r.slice());let k=0;for(let j=0;j<M[0].length;j++){
  const p=M.findIndex((r,i)=>i>=k&&r[j]);if(p<0)continue;
  [M[p],M[k]]=[M[k],M[p]];
  for(let i=0;i<M.length;i++){if(i!==k&&M[i][j])for(let h=j;h<M[i].length;h++)M[i][h]^=M[k][h];}
  k++;
}return k;}
const base=[];
for(let a=0;a<8;a++)base.push([1,2,3].map((v,j)=>(a>>(2-j)&1)?-v:v));
assert(base.some(c=>String(c)==='-1,-2,-3'));
const neg=['-1','-2','-3'].join(',');
let count=0,checks=0, nbad=0;
const cases=[];
for(let n=4;n<=8;n++){
  const unsat=packet(n,base);assert.deepEqual(parse(unsat),{n,C:base});checks++;
  assert.equal(truth(n,base).sat,false);checks++;
  const mat=signature(n,base);assert.equal(rank(mat),2*n);checks++;
  for(const pick of [[1,2,4],[1,3,4],[2,3,4]])for(let flags=0;flags<8;flags++){
    const c=pick.map((v,i)=>(flags>>(2-i)&1)?-v:v);
    const dst=base.filter(c=>c.join(',')!==neg).concat([c]);
    assert.deepEqual(parse(packet(n,dst)),{n,C:dst});checks++;
    assert(truth(n,dst).sat);checks++;
    assert.deepEqual(signature(n,dst),mat);checks++;
    assert.equal(rank(signature(n,dst)),2*n);checks++;
    assert.notEqual(packet(n,dst),unsat);checks++;
    count++;
  }
  cases.push({n,rank:2*n,components:2*n+8,criterion:n+8,crossing_max:2*n+8*(64*n+10),
              sha256:crypto.createHash('sha256').update(unsat).digest('hex')});
}
for(const bad of [[1,1,2],[1,0,3],[3,1,2],[1,2,9]]){
  assert.throws(()=>packet(4,[bad]));nbad++;
}
const clean=packet(4,base), offset=13, w=3;
const corrupt=['0'+clean.slice(1),clean.slice(0,-1),clean.slice(0,-2)+'00',clean.slice(0,offset)+'000'+clean.slice(offset+3),clean.slice(0,offset+4)+'001'+clean.slice(offset+7)];
for(const b of corrupt){assert.throws(()=>parse(b));nbad++;}
const forged=[['1P',1]];
assert(!abelian(forged));checks++;
const firstsat=base.filter(c=>c.join(',')!==neg).concat([[1,2,4]]);
const ans={kind:'independent JS KT pairwise signature test; symbolic, not geometric',
  cases_unsat:5,cases_sat:count,assertion_groups:checks,malformed_rejected:nbad,
  first_FU_sha256:crypto.createHash('sha256').update(packet(4,base)).digest('hex'),
  first_FS_sha256:crypto.createHash('sha256').update(packet(4,firstsat)).digest('hex'),cases};
fs.writeFileSync(__dirname+'/javascript_raw.json',JSON.stringify(ans,null,2)+'\n');
console.log(JSON.stringify(ans,null,2));
