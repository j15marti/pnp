"use strict";
// TMR-1/007 supplementary gate-order counterexample, independently brute forced.
// Native command: node experiments/tmr/tmr1_gate_order_bowtie007.cjs
function bad(c){let q=[];for(let i=0;i<8;i++){let t=[(i>>2)&1,(i>>1)&1,i&1];if((t[0]^t[1]^t[2])!==c)q.push(t)}return q}
function one(order,b0,b6,q,tau){
 let examined=0;
 for(let mask=0;mask<512;mask++){
  examined++;
  const x={},y=[(mask>>6)&1,(mask>>7)&1,(mask>>8)&1];
  order.forEach((u,i)=>x[u]=(mask>>i)&1);
  if((x[1]^x[2]^x[3])!==0)continue;
  if((x[4]^x[5]^x[6])!==b6)continue;
  const es=order.map(u=>x[u]);
  const gates=[[es[0],es[1],y[0]],[y[0],es[2],y[1]],[y[1],es[3],y[2]],[y[2],es[4],es[5]]];
  let good=true;
  for(let i=0;i<4;i++){
   const c=i===3?b0:0;
   if(i===q){if(tau.some((z,k)=>z!==gates[i][k]))good=false}
   else if((gates[i][0]^gates[i][1]^gates[i][2])!==c)good=false;
  }
  if(good)return {sat:true,witness:{edge_by_neighbor:x,aux:y},examined};
 }
 return {sat:false,examined};
}
function audit(){
 const result={status:"COMPUTATIONAL",model:"two K4 sharing cutvertex 0; fixed odd-charge graph; independently brute force 2^9 local incident/aux configurations",checks:0,configurations_examined:0,cases:[],failures:0};
 const variants={blocked:[1,2,3,4,5,6],interleaved:[1,4,2,5,3,6]};
 for(let [label,order] of Object.entries(variants))for(let target of [0,6]){
  const b0=+(target===0),b6=+(target===6);
  let ok=0,fail=0,badClauses=[];
  for(let q=0;q<4;q++)for(let t of bad(q===3?b0:0)){
    const z=one(order,b0,b6,q,t);
    result.checks++;result.configurations_examined+=z.examined;
    if(z.sat)ok++;else {fail++;badClauses.push({gate:q,tuple:t})}
  }
  if(label==="blocked"&&(ok!==12||fail!==4))throw Error("blocked expected exactly 4 redundant clauses");
  if(label==="interleaved"&&(ok!==16||fail!==0))throw Error("interleaved expected all center clauses essential");
  result.cases.push({order:label,charge_vertex:target,center_deleted_clause_sat:ok,center_deleted_clause_unsat:fail,overall_deleted_clause_sat:ok+24,overall_deleted_clause_unsat:fail,original_variable_count:15,original_clause_count:40,encoded_length_bits:657,badClauses});
 }
 return result;
}
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(audit(),null,2));
if(typeof module!=="undefined")module.exports={audit};
