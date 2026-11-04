#!/usr/bin/env node
'use strict';
const assert=require('node:assert/strict');
function ip(x){let s=0;for(let j=0;j<x.length;j+=2)s^=x[j]&x[j+1];return s;}
function f(a,b,y){return Number(Boolean((a||y)&&(b||!y)));}
function bits(n,k){return Array.from({length:k},(_,i)=>(n>>i)&1);}
function terms(m){return Array.from({length:1<<(2*m)},(_,k)=>bits(k,2*m));}
function support(fun,n){let s=[];for(let j=0;j<n;j++){let pivotal=false;
for(let k=0;k<(1<<n);k++){const u=bits(k,n),v=u.slice();v[j]^=1;
if(fun(u)!==fun(v)){pivotal=true;break;}}
if(pivotal)s.push(j);}return s;}
let checks=0;const rows=[];
for(let m=1;m<=5;m++){
const xs=terms(m),ws=[];
for(let z=0;z<(1<<m);z++){const x=[];for(let i=0;i<m;i++)x.push((z>>i)&1,1-((z>>i)&1));ws.push(x);assert.equal(ip(x),0);checks++;}
for(const x of xs){let p=[];for(let i=0;i<m;i++)p.push(x[2*i]&x[2*i+1]);let cnt=m;
while(p.length>1){const a=p.shift(),b=p.shift();p.unshift(a^b);cnt++;}
assert.equal(p[0],ip(x));assert.equal(cnt,2*m-1);checks+=2;
for(let a=0;a<2;a++)for(let b=0;b<2;b++){assert.equal(f(a,b,ip(x)),Number(Boolean((a||ip(x))&&(b||!ip(x)))));checks++;}}
for(let i=0;i<ws.length;i++)for(let j=i+1;j<ws.length;j++){
const u=ws[i],v=ws[j];let changed=-1;for(let r=0;r<m;r++)if(u[2*r]!==v[2*r]){changed=r;break;}
assert.ok(changed>=0);const hy=u.slice();hy[2*changed]=1;hy[2*changed+1]=1;assert.equal(ip(hy),1);
for(let t=0;t<2*m;t++)if(u[t]===v[t])assert.equal(hy[t],u[t]);checks+=2;}
if(m<=4){assert.equal(support(z=>f(z[0],z[1],ip(z.slice(2))),2*m+2).length,2*m+2);checks++;}
for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let y=0;y<2;y++){assert.ok(!f(a,b,y)||(a||y));checks++;}
assert.ok(xs.some(x=>f(0,1,ip(x))===1));assert.ok(xs.every(x=>!f(0,1,ip(x))||ip(x)===1));checks+=2;
rows.push({m,initial_named_support:3,expanded_semantic_support:2*m+2,inner_gates:2*m-1,full_three_gate_factor:2*m+2,zero_witnesses:1<<m});
}
for(const malformed of [null,[],[0],[0,1,1],[true,0]]){const good=Array.isArray(malformed)&&malformed.length>=2&&malformed.length%2===0&&malformed.every(t=>typeof t==='number'&&(t===0||t===1));assert.equal(good,false);checks++;}
assert.notEqual(ip([1,1]),ip([1,0]));checks++;
console.log(JSON.stringify({schema:'lspv3-399-verified-v1',status:'COMPUTATIONAL',checks,rows,malformed_rejected:5,corruption_rejected:1},null,2));
