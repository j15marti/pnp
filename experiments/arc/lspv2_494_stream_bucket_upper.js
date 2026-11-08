'use strict';
/* LSPV-2/494 independent finite check, not an FLMV or R_mix341 implementation. */
const assert = require('node:assert/strict');
const edges = {
 K4: [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],
 prism3:[[0,1],[1,2],[0,2],[3,4],[4,5],[3,5],[0,3],[1,4],[2,5]],
 cube:(()=>{const e=[];for(let i=0;i<8;i++)for(let j=i+1;j<8;j++){let d=i^j;if(d && !(d&(d-1)))e.push([i,j]);}return e;})()
};
function source(ee){const h=1+Math.max(...ee.flat());const inc=Array.from({length:h},()=>[]);ee.forEach(([a,b],i)=>{inc[a].push(i);inc[b].push(i)});const out=[];for(let v=0;v<h;v++){assert.equal(inc[v].length,3);for(let pat=0;pat<8;pat++){const b=[pat&1,(pat>>1)&1,(pat>>2)&1];if((b[0]^b[1]^b[2])!==(v===0?1:0))out.push(inc[v].map((e,j)=>(e+1)*(b[j]?-1:1)));}}return [out,ee.length];}
function sat(c,n){for(let bits=0;bits<2**n;bits++){if(c.every(cl=>cl.some(l=>((bits>>(Math.abs(l)-1))&1)===(l>0?1:0))))return true;}return false;}
function isperm(w,m){return w.length===m && new Set(w).size===m && w.every(x=>Number.isInteger(x)&&x>=0&&x<m);}
function passBucket(w,m,b){if(w.length!==m)return false;let valid=true;for(let low=0;low<m;low+=b){const high=Math.min(low+b,m);const state=new Set();for(const x of w)if(x>=low&&x<high)state.add(x);if(state.size!==high-low)valid=false;}return valid;}
let checks=0;const rec=[];let seed=494;function rng(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/2**32;}
for(const [name,e] of Object.entries(edges)){const [cl,n]=source(e);const m=cl.length;assert.equal(m,4*(Math.max(...e.flat())+1));assert(!sat(cl,n));checks++;
for(let j=0;j<m;j++){assert(sat(cl.filter((_,i)=>i!==j),n));checks++;}
for(let z=0;z<250;z++){const w=Array.from({length:m},(_,i)=>i);for(let i=m-1;i>0;i--){const j=Math.floor(rng()*(i+1));[w[i],w[j]]=[w[j],w[i]];}if(z%2){const i=Math.floor(rng()*m),j=(i+1)%m;w[i]=w[j];}const exp=isperm(w,m);assert.equal(sat(w.map(i=>cl[i]),n),!exp);checks++;for(const b of [1,2,4,5,Math.max(1,Math.floor(m/3)),m]){assert.equal(passBucket(w,m,b),exp);checks++;}}
rec.push({graph:name,clauses:m,variables:n,random_cases:250});}
function* tuples(m,k,p=[]){if(p.length===k){yield p;return;}for(let v=0;v<m;v++)yield* tuples(m,k,[...p,v]);}
for(const m of [2,3,4])for(const a of tuples(m,m)){const expected=isperm(a,m);for(let b=1;b<=m;b++){assert.equal(passBucket(a,m,b),expected);checks++;}}
function subsets(m,k){const out=[];function go(start,p){if(p.length===k){out.push(p);return;}for(let i=start;i<m;i++)go(i+1,[...p,i]);}go(0,[]);return out;}
for(const m of [4,6,8]){const ss=subsets(m,m/2);for(const a of ss){const comp=Array.from({length:m},(_,i)=>i).filter(i=>!a.includes(i));for(const b of ss){assert.equal(isperm([...b,...comp],m),JSON.stringify(a)===JSON.stringify(b));checks++;}}}
console.log(JSON.stringify({status:'PASS',checks,graphs:rec,algorithm:'independent Set-based bucket-pass and bitmask truth table'},null,2));
