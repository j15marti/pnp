'use strict';
// LSPV-1/455 independent, finite, self-contained checker; NOT historical Rmix341.
const assert=require('node:assert/strict');
const b=(a,i)=>(a>>i)&1;
function ys(k,a){return Array.from({length:k-3},(_,i)=>{
  const p=i+2,s=k-p;
  return p<s?Number((a&((1<<p)-1))===0):Number((a>>p)!==0);
});}
function legal(k,a,v){
  if(!(b(a,0)||b(a,1)||v[0]))return false;
  for(let j=2;j<=k-3;j++)if(!(!v[j-2]||b(a,j)||v[j-1]))return false;
  return !!(!v[k-4]||b(a,k-2)||b(a,k-1));
}
let checks=0,hostile=0;
for(let k=4;k<=14;k++){
  for(let a=0;a<2**k;a++){
    assert.equal(legal(k,a,ys(k,a)),a!==0); checks++;
  }
  for(let j=1;j<=k-3;j++){
    const p=j+1,s=k-p;
    assert.equal(Math.min(p,s),Math.min(j+1,k-j-1)); checks++;
    let a=1<<p,v=ys(k,a);
    assert.equal(v[j-1],1);v[j-1]=0;
    assert.equal(legal(k,a,v),false);checks++;hostile++;
  }
}
console.log(JSON.stringify({artifact:'LSPV1_455_COMPACT',checked:checks,hostile,status:'COMPUTATIONAL only'}));
