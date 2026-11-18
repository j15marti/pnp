'use strict';
// TMR-1/092: exact cyclotomic Fourier-flow verifier, Node.js >=18.
const A=require('assert');let tests=0,graphs=0,states=0;
function ok(v){tests++;A.ok(v)}
const z=x=>((x%5)+5)%5,P=[[1n,0n,0n,0n],[0n,1n,0n,0n],[0n,0n,1n,0n],[0n,0n,0n,1n],[-1n,-1n,-1n,-1n]];
const add=(a,b)=>a.map((x,i)=>x+b[i]);
function mul(a,b){let c=Array(7).fill(0n);for(let i=0;i<4;i++)for(let j=0;j<4;j++)c[i+j]+=a[i]*b[j];for(let d=6;d>=4;d--)for(let j=0;j<4;j++)c[d-4+j]-=c[d];return c.slice(0,4)}
const W=Array.from({length:5},(_,j)=>add(P[j],P[3*j%5]));
function calc(n,E){const m=E.length,adj=Array.from({length:n},()=>[]);E.forEach(([a,b],i)=>{adj[a].push([b,i]);if(a!==b)adj[b].push([a,i]);});let seen=Array(n).fill(false),pa=Array(n).fill(-1),pe=Array(n).fill(-1),used=Array(m).fill(false),ord=[],roots=[];for(let r=0;r<n;r++)if(!seen[r]){roots.push(r);seen[r]=true;let Q=[r];for(let k=0;k<Q.length;k++){let v=Q[k];ord.push(v);for(let [u,i] of adj[v])if(!seen[u]){seen[u]=true;pa[u]=v;pe[u]=i;used[i]=true;Q.push(u)}}}let chords=[];for(let i=0;i<m;i++)if(!used[i])chords.push(i);
let total=[0n,0n,0n,0n],N=5**chords.length;states+=N;ok(Number.isSafeInteger(N));for(let t=0;t<N;t++){let q=t,bal=Array(n).fill(0),f=Array(m).fill(0);for(let e of chords){let k=q%5;q=Math.floor(q/5);f[e]=k;let [a,b]=E[e];bal[a]=z(bal[a]+k);bal[b]=z(bal[b]-k)}for(let j=ord.length-1;j>=0;j--){let v=ord[j],e=pe[v];if(e<0)continue;let p=pa[v],fw=E[e][0]===p,k=z(fw?bal[v]:-bal[v]);f[e]=k;bal[p]=z(bal[p]+(fw?k:-k));bal[v]=0}for(let r of roots)ok(bal[r]===0);let t0=[1n,0n,0n,0n];for(let k of f)t0=mul(t0,W[k]);total=add(total,t0)}let exponent=n-m,factor=5n**BigInt(Math.abs(exponent));if(exponent>=0)total=total.map(a=>a*factor);else{ok(total.every(a=>a%factor===0n));total=total.map(a=>a/factor)}ok(total.slice(1).every(a=>a===0n));return total[0]}
function brute(n,E){let count=0n;for(let t=0;t<5**n;t++){let v=t,x=[];for(let i=0;i<n;i++){x.push(v%5);v=Math.floor(v/5)}if(E.every(([a,b])=>{let d=z(x[b]-x[a]);return d===1||d===3}))count++}return count}
for(let n=0;n<=3;n++){let all=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++)all.push([i,j]);for(let mask=0;mask<2**all.length;mask++){let E=all.filter((_,i)=>mask&2**i);ok(calc(n,E)===brute(n,E));graphs++}}
for(let n=4;n<=5;n++)for(let k=0;k<100;k++){let E=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++)if((i*11+j*37+k*29+((k*i*j+17)%31))%23<4)E.push([i,j]);let rho=E.length-n+1;if(rho>6)continue;ok(calc(n,E)===brute(n,E));graphs++}
console.log(JSON.stringify({graphs,tests,flowStates:states,failures:0}));
