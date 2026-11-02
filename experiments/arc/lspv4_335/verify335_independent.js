#!/usr/bin/env node
// LSPV-4 PROJECTION-ERASER335, independent no-import source-level referee.
// Exhaustive on every Z6/F9 original source assignment and every one-swap
// gadget completion. All-swap outputs use explicit independently checked witnesses.
// No SAT oracle, no free semantic equality, no claim about unrestricted P vs NP.
'use strict';
const Z=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-3],[-1,-4,-5],[-2,-4,-6],[-3,-5,-6]];
const F9=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9],[-4,-6,-8],[-1,-6,-7],[-2,-3,-4],[-3,-5,-8],[-1,-2,-9],[-5,-7,-9]];
let tests=0;
function assert(p,s){tests++;if(!p)throw Error(s);}
function evalCNF(F,a){a=BigInt(a);return F.every(c=>c.some(v=>Number((a>>BigInt(Math.abs(v)-1))&1n)===Number(v>0)));}
function auth(F,n){
 if(n%3||F.length*3!==4*n)return false;
 let pos=Array(n).fill(0),neg=Array(n).fill(0),seen=new Set();
 for(const c of F){
  if(c.length!==3||new Set(c.map(v=>Math.abs(v))).size!==3)return false;
  if(!c.every(v=>Number.isInteger(v)&&v&&Math.abs(v)<=n))return false;
  if(!c.every(v=>v>0)&&!c.every(v=>v<0))return false;
  let id=c.slice().sort((a,b)=>a-b).join(',');
  if(seen.has(id))return false;seen.add(id);
  for(const v of c){if(v>0)pos[v-1]++;else neg[-v-1]++;}
 }
 return pos.every(v=>v===2)&&neg.every(v=>v===2);
}
const nvars=F=>Math.max(...F.flat().map(v=>Math.abs(v)));
const shift=(F,d)=>F.map(c=>c.map(v=>Math.sign(v)*(Math.abs(v)+d)));
function lift(G,j){
 const n=nvars(G),m=G.length,source=G.map(c=>c.slice()),guard=shift(Z,n);
 const k=guard.findIndex(c=>(c[0]>0)===(G[j][0]>0));
 source.push(...guard);
 [source[j][0],source[m+k][0]]=[source[m+k][0],source[j][0]];
 return source;
}
function guardWitness(polarity){
 const k=polarity>0?0:4,cl=Z[k],rest=Z.filter((_,i)=>i!==k);
 return Array.from({length:64},(_,a)=>a).filter(a=>
   evalCNF(rest,a)&&Number((BigInt(a)>>BigInt(Math.abs(cl[0])-1))&1n)===Number(cl[0]>0)
   &&cl.slice(1).some(v=>Number((BigInt(a)>>BigInt(Math.abs(v)-1))&1n)===Number(v>0)));
}
function one(G,j){
 const n=nvars(G),Q=lift(G,j),R=G.filter((_,i)=>i!==j);
 assert(auth(G,n)&&auth(Q,n+6),'auth one-swap');
 let source=0,del=0,proj=0,lifted=0,gain=0,loss=0;
 for(let x=0;x<2**n;x++){
  let old=evalCNF(G,x),r=evalCNF(R,x),z=0;
  for(let a=0;a<64;a++)if(evalCNF(Q,BigInt(x)|(BigInt(a)<<BigInt(n))))z++;
  assert(Boolean(z)===r,'projection x='+x);
  source+=Number(old);del+=Number(r);proj+=Number(z>0);
  lifted+=z;gain+=Number(!old&&z>0);loss+=Number(old&&!z);
 }
 return {n,source,deleted:del,projected:proj,lifted,gain,loss};
}
function eraseAll(G){
 const n=nvars(G),m=G.length,Q=G.map(c=>c.slice()),witnesses=[];
 for(let j=0;j<m;j++){
  const guard=shift(Z,n+6*j),k=guard.findIndex(c=>(c[0]>0)===(G[j][0]>0));
  const guards=guardWitness(G[j][0]);assert(guards.length===6,'six exact witnesses');
  Q.push(...guard);witnesses.push(guards[0]);
  [Q[j][0],Q[m+8*j+k][0]]=[Q[m+8*j+k][0],Q[j][0]];
 }
 assert(auth(Q,n+6*m),'all-swap auth');
 for(let x=0;x<2**n;x++){
  let a=BigInt(x);
  for(let j=0;j<m;j++)a|=BigInt(witnesses[j])<<BigInt(n+6*j);
  assert(evalCNF(Q,a),'all-swap witness');
 }
 return {n:n+6*m,m:Q.length,oldAssignmentsChecked:2**n};
}
function main(){
 assert(auth(Z,6)&&auth(F9,9),'known canonicals');
 let out={Z6:one(Z,0),F9:one(F9,0),Z6_negative:one(Z,4)};
 assert(JSON.stringify(out.Z6)===JSON.stringify({n:6,source:18,deleted:22,projected:22,lifted:318,gain:4,loss:0}),'Z6 counts');
 assert(JSON.stringify(out.F9)===JSON.stringify({n:9,source:70,deleted:83,projected:83,lifted:1117,gain:13,loss:0}),'F9 counts');
 out.allErasedZ6=eraseAll(Z);out.allErasedF9=eraseAll(F9);
 let pins=[0,0];
 for(let x=0;x<512;x++)if(evalCNF(F9,x)&&!(x&(1<<1))&&!(x&(1<<2))&&(x&(1<<5)))pins[x&1]++;
 assert(pins[0]===1&&pins[1]===0,'same source SAT UNSAT pins');
 out.sameOriginalPins=pins;
 let bad=[Z.concat([Z[0]]),Z.slice(1),[[1,-2,3],...Z.slice(1)],[[1,1,3],...Z.slice(1)],[[0,2,3],...Z.slice(1)],[[1,2,7],...Z.slice(1)]];
 for(const b of bad)assert(!auth(b,6),'malformed original accepted');
 out.malformedRejected=bad.length;out.assertions=tests;out.P_vs_NP='OPEN';
 console.log(JSON.stringify(out,null,2));
}
main();
