#!/usr/bin/env node
const assert=require('assert/strict');
function check(name,h,E){
const inc=Array.from({length:h},(_,v)=>E.map((p,i)=>p.includes(v)?i+1:0).filter(Boolean));
for(const odd of [0,1]){
let C=[],acc=Array(E.length+1).fill(0);
for(let v=0;v<h;v++){
const R=inc[v],rhs=odd&&v===0?1:0;
assert.equal(R.length,3);
for(let z=0;z<8;z++){
const b=[z&1,z>>1&1,z>>2&1];
if((b[0]^b[1]^b[2])!==rhs)C.push(R.map((u,j)=>b[j]?-u:u));
}
for(const u of R)acc[u-1]^=1;acc.at(-1);
acc[E.length]^=rhs;
}
let models=0;
for(let a=0;a<2**E.length;a++)if(C.every(c=>c.some(x=>Boolean(a>> (Math.abs(x)-1)&1)===(x>0))))models++;
assert.equal(models,odd?0:2**(E.length-h+1));
assert.ok(acc.slice(0,-1).every(x=>x===0));
assert.equal(acc.at(-1),odd);
console.log(name,odd?'UNSAT':'SAT',models,'paid_nodes',4*h-1);
}}
const K=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)K.push([i,j]);
const P=[[0,1],[1,2],[2,0],[3,4],[4,5],[5,3],[0,3],[1,4],[2,5]];
const C=[];for(let i=0;i<8;i++)for(let j=i+1;j<8;j++)if(((i^j)&((i^j)-1))===0)C.push([i,j]);
check('K4',4,K);check('prism3',6,P);check('cube',8,C);
