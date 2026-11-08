'use strict';
// Independent exact finite witness checker for clause-minimal signed proper-3CNF BPHP.
// Not an R_mix341 checker or a proof of the cited asymptotic Res(XOR) theorem.
const assert = require('assert');
function run(ell) {
  const n = 2 ** ell, A = n * (n * (n + 1) / 2), w = 2 * ell;
  const clauses = [], groups = [];
  let id = (n + 1) * ell;
  for (let p = 0; p <= n; p++) for (let q = p + 1; q <= n; q++)
  for (let h = 0; h < n; h++) {
    const wide = [];
    for (const i of [p, q]) for (let k = 0; k < ell; k++) {
      const x = 1 + i * ell + k;
      wide.push((h >> k) & 1 ? -x : x);
    }
    const z = Array.from({length:w - 3}, () => ++id);
    const split = [[wide[0], wide[1], z[0]]];
    for (let j = 1; j < w - 3; j++) split.push([-z[j-1], wide[j+1], z[j]]);
    split.push([-z[z.length-1], wide[w-2], wide[w-1]]);
    const start = clauses.length;
    clauses.push(...split);
    groups.push({p,q,h,wide,z,start,len:split.length});
  }
  assert.strictEqual(clauses.length, A * (w-2));
  assert.strictEqual(id, (n+1)*ell + A*(w-3));
  const value = (lit,a) => (a[Math.abs(lit)] === (lit>0));
  const holds = (cl,a) => cl.some(lit=>value(lit,a));
  for (const target of groups) for (let gap=0; gap<target.len;gap++) {
    const a = Array(id+1).fill(false);
    const holes = Array(n+1).fill(null);
    holes[target.p]=target.h;holes[target.q]=target.h;
    let other=0;
    for(let i=0;i<=n;i++) if(holes[i]===null) {
      while(other===target.h) other++;
      holes[i]=other++;
    }
    for(let i=0;i<=n;i++) for(let k=0;k<ell;k++)
      a[1+i*ell+k]=Boolean((holes[i]>>k)&1);
    for(const g of groups) {
      if(g===target) g.z.forEach((v,j)=>a[v]=j<gap);
      else g.z.forEach((v,j)=>a[v]=!g.wide.slice(0,j+2).some(lit=>value(lit,a)));
    }
    let count=0, bad=-1;
    clauses.forEach((cl,i)=>{if(!holds(cl,a)){count++;bad=i;}});
    assert.strictEqual(count,1);
    assert.strictEqual(bad,target.start+gap);
  }
  return {ell,holes:n,pigeons:n+1,vars:id,wide_clauses:groups.length,strict3_clauses:clauses.length,verified_deletion_witnesses:clauses.length,binary_unit_work_floor:clauses.length-1};
}
console.log(JSON.stringify({model:'independent full-source witness replay',status:'COMPUTATIONAL',cases:[run(2),run(3)]},null,2));
