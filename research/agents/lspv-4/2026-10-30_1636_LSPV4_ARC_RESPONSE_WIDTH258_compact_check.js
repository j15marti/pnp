"use strict";
/* ARC-RESPONSE-WIDTH258 independently runnable standard Node.js source/width audit. */
const assert=require("assert");
const W="-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14";
const W1=W.split(";").map(s=>s.trim().split(/\s+/).map(Number));
const W1prime=W1.map(c=>c.slice());assert.equal(W1prime[7][0],1);assert.equal(W1prime[19][0],-1);W1prime[7][0]=-1;W1prime[19][0]=1;
const S=[[-1,-2,-3],[-1,-2,3],[-1,2,-3],[-1,2,3],[1,-2,-3],[1,-2,3],[1,2,-3]];
const U=S.concat([[1,2,3]]);
const cases=[["W1",W1,15,0],["W1prime",W1prime,15,168],["S",S,3,1],["U",U,3,0]];
const truth=(lit,a)=>Number((a>>>(Math.abs(lit)-1))&1)===Number(lit>0);
function local(clause,type){const t={};for(const l of clause)t[Math.abs(l)]=type==="S"?Number(l>0):Number(l<0);return t;}
function pair(A,B) {const p={};for(const u of ["S","U"])for(const v of ["S","U"]){const x=local(A,u),y=local(B,v);
 p[u+v]=Object.keys(x).every(k=>!(k in y)||x[k]===y[k]);}return p;}
function brute(A,B){const ids=[...new Set([...A,...B].map(Math.abs))];const p={SS:false,SU:false,US:false,UU:false};
 for(let mask=0;mask<(1<<ids.length);mask++){const a={};ids.forEach((x,k)=>a[x]=(mask>>k)&1);
  const t=c=>c.reduce((s,l)=>s+Number(a[Math.abs(l)]===Number(l>0)),0),i=t(A),j=t(B);
  for(const z of ["SS","SU","US","UU"])if(i===(z[0]==="S"?3:0)&&j===(z[1]==="S"?3:0))p[z]=true;}
 return p;}
let pairModes=0;
for(const [name,F,n,want] of cases){
 let models=0,all=(1<<n)-1;
 for(const c of F) {assert.equal(c.length,3);assert.equal(new Set(c.map(Math.abs)).size,3);
  const x=local(c,"S"),y=local(c,"U");for(const k of Object.keys(x))assert.equal(x[k],1-y[k]);}
 for(let i=0;i<F.length;i++)for(let j=i+1;j<F.length;j++){
  assert.deepEqual(pair(F[i],F[j]),brute(F[i],F[j]));pairModes+=4;}
 for(let a=0;a<=all;a++){
  const h=[0,0,0,0],g=[0,0,0,0];
  for(const c of F){h[c.reduce((s,l)=>s+Number(truth(l,a)),0)]++;
                     g[c.reduce((s,l)=>s+Number(truth(l,all^a)),0)]++;}
  for(let r=0;r<4;r++)assert.equal(h[r],g[3-r]);
  if(h[0]===0)models++;
 }
 assert.equal(models,want,name+" model count");
}
assert.equal(pairModes,1744);assert(W1prime.every(c=>c.some(l=>truth(l,97))));
// Exact-rational FLMV Theorem 5.7 envelope, certified tail.
const abs=x=>x<0n?-x:x;
function gcd(a,b){a=abs(a);b=abs(b);while(b){const t=a%b;a=b;b=t;}return a;}
function f(a,b=1n){a=BigInt(a);b=BigInt(b);const g=gcd(a,b);return [a/g,b/g];}
const add=(a,b)=>f(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const mul=(a,b)=>f(a[0]*b[0],a[1]*b[1]);
const div=(a,b)=>f(a[0]*b[1],a[1]*b[0]);
const sub=(a,b)=>add(a,[-b[0],b[1]]);
const lt=(a,b)=>a[0]*b[1]<b[0]*a[1];
const str=x=>x[0]+"/"+x[1];
function envelope(c,kmax=24){let fk=f(1),best=f(0),where=0,tail=null,ck=f(1);const one=f(1);
 for(let k=1;k<=kmax;k++){
  fk=div(mul(c,fk),add(one,fk));ck=mul(ck,c);
  const a=div(sub(div(one,fk),c),f(k)),b=div(one,ck);
  const d=lt(a,b)?a:b;if(lt(best,d)){best=d;where=k;}
  const bound=div(b,c);
  if(lt(bound,best)){tail=k+1;break;}
 }
 assert(tail!==null);return {best:str(best),where,tail};}
const flmv=[["6/5",f(6,5),"23/45",2,4],["241/200",f(241,200),"11642479/23232400",2,4],["7/5",f(7,5),"949/5145",3,6]];
for(const [name,c,target,k,tail] of flmv){const z=envelope(c);assert.equal(z.best,target);assert.equal(z.where,k);assert.equal(z.tail,tail);}
// Prefix-equivalence classes in a fixed stream.
function residualWidth(q,k,kind){
 const h=q/2;
 function yes(mask){
  if(kind==="and")return mask===(1<<q)-1;
  const v=Array(q).fill(0);
  for(let pos=0;pos<q;pos++){const index=kind==="paired"?(pos%2===0?pos/2:h+(pos-1)/2):pos;
    v[index]=(mask>>pos)&1;}
  return v.slice(0,h).every((b,j)=>b===v[h+j]);}
 const signatures=new Set();
 for(let u=0;u<(1<<k);u++){
  let s="";for(let tail=0;tail<(1<<(q-k));tail++)s+=yes((u<<(q-k))|tail)?"1":"0";
  signatures.add(s);}
 return signatures.size;}
for(let h=1;h<=7;h++){
 const q=2*h;assert.equal(residualWidth(q,h,"blocked"),1<<h);
 let max=0;for(let k=0;k<=q;k++)max=Math.max(max,residualWidth(q,k,"paired"));
 assert(max<=3);
}
assert.equal(residualWidth(12,6,"blocked"),64);
assert.equal(residualWidth(12,5,"paired"),3);
assert.equal(residualWidth(12,6,"and"),2);
process.stdout.write(JSON.stringify({result:"PASS",pair_modes:pairModes,model_counts:{W1:0,W1prime:168,S:1,U:0},FLMV:flmv.map(([c,_,d,k,tail])=>({c,d,k,tail})),blocked_q12_midpoint_states:64,paired_q12_max_states:3})+"\n");