'use strict';
// LSPV-3/417. Standalone CONDITIONAL exported-term checker, NOT native R_mix341.
const assert=require('assert');
const truth=(op,a,b)=>(op>>(a*2+b))&1;
const cofactor=(m,k)=>[0,1,2,3].reduce((z,j)=>z+(((m>>(4*k+j))&1)<<j),0);
function synth(mask,inputs){
 const [x,y,z]=inputs;
 return {mask,inputs,out:'out',gates:[
  ['p0',cofactor(mask,0),y,z],
  ['p1',cofactor(mask,1),y,z],
  ['delta',6,'p0','p1'],
  ['mul',8,x,'delta'],
  ['out',6,'p0','mul']]};
}
function evaluate(c,bits){
 let env={};bits.forEach((b,i)=>env['x'+i]=b);
 if(!Array.isArray(c.gates))throw Error('missing');
 for(let [id,op,a,b] of c.gates) {
  if(typeof id!=='string'||!(Number.isInteger(op)&&op>=0&&op<=15)
     ||!Object.hasOwn(env,a)||!Object.hasOwn(env,b)||Object.hasOwn(env,id))
    throw Error('bad gate');
  env[id]=truth(op,env[a],env[b]);
 }
 if(!Object.hasOwn(env,c.out))throw Error('bad output');
 return env[c.out];
}
let checks=0;
for(let m=0;m<256;m++){
 let c=synth(m,['x0','x1','x2']);
 for(let a=0;a<8;a++){
  let bits=[(a>>2)&1,(a>>1)&1,a&1];
  assert.equal(evaluate(c,bits),(m>>a)&1);checks++;
 }
}
let ports=[];
for(let j=0;j<84;j++){
 let names=[0,2,4].map(k=>'x'+((j+k)%6)),mask=(j*97+90)%256;
 let c=synth(mask,names);ports.push(c);
 for(let a=0;a<64;a++){
  let bits=Array.from({length:6},(_,i)=>(a>>i)&1);
  let row=names.reduce((r,v)=>r*2+bits[Number(v.slice(1))],0);
  assert.equal(evaluate(c,bits),(mask>>row)&1);checks++;
 }
}
let p=ports[0];
for(let bad of [
 {...p,out:'unknown'},
 {...p,gates:[['p0',16,p.inputs[1],p.inputs[2]],...p.gates.slice(1)]},
 {...p,gates:[['p0',p.gates[0][1],'unknown',p.inputs[2]],...p.gates.slice(1)]},
 {...p,gates:[p.gates[0],['p0',p.gates[1][1],p.inputs[1],p.inputs[2]],...p.gates.slice(2)]}
]){assert.throws(()=>evaluate(bad,[0,1,0,1,0,1]));checks++;}
let counting=[];
for(let n of [10,12,16,20,24,32,40]){
 let s=Math.floor(2**n/(100*n));
 let logBound=Math.log2(s+1)+Math.log2(n+s)+s*(4+2*Math.log2(n+s));
 assert(logBound<2**n);checks++;
 counting.push({n,s,logBound});
}
function modelCount(clauses,n){
 let ans=0;
 for(let a=0;a<2**n;a++)
  if(clauses.every(C=>C.some(l=>(((a>>(Math.abs(l)-1))&1)===Number(l>0)))))ans++;
 return ans;
}
assert.equal(modelCount([[1],[1,2]],2),2);
assert.equal(modelCount([[1],[-1]],1),0);checks+=2;
let reconv={gates:[['a',6,'x0','x0'],['out',14,'a','x1']],out:'out'};
for(let a=0;a<8;a++){
 let bits=[(a>>2)&1,(a>>1)&1,a&1];
 assert.equal(evaluate(reconv,bits),bits[1]);checks++;
}
console.log(JSON.stringify({run:'LSPV-3/417',status:'conditional',checks,functions:256,ports:84,port_rows:5376,malformed:4,counting,passed:true},null,2));
