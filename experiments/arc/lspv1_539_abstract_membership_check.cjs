'use strict';
// LSPV-1/539. Independent executable of the parameterized query-collision construction.
// Native historical R_mix341 rule checker NOT implemented.
const assert=require('assert');
const C=a=>a.slice().sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y).join(',');
const choose=(a,k,cb,start=0,out=[])=>{if(!k){cb(out);return}for(let i=start;i<=a.length-k;i++)choose(a,k-1,cb,i+1,[...out,a[i]])};
function build(h,edges){const incident=Array.from({length:h},()=>[]);edges.forEach(([u,v],i)=>{incident[u].push(i+1);incident[v].push(i+1)});const present=new Set(),missing=Array.from({length:h},()=>[]),at=Array.from({length:h},()=>[]);for(let v=0;v<h;v++){assert.equal(incident[v].length,3);for(let bits=0;bits<8;bits++){const key=C(incident[v].map((x,i)=>(bits>>i&1)?-x:x));((pop(bits)%2)===(v===0?1:0)?missing[v]:at[v]).push(key);}}for(let a of at)for(let c of a)present.add(c);assert.equal(present.size,4*h);return{present,missing,at,incident}}
function pop(n){let s=0;while(n){n&=n-1;s++}return s}
function test(q,h,d){const Q=new Set(q);let v=d.missing.findIndex(a=>a.every(x=>!Q.has(x)));assert(v>=0);const remove=[...d.present].filter(x=>!Q.has(x)&&!d.at[v].includes(x)).slice(0,4);assert.equal(remove.length,4);const E=new Set(d.present);for(let c of remove)E.delete(c);for(let c of d.missing[v])E.add(c);assert.equal(E.size,4*h);for(let c of Q)assert.equal(E.has(c),d.present.has(c));for(let c of d.at[v])assert(E.has(c));for(let c of d.missing[v])assert(E.has(c));return{v,remove,add:d.missing[v]}}
const k4=build(4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]);
const U=[];choose([1,2,3,4,5,6],3,trip=>{for(let bits=0;bits<8;bits++)U.push(C(trip.map((x,i)=>(bits>>i&1)?-x:x)))});assert.equal(U.length,160);
let count=0;for(let k=0;k<4;k++)choose(U,k,Q=>{test(Q,4,k4);count++});assert.equal(count,682801);
const blocks=[...Array(4).keys()].map(v=>k4.missing[v][0]);assert.equal(k4.missing.findIndex(a=>a.every(x=>!new Set(blocks).has(x))),-1);
const prism=build(6,[[0,1],[1,2],[0,2],[3,4],[4,5],[3,5],[0,3],[1,4],[2,5]]);
const cube=build(8,Array.from({length:8},(_,i)=>Array.from({length:8},(_,j)=>i<j&&pop(i^j)===1?[i,j]:null).filter(Boolean)).flat());
let samples=0;for(let [h,d] of [[6,prism],[8,cube]]){let all=[...d.present,...d.missing.flat()];for(let t=0;t<100;t++){const Q=[];for(let i=0;i<t%h;i++)Q.push(all[(17*t+31*i)%all.length]);test(Q,h,d);samples++}}
console.log(JSON.stringify({id:'LSPV1_539',status:'PASS',exact_K4_query_subsets:count,extra_samples:samples,universe:U.length,critical_threshold:4}));
