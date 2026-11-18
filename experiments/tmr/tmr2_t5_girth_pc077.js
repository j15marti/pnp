"use strict";
// TMR-2/077: independently executable 4-step saturation and oriented-C7 count audit.
const beat=(a,b)=>{let d=(b-a+10)%5;return d===1||d===3};
const steps=[-1,1];let checks=0;
function ck(ok,why){checks++;if(!ok)throw Error(why)}
function multiply(A,B){return A.map(row=>Array.from({length:5},(_,j)=>row.reduce((s,v,k)=>s+v*B[k][j],0)))}
function matrix(sign){return Array.from({length:5},(_,i)=>Array.from({length:5},(_,j)=>+(sign===1?beat(i,j):beat(j,i))))}
function path(word){let A=Array.from({length:5},(_,i)=>Array.from({length:5},(_,j)=>+(i===j)));
 for(let sign of word)A=multiply(A,matrix(sign));
 return A}
let saturation={};
for(let length=0;length<=6;length++){let sizes=new Set();
 for(let code=0;code<2**length;code++){
  let word=Array.from({length},(_,i)=>(code>>i)&1?1:-1);
  let A=path(word),nz=A.reduce((s,row)=>s+row.filter(Boolean).length,0);
  ck(nz===5*Math.min(length+1,5),"signed-path support length "+length);sizes.add(nz)
 }saturation[length]=[...sizes]}
let masks=[];
for(let m=0;m<32;m++){let f=0,r=0;
 for(let a=0;a<5;a++)if(m&(1<<a))for(let b=0;b<5;b++){if(beat(a,b))f|=1<<b;if(beat(b,a))r|=1<<b}
 masks.push([m,f,r]);ck((m===0)===(f===0&&r===0),"mask support")}
let histogram={};
for(let m=0;m<128;m++){let word=Array.from({length:7},(_,i)=>m&(1<<i)?1:-1);
 let A=path(word),count=A.reduce((s,row,i)=>s+row[i],0);
 ck(count>0,"oriented 7-cycle SAT");histogram[count]=(histogram[count]||0)+1}
ck(histogram[70]===14&&histogram[110]===70&&histogram[175]===44&&Object.keys(histogram).length===3,"C7 exact histogram");
console.log(JSON.stringify({revision:"tmr2-t5-girth-pc077-js.v1",checks,failures:0,saturation,domain_masks:masks,C7_exact_count_histogram:histogram,
  independent_Python_full_PC_audit:"715 checks; separate downloadable original source, not this JavaScript",unrestricted_lower_bound:"OPEN"},null,2));
