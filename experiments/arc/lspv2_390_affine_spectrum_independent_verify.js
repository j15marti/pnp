#!/usr/bin/env node
"use strict";
// INDEPENDENT truth-table verifier for LSPV-2/390, no linear algebra.
const fs=require("fs");
const data=JSON.parse(fs.readFileSync(process.argv[2]||"results/raw/arc/2026-11-04_0512_LSPV2_AFFINE_SPECTRUM390_raw.json","utf8"));
let checks=0;
function assert(x,msg){checks++;if(!x)throw Error(msg)}
function parity(x){let p=0;while(x){p^=1;x&=x-1}return p}
function sources(rows,n){
 const cs=[];
 rows.forEach(([mask,b],i)=>{const support=[];for(let j=0;j<n;j++)if((mask>>j)&1)support.push(j);
 for(let w=0;w<(1<<support.length);w++)if(parity(w)!==b)cs.push({i,support,w});
 });return cs;
}
function falseOn(a,c){return c.support.reduce((v,j,k)=>v|(((a>>j)&1)<<k),0)===c.w}
function examine(r){
 const {n,rows}=r;assert(Number.isInteger(n)&&n>0&&n<20&&rows.every(([m,b])=>m>0&&m<(1<<n)&&(b===0||b===1)),"invalid");
 const cs=sources(rows,n), assignments=Array.from({length:1<<n},(_,a)=>a);
 const models=assignments.filter(a=>rows.every(([m,b])=>parity(m&a)===b));
 if(r.label==="SAT"){assert(models.length===r.models,"SAT model mismatch");return}
 assert(models.length===0&&r.M===cs.length,"UNSAT or M mismatch");
 let E=0,S=0;
 rows.forEach(([m,b],i)=>{
   const local=cs.filter(c=>c.i===i),rest=rows.filter((_,j)=>j!==i);
   const projections=new Set();
   for(const a of assignments)if(rest.every(([mask,bit])=>parity(mask&a)===bit)){
     projections.add(local[0].support.reduce((w,j,k)=>w|(((a>>j)&1)<<k),0));
   }
   let essential=0;
   for(const c of local){
     const witness=assignments.find(a=>cs.every(other=>other===c||!falseOn(a,other)));
     if(witness!==undefined){
       essential++;
       assert(falseOn(witness,c),"source deletion failure");
       for(let k=0;k<c.support.length;k++){
         const flip={support:c.support,w:c.w^(1<<k)};
         assert(!falseOn(witness,flip),"source signed flip failed");
       }
     }
   }
   const row=r.spectrum[i];
   assert(row.essential===essential&&row.total===local.length,"row essential mismatch");
   assert(row.other_rows_consistent===(projections.size>0),"deletion consistency mismatch");
   assert(projections.size===essential,"independent affine image differs from deleted-clause witnesses");
   if(projections.size>0)assert(2**row.projected_dimension===essential,"rank dimensionality mismatch");
   else assert(row.projected_dimension===null,"nonempty rank of empty image");
   E+=essential;S+=essential*local[0].support.length;
 });
 assert(E===r.E&&S===r.sensitive_occurrences,"total sensitivity mismatch");
}
assert(data.schema==="LSPV2_AFFINE_SPECTRUM_390_V1","schema");
for(const r of data.named)examine(r);
let agg={total:0,sat:0,unsat:0,essential:0,clauses:0,row_checks:0};
const choices=[];for(let m=1;m<=7;m++)for(let b=0;b<=1;b++)choices.push([m,b]);
for(let len=2;len<=4;len++){
 function recur(start,idx){
 if(idx.length<len){for(let i=start;i<choices.length;i++)recur(i,idx.concat(i));return}
 const rows=idx.map(i=>choices[i]),cs=sources(rows,3);
 agg.total++;const assignments=Array.from({length:8},(_,a)=>a);
 if(assignments.some(a=>rows.every(([m,b])=>parity(a&m)===b))){agg.sat++;return}
 agg.unsat++;agg.clauses+=cs.length;agg.row_checks+=len;
 cs.forEach(c=>{if(assignments.some(a=>cs.every(d=>d===c||!falseOn(a,d))))agg.essential++});
 }
 recur(0,[]);
}
for(const k of Object.keys(agg))assert(agg[k]===data.exhaustive[k],"aggregate "+k);
const original=JSON.stringify(data.named[0]);
for(let idx=0;idx<5;idx++){
 const bad=JSON.parse(original);
 if(idx===0)bad.M++;
 if(idx===1)bad.E++;
 if(idx===2)bad.spectrum[0].projected_dimension++;
 if(idx===3)bad.label="SAT";
 if(idx===4)bad.sensitive_occurrences++;
 let rejected=false;try{examine(bad)}catch(e){rejected=true}
 assert(rejected,"forged certificate not rejected");
}
process.stdout.write(JSON.stringify({ok:true,checks,malformed_or_corrupt_rejections:5,aggregate:agg})+"\\n");
