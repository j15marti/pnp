/* ARC-INDEXED-GUARD263: independent compact checker; node >=16.
   Finite controls use materialized proof nodes, not an uncharged ARC oracle. */
"use strict";
function check(){
 let tests=0,wrong=0,modes=0;
 const ok=(v,msg)=>{tests++;if(!v)throw Error(msg||"test")};
 const norm=a=>[...new Set(a)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
 const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const lit=(l,a)=>l>0?a[l-1]===1:a[-l-1]===0;
 const t=(c,a)=>c.filter(l=>lit(l,a)).length;
 const assignments=Array.from({length:8},(_,k)=>[k&1,k>>1&1,k>>2&1]);
 const F8=Array.from({length:8},(_,k)=>[1,2,3].map((v,i)=>k>>i&1?v:-v));
 const F7=F8.filter(c=>!eq(c,[-1,-2,-3]));
 function res(A,B,p){ok(A.includes(p)&&B.includes(-p),"pivot");return norm([...A.filter(x=>x!==p),...B.filter(x=>x!==-p)])}
 function derive(F,s){let P=[];for(let [y,z] of [[2,3],[2,-3],[-2,3],[-2,-3]]){
  let c=norm([s,y,z]),id=F.findIndex(d=>eq(c,d));if(id<0)return null;
  P.push({type:"source",id,c})}
  for(let [i,j,p] of [[0,1,3],[2,3,3],[4,5,2]])P.push({type:"res",parents:[i,j],pivot:p,c:res(P[i].c,P[j].c,p)});
  ok(eq(P[6].c,[s]),"unit");P.push({type:"assume",c:[-s]});
  P.push({type:"res",parents:[6,7],pivot:s,c:res(P[6].c,P[7].c,s)});return P}
 function verify(F,assumptions,P){let U=new Set();for(let i=0;i<P.length;i++){
  let r=P[i];ok(eq(r.c,norm(r.c)),"canonical");
  if(r.type==="source")ok(r.id>=0&&r.id<F.length&&eq(F[r.id],r.c),"source");
  else if(r.type==="assume"){ok(r.c.length===1&&assumptions.includes(r.c[0]),"scope");U.add(r.c[0])}
  else if(r.type==="res"){let [p,q]=r.parents;ok(p>=0&&q>=0&&p<i&&q<i,"index");ok(eq(r.c,res(P[p].c,P[q].c,r.pivot)),"step")}
  else throw Error("node")}
  ok(P.at(-1).c.length===0,"root");let guard=norm([...U].map(x=>-x));
  for(let a of assignments)if(F.every(c=>t(c,a)>0))ok(guard.some(l=>lit(l,a)),"entailment");
  return guard}
 let cases=[];for(let [name,F] of [["SAT_7_of_8",F7],["UNSAT_8_of_8",F8]]){
  let models=assignments.filter(a=>F.every(c=>t(c,a)>0));
  for(let a of assignments)for(let c of F)ok(t(c,a)+t(c,a.map(x=>1-x))===3,"complement");
  for(let i=0;i<F.length;i++)for(let j=i+1;j<F.length;j++)for(let mask=0;mask<4;mask++){
   let map=new Map(),consistent=true;
   for(let [h,c] of [F[i],F[j]].entries())for(let l of c){let v=Math.abs(l),mode=!!(mask>>h&1),b=(l>0?mode:!mode)?1:0;
    if(map.has(v)&&map.get(v)!==b)consistent=false;map.set(v,b)}
   let brute=assignments.some(a=>t(F[i],a)===(mask&1?3:0)&&t(F[j],a)===(mask&2?3:0));
   ok(brute===consistent,"pair");modes++}
  let left=derive(F,1),right=derive(F,-1);
  ok(!!left&&eq(verify(F,[-1],left),[1]),"left");
  if(right)ok(eq(verify(F,[1],right),[-1]),"right");
  else ok(models.length>0&&models.some(a=>a[0]===1),"witness");
  ok((models.length===0)===!!right,"join");
  cases.push({name,models:models.length,x0:"UNSAT",x1:right?"UNSAT":"SAT"})}
 let bad=derive(F7,1);bad[0].id=99;
 try{verify(F7,[-1],bad);throw Error("accepted forged source")}
 catch(e){if(e.message==="accepted forged source")throw e;wrong++}
 return{tests,pair_extreme_modes:modes,forgeries_rejected:wrong,cases}}
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(check(),null,2));
