"use strict";
// LSPV-1/502: finite syntax audit for elimination of conservative Boolean wires.
// Proposed extension-bearing Resolution model only. Not the historical R_mix341 checker.
const N = 3, Z = 4, defs = new Map([[Z,[1,2]]]);
const source = [[1,3],[-1,3],[2],[-3]];
const facets = [[-4,1],[-4,2],[4,-1,-2]];
const native = [
  ...source.map(c=>["SOURCE",c]),
  ...facets.map(c=>["DEF",c]),
  ["RES",[4,-2,3],6,0,1],
  ["RES",[4,3],7,2,2],
  ["RES",[-4,3],4,1,1],
  ["RES",[3],8,9,4],
  ["RES",[],10,3,3]
];
let checks=0, negatives=0;
const assert=(v,msg)=>{ checks++; if(!v) throw new Error(msg||"assert"); };
const uniq=a=>Array.from(new Set(a)).sort((x,y)=>x-y);
const isSub=(a,b)=>a.every(x=>b.includes(x));
const eq=(a,b)=>JSON.stringify(uniq(a))===JSON.stringify(uniq(b));
function resolve(A,B,p){
  let a=A,b=B;
  if(a.includes(-p)&&b.includes(p)){[a,b]=[b,a];}
  if(!(a.includes(p)&&b.includes(-p))) throw Error("illegal RES pivot");
  return uniq([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
}
function support(k){k=Math.abs(k); if(k<=N)return [k];return uniq(defs.get(k).flatMap(support));}
function wireSupport(c){return uniq(c.filter(x=>Math.abs(x)>N).flatMap(support));}
function bitValue(v,a){
  let k=Math.abs(v),value;
  if(k<=N){value=a[k];}
  else{const [u,w]=defs.get(k);value=bitValue(u,a)&bitValue(w,a);}
  return v>0?value:1-value;
}
function trueClause(c,a){return c.some(x=>bitValue(x,a));}
function assignments(U){
  const out=[];
  for(let bits=0;bits<(1<<U.length);bits++){
    const a={};U.forEach((v,i)=>a[v]=(bits>>i)&1);
    out.push(a);
  }
  return out;
}
function exclusion(a){return uniq(Object.entries(a).map(([k,v])=>v?-Number(k):Number(k)));}
const key=(a,U)=>U.map(u=>a[u]).join("");
function image(c){
  const U=wireSupport(c);
  const G=uniq(c.filter(l=>Math.abs(l)<=N&&!U.includes(Math.abs(l))));
  const L=uniq(c.filter(l=>!G.includes(l)));
  const m=new Map();
  for(const a of assignments(U))if(!trueClause(L,a))m.set(key(a,U),uniq([...G,...exclusion(a)]));
  return {U,G,L,m};
}
for(let i=0;i<native.length;i++){
  const [tag,c,p1,p2,p]=native[i];
  assert(!c.some(l=>c.includes(-l)),"tautological source-control node");
  if(tag==="SOURCE")assert(source.some(s=>eq(s,c)),"invented source");
  if(tag==="DEF")assert(facets.some(s=>eq(s,c)),"invalid facet");
  if(tag==="RES"){assert(p1<i&&p2<i,"cycle");assert(eq(resolve(native[p1][1],native[p2][1],p),c),"native resolution incorrect");}
}
assert(native[native.length-1][1].length===0,"not a refutation");
const t=[], memo=new Map(), maps=[];
function emit(tag,c,parents=[],p=0){
  c=uniq(c);
  if(tag==="SOURCE")assert(source.some(s=>eq(s,c)),"external source rejected");
  else if(tag==="W")assert(parents.length===1&&isSub(t[parents[0]].clause,c),"bad weakening");
  else if(tag==="R")assert(parents.length===2&&eq(resolve(t[parents[0]].clause,t[parents[1]].clause,p),c),"bad Resolution");
  else throw Error("unknown rule");
  const k=JSON.stringify([tag,c,parents,p]);
  if(memo.has(k))return memo.get(k);
  const j=t.length;t.push({tag,clause:c,parents,p});memo.set(k,j);return j;
}
for(let i=0;i<native.length;i++){
  const [tag,c,p1,p2,p]=native[i],out=image(c);
  const map=new Map();
  if(tag==="SOURCE"){for(const [bits,C] of out.m)map.set(bits,emit("SOURCE",C));}
  else if(tag==="DEF"){assert(out.m.size===0,"nonconservative DEF");}
  else{
    const P=[native[p1][1],native[p2][1]],PI=P.map(image);
    const V=uniq([...PI[0].U,...PI[1].U,...out.U]);
    for(const [prefix,goal] of out.m){
      const a0={};out.U.forEach((v,j)=>a0[v]=Number(prefix[j]));
      let live=new Map();
      for(const a of assignments(V)){
        if(out.U.some(v=>a[v]!==a0[v]))continue;
        const D=exclusion(a), leaf=uniq([...out.G,...D]);
        function parentIdx(k){
          const ij=PI[k],kb=key(a,ij.U);
          assert(ij.m.has(kb),"chosen parent not false");
          return maps[k? p2:p1].get(kb);
        }
        let idx;
        if(Math.abs(p)>N||V.includes(p)){
          const falses=P.map((parent,j)=>j).filter(j=>!trueClause(P[j].filter(v=>Math.abs(v)>N||V.includes(Math.abs(v))),a));
          assert(falses.length>=1,"no parent false");
          const from=parentIdx(falses[0]);
          assert(isSub(t[from].clause,leaf),"nonweakening aux lift");
          idx=eq(t[from].clause,leaf)?from:emit("W",leaf,[from]);
        }else{
          const A=parentIdx(0),B=parentIdx(1),g0=uniq([...PI[0].G,...D]),g1=uniq([...PI[1].G,...D]);
          assert(isSub(t[A].clause,g0)&&isSub(t[B].clause,g1),"guard mismatch");
          const aa=eq(t[A].clause,g0)?A:emit("W",g0,[A]);
          const bb=eq(t[B].clause,g1)?B:emit("W",g1,[B]);
          idx=emit("R",leaf,[aa,bb],p);
        }
        live.set(key(a,V),idx);
      }
      let VV=[...V];
      for(const v of V.filter(x=>!out.U.includes(x))){
        const ix=VV.indexOf(v),next=new Map();
        for(const [bits,idx] of live){
          if(bits[ix]!=="0")continue;
          const flip=bits.slice(0,ix)+"1"+bits.slice(ix+1),other=live.get(flip);
          assert(other!==undefined,"incomplete AND cases");
          const C=resolve(t[idx].clause,t[other].clause,v);
          next.set(bits.slice(0,ix)+bits.slice(ix+1),emit("R",C,[idx,other],v));
        }
        live=next;VV=VV.filter(x=>x!==v);
      }
      assert(live.size===1,"unclosed assignments");
      const final=[...live.values()][0];
      assert(eq(t[final].clause,goal),"incorrect projected target");
      map.set(prefix,final);
    }
  }
  maps.push(map);
  for(const a of assignments([1,2,3])){
    const lhs=trueClause(c,a),rhs=[...map.values()].every(j=>trueClause(t[j].clause,a));
    assert(lhs===rhs,"invalid Boolean semantics");
  }
}
assert(t[maps.at(-1).get("")].clause.length===0,"missing syntactic target contradiction");
// Four purpose-built hostile cases must be rejected by the same rule checkers.
for(const bad of [
 ()=>resolve([4,3],[-4,3],2),
 ()=>resolve([4,3],[-4,3],-2),
 ()=>emit("SOURCE",[4]),
 ()=>emit("W",[-1],[maps[0].get("")]),
]){
 try{bad();}catch(e){negatives++;}
}
assert(negatives===4,"corruption not rejected");
const result={status:"COMPUTATIONAL",historical_checker_executed:false,
 model:"distinct conservative AND4 wire and arbitrary extension-bearing RES",
 original_source_variables:3,source_clauses:source.length,source_facets:facets.length,
 native_nodes:native.length,target_nodes:t.length,
 target_final_empty:true,max_extension_parent_ancestor_union:2,
 syntactic_rules:["source","weakening","Resolution"],checks,corrupt_rejected:negatives};
result.trace_sha_hint="not a cryptographic SHA; inspect published source and raw";
globalThis.__lspv502_result=result;

console.log(JSON.stringify(result,null,2));
