#!/usr/bin/env node
'use strict';
// Different algorithm: enumerate masks in ascending numeric order and assign
// ordinal ranks by popcount. Checks independent combinatorial rank formula.
const fs=require('fs');
function choose(n,k){let out=1;for(let i=1;i<=k;i++)out=out*(n-i+1)/i;return Math.round(out)}
function popcount(x){let c=0;while(x){c+=x&1;x>>>=1}return c}
function rankByCombinadic(mask,H){let rank=0,j=0;for(let p=0;p<H;p++){if(mask&(1<<p)){j++;rank+=choose(p,j)}}return rank}
function tseitin(charges){const edges=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)edges.push([a,b]);let clauses=[];for(let v=0;v<4;v++){let inc=[];edges.forEach((e,i)=>{if(e.includes(v))inc.push(i)});for(let a=0;a<8;a++){const vals=[a&1,(a>>1)&1,(a>>2)&1];if(vals.reduce((x,y)=>x+y,0)%2!==charges[v])clauses.push(vals.map((z,j)=>z?-(inc[j]+1):inc[j]+1))}}return clauses}
let checks=0,count=0;
for(let H=1;H<=13;H++){
  let counters=new Array(H+1).fill(0);
  for(let mask=0;mask<(1<<H);mask++){
    let k=popcount(mask),expected=counters[k]++;
    if(rankByCombinadic(mask,H)!==expected)throw new Error(`ranking H${H} mask${mask}`);
    checks++;count++;
  }
  for(let k=0;k<=H;k++){if(counters[k]!==choose(H,k))throw Error('count');checks++;}
}
for(let charge=0;charge<16;charge++){
  let cc=Array.from({length:4},(_,j)=>(charge>>j)&1),clauses=tseitin(cc);
  if(clauses.length!==16)throw Error('clause count');
  let solutions=0;
  for(let mask=0;mask<64;mask++){
     const valid=clauses.every(cl=>cl.some(l=>!!(mask&(1<<(Math.abs(l)-1)))===(l>0)));
     if(valid)solutions++;
     checks++;
  }
  if(solutions!==(cc.reduce((a,b)=>a+b,0)%2?0:8))throw Error('incorrect SAT parity');
  checks++;
}
console.log(JSON.stringify({method:'independent numeric-order rank enumeration',maxH:13,subsets:count,checks,charges:16,passed:true}));
