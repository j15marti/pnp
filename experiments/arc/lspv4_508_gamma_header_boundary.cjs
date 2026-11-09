#!/usr/bin/env node
'use strict';
// LSPV-4/508 supplemental resource encoding audit: finite 12-bit header cap
// and exact prefix-free gamma header repair. Hosted checks, not native FLMV.
const assert=require('node:assert/strict');
const gamma=x=>{assert(Number.isSafeInteger(x)&&x>0);const b=x.toString(2);return '0'.repeat(b.length-1)+b};
function readGamma(s,p){let zeros=0;while(s[p+zeros]==='0')zeros++;const width=zeros+1, at=p+zeros;const bits=s.slice(at,at+width);assert.equal(bits.length,width);return [parseInt(bits,2),at+width]}
function encode(H){
 assert(Number.isInteger(H)&&H>0&&H%2===0);
 const m=3*H/2,w=Math.ceil(Math.log2(m+1));
 const header='10100110'+gamma(H)+gamma(m);
 const N=header.length+12*H*(w+1);
 let [h,k]=readGamma(header,8),[e,z]=readGamma(header,k);
 assert.equal(h,H);assert.equal(e,m);assert.equal(z,header.length);
 return {H,m,w,old12bitFits:H<=4095&&m<=4095,oldNominalN:32+12*H*(w+1),newGammaN:N,newHeaderBits:header.length};
}
function main(){
 const rows=[4,6,8,14,2730,2732,4094,4096,16384].map(encode);
 assert.equal(rows[4].old12bitFits,true);
 assert.equal(rows[5].old12bitFits,false);
 assert.equal(rows[4].m,4095);
 assert.equal(rows[5].m,4098);
 for(let i=0;i<rows.length;i++){
  assert.equal(rows[i].newHeaderBits,8+gamma(rows[i].H).length+gamma(rows[i].m).length);
  assert.equal(rows[i].newGammaN,rows[i].newHeaderBits+12*rows[i].H*(rows[i].w+1));
 }
 return {status:'PROVED/RESTRICTED grammar correction plus COMPUTATIONAL controls',passed:true,fix12_max_even_H:2730,source_header:'8-bit 0xA6 + Elias gamma(H) + gamma(m)',rows};
}
if(require.main===module)console.log(JSON.stringify(main(),null,2));
module.exports={main};
