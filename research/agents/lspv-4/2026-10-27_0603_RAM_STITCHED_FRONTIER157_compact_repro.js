"use strict";
/* RAT-STITCHED-FRONTIER157, compact independent Node.js reproducer.
   Run: node 2026-10-27_0603_RAM_STITCHED_FRONTIER157_compact_repro.js
   Deterministic, no dependencies, no randomness.
   The table is transcribed from Buss-Williams original ECCC TR11-031
   figures 2-3; numerical checks are NOT proofs of SAT lower bounds. */
const ROWS=[
 [0.001,1.80083,1.80084,11,455],
 [0.010,1.79092,1.79093,11,278],
 [0.100,1.69618,1.69619,26,435],
 [0.250,1.55242,1.55243,33,297],
 [0.500,1.34070,1.34071,44,406],
 [0.750,1.15765,1.15766,27,167],
 [0.900,1.06011,1.06012,19,88],
 [0.990,1.00583,1.00584,7,20],
 [0.999,1.00058,1.00059,24,10]
];
const PHI=(1+Math.sqrt(5))/2, GAMMA=2*Math.cos(Math.PI/7);
let tests=0;
function check(condition,message){tests++; if(!condition)throw new Error(message);}
function beta(c){return ((c+2)/(c*c)-c)/2;}
function inverse(s){
  check(s>=0&&s<1,"inverse range");
  let lo=1,hi=2;
  for(let j=0;j<90;j++){
    const mid=(lo+hi)/2;
    if(beta(mid)>s)lo=mid;else hi=mid;
  }
  return (lo+hi)/2;
}
function point(s){
  let bw=0,which=null;
  for(const row of ROWS)if(s<row[0]&&row[1]-1e-4>bw){
    bw=row[1]-1e-4; which=row[0];
  }
  const candidates=[
    ["FLMV_cor_5_8",inverse(s)],
    ["Williams_phi_product",PHI-s],
    ["Buss_Williams_certified_strict",bw],
    ["trivial_input",1]
  ];
  if(s===0)candidates.push(["Williams_cosine_subpoly_only",GAMMA]);
  candidates.sort((a,b)=>b[1]-a[1]);
  return {sigma:s,BW_strict_eligible:which,BW_bound:bw,FLMV_inverse:inverse(s),
    Williams_phi:PHI-s,certified_lower:candidates[0][1],
    active_source:candidates[0][0]};
}
function run(){
  check(Math.abs(PHI-1.618033988749895)<1e-13,"phi");
  check(Math.abs(GAMMA-1.801937735804838)<1e-13,"gamma");
  check(11642479*2>23232400,"FLMV rational strict 1/2");
  const c=241/200, rational=11642479/23232400;
  check(Math.abs(beta(c)-rational)<1e-14,"FLMV rational equality");
  for(const row of ROWS){
    check(row[1]<row[2],"yes before no");
    check(Math.abs(row[2]-row[1]-0.00001)<1e-8,"step 1e-5");
    check(row[3]>0&&row[4]>0,"finite original search rounds/triples");
    check(row[1]-0.0001>1,"positive strict certified c");
  }
  const cases=[0,0.001,0.01,0.10,0.249,0.25,0.251,0.49,0.499,
       0.5,0.501,0.6,0.749,0.75,0.899,0.9,0.989,0.99,0.999];
  const chart=cases.map(point);
  for(const x of chart){
    check(beta(x.FLMV_inverse)>0 || x.sigma===0,"inverse positive");
    check(Math.abs(beta(x.FLMV_inverse)-x.sigma)<1e-12,"inverse residual");
    check(x.certified_lower>=x.FLMV_inverse-1e-12,"envelope FLMV");
    check(x.certified_lower>=x.Williams_phi-1e-12,"envelope phi");
  }
  check(point(0.25).active_source==="Williams_phi_product","strict endpoint .25");
  check(point(0.5).active_source==="FLMV_cor_5_8","strict endpoint .5");
  check(point(0).active_source==="Williams_cosine_subpoly_only","subpoly only");
  check(point(0.49).active_source==="Buss_Williams_certified_strict","row .5 eligible");
  check(point(0.25).BW_strict_eligible===0.5,"same row .25 ineligible");
  check(point(0.5).BW_strict_eligible===0.75,"same row .5 ineligible");
  for(let k=0;k<9;k++){
    const row=ROWS[k];
    check(point(row[0]).BW_strict_eligible!==row[0],"strict epsilon equality");
    const justBelow=row[0]-1e-8;
    check(point(justBelow).BW_bound>=row[1]-0.0001001,
          "positive epsilon slack");
  }
  const winners={}; let previous=Infinity;
  for(let j=0;j<1000;j++){
    const s=j/1000,x=point(s);
    check(x.certified_lower>=1,"trivial time");
    check(x.certified_lower<=previous+1e-8,"envelope monotonic");
    previous=x.certified_lower;
    winners[x.active_source]=(winners[x.active_source]||0)+1;
  }
  check(winners.Williams_cosine_subpoly_only===1,"isolated subpoly cosine");
  check(winners.Buss_Williams_certified_strict===696,"sampled BW dominance");
  check(winners.FLMV_cor_5_8===275,"sampled FLMV dominance");
  check(winners.Williams_phi_product===28,"sampled phi dominance");
  return {id:"RAT-STITCHED-FRONTIER157",status:"COMPUTATIONAL only; source theorem is external",
    reproducibility:"deterministic; no seed; Node.js >=16",tests,errors:0,
    rows:ROWS.map(r=>({epsilon:r[0],Yes:r[1],No:r[2],
       Yes_rounds:r[3],Yes_triples:r[4],conservative_c:r[1]-0.0001})),
    selected:chart,dense_grid_winners:winners,
    strict_controls:{quarter:point(.25),half:point(.5)},
    limitations:"Compares established native RAT exclusion bounds only. Numerical sampling is not an asymptotic proof, RAM algorithm construction, or all-UNSAT certificate coverage. Strict epsilon and uniform effective proof cap required."};
}
if(typeof require!=="undefined"&&typeof module!=="undefined"&&require.main===module){
  console.log(JSON.stringify(run(),null,2));
}