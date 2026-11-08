'use strict';
// Independently implemented finite controls for LSPV-4/488. Run:
// node experiments/arc/lspv4_488_independent.cjs [output.json]
// PROVED/RESTRICTED communication theorem is in the accompanying report;
// this executable checks original signed 3-CNF semantics, not machine time.
const assert = require('assert');
const fs = require('fs');
function edgesFor(type) {
  let n, e=[];
  if(type==='K4'){n=4;for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)e.push([i,j]);}
  if(type==='K33'){n=6;for(let i=0;i<3;i++)for(let j=3;j<6;j++)e.push([i,j]);}
  if(type==='Q3'){n=8;for(let i=0;i<n;i++)for(let k=0;k<3;k++){let j=i^(1<<k);if(i<j)e.push([i,j]);}}
  if(type==='Petersen'){n=10;for(let i=0;i<5;i++){e.push([i,(i+1)%5],[i,i+5],[i+5,5+(i+2)%5]);}}
  if(type==='Prism12'){n=12;for(let i=0;i<6;i++){e.push([i,(i+1)%6],[i+6,6+(i+1)%6],[i,i+6]);}}
  e=e.map(([a,b])=>a<b?[a,b]:[b,a]);e.sort((x,y)=>x[0]-y[0]||x[1]-y[1]);
  assert.equal(e.length,3*n/2);return {n,e};
}
function source(type,odd){
  let {n,e}=edgesFor(type),loc=Array.from({length:n},()=>[]);
  e.forEach(([a,b],i)=>{loc[a].push(i);loc[b].push(i)});
  let cls=[],facet=[];
  for(let v=0;v<n;v++){
    assert.equal(loc[v].length,3);
    for(let z=0;z<8;z++){
      let a=(z>>2)&1,b=(z>>1)&1,c=z&1;
      if((a^b^c)!==(odd&&v===0?1:0)){
        let vrs=loc[v];cls.push([a?-vrs[0]-1:vrs[0]+1,b?-vrs[1]-1:vrs[1]+1,c?-vrs[2]-1:vrs[2]+1]);
        facet.push({v,pattern:z});
      }
    }
  }
  return {n,e,cls,facet};
}
function meets(c,bits){return c.some(l=>Boolean(bits&(1<<(Math.abs(l)-1)))===(l>0))}
function run(type){
  const o=source(type,true),ev=source(type,false),m=o.cls.length,nbits=o.e.length,full=(1n<<BigInt(m))-1n;
  const witness=Array(m).fill(null);let satOdd=0,satEven=0,checks=0;
  for(let bits=0;bits<(1<<nbits);bits++){
    let mask=0n;
    o.cls.forEach((c,i)=>{if(meets(c,bits))mask|=1n<<BigInt(i)});
    if(mask===full)satOdd++;
    for(let i=0;i<m;i++)if(witness[i]===null&&(mask|(1n<<BigInt(i)))===full)witness[i]=bits;
    if(ev.cls.every(c=>meets(c,bits)))satEven++;
  }
  assert.equal(satOdd,0);assert(witness.every(x=>x!==null));
  assert.equal(satEven,2**(nbits-o.n+1));checks+=m+3;
  let state=(92817+o.n)>>>0;
  const next=()=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state};
  const sub=k=>{const a=Array.from({length:m},(_,i)=>i);for(let i=m-1;i>0;i--){let j=next()%(i+1);[a[i],a[j]]=[a[j],a[i]];}return a.slice(0,k).sort((a,b)=>a-b)};
  const k=m/2;
  for(let t=0;t<1150;t++){
    let A=sub(k),B=sub(k);
    if(A.join(',')===B.join(',')){
      B=sub(k);
      if(A.join(',')===B.join(','))B=[...A.slice(0,k-1),...Array.from({length:m},(_,i)=>i).filter(i=>!A.includes(i)).slice(0,1)].sort((a,b)=>a-b);
    }
    assert.notEqual(A.join(','),B.join(','));
    let missing=A.find(j=>!B.includes(j));assert(missing!==undefined);
    let clauses=B.map(j=>o.cls[j]).concat(Array.from({length:m},(_,i)=>i).filter(j=>!A.includes(j)).map(j=>o.cls[j]));
    assert.equal(clauses.length,m);assert(clauses.every(c=>meets(c,witness[missing])));
    assert.equal(clauses.filter((c,i,all)=>all.some((d,j)=>j<i&&d.join()==c.join())).length>0,true);
    checks+=4;
  }
  return {graph:type,variables:nbits,vertices:o.n,clauses:m,odd_models:satOdd,even_models:satEven,verified_deleted_clauses:witness.length,random_mixed_pairs:1150,assertions:checks};
}
const graphs=['K4','K33','Q3','Petersen','Prism12'].map(run);
const result={status:'COMPUTATIONAL independent original-signed-CNF verifier only',graphs,assertions:graphs.reduce((a,b)=>a+b.assertions,0),failures:0};
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+'\n');
process.stdout.write(JSON.stringify(result,null,2)+'\n');
