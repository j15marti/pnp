// TMR-2 / SWEEP-TIGHTNESS-002. Node >=18, no dependencies.
// Executing this script prints deterministic, bounded finite evidence.
// Semantic test runner only: asymptotic TM simulation is a symbolic claim in the report.
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
function make(a,b) {
  const n=a.length;
  assert(n>=1 && b.length===n);
  const N=5*n, M=8*n, w=Math.max(1,Math.ceil(Math.log2(N)));
  let src="1".repeat(N)+"0"+"1".repeat(M)+"0";
  for (const [side,bits] of [a,b].entries()) for(let i=0;i<n;i++) {
    const aux=(side===0?1:3)*n+2*i;
    for(const [u,v] of [[0,0],[0,1],[1,0],[1,1]]) {
      for(const [sign,idx] of [[1-bits[i],i],[u,aux],[v,aux+1]]) {
        src+=String(sign)+idx.toString(2).padStart(w,"0");
      }
    }
  }
  return src;
}
function inspect(s) {
  if(typeof s!=="string" || /[^01]/.test(s))return null;
  const z=s.indexOf("0");
  if(z<5 || z%5!==0)return null;
  const n=z/5,N=5*n,M=8*n,w=Math.max(1,Math.ceil(Math.log2(N)));
  const p=z+1;
  if(s.slice(p,p+M)!=="1".repeat(M) || s[p+M]!=="0")return null;
  let j=p+M+1;
  if(s.length!==j+24*n*(1+w))return null;
  const signs=[];
  for(let side=0;side<2;side++) {
    const bits=[];
    for(let i=0;i<n;i++) {
      const aux=(side===0?1:3)*n+2*i;
      let first=null;
      for(const [u,v] of [[0,0],[0,1],[1,0],[1,1]]) {
        const row=[];
        for(let t=0;t<3;t++) {
          row.push([Number(s[j]),parseInt(s.slice(j+1,j+1+w),2)]);
          j+=1+w;
        }
        if(row[0][1]!==i || row[1][1]!==aux || row[2][1]!==aux+1 ||
           row[1][0]!==u || row[2][0]!==v)return null;
        if(first===null)first=row[0][0];
        if(row[0][0]!==first)return null;
      }
      bits.push(1-first);
    }
    signs.push(bits);
  }
  return signs[0].every((bit,i)=>bit===signs[1][i]);
}
function audit() {
  const stats={status:"COMPUTATIONAL finite only",test:"TMR2_SWEEP_TIGHTNESS002",
    cases:0,sat_cases:0,unsat_cases:0,bit_flips_rejected:0,
    valid_four_bit_block_flips:0,malformed_rejected:0,source_lengths:{}};
  for(let n=1;n<=6;n++) {
    stats.source_lengths[n]=make(Array(n).fill(0),Array(n).fill(0)).length;
    for(let x=0;x<2**n;x++) {
      const a=Array.from({length:n},(_,i)=>(x>>i)&1);
      for(let y=0;y<2**n;y++) {
        const b=Array.from({length:n},(_,i)=>(y>>i)&1);
        const r=inspect(make(a,b));
        assert.equal(r,x===y);
        stats.cases++;
        stats[r?"sat_cases":"unsat_cases"]++;
      }
      const src=make(a,a);
      for(let side=0;side<2;side++)for(let i=0;i<n;i++) {
        const changed=a.slice();changed[i]^=1;
        const alt=side===0?make(changed,a):make(a,changed);
        assert.equal(inspect(alt),false);
        const differences=[...src].reduce((acc,v,j)=>(v!==alt[j]&&acc.push(j),acc),[]);
        assert.equal(differences.length,4);
        stats.valid_four_bit_block_flips++;
      }
      const first=5*n+1+8*n+1;
      const bad=src.slice(0,first)+String(1-Number(src[first]))+src.slice(first+1);
      assert.equal(inspect(bad),null);
      stats.bit_flips_rejected++;
    }
    const baseline=make(Array(n).fill(0),Array(n).fill(0));
    for(const bad of ["","0","1","1110",baseline.slice(0,-1),baseline+"1"]) {
      assert.equal(inspect(bad),null);
      stats.malformed_rejected++;
    }
  }
  return stats;
}
if(require.main===module) {
  const result=audit();
  if(process.argv[2]) fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+"\n");
  console.log(JSON.stringify(result,null,2));
}
module.exports={make,inspect,audit};
