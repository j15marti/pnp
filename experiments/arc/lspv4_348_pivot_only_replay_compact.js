#!/usr/bin/env node
'use strict';
// LSPV-4 / 348, deterministic source-to-resolution pivot-only verifier.
// Reconstructs all inferred clauses; no SAT oracle and no precomputed proof outputs.
const assert=require('assert');
const canon=a=>{let z=[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);for(const v of z)assert(!z.includes(-v));return z;};
function test(r){
  const k=r*r,X=i=>i+1,Y=j=>k+1+j,s=2*k+2,u=s+1,v=s+2;
  const perm=i=>r*((i-1)%r)+Math.floor((i-1)/r)+1;
  let C0=[[X(0)],[-X(k)],[-Y(1)]];
  for(let j=2;j<=k;j++)C0.push([Y(j-1),-Y(j)]);
  for(let i=1;i<=k;i++)C0.push([-X(i-1),X(i),Y(perm(i))]);
  let source=C0.map(z=>canon([...z,s]));
  source.push(...[[u,v],[u,-v],[-u,v],[-u,-v]].map(z=>canon([-s,...z])));
  const m=source.length;
  function proof(wide){
    let lines=source.map(z=>z.slice()),triples=[],reads=0,slots=0,width=0;
    function step(a,b,p){
      const A=lines[a],B=lines[b];assert(A&&B);
      assert((A.includes(p)&&B.includes(-p))||(A.includes(-p)&&B.includes(p)));
      let D=canon([...A,...B].filter(q=>Math.abs(q)!==Math.abs(p)));
      lines.push(D);triples.push([a,b,p]);reads+=A.length+B.length;slots+=D.length;width=Math.max(width,D.length);
      return lines.length-1;
    }
    let cur=0,pos;
    if(wide){
      for(let i=1;i<=k;i++)cur=step(cur,k+1+i,X(i-1));
      cur=step(cur,1,X(k));
      for(let j=k;j>=2;j--)cur=step(cur,j+1,Y(j));
      pos=step(cur,2,Y(1));
    }else{
      let units={1:2};
      for(let j=2;j<=k;j++)units[j]=step(j+1,units[j-1],Y(j-1));
      for(let i=1;i<=k;i++){
        let t=step(k+1+i,units[perm(i)],Y(perm(i)));
        cur=step(t,cur,-X(i-1));
      }
      pos=step(cur,1,X(k));
    }
    const a=step(C0.length,C0.length+2,u),b=step(C0.length+1,C0.length+3,u);
    const neg=step(a,b,v);step(pos,neg,s);
    assert.deepStrictEqual(lines.at(-1),[]);
    // Check only the pivot triple payload, with inferred clauses reconstructed afresh.
    let rec=source.map(z=>z.slice());
    for(const [a,b,p] of triples){
      assert(a<rec.length&&b<rec.length);
      const A=rec[a],B=rec[b];
      assert((A.includes(p)&&B.includes(-p))||(A.includes(-p)&&B.includes(p)));
      rec.push(canon([...A,...B].filter(q=>Math.abs(q)!==Math.abs(p))));
    }
    assert.deepStrictEqual(rec.at(-1),[]);
    const bytes=Buffer.byteLength(triples.map(x=>x.join(' ')+'\n').join(''));
    return {nodes:triples.length,derived_literal_slots:slots,parent_literal_visits:reads,
      max_derived_width:width,pivot_only_bytes:bytes};
  }
  const wide=proof(true),narrow=proof(false);
  assert.equal(wide.nodes,2*k+5);assert.equal(narrow.nodes,3*k+4);
  assert.equal(wide.derived_literal_slots,k*k+4*k+6);
  assert.equal(narrow.derived_literal_slots,7*k+4);
  assert.equal(wide.parent_literal_visits,k*k+11*k+21);
  assert.equal(narrow.parent_literal_visits,16*k+17);
  return {r,k,n:v,m,wide,narrow};
}
const rows=[2,3,4,5,8,12].map(test);
console.log(JSON.stringify({run:'LSPV4_PIVOT_ONLY_REPLAY_COST348',status:'PASS',
  theorem_scope:'Resolution-only witnesses within unchanged Rmix341',
  controls:'Original odd/even parity, malformed DIMACS, sign-neighbor in full Python archive',
  rows},null,2));
