"use strict";
let checks = 0;
const ck = (v, m) => { checks++; if (!v) throw Error(m); };
const pts = [[0,0],[0,1],[1,0],[1,1]];
const q1 = (u,v) => u & v;
const q2 = (u,v) => u & (1 ^ v);
const e = (u,v) => q1(u,v) ^ q2(u,v);
const affine = (a,u,v) => a[0] ^ (a[1]&u) ^ (a[2]&v);
const allA = [];
for(let a=0;a<8;a++) allA.push([a&1,(a>>1)&1,(a>>2)&1]);
ck(pts.some(([u,v])=>q1(u,v)!==q2(u,v)),"distinct coordinates");
for(const q of [q1,q2]) ck(!allA.some(a=>pts.every(([u,v])=>q(u,v)===affine(a,u,v))),"nonlinear coordinate");
ck(pts.every(([u,v])=>e(u,v)===u),"quadratic cancellation");
let fullBest=0, outBest=0;
for(const a of allA) for(const b of allA)
  fullBest=Math.max(fullBest,pts.filter(([u,v])=>q1(u,v)===affine(a,u,v)&&q2(u,v)===affine(b,u,v)).length);
for(const a of allA) outBest=Math.max(outBest,pts.filter(([u,v])=>e(u,v)===affine(a,u,v)).length);
ck(fullBest===3&&outBest===4,"affine optimums");

const w=1,t=2,v=3,o=4;
const val=(lit,A)=>lit>0?A[lit]:!A[-lit];
const sat=(C,A)=>C.some(l=>val(l,A));
const P=[-w,v], bad=[w,-v,o], good=[-w,-v,o];
let badWitness=[];
for(const W of [0,1]) for(const T of [0,1]){
  const V=W|T,E=W&V,A={1:!!W,2:!!T,3:!!V,4:!!E};
  ck(sat(P,A)&&sat(good,A)&&E===W,"correct absorption facets");
  if(!sat(bad,A)) badWitness.push({w:W,t:T,v:V,e:E});
}
ck(JSON.stringify(badWitness)===JSON.stringify([{w:0,t:1,v:1,e:0}]),"published facet countermodel");
const resolve=(A,B,p)=>{
  ck(A.includes(p)&&B.includes(-p),"oriented pivot");
  const C=[...new Set(A.filter(x=>x!==p).concat(B.filter(x=>x!==-p)))].sort((a,b)=>a-b);
  ck(!C.some(x=>C.includes(-x)),"non-tautological resolvent"); return C;
};
ck(JSON.stringify(resolve(P,good,v))===JSON.stringify([-w,o]),"correct signed resolvent");
let rejected=false; try{resolve(P,bad,v)}catch{rejected=true} ck(rejected,"bad sign rejected");
process.stdout.write(JSON.stringify({status:"PASS",assertions:checks,fullBest,outBest,badWitness},null,2)+"\n");
