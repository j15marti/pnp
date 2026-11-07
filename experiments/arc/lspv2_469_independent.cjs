'use strict';
const assert=require('node:assert/strict');
const q=257,k=3,r=Math.ceil(Math.log2(q+1)),d=Math.ceil(Math.log2(r+2)),R=2**d;
let checks=0,ops=0,s=4692026;
function rnd(max){s=(Math.imul(1664525,s)+1013904223)>>>0;return s%max}
const guest=Array.from({length:k},()=>({head:0n,index:new Set(),idxhead:0,mem:new Map(),max:0n}));
const host=Array.from({length:k},()=>({head:0n,index:new Set(),idxhead:0,mem:new Map(),max:0n}));
let generation=1;
function mark(h){const v=h.head+BigInt(r);if(v>h.max)h.max=v}
function tag(h){let t=0;for(let i=0;i<r;i++)t+=(h.mem.get(h.head+BigInt(i))||0)*(2**i);return t}
function read(h,g){mark(h);return tag(h)===g?(h.mem.get(h.head+BigInt(r))||0):0}
function workwrite(h,g,v){mark(h);for(let i=0;i<r;i++)h.mem.set(h.head+BigInt(i),(g>>>i)&1);h.mem.set(h.head+BigInt(r),v)}
for(let e=0;e<q;e++){
 if(e){generation++;for(let i=0;i<k;i++){guest[i].head=0n;guest[i].index.clear();guest[i].idxhead=0;guest[i].mem.clear();host[i].head=0n;host[i].index.clear();host[i].idxhead=0;}}
 for(let j=0;j<64;j++){
  const i=rnd(k),g=guest[i],h=host[i],act=rnd(9);
  if(act===0){let b=rnd(2);if(b){g.index.add(g.idxhead);h.index.add(h.idxhead+d)}else{g.index.delete(g.idxhead);h.index.delete(h.idxhead+d)}}
  else if(act===1){const z=rnd(2)?1:-1;g.idxhead=Math.max(0,g.idxhead+z);h.idxhead=Math.max(0,h.idxhead+z)}
  else if(act===2){let a=0n;for(const bit of g.index)a|=1n<<BigInt(bit);let b=0n;for(const bit of h.index)b|=1n<<BigInt(bit);assert.equal(b,BigInt(R)*a);checks++;g.head=a;h.head=b;g.index.clear();h.index.clear();}
  else if(act===3||act===4){const z=rnd(2)?1n:-1n;g.head=g.head+z<0n?0n:g.head+z;h.head=h.head+BigInt(R)*z<0n?0n:h.head+BigInt(R)*z;}
  else if(act===5||act===6){const v=rnd(2);g.mem.set(g.head,v);workwrite(h,generation,v)}
  else {assert.equal(read(h,generation),g.mem.get(g.head)||0);checks++;}
  if(g.head>g.max)g.max=g.head;mark(h);
  assert.equal(h.head,BigInt(R)*g.head);assert.equal(h.idxhead,g.idxhead);assert.ok(h.max<=BigInt(R)*g.max+BigInt(r));
  checks+=3;ops++;
 }
 for(let i=0;i<k;i++){assert.equal(read(host[i],generation),guest[i].mem.get(guest[i].head)||0);checks++;}
}
function strictCNF(src){if(!Array.isArray(src))return false;return src.every(c=>Array.isArray(c)&&c.length===3&&c.every(x=>Number.isSafeInteger(x)&&x!==0)&&new Set(c.map(x=>Math.abs(x))).size===3)}
const bad=[[1,2,2],[1,0,3],[1,2],[1,2,1],['x',2,3]];
for(const clause of bad){assert.equal(strictCNF([clause]),false);checks++;}
assert.equal(strictCNF([[1,-2,3],[-1,2,-3]]),true);checks++;
console.log(JSON.stringify({status:'PASS',q,k,r,d,R,guest_ops:ops,assertions:checks,source_negative_controls:bad.length,native_FLVM_run:false},null,2));
