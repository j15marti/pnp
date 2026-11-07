#!/usr/bin/env node
// LSPV-3/464 public mini-replay. Node >= 18; uses only built-ins.
// The complete *independent* XLRUP semantics checker is in the conversation archive.
// This code reproduces the original 3-CNF and typed certificate strings; it is
// not an invocation of either historical Rmix341 or the official cake_xlrup binary.
"use strict";
const fs=require('fs'),crypto=require('crypto'),assert=require('assert'),path=require('path');
function gen(h,edges) {
  edges=edges.map(([a,b])=>a<b?[a,b]:[b,a]).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
  let cnf=[],even=[],lines=[];
  for(let v=0;v<h;v++) {
    const vars=edges.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean).sort((a,b)=>a-b);
    assert.equal(vars.length,3);
    const start=cnf.length+1,charge=v===0?1:0;
    for(let b=0;b<8;b++) {
      const bits=[b>>2&1,b>>1&1,b&1],par=bits[0]^bits[1]^bits[2];
      const clause=vars.map((x,i)=>bits[i]?-x:x);
      if(par!==charge)cnf.push(clause);if(par!==0)even.push(clause);
    }
    const literals=[...vars];if(!charge)literals[0]=-literals[0];
    lines.push('i x '+(v+1)+' '+literals.join(' ')+' 0 '+[start,start+1,start+2,start+3].join(' ')+' 0');
  }
  lines.push('x '+(h+1)+' 0 '+Array.from({length:h},(_,i)=>i+1).join(' ')+' 0');
  lines.push('i cx '+(cnf.length+1)+' 0 '+(h+1)+' 0');
  function dim(c) {return 'p cnf '+edges.length+' '+c.length+'\n'+c.map(x=>x.join(' ')+' 0\n').join('')}
  return {src:dim(cnf),even:dim(even),cert:lines.join('\n')+'\n',n:edges.length,cnf,evenClauses:even};
}
const specs={
  K4:[4,Array.from({length:4},(_,i)=>Array.from({length:3-i},(_,j)=>[i,i+j+1])).flat()],
  K33:[6,Array.from({length:3},(_,i)=>Array.from({length:3},(_,j)=>[i,j+3])).flat()],
  PRISM4:[8,[...Array.from({length:4},(_,i)=>[i,(i+1)%4]),...Array.from({length:4},(_,i)=>[i+4,4+(i+1)%4]),...Array.from({length:4},(_,i)=>[i,i+4])]]
};
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const hashes={K4:'ea08104837e167b9ebd06d8f50442d828e3ba4d81f79dff8c14a09ba30050096',
 K33:'96a09b484af2033b3fbf5af778640abd04f7c5a3a7e7a52a29813263aa1575e6',
 PRISM4:'e976647b16978d5848ba71e727e45809958c0ef10691268463b13cfe65eaf290'};
let assertions=0;
for(const [name,[h,edges]] of Object.entries(specs)) {
  const z=gen(h,edges),base=path.join(__dirname,'../../results/raw/arc/lspv3_464_'+name);
  for(const [ext,want] of [['.cnf',z.src],['.xlrup',z.cert],['.even.cnf',z.even]]) {
    assert.equal(fs.readFileSync(base+ext,'utf8'),want);assertions++;
  }
  assert.equal(sha(z.src),hashes[name]);assertions++;
  const count=c=>Array.from({length:1<<z.n},(_,a)=>c.every(cl=>cl.some(l=>(((a>>(Math.abs(l)-1))&1)===Number(l>0))))).filter(Boolean).length;
  assert.equal(count(z.cnf),0);assertions++;
  assert.equal(count(z.evenClauses),1<<(z.n-h+1));assertions++;
  for(let i=0;i<z.cnf.length;i++) {
    let found=false;
    for(let a=0;a<(1<<z.n);a++){
      const evalClause=cl=>cl.some(l=>((a>>(Math.abs(l)-1))&1)===Number(l>0));
      if(!evalClause(z.cnf[i])&&z.cnf.every((cl,j)=>j===i||evalClause(cl))){found=true;break}
    }
    assert(found);assertions++;
  }
  console.log(name,'original clauses:',z.cnf.length,'external records:',h+2,'historical semantic minimum:',4*h-1);
}
console.log('PASS: replay and source-deletion assertions',assertions);
