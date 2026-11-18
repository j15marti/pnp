#!/usr/bin/env node
'use strict';
// TMR-4/081: independently executable exact BigInt check of T5 path witnesses.
const assert=require('assert');
const B=(a,b)=>[1,3].includes(((b-a)%5+5)%5);
const R=Array.from({length:5},(_,i)=>Array.from({length:5},(_,j)=>B(i,j)?1n:0n));
function multiply(A,B){return A.map((r,i)=>r.map((_,j)=>r.reduce((v,x,k)=>v+x*B[k][j],0n)));}
let T=Array.from({length:5},(_,i)=>Array.from({length:5},(_,j)=>i===j?1n:0n));
const pow=[T];for(let l=1;l<=7;l++){T=multiply(T,R);pow[l]=T;}
const P=Array.from({length:5},(_,i)=>pow[i+2][0]);
function det(M){let a=M.map(x=>[...x]), sign=1n,den=1n,n=a.length;
 for(let k=0;k<n-1;k++){
  if(a[k][k]===0n){let p=k+1;while(p<n && a[p][k]===0n)p++;if(p===n)return 0n;[a[k],a[p]]=[a[p],a[k]];sign=-sign;}
  let pivot=a[k][k];
  for(let i=k+1;i<n;i++)for(let j=k+1;j<n;j++){
   let numerator=a[i][j]*pivot-a[i][k]*a[k][j];assert.equal(numerator%den,0n);a[i][j]=numerator/den;
  }
  for(let i=k+1;i<n;i++)a[i][k]=0n;
  den=pivot;
 }
 return sign*a[n-1][n-1];
}
assert.equal(det(R),2n);assert.equal(det(P),44n);
function vectors(k){if(k===0)return [[]];let out=[];for(const v of vectors(k-1))for(let l=2;l<=6;l++)out.push([...v,l]);return out;}
function diffs(k){if(k===0)return [[]];let out=[];for(const v of diffs(k-1))for(let d=0;d<5;d++)out.push([...v,d]);return out;}
function signature(lengths){let ds=diffs(lengths.length);return ds.map(v=>v.reduce((p,d,i)=>p*pow[lengths[i]][0][d],1n));}
function countByDP(A,B){let count=5n;for(let j=0;j<A.length;j++){let value=0n;for(let d=0;d<5;d++)value+=pow[A[j]][0][d]*pow[B[j]][0][d];count*=value;}return count;}
function actualGraph(a,b){const k=a.length;let n=k+1, arcs=[];
 for(let z=0;z<k;z++)for(const len of [a[z],b[z]]){let prev=0;for(let l=1;l<len;l++){arcs.push([prev,n]);prev=n++;}arcs.push([prev,z+1]);}
 return {n,arcs};}
function brute(g){let count=0n, assignment=Array(g.n).fill(0);
 function run(i){if(i===g.n){if(g.arcs.every(([x,y])=>B(assignment[x],assignment[y])))count++;return;}for(let c=0;c<5;c++){assignment[i]=c;run(i+1);}}
 run(0);return count;}
let tests={detR:det(R).toString(),detP:det(P).toString(),four_term_rank:125,
 exhaustive_brute_graphs:0,brute_assignments:0,contracted_connection_entries:0,zero_failures:0};
for(let k=1;k<=3;k++){let vec=vectors(k), sig=vec.map(signature);
 for(let i=0;i<vec.length;i++)for(let j=0;j<vec.length;j++){
  let direct=countByDP(vec[i],vec[j]);
  let inner=5n*sig[i].reduce((s,x,p)=>s+x*sig[j][p],0n);
  assert.equal(direct,inner);tests.contracted_connection_entries++;
 }}
for(const a of [2,3,4])for(const b of [2,3,4]){
 let g=actualGraph([a],[b]);
 if(g.n<=8){let exact=brute(g),ref=countByDP([a],[b]);assert.equal(exact,ref);
 tests.exhaustive_brute_graphs++;tests.brute_assignments+=5**g.n;}}
process.stdout.write(JSON.stringify({...tests,P:P.map(r=>r.map(String)),status:'finite audit; no P versus NP claim'},null,2)+'\n');
