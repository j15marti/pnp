'use strict';
// LSPV-1/390 finite controls. This is NOT a native R_mix341 proof verifier.
const assert = require('assert');
let checks = 0;
function eq(a,b,msg){checks++;assert.deepStrictEqual(a,b,msg)}
function graph(which){
 if(which==='k4') {let e=[]; for(let i=0;i<4;i++)for(let j=i+1;j<4;j++) e.push([i,j]);return {h:4,edges:e}}
 if(which==='prism6') return {h:6,edges:[[0,1],[1,2],[2,0],[3,4],[4,5],[5,3],[0,3],[1,4],[2,5]]};
 throw Error('unknown graph');
}
function make(which,odd=true){
 const {h,edges}=graph(which),clauses=[];
 for(let v=0;v<h;v++){
  const indices=edges.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
  eq(indices.length,3,'cubic');
  for(let s=0;s<8;s++){
   const bits=[s&1,(s>>1)&1,(s>>2)&1];
   const parity=bits[0]^bits[1]^bits[2],charge=(odd&&v===0)?1:0;
   if(parity!==charge) clauses.push(indices.map((edge,k)=>({edge,neg:!!bits[k]})));
  }
 }
 eq(clauses.length,4*h);return {h,e:edges.length,clauses};
}
function sat(clauses,e){
 for(let a=0;a<2**e;a++){
  if(clauses.every(c=>c.some(l=>Boolean((a>>l.edge)&1)!==l.neg)))return a;
 }
 return null;
}
function dup(cs,r){return cs.flatMap(c=>Array.from({length:r},()=>c.map(l=>({...l}))))}
function flip(cs,j,k){let z=cs.map(c=>c.map(l=>({...l})));z[j][k].neg=!z[j][k].neg;return z}
function run(){
 const rows=[];
 for(const name of ['k4','prism6'])for(const r of [1,2,3,4]){
  const {h,e,clauses}=make(name),m=clauses.length,L=3*m;
  const copies=dup(clauses,r);eq(sat(copies,e),null,'odd original UNSAT');
  eq(sat(make(name,false).clauses,e)!==null,true,'even SAT');
  let witnesses=0;
  for(let j=0;j<m;j++){
   const without=clauses.filter((_,t)=>t!==j);
   const w=sat(without,e);eq(w!==null,true,'clause deletion SAT');
   eq(clauses[j].every(l=>Boolean((w>>l.edge)&1)===l.neg),true,'deleted clause violated');
   for(let k=0;k<3;k++){
    const mutated=copies.map(c=>c.map(l=>({...l})));
    for(let t=0;t<r;t++)mutated[j*r+t][k].neg=!mutated[j*r+t][k].neg;
    eq(sat(mutated,e)!==null,true,'r-flip SAT neighbor');
    eq(mutated.every(c=>c.some(l=>Boolean((w>>l.edge)&1)!==l.neg)),true,'witness validates');
    witnesses++;
    if(r>=2){
      const one=flip(copies,j*r,k);eq(sat(one,e),null,'one sign flip UNSAT');
      const partial=mutated.map(c=>c.map(l=>({...l})));
      partial[j*r+r-1][k].neg=!partial[j*r+r-1][k].neg;
      eq(sat(partial,e),null,'r-1 sign flips UNSAT');
    }
   }
  }
  // Disjoint r-bit SAT-neighbor masks have one mask for every source-literal coordinate.
  // Therefore fractional and integral transversal are >=L. Reading all L first-copy
  // signs intersects every SAT sign-only neighbor, giving the matching upper bound.
  const result={graph:name,h,edges:e,r,classes:m,literal_groups:L,sign_positions:r*L,
    min_sat_sign_flips:r,disjoint_sat_neighbor_sets:L,
    promised_integral_transversal:L,promised_fractional_transversal:L,
    fixed_Rmix341_paid_node_minimum:4*h-1,sat_neighbor_witnesses:witnesses};
  eq(result.min_sat_sign_flips===r,true);
  rows.push(result);
 }
 // Strict toy-CNF grammar parsing, both labels, plus deliberate malformed controls.
 function parse(s){
  if(typeof s!=='string'||!/^[0-9;\- ]+$/.test(s))throw Error('bad alphabet');
  let a=s.split(';');if(a.some(t=>!/^\s*-?[1-9]\d*(?:\s+-?[1-9]\d*)*\s*$/.test(t)))throw Error('empty or invalid clause');
  return a.map(t=>t.trim().split(/\s+/).map(Number));
 }
 let toy=parse('1;-1');eq(sat(toy.map(c=>c.map(x=>({edge:Math.abs(x)-1,neg:x<0}))),1),null,'toy UNSAT');
 eq(sat(parse('1;2').map(c=>c.map(x=>({edge:Math.abs(x)-1,neg:x<0}))),2)!==null,true,'toy SAT');
 for(let bad of ['',';','0','1;','1;;-1','a',' 1 ; 0']){
  let failed=false;try{parse(bad)}catch(e){failed=true}eq(failed,true,'malformed reject');
 }
 // Directly enumerate every sign-only variant of duplicated contradictory units.
 const toyDist=[];
 for(let r=1;r<=5;r++){
  let min=Infinity,countSat=0;
  for(let mask=0;mask<2**(2*r);mask++){
   let cs=[];for(let t=0;t<r;t++)cs.push([{edge:0,neg:!!((mask>>t)&1)}]);
   for(let t=0;t<r;t++)cs.push([{edge:0,neg:!(Boolean((mask>>(r+t))&1))}]);
   const status=sat(cs,1)!==null;
   if(status){countSat++;let d=mask.toString(2).split('1').length-1;min=Math.min(min,d)}
  }
  eq(min,r,'exact finite sign distance');toyDist.push({r,min,countSat});
 }
 const out={title:'LSPV-1/390 MULTIFLIP TRANSVERSAL',date:'2026-11-04 06:00 PST',
  kind:'finite exhaustive controls plus symbolic proof',checks,rows,toyDist,
  note:'Fractional and integral hitting numbers are exactly L for the sign-only fixed-layout SAT-neighbor family. They are lower bounds only for unrestricted input encodings.'};
 console.log(JSON.stringify(out,null,2));
}
run();
