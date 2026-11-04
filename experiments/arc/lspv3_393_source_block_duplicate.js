/* LSPV-3/393: executable finite audit of source-class duplication. No dependencies. */
"use strict";
function check(c,m){if(!c)throw Error(m);}
function graph(k){const E=[];let h;if(k===0){h=4;for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)E.push([u,v]);}
else{h=2*k;for(let i=0;i<k;i++)E.push([i,(i+1)%k],[k+i,k+(i+1)%k],[i,k+i]);}
return {h,E};}
function sat(c,x){return c.some(l=>((x>>Math.abs(l)-1)&1)===(l>0?1:0));}
function all(C,x){return C.every(c=>sat(c,x));}
function main(){let tests=0;const fixtures=[];
for(const k of [0,3,4]){
 const {h,E}=graph(k),B=[];
 for(let v=0;v<h;v++){
 const I=E.map((edge,i)=>edge.includes(v)?i:-1).filter(j=>j>=0);
 check(I.length===3,"not cubic");tests++;
 for(let a=0;a<8;a++){let parity=0,C=[];
 for(let s=0;s<3;s++){const b=(a>>s)&1;parity^=b;C.push(b?-(I[s]+1):(I[s]+1));}
 if(parity!==(v===0?1:0))B.push(C);
 }
 }
 check(B.length===4*h,"source count");tests++;
 for(let r of [1,2,3]){
 const S=B.flatMap(c=>Array.from({length:r},()=>c));const cap=1<<E.length;
 check(!Array.from({length:cap},(_,a)=>a).some(x=>all(S,x)),"odd source SAT");tests++;
 for(let j=0;j<B.length;j++){
 const D=S.filter((c,i)=>Math.floor(i/r)!==j);
 let w=-1;for(let x=0;x<cap;x++)if(all(D,x)){w=x;break;}
 check(w>=0,"class deletion UNSAT");tests++;
 check(!sat(B[j],w),"wrong local witness");tests++;
 if(r>1)for(let s=0;s<3;s++){
 const T=S.map((c,i)=>i===j*r?c.map((l,t)=>t===s?-l:l):c);
 check(!Array.from({length:cap},(_,a)=>a).some(x=>all(T,x)),"single sign flip SAT");tests++;
 }
 }
 fixtures.push({graph:k===0?"K4":"prism"+k,h,r,source_labels:S.length,distinct_clause_classes:B.length,unit_paid_optimum:4*h-1,pivotal_labels:r===1?B.length:0});
 }
}
return {status:"PASS",tests,fixtures, theorem_scope:"Fixed Rmix341 mathematical proof; finite enumeration checks labels only",seed:null};}
const result=main();

if(typeof console!=='undefined'&&console.log) console.log(JSON.stringify(result,null,2));
