#!/usr/bin/env node
// LSPV-5/507 sweep: exact minimal transient payload thresholds of the fixed
// LSPV-4/560 /386 DAG under four register conventions. Each solve < 1 s.
// Usage (from repo root): node experiments/review/lspv5_507_sweep.cjs > out.json
'use strict';
const {solve}=require('./lspv5_507_peak_frontier_redteam.cjs');
const conv=[{CAP:4,OW:1},{CAP:35,OW:1},{CAP:4,OW:0},{CAP:5,OW:0},{CAP:35,OW:0},{CAP:3,OW:1}];
const out=[];
const pick=process.argv[2]===undefined?conv:[conv[+process.argv[2]]];
for(const c of pick){
  const row={...c,thresholds:{}};let prevRes=null;
  for(let P=29;P<=75;P++){
    const r=solve(P,c.CAP,c.OW,1);
    const res=r.feasible?r.res:null;
    if(res!==prevRes){row.thresholds[P]=r.feasible?{res:r.res,area:r.area}:'infeasible';prevRes=res;}
    if(res===35) break;
  }
  out.push(row);
}
// Hostile self-checks: confirm LSPV-4/565 published numbers
const h=[[40,null],[41,[36,793]],[44,[36,760]],[45,[35,958]]].map(([P,e])=>{
  const r=solve(P,4,1,1);const got=r.feasible?[r.res,r.area]:null;
  return {P,expected:e,got,match:JSON.stringify(got)===JSON.stringify(e)};});
console.log(JSON.stringify({run:'LSPV-5/507',date:'2026-11-12 09:48 PST',
 scope:'fixed LSPV-4/560 /386 W38 DAG only; NOT all-proof, NOT R_mix341, NOT machine space',
 lspv4_565_reproduction:h,conventions:out},null,1));
