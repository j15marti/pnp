/* LSPV-3/388 independent truth-table bitset verifier.
 * Separate representation and entailment algorithm from producer.
 * Run: node lspv3_388_independent_bitset.js
 */
"use strict";
const q=(a,b)=>a*2+b;
function mask(atom,width){let ans=0;for(let z=0;z<(1<<width);z++){
  const a=atom>>1, b=atom&1; let v=a&z,p=0;
  while(v){v&=v-1;p^=1}if(p===b)ans|=1<<z;
}return ans}
function clauses(width){
 const atoms=Array.from({length:(1<<width)*2},(_,i)=>i),out=[[]];
 for(const x of atoms)out.push([x]);
 for(let i=0;i<atoms.length;i++)for(let j=i+1;j<atoms.length;j++)out.push([atoms[i],atoms[j]]);
 return out
}
function cm(C,n){return C.reduce((s,a)=>s|mask(a,n),0)}
const take=(m)=>(m>>4)&15;
const c2=clauses(2),c3=clauses(3),vals=255;
function semantic(A,B){return (A&(~B)&vals)===0}
let checks=0,weak=0,cofactor=0,res=0,degenerate=0,guardedRes=0;
function ok(t,m){checks++;if(!t)throw Error(m)}
for(const A of c2)for(const B of c2){let a=cm(A,2),b=cm(B,2);if((a&(~b)&15)===0){
weak++;ok(semantic(15|(a<<4),15|(b<<4)),"guard shift");
}}
for(const A of c3)for(const B of c3){let a=cm(A,3),b=cm(B,3);if(semantic(a,b)){
cofactor++;ok((take(a)&~take(b)&15)===0,"cofactor shift");
}}
for(let p=1;p<8;p++)for(const A of c2)for(const B of c2){
 const am=cm(A,3),bm=cm(B,3),p0=mask(q(p,0),3),p1=mask(q(p,1),3);
 const left=am|p0,right=bm|p1,out=am|bm;
 res++;ok(semantic(left&right,out),"bad pivot");
 ok((take(left)&take(right)&(~take(out))&15)===0,"bad restricted pivot");
 if(p===4){degenerate++;ok(((take(left)&~take(out)&15)===0)||((take(right)&~take(out)&15)===0),"not one-parent");}
 if(p<4){guardedRes++;ok(semantic((15|left<<4)&(15|right<<4),15|out<<4),"failed lift");}
}
const result={schema:"LSPV3_388_INDEPENDENT_BITSET",semantic_lifts:weak,cofactor_semantic_checks:cofactor,
 res_steps:res,t_only_pivot_cases:degenerate,guarded_resolution:guardedRes,assertions:checks};
ok(result.semantic_lifts===591,"producer disagreement weak");
ok(result.cofactor_semantic_checks===4191,"producer disagreement cofactor");
ok(result.res_steps===9583,"producer disagreement res");
ok(result.t_only_pivot_cases===1369,"producer disagreement pivot");
ok(result.guarded_resolution===4107,"producer disagreement lift");
result.assertions=checks;
console.log(JSON.stringify(result,null,2));