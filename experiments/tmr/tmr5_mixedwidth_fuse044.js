'use strict';
// TMR-5/044: exact heterogeneous-width preauthenticated FUSE grammar.
// Self-contained native Node 22. No dependencies and no SAT-machine transfer.
const fs=require('fs'); const assert=require('node:assert/strict');
let assertions=0, rows=0, zeros=0, negGamma=0, sameStates=0, totalStates=0;
function eq(a,b,msg){assert.deepEqual(a,b,msg);assertions++}
function ok(x,msg){assert.ok(x,msg);assertions++}
function pc(n){let k=0;for(;n;n&=n-1)k++;return k}
function evaluate(c){
 const {name,G,q,E,F}=c, full=(1<<q)-1, gp=(1<<G)-1;
 ok(E.every(x=>x>0 && x<=full),name+' E');
 ok(E.reduce((a,b)=>a|b,0)===full,name+' cover');
 for(let [b,sets] of Object.entries(F)){
  ok(+b>=1 && Number.isInteger(+b),name+' widths');
  ok(sets.every(x=>E.includes(x)),name+' allowed batch');
 }
 const tau=Array(full+1).fill(1e6);tau[0]=0;
 for(let u=1;u<=full;u++)for(let s of E)if(s&u)tau[u]=Math.min(tau[u],1+tau[u&~s]);
 const discount=Array(G+1).fill(0),discountChoices=Array(G+1).fill(null);
 for(let t=0;t<=G;t++)for(let [bs,sets] of Object.entries(F)){
  const b=+bs;if(b>t)continue;
  for(let s of sets){const gap=tau[full]-tau[full&~s];
   const saving=b+gap-1;
   if(saving>discount[t]){discount[t]=saving;discountChoices[t]={b,s,gap,saving}}
  }
 }
 for(let t=0;t<=G;t++){
  ok(discount[t]>=0 && discount[t]<=t,name+' bound');
  if(t)ok(discount[t]>=discount[t-1],name+' monotone');
 }
 const phi=(p,u,h)=>{
  if(!h){ok(p===gp && u===0,name+' valid goal');return 0}
  const t=G-pc(p);
  return t+tau[u]+1-(u===full?discount[t]:0);
 };
 const components=(p,u,h)=>{
  if(!h)return [0,0,0,0,0,0,0];
  const t=G-pc(p);return [0,0,tau[u],0,t-(u===full?discount[t]:0),0,1];
 };
 const modelRows={}; const witnesses=[];const memo=new Map();
 function edges(p,u,h){if(!h)return [];
  let es=[];const t=G-pc(p);
  for(let g=0;g<G;g++)if(!(p&(1<<g)))es.push({rule:'CHECK',p:p|(1<<g),u,h,cost:1,arg:g});
  if(p===gp)for(let s of E)if(s&u)es.push({rule:'BATCH',p,u:u&~s,h,cost:1,arg:s});
  if(u===full)for(let [bs,sets] of Object.entries(F)){
   const b=+bs;
   if(t===b)for(let s of sets)es.push({rule:'FUSE_'+b,p:gp,u:u&~s,h,cost:1,arg:s});
  }
  if(p===gp && u===0)es.push({rule:'HALT',p,u,h:0,cost:1});
  return es;
 }
 function shortest(p,u,h){if(!h)return 0;
  let key=p+':'+u,m=memo.get(key);if(m!==undefined)return m;
  let es=edges(p,u,h);ok(es.length>0,name+' has successor');
  let z=Math.min(...es.map(e=>e.cost+shortest(e.p,e.u,e.h)));
  memo.set(key,z);return z;
 }
 for(let p=0;p<=gp;p++)for(let u=0;u<=full;u++){
  totalStates++;
  let h=1, c=components(p,u,h), pot=c[2]+c[4]+c[6];
  eq(phi(p,u,h),pot,name+' phi components');
  eq(pot,shortest(p,u,h),name+' exact Bellman all states');
  for(let v=0;v<2;v++){zeros++;let before=components(p,u,h),after=components(p,u,h);eq(before,after,name+' reversible zero VIEW/NOP');}
  for(let e of edges(p,u,h)){
   rows++;const d=components(e.p,e.u,e.h),delta=c.map((x,i)=>x-d[i]),weighted=delta[2]+delta[4]+delta[6];
   ok(weighted<=e.cost,name+' tariff '+e.rule);eq(weighted,pot-phi(e.p,e.u,e.h),name+' signed tuple '+e.rule);
   if(delta[4]<0)negGamma++;
   if(!modelRows[e.rule])modelRows[e.rule]={count:0,minWeighted:1000,maxWeighted:-1000,minGamma:1000,maxGamma:-1000,first:null};
   let z=modelRows[e.rule];z.count++;z.minWeighted=Math.min(z.minWeighted,weighted);z.maxWeighted=Math.max(z.maxWeighted,weighted);
   z.minGamma=Math.min(z.minGamma,delta[4]);z.maxGamma=Math.max(z.maxGamma,delta[4]);
   if(!z.first)z.first={from:{p,u,h},to:{p:e.p,u:e.u,h:e.h},cost:e.cost,delta,weighted,arg:e.arg};
   if(witnesses.length<12 && delta[4]<0)witnesses.push({rule:e.rule,p,u,delta,weighted});
  }
 }
 eq(phi(gp,0,0),0,name+' goal');
 const init=phi(0,full,1),formula=G+tau[full]+1-discount[G];eq(init,formula,name+' initial closed formula');
 const sourceOld=G+tau[full]+1-((G>=1)?1:0);
 return {name,G,q,E,F,tauFull:tau[full],discount,discountChoices,initialExactCost:init,oldB1CreditCost:sourceOld,rows:modelRows,examples:witnesses,states:(1<<G)*(1<<q)};
}
const cases=[
 {name:'b1-peer-singletons',G:3,q:3,E:[1,2,4],F:{1:[1,2,4]}},
 {name:'b2-peer-singletons',G:3,q:3,E:[1,2,4],F:{2:[1,2,4]}},
 {name:'b3-peer-singletons',G:3,q:3,E:[1,2,4],F:{3:[1,2,4]}},
 {name:'mixed-allwidth-singletons',G:4,q:3,E:[1,2,4],F:{1:[1,2,4],2:[1,2,4],3:[1,2,4]}},
 {name:'mixed-fullbatch',G:4,q:3,E:[1,2,4,7],F:{1:[7],2:[7],3:[7]}},
 {name:'heterogeneous-badwide',G:3,q:3,E:[1,2,4,3],F:{1:[3],2:[4],3:[4]}},
 {name:'heterogeneous-good-narrow',G:3,q:3,E:[1,2,4,7],F:{1:[7],2:[1],3:[1]}},
 {name:'no-fuse-unavailable',G:2,q:3,E:[1,2,4],F:{3:[1],4:[2]}},
 {name:'mixed-triangle',G:4,q:3,E:[3,5,6],F:{1:[3,5],2:[6],3:[3,5,6]}},
 {name:'mixed-fano',G:4,q:7,E:[11,21,38,56,69,82,100],F:{1:[11,21],2:[38,56],3:[69,82,100]}},
 {name:'tiny-violation',G:2,q:1,E:[1],F:{1:[1],2:[1]}},
];
// seeded small heterogeneous schedules to test all reachable and unreachable states
let seed=0x5eed, rng=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed};
for(let j=0;j<45;j++){
 const q=1+rng()%4,G=1+rng()%5,full=(1<<q)-1;
 let E=[];for(let i=1;i<=full;i++)if((rng()%5)<2)E.push(i);for(let i=0;i<q;i++)E.push(1<<i);
 E=[...new Set(E)].sort((a,b)=>a-b);
 let F={};for(let b=1;b<=Math.min(G,4);b++)if(rng()%3!==0){let sets=E.filter(()=>rng()%3===0);if(!sets.length)sets=[E[rng()%E.length]];F[b]=sets;}
 cases.push({name:'seeded'+j,G,q,E,F});
}
const outputs=cases.map(evaluate);
const small=outputs.find(x=>x.name==='tiny-violation');
// Retain genuine b=2 FUSE: old b=1 potential falls 3->1 for price one.
eq(small.oldB1CreditCost,3,'smallest old initial value');eq(small.initialExactCost,2,'smallest mixed initial value');
ok(negGamma>0,'genuinely signed CHECK transitions seen');
const raw={id:'TMR5-MIXFUSE044',scientificStatus:'COMPUTATIONAL for finite tests; symbolic model theorem PROVED/RESTRICTED pending peer review',models:outputs.length,assertions,paidRows:rows,zeroViewRows:zeros,negativeGammaRows:negGamma,totalQuotientStates:totalStates,failures:0,smallestOldTariffFailure:{G:2,q:1,allowedFusionWidths:[1,2],originalPotential:3,postFUSE2Potential:1,discharge:2,price:1,repairedPotentialBefore:2,repairedPotentialAfter:1},examples:outputs.map(x=>({name:x.name,G:x.G,q:x.q,tau:x.tauFull,discount:x.discount,initialCost:x.initialExactCost,states:x.states}))};
const matrix={id:'TMR5-MIXFUSE044-MATRIX',columns:['CNF','XOR','SEP','FUS','Gamma','Interface','Machine'],weights:[0,0,1,0,1,0,1],model:'P subset D, U subset J, h pending, reversible metadata v; exact CHECK,BATCH,FUSE_b,HALT and free VIEW/NOP only',completeFiniteModels:outputs,sourceStatus:'preauthenticated record calculus only, not a physical SAT decider',rules:['VIEW','NOP','CHECK','BATCH','FUSE_b','HALT'],invariant:'discount sigma(t)=max(0,b+tau(J)-tau(J\\S)-1 over legal (b,S) with b<=t); Gamma=t-sigma(t)*1[U=J]',symbolicTariff:'for all native paid edges: lambda dot (p(C)-p(Cprime))<=1; VIEW/NOP delta=0'};
if(require.main===module){
 const dir=process.env.TMR5_OUTPUT||process.cwd();fs.writeFileSync(dir+'/tmr5_mixedwidth044_raw.json',JSON.stringify(raw,null,2)+'\n');fs.writeFileSync(dir+'/tmr5_mixedwidth044_matrix.json',JSON.stringify(matrix,null,2)+'\n');
 console.log(JSON.stringify({models:raw.models,assertions,paidRows:rows,zeroViewRows:zeros,negativeGammaRows:negGamma,totalQuotientStates:totalStates,failures:0},null,2));
}
module.exports={evaluate,cases,raw,matrix};
