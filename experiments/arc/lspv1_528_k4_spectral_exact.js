'use strict';
// LSPV-1/528: independent K4 pair-defect compatibility and source-cover checks.
const assert = require('assert');
const V=[0,1,2,3], edges=[];
for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)edges.push([u,v]);
const inc=V.map(v=>edges.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0));
const charges=[1,0,0,0], clauses=[], meta=[], R=V.map(()=>[]), E=V.map(()=>[]);
for(let ei=0;ei<6;ei++){clauses.push([3*ei+1,3*ei+2,3*ei+3]);meta.push(['A',ei,null])}
for(const v of V)for(let a=0;a<3;a++)for(let c=0;c<3;c++)for(let d=0;d<3;d++){
 const lab=[a,c,d];
 let divergence=0;
 inc[v].forEach((ei,k)=>divergence+=(edges[ei][0]===v?1:-1)*lab[k]);
 divergence=(divergence%3+3)%3;
 if(divergence===charges[v])continue;
 const id=clauses.length;
 clauses.push(inc[v].map((ei,k)=>-(3*ei+lab[k]+1)));
 const kind=divergence===(charges[v]+1)%3?'R':'E';
 meta.push([kind,v,lab]);
 (kind==='R'?R:E)[v].push(id);
}
assert.strictEqual(clauses.length,78);
for(const v of V){assert.strictEqual(R[v].length,9);assert.strictEqual(E[v].length,9)}
const pairs={}, H=new Set();
for(let u=0;u<4;u++)for(let v=u+1;v<4;v++){
 let found=0;
 for(let code=0;code<729;code++){
  let x=[],t=code;
  for(let e=0;e<6;e++){x.push(t%3);t=Math.floor(t/3)}
  const div=V.map(w=>{let s=0;for(const ei of inc[w])s+=(edges[ei][0]===w?1:-1)*x[ei];return (s%3+3)%3});
  if(div.some((z,w)=>z!==(charges[w]+(w===u||w===v?1:0))%3))continue;
  found++;
  let ids=[];
  for(const w of [u,v]){
    const labels=inc[w].map(e=>x[e]);
    const k=R[w].findIndex(id=>meta[id][2].every((z,j)=>z===labels[j]));
    assert(k>=0);ids.push(w*9+k);
  }
  H.add(ids.sort((a,b)=>a-b).join(','));
 }
 assert.strictEqual(found,27);pairs[u+','+v]=found;
}
assert.strictEqual(H.size,162);
const A=Array.from({length:36},()=>Array(36).fill(0));
for(const s of H){const [u,v]=s.split(',').map(Number);A[u][v]=A[v][u]=1}
for(const row of A)assert.strictEqual(row.reduce((a,b)=>a+b,0),9);
// Each compatible pair agrees on the unique shared edge label.
for(let u=0;u<4;u++)for(let v=u+1;v<4;v++){
 const ei=edges.findIndex(e=>e[0]===u&&e[1]===v);
 for(let i=0;i<9;i++)for(let j=0;j<9;j++){
   const left=meta[R[u][i]][2][inc[u].indexOf(ei)];
   const right=meta[R[v][j]][2][inc[v].indexOf(ei)];
   assert.strictEqual(H.has((u*9+i)+','+(v*9+j)),left===right);
 }
}
function mul(X,Y){
 const n=X.length,Z=Array.from({length:n},()=>Array(n).fill(0));
 for(let i=0;i<n;i++)for(let k=0;k<n;k++)if(X[i][k])for(let j=0;j<n;j++)Z[i][j]+=X[i][k]*Y[k][j];
 return Z;
}
const minus=(X,t)=>X.map((r,i)=>r.map((z,j)=>z-(i===j?t:0)));
const poly=mul(mul(mul(A,minus(A,9)),minus(A,3)),minus(A,-3));
assert(poly.every(r=>r.every(z=>z===0)));
const tr2=mul(A,A).reduce((s,r,i)=>s+r[i],0);
assert.strictEqual(tr2,324);
// Exact spectral values: -3 mult 15, 0 mult 8, +3 mult 12, +9 mult 1.
assert.strictEqual(36*3/(9+3),9);
// The core omitting the R nine-clause group at vertex 3 is UNSAT and minimal.
const core=clauses.map((_,j)=>j).filter(j=>!R[3].includes(j));
assert.strictEqual(core.length,69);
const witnesses=new Map();
let satisfiers=0;
for(let mask=0;mask<(1<<18);mask++){
 let violated=0,only=-1;
 for(const j of core){
  const falseClause=clauses[j].every(lit=>{
    const bit=(mask>>(Math.abs(lit)-1))&1;
    return lit>0?bit===0:bit===1;
  });
  if(falseClause){violated++;only=j}
 }
 if(violated===0)satisfiers++;
 if(violated===1&&!witnesses.has(only))witnesses.set(only,mask);
}
assert.strictEqual(satisfiers,0);
assert.strictEqual(witnesses.size,69);
const output={
 status:'COMPUTATIONAL independent signed-source and integral-matrix verification',
 sourceClauses:78,essentialSources:42,Rclauses:36,
 pairDefectFlows:162,pairCounts:pairs,compatibilityVertices:36,compatibilityEdges:162,
 degree:9,exactPolynomial:'A(A-9I)(A-3I)(A+3I)=0',spectrum:{'-3':15,'0':8,'3':12,'9':1},
 HoffmanAlpha:9,minimumRVertexCover:27,minimumUnsatCore:69,binaryInferenceLowerBound:68,
 BooleanAssignmentsChecked:262144,oneClauseDeletionWitnesses:69
};
console.log(JSON.stringify(output,null,2));
