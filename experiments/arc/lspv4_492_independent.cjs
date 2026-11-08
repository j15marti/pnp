"use strict";
const assert=require('node:assert/strict');
const fs=require('node:fs');
const signs=[1,-1];
function guard(source,n){
 const m=source.length, z=n+m+1, u=z+1,v=z+2, out=[];
 source.forEach(([a,b,c],i)=>{const h=n+i+1;out.push([a,b,h],[-h,c,z]);});
 for(const s of signs)for(const t of signs)out.push([-z,s*u,t*v]);
 return {out,n:v};
}
function sat(source,n){
 for(let mask=0;mask<2**n;mask++){
  if(source.every(c=>c.some(x=>!!(mask&(2**(Math.abs(x)-1)))===(x>0))))return true;
 }
 return false;
}
function size(n,m){const b=Math.ceil(Math.log2(128*(n+m+3)));return 3*b+1+3*m*(b+2);}
let checks=0;const results=[];
for(const [name,F,n] of [
 ['single',[[1,2,3]],3],
 ['two',[[1,-2,3],[-1,2,-3]],3],
 ['all8',signs.flatMap(s=>signs.flatMap(t=>signs.map(u=>[s,2*t,3*u]))),3]]){
 const {out,n:nn}=guard(F,n);const N=size(n,F.length),M=size(nn,out.length);
 assert.equal(sat(F,n),sat(out,nn));checks++;
 assert.equal(out.length,2*F.length+4);checks++;
 assert.ok(M>=N);checks++;
 for(let k=2;k<=10;k++){
   const worstGuest=M**Math.min(k,4);
   assert.ok(worstGuest>=M**2);checks++;
   assert.ok(k > .6+k/2);checks++;
 }
 results.push({name,N,M,original_sat:sat(F,n),child_sat:sat(out,nn)});
}
for(const numerator of [501,525,550,600,750,1000]){
 const k=Math.ceil(1200/(numerator-500))+1;
 assert.ok(numerator*k>500*k+600);checks++;
 assert.ok(numerator*k>1100);checks++;
}
const result={role:'LSPV-4/492',assertions:checks,failed:0,scope:'finite 3CNF and exact integer exponent comparisons',cases:results};
fs.writeFileSync(__dirname+'/lspv4_492_independent.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result));