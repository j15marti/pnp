#!/usr/bin/env node
'use strict';
// An independent floating-point and Boolean-source control, NOT a native FLMV interpreter.
const assert = require('node:assert/strict');
let passed=0;
function check(x,label){passed++;if(!x)throw Error("check "+passed+" "+label)}
function beta(c){return 0.5*((c+2)/(c*c)-c)}
function poly(e){return ((1000*e+1750)*e+895)*e-2}
function step(t,s,e){return [Math.max(1.1,0.6+t/2)+e,Math.max(0.5,s/2)+e]}
function margin(e){return beta(1.2+2*e)-0.5-e}
let lo=0,hi=.01;
check(poly(lo)<0 && poly(hi)>0,'root bracket');
for(let i=0;i<90;i++){let m=(lo+hi)/2;if(poly(m)<0)lo=m;else hi=m}
let root=(lo+hi)/2;
check(root>0.00222494504 && root<0.00222494506,'root independent');
const eps=[0,.0001,.001,.002,1/450,.0025];
let state=128744;
function random(){state=(Math.imul(state,1664525)+1013904223)>>>0;return state/2**32}
const L=433/216;
let worstBoundSlack=Infinity;
let maxDepth=0;
for(let e of eps){
 const c=1.2+2*e, sf=.5+e, gap=margin(e);
 let formula=-poly(e)/(20*(5*e+3)**2);
 check(Math.abs(formula-gap)<3e-14,'independent closed-form');
 let [ct,cs]=step(c,sf,e);
 check(Math.abs(ct-c)<2e-15 && Math.abs(cs-sf)<2e-15,'fixed point');
 check((gap>0)==(e<root),'sign');
 for(let i=0;i<200;i++){
  const t0=1+random()*75, s0=random()*35;
  const A=L*Math.max(0,t0-c)+Math.max(0,s0-sf);
  let [t,s]=[t0,s0];let first=-1;
  for(let j=0;j<85;j++){
   let actual=beta(t)-s, bound=gap-2**(-j)*A;
   worstBoundSlack=Math.min(worstBoundSlack,actual-bound);
   check(actual>=bound-2e-12,'mean-value envelope');
   check(Math.abs(t-c)<=2**(-j)*Math.abs(t0-c)+2e-13,'time contraction');
   check(Math.abs(s-sf)<=2**(-j)*Math.abs(s0-sf)+2e-13,'space contraction');
   if(actual>0 && first===-1)first=j;
   [t,s]=step(t,s,e)
  }
  if(gap>0){check(first>=0,'must reach strict region');maxDepth=Math.max(maxDepth,first)}
 }
}
// K4 original source, independent of the Python construction's bit mapping.
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const incident=Array.from({length:4},(_,v)=>edges.map(([a,b],i)=>a===v||b===v?i:-1).filter(i=>i>=0));
function validK4(source){
 const expected=incident.map(xs=>xs.map(x=>x+1).sort((a,b)=>a-b).join(','));
 const groups=new Map();
 for(let cl of source){
  if(!Array.isArray(cl)||cl.length!==3||cl.some(x=>!Number.isSafeInteger(x)||x===0))return false;
  const support=cl.map(Math.abs).sort((a,b)=>a-b);
  if(new Set(support).size!==3||!expected.includes(support.join(',')))return false;
  const key=support.join(',');if(!groups.has(key))groups.set(key,[]);groups.get(key).push(cl);
 }
 if(groups.size!==4)return false;
 for(let [key,clauses] of groups){
  if(clauses.length!==4)return false;
  const support=key.split(',').map(Number);
  const masks=clauses.map(cl=>support.map(x=>cl.some(l=>l===-x)?1:0).join(''));
  if(new Set(masks).size!==4||new Set(masks.map(bits=>[...bits].reduce((x,y)=>x^Number(y),0))).size!==1)return false;
 }
 return true;
}
let SAT=0,UNSAT=0; let hostile=0;
for(let charge=0;charge<16;charge++){
 const cls=[];
 for(let v=0;v<4;v++)for(let bits=0;bits<8;bits++){
  let chi=(charge>>v)&1;
  let parity=((bits&1)^((bits>>1)&1)^((bits>>2)&1));
  if(parity===chi)continue;
  cls.push(incident[v].map((e,k)=>((bits>>k)&1)?-(e+1):(e+1)));
 }
 check(cls.length===16 && cls.every(cl=>new Set(cl.map(Math.abs)).size===3),'proper source');
 check(validK4(cls),'K4 source facets');
 if(charge===0){
  const corrupted=[
   cls.slice(0,-1),[...cls.slice(0,-1),cls[0]],
   cls.map((cl,i)=>i===0?[-cl[0],cl[1],cl[2]]:cl),
   cls.map((cl,i)=>i===0?[999,cl[1],cl[2]]:cl),
   cls.map((cl,i)=>i===0?cl.slice(0,2):cl),
   cls.map((cl,i)=>i===0?[0,cl[1],cl[2]]:cl)
  ];
  for(let bad of corrupted){check(!validK4(bad),'hostile K4 corruption rejected');hostile++}
 }
 let count=0;
 for(let a=0;a<64;a++){
  let cnf=cls.every(cl=>cl.some(l=>l>0?Boolean(a&(1<<(l-1))):!Boolean(a&(1<<(-l-1)))));
  let eq=incident.every((incs,v)=>incs.reduce((acc,i)=>acc^((a>>i)&1),0)===((charge>>v)&1));
  check(cnf===eq,'original parity equivalent');
  count+=cnf?1:0;
 }
 check(count=== (popcount(charge)%2===0?8:0),'models');
 if(count)SAT++;else UNSAT++;
}
function popcount(x){let k=0;while(x){k+=x&1;x>>=1}return k}
check(SAT===8 && UNSAT===8,'both labels');
console.log(JSON.stringify({run:'LSPV-2/486 independent JS',root,checks:passed,maxDepth,worstBoundSlack,SAT,UNSAT,hostile,status:'restricted arithmetic / original-source controls only; no FLMV execution'},null,2));
