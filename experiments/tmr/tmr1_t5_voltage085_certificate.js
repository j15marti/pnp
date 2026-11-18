'use strict';
const assert=require('node:assert/strict');
let tests=0; const mod=x=>((x%5)+5)%5;
function same(x,y){assert.deepEqual(x,y);tests++;}
function ok(x){assert.ok(x);tests++;}
const S=[1,3];
function transfer(w){let a=[1,0,0,0,0];for(const s of w){const b=[0,0,0,0,0];for(let i=0;i<5;i++)for(const t of S)b[mod(i+(s==='+'?t:-t))]+=a[i];a=b;}return a;}
function product(ws){return [0,1,2,3,4].map(d=>ws.map(transfer).reduce((a,p)=>a*p[d],1));}
const forward=['++','+++','++-','+++'];
const reverse=['--','---','+--','---'];
same(transfer('++'),[0,1,1,0,2]);
same(transfer('+++'),[3,0,3,1,1]);
same(transfer('++-'),[1,3,0,3,1]);
same(product(forward),[0,0,0,0,2]);
same(product(reverse),[0,2,0,0,0]);
const F=product(forward), B=product(reverse);
function enumerate(q,flipped){let count=0;for(let t=0;t<5**(2*q);t++){const a=[];let x=t;for(let i=0;i<2*q;i++){a.push(x%5);x=Math.floor(x/5);}let ways=1;for(let i=0;i<q;i++)for(let j=0;j<q;j++){ways*=(flipped&&i===0&&j===0?B:F)[mod(a[q+j]-a[i])];if(ways===0)break;}count+=ways;}return count;}
for(const q of [2,3])for(const flip of [false,true])same(enumerate(q,flip),flip?0:5*2**(q*q));
function potential(q,flip){const N=2*q,adj=Array.from({length:N},()=>[]);for(let i=0;i<q;i++)for(let j=0;j<q;j++){const a=i,b=q+j,d=(flip&&i===0&&j===0)?1:4;adj[a].push([b,d]);adj[b].push([a,mod(-d)]);}const val=Array(N).fill(-1),stack=[0];val[0]=0;let possible=true;while(stack.length){const u=stack.pop();for(const [v,d] of adj[u]){const z=mod(val[u]+d);if(val[v]===-1){val[v]=z;stack.push(v);}else if(val[v]!==z)possible=false;}}return possible;}
for(let q=2;q<=16;q++)for(const flip of [false,true]){ok(potential(q,flip)===!flip);const n=2*q+7*q*q,m=11*q*q;same(m-n+1,4*q*q-2*q+1);}
console.log(JSON.stringify({id:'TMR1_T5_VOLTAGE085_CERTIFICATE',status:'PASS',assertions:tests,failures:0,enumerated_core_cases:[2,3],symbolic_scope:'restricted Kqq image and modular voltage',computational_only:true}));
