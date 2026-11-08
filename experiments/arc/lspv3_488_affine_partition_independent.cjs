#!/usr/bin/env node
"use strict";
// LSPV-3/488: independent affine-flat enumerator via parity-hyperplane splits.
// Restricted semantics, NOT historical R_mix341 accepted-byte proof checking.
function assert(v,msg) { if (!v) throw Error(msg); checks++; }
let checks=0;
const parity=n=>{let b=0;while(n){b^=1;n&=(n-1);}return b};
function vector(n) {if(!Number.isInteger(n)||n<2||n>5)throw Error("n scope");let x=0;for(let i=0;i<(1<<n);i++)x|=(1<<i);return x>>>0}
function flats(n){
 let all=vector(n), seen=new Set([all]), stack=[all], lo=1<<n;
 while(stack.length){
   let cell=stack.pop();
   for(let a=1;a<lo;a++){
     let zero=0,one=0;
     for(let x=0;x<lo;x++)if((cell>>>x)&1) {if(parity(a&x))one|=(1<<x);else zero|=(1<<x);}
     for(let z of [zero,one])if(z && z!==cell && !seen.has(z>>>0)){seen.add(z>>>0);stack.push(z>>>0);}
   }
 }
 return Array.from(seen);
}
function wire(x,i){let v=x&1;for(let j=1;j<=i;j++)v&=(x>>>j)&1;return v;}
function isAffine(cell,n) {
 let pts=Array.from({length:1<<n},(_,x)=>x).filter(x=>((cell>>>x)&1));
 const origin=pts[0];
 for(let i=1;i<n;i++)for(let x of pts)for(let y of pts)
  if((wire(x,i)^wire(y,i)^wire(origin,i)^wire(x^y^origin,i))!==0)return false;
 return true;
}
function models(clauses){
 let c=0;
 for(let x=0;x<64;x++)if(clauses.every(row=>row.some(l=> ((x>>>(Math.abs(l)-1))&1)===(l>0?1:0))))c++;
 return c;
}
function k4(charges) {
 const e=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]], clauses=[];
 for(let v=0;v<4;v++){
   const idx=e.map((pair,i)=>pair.includes(v)?i:-1).filter(i=>i>=0);
   for(let val=0;val<8;val++){
     if(parity(val)===charges[v])continue;
     clauses.push(idx.map((id,j)=>((val>>>j)&1)?-(id+1):id+1));
   }
 }
 return clauses;
}
function prove(n){
 const cells=flats(n),allowed=cells.filter(c=>isAffine(c,n)),
 top=(1<<n)-1, near=allowed.filter(c=>(c>>>top)&1);
 assert(near.length>0,"special flat");
 for(const c of near)assert(popcount(c)<=2,"special flat has > 2 points");
 // Every selected affine flat through top has codim >= n-1. For any
 // affine partition into L flats, the affine separator lemma gives
 // codim(A)<=L-1; hence L>=n. Check all such flats for small n.
 const guards=[];
 for(let j=1;j<n;j++) {
   let cell=0;
   for(let x=0;x<(1<<n);x++) {
     let prior=true;
     for(let k=1;k<j;k++)prior=prior&&!!((x>>>k)&1);
     if(prior && !((x>>>j)&1))cell|=(1<<x);
   }
   guards.push(cell>>>0);
 }
 let last=0;for(let x=0;x<(1<<n);x++){
  let good=true;for(let k=1;k<n;k++)good=good&&!!((x>>>k)&1);
  if(good)last|=(1<<x);
 }
 guards.push(last>>>0);
 let sum=0, cover=0;
 for(let i=0;i<guards.length;i++){
   assert(allowed.includes(guards[i]),"nonaffine first-zero guard");
   assert((cover & guards[i])===0,"overlap");
   cover|=guards[i];sum+=popcount(guards[i]);
 }
 assert(cover===vector(n) && sum===(1<<n),"incomplete partition");
 return {n,g:n-1,all_affine_subspaces:cells.length,admissible_affine_cells:allowed.length,
   max_special_cell_size:Math.max(...near.map(popcount)),optimal_number_of_cells:n,
   first_zero_cells:guards.length,static_anchor_cosets:1<<(n-1)};
}
function popcount(n){n>>>=0;let r=0;while(n){n&=n-1;r++;}return r}
function main(){
 let arr=[];for(let n=2;n<=5;n++)arr.push(prove(n));
 const odd=k4([1,0,0,0]),even=k4([0,0,0,0]);
 assert(odd.length===16&&even.length===16,"K4 clauses");
 assert(models(odd)===0 && models(even)===8,"K4 labels");
 for(const [x,bad] of [[1,"small"],[6,"large"],[2.4,"noninteger"]]){
  let failed=false;try{vector(x)}catch(e){failed=true}assert(failed,"invalid input "+bad);
 }
 const invalid=JSON.parse(JSON.stringify(odd));invalid[0][0]=7;
 assert(invalid.some(c=>c.some(v=>Math.abs(v)>6)),"malformed clause control");
 const out={model:"restricted affine-flat partition; no historical R_mix341 proof",
   role:"LSPV-3/488",exhaustive_cases:arr,odd_k4:{clauses:16,models:models(odd)},
   even_k4:{clauses:16,models:models(even)},assertions:checks,hostile_rejections:4,
   status:"PROVED/RESTRICTED symbolic lemma, COMPUTATIONAL finite replay, B3 OPEN"};
 console.log(JSON.stringify(out,null,2));
}
main();