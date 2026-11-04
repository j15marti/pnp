#!/usr/bin/env node
"use strict";
/* Independent LSPV-2/400 adaptive gate-collapse test, no producer import. */
const fs=require('fs');
const norm=c=>{if(c.some(x=>x===0||c.includes(-x))||new Set(c).size!==c.length)throw Error('malformed clause');return [...c].sort((a,b)=>Math.abs(a)-Math.abs(b)||(a<0)-(b<0));};
function res(a,b,x){if(!a.includes(x)||!b.includes(-x))throw Error('illegal pivot');return norm([...new Set(a.filter(y=>y!==x).concat(b.filter(y=>y!==-x)))]);}
const source=n=>Array.from({length:n},(_,i)=>[i+1]).concat([Array.from({length:n},(_,i)=>-i-1)]).map(norm);
function defs(n){let D=[];for(let j=2;j<=n;j++){let y=n+j-1,a=j===2?1:n+j-2;D.push(norm([-y,a]),norm([-y,j]),norm([y,-a,-j]));}return D;}
function cert(n){let S=source(n),D=defs(n),P=[],lines=S.concat(D);
const add=(a,b,x)=>{let c=res(lines[a],lines[b],x);P.push({a,b,x,c});lines.push(c);return lines.length-1;};
let prev;
for(let j=2;j<=n;j++){let a=j===2?1:n+j-2,third=n+1+3*(j-2)+2;prev=add(add(third,j===2?0:prev,-a),j-1,-j);}
let q=n;for(let j=1;j<n;j++)q=add(j-1,q,j);
let negy=add(n+1+3*(n-2)+1,q,n);add(prev,negy,2*n-1);
return {S,D,P};}
function check(c){let lines=c.S.concat(c.D).map(norm);for(let z of c.P){if(z.a>=lines.length||z.b>=lines.length||z.a<0||z.b<0)throw Error('forward');let q=res(lines[z.a],lines[z.b],z.x);if(JSON.stringify(q)!==JSON.stringify(z.c))throw Error('bad conclusion');lines.push(q);}if(lines.at(-1).length!==0)throw Error('not UNSAT');return true;}
function assignments(n){return Array.from({length:2**n},(_,i)=>Array.from({length:n},(_,j)=>(i>>j)&1));}
function envs(n,partial){let free=Array.from({length:n},(_,j)=>j+1).filter(j=>!Object.hasOwn(partial,j));return assignments(free.length).map(bits=>{let e=Array(n).fill(0);for(let j=0;j<free.length;j++)e[free[j]-1]=bits[j];for(let [j,v]of Object.entries(partial))e[Number(j)-1]=v;let x=e[0];for(let k=2;k<=n;k++){x&=e[k-1];e[n+k-2]=x;}return e;});}
function collapse(n,p){let a=envs(n,p);for(let j=n;j<2*n-1;j++){let v=a.map(e=>e[j]);if(v.every(x=>x===0)||v.every(x=>x===1))continue;let ok=false;for(let x=0;x<n;x++)if(v.every((z,i)=>z===a[i][x])||v.every((z,i)=>z===1-a[i][x]))ok=true;if(!ok)return false;}return true;}
function main(){let checks=0,rows=[];for(let n=2;n<=9;n++){
let C=cert(n);check(C);checks++;if(C.P.length!==3*n-1)throw Error('r');checks++;
const sat=(f,v)=>f.every(c=>c.some(l=>l>0?v[l-1]===1:v[-l-1]===0));
if(assignments(n).some(v=>sat(C.S,v)))throw Error('UNSAT model');checks++;
if(!sat(C.S.slice(0,n),Array(n).fill(1)))throw Error('SAT control');checks++;
let leaves=[];for(let k=1;k<n;k++){let p={};for(let j=1;j<k;j++)p[j]=1;p[k]=0;leaves.push(p);}let tail={};for(let j=1;j<n;j++)tail[j]=1;leaves.push(tail);
for(let p of leaves){if(!collapse(n,p))throw Error('leaf');checks++;}
for(let mask=0;mask<2**n;mask++){let B=Array.from({length:n},(_,j)=>j+1).filter(j=>mask&(1<<(j-1)));if(B.length>=n-1)continue;let ok=true;for(let bit=0;bit<2**B.length;bit++){let p={};B.forEach((j,k)=>p[j]=(bit>>k)&1);if(!collapse(n,p)){ok=false;break;}}if(ok)throw Error('small static backdoor');checks++;}
let bad=JSON.parse(JSON.stringify(C));bad.P[0].x=0;try{check(bad);throw Error('accepted bad pivot');}catch(e){if(e.message==='accepted bad pivot')throw e;checks++;}
bad=JSON.parse(JSON.stringify(C));bad.S[0]=[1,-1];try{check(bad);throw Error('accepted malformed');}catch(e){if(e.message==='accepted malformed')throw e;checks++;}
rows.push({n,g:n-1,r:C.P.length,b:n-1,L:leaves.length,old:2**(n-1)*(3*n)-1,revised:n*3*n-1,source_opt:n});
}
console.log(JSON.stringify({checks,rows},null,2));}
main();
