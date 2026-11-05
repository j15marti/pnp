"use strict";
// LSPV-2/419: fully deterministic, no dependencies, bounded control experiment.
// This is a semantic circuit-support test, NOT a native R_mix341 proof checker.
function assert(cond,msg){if(!cond)throw Error(msg);}
function clauseValue(clause, assignment){
  if(!Array.isArray(clause))throw Error("bad clause"); // Empty clause is legal and false.
  return clause.some(lit=>{
    if(!Number.isInteger(lit)||lit===0)throw Error("bad literal");
    const v=Math.abs(lit)-1;
    if(v>=assignment.length)throw Error("undeclared variable");
    return lit>0?assignment[v]===1:assignment[v]===0;
  });
}
function cnfValue(clauses,assignment){
  if(!Array.isArray(clauses))throw Error("bad CNF");
  return clauses.every(c=>clauseValue(c,assignment));
}
function assignmentFromInt(z,n){return Array.from({length:n},(_,i)=>(z>>i)&1);}
function support(fn,n){
 const answer=[];
 for(let j=0;j<n;j++){
   let pair=null;
   for(let z=0;z<(1<<n);z++){
     if(z&(1<<j))continue;
     const a=assignmentFromInt(z,n),b=assignmentFromInt(z|(1<<j),n);
     if(fn(a)!==fn(b)){pair={variable:j,low:z,high:z|(1<<j)};break;}
   }
   if(pair)answer.push(pair);
 }
 return answer;
}
function fullClauses3(){
 return Array.from({length:8},(_,forbidden)=>
   Array.from({length:3},(_,j)=>((forbidden>>j)&1)?-(j+1):(j+1)));
}
function run(){
 const basis=fullClauses3();let checks=0,sat=0,unsat=0;
 let distribution={};
 const cases=[];
 for(let mask=0;mask<256;mask++){
   const clauses=basis.filter((c,i)=>(mask&(1<<i))!==0);
   let models=0;
   for(let z=0;z<8;z++)models+=Number(cnfValue(clauses,assignmentFromInt(z,3)));
   const g=x=>cnfValue(clauses,x.slice(0,3));
   const h=a=>g(a)&&a.slice(3,7).every(Boolean);
   const witnesses=support(h,7);
   const declaredSmall=witnesses.length<=3;
   assert(declaredSmall===(models===0),"reduction failed for mask "+mask);checks++;
   for(let j=3;j<7;j++){
     assert((models===0)===(!witnesses.some(w=>w.variable===j)),"y witness error");checks++;
   }
   for(const w of witnesses){
     let a=assignmentFromInt(w.low,7),b=assignmentFromInt(w.high,7);
     assert(h(a)!==h(b),"invalid essential variable witness");checks++;
   }
   if(models) sat++;else unsat++;
   distribution[witnesses.length]=(distribution[witnesses.length]||0)+1;
   if([0,1,127,254,255].includes(mask))
      cases.push({mask,source_label:models?"SAT":"UNSAT",models,essential_support:witnesses.map(w=>w.variable),witnesses});
 }
 assert(sat===255&&unsat===1,"unexpected exhaustive labels");checks++;
 // Deep conservative XOR definitions. Every input has a unique gate extension.
 let cancellation=[];
 for(let k=2;k<=7;k++){
   const evalCircuit=bits=>{
     let a=bits[0],gates=0;
     for(let i=1;i<k;i++){a^=bits[i];gates++;}
     for(let i=k-1;i>=1;i--){a^=bits[i];gates++;}
     return {output:a,gates};
   };
   let outputSupport=support(bits=>evalCircuit(bits).output,k);
   assert(outputSupport.length===1&&outputSupport[0].variable===0,"XOR cancellation failure");checks++;
   for(let z=0;z<(1<<k);z++){
     const x=assignmentFromInt(z,k),v=evalCircuit(x);
     assert(v.output===x[0]&&v.gates===2*(k-1),"bad nested gate extension");checks++;
   }
   cancellation.push({original_inputs:k,paid_XOR_definitions:2*(k-1),transitive_source_count:k,essential_source_count:1});
 }
 // Adversarial controls: a single changed gate breaks identity.
 const altered=bits=>((bits[0]^bits[1])&bits[1])^bits[1];
 assert(support(altered,2).length!==1 || support(altered,2)[0].variable!==0,"mutated circuit escaped");checks++;
 // Correct general-CNF semantics: an empty clause is a valid UNSAT clause.
 assert(cnfValue([[]],[1,0,0])===false,"empty clause not handled");checks++;
 for(const malformed of [[[0]],[[4]],[[1.2]],"invalid",[[1],null]]){
   let rejected=false;try{cnfValue(malformed,[1,0,0]);}catch(e){rejected=true;}
   assert(rejected,"bad CNF accepted");checks++;
 }
 return {id:"LSPV2_419_ESSENTIAL_SUPPORT_FIREWALL",status:"PROVED theorem + COMPUTATIONAL finite controls",n_original_G:3,full_width3_clauses:8,cnf_subsets:256,sat,unsat,support_distribution:distribution,assertions:checks,selected_cases:cases,cancellation,model:"boolean circuits with paid conservative two-input definitions; essential support is extensional, source (w) stays SAT; no native LOCAL export authorization assumed",claim:"deciding essential original-variable support <=3 for succinct circuits is coNP-complete; gate syntactic cones are efficiently checkable but can overapproximate essential support",limitations:"finite tests are not lower bounds for R_mix341 node counts, machine time, or B3"};
}
if(typeof module!=="undefined" && typeof require!=="undefined" && require.main===module)console.log(JSON.stringify(run(),null,2));
