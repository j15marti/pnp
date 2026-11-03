#!/usr/bin/env node
"use strict";
/* Independent executable control for LSPV4 367, deterministic exhaustive.
 * node experiments/arc/lspv4_367_source_exact_library_compact.js
 */
const assert=require("assert");
function library(n){
 const out=[];
 function go(i,C){if(i===n){if(C.length)out.push(C.slice());return;}
 go(i+1,C); C.push(i+1);go(i+1,C);C.pop();
 C.push(-(i+1));go(i+1,C);C.pop();}
 go(0,[]);return out;
}
function assignments(n){return Array.from({length:2**n},(_,m)=>Array.from({length:n},(_,i)=>Boolean((m>>i)&1)));}
function satClause(C,a){return C.some(l=>a[Math.abs(l)-1]===(l>0));}
function sat(F,n){return assignments(n).some(a=>F.every(C=>satClause(C,a)));}
const stats={date:"2026-11-03 11:36 PST",scope:"auxiliary-only restriction with fixed witness variables",
unsat:0, deletionSAT:0,flipSAT:0,exactRestrictions:0,checks:0,perN:{}};
function ok(x,msg){assert.ok(x,msg);stats.checks++;}
for(let n=1;n<=6;n++){
 const D=library(n);ok(D.length===3**n-1,"3^n-1");
 let deletions=0,flips=0;
 for(const C of D){
   const F=[C,...C.map(l=>[-l])];ok(!sat(F,n),"F_C UNSAT");stats.unsat++;
   for(let i=0;i<F.length;i++){
      ok(sat(F.filter((_,j)=>i!==j),n),"every clause indispensable");
      stats.deletionSAT++;deletions++;
      for(let j=0;j<F[i].length;j++){
        const G=F.map((row,k)=>i===k?row.map((l,z)=>z===j?-l:l):row);
        ok(sat(G,n),"sign flip makes SAT");
        stats.flipSAT++;flips++;
      }
   }
 }
 stats.perN[n]={distinctClauses:D.length,deletedSAT:deletions,signFlipSAT:flips};
 if(n<=3){
   const z=D.map((_,i)=>n+i+1),p=D.map((_,i)=>n+D.length+i+1);
   const H=[[-z[0],p[0]],[z[0],-p[0]]];
   for(let i=1;i<D.length;i++){
      H.push([-p[i-1],p[i]],[-z[i],p[i]],[p[i-1],z[i],-p[i]],[-p[i-1],-z[i]]);
   }
   H.push([p[p.length-1]]);
   for(let i=0;i<D.length;i++){
      H.push([-z[i],...D[i]]);
      for(const l of D[i])H.push([-z[i],-l]);
   }
   for(let idx=0;idx<D.length;idx++){
      const rho=new Map(z.map((v,i)=>[v,i===idx]));
      p.forEach((v,i)=>rho.set(v,i>=idx));
      const residual=[];
      for(const C of H){
        if(C.some(l=>rho.has(Math.abs(l)) && rho.get(Math.abs(l))===(l>0)))continue;
        residual.push(C.filter(l=>!rho.has(Math.abs(l))));
      }
      const expected=[D[idx],...D[idx].map(l=>[-l])];
      ok(JSON.stringify(residual)===JSON.stringify(expected),"source-exact restriction");
      stats.exactRestrictions++;
   }
   stats.perN[n].wrapperClauses=H.length;
 }
}
function k4(charge){
 const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]], F=[];
 for(let v=0;v<4;v++){
   const edgeids=E.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
   for(let t=0;t<8;t++){
      const bits=[0,1,2].map(i=>(t>>i)&1);
      if(bits.reduce((a,b)=>a+b,0)%2===charge[v])continue;
      F.push(edgeids.map((e,i)=>(bits[i]?-1:1)*(e+1)));
   }
 }
 return F;
}
const mOdd=assignments(6).filter(a=>k4([1,0,0,0]).every(c=>satClause(c,a))).length;
const mEven=assignments(6).filter(a=>k4([0,0,0,0]).every(c=>satClause(c,a))).length;
ok(mOdd===0 && mEven===8,"odd/even Tseitin control");
stats.parity={odd:mOdd,even:mEven};stats.success=true;
console.log(JSON.stringify(stats,null,2));
