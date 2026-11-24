"use strict";
function experiment(){
  let state=20261124; const rnd=n=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state%n};
  const B=i=>1n<<BigInt(i);
  function basis(vs){let rows=[]; for(let i=0;i<vs.length;i++){let v=vs[i],c=B(i);for(const [p,u,z] of rows)if(v&p){v^=u;c^=z}if(v){let p=B(v.toString(2).length-1);rows.push([p,v,c]);rows.sort((a,b)=>a[0]>b[0]?-1:1)}}return rows}
  function reduce(v,rows){let c=0n;for(const [p,u,z] of rows)if(v&p){v^=u;c^=z}return [v,c]}
  function match(A,skipL=[],skipR=[]){const N=A.length, sr=new Set(skipR), sl=new Set(skipL), R=Array(N).fill(-1);
    function dfs(i,seen){for(let j=0;j<N;j++)if(A[i][j]!==null&&!sr.has(j)&&!seen.has(j)){seen.add(j);if(R[j]<0||dfs(R[j],seen)){R[j]=i;return true}}return false}
    for(let i=0;i<N;i++)if(!sl.has(i)&&!dfs(i,new Set()))return null;
    const p=Array(N).fill(-1);for(let j=0;j<N;j++)if(R[j]>=0)p[R[j]]=j;return p;
  }
  function all(A){const out=[],p=[],N=A.length;function go(i,used,s){if(i===N){out.push({p:[...p],s});return}for(let j=0;j<N;j++)if(A[i][j]!==null&&!(used&B(j))){p.push(j);go(i+1,used|B(j),s^A[i][j]);p.pop()}}go(0,0n,0n);return out}
  function syndrome(A,p){return p.reduce((s,j,i)=>s^A[i][j],0n)}
  function certify(A,u,v){const N=A.length,ne=[];for(let j=0;j<N;j++){if((A[u][j]===null)!==(A[v][j]===null))return null;if(A[u][j]!==null)ne.push(j)}
    let d=null,queries=0;for(let i=0;i<ne.length;i++)for(let j=i+1;j<ne.length;j++){const a=ne[i],b=ne[j];queries++;if(!match(A,[u,v],[a,b]))continue;const q=A[u][a]^A[v][a]^A[u][b]^A[v][b];if(d!==null&&d!==q)return {valid:false,queries};d=q}
    return {valid:d!==null,d,queries};
  }
  function clone(A,tags,noise=false){const n=A.length,C=Array.from({length:2*n},()=>Array(2*n).fill(null));for(let i=0;i<n;i++){C[2*i][n+i]=0n;C[2*i+1][n+i]=tags[i];for(let j=0;j<n;j++)if(A[i][j]!==null){C[2*i][j]=A[i][j];C[2*i+1][j]=A[i][j]^(noise?BigInt(rnd(8)):0n)}}return C}
  function cycle(n,hole){const A=Array.from({length:n},()=>Array(n).fill(null));for(let i=0;i<n;i++){A[i][i]=0n;A[i][(i+1)%n]=i===0?1n:0n}if(hole)A[0][2]=2n;return A}
  function check(x,msg){if(!x)throw Error(msg)}
  let counts={graphs:0,reference_matchings:0,twin_candidates:0,certified_nonzero:0,rejected_nonconstant:0,matching_queries:0,target_checks:0,sat:0,unsat:0,protected_checks:0,protected_nonzero_ranks:0,overlap_hole:0};
  for(let z=0;z<240;z++){
    const n=2+rnd(3);let A;
    if(z<120){A=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i===j||rnd(3)?BigInt(rnd(16)):null));}
    else{const D=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i===j||rnd(3)?BigInt(rnd(8)):null));A=clone(D,Array.from({length:n},()=>BigInt(rnd(16))),z>=200)}
    const ms=all(A),support=new Set(ms.map(m=>m.s));check(ms.length>0,"empty control");counts.graphs++;counts.reference_matchings+=ms.length;
    let gen=[],swaps=[];
    for(let u=0;u<A.length;u++)for(let v=u+1;v<A.length;v++){const c=certify(A,u,v);if(c===null)continue;counts.twin_candidates++;counts.matching_queries+=c.queries;
      const ds=new Set(ms.map(m=>{let p=[...m.p];[p[u],p[v]]=[p[v],p[u]];return m.s^syndrome(A,p)}));check(c.valid===(ds.size===1),"certificate completeness");
      if(!c.valid){counts.rejected_nonconstant++;continue}check(ds.has(c.d),"wrong delta");if(c.d){gen.push(c.d);swaps.push([u,v]);counts.certified_nonzero++}}
    const rows=basis(gen), representatives=new Map();for(const m of ms){const [q]=reduce(m.s,rows);if(!representatives.has(q))representatives.set(q,m)}
    for(let t=0;t<16;t++){const target=BigInt(t),[q]=reduce(target,rows),m=representatives.get(q);counts.target_checks++;check(Boolean(m)===support.has(target),"quotient mismatch");if(m){counts.sat++;const [rem,comb]=reduce(target^m.s,rows);check(rem===0n,"lift residual");let p=[...m.p];for(let i=0;i<swaps.length;i++)if(comb&B(i)){let [u,v]=swaps[i];[p[u],p[v]]=[p[v],p[u]]}check(syndrome(A,p)===target,"lift mismatch");}else counts.unsat++}
    // Protected coordinate bit 0. Compute kernel of projection on generators.
    const pivot=gen.findIndex(g=>g&1n),ker=gen.filter((g,i)=>i!==pivot).map(g=>g&1n?g^gen[pivot]:g),kr=basis(ker);if(kr.length)counts.protected_nonzero_ranks++;
    for(const m of ms){for(const g of ker){check(!(g&1n)&&support.has(m.s^g),"protected translation");counts.protected_checks++}}
  }
  // Hole: two edge labels sharing a vertex, each separately attainable but not together.
  const hole=cycle(3,true),hs=new Set(all(hole).map(m=>m.s));check(hs.size===3&&hs.has(0n)&&hs.has(1n)&&hs.has(2n)&&!hs.has(3n),"rank-two hole");counts.overlap_hole=1;
  const scaling=[];
  for(const n of [4,8,16,32,64,128]){
    const A=cycle(n,true),tags=Array.from({length:n},(_,i)=>B(i+2)),C=clone(A,tags);
    // Certify private triples without matching queries: both clones have identical
    // external labels and share a degree-two private neighbor. Exactly one internal
    // and one external match per triple. Every base edge is allowed (two cycle PMs,
    // plus the chord PM), and every expanded edge extends by local flips.
    for(let i=0;i<n;i++){check(C[2*i][n+i]===0n&&C[2*i+1][n+i]===tags[i],"private tags");for(let j=0;j<n;j++)check(C[2*i][j]===C[2*i+1][j],"clone mismatch");for(let k=0;k<2*n;k++)if(k!==2*i&&k!==2*i+1)check(C[k][n+i]===null,"private degree")}
    const rows=basis(tags),targets=[(B(n+2)-4n)^1n,(B(n+2)-4n)^3n];let got=[];
    for(const t of targets){const [q]=reduce(t,rows);let found=null;
      // All residual nonzero tags lie on row 0. Force each possible partner;
      // verify complete ordinary PM of remaining graph. No recursive search.
      for(let j=0;j<n;j++)if(A[0][j]!==null&&A[0][j]===q){const p=match(A,[0],[j]);if(p){p[0]=j;found=p;break}}
      if(found){let p=Array(2*n);for(let i=0;i<n;i++){p[2*i]=found[i];p[2*i+1]=n+i}const [rem,comb]=reduce(t^syndrome(C,p),rows);check(rem===0n,"scale residual");for(let i=0;i<n;i++)if(comb&B(i))[p[2*i],p[2*i+1]]=[p[2*i+1],p[2*i]];check(new Set(p).size===2*n&&syndrome(C,p)===t,"scale lift")}
      got.push(Boolean(found))}
    check(got[0]&&!got[1],"scale targets");scaling.push({base_order:n,vertices:4*n,edges:6*n+2,affine_rank:n+2,translation_rank:rows.length,residual_rank:2,sat_witness:got[0],unsat_hole:!got[1],component_count:1});
  }
  return {seed:20261124,counts,scaling,limitations:"Exhaustive small bipartite references and deterministic augmenting-path pair certificate; scaling uses directly verified private triple rule and analytically established affine hull/allowed connectivity. No general Lovasz/CPM, full cooperative closure, or strict wheel compiler executed."};
}
console.log(JSON.stringify(experiment(),null,2));
