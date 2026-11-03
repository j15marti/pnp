#!/usr/bin/env node
// Standalone selector-tree source/proof generator and signed Resolution checker.
// Run: node lspv4_351_selector_compact.js (Node 18+).
'use strict';
function ck(x,m){if(!x)throw Error(m)}
function gl(v){return 2*v.toString(2).length-1}
function run(k,shape){
 let nextSelector=1,nextLeaf=k,sources=[],proof=[];
 function build(size,guards){
   if(size===1)return {leaf:true,guards,x:nextLeaf++};
   const selector=nextSelector++,ls=shape==='balanced'?size/2:1;
   return {selector,guards,left:build(ls,guards.concat(selector)),
           right:build(size-ls,guards.concat(-selector))};
 }
 const root=build(k,[]);
 function visit(t){
   if(t.leaf){t.id=sources.length;sources.push(t.guards.concat(t.x),t.guards.concat(-t.x));}
   else{visit(t.left);visit(t.right)}
 }
 visit(root);
 function derive(t){
   let a,b,pivot;
   if(t.leaf){a=t.id;b=a+1;pivot=t.x;}
   else{a=derive(t.left);b=derive(t.right);pivot=t.selector;}
   let id=sources.length+proof.length;
   proof.push({a,b,pivot,clause:t.guards});return id;
 }
 derive(root);
 const m=sources.length,n=2*k-1,q=proof.length,bs=n.toString(2).length;
 ck(m===2*k&&q===m-1,'counts');
 const data=sources.map(c=>[...c]);let reads=0;
 for(let i=0;i<q;i++){
   const step=proof[i];ck(step.a<m+i&&step.b<m+i,'parent order');
   const A=data[step.a],B=data[step.b],p=step.pivot;
   ck(A.includes(p)&&B.includes(-p),'signed pivot');
   const R=[...new Set(A.filter(v=>v!==p).concat(B.filter(v=>v!==-p)))];
   ck(!R.some(v=>R.includes(-v)),'non-tautological resolvent');
   const sort=c=>c.slice().sort((a,b)=>a-b).join(',');
   ck(sort(R)===sort(step.clause),'replay');
   data.push(R);reads+=A.length+B.length;
 }
 ck(proof[q-1].clause.length===0,'contradiction');
 const L=sources.reduce((s,c)=>s+c.length,0),d=Math.log2(k);
 ck(L===(shape==='balanced'?2*k*(d+1):k*k+3*k-2),'source literal count');
 ck(reads===(shape==='balanced'?4*k*d+2:2*k*k+2*k-2),'read count');
 const N=gl(n+1)+gl(m+1)+sources.reduce((s,c)=>s+gl(c.length+1)+c.length*(1+bs),0);
 const P=q*(2*(m+q).toString(2).length+bs);
 return {k,shape,variables:n,sources:m,min_mixed_nodes:q,sign_fields:L,
         encoded_source_bits:N,pivot_only_proof_bits:P,checked_parent_literals:reads};
}
const result=[];
for(const k of [2,4,8,16,32,64])
 for(const shape of ['balanced','comb'])result.push(run(k,shape));
console.log(JSON.stringify({status:'PASS',cases:result},null,2));