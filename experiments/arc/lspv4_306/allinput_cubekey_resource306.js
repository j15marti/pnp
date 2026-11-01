// LSPV-4 ALLINPUT-CUBEKEY-RESOURCE306, standard Node.js no dependencies.
'use strict';
const POS=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9]];
const NEG=[[4,6,8],[1,6,7],[2,3,4],[3,5,8],[1,2,9],[5,7,9]];
function G(t){let c=[];for(let i=0;i<t;i++){for(let j=0;j<6;j++){let v=POS[j].map(x=>9*i+x);if(j===0)v[1]=9*((i+1)%t)+5;c.push({s:1,v});}for(const a of NEG)c.push({s:-1,v:a.map(x=>9*i+x)});}return {n:9*t,c};}
function valid(F){const p=Array(F.n+1).fill(0),q=p.slice(),seen=new Set();if(F.c.length*3!==4*F.n)return false;for(const z of F.c){const v=z.v;if(new Set(v).size!==3||![-1,1].includes(z.s)||v.some(x=>x<1||x>F.n))return false;const id=z.s+':'+v.slice().sort((a,b)=>a-b).join(',');if(seen.has(id))return false;seen.add(id);for(const x of v)(z.s===1?p:q)[x]++;}return p.slice(1).every(x=>x===2)&&q.slice(1).every(x=>x===2);}
function connected(F){const g=Array.from({length:F.n+1},()=>[]);for(const z of F.c)for(const [i,j] of [[0,1],[1,2],[2,0]]){g[z.v[i]].push(z.v[j]);g[z.v[j]].push(z.v[i]);}const q=[1],set=new Set(q);for(let i=0;i<q.length;i++)for(const x of g[q[i]])if(!set.has(x)){set.add(x);q.push(x)}return set.size===F.n;}
function noFalse(F,p){return F.c.every(z=>z.v.some(x=>p[x]===-1||p[x]===(z.s===1?1:0)));}
function models(F,p){const free=[];for(let x=1;x<=F.n;x++)if(p[x]===-1)free.push(x);if(free.length>18)throw Error('small-control only');let n=0;const a=p.slice();for(let m=0;m<2**free.length;m++){for(let j=0;j<free.length;j++)a[free[j]]=(m>>j)&1;if(F.c.every(z=>z.v.some(x=>a[x]===(z.s===1?1:0))))n++;}return n;}
function P(t,label){const a=[1,0,1,0,-1,-1,-1,0,-1],b=[1,1,0,0,-1,-1,-1,0,-1],p=Array(9*t+1).fill(-1);for(let i=0;i<t;i++)for(let j=1;j<=9;j++)p[9*i+j]=(label==='Q'&&i===0?b:a)[j-1];return p;}
const E=[2,3,4,6,7,8,9],opts=[];for(let i=0;i<7;i++)for(let j=i+1;j<7;j++)for(let x=0;x<2;x++)for(let y=0;y<2;y++)opts.push([[E[i],x],[E[j],y]]);
if(opts.length!==84)throw Error('84');
let checked=0;for(let t of [1,2]){const F=G(t);if(!valid(F)||!connected(F))throw Error('invalid');if(t===1)for(const a of opts){const p=Array(10).fill(-1);for(const [x,v] of a)p[x]=v;if(!noFalse(F,p))throw Error('F9 unsafe');checked++;}else for(const a of opts)for(const b of opts){const p=Array(19).fill(-1);for(const [x,v] of a)p[x]=v;for(const [x,v] of b)p[9+x]=v;if(!noFalse(F,p))throw Error('G2 unsafe');checked++;}}
if(checked!==7140||models(G(1),Array(10).fill(-1))!==70||models(G(2),Array(19).fill(-1))!==4614)throw Error('source models');
const paired=[];for(let t of [1,2,3]){const F=G(t);if(!valid(F)||!connected(F))throw Error('grammar');const s=models(F,P(t,'P')),u=models(F,P(t,'Q'));if(s!==1||u!==0)throw Error('paired');paired.push({t,SAT_extensions:s,UNSAT_extensions:u});}
const rows=[1,2,3,4,8,16,32,64,128].map(t=>{const F=G(t);if(!valid(F)||!connected(F))throw Error('family');const B=Math.ceil(Math.log2(9*t+1)),H=Math.ceil(Math.log2(12*t+1));return {t,N:B+3*H+2+36*t*(B+1),key_floor:(84n**BigInt(t)-1n).toString(2).length}});
console.log(JSON.stringify({tag:'ALLINPUT-CUBEKEY-RESOURCE306',status:'conditional syntactic memo interface only, P versus NP OPEN',checked_safe_cubes:checked,paired,rows},null,2));
