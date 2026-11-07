#!/usr/bin/env node
"use strict";
/* LSPV-1/476 compact replayer, distinct typed grammar R_or476.
   It is NOT a historical R_mix341 accepted-byte checker. */
const assert=require("assert");
const widths=[2,3,4,5,6,7,8,9,10,11,12,16,24,32,48,64];
function sortClause(xs){
  let a=[...new Set(xs)].sort((u,v)=>Math.abs(u)-Math.abs(v)||u-v);
  for(let x of a)assert(!a.includes(-x),"tautological clause");
  return a;
}
function same(a,b){return JSON.stringify(sortClause(a))===JSON.stringify(sortClause(b));}
function res(a,b,p){
  assert(a.includes(p)&&b.includes(-p),"bad oriented pivot");
  return sortClause(a.filter(x=>x!==p).concat(b.filter(x=>x!==-p)));
}
function sat(a,v){return a.some(t=>t>0?Boolean(v[Math.abs(t)]):!Boolean(v[Math.abs(t)]));}
let rows=[],checked=0;
for(const w of widths){
  let front=Array.from({length:w},(_,i)=>i+1);
  let known=new Map([["F.C1",front.slice()]]),gates=[],proofs=[],root="F.C1";
  let output=w,nres=0;
  while(front.length>1){
    let follow=[];
    for(let i=0;i<front.length;i+=2){
      if(i+1===front.length){follow.push(front[i]);continue;}
      let a=front[i],b=front[i+1],z=++output;
      let owner="D"+(gates.length+1);
      let facets=[[-a,z],[-b,z],[a,b,-z]].map(sortClause);
      for(let j=0;j<3;j++)known.set(owner+".facet"+(j+1),facets[j]);
      gates.push({a,b,z,owner,facets});
      for(let [p,facet] of [[a,1],[b,2]]){
        let left=root,right=owner+".facet"+facet;
        let next="R"+(++nres);
        let out=res(known.get(left),known.get(right),p);
        assert(!known.has(next));known.set(next,out);
        proofs.push({left,right,next,p,out});
        root=next;
      }
      follow.push(z);
    }
    front=follow;
  }
  let final=front[0];
  assert(same(known.get(root),[final]));
  assert(gates.length===w-1&&proofs.length===2*(w-1));
  let degree=Object.fromEntries(Array.from({length:w},(_,i)=>[i+1,0]));
  for(const g of gates){
    assert(g.a<g.z&&g.b<g.z&&g.a!==g.b);
    degree[g.z]=1+Math.max(degree[g.a],degree[g.b]);
    for(let av=0;av<2;av++)for(let bv=0;bv<2;bv++)for(let zv=0;zv<2;zv++){
      let val={[g.a]:av,[g.b]:bv,[g.z]:zv};
      assert.strictEqual(g.facets.every(f=>sat(f,val)),zv===(av|bv));
      checked++;
    }
  }
  assert.strictEqual(degree[final],Math.ceil(Math.log2(w)));
  for(const p of proofs){
    assert(same(res(known.get(p.left),known.get(p.right),p.p),p.out));
    checked++;
  }
  let ntests=0;
  if(w<=12){
    for(let bits=0;bits<(1<<w);bits++){
      let val={};
      for(let j=1;j<=w;j++)val[j]=(bits>>(j-1))&1;
      let wanted=sat(Array.from({length:w},(_,i)=>i+1),val);
      for(const g of gates){
        val[g.z]=val[g.a]|val[g.b];
        assert(g.facets.every(f=>sat(f,val)));
      }
      assert.strictEqual(Boolean(val[final]),wanted);
      ntests++;checked++;
    }
  }
  rows.push({w,paidDEF:gates.length,paidRES:proofs.length,paidTotal:3*(w-1),gateDepth:degree[final],constructedProofSpan:2*(w-1)+1,exhaustedAssignments:ntests});
}
function tee(charge){
 let edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],src=[];
 for(let v=0;v<4;v++){
  let es=edges.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);
  for(let a=0;a<8;a++){
   let parity=((a&1)>0)^((a&2)>0)^((a&4)>0);
   if(Number(parity)===charge[v])continue;
   src.push(es.map((e,j)=>((a>>j)&1)?-e:e));
  }
 }
 assert(src.length===16);
 let models=0;
 for(let a=0;a<64;a++){
  let vals={};for(let i=1;i<=6;i++)vals[i]=(a>>(i-1))&1;
  if(src.every(cl=>sat(cl,vals)))models++;
 }
 return models;
}
assert.strictEqual(tee([1,0,0,0]),0);
assert.strictEqual(tee([0,0,0,0]),8);
process.stdout.write(JSON.stringify({schema:"LSPV1_476_COMPACT_R_or476_REPLAYER",status:"COMPUTATIONAL, separate typed grammar, historical R_mix341 OPEN",checked,rows,tseitin:{odd:0,even:8}},null,2)+"\n");