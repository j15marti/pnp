"use strict";
/* LSPV-3/555: DIFFERENT, COUNTERFACTUAL FREE-CASE proof language.
   This is not an R_mix341 parser, rule, historical checker or legal native certificate.
   Run: node experiments/arc/lspv3_555_free_case_refutation.cjs
*/
const assert = require("assert");
function valid(F){
  assert(Number.isSafeInteger(F.n) && F.n > 0 && Array.isArray(F.cs));
  for (const c of F.cs) {
    assert(Array.isArray(c) && c.length > 0);
    assert(c.every(l=>Number.isSafeInteger(l) && l!==0 && Math.abs(l)<=F.n));
  }
}
function full(n){
  const cs=Array.from({length:2**n},(_,a)=>
    Array.from({length:n},(_,i)=>a&(1<<i)?-(i+1):i+1));
  return {n,cs};
}
function k4(){
  const edges=[];for(let v=0;v<4;v++)for(let w=v+1;w<4;w++)edges.push([v,w]);
  const cs=[];
  for(let v=0;v<4;v++){
    const inc=edges.flatMap(([a,b],i)=>a===v||b===v?[i]:[]);
    for(let mask=0;mask<8;mask++){
      const parity=(mask&1)^((mask>>1)&1)^((mask>>2)&1);
      if(parity !== (v===0?1:0))
        cs.push(inc.map((e,j)=>((mask>>j)&1)?-(e+1):(e+1)));
    }
  }
  return {n:6,cs};
}
const cSat=(c,a)=>c.some(l=>a[Math.abs(l)-1] === Number(l>0));
function countModels(F){
  let ct=0;for(let a=0;a<2**F.n;a++){
    const bits=Array.from({length:F.n},(_,i)=>(a>>i)&1);
    if(F.cs.every(c=>cSat(c,bits)))ct++;
  }return ct;
}
let next=0;
function build(F,scope=[]){
  const id=String(next++);
  if(scope.length===F.n)
    return {id,rule:"CLOSE",scope:scope.slice(),source:F.cs.findIndex(c=>!cSat(c,scope))};
  return {id,rule:"SPLIT",scope:scope.slice(),var:scope.length,
    children:[build(F,[...scope,0]),build(F,[...scope,1])]};
}
function check(F,root){
  valid(F);const seen=new Set();let splits=0,leaves=0;
  function walk(x,scope){
    assert(x && typeof x.id==="string" && !seen.has(x.id),"unique ID");
    seen.add(x.id);assert(JSON.stringify(x.scope)===JSON.stringify(scope),"scope");
    if(x.rule==="CLOSE"){
      assert(scope.length===F.n && Number.isSafeInteger(x.source) &&
        x.source>=0 && x.source<F.cs.length,"real source");
      assert(!cSat(F.cs[x.source],scope),"falsified original");
      leaves++;return;
    }
    assert(x.rule==="SPLIT" && x.var===scope.length &&
      x.var<F.n && Array.isArray(x.children) && x.children.length===2,"two-arm split");
    splits++;walk(x.children[0],[...scope,0]);walk(x.children[1],[...scope,1]);
  }
  walk(root,[]);return {nodes:seen.size,splits,leaves,paid:0};
}
function rejects(F,p){let failed=false;try{check(F,p);}catch(e){failed=true;}assert(failed);}
function clone(x){return JSON.parse(JSON.stringify(x));}
const F=full(3), K=k4(), S={n:3,cs:F.cs.slice(1)};
assert(countModels(F)===0 && countModels(K)===0 && countModels(S)===1);
next=0;const fp=build(F), f=check(F,fp);
next=0;const kp=build(K), k=check(K,kp);
assert(f.splits===7 && f.leaves===8 && k.splits===63 && k.leaves===64);
let t=clone(fp);t.children.pop();rejects(F,t); // omitted AND arm
t=clone(fp);t.children[0].scope=[1];rejects(F,t); // illegal context
t=clone(fp);while(t.rule==="SPLIT")t=t.children[0];t.source=(t.source+1)%8;rejects(F,t); // forged source
t=clone(fp);t.children[0].id=t.id;rejects(F,t); // repeated ID
rejects(S,fp); // SAT source cannot close
rejects({n:3,cs:[[1,0,2]]},fp); // malformed literal
const width=[];
for(let n=1;n<=6;n++){
  const G=full(n);assert(countModels(G)===0);
  for(let a=0;a<2**n;a++){
    const bits=Array.from({length:n},(_,i)=>(a>>i)&1);
    assert(G.cs.filter(c=>!cSat(c,bits)).length===1);
  }
  width.push({n,clauses:2**n,requiredLeaves:2**n});
}
console.log(JSON.stringify({name:"LSPV-3/555",calculus:"COUNTERFACTUAL FREE-CASE, NOT R_mix341",
  F3:{variables:3,clauses:8,models:0,...f},
  oddK4:{variables:6,clauses:16,models:0,...k},
  satControl:{models:1,refutationRejected:true},
  corruptionsRejected:6,width,scientificStatus:"PROVED/RESTRICTED",pVsNP:"OPEN"},null,2));
