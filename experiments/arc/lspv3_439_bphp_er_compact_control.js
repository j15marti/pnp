#!/usr/bin/env node
'use strict';
// LSPV-3/439 compact arithmetic/semantic crosscheck, NOT historical /341 parser.
// Complete source-authenticated proof DAGs and independent certificate replay
// are in the separate archived Python+JavaScript reproduction package.
const assert=require('node:assert/strict');
const res=[];
for (const ell of [2,3]) {
  const n=2**ell,m=n+1,src=n*m*(m-1)/2;
  const D=m*(2*n-4);
  let imp=0;for(let d=3;d<=ell;d++)imp+=(2**d)*(d-1);
  const R=m*(2*n-5+imp)+2*ell*src;
  let checked=0;
  for(let i=0;i<m;i++)for(let j=i+1;j<m;j++)
    for(let a=0;a<n;a++)
      for(let u=0;u<n;u++)for(let v=0;v<n;v++){
        const bit=(x,t)=>(x>>(ell-1-t))&1;
        let source=false;
        for(let t=0;t<ell;t++){
          source ||= bit(u,t)!==bit(a,t);
          source ||= bit(v,t)!==bit(a,t);
        }
        const collision=(u!==a)||(v!==a);
        assert.equal(source,collision);checked++;
      }
  // For every prefix, the two child AND-gate defining implications produce
  // the bridge: NOT(parent) OR child0 OR child1.
  for(let i=0;i<m;i++)for(let depth=1;depth<ell;depth++)
    for(let p=0;p<2**depth;p++)for(let a=0;a<n;a++){
      const first=a>>(ell-depth);
      const parent=first===p;
      const child=(a>>(ell-depth-1))===2*p||(a>>(ell-depth-1))===2*p+1;
      assert.equal(!parent||child,true);checked++;
    }
  res.push({ell,n_holes:n,m_pigeons:m,source_clauses:src,
    paid_def:D,paid_resolution:R,total_paid:D+R,semantic_checks:checked});
}
assert.equal(res[0].total_paid,195);assert.equal(res[1].total_paid,2079);
console.log(JSON.stringify({results:res,
  status:'CONDITIONAL FACET-A local semantic and arithmetic control; NOT full proof DAG replay'},null,2));
