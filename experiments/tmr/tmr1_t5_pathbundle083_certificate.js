'use strict';
// TMR-1/083 deterministic certificate; independent full verifier in local attachment.
const assert=require('node:assert/strict');
const mod=x=>(x%5+5)%5;
let assertions=0;
function eq(a,b){assert.deepStrictEqual(a,b);assertions++;}
function tr(s){let a=[1,0,0,0,0];for(const sign of s){let b=[0,0,0,0,0];for(let d=0;d<5;d++)for(const t of [1,3])b[mod(d+(sign==='+'?t:-t))]+=a[d];a=b;}return a;}
function brute(s){let a=[0,0,0,0,0],n=s.length;for(let bits=0;bits<2**n;bits++){let d=0;for(let i=0;i<n;i++)d=mod(d+(s[i]==='+'?1:-1)*(bits&(1<<i)?3:1));a[d]++;}return a;}
for(let n=0;n<=8;n++)for(let bits=0;bits<2**n;bits++){let s='';for(let j=0;j<n;j++)s+=bits&(1<<j)?'-':'+';eq(tr(s),brute(s));}
const patterns=['++','+++','++-','---'];const tables=Object.fromEntries(patterns.map(s=>[s,tr(s)]));
eq(tables['++'],[0,1,1,0,2]);eq(tables['+++'],[3,0,3,1,1]);eq(tables['++-'],[1,3,0,3,1]);eq(tables['---'],[3,1,1,3,0]);
function block(q){let v=[1,1,1,1,1];for(const s of ['++','+++','++-',q])v=v.map((x,d)=>x*tr(s)[d]);return v;}
eq(block('+++'),[0,0,0,0,2]);eq(block('---'),[0,0,0,0,0]);
for(let k=1;k<=100;k++){
 const yes=5n*2n**BigInt(k),no=0n;
 let a=[1n,0n,0n,0n,0n];for(let i=0;i<k;i++){let b=block('+++').map(BigInt),next=Array(5).fill(0n);for(let d=0;d<5;d++)for(let e=0;e<5;e++)next[(d+e)%5]+=a[d]*b[e];a=next;}
 eq(5n*a.reduce((x,y)=>x+y,0n),yes);
 eq(5n*a.reduce((x,y)=>x+y,0n)>no,true);
}
console.log(JSON.stringify({run:'TMR-1/083',status:'COMPUTATIONAL',orientation_tables:tables,yes_bundle_transfer:block('+++'),no_bundle_transfer:block('---'),max_k:100,assertions,failures:0},null,2));
