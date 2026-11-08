'use strict';
const assert = require('node:assert/strict');
// Finite controls only: this is NOT a time hierarchy or FLMV native proof.
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
let checks=0;
function cnf(mask){const clauses=[];
  for(let v=0;v<4;v++){const ids=[];
    for(let i=0;i<6;i++)if(edges[i].includes(v))ids.push(i);
    assert.equal(ids.length,3);
    for(let p=0;p<8;p++){
      const parity=(p&1)^((p>>1)&1)^((p>>2)&1);
      if(parity===((mask>>v)&1))continue;
      clauses.push(ids.map((i,k)=>(p&(1<<k))?-(i+1):(i+1)));
    }
  }
  return clauses;
}
function models(cs){let n=0;for(let a=0;a<64;a++)
  if(cs.every(c=>c.some(l=>l>0?((a>>(l-1))&1):!((a>>(-l-1))&1))))n++;
  return n;
}
for(let mask=0;mask<16;mask++){
  const f=cnf(mask);assert.equal(f.length,16);
  const odd=[0,1,2,3].reduce((a,i)=>a^((mask>>i)&1),0);
  assert.equal(models(f),odd?0:8);checks++;
}
function gcd(a,b){while(b){const r=a%b;a=b;b=r;}return a;}
function frac(n,d){const g=gcd(n,d);return [n/g,d/g];}
function next([n,d]){
  const a=frac(11,10),b=frac(6*d+5*n,10*d);
  return a[0]*b[1]>=b[0]*a[1]?a:b;
}
let t=[2,1];const seq=[t];
for(let j=0;j<6;j++){t=next(t);seq.push(t);checks++;}
assert.deepEqual(seq[1],[8,5]);
assert.deepEqual(seq[2],[7,5]);
assert.ok(2*seq[2][0]<3*seq[2][1]);checks+=3;
console.log(JSON.stringify({status:'finite-controls-not-hierarchy-proof',checks,
 recurrence:seq.map(x=>x.join('/')),k4_instances:16}));
