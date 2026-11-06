#!/usr/bin/env node
'use strict';
// LSPV-1/454, independently checked local semantic theorem.
// No accepted-byte historical R_mix341 claims. Node.js >=18.
const assert=require('node:assert/strict');
let checks=0;
function ok(x,msg){checks++;assert(x,msg)}
function assignment(n,k){return Array.from({length:k},(_,i)=>Boolean(n&(1<<i)))}
function chain(x,y){const k=x.length;
 if(k<4||y.length!==k-3)throw Error('invalid chain shape');
 if(!(x[0]||x[1]||y[0]))return false;
 for(let i=1;i<k-3;i++)if(!(!y[i-1]||x[i+1]||y[i]))return false;
 return !!(!y[k-4]||x[k-2]||x[k-1]);
}
function affine(m,x){let v=m&1;for(let i=0;i<x.length;i++)if(x[i]&&(m&(2<<i)))v^=1;return !!v}
function allowed(x,y0){for(let m=0;m<(1<<(x.length-4));m++){
 let tail=assignment(m,x.length-4);
 if(chain(x,[!!y0,...tail]))return true;
}return false}
function canonical(x){let y=[],prefix=!(x[0]||x[1]);y.push(prefix);
 for(let i=1;i<x.length-3;i++){prefix=prefix&&!x[i+1];y.push(prefix)}
 return y;
}
let result=[];
for(let k=4;k<=8;k++){
 let valid=0,forced1=0,forced0=0,free=0,models=0;
 for(let s=0;s<(1<<k);s++){
  let x=assignment(s,k),a=allowed(x,false),b=allowed(x,true);
  ok(a||b||s===0,'existential projection');
  ok((a||b)===(s!==0),'projection exact');
  if(s!==0){models++;ok(chain(x,canonical(x)),'nonlinear AND section');
   if(a&&b)free++;else if(b)forced1++;else forced0++;
  }
 }
 for(let m=0;m<(1<<(k+1));m++){
  let no=false;
  for(let s=1;s<(1<<k);s++){
   const x=assignment(s,k);if(!allowed(x,affine(m,x))){no=true;break}
  }
  if(!no)valid++;
 }
 ok(valid===0,'no affine Skolem section');
 ok(forced1===(1<<(k-2))-1&&forced0===3&&free===3*((1<<(k-2))-1),'forcing counts');
 result.push({k,models,affine_candidates:1<<(k+1),valid,forced1,forced0,free});
}
for(let k=4;k<=20;k++){
 let patterns=[4,8,12,1,2,3],expect=[1,1,1,0,0,0];
 let xorMasks=0,xorVals=0;
 for(let i=0;i<6;i++){
  let x=Array.from({length:k},(_,j)=>Boolean(patterns[i]&(1<<j)));
  ok(x.some(Boolean),'original clause model');
  ok(allowed(x,!!expect[i])&&!allowed(x,!expect[i]),'forced affine output');
  xorMasks^=patterns[i];xorVals^=expect[i];
 }
 ok(xorMasks===0&&xorVals===1,'inconsistent six-row constraints');
}
let rejected=0;
for(const [x,y] of [[[true,true],[false]],[[true,true,true],[]],[[true,true,true,true],[]]]){
 try{chain(x,y);throw Error('accepted bad shape')}catch(e){if(e.message==='invalid chain shape')rejected++;else throw e}
}
ok(rejected===3,'hostile controls rejected');
console.log(JSON.stringify({schema:'LSPV1_454_CLAUSE_SPLITTER_AFFINE_NOGO/v1',checks,hostile_rejected:rejected,results:result,scope:'restricted local semantic section, not historical R_mix341',open:'B3 and P versus NP'}));
