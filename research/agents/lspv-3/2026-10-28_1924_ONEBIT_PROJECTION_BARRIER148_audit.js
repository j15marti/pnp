#!/usr/bin/env node
"use strict";
/* LSPV-3 ONEBIT-PROJECTION-BARRIER148: independent finite audit.
 * Complete brute force over 255 nonempty subsets of the eight ternary
 * clauses on 3 variables. Auxiliary variable choices are checked exactly.
 * It is NOT a test of asymptotic coNP-completeness or a TM resource bound.
 */
function claim(ok,label) { if (!ok) throw Error(label); }
function lit(l,a) { return l>0 ? !!a[Math.abs(l)] : !a[Math.abs(l)]; }
function satClause(c,a) { return c.some(l=>lit(l,a)); }
function satF(F,a) { return F.every(c=>satClause(c,a)); }
function guardTest(F,a,y) {
  // For every source clause, enumerate both actual t_i settings.
  // The module has no shared t_i between source clauses.
  return F.every(c=>[false,true].some(t=>
    ((!y)||lit(c[0],a)||t)&&((!t)||lit(c[1],a)||lit(c[2],a))));
}
function truth(m) { return Array.from({length:3},(_,j)=>!(m&(1<<j))?j+1:-(j+1));}
function main() {
  let checks=0,sat=0,unsat=0,y0yes=0,y1yes=0,twoway=0;
  for(let subset=1;subset<256;subset++) {
    let F=Array.from({length:8},(_,i)=>i).filter(i=>subset&(1<<i)).map(truth);
    let projected=[false,false], original=false;
    for(let x=0;x<8;x++) {
      let a={};for(let i=1;i<=3;i++)a[i]=!!(x&(1<<(i-1)));
      let yes=satF(F,a); original ||=yes;
      for(let y=0;y<=1;y++) {
        let g=guardTest(F,a,!!y);
        projected[y] ||=g;
        // Literal 3-SAT variable elimination identity:
        // exists t [(not y or a or t) and (not t or b or c)]
        // iff not y or a or b or c.
        claim(g===((!y)||yes),"guard equivalence on complete X assignment");
        checks++;
      }
    }
    claim(projected[0]===true && projected[1]===original,"wrong projected relation");
    if(original) sat++;else unsat++;
    y0yes+=Number(projected[0]);y1yes+=Number(projected[1]);twoway++;
  }
  claim(sat===254 && unsat===1,"subset count");
  const W="-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14";
  let rows=W.split(";").map(row=>row.split(" ").map(Number));
  for(let i=1;i<=15;i++){
    claim(rows.flat().filter(z=>z===i).length===2,"W1 positive quota");
    claim(rows.flat().filter(z=>z===-i).length===2,"W1 negative quota");
    checks+=2;
  }
  let any=false; for(let mask=0;mask<(1<<15);mask++) {
    let a={};for(let v=1;v<=15;v++) a[v]=!!(mask&(1<<(v-1)));
    any ||=satF(rows,a);
  }
  claim(!any,"W1 is UNSAT"); checks++;
  return {status:"COMPUTATIONAL",guarded_formulas:twoway,guards_on_sat: sat,
      guards_on_unsat:unsat,projection_y0_yes:y0yes,
      projection_y1_yes:y1yes,W1_strict_signed_22:true,W1_unsat:true,
      brute_W1_assignments:32768,assertion_groups:checks+256+2,
      limitations:"Finite controls; no general SAT time lower bound, no claim P != NP"};
}
if(require.main===module)console.log(JSON.stringify(main(),null,2));
module.exports={main};
