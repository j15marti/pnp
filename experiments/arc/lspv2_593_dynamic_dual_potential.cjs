#!/usr/bin/env node
'use strict';
/* LSPV-2/593, standalone restricted cover-domain reference replayer.
   No claim to implement historical R_mix341. For original /386 controls:
   node lspv2_593_dynamic_dual_potential.cjs --native DIRECTORY
   DIRECTORY contains native_checker_pinned.js, native_W29.json,
   native_W32.json and native_W32_repeat128_raw.json. */
const assert=require('assert');
const fs=require('fs'),path=require('path'),cp=require('child_process'),crypto=require('crypto');
let checks=0;function ok(a,msg){checks++;assert(a,msg)}
let seed=0x593c0de;function rnd(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed}
function pop(n){let k=0;while(n){n&=n-1;k++}return k}
function covers(paid,instance,u){return instance.owners.some((i,j)=>((paid>>j)&1)&&i.cover.includes(u))}
function marginal(instance,from,to){return instance.owners.reduce((v,o,i)=>v+(((to>>i)&1)&&!((from>>i)&1)?o.cost:0),0)}
function paidCost(instance,S){return instance.owners.reduce((v,o,i)=>v+((S>>i)&1?o.cost:0),0)}
function dual(instance){return Array.from({length:instance.n},(_,u)=>{
 const containing=instance.owners.filter(i=>i.cover.includes(u));
 ok(containing.length>0,'uncoverable obligation');
 return Math.min(...containing.map(i=>i.cost/i.cover.length));
})}
function potential(instance,S,y){return y.reduce((s,a,u)=>s+(covers(S,instance,u)?0:a),0)}
function run(instance){const y=dual(instance),n=instance.owners.length,full=(1<<n)-1;
 for(let i=0;i<n;i++){
   const o=instance.owners[i],lhs=o.cover.reduce((s,u)=>s+y[u],0);
   ok(lhs<=o.cost+1e-9,'dual violates owner constraint');
 }
 let completions=0,transitions=0,nonzero=0;
 for(let S=0;S<=full;S++){
   let best=Infinity;
   for(let T=0;T<=full;T++)if((T&S)===S){
      if(Array.from({length:instance.n},(_,u)=>u).every(u=>covers(T,instance,u)))
        best=Math.min(best,marginal(instance,S,T));
   }
   ok(Number.isFinite(best),'no concrete cover');
   ok(potential(instance,S,y)<=best+1e-9,'unsafe heuristic at paid prefix');
   completions++;
   let remainder=full^S,move=remainder;
   while(true){let T=S|move,dW=marginal(instance,S,T);
     ok(potential(instance,S,y)<=dW+potential(instance,T,y)+1e-9,
       'inconsistent transition potential');
     transitions++;if(dW>0)nonzero++;
     if(move===0)break;move=(move-1)&remainder;
   }
 }
 return {owners:n,obligations:instance.n,initialPotential:potential(instance,0,y),
         initialExactMinimum:(()=>{let b=Infinity;for(let T=0;T<=full;T++)
         if(Array.from({length:instance.n},(_,u)=>u).every(u=>covers(T,instance,u)))
           b=Math.min(b,paidCost(instance,T));return b})(),
         checkedPrefixes:completions,checkedTransitions:transitions,positiveCostTransitions:nonzero};
}
let cases=[];
// Two-owner-per-obligation common sharing. Many private owners compete with one globally paid owner.
for(let m=2;m<=6;m++){
 const owners=[{name:'shared',cost:1,cover:Array.from({length:m},(_,i)=>i)}];
 for(let i=0;i<m;i++)owners.push({name:'private'+i,cost:1,cover:[i]});
 const result=run({n:m,owners});ok(result.initialExactMinimum===1,'shared owner missed');cases.push({label:'shared-'+m,...result});
}
// A triangle has a fractional potential 3/2 but its cheapest integer cover costs 2.
{
 const result=run({n:3,owners:[{cost:1,cover:[0,1]},{cost:1,cover:[0,2]},{cost:1,cover:[1,2]}]});
 ok(Math.abs(result.initialPotential-1.5)<1e-9&&result.initialExactMinimum===2,
  'triangle fractional relaxation lost');cases.push({label:'triangle',...result});
}
for(let t=0;t<120;t++){
 const m=2+rnd()%5,n=2+rnd()%6,owners=[];
 for(let i=0;i<n;i++){
   let mask=1+(rnd()%((1<<m)-1));
   owners.push({cost:1+rnd()%5,cover:Array.from({length:m},(_,u)=>u).filter(u=>(mask>>u)&1)});
 }
 for(let u=0;u<m;u++)if(!owners.some(o=>o.cover.includes(u)))owners.push({cost:1+rnd()%5,cover:[u]});
 const result=run({n:m,owners});cases.push({label:'seed-'+t,...result});
}
// False positive from treating an unrecognized zero-price mixed rule as excluded.
const toy={n:2,owners:[{name:'RES',cost:1,cover:[0]},{name:'DEF',cost:1,cover:[1]}]};
const y=dual(toy),prior=potential(toy,0,y);
const unknown={n:2,owners:[...toy.owners,{name:'UNAUTHENTICATED_SHORTCUT',cost:0,cover:[0,1]}]};
const falseStep=prior-marginal(unknown,0,4)-potential(unknown,4,y);
ok(falseStep>0,'missing-shortcut unsoundness not detected');
const repaired=dual(unknown);ok(repaired.every(v=>v===0),'unknown zero-cost shortcut should collapse dual');
const zeroRule=run(unknown);cases.push({label:'unknown-zero-cost-shortcut',
   preRepairPotential:prior,spuriousPotentialDrop:falseStep,
   postRepairPotential:zeroRule.initialPotential});
let native=[];const ni=process.argv.indexOf('--native');
if(ni!==-1){assert(process.argv[ni+1],'--native requires directory');const dir=process.argv[ni+1];
 const checker=path.join(dir,'native_checker_pinned.js');
 const expected='22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113';
 const sha=crypto.createHash('sha256').update(fs.readFileSync(checker)).digest('hex');
 ok(sha===expected,'original archived /386 checker changed');
 for(const [label,file] of [['W29','native_W29.json'],['W32','native_W32.json'],
                             ['W32-plus-128-free-facets','native_W32_repeat128_raw.json']]){
   const p=path.join(dir,file),packet=JSON.parse(fs.readFileSync(p));
   let result=cp.spawnSync(process.execPath,[checker,p],{encoding:'utf8',timeout:30000});
   ok(result.status===0,'original /386 rejected '+label+': '+result.stderr);
   ok(packet.gate_defs.length===1,'wrong number of globally paid owners');
   const paid=packet.records.filter(r=>r.kind==='RES').length+packet.gate_defs.length;
   ok(packet.summary.paid_total===paid,'paid ledger mismatch');
   native.push({label,accepted:true,paid,sourceRecords:packet.records.filter(r=>r.kind==='SOURCE').length,
         freeFacetRecords:packet.records.filter(r=>r.kind==='DEF').length,
         bytes:fs.statSync(p).size});
   const bad=structuredClone(packet);bad.records[bad.records.length-1].pivot=999999;
   const hostile=path.join(dir,'_593_hostile_'+label+'.json');fs.writeFileSync(hostile,JSON.stringify(bad));
   try{let res=cp.spawnSync(process.execPath,[checker,hostile],{encoding:'utf8',timeout:30000});
       ok(res.status!==0,'original /386 accepted invalid pivot '+label);
       native.push({label:label+'-bad-final-pivot',accepted:false,exit:res.status});
   }finally{fs.unlinkSync(hostile)}
 }
}
const result={status:'PASS',model:'SEPARATE_CERTIFIED_OBLIGATION_COVER_REFERENCE',
   originalRmix341Authenticated:false,seed:'0x593c0de',cases:cases.length,
   abstractChecks:checks,checkedPrefixes:cases.reduce((s,x)=>s+(x.checkedPrefixes||0),0),
   checkedTransitions:cases.reduce((s,x)=>s+(x.checkedTransitions||0),0),
   zeroCostShortcut:{oldPotential:prior,invalidDrop:falseStep,repairedPotential:zeroRule.initialPotential},
   nativeOriginal386: native,examples:[...cases.slice(0,6),cases.find(c=>c.label==='triangle')]};
console.log(JSON.stringify(result,null,2));
