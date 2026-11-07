#!/usr/bin/env node
'use strict';
const assert=require('node:assert/strict');
const C=[[1,2,3],[-1,2,4],[-2,3,4]];let checks=0;
function ck(x,m){checks++;assert.ok(x,m)}
function sat(c,b){return c.some(x=>((x>0)===b[Math.abs(x)-1]))}
function res(a,b,p){ck(a.includes(p)&&b.includes(-p),'oriented RES');const s=[...new Set([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)])];ck(!s.some(x=>s.includes(-x)));return s.sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y)}
ck(new Set(C.map(c=>c.map(Math.abs).sort().join(','))).size===3);
for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)ck(new Set([...C[i].map(Math.abs),...C[j].map(Math.abs)]).size===4);
const D=res(C[0],C[1],1);ck(JSON.stringify(D)===JSON.stringify([2,3,4]));
for(let t=0;t<16;t++){const b=[0,1,2,3].map(i=>!!((t>>i)&1));ck((sat(D,b)&&sat(C[2],b))===(b[2]||b[3]))}
let rejected=0;try{res(C[1],C[0],1)}catch(_){rejected++}ck(rejected===1);
console.log(JSON.stringify({pass:true,checks,rejected,source:C,proposed_PORT1_paid_nodes:3,scope:'distinct proposed port, NOT historical R_mix341'}));
