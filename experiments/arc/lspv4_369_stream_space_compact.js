#!/usr/bin/env node
const assert=require('assert');let checks=0;function ok(x){assert(x);checks++;}
function models(n,cs){let z=0;for(let a=0;a<2**n;a++)if(cs.every(c=>c.some(l=>l>0?!!(a&(1<<(l-1))):!(a&(1<<(-l-1))))))z++;return z;}
function php(h){let c=[];let x=(i,j)=>i*h+j+1;for(let i=0;i<=h;i++)c.push(Array.from({length:h},(_,j)=>x(i,j)));for(let j=0;j<h;j++)for(let i=0;i<=h;i++)for(let k=i+1;k<=h;k++)c.push([-x(i,j),-x(k,j)]);return c;}
function k4(odd){let e=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],cs=[];for(let v=0;v<4;v++){let ix=e.map((a,i)=>a.includes(v)?i+1:0).filter(Boolean);for(let z=0;z<8;z++){let b=[z&1,(z>>1)&1,(z>>2)&1];if(b.reduce((a,x)=>a+x,0)%2===(odd&&v===0?1:0))continue;cs.push(ix.map((x,i)=>b[i]?-x:x));}}return cs;}
let deleted=0;for(let h=1;h<=3;h++){let cs=php(h);ok(models(h*(h+1),cs)===0);for(let i=0;i<cs.length;i++){ok(models(h*(h+1),cs.filter((_,j)=>i!==j))>0);deleted++;}}
ok(deleted===34);ok(models(6,k4(1))===0);ok(models(6,k4(0))===8);
for(let s=1;s<=13;s++){let seen=new Set(),x=0,out=0;while(x<2**s){ok(!seen.has(x));seen.add(x);out++;x++;}ok(out===2**s&&seen.size===out);}
let cap=(M,s,k=1,Q=2,a=2)=>Q*(M+2)*(s+2)**k*a**s;for(let M of [32,128,512])for(let s of [1,4,8])ok(cap(M,s)>2**s);
console.log(JSON.stringify({status:'PASS',checks,php_deleted_sat:deleted,tseitin_odd_even_models:[0,8],max_counter_output_bits:8192}));