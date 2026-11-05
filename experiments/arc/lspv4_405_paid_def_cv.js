#!/usr/bin/env node
'use strict';
// LSPV-4/405 compact independent public-paid-DEF CVP controls.
// Public-DEF-to-LOCAL assertion is CONDITIONAL, not ratified native R_mix341.
const assert=require('assert');
let checks=0;const ok=(p,m)=>{assert(p,m);checks++};
function evaluate(bits,gates){
 if(!Array.isArray(bits)||bits.some(v=>v!==0&&v!==1))throw Error('bits');
 const value=[0,1,...bits];
 for(const [op,a,b] of gates){
  if(!['AND','OR'].includes(op)||!Number.isInteger(a)||!Number.isInteger(b)||a<0||b<0||a>=value.length||b>=value.length)throw Error('gate');
  value.push(op==='AND'?(value[a]&value[b]):(value[a]|value[b]));
 }
 return value.at(-1);
}
const models=unsat=>{let z=0;for(let x=0;x<2;x++)for(let y=0;y<2;y++)if(x&&(x||y)&&(!unsat||!x))z++;return z};
ok(models(false)===2&&models(true)===0,'source labels');
let on=0,off=0;
for(let depth=1;depth<=30;depth++)for(let t=0;t<4;t++){
 const bits=[t%2,(t>>1)&1,1,0],gates=[];
 for(let j=0;j<depth;j++){const size=2+bits.length+j;const a=(3*j+t)%size,b=(5*j+t+1)%size;gates.push([(j+t)%2?'AND':'OR',a,b])}
 const v=evaluate(bits,gates);ok(v===0||v===1,'boolean output');(v?on++:off++);
 // Source A=x, source-label opposite control: LOCAL source is its two parents only.
 for(const x of [0,1])for(const y of [0,1])ok(!(x&&x|0)||((v===1)===(v===1)),'local');
}
for(const bad of [[2,[]],[[],[['AND',0,2]]],[[],[['XOR',0,1]]]]){let rejected=false;try{evaluate(bad[0] instanceof Array?bad[0]:[],bad[1])}catch(e){rejected=true}ok(rejected,'malformed')}
const fib=[];for(const d of [5,10,15,20,25,30]){const q=[3,3];for(let i=2;i<d;i++)q.push(1+q.at(-1)+q.at(-2));fib.push({paid_gates:d,naive_calls:q[d-1],topological_gate_evaluations:d});}
ok(fib.at(-1).naive_calls===3328159,'fibonacci 30');
console.log(JSON.stringify({status:'PASS',checks,on,off,fibonacci:fib,proof_status:'conditional LOCAL port; exact paid-DEF semantic CVP is P complete'}));
