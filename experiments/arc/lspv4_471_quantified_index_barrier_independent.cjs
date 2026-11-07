'use strict';
const assert=require('node:assert/strict');
let checks=0;
const out=[];
const floorlog=x=>Math.floor(Math.log2(x));
for(const N of [4,8,16])for(const d of [2,4]){
  const r=2**floorlog(d*floorlog(N));
  const m=2**r,L=r*m;
  assert.equal(2**floorlog(r),r);checks++;
  if(r<=8){
    const words=new Set();
    for(let z=0;z<m;z++)words.add(Array.from({length:r},(_,j)=>String((z>>j)&1)).join(''));
    assert.equal(words.size,m);checks++;
    assert.equal([...words].filter(x=>x.includes('1')).length,m-1);checks++;
  }
  out.push({N,d,r,L,distinct_nonzero_height_log2r:m-1});
}
function models(charges){
  const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]],cs=[];
  for(let v=0;v<4;v++){
    const inc=E.flatMap(([a,b],j)=>(a===v||b===v)?[j]:[]);
    for(let z=0;z<8;z++){
      if(z.toString(2).replaceAll('0','').length%2===charges[v])continue;
      cs.push(inc.map((edge,j)=>((z>>j)&1)?-(edge+1):edge+1));
    }
  }
  assert.equal(cs.length,16);checks++;
  let count=0;
  for(let x=0;x<64;x++)if(cs.every(c=>c.some(l=>((x>>(Math.abs(l)-1))&1)===(l>0?1:0))))count++;
  return count;
}
assert.equal(models([0,0,0,0]),8);checks++;
assert.equal(models([1,0,0,0]),0);checks++;
assert.equal(new Set([1,1,2].map(Math.abs)).size,2);checks++;
console.log(JSON.stringify({cases:out,checks_passed:checks,even_K4:8,odd_K4:0,failures:0},null,2));