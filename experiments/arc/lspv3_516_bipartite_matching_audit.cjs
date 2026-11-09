'use strict';
// LSPV-3/516: independent bipartite Q4 matching, original-source, XLRUP hint audit.
// Exact source clause semantics, no historical R_mix341 or official CakeML checker.
const assert=require('node:assert/strict');
const even=Array.from({length:16},(_,i)=>i).filter(i=>pop(i)%2===0);
const odd=Array.from({length:16},(_,i)=>i).filter(i=>pop(i)%2===1);
function pop(x){let n=0;for(;x;x&=x-1)n++;return n}
let total=0,withFour=0,withoutFour=0,assertions=0;
const hist={};
function recur(depth,mask,edges){
 if(depth===8){
   total++;
   const cnt=[0,0,0,0];
   const clauses=[];
   for(const [a,b] of edges){let delta=a^b;let j=31-Math.clz32(delta);cnt[j]++;
     clauses.push(Array.from({length:4},(_,i)=>i).filter(i=>i!==j).map(i=>a>>i&1?-(i+1):i+1));}
   const key=cnt.filter(x=>x).sort((a,b)=>a-b).join(',');hist[key]=(hist[key]||0)+1;
   assertions++;assert(cnt.every(n=>n%2===0));
   for(let a=0;a<16;a++){
     let bad=clauses.filter(c=>c.every(l=> ((a>>(Math.abs(l)-1))&1)!==(l>0?1:0)));
     assertions++;assert.equal(bad.length,1);
   }
   for(const rhs of [0,1])for(let a=0;a<16;a++)if(pop(a)%2!==rhs){
     const cnf=Array.from({length:4},(_,i)=>a>>i&1?-(i+1):i+1);
     assertions++;assert.equal(clauses.filter(c=>c.every(l=>cnf.includes(l))).length,1);
   }
   if(cnt.every(x=>x>0))withFour++;else withoutFour++;
   return;
 }
 const a=even[depth];
 for(let j=0;j<4;j++){
   const b=a^(1<<j),index=odd.indexOf(b);
   if(index<0 || (mask>>index&1))continue;
   recur(depth+1,mask|(1<<index),[...edges,[a,b]]);
 }
}
recur(0,0,[]);
assert.equal(total,272);assert.equal(withFour,40);assert.equal(withoutFour,232);
console.log(JSON.stringify({independent_js:true,total,full_support:withFour,missing_direction:withoutFour,
 histogram:hist,assertion_groups:assertions,external_format_only:true,original_historical_checker:false},null,2));
