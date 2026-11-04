#!/usr/bin/env node
'use strict';
// LSPV-3/400 independent exhaustive verifier: all (m+1)-dim affine flats, 1<=m<=3.
// Run: node experiments/arc/lspv3_400_affine_flat_checker.js
const assert=require('node:assert/strict');
let checks=0;
function ok(t,msg){ checks++; assert.ok(t,msg); }
function ip(m,x){let r=0;for(let i=0;i<m;i++)r^=((x>>(2*i))&1)&((x>>(2*i+1))&1);return r;}
function combos(n,k){let ans=[];function go(a,j){if(a.length===k){ans.push(a.slice());return;}for(let i=j;i<=n-(k-a.length);i++){a.push(i);go(a,i+1);a.pop();}}go([],0);return ans;}
function subspaces(n,d){let out=[];
 for(let pivots of combos(n,d)){
  let free=[];
  for(let i=0;i<d;i++)for(let col=pivots[i]+1;col<n;col++)if(!pivots.includes(col))free.push([i,col]);
  for(let choice=0;choice<2**free.length;choice++){
   let b=pivots.map(p=>1<<p);
   for(let j=0;j<free.length;j++)if(choice&(1<<j)){let [i,col]=free[j];b[i]|=1<<col;}
   out.push(b);
  }
 }return out;
}
function span(b){let xs=[0];for(let v of b)xs=xs.concat(xs.map(x=>x^v));return xs;}
function affine(m,z,b){let c=ip(m,z),d=b.map(v=>ip(m,z^v)^c);
 for(let t=0;t<(1<<b.length);t++){
  let x=z,val=c;for(let j=0;j<b.length;j++)if((t>>j)&1){x^=b[j];val^=d[j];}
  if(ip(m,x)!==val)return false;
 }return true;
}
let rows=[];
for(let m=1;m<=3;m++){
 let n=2*m,d=m+1,subs=subspaces(n,d),cosets=0,bad=0;
 for(let b of subs){
  let S=span(b);ok(new Set(S).size===(1<<d),'independent basis');
  let reps=new Set();for(let x=0;x<(1<<n);x++)reps.add(Math.min(...S.map(y=>x^y)));
  ok(reps.size===(1<<(n-d)),'correct coset count');
  for(let z of reps){cosets++;if(affine(m,z,b))bad++;}
 }
 ok(bad===0,'larger-than-m affine flat');
 let good=Array.from({length:m},(_,j)=>1<<(2*j));
 ok(affine(m,0,good),'dimension m control');
 rows.push({m,maximum_affine_flat_dimension:m,subspaces_dim_m_plus_1:subs.length,cosets_checked:cosets,violations:bad});
}
ok(ip(1,3)===1,'one product true');
ok(ip(2,15)===0,'even product parity');
ok(ip(3,63)===1,'odd product parity');
console.log(JSON.stringify({schema:'LSPV3-400-independent-affine-flat-v1',status:'FINITE_ENUMERATION_ONLY',checks,rows},null,2));
