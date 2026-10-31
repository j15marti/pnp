// BACKDOOR-GRAY-TERMINAL283 finite spot check. node compact283.js
"use strict";
const assert=require("node:assert/strict");
const F=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]];
const n=6,m=8,G=t=>t^(t>>1),wt=x=>{let r=0;for(;x;x>>=1)r+=x&1;return r};
const counts=a=>F.map(c=>c.reduce((r,z)=>r+Number(((a>>(Math.abs(z)-1))&1)===Number(z>0)),0));
const pos=Array(n).fill(0),neg=Array(n).fill(0),seen=new Set();
for(const c of F){assert.equal(c.length,3);assert.equal(new Set(c.map(Math.abs)).size,3);
 assert(c.every(z=>(z>0)===(c[0]>0)));const key=[...c].sort((a,b)=>a-b).join();
 assert(!seen.has(key));seen.add(key);for(const z of c)(z>0?pos:neg)[Math.abs(z)-1]++}
assert(pos.every(v=>v===2)&&neg.every(v=>v===2));
let models=0,flips=0,restrictions=0,modes=0;
for(let a=0;a<1<<n;a++){const t=counts(a),back=counts(a^((1<<n)-1));
 if(t.every(v=>v>0))models++;assert(t.every((v,j)=>back[j]===3-v));
 assert.equal(t.reduce((r,v,j)=>r+wt(G(v)^G(back[j])),0),m);
 assert.equal(t.reduce((r,v,j)=>r+wt(v^back[j]),0),2*m);
 for(let i=0;i<n;i++){const after=counts(a^(1<<i));assert.equal(
 t.reduce((r,v,j)=>r+wt(G(v)^G(after[j])),0),4);flips++}}
for(let mask=0;mask<1<<n;mask++){let untouched=[0,0];
 for(const c of F)if(c.every(z=>!(mask&(1<<(Math.abs(z)-1)))))untouched[Number(c[0]>0)]++;
 assert(untouched.every(x=>x>=Math.max(0,2*n/3-2*wt(mask))));
 if(wt(mask)<n/3)assert(untouched.every(x=>x>0));restrictions++}
for(let i=0;i<m;i++)for(let j=i+1;j<m;j++)
 for(const x of ["S","U"])for(const y of ["S","U"]){let vals=new Map(),possible=true;
 for(const [c,mode] of [[F[i],x],[F[j],y]])for(const z of c){
 const v=Math.abs(z),b=Number((z>0)===(mode==="S"));if(vals.has(v)&&vals.get(v)!==b)possible=false;vals.set(v,b)}
 let actual=false;for(let a=0;a<1<<n;a++){
 const matches=(c,mode)=>c.every(z=>((a>>(Math.abs(z)-1))&1)===Number((z>0)===(mode==="S")));
 if(matches(F[i],x)&&matches(F[j],y))actual=true}
 assert.equal(possible,actual);modes++}
console.log(JSON.stringify({status:"COMPUTATIONAL",verdict:"PASS",models,flips,restrictions,modes,proves_unrestricted_SAT:false}));
