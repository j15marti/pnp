'use strict'; // Independent finite self-check; no external packages.
let checks=0;const ck=x=>{checks++;if(!x)throw Error('failed '+checks)};
const bits=n=>Array.from({length:1<<n},(_,b)=>Array.from({length:n},(_,i)=>(b>>i)&1));
for(let t=1;t<=7;t++){
 const cls=bits(t).map(s=>s.map((v,i)=>2*i+v));
 for(let a of bits(2*t)){
  let f=Array.from({length:t},(_,i)=>a[2*i]&&a[2*i+1]).some(Boolean);
  let g=cls.every(c=>c.some(j=>a[j]));ck(f===g);
 }
 for(let c=0;c<cls.length;c++){
  let a=Array(2*t).fill(0);for(let j of cls[c])a[j^1]=1;
  ck(cls[c].every(j=>!a[j]));ck(cls.every((q,j)=>j===c||q.some(k=>a[k])));
 }
}
const val=(cl,x)=>cl.some(v=>x[Math.abs(v)-1]===+(v>0));
for(let d=4;d<=8;d++){
 let chain=[[1,2,d+1]];
 for(let j=1;j<d-3;j++)chain.push([-(d+j),j+2,d+j+1]);
 chain.push([-(2*d-3),d-1,d]);
 for(let x of bits(d)){
  let y=Array.from({length:d-3},(_,j)=>+(x.slice(0,j+2).every(v=>!v)));
  ck(chain.every(cl=>val(cl,x.concat(y)))===x.some(Boolean));
  ck(bits(d-3).some(w=>chain.every(cl=>val(cl,x.concat(w))))===x.some(Boolean));
 }
}
console.log(JSON.stringify({status:'PASS',checks,cnf_exact_minimum_t:7,chain_width_through:8}));
