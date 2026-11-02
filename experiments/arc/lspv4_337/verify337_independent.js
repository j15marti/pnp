#!/usr/bin/env node
"use strict";
// Independent, no-Python-import referee for CONNECTED12-PORT-ROBUST-WIDTH337.
// Exec: node experiments/arc/lspv4_337/verify337_independent.js
const assert=require("assert");
const Z=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-3],[-1,-4,-5],[-2,-4,-6],[-3,-5,-6]];
const F9=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9],[-4,-6,-8],[-1,-6,-7],[-2,-3,-4],[-3,-5,-8],[-1,-2,-9],[-5,-7,-9]];
const K=Z.concat(Z.map(C=>C.map(v=>Math.sign(v)*(Math.abs(v)+6))));
let checks=0;function ck(x,msg){checks++;assert(x,msg);}
const lit=(l,a)=>((a>>(Math.abs(l)-1))&1)===(l>0?1:0);
const sat=(F,a)=>F.every(C=>C.some(l=>lit(l,a)));
function legal(F,n){
 if(F.length*3!==n*4||n%3)return false;
 const d=Array.from({length:n+1},()=>[0,0]),seen=new Set();
 for(const C of F){
  if(C.length!==3||C.some(v=>!Number.isInteger(v)||v===0||Math.abs(v)>n)||new Set(C.map(Math.abs)).size!==3||!C.every(v=>Math.sign(v)===Math.sign(C[0])))return false;
  const key=C.slice().sort((a,b)=>a-b).join(",");
  if(seen.has(key))return false;seen.add(key);
  C.forEach(v=>d[Math.abs(v)][+(v>0)]++);
 }
 return d.slice(1).every(x=>x[0]===2&&x[1]===2);
}
function connected(F,n){
 const adj=Array.from({length:n},()=>new Set());
 for(const C of F)for(const a of C)for(const b of C)if(Math.abs(a)!==Math.abs(b))adj[Math.abs(a)-1].add(Math.abs(b)-1);
 const seen=new Set([0]),queue=[0];
 while(queue.length)for(const b of adj[queue.pop()])if(!seen.has(b)){seen.add(b);queue.push(b);}
 return seen.size===n;
}
function swap(F,i,p,j,q){const C=F.map(c=>c.slice());[C[i][p],C[j][q]]=[C[j][q],C[i][p]];return C;}
function main(){
 ck(legal(Z,6)&&legal(F9,9)&&legal(K,12),"canonical inputs");
 let orig=0;for(let a=0;a<4096;a++)if(sat(K,a))orig++;
 ck(orig===324,"source models");
 const portHist=new Map(),pinHist=new Map();
 let swaps=0,nport=0,npins=0;
 for(const sign of [1,-1])for(let i=0;i<8;i++)for(let j=8;j<16;j++){
   if(Math.sign(K[i][0])!==sign||Math.sign(K[j][0])!==sign)continue;
   for(let p=0;p<3;p++)for(let q=0;q<3;q++){
     const Q=swap(K,i,p,j,q);
     ck(legal(Q,12)&&connected(Q,12),"connected canonical guard");swaps++;
     const M=[];for(let a=0;a<4096;a++)if(sat(Q,a))M.push(a);
     ck(M.length===318,"single swap model count");
     for(const C of Q)for(let v=0;v<3;v++){
       const other=C.filter((_,t)=>t!==v);
       const count=M.reduce((s,a)=>s+(lit(C[v],a)&&(lit(other[0],a)||lit(other[1],a))?1:0),0);
       portHist.set(count,(portHist.get(count)||0)+1);nport++;
     }
     for(let a=1;a<=12;a++)for(let b=a+1;b<=12;b++)for(let u=0;u<2;u++)for(let v=0;v<2;v++){
       const count=M.reduce((s,z)=>s+((((z>>(a-1))&1)===u&&((z>>(b-1))&1)===v)?1:0),0);
       pinHist.set(count,(pinHist.get(count)||0)+1);npins++;
     }
   }
 }
 ck(swaps===288&&nport===13824&&npins===76032,"exhaustive domains");
 const minW=Math.min(...portHist.keys()),minPin=Math.min(...pinHist.keys());
 ck(minW===90&&minPin===37,"minima");
 const guard=swap(K,0,0,8,0),v=guard[0][1],B=[guard[0][0],guard[0][2]];
 const W=[[0,0],[0,0]];
 for(let a=0;a<4096;a++)if(sat(guard.slice(1),a)){
   W[+lit(v,a)][+(lit(B[0],a)||lit(B[1],a))]++;
 }
 ck(JSON.stringify(W)===JSON.stringify([[75,162],[66,90]]),"guard W");
 const E=[[W[1][1],W[0][1]+W[1][1]],[W[1][0]+W[1][1],W.flat().reduce((a,b)=>a+b,0)]];
 ck(JSON.stringify(E)===JSON.stringify([[90,252],[156,393]]),"guard E");
 const raised=guard.map(C=>C.map(l=>Math.sign(l)*(Math.abs(l)+9)));
 const Q=swap(F9.concat(raised),0,0,12,1);
 ck(legal(Q,21)&&connected(Q,21),"connected canonical F9+guard");
 const pivot=[];
 for(const x1 of [0,1]){
   const pins={1:x1,2:0,4:0,6:0};let source=0,deleted=0,lifted=0;
   ck(F9.every(C=>!C.every(l=>pins[Math.abs(l)]!==undefined&&pins[Math.abs(l)]!==+(l>0))),"no direct contradiction");
   for(let x=0;x<512;x++){
     if(Object.entries(pins).some(([k,b])=>((x>>(Number(k)-1))&1)!==b))continue;
     if(sat(F9,x))source++;
     if(!sat(F9.slice(1),x))continue;
     deleted++;
     for(let z=0;z<4096;z++)if(sat(Q,x|(z<<9)))lifted++;
   }
   pivot.push([source,deleted,lifted]);
 }
 ck(JSON.stringify(pivot)===JSON.stringify([[0,2,180],[3,3,468]]),"same original opposite-label lift");
 let malformed=0;
 for(const F of [K.slice(1),K.concat([K[0]]),[[1,1,2],...K.slice(1)],[[1,-2,3],...K.slice(1)],[[1,2,13],...K.slice(1)]]){
  ck(!legal(F,12),"malformed source rejected");malformed++;
 }
 const widths=[];
 for(const r of [8,12,16,20,24]){
   const k=Math.floor((2**r-1)/7),n=3*k,m=4*k;
   const w=Math.ceil(Math.log2(64*(n+m+1))),wp=Math.ceil(Math.log2(64*(n+m+29)));
   const N=(4*m+2)*w,Np=(4*m+66)*wp;
   ck(wp===w+1&&Np-N===(4*m+2)+64*wp,"fixed-width threshold");
   widths.push([n,w,wp,N,Np,Np-N]);
 }
 return {status:"PASS",independent_checks:checks,connected_swaps:swaps,models_per_swap:318,
         two_pin_min:minPin,two_pin_cases:npins,port_min_W11:minW,port_cases:nport,
         port_hist:Object.fromEntries(portHist),pin_hist:Object.fromEntries(pinHist),
         W,E,F9_pivot:pivot,malformed,widths,P_vs_NP:"OPEN"};
}
console.log(JSON.stringify(main(),null,2));
