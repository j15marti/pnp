#!/usr/bin/env node
// LSPV4 336 no-producer-import independent native JS referee. No FLMV native costs.
'use strict';
const assert=require('node:assert/strict');
const Z=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-3],[-1,-4,-5],[-2,-4,-6],[-3,-5,-6]];
const F=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9],[-4,-6,-8],[-1,-6,-7],[-2,-3,-4],[-3,-5,-8],[-1,-2,-9],[-5,-7,-9]];
let assertions=0;
function check(x,s){assertions++;assert.equal(x,true,s);}
const cl=(c,a)=>c.some(x=>Boolean((a>>>(Math.abs(x)-1))&1)===(x>0));
const cnf=(f,a)=>f.every(c=>cl(c,a));
function valid(f,n){
 if(n%3||f.length*3!==4*n)return false;
 let p=Array(n).fill(0),q=Array(n).fill(0),seen=new Set();
 for(const c of f){
  if(c.length!==3||new Set(c.map(x=>Math.abs(x))).size!==3)return false;
  if(c.some(x=>!Number.isInteger(x)||x===0||Math.abs(x)>n))return false;
  if(!(c.every(x=>x>0)||c.every(x=>x<0)))return false;
  const key=c.slice().sort((a,b)=>a-b).join(',');
  if(seen.has(key))return false;seen.add(key);
  for(const x of c){if(x>0)p[x-1]++;else q[-x-1]++;}
 }
 return [...p,...q].every(x=>x===2);
}
function shapes(){
 let t=[],o=[];
 for(let a=0;a<6;a++)for(let b=a+1;b<6;b++)for(let c=b+1;c<6;c++)t.push([a,b,c]);
 for(let a=0;a<t.length;a++)for(let b=a+1;b<t.length;b++)for(let c=b+1;c<t.length;c++)for(let d=c+1;d<t.length;d++){
  const set=[t[a],t[b],t[c],t[d]],counts=Array(6).fill(0);
  for(const triple of set)for(const i of triple)counts[i]++;
  if(counts.every(x=>x===2))o.push(set);
 }
 return o;
}
function pop(m){let r=0;while(m){m&=m-1n;r++;}return r;}
function fullMask(f){let m=0n;for(let a=0;a<64;a++)if(cnf(f,a))m|=1n<<BigInt(a);return m;}
function literalMask(x){let m=0n;for(let a=0;a<64;a++)if(Boolean((a>>>(Math.abs(x)-1))&1)===(x>0))m|=1n<<BigInt(a);return m;}
function guards(){
 const sets=shapes();check(sets.length===75,'75 exact shapes');
 let modelHist=new Map(),portHist=new Map(),ports=0;
 for(const P of sets)for(const N of sets){
  const f=[...P.map(c=>c.map(x=>x+1)),...N.map(c=>c.map(x=>-x-1))];
  check(valid(f,6),'original grammar');
  const v=pop(fullMask(f));modelHist.set(v,(modelHist.get(v)||0)+1);
  for(let d=0;d<8;d++)for(let pivot=0;pivot<3;pivot++){
   const D=f[d],H=fullMask(f.filter((_,i)=>i!==d));
   const B=D.filter((_,j)=>j!==pivot);
   const w=pop(H & literalMask(D[pivot]) & (literalMask(B[0])|literalMask(B[1])));
   portHist.set(w,(portHist.get(w)||0)+1);ports++;
  }
 }
 check(ports===135000,'complete signed port scan');
 check(Math.min(...portHist.keys())===4,'sharp min W11');
 const out={shapes:sets.length,closed_originals:sets.length**2,ports,
  models:Object.fromEntries([...modelHist.entries()].sort((a,b)=>a[0]-b[0])),
  W11:Object.fromEntries([...portHist.entries()].sort((a,b)=>a[0]-b[0]))};
 check(JSON.stringify(out.W11)===JSON.stringify({'4':5040,'5':16560,'6':40680,'7':36720,'8':27360,'9':7560,'10':1080}),'signed distribution');
 return out;
}
function swapF(){
 const Q=F.map(x=>x.slice()).concat(Z.map(c=>c.map(x=>Math.sign(x)*(Math.abs(x)+9))));
 [Q[0][0],Q[12][0]]=[Q[12][0],Q[0][0]];
 check(valid(Q,15),'swapped output canonical');
 let rows=[];
 for(let p=0;p<2;p++){
  let original=0,deleted=0,lift=0,empty=0;
  for(const c of F)if(c.every(x=>[1,2,4,6].includes(Math.abs(x)) && Boolean({1:p,2:0,4:0,6:0}[Math.abs(x)])!==(x>0)))empty++;
  for(let a=0;a<512;a++){
   if((a&1)!==p || ((a>>1)&1)!==0 || ((a>>3)&1)!==0 || ((a>>5)&1)!==0)continue;
   original+=Number(cnf(F,a));deleted+=Number(cnf(F.slice(1),a));
   for(let b=0;b<64;b++)lift+=Number(cnf(Q,a+(b<<9)));
  }
  rows.push({x1:p,original,deleted,lift,empty});
 }
 check(JSON.stringify(rows)===JSON.stringify([{x1:0,original:0,deleted:2,lift:12,empty:0},{x1:1,original:3,deleted:3,lift:27,empty:0}]),'same-original collapse');
 return rows;
}
function reducedBDD(order){
 let intern=new Map(),next=2;
 function visit(level,a){
  if(level===9)return Number(cnf(F,a));
  let bit=1<<(order[level]-1);
  const lo=visit(level+1,a&~bit),hi=visit(level+1,a|bit);
  if(lo===hi)return lo;
  const key=order[level]+':'+lo+':'+hi;
  if(!intern.has(key))intern.set(key,next++);
  return intern.get(key);
 }
 visit(0,0);return intern.size;
}
function main(){
 check(valid(F,9)&&valid(Z,6),'two certified originals');
 check(Array.from({length:512},(_,a)=>Number(cnf(F,a))).reduce((x,y)=>x+y,0)===70,'F9 models');
 const r={n6:guards(),F9_opposite_pin:swapF(),BDD:{}};
 for(const [name,order,expected] of [['minimum',[2,6,7,9,8,4,3,1,5],52],['natural',[1,2,3,4,5,6,7,8,9],66],['maximum',[2,6,8,9,1,3,4,5,7],80]]){
  let nodes=reducedBDD(order);check(nodes===expected,'BDD '+name);r.BDD[name]=nodes;
 }
 const malformed=[[...Z,Z[0]],Z.slice(1),[[1,-2,3],...Z.slice(1)],[[1,1,3],...Z.slice(1)],[[0,2,3],...Z.slice(1)],[[1,2,7],...Z.slice(1)]];
 for(const bad of malformed)check(!valid(bad,6),'invalid input rejection');
 r.assertions=assertions;r.status='COMPUTATIONAL independent; P versus NP OPEN';
 console.log(JSON.stringify(r,null,2));
}
main();
