#!/usr/bin/env node
"use strict";
/* LSPV-1/533: independent finite degree/adder test, NOT R_mix341. */
const check=(p,m)=>{if(!p)throw Error(m);};
const mod=(a,q)=>(a%q+q)%q;
function tuples(q,n) {
  let out=[[]];
  for(let j=0;j<n;j++){out=out.flatMap(z=>Array.from({length:q},(_,x)=>z.concat(x)));}
  return out;
}
function charge(x,e,c,q){return +(mod(x.reduce((s,a,i)=>s+e[i]*a,0),q)===c);}
function run(){
 let cases=[],derivatives=0,pairs=0,valid=0,invalid=0;
 for(const [q,bmax] of [[3,7],[5,4],[7,3],[9,3]])for(let b=1;b<=bmax;b++){
  const c=mod(b+1,q),e=Array.from({length:b},(_,i)=>i%2?-1:1),xs=tuples(q,b);
  let ok=xs.filter(x=>charge(x,e,c,q)).length;
  check(ok===q**(b-1),"fiber size");valid+=ok;invalid+=xs.length-ok;
  // b-fold mixed derivative is zero for every polynomial of group-degree <b.
  let witness=null;
  for(const a of tuples(q-1,b)){
   let parity=0;
   for(let mask=0;mask<(1<<b);mask++){
    const x=Array(b).fill(q-1);
    for(let i=0;i<b;i++)if(mask&(1<<i))x[i]=a[i];
    parity^=charge(x,e,c,q);derivatives++;
   }
   if(parity){witness=a;break;}
  }
  check(witness!==null,"nonzero top-degree witness q="+q+" b="+b);
  for(let i=0;i<q;i++)for(let j=0;j<q;j++){
   const left=Array.from({length:q},(_,k)=>+(k===i));
   const right=Array.from({length:q},(_,k)=>+(k===j));
   const o=Array(q).fill(0);
   for(let x=0;x<q;x++)for(let y=0;y<q;y++)o[(x+y)%q]^=left[x]&right[y];
   check(o.reduce((a,b)=>a+b,0)===1&&o[(i+j)%q]===1,"adder");pairs++;
  }
  cases.push({q,b,c,signs:e,valid:ok,invalid:xs.length-ok,
   degree:b,top_degree_witness:witness,
   and3_depth_lower_bound:Math.ceil(Math.log(b)/Math.log(3)-1e-12),
   balanced_and2_depth_upper_bound:Math.ceil(Math.log2(b)-1e-12),
   and2_gates:q*q*(b-1),xor2_gates:q*(q-1)*(b-1)});
 }
 for(let b=2;b<=6;b++)for(const x of tuples(2,b)){
  check(x.reduce((a,v)=>a^v,0)===mod(x.reduce((a,v)=>a+v,0),2),"even q=2");
 }
 return {status:"COMPUTATIONAL",model:"separate XOR/AND2 onehot comparator; not historical",
   historical_R_mix341_checker_executed:false,case_count:cases.length,
   mixed_derivative_evaluations:derivatives,adder_pair_checks:pairs,
   valid_charge_tuples:valid,invalid_charge_tuples:invalid,
   negative_control:"q=2 parity degree 1, b=2..6",cases};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
