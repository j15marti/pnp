#!/usr/bin/env node
'use strict';
// LSPV-3/471; declared unit-paid binary-source calculus, not native bytes.
const assert=require('assert');let families=0,covered=0,steps=0;
function smallest(k,M){let opt=Infinity,best=[];
for(let b=0;b<(1<<M.length);b++){let J=[],mask=0;
for(let j=0;j<M.length;j++)if((b>>j)&1){J.push(j);mask|=M[j]}
if(mask===(1<<k)-1&&J.length<opt){opt=J.length;best=J}}
return Number.isFinite(opt)?best:null}
function verify(k,M,J){const r=M.length,s=j=>2+j,g=i=>2+r+i;
const cs=[[1],...M.map((_,j)=>[-1,s(j)])],loc={};
for(let j=0;j<r;j++)for(let i=0;i<k;i++)if(M[j]&(1<<i)){loc[j+','+i]=cs.length;cs.push([-s(j),g(i)])}
const last=cs.length;cs.push(Array.from({length:k},(_,i)=>-g(i)));
let cur=cs[last].slice(),q=0,used=new Set([last]);
function resolve(src,p,id){assert(src.includes(p)&&cur.includes(-p));cur=[...new Set(cur.filter(x=>x!==-p).concat(src.filter(x=>x!==p)))];assert(cur.every(x=>!cur.includes(-x)));used.add(id);q++}
for(let i=0;i<k;i++){const j=J.find(j=>(M[j]>>i)&1);resolve(cs[loc[j+','+i]],g(i),loc[j+','+i])}
for(const j of J)resolve(cs[1+j],s(j),1+j);
resolve(cs[0],1,0);
assert(cur.length===0&&q===k+J.length+1&&used.size===q+1);steps+=q}
for(let k=1;k<=4;k++)for(let r=1;r<=4;r++){
function go(M){if(M.length<r){for(let x=0;x<(1<<k);x++)go([...M,x]);return}
families++;const J=smallest(k,M);if(J!==null){covered++;verify(k,M,J)}}
go([])}
assert(families===74954&&covered===57164&&steps===381164);
console.log(JSON.stringify({families,covered,uncovered:families-covered,paid_resolution_nodes_checked:steps,model:'unit-paid binary original-source calculus; historical parser unverified',status:'PROVED/RESTRICTED; computational replay; P vs NP OPEN'}));
