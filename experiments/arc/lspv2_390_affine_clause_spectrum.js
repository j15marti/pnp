#!/usr/bin/env node
"use strict";
// LSPV-2/390: explicit affine CNF source-clause deletion spectrum.
// Source model: each row (mask,b) is expanded into every forbidden parity word.
// No SAT oracle, no adaptive solver, no new Rmix341 rule.
const fs=require("fs");
function check(x,msg){if(!x)throw Error(msg||"check failed")}
function rank(v){let basis=new Map();for(let w of v){while(w){let b=31-Math.clz32(w);if(basis.has(b))w^=basis.get(b);else{basis.set(b,w);break}}}return basis.size}
function consistent(R,n){return rank(R.map(([a,b])=>a|(b<<n)))===rank(R.map(([a,b])=>a))}
function projection(R,n,mask){let a=R.map(x=>x[0]),e=[];for(let j=0;j<n;j++)if((mask>>j)&1)e.push(1<<j);return rank(a.concat(e))-rank(a)}
function parity(x){let b=0;while(x){b^=1;x&=x-1}return b}
function clauses(R,n){let out=[];R.forEach(([mask,b],i)=>{const ids=[];for(let j=0;j<n;j++)if(mask&(1<<j))ids.push(j);for(let w=0;w<2**ids.length;w++)if(parity(w)!==b)out.push({i,w,ids})});return out}
function falsifies(a,c){return c.ids.reduce((x,j,k)=>x|(((a>>j)&1)<<k),0)===c.w}
function analyze(n,R,{brute=true}={}){
 check(n>0&&n<30&&R.every(([m,b])=>Number.isInteger(m)&&m>0&&m<(1<<n)&&(b===0||b===1)),"malformed affine rows");
 const cs=clauses(R,n);if(consistent(R,n))return {label:"SAT",models:n<=12?Array.from({length:1<<n},(_,a)=>a).filter(a=>R.every(([m,b])=>parity(a&m)===b)).length:null};
 let spectrum=[],sensitive=0,essential=0;
 R.forEach(([mask,b],i)=>{
  const rest=R.filter((_,j)=>i!==j),width=popcount(mask),size=2**(width-1),ok=consistent(rest,n);
  let r=ok?projection(rest,n,mask):null,e=ok?2**r:0;
  check(!ok||r<=width-1,"row projection exceeded parity hyperplane");
  spectrum.push({row:i,width,total:size,essential:e,projected_dimension:r,other_rows_consistent:ok});
  sensitive+=width*e;essential+=e;
  if(brute&&n<=12){
   const local=cs.filter(c=>c.i===i);
   let bruteE=0;for(const c of local){
    let witness=-1;
    for(let a=0;a<(1<<n);a++)if(cs.every(d=>d===c||!falsifies(a,d))){witness=a;break}
    if(witness>=0){bruteE++;check(falsifies(witness,c),"invalid deletion witness")}
   }
   check(e===bruteE,"rank/pattern deletion mismatch");
  }
 });
 return {label:"UNSAT",M:cs.length,E:essential,sensitive_occurrences:sensitive,spectrum};
}
function popcount(x){let n=0;while(x){x&=x-1;n++}return n}
const fixtures=[
 ["odd_xor_triangle",3,[[3,1],[6,1],[5,1]]],
 ["mixed_4v_circuit",4,[[7,1],[9,1],[14,1]]],
 ["mixed_5v_circuit",5,[[7,1],[28,1],[9,1],[18,0]]],
 ["rank_failure_control",4,[[7,1],[13,1],[3,1],[9,0]]],
 ["duplicate_inconsistent",3,[[1,0],[1,1],[1,0]]],
 ["redundant_odd_triangle",3,[[3,1],[6,1],[5,1],[1,1]]],
 ["even_xor_triangle",3,[[3,1],[6,1],[5,0]]]
];
const named=fixtures.map(([name,n,rows])=>({name,n,rows,...analyze(n,rows)}));
let agg={total:0,sat:0,unsat:0,essential:0,clauses:0,row_checks:0};
const opts=[];for(let m=1;m<=7;m++)for(let b=0;b<=1;b++)opts.push([m,b]);
for(let k=2;k<=4;k++){function visit(prefix,start){if(prefix.length===k){let R=prefix.map(i=>opts[i]),v=analyze(3,R,{brute:false});agg.total++;if(v.label==="SAT")agg.sat++;else{agg.unsat++;agg.essential+=v.E;agg.clauses+=v.M;agg.row_checks+=k}return}for(let i=start;i<opts.length;i++)visit(prefix.concat(i),i)}visit([],0)}
check(agg.total===3045&&agg.sat===1834&&agg.unsat===1211&&agg.essential===2846&&agg.row_checks===4704,"regression");
const out={schema:"LSPV2_AFFINE_SPECTRUM_390_V1",named,exhaustive:agg,labels:"B1 B2 B3 and P versus NP OPEN"};
const asText=JSON.stringify(out,null,2)+"\n";
if(process.argv[2])fs.writeFileSync(process.argv[2],asText);else process.stdout.write(asText);
