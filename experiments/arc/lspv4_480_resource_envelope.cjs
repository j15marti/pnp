#!/usr/bin/env node
// LSPV-4/480 independent finite audit (not a native FLMV simulator).
"use strict";
const assert=require("assert");
const beta=c=>((c+2)/(c*c)-c)/2;
function bisect(f,target,lo,hi){for(let i=0;i<120;i++){const mid=(lo+hi)/2;if(f(mid)>target)lo=mid;else hi=mid}return(lo+hi)/2}
const c0=bisect(beta,.5,1.2,1.3), ac=c0/2, lc=1-.6/c0;
let checks=0,maxErr=0,seed=480;
const random=()=>{seed=(Math.imul(1664525,seed)+1013904223)>>>0;return seed/2**32;};
for(let j=0;j<3000;j++){
 const a=.15+1.1*random(),l=.15+.6*random(),r=1+.6*random(),e=.1+.85*random();
 let t=1+69*random(),s=.1+39.9*random();
 for(let k=0;k<240;k++){t=Math.max(r,a+l*t);s=Math.max(e,l*s)}
 const err=Math.max(Math.abs(t-Math.max(r,a/(1-l))),Math.abs(s-e));
 assert(err<1e-9);maxErr=Math.max(maxErr,err);checks++;
}
let caseResult=[];
for(let [name,a,l,r,e] of [["nominal",.6,.5,1.1,.5],["call_above",ac+1e-6,.5,1.1,.5],["call_below",ac-1e-6,.5,1.1,.5],["child_above",.6,lc+1e-6,1.1,.5],["child_below",.6,lc-1e-6,1.1,.5],["full_cache",.6,.5,1.1,.6],["equality",.6,.5,1.1,23/45]]){
 const limit=Math.max(r,a/(1-l)),gap=beta(limit)-e;let t=1000,s=1000,first=null;
 for(let j=0;j<=500;j++){if(s<beta(t)-1e-14){first=j;break}t=Math.max(r,a+l*t);s=Math.max(e,l*s)}
 assert.strictEqual(first!==null,gap>1e-12);caseResult.push({name,limit,gap,first});checks++;
}
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const inc=[0,1,2,3].map(v=>edges.map(([u,w],i)=>u===v||w===v?i+1:0).filter(Boolean));
function packet(v,c){let p=[];for(let i=0;i<8;i++){let b=[i&1,i>>1&1,i>>2&1];if((b[0]^b[1]^b[2])!==c)p.push(inc[v].map((x,j)=>b[j]?-x:x))}return p}
const normalize=p=>p.map(x=>x.join(",")).sort().join("|");
function source(cs){return cs.map((c,v)=>packet(v,c))}
function valid(f){return Array.isArray(f)&&f.length===4&&f.every((p,v)=>Array.isArray(p)&&p.length===4&&p.every(c=>Array.isArray(c)&&c.length===3&&c.map(x=>Math.abs(x)).sort((a,b)=>a-b).join(",")===inc[v].slice().sort((a,b)=>a-b).join(","))&&(normalize(p)===normalize(packet(v,0))||normalize(p)===normalize(packet(v,1))))}
function models(f){let count=0;for(let bits=0;bits<64;bits++)if(f.every(p=>p.every(c=>c.some(l=>l>0?Boolean(bits&(1<<(l-1))):!Boolean(bits&(1<<(-l-1)))))))count++;return count}
let sat=0,unsat=0;
for(let n=0;n<16;n++){const cs=[n&1,n>>1&1,n>>2&1,n>>3&1],f=source(cs),want=cs.reduce((a,b)=>a+b,0)%2?0:8;assert(valid(f));assert.strictEqual(models(f),want);want?sat++:unsat++;checks++}
const z=source([0,0,0,0]);
for(let b of [z.slice(0,3),[z[0].slice(0,3),...z.slice(1)],[[[1,1,3],...z[0].slice(1)],...z.slice(1)],[[[1,2,3],[1,2,3],[1,2,3],[1,2,3]],...z.slice(1)]]){assert(!valid(b));checks++}
assert(Math.abs(beta(1.2)-23/45)<1e-13);
console.log(JSON.stringify({status:"FINITE CONTROLS ONLY",c0,ac,lc,random_tests:3000,maxErr,caseResult,K4:{sat,unsat,malformed:4},assertion_groups:checks},null,2));
