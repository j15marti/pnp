#!/usr/bin/env node
'use strict';
const benchmark304=function benchmark304(){
 const P=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9]],Q=[[4,6,8],[1,6,7],[2,3,4],[3,5,8],[1,2,9],[5,7,9]],F=P.concat(Q.map(c=>c.map(v=>-v)));
 const residual=p=>F.filter(c=>!c.some(l=>p[Math.abs(l)]!==undefined&&p[Math.abs(l)]===(l>0?1:0))).map(c=>c.filter(l=>p[Math.abs(l)]===undefined));
 function solve(C){
  let nodes=0,clause_tests=0,literal_tests=0,unit_elims=0,branches=0,assignments=[];
  function evaluate(cs,route){
   nodes++;
   while(true){
    let unit=null,hasEmpty=false;
    for(const clause of cs){clause_tests++;literal_tests+=clause.length;if(clause.length===0)hasEmpty=true;else if(clause.length===1&&unit===null)unit=clause[0]}
    if(hasEmpty)return false;
    if(cs.length===0){assignments=route.slice();return true}
    if(unit===null)break;
    unit_elims++;route=route.concat([unit]);cs=cs.filter(c=>{clause_tests++;return !c.includes(unit)}).map(c=>{literal_tests+=c.length;return c.filter(x=>x!==-unit)});
   }
   const x=cs[0][0];branches++;
   for(let l of [x,-x]){
    const next=cs.filter(c=>{clause_tests++;return !c.includes(l)}).map(c=>{literal_tests+=c.length;return c.filter(y=>y!==-l)});
    if(evaluate(next,route.concat([l])))return true;
   }
   return false;
  }
  const sat=evaluate(C,[]);
  return {label:sat?'SAT':'UNSAT',nodes,branches,unit_eliminations:unit_elims,clause_inspections:clause_tests,literal_inspections:literal_tests,complete_assignment_literals:assignments};
 }
 const s=solve(residual({1:0,2:0,8:1,9:1})),u=solve(residual({3:0,6:1,7:1,9:1}));
 if(s.label!=='SAT'||u.label!=='UNSAT')throw Error("failed baseline labels");
 return {status:"PASS",source:"same original valid canonical F9, noncanonical raw cofactors",SAT:s,UNSAT:u,gate:"No optional prepass, selected work; full source grammar and end-to-end FLMV steps separately charged",proof:"UP-DPLL all-or-branch exact recursion; UNSAT root if both branches fail",P_versus_NP:"OPEN"};
};
console.log(JSON.stringify(benchmark304(),null,2));
