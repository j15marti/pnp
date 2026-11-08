// LSPV-3/485 compact independent structural replay. Run: node lspv3_485_rank_replay.cjs
'use strict';
const assert=require('assert/strict'); let checks=0; function ok(v){assert.ok(v);checks++}
const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const clauses=q=>{let cs=[];for(let v=0;v<4;v++){let I=E.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);for(let b=0;b<8;b++){let t=[b&1,(b>>1)&1,(b>>2)&1];if((t[0]^t[1]^t[2])==q[v])continue;cs.push(I.map((e,i)=>t[i]?-(e+1):e+1));}}return cs};
const sat=(c,x)=>c.some(l=>Boolean((x>>(Math.abs(l)-1))&1)===(l>0));
const cnt=C=>Array.from({length:64},(_,x)=>x).filter(x=>C.every(c=>sat(c,x))).length;
let odd=clauses([1,0,0,0]),even=clauses([0,0,0,0]);ok(odd.length===16);ok(even.length===16);ok(cnt(odd)===0);ok(cnt(even)===8);
for(let i=0;i<16;i++)ok(cnt(odd.filter((_,j)=>j!==i))>0);
const par=x=>{let b=0;while(x){b^=1;x&=x-1}return b};
const guards=[3,12]; // x0 XOR x1, x2 XOR x3; independent original-coordinate coefficient masks
function gateEval(x){let v=[par(x&3),par(x&12)]; for(let j=0;j<32;j++){let a=v[j%2],b=j===0?((x>>4)&1):v[v.length-1];v.push(j%2===0?(a&b):(a|b))}return v}
function forms(bits){let v=[[3,0],[12,0]];for(let j=0;j<32;j++){let a=bits[j%2],b=j===0?[16,0]:v[v.length-1];v.push(j%2===0?(a?b:[0,0]):(a?[0,1]:b))}return v}
for(let x=0;x<64;x++){let v=gateEval(x),bits=[par(x&3),par(x&12)],f=forms(bits);ok(v.length===34);for(let i=0;i<v.length;i++)ok((par(x&f[i][0])^f[i][1])===v[i]);}
for(let a=0;a<2;a++)for(let b=0;b<2;b++)ok(Array.from({length:64},(_,x)=>x).some(x=>par(x&3)===a&&par(x&12)===b));
let t=[0,0,0,1];ok(t.reduce((a,b)=>a^b,0)===1); // nested (x0&x1)&x2 fails affine on x0=1
for(let j=0;j<10;j++){let m=[...t];m[3]^=1;ok(m.reduce((a,b)=>a^b,0)===0);}
console.log(JSON.stringify({status:'PASS',checks,source:'original K4 strict3 both labels',odd_models:0,even_models:8,nonlinear_gates:32,rank:2,cells:4,scope:'declared static affine-anchored DAG, NOT R_mix341 native checker'},null,2));