'use strict';
// LSPV-4/389 independent no-import, explicit local-gate trace verifier.
// Host memory is not a measurement of TM writable space.
const assert=require('assert');let checks=0;
function ok(b){checks++;assert(b)}
function gate(op,a,b=0){if(op==='NOT')return a^1;if(op==='AND')return a&b;
 if(op==='OR')return a|b;if(op==='XOR')return a^b;throw Error('bad op')}
function circuit(k,g){const a=Array.from({length:k},(_,i)=>['IN',i]);
 a.push(['CONST',0],['CONST',1]);
 for(let i=a.length;i<g+k+2;i++){let op=['AND','OR','XOR','NOT'][(3*i+k)%4],
  x=(i*7+1)%i,y=(i*3+2)%i;a.push(op==='NOT'?[op,x]:[op,x,y])}
 return a}
function produce(g,k){let t=g.map(()=>Array(2**k).fill(0));
 for(let b=0;b<2**k;b++)for(let i=0;i<g.length;i++){
  const v=g[i],op=v[0];t[i][b]=op==='IN'?(b>>v[1])&1:op==='CONST'?v[1]:
    gate(op,t[v[1]][b],v.length===3?t[v[2]][b]:0)}return t}
function verify(g,t,k){if(!Number.isInteger(k)||k<0||k>3||g.length!==t.length)return false;
 for(let i=0;i<g.length;i++){let v=g[i],op=v[0];
  if(!Array.isArray(v)||!Array.isArray(t[i])||t[i].length!==2**k)return false;
  if(op==='IN'&&!(v.length===2&&Number.isInteger(v[1])&&v[1]>=0&&v[1]<k))return false;
  if(op==='CONST'&&!(v.length===2&&(v[1]===0||v[1]===1)))return false;
  if(!['IN','CONST','AND','OR','XOR','NOT'].includes(op))return false;
  if(!['IN','CONST'].includes(op)&&!(v.length===(op==='NOT'?2:3)&&v.slice(1).every(j=>Number.isInteger(j)&&j>=0&&j<i)))return false;
  for(let a=0;a<2**k;a++){let want=op==='IN'?a>>v[1]&1:op==='CONST'?v[1]:
    gate(op,t[v[1]][a],v.length===3?t[v[2]][a]:0);
   if(t[i][a]!==want)return false}}
 return true}
let valid=0,bad=0,malformed=0,implications=0;
for(let k=0;k<4;k++)for(let n=1;n<=40;n++){
 const g=circuit(k,n),t=produce(g,k);ok(verify(g,t,k));valid++;
 let corrupt=t.map(v=>v.slice());corrupt[n%corrupt.length][0]^=1;
 ok(!verify(g,corrupt,k));bad++;
 ok(!verify(g.concat([['AND',999,0]]),t.concat([[0]]),k));malformed++;
 if(k){let implied=Array.from({length:2**k},(_,a)=>!(a&1)||t.at(-1)[a]===1);
   ok(implied.every(Boolean)===implied.reduce((x,y)=>x&&y,true));implications++}}
function k4(c){let e=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)e.push([i,j]);
 let models=0;for(let a=0;a<64;a++){let sat=true;for(let v=0;v<4;v++){
  let parity=0;for(let z=0;z<6;z++)if(e[z].includes(v))parity^=a>>z&1;
  if(parity!==c[v])sat=false}if(sat)models++}return models}
ok(k4([1,0,0,0])===0);ok(k4([0,0,0,0])===8);
console.log(JSON.stringify({valid,bad,malformed,implications,k4_odd:0,k4_even:8,checks}));
