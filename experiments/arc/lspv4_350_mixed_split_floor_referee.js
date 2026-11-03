#!/usr/bin/env node
"use strict";
/*
Independent no-producer-import referee for Rmix341^VARDEF source-once
mixed-tree DP, with BigInt Boolean truth masks instead of producer strings.
Enumerates all binary source partitions, and checks exact RES/AND3/XOR
outputs under a STRONGER output-support-3 AND3 relaxation.
Run: node experiments/arc/lspv4_350_mixed_split_floor_referee.js
*/
const assert=require("assert");
const V=7, ASS=1<<V;
const CORE=[[-3,1,4],[-1,2],[1,3],[-4,-3],[-2,-1,3],[-2,4]];
function value(c){let m=0n;outer:for(let a=0;a<ASS;a++){for(let l of c){
 if(((a>>>(Math.abs(l)-1))&1)===(l>0?1:0)){m|=1n<<BigInt(a);continue outer;}
 }}return m;}
const cm=new Map();
for(let t=0;t<3**V;t++){let a=t,c=[];for(let v=1;v<=V;v++){let d=a%3;a=(a-d)/3;if(d)c.push(d===1?v:-v);}cm.set(value(c),c);}
const am=new Map(),rm=new Map();
for(let c=0;c<ASS;c++)for(let b=0;b<2;b++){
 let m=0n;for(let a=0;a<ASS;a++){let v=0;for(let k=0;k<V;k++)if(c&(1<<k))v^=(a>>k)&1;if(v===b)m|=1n<<BigInt(a);}
 am.set(m,[c,b]);rm.set(c+","+b,m);
}
const sc=new Map(),memo=new Map();
function support(m){if(sc.has(m))return sc.get(m);let w=0;for(let v=0;v<V;v++){
  for(let a=0;a<ASS;a++)if(((m>>BigInt(a))&1n)!==((m>>BigInt(a^(1<<v)))&1n)){w++;break;}
 }sc.set(m,w);return w;}
function merge(x,y){
 const key=x.toString()+":"+y.toString();if(memo.has(key))return memo.get(key);
 const out=new Set();let both=x&y;if(support(both)<=3)out.add(both);
 let a=am.get(x),b=am.get(y);if(a&&b)out.add(rm.get((a[0]^b[0])+","+(a[1]^b[1])));
 let A=cm.get(x),B=cm.get(y);if(A&&B)for(let p=1;p<=V;p++){
  if(!(A.includes(p)&&B.includes(-p)||A.includes(-p)&&B.includes(p)))continue;
  let c=Array.from(new Set(A.concat(B).filter(l=>Math.abs(l)!==p)));
  if(c.some(l=>c.includes(-l)))continue;out.add(value(c));
 }
 const v=Array.from(out);memo.set(key,v);return v;
}
function run(F){
 const n=F.length,dp=Array.from({length:1<<n},()=>new Set());for(let j=0;j<n;j++)dp[1<<j].add(value(F[j]));
 const layers=[];for(let k=2;k<=n;k++){let states=0,pairs=0;
  for(let s=1;s<dp.length;s++){let t=s,count=0;while(t){t&=t-1;count++;}if(count!==k)continue;
   for(let L=(s-1)&s;L;L=(L-1)&s){let R=s^L;if(L>=R)continue;
    for(let x of dp[L])for(let y of dp[R]){pairs++;for(let r of merge(x,y))dp[s].add(r);}
   }states+=dp[s].size;
  }layers.push([k,states,pairs]);
 }
 return {found:dp[dp.length-1].has(0n),totalStates:dp.reduce((a,b)=>a+b.size,0),
   pairs:layers.reduce((a,b)=>a+b[2],0),layers};
}
function single(i){const f=CORE.filter((_,j)=>i!==j).map(c=>[...c]);f.push([...CORE[i],5],[...CORE[i],-5]);return f;}
function nested(t){let f=CORE.slice(1).map(c=>[...c]);let c=[...CORE[0]];for(let i=0;i<t;i++){f.push([...c,-(5+i)]);c.push(5+i);}f.push(c);return f;}
const singleData=Array.from({length:6},(_,i)=>run(single(i)));
const nestedData=[0,1,2,3].map(t=>run(nested(t)));
assert.deepStrictEqual(singleData.map(x=>x.found),Array(6).fill(false));
assert.deepStrictEqual(nestedData.map(x=>x.found),Array(4).fill(false));
assert.deepStrictEqual(singleData.map(x=>x.totalStates),[592,795,758,795,592,562]);
assert.deepStrictEqual(singleData.map(x=>x.pairs),[2170,2642,2679,2642,2170,1949]);
assert.deepStrictEqual(nestedData.map(x=>x.totalStates),[320,592,1229,2977]);
assert.deepStrictEqual(nestedData.map(x=>x.pairs),[844,2170,6715,24618]);
const horn=[[1],[-1,2],[-2,3],[-3,4],[-4,5],[-5]];
assert.equal(run(horn).found,true);
console.log(JSON.stringify({referee:"PASS",independent:"BigInt, no producer imports",singleData,nestedData,positiveHorn:"PASS"},null,2));
