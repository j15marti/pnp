// Small-mask reproducible tests (seed 481); run with Node. Not a production bit-RAM implementation.
function main(){
"use strict";
const assert=(x,msg)=>{if(!x)throw Error(msg)};
function parity(x){let a=0;while(x){a^=1;x&=x-1}return a}
function basis(xs){const p=new Map();for(let x of xs){while(x){const i=31-Math.clz32(x);if(p.has(i))x^=p.get(i);else{p.set(i,x);break}}}const ks=[...p.keys()].sort((a,b)=>a-b);for(const i of ks)for(const j of ks)if(j>i&&(p.get(j)&(1<<i)))p.set(j,p.get(j)^p.get(i));return ks.map(i=>p.get(i))}
const rank=xs=>basis(xs).length;
function span(B){let a=[0];for(const x of B)a=a.concat(a.map(v=>v^x));return a}
function norm(rows,bits,d){const a=basis(rows.map((x,i)=>x|(bits[i]<<d)));const r=rank(rows);if(a.length>r)return null;return {rows,bits,r}}
const hit=(H,F)=>F.r+H.length-rank(H.concat(F.rows))>=F.r-1;
function findH(F,k,H=[]){const f=F.find(f=>!hit(H,f));if(!f)return H;if(H.length===k)return null;
 for(const v of span(basis(f.rows)))if(v&&rank(H.concat(v))>H.length){const out=findH(F,k,basis(H.concat(v)));if(out)return out}return null}
function minH(F,d){for(let k=0;k<=d;k++){const h=findH(F,k);if(h)return h}throw Error("no H")}
function allSpaces(d){let Q=[[]],seen=new Set([""]);for(let i=0;i<Q.length;i++)for(let v=1;v<(1<<d);v++){const h=basis(Q[i].concat(v)),key=h.join(",");if(!seen.has(key)){seen.add(key);Q.push(h)}}return Q}
const violated=(f,x)=>f.rows.every((r,i)=>parity(r&x)===f.bits[i]);
const brute=(F,d)=>{let z=0;for(let x=0;x<(1<<d);x++)if(!F.some(f=>violated(f,x)))z++;return z};
function countH(F,d,H){let count=0;for(let s=0;s<(1<<H.length);s++){
 let rows=H.slice(),bits=H.map((_,i)=>(s>>i)&1),bad=false;
 for(const f of F){
 const R=H.concat(f.rows), B=H.map((_,i)=>(s>>i)&1).concat(f.bits);
 const ff=norm(R,B,d);if(!ff)continue;
 const delta=ff.r-H.length;assert(delta<=1,"not hit");
 if(delta===0){bad=true;break}
 const j=f.rows.findIndex(x=>rank(H.concat(x))>H.length);
 rows.push(f.rows[j]);bits.push(f.bits[j]^1)
 }
 if(!bad){const g=norm(rows,bits,d);if(g)count+=2**(d-g.r)}
 }return count}
let seed=481;function rng(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/2**32*n)}
let random=0, sat=0, unsat=0, deps=0;const profiles=new Set();
for(let d=1;d<=5;d++){const spaces=allSpaces(d);
 for(let t=0;t<80;t++){let F=[];for(let i=0,m=1+rng(8);i<m;i++){const rows=[],bits=[];for(let j=0,k=1+rng(4);j<k;j++){rows.push(rng(1<<d));bits.push(rng(2))}const f=norm(rows,bits,d);if(f)F.push(f);else deps++}
  const H=minH(F,d), k=Math.min(...spaces.filter(h=>F.every(f=>hit(h,f))).map(h=>h.length));
  assert(H.length===k,"minimum");const z=brute(F,d);assert(countH(F,d,H)===z,"count");random++;z?sat++:unsat++;profiles.add([d%2,k%2,(d-k)%2].join(""))
 }}
function graphFactors(n,E,charges){let F=[];for(let i=0;i<E.length;i++){let [u,v]=E[i],a=1<<u,b=1<<v,p=1<<(n+i),c=charges[i];
 for(let q=0;q<2;q++)F.push({rows:[a^b,a^p],bits:[1^c,q],r:2})
 }return F}
function graphRank(n,E){return rank(E.map(([u,v])=>(1<<u)^(1<<v)))}
function cpCount(n,E,charges){const f=norm(E.map(([u,v])=>(1<<u)^(1<<v)),charges,n);return f?2**(n+E.length-f.r):0}
let cycles=0,neighbors=0,cuts=0,graphTests=0,hitTests=0;const cycleRows=[],cutParities=new Set();
function checkGraph(n,E,checkMin){const m=E.length,d=n+m;const balanced=E.map(([u,v])=>(u^v)&1), flipped=balanced.slice();flipped[0]^=1;
 for(const c of [balanced,flipped]){let F=graphFactors(n,E,c);assert(brute(F,d)===cpCount(n,E,c),"CG exact count");graphTests++;
 if(checkMin){const H=minH(F,d);assert(H.length===graphRank(n,E),"graph min");hitTests++}
 }
 for(let mask=1;mask<(1<<m)-1;mask++){const A=E.filter((_,i)=>(mask>>i)&1),B=E.filter((_,i)=>!((mask>>i)&1));const F=graphFactors(n,E,balanced);
 const RA=F.filter((_,j)=>(mask>>(j>>1))&1).flatMap(f=>f.rows),RB=F.filter((_,j)=>!((mask>>(j>>1))&1)).flatMap(f=>f.rows);
 const s=rank(RA)+rank(RB)-rank(RA.concat(RB));assert(s===graphRank(n,A)+graphRank(n,B)-graphRank(n,E),"cut");cutParities.add(s%2);cuts++
 }}
for(let n=3;n<=8;n++){let E=Array.from({length:n},(_,i)=>[i,(i+1)%n]);const a=Array(n).fill(1),b=a.slice();b[0]^=1;
 const counts=[a,b].map(c=>{const F=graphFactors(n,E,c),z=brute(F,2*n);assert(z===cpCount(n,E,c),"cycle count");cycles++;if(!z)for(let i=0;i<F.length;i++){assert(brute(F.filter((_,j)=>i!==j),2*n)===2**n,"deletion count");neighbors++}return z});
 cycleRows.push([n,...counts]);checkGraph(n,E,n<=5)
}
checkGraph(4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],true);
checkGraph(5,[[0,1],[1,2],[2,3],[3,4]],true);
checkGraph(6,Array.from({length:9},(_,i)=>[Math.floor(i/3),3+i%3]),false);
return {random,sat,unsat,inconsistentForbiddenSystems:deps,dimensionBackdoorNullityParity:[...profiles].sort(),cycles,neighbors,cuts,graphTests,hitTests,cycleRows,cutParities:[...cutParities].sort()};
}
console.log(JSON.stringify(main(),null,2));
