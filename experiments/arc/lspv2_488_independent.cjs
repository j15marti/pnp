'use strict';
// Independent explicit existential SAT enumerator for the original 16-clause port gadget.
// No machine-space or R_mix341 certificate claims.
const assert = require('node:assert/strict');
const cases = [[],[1],[1,-1],[1,1,1],[1,2],[1,2,3],[-1,-2,-3],[1,1,-1]];
function b(x,assignment){return (x>0?1:0) === (assignment[Math.abs(x)] ?? 0)}
function holds(C,a){return C.every(c=>c.some(v=>b(v,a)))}
function sourceClause(c,a){return c.some(v=>b(v,a))}
function vec(p){return [[p[0],p[1],p[2]]]}
function normalized(c){
  let p=[5,9,13],D=[];
  if(c.some(v=>c.includes(-v))){D=Array(8).fill([...p]);}
  else {
    let u=[...new Set(c.map(v=>Math.sign(v)*Math.abs(v)*4))];
    if(u.length===3) D=[u, ...Array(7).fill([...p])];
    else if(u.length===2) D=[[u[0],u[1],p[0]],[u[0],u[1],-p[0]],...Array(6).fill([...p])];
    else if(u.length===1){for(let s of [1,-1])for(let t of [1,-1])D.push([u[0],s*p[0],t*p[1]]);D.push(...Array(4).fill([...p]));}
    else {for(let s of [1,-1])for(let t of [1,-1])for(let v of [1,-1])D.push([s*p[0],t*p[1],v*p[2]])}
  }
  assert.equal(D.length,8);
  let R=[];
  for(let j=0;j<8;j++){
    let a=4*(j+1)+2,d=D[j];R.push([d[0],d[1],a],[-a,d[2],3]);
  }
  assert.equal(R.length,16);
  assert(R.every(r=>new Set(r.map(v=>Math.abs(v))).size===3));
  return R;
}
let counts={existential_checked:0,candidate_assignments:0,positive_cases:0,negative_cases:0,source_cases:cases.length,distinct_pins_verified:0};
for(let clause of cases){
  const C=normalized(clause);
  for(let mask=0;mask<8;mask++){
    let old={1:mask&1,2:(mask>>1)&1,3:(mask>>2)&1};
    let original=sourceClause(clause,old);
    for(let z=0;z<=1;z++){
      let expected=Boolean(z||original),found=false;
      for(let m=0;m<2048;m++){
        let a={3:z,4:old[1],8:old[2],12:old[3],5:m&1,9:(m>>1)&1,13:(m>>2)&1};
        for(let j=0;j<8;j++)a[4*(j+1)+2]=(m>>(j+3))&1;
        counts.candidate_assignments++;
        if(holds(C,a)){found=true;break}
      }
      assert.equal(found,expected,`clause ${clause} x ${mask} z ${z}`);
      counts.existential_checked++;
      if(expected)counts.positive_cases++; else counts.negative_cases++;
    }
  }
}
for(let k=1;k<=8;k++){
  let pins=[...Array(k)].map((_,j)=>3*Math.pow(4,k-1-j));
  assert.equal(new Set(pins).size,k);
  assert.equal(pins[k-1],3);
  counts.distinct_pins_verified++;
}
console.log(JSON.stringify({status:'PASS',kind:'independent exhaustive existential guard control',counts,notes:['Full 2^11 local private-variable enumeration; each of eight source-clause types and eight original 3-bit assignments, both port values.','Independent test does not materialize k=3 sources and does not establish their unsatisfiability by brute-force.', 'No FLMV native machine, no R_mix341 proof acceptance.']},null,2));
