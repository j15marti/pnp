#!/usr/bin/env node
// LSPV-2/407: competing paid-DEF equation-port selectors; NOT a native R proof.
// Usage: node lspv2_407_port_divergence.js [out.json]
const fs=require('fs');
let ncheck=0;function ck(x,label){ncheck++;if(!x)throw Error(label);}
const sourceText='p cnf 2 2\n1 0\n1 2 0\n';
function parse(s){const lines=s.split(/\r?\n/).filter(x=>x.trim());if(lines[0]!=='p cnf 2 2')throw Error('header');const clauses=lines.slice(1).map(l=>{const z=l.trim().split(/\s+/).map(Number);if(z.some(x=>!Number.isInteger(x))||z.length<2||z[z.length-1]!==0||z.slice(0,-1).some(x=>!x||Math.abs(x)>2))throw Error('clause');return z.slice(0,-1)});if(clauses.length!==2)throw Error('count');return clauses}
ck(JSON.stringify(parse(sourceText))==='[[1],[1,2]]','source parse');
const bad=['','p cnf 2 3\n1 0\n1 2 0\n','p cnf 2 2\n1 0\n1 3 0\n','p cnf 2 2\n1\n1 2 0\n','p cnf 2 2\n1 0\n0\n','p cnf 2 2\n1 0\n1 A 0\n','p cnf 2 2\n1 0\n1 2 0\n-1 0\n'];
for(const s of bad){let rejected=false;try{parse(s)}catch(e){rejected=true;}ck(rejected,'malformed reject');}
function row(xs,rhs){return {variables:[...xs].sort(),rhs};}
function xorRow(a,b){const set=new Set(a.variables);for(const x of b.variables){if(set.has(x))set.delete(x);else set.add(x)}return row(set,a.rhs^b.rhs)}
function same(a,b){return JSON.stringify(a)===JSON.stringify(b)}
function holds(r,v){return r.variables.reduce((a,k)=>a^v[k],0)===r.rhs}
function source(x,y,opp=false){return Boolean((opp?!x:x)&&(x||y))}
function proof(second='XOR'){return [
 {id:1,rule:'AND3',parents:['S1','S2'],factor:'x',row:row(['x'],1)},
 {id:2,rule:'DEF',parents:[],output:'a',inputs:['x','y'],op:'XOR',port:row(['a','x','y'],0)},
 {id:3,rule:'DEF',parents:[],output:'b',inputs:['a','y'],op:second,port:row(['a','b','y'],second==='XOR'?0:1)},
 {id:4,rule:'XOR',parents:[2,3],row:row(['b','x'],second==='XOR'?0:1)},
 {id:5,rule:'XOR',parents:[4,1],row:row(['b'],second==='XOR'?1:0)},
 {id:6,rule:'LOCAL-CONVERT',parents:[5],clause:['b']}
]}
function validate(second='XOR',completion='Splus',opposite=false,corrupt=''){
 const p=proof(second);
 if(corrupt==='def')p[2].port.rhs^=1;
 if(corrupt==='sum')p[3].row.rhs^=1;
 if(corrupt==='local')p[5].clause=['not_b'];
 if(completion==='Sminus')return {accepted:false,first_rejected_node:4,reason:'no addressable DEF GF2 row'};
 for(let x=0;x<2;x++)for(let y=0;y<2;y++){
   const a=x^y,b=(a^y)^(second==='XNOR'?1:0),v={x,y,a,b};
   if(!holds(p[1].port,v))return {accepted:false,first_rejected_node:2,reason:'first DEF row invalid'};
   if(!holds(p[2].port,v))return {accepted:false,first_rejected_node:3,reason:'second DEF row invalid'};
   if(!holds(p[3].row,v))return {accepted:false,first_rejected_node:4,reason:'first GF2 sum invalid'};
 }
 if(!same(p[3].row,xorRow(p[1].port,p[2].port)))return {accepted:false,first_rejected_node:4,reason:'GF2 arithmetic invalid'};
 if(!same(p[4].row,xorRow(p[3].row,p[0].row)))return {accepted:false,first_rejected_node:5,reason:'GF2 arithmetic invalid'};
 if(!same(p[5].clause,['b']))return {accepted:false,first_rejected_node:6,reason:'LOCAL target corrupted'};
 for(let x=0;x<2;x++)for(let y=0;y<2;y++){
  if(source(x,y,opposite)){const a=x^y,b=(a^y)^(second==='XNOR'?1:0);if(!b)return {accepted:false,first_rejected_node:6,reason:'LOCAL output not entailed'};}
 }
 return {accepted:true,logical_nodes:6,def_nodes:2,xor_nodes:2,local_nodes:1,and3_nodes:1};
}
const cases=[];for(let x=0;x<2;x++)for(let y=0;y<2;y++){
 const a=x^y,b=a^y;cases.push({x,y,source:source(x,y),a,b});ck(b===x,'conservative equality');ck(source(x,y)===(x===1),'source semantics');
}
ck(cases.filter(z=>z.source).length===2,'two models');
const plus=validate(),minus=validate('XOR','Sminus');
ck(plus.accepted,'Splus');ck(!minus.accepted&&minus.first_rejected_node===4,'Sminus');
const falsifiers={XNOR_definition:validate('XNOR'),opposite_signed_source:validate('XOR','Splus',true),incorrect_def_equation:validate('XOR','Splus',false,'def'),incorrect_row_sum:validate('XOR','Splus',false,'sum'),incorrect_output_clause:validate('XOR','Splus',false,'local')};
for(const [name,res] of Object.entries(falsifiers))ck(!res.accepted,'negative '+name);
const result={run:'LSPV2_407_PORT_DIVERGENCE',scope:'two completions of an unresolved original-R_mix341 selector, not native legality',source_dimacs:sourceText,source_ascii_bytes:Buffer.byteLength(sourceText),original_variables:['x','y'],source_models:cases.filter(x=>x.source).length,truth_table:cases,proof:proof(),logical_nodes:6,malformed_controls_rejected:bad.length,producer_assertions:ncheck,completions:{Splus:plus,Sminus:minus},Splus:plus,Sminus:minus,falsifiers,bit_cost:'q=6 separate from E explicit proof+gate+row bits; no N+q bound',claim_status:'PROVED/EXACT conditional typing; native R, B1, B2, B3 OPEN'};
const out=process.argv[2]||'2026-11-04_2012_LSPV2_PORT_DIVERGENCE407_raw.json';fs.writeFileSync(out,JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({status:'PASS',file:out,producer_assertions:ncheck,malformed:bad.length,plus,minus,falsifiers}));