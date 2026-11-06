// LSPV-4/451 restricted promise checker, deterministic, dependency-free.
// Run: node experiments/arc/lspv4_451_promise_checksum_public.mjs
// Decoded IDs are assumed authenticated by a trusted indexed graph header.
import assert from 'node:assert/strict';
const stats={valid:0,replacements:0,multi_collisions:0,prefix_clique_edges:0};
const checksum=(items,m)=>items.length===m && items.every(x=>Number.isInteger(x)&&x>=1&&x<=m) &&
  items.reduce((s,x)=>(s+x)%m,0)===(m*(m+1)/2)%m;
for (const m of [4,8,16,32,40]) {
  const expected=Array.from({length:m},(_,i)=>i+1);
  assert(checksum(expected,m));stats.valid++;
  const reversed=[...expected].reverse();
  assert(checksum(reversed,m));stats.valid++;
  for(let a=1;a<=m;a++)for(let b=1;b<=m;b++)if(a!==b){
    const corrupt=expected.map(x=>x===a?b:x);
    assert(!checksum(corrupt,m));stats.replacements++;
  }
  const k=m/2, core=Array.from({length:k-1},(_,i)=>i+1);
  for(let a=k;a<=m;a++)for(let b=a+1;b<=m;b++){
    const one=[...core,a],two=[...core,b];
    assert(one.reduce((s,x)=>s+x,0)%m!==two.reduce((s,x)=>s+x,0)%m);
    stats.prefix_clique_edges++;
  }
  const collision=[...expected];collision[1]=1;collision[2]=4;
  assert(checksum(collision,m));assert(new Set(collision).size<m);
  stats.multi_collisions++;
}
const left=[1,4,6,7],right=[2,3,5,8];
assert(left.reduce((s,x)=>s+x,0)===right.reduce((s,x)=>s+x,0));
assert(left.reduce((s,x)=>s+x*x,0)===right.reduce((s,x)=>s+x*x,0));
assert(!checksum([1,2,3],4));assert(!checksum([1,2,3,4,4],4));
console.log(JSON.stringify({pass:true,stats,model:'decoded-ID exact-one-replacement promise only'}));
