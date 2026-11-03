#!/usr/bin/env node
'use strict';
/* GUARD-SUM-EXACT350: standalone proof-producing family, independent of SAT libraries.
   Node >=16: node experiments/arc/lspv3_349_guarded_sum_compact.js */
const assert=require('assert');
const canon=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
function build(r){
  assert(r>=2&&Number.isInteger(r));const k=r*r;
  const X=i=>i+1,Y=j=>k+1+j, s=2*k+2,u=s+1,v=s+2;
  const pi=i=>r*((i-1)%r)+Math.floor((i-1)/r)+1;
  let F=[[X(0)],[-X(k)],[-Y(1)]];
  for(let j=2;j<=k;j++)F.push([Y(j-1),-Y(j)]);
  for(let i=1;i<=k;i++)F.push([-X(i-1),X(i),Y(pi(i))]);
  const mF=F.length;
  const clauses=F.map(c=>canon([...c,s]));
  clauses.push(...[[u,v],[u,-v],[-u,v],[-u,-v]].map(c=>canon([-s,...c])));
  const m=clauses.length;let derived=[];
  const get=i=>i<m?clauses[i]:derived[i-m].clause;
  function res(a,b,p){
    const A=get(a),B=get(b);
    assert((A.includes(p)&&B.includes(-p))||(A.includes(-p)&&B.includes(p)));
    const C=canon([...A,...B].filter(t=>Math.abs(t)!==Math.abs(p)));
    assert(C.every(t=>!C.includes(-t)));
    derived.push({a,b,pivot:p,clause:C});
    return m+derived.length-1;
  }
  // Source-once exact-optimal proof: first collect all y literals in one clause,
  // then use the y implications in REVERSE order to eliminate each exactly once.
  let cur=0;
  for(let i=1;i<=k;i++)cur=res(cur,k+1+i,X(i-1));
  cur=res(cur,1,X(k));
  assert.deepStrictEqual(get(cur),canon([s,...Array.from({length:k},(_,j)=>Y(j+1))]));
  for(let j=k;j>=2;j--)cur=res(cur,j+1,Y(j));
  const pos_s=res(cur,2,Y(1));
  const left=res(mF,mF+2,u),right=res(mF+1,mF+3,u);
  const neg_s=res(left,right,v);
  const root=res(pos_s,neg_s,s);
  assert.deepStrictEqual(get(root),[]);
  assert.equal(derived.length,m-1);
  assert.equal(m,2*k+6);
  // Every source and every non-root derived node occurs as a named premise ONCE.
  const refs=Array(m+derived.length).fill(0);
  for(const d of derived){refs[d.a]++;refs[d.b]++;}
  assert(refs.slice(0,m).every(v=>v===1));
  assert(refs.slice(m,-1).every(v=>v===1));
  assert.equal(refs.at(-1),0);
  const literalSlots=derived.reduce((n,d)=>n+d.clause.length,0);
  assert.equal(literalSlots,k*k+4*k+6);
  const dimacs='p cnf '+v+' '+m+'\n'+clauses.map(c=>c.join(' ')+' 0\n').join('');
  return {r,n:v,m,s,u,v,clauses,derived,dimacs,literalSlots};
}
const sat=(C,a)=>C.every(c=>c.some(t=>a[Math.abs(t)]===(t>0)));
function witness(F,j){
  const k=F.r*F.r,r=F.r,mF=2*k+2;
  const a=Array(F.n+1).fill(false);const {s,u,v}=F;
  if(j<mF){
    a[s]=false;
    if(j===1)for(let i=0;i<=k;i++)a[i+1]=true;
    if(j===2){a[1]=true;for(let t=1;t<=k;t++)a[k+1+t]=true;}
    if(j>=3&&j<k+2){
      let h=j-1;for(let t=h;t<=k;t++)a[k+1+t]=true;
      let i=1;while(r*((i-1)%r)+Math.floor((i-1)/r)+1!==h)i++;
      for(let t=0;t<i;t++)a[t+1]=true;
    }
    if(j>=k+2){let i=j-(k+1);for(let t=0;t<i;t++)a[t+1]=true;}
  }else{
    a[s]=true;
    for(const t of F.clauses[j])if(Math.abs(t)===u||Math.abs(t)===v)a[Math.abs(t)]=t<0;
  }
  return a;
}
function main(){
  let cases=[];
  for(let r of [2,3,4,5]){
    let F=build(r),m=F.m;let signs=0;
    for(let j=0;j<m;j++){
      const a=witness(F,j);
      assert(!sat([F.clauses[j]],a));
      assert(sat(F.clauses.filter((_,i)=>i!==j),a));
      for(let t=0;t<F.clauses[j].length;t++){
        const changed=F.clauses.map(c=>[...c]);changed[j][t]*=-1;
        assert(sat(changed,a));signs++;
      }
    }
    if(r===2){
      let count=0,altered=F.clauses.map(c=>[...c]);altered[0][0]*=-1;let satcontrol=0;
      for(let mask=0;mask<(1<<F.n);mask++){
        let a=Array.from({length:F.n+1},(_,i)=>!!(mask&(1<<(i-1))));
        if(sat(F.clauses,a))count++;
        if(sat(altered,a))satcontrol++;
      }
      assert(count===0&&satcontrol>0);
    }
    const ledger=[...F.clauses];
    for(const e of F.derived){
      assert(e.a<ledger.length&&e.b<ledger.length);
      const A=ledger[e.a],B=ledger[e.b];
      assert((A.includes(e.pivot)&&B.includes(-e.pivot))||(A.includes(-e.pivot)&&B.includes(e.pivot)));
      assert.deepStrictEqual(canon([...A,...B].filter(t=>Math.abs(t)!==Math.abs(e.pivot))),e.clause);
      ledger.push(e.clause);
    }
    assert.deepStrictEqual(ledger.at(-1),[]);
    cases.push({r,n:F.n,m,signs,logical_nodes:F.derived.length,
      source_floor:m-1,explicit_derived_literal_slots:F.literalSlots,source_bits:8*Buffer.byteLength(F.dimacs)});
  }
  console.log(JSON.stringify({name:'GUARD-SUM-EXACT350',status:'COMPUTATIONAL',cases},null,2));
}
main();
