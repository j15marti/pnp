'use strict';
// LSPV-4/387: separate K4 odd/even Tseitin hostile control, no proof inference.
const assert=require('assert');
const edges=[];
for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)edges.push([u,v]);
function tseitin(odd){
 const charges=[odd?1:0,0,0,0], clauses=[];
 for(let v=0;v<4;v++){
  const ids=edges.map((e,i)=>e.includes(v)?i+1:null).filter(x=>x!==null);
  for(let a=0;a<8;a++){
   const bits=ids.map((_,k)=>(a>>k)&1);
   if(bits.reduce((p,b)=>p^b,0)!==charges[v])clauses.push(ids.map((x,k)=>bits[k]?-x:x));
  }
 }
 return clauses;
}
function models(cs){
 let n=0;
 for(let a=0;a<64;a++)if(cs.every(c=>c.some(x=>Boolean(a&(1<<(Math.abs(x)-1)))===(x>0))))n++;
 return n;
}
const odd=tseitin(true),even=tseitin(false);
assert.strictEqual(edges.length,6);
assert.strictEqual(odd.length,16);assert.strictEqual(even.length,16);
const output={status:'PASS',odd_models:models(odd),even_models:models(even),odd_clauses:odd.length,even_clauses:even.length,edges:edges.length};
assert.strictEqual(output.odd_models,0);assert.strictEqual(output.even_models,8);
console.log(JSON.stringify(output));
