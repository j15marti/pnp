// FP13 independent audit. Node.js, no packages.
'use strict';
const assert=require('assert');
const E=[[0,1],[1,2],[2,3],[3,4],[4,5],[5,0],[6,7],[7,8],[8,6],[9,10],[10,11],[11,9],[0,7],[1,8],[3,10],[4,11],[2,5],[6,9]];
const D=Array.from({length:12},(_,v)=>E.reduce((x,e,i)=>x|(e.includes(v)?1<<i:0),0));
const parity=x=>{let p=0;while(x){x&=x-1;p^=1}return p};
const F=Array.from({length:1<<18},(_,i)=>i).filter(x=>D.every(d=>!parity(d&x)));
const M=(1<<18)-1,a=4095,z=1<<17;
const good=new Set(F.filter(b=>F.some(c=>(b|c)===M)));
const B=F.filter(b=>(M^(a|b))===z);
assert(F.length===128&&B.length===8&&!B.some(b=>good.has(b)));
assert(F.includes(64374)&&F.includes(220571)&&(64374|220571)===M);
function cc(n,es){const p=Array.from({length:n},(_,i)=>i);function root(i){while(p[i]!==i)i=p[i];return i}for(const [u,v] of es)p[root(u)]=root(v);return p.map((_,i)=>root(i))}
const spanning=B.filter(b=>D.every(d=>{let x=b&d,k=0;while(x){x&=x-1;k++}return k===2}));
assert(spanning.length===2);
const union=spanning.reduce((x,b)=>x|b,0);
assert(new Set(cc(12,E.filter((_,i)=>union>>i&1))).size===1);
for(const b of spanning){const c=cc(12,E.filter((_,i)=>b>>i&1));const sizes=[...new Set(c)].map(x=>c.filter(y=>x===y).length).sort();assert.deepStrictEqual(sizes,[5,7])}
console.log('hex',B,spanning,'both spanning factors have cycle lengths 5,7; no chart member extends to proper flow');
function* match(xs){if(!xs.length){yield [];return}for(let j=1;j<xs.length;j++)for(const r of match(xs.slice(1).filter((_,i)=>i!==j-1)))yield [[xs[0],xs[j]],...r]}
let tests=0,yes=0,no=0;
for(const k of [1,2,3]){
 const n=4*k,ports=Array.from({length:n},(_,i)=>i);
 const switches=Array.from({length:k},(_,i)=>{let v=4*i;return [[[v,v+1],[v+2,v+3]],[[v+1,v+2],[v+3,v]]]});
 const all=switches.flat(2);
 for(const P of match(ports)){
  const u=cc(n,P.concat(all)),parts=[];
  for(let x=0;x<1<<k;x++)parts.push(cc(n,P.concat(switches.flatMap((s,i)=>s[x>>i&1]))));
  for(let j=0;j<P.length;j++)for(let l=j+1;l<P.length;l++){
   const s=P[j][0],t=P[l][0],want=u[s]===u[t],got=parts.some(p=>p[s]===p[t]);
   assert.strictEqual(got,want);tests++;if(got)yes++;else no++;
  }
 }
}
console.log({tests,yes,no});
