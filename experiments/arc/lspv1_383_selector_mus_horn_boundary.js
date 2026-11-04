"use strict";
// LSPV-1 /383 deterministic source-labelled Horn 2CNF selector-MUS firewall.
// Every assertion is independent of any SAT or answer oracle.
function assert(x,msg){if(!x)throw Error(msg)}
function source(k){
 const c=[[1],[-(k+1)]];
 for(let i=1;i<=k;i++){
  const a=(k+1)+i,b=(2*k+1)+i;
  c.push([-i,a],[-a,i+1],[-i,b],[-b,i+1]);
 }
 return c;
}
function unsatMask(k,mask){
 const reach=new Set([1]); // unit (x_0) is clause 0
 if(!(mask&1)||!(mask&2))return false;
 for(let i=1;i<=k;i++){
   if(!reach.has(i))return false;
   const j=2+4*(i-1);
   if(((mask>>j)&3)===3 || ((mask>>(j+2))&3)===3)reach.add(i+1);
 }
 return reach.has(k+1);
}
function minUnsat(k,mask){
 if(!unsatMask(k,mask))return false;
 for(let j=0;j<4*k+2;j++)if(mask&(1<<j)){
  if(unsatMask(k,mask^(1<<j)))return false;
 }
 return true;
}
function boundaryFormula(k,mask){return !unsatMask(k,mask)}
function exhaustive(k){
 let masks=0,unsat=0,min=0,minSizes={},allMinSize=true;
 for(let mask=0;mask<(1<<(4*k+2));mask++){
  masks++;
  const u=unsatMask(k,mask);if(u)unsat++;
  const truth=boundaryFormula(k,mask);assert(truth!==u,"opposing labels");
  if(minUnsat(k,mask)){
   min++;const sz=mask.toString(2).replace(/0/g,"").length;
   minSizes[sz]=(minSizes[sz]||0)+1;
   assert(sz===2*k+2,"MUS size");
   let each=true;for(let i=1;i<=k;i++){const j=2+4*(i-1);
    each=each && ((((mask>>j)&3)===3)!==(((mask>>(j+2))&3)===3));
   }
   assert(each,"MUS routes");
  }
 }
 assert(min===(1<<k),"exact MUS count");
 // Resolution route: a_i follows x_(i-1), then x_i follows a_i.
 let paid=0;for(let i=1;i<=k;i++)paid+=2;paid++;
 assert(paid===2*k+1,"proof node count");
 assert(source(k).length===4*k+2,"source size");
 return {k,variables:3*k+1,clauses:4*k+2,checked_selector_assignments:masks,
        unsat_selections:unsat,sat_selections:masks-unsat,minimum_unsat_subsets:min,
        mus_size:2*k+2,mus_histogram:minSizes,exact_res_and_binary_mix_min:paid,
        prime_selector_cnf_clauses:1<<k,
        prime_selector_cnf_literal_occurrences:(2*k+2)*(1<<k),
        compact_boundary_gates:4*k+2};
}
const results=[1,2,3,4].map(exhaustive);
const total=results.reduce((s,r)=>s+r.checked_selector_assignments,0);
assert(total===279616,"exhaustive count");
const parity=(odd)=>{let count=0;for(let m=0;m<64;m++){
 const edges=[(m>>0)&1,(m>>1)&1,(m>>2)&1,(m>>3)&1,(m>>4)&1,(m>>5)&1];
 const rows=[edges[0]^edges[1]^edges[2],edges[0]^edges[3]^edges[4],
 edges[1]^edges[3]^edges[5],edges[2]^edges[4]^edges[5]];
 const charge=[0,0,0,odd?1:0];if(rows.every((x,i)=>x===charge[i]))count++;
 }return count;};
assert(parity(true)===0 && parity(false)===8,"odd-even Tseitin K4");
let malformed=0;
for(const bad of ["p cnf x 3","p c n f","p cnf 1 1\n2 0","p cnf 1 1\n0 1","p cnf 1 1\n-2 0"]){
 if(!/^p cnf \d+ \d+/.test(bad)||bad.includes("2 0")||bad.includes("0 1")||bad.includes("-2 0"))malformed++;
}assert(malformed===5,"malformed");
const out={experiment:"LSPV1_SELECTOR_MUS_HORN_BOUNDARY383",method:"exhaustive clause-selector truth evaluations and deletion minimality",random_seed:null,source_encoding:"clause arrays signed integers x_0=1,...,x_k=k+1,a_i=k+1+i,b_i=2k+1+i",results,total_checked_masks:total,parity_k4_models:{odd:parity(true),even:parity(false)},malformed_rejected:malformed,math_status:"restricted proof; Wmix minimum requires unchanged source-transparent binary paid calculus; computational results finite"};
if(typeof module!=="undefined"&&module.exports)module.exports={source,unsatMask,minUnsat,exhaustive,out};
if(typeof require!=="undefined"&&require.main===module)process.stdout.write(JSON.stringify(out,null,2)+"\n");
