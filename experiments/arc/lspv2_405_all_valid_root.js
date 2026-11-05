#!/usr/bin/env node
'use strict';
// LSPV2/405: conditional explicit-root-payload U, NOT certified native syntax.
// Authenticated source p cnf 2 2; clauses (x),(x or y).
const assert=require('assert');
function build(k,flip=-1) {
  if(!Number.isInteger(k)||k<1)throw Error("invalid k");
  const gates=[["X"]], cells=[];
  for(let j=0;j<k;j++){cells.push(gates.length);gates.push(["K",j===flip?0:1]);}
  let t=cells[0];
  for(let j=1;j<k;j++){gates.push(["AND",t,cells[j]]);t=gates.length-1;}
  gates.push(["NOT",t]);const n=gates.length-1;
  gates.push(["OR",0,n]);return gates;
}
function value(gates,x) {
 const out=[];
 for(let i=0;i<gates.length;i++){
  const [op,a,b]=gates[i];
  if(op==="X"){assert(i===0);out.push(x);}
  else if(op==="K"){assert(a===0||a===1);out.push(a);}
  else if(op==="NOT"){assert(Number.isInteger(a)&&a>=0&&a<i);out.push(1-out[a]);}
  else if(op==="AND"||op==="OR"){
    assert([a,b].every(t=>Number.isInteger(t)&&t>=0&&t<i));
    out.push(op==="AND"?(out[a]&out[b]):(out[a]|out[b]));
  }else throw Error("invalid gate");
 }
 return out[out.length-1];
}
function rootTable(gates){
 let s='';
 for(const x of [0,1])for(const y of [0,1]){
  const parent=x&&(x||y);const root=value(gates,x);
  assert(!parent||root===1); s+=String(root);
 }
 return s;
}
let cases=[],neighbors=0;
for(let k of [1,2,3,5,8,16,32,64,128,256]){
 const base=build(k),tb=rootTable(base);assert(tb==="0011");
 for(let j=0;j<k;j++){const one=build(k,j);assert(rootTable(one)==="1111");neighbors++;}
 cases.push({k,paid_nodes:2,payload_gate_records:base.length,
            valid_one_bit_neighbors:k,base_truth_table:tb,neighbors_truth_table:"1111"});
}
// Three paid fresh XOR2 definitions. Attributed exact GF(2) rows:
// z+x+y=0, w+z+x=0, t+w+y=0; two paid row sums give w+y=0 then t=0.
const models=[];
for(let x of [0,1])for(let y of [0,1]){
 const z=x^y,w=z^x,t=w^y;
 assert(t===0);assert((z^x^y)===0);assert((w^z^x)===0);assert((t^w^y)===0);
 assert((x&&(x||y))===x);models.push({x,y,z,w,t});
}
assert(models.some(m=>m.x===1&&m.y===0&&m.w===0));
const raw={run:"LSPV2-405-ALL-VALID-ROOT/v1",scope:"conditional explicit LOCAL-CONVERT payload grammar U; not certified native R_mix341",source:"p cnf 2 2\n1 0\n1 2 0\n",source_sat:true,source_plus_negx_unsat:true,neighbors,tests:cases,nested_paid:{def:3,xor:2,and3:1,local:1,models},status:"COMPUTATIONAL finite checks; universal root-acquisition lemma has separate proof; B3 OPEN"};
console.log(JSON.stringify(raw,null,2));
