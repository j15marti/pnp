#!/usr/bin/env node
'use strict';
/* LSPV-1/517 standalone strict signed 3CNF -> shared multi-output circuit controls.
Not a R_mix341 checker. Finite tests do not establish the symbolic theorem. */
const assert=require('assert');
function proper(n,cs){assert(Number.isInteger(n)&&n>=3&&Array.isArray(cs));
 for(const c of cs){assert(Array.isArray(c)&&c.length===3);assert(c.every(v=>Number.isInteger(v)&&v!==0&&Math.abs(v)<=n));assert(new Set(c.map(Math.abs)).size===3);}}
function formula(cs,x){return cs.every(c=>c.some(l=>{let v=(x>>(Math.abs(l)-1))&1;return l>0?v===1:v===0;}));}
function construct(n,cs,k){proper(n,cs);assert(Number.isInteger(k)&&k>=1);
 let arity=n+2*k+2,gates=[];const emit=(op,a,b)=>{let id=arity+gates.length;assert(a<id&&(b===undefined||b<id));gates.push({op,a,b});return id;};
 const NOT=a=>emit('not',a),AND=(a,b)=>emit('and',a,b),OR=(a,b)=>emit('or',a,b);
 let acc=null;for(const c of cs){let term=null;for(let l of c){let v=Math.abs(l)-1;if(l<0)v=NOT(v);term=term===null?v:OR(term,v);}acc=acc===null?term:AND(acc,term);}
 if(acc===null)acc=emit('one',0);
 let outs=[AND(n+2*k,n+2*k+1)];
 for(let i=0;i<k;i++)outs.push(AND(AND(acc,n+2*i),n+2*i+1));
 return {arity,gates,outs};
}
function calc(c,z){let bits=Array.from({length:c.arity},(_,i)=>(z>>i)&1);
 for(const g of c.gates){let a=bits[g.a],b=bits[g.b];bits.push(g.op==='not'?a^1:g.op==='and'?a&b:g.op==='or'?a|b:g.op==='one'?1:(()=>{throw Error('bad op')})());}
 return c.outs.map(i=>bits[i]);}
const all8=Array.from({length:8},(_,z)=>[1,2,3].map(i=>((z>>(i-1))&1)?-i:i));
let cases=0,derivatives=0,labels={SAT:0,UNSAT:0},checks=0;
for(let mask=0;mask<256;mask++){
 let cs=all8.filter((_,i)=>(mask>>i)&1),k=mask%2+1,c=construct(3,cs,k);
 let sat=Array.from({length:8},(_,x)=>formula(cs,x)).some(Boolean);labels[sat?'SAT':'UNSAT']++;
 for(let x=0;x<8;x++){
  let f=formula(cs,x);
  for(let i=0;i<k;i++){let t=1<<(3+2*i),u=1<<(3+2*i+1);
   let d=calc(c,x)[i+1]^calc(c,x^t)[i+1]^calc(c,x^u)[i+1]^calc(c,x^t^u)[i+1];
   assert.strictEqual(d,Number(f));derivatives++;}
  let a=1<<(3+2*k),b=1<<(3+2*k+1);
  assert.strictEqual(calc(c,x)[0]^calc(c,x^a)[0]^calc(c,x^b)[0]^calc(c,x^a^b)[0],1);checks++;
 }
 if(!sat)for(let x=0;x<8;x++)for(let i=1;i<c.outs.length;i++){assert.strictEqual(calc(c,x)[i],0);checks++;}
 cases++;
}
let bads=[[1,2,2],[1,2,0],[1,2,4]],rejected=0;
for(const b of bads){assert.throws(()=>construct(3,[b],1));rejected++;}
assert.throws(()=>construct(2,[],1));rejected++;
let positive=construct(3,[all8[0]],1),tampered=JSON.parse(JSON.stringify(positive));
tampered.gates[tampered.outs[1]-tampered.arity].op='or';
let corrupted=false;for(let x=0;x<8;x++)if(calc(tampered,x|(1<<3))[1]!==calc(positive,x|(1<<3))[1])corrupted=true;
assert(corrupted);checks++;
console.log(JSON.stringify({result:'PASS',cases,labels,derivative_identity_assertions:derivatives,baseline_polar_assertions:2048,extra_assertions:checks,malformed_rejected:rejected,corrupted_circuit_detected:corrupted,scope:'strict signed proper 3CNF, native Rmix341 not executed'},null,2));