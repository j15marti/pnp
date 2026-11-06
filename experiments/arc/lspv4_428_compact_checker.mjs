#!/usr/bin/env node
// LSPV-4/428 self-contained exact finite no-reuse control. Node >=18.
// Distinct same-label odd-Tseitin descendants; native FLMV costs not measured.
import assert from 'node:assert/strict';
const graphs=[
 ['K4',4,Array.from({length:4},(_,i)=>Array.from({length:4-i-1},(_,j)=>[i,i+j+1])).flat()],
 ['cube',8,Array.from({length:8},(_,x)=>[0,1,2].map(b=>[x,x^(1<<b)]).filter(([a,b])=>a<b)).flat()],
 ['Petersen',10,[...Array.from({length:5},(_,i)=>[i,(i+1)%5]),...Array.from({length:5},(_,i)=>[i+5,5+(i+2)%5]),...Array.from({length:5},(_,i)=>[i,i+5])]]
];
function gamma(v){const s=v.toString(2);return '0'.repeat(s.length-1)+s}
function encode(C,m){
 const w=m.toString(2).length;
 return gamma(m)+gamma(C.length)+C.flat().map(x=>(x<0?'1':'0')+Math.abs(x).toString(2).padStart(w,'0')).join('');
}
function core(n,E){
 const inc=Array.from({length:n},()=>[]);
 E.forEach(([a,b],i)=>{inc[a].push(i+1);inc[b].push(i+1)});
 const C=[];
 for(let v=0;v<n;v++)for(let z=0;z<8;z++){
   const p=(z&1)^((z>>1)&1)^((z>>2)&1);
   if(p===(v===0?1:0))continue;
   C.push(inc[v].map((e,j)=>((z>>j)&1)?-e:e));
 }
 return C;
}
let checks=0, comparisons=0, guestRuns=0;
for(const [name,n,E] of graphs)for(let k=1;k<=5;k++){
 const q=2**k,C=core(n,E);
 assert.equal(C.length,4*n);checks++;
 const make=t=>{
   const tail=Array.from({length:k},(_,i)=>{const v=E.length+3*i+1;return [(t>>i)&1?-v:v,v+1,v+2]});
   return encode([...C,...tail],E.length+3*k);
 };
 const port=Array.from({length:q},(_,t)=>make(t));
 assert.equal(new Set(port).size,q);checks++;
 const L=port[0].length;
 const w=(E.length+3*k).toString(2).length;
 const prefix=gamma(E.length+3*k).length+gamma(4*n+k).length+12*n*(w+1);
 for(let j=1;j<q;j++){
   let i=0;while(i<L&&port[j][i]===port[j-1][i])i++;
   assert.ok(i>=prefix&&i<L,`${name}, k${k}: difference outside fresh tail`);checks++;
   comparisons+=i+1;
 }
 guestRuns+=q;
 // Alter the first sign bit as a corruption control without changing length.
 const spot=gamma(E.length+3*k).length+gamma(4*n+k).length;
 const flipped=port[0].slice(0,spot)+(port[0][spot]==='1'?'0':'1')+port[0].slice(spot+1);
 assert.equal(flipped.length,L);checks++;
}
console.log(JSON.stringify({checks,cases:graphs.length*5,comparisons,guest_runs:guestRuns,scope:'finite exact read-all cache; not an arbitrary-SAT lower bound'}));
