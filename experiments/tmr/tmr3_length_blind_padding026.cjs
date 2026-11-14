"use strict";
// TMR-3/026: finite controls for a length-blind, one-way MCSP padding source.
// Run: node experiments/tmr/tmr3_length_blind_padding026.cjs
// All tests are computational, not a physical Turing-machine implementation.
function check(p,msg){if(!p) throw new Error(msg);}
function pad(x,t){return [...x].map(v=>v.repeat(2**t)).join("");}
function padIndex(x,t){let out="";for(let j=0;j<x.length*(2**t);j++)out+=x[Math.floor(j/(2**t))];return out;}
function lcp(a,b){let i=0;while(i<a.length&&i<b.length&&a[i]===b[i])i++;return i;}
function main(){
  let cases=0,generated=0,distinct=0,fixed=0;
  const rows=[];
  for(const n of [2,3,4]){
    const N=2**n,t=Math.ceil(n/2),R=2**t,n2=n+2,t2=Math.ceil(n2/2),R2=2**t2;
    check(R2>R,"expansion must grow");
    const post=new Set();
    for(let k=0;k<2**(N-2);k++){
      const x="01"+k.toString(2).padStart(N-2,"0");
      const longer=x+"0".repeat(2**n2-N);
      const short=pad(x,t),long=padIndex(longer,t2);
      check(short===padIndex(x,t),"two independent extension algorithms disagree");
      check(lcp(short,long)===R,"shared source prefix output split incorrect");
      check(short.slice(0,R)==="0".repeat(R)&&short[R]==="1"&&long[R]==="0","branch mismatch");
      check(!post.has(short.slice(R)),"two distinct source suffixes collided");
      post.add(short.slice(R));cases++;generated+=2;distinct++;
    }
    rows.push({n,N,t,R,n2,R2,variable_suffixes:post.size,retained_bits:N-2,output_bits:N*R});
  }
  // Fixed t has a streaming finite-control producer even without a length header.
  for(const n of [2,3,4]){
    const N=2**n;
    for(let k=0;k<2**N;k++){
      let s="";
      for(let j=0;j<N;j++)s+=(k>>j)&1;
      check(pad(s,1)===padIndex(s,1),"fixed-t control failed");fixed++;
    }
  }
  return {label:"TMR3_LENGTH_BLIND_PADDING026",status:"COMPUTATIONAL",
    tested_lengths:[2,3,4],rows,ambiguous_prefix_cases:cases,
    generated_padded_tables:generated,unique_postcut_suffixes:distinct,
    fixed_t_positive_controls:fixed,failed_assertions:0,
    limits:"finite source tables; no instruction-level finite-alphabet TM compiler"};
}
const result=main();
if(typeof console!=="undefined"&&typeof console.log==="function") console.log(JSON.stringify(result,null,2));
result;
