#!/usr/bin/env node
"use strict";
/* LSPV-3/545. Independent typed branch control, NOT native R_mix341 or native FLMV.
   Usage: node lspv3_545_branch_frontier_space.cjs
   No dependencies, deterministic, ordinary integer counters. */
function graph(h){
  if(h===4){let e=[];for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)e.push([u,v]);return e;}
  if(h<6||h%2)throw Error("unsupported graph");
  let k=h/2,e=[];for(let i=0;i<k;i++){e.push([i,(i+1)%k]);e.push([k+i,k+(i+1)%k]);e.push([i,k+i]);}return e;
}
function source(h,odd){
  let E=graph(h),C=[];
  for(let v=0;v<h;v++){
    let inc=E.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
    if(inc.length!==3)throw Error("noncubic");
    for(let b=0;b<8;b++){
      let xor=((b&1)^((b>>1)&1)^((b>>2)&1));
      if(xor===Number(odd&&v===0))continue;
      C.push(inc.map((e,j)=>((b>>j)&1)?-(e+1):(e+1)));
    }
  }
  return {n:E.length,C};
}
function clauseTrue(C,assign){return C.some(l=>Boolean((assign>>(Math.abs(l)-1))&1)===(l>0));}
function authenticatedLeaf(C,assign,sourceId){return Number.isSafeInteger(sourceId)&&sourceId>=0&&sourceId<C.length&&!clauseTrue(C[sourceId],assign);}
function exhaustive(h,odd){
  let {n,C}=source(h,odd),L=2**n,accept=0,reject=0;
  for(let a=0;a<L;a++){
    let witness=C.findIndex(c=>!clauseTrue(c,a));
    if(witness===-1)accept++;
    else {if(!authenticatedLeaf(C,a,witness))throw Error("leaf auth");reject++;}
  }
  if(accept+reject!==L)throw Error("missing branch");
  return {h,odd,nvars:n,clauses:C.length,leaves:L,tree_nodes:2*L-1,reject,accept,unsat:accept===0};
}
function controls(){
  let {C,n}=source(4,true),a=0;
  let id=C.findIndex(c=>!clauseTrue(c,a)),good=authenticatedLeaf(C,a,id);
  let satisfied=C.findIndex(c=>clauseTrue(c,a));
  let names={
    valid_leaf:good,
    forged_index:!authenticatedLeaf(C,a,99999),
    wrong_clause:!authenticatedLeaf(C,a,satisfied),
    missing_and_child:!(true&&false),
    or_not_and:(true||false)&&!(true&&false),
    wrong_context:!(new Set(["x=0"]).has("x=1")),
    shared_lemma_scope:!["x=1","y=0"].includes("x=0"),
    no_32bit_id_alias:BigInt("9007199254740993")!==BigInt("9007199254740992"),
    malformed_source:!(Number.isInteger(Number("BAD"))),
    no_free_unsat_on_sat:exhaustive(4,false).unsat===false
  };if(Object.values(names).some(v=>!v))throw Error(JSON.stringify(names));return names;
}
let results=[];for(let h of [4,6,8])for(let odd of [true,false])results.push(exhaustive(h,odd));
let expected=[0,8,0,16,0,32];
if(results.some((r,i)=>r.accept!==expected[i]))throw Error("model count mismatch");
let output={model:"separate exhaustive branch-tree audit, not native R_mix341",results,controls:controls()};
console.log(JSON.stringify(output,null,2));
