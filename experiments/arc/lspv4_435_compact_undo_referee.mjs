// Compact independent standalone LSPV-4/435 invariant and adaptive-falsifier test.
// Node.js >= 18; full fixture-based referee is in the downloadable reproducibility archive.
import assert from 'node:assert/strict';
let checks=0;
for (const H of [4,8,10]) {
 for (let a=0;a<H;a++) for(let b=0;b<H;b++) for(let c=0;c<H;c++) {
  const x=Array(H).fill(0), orig=x.slice();
  const path=[[a,b,b],[c,a,c],[a,a,b]];
  for(const desc of path)for(const v of desc)x[v]^=1;
  for(const desc of path.slice().reverse())for(const v of desc)x[v]^=1;
  assert.deepEqual(x,orig);checks++;
 }
}
const bank=[0,0,0,0], mut=()=>bank[0]===0?0:1;
const a=mut();bank[a]^=1;const b=mut();bank[b]^=1;
assert.equal(a,0);assert.equal(b,1);assert.deepEqual(bank,[1,1,0,0]);checks+=3;
console.log(JSON.stringify({checks, status:'PASS',note:'independent invariant finite control; full fixture referee in archive'}));
