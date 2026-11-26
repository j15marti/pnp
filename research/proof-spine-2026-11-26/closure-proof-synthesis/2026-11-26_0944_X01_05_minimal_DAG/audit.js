console.log(JSON.stringify((function audit(){
  let assertions=0,rankOps=0,dpTransitions=0,cofactorVisits=0;const ok=(x)=>{if(!x)throw Error("check "+assertions);assertions++};
  const K4={name:"K4",n:4,E:[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]};
  function prism(k,name){const E=[];for(let i=0;i<k;i++)E.push([i,(i+1)%k],[k+i,k+(i+1)%k],[i,k+i]);return {name,n:2*k,E}}
  const P={name:"Petersen",n:10,E:Array.from({length:5},(_,i)=>[[i,(i+1)%5],[i,5+i],[5+i,5+(i+2)%5]]).flat()};
  const graphs=[K4,prism(3,"Triangular prism"),prism(4,"Cube"),P,prism(6,"Hexagonal prism")];
  const pc=(x)=>{let n=0;for(;x;x&=x-1)n++;return n};
  function rankTable(C,r){const m=C.length,L=1<<m,B=new Int32Array(r),R=new Uint8Array(L);function visit(j,S,d){if(j===m){R[S]=d;return}visit(j+1,S,d);let v=C[j];while(v){const p=31-Math.clz32(v);rankOps++;if(!B[p]){B[p]=v;visit(j+1,S|(1<<j),d+1);B[p]=0;return}v^=B[p]}visit(j+1,S|(1<<j),d)}visit(0,0,0);return R}
  function affine(C,r){const m=C.length,L=1<<m,all=L-1,R=rankTable(C,r),D=new Float64Array(L),prev=new Uint8Array(L);D.fill(Infinity);D[0]=0;let widths=new Uint8Array(L);widths[0]=0;for(let S=0;S<L;S++){const lambda=R[S]+R[all^S]-R[all];ok(lambda>=0);for(let B=all^S;B;B&=B-1){const b=B&-B,j=31-Math.clz32(b),q=S|b,c=D[S]+(C[j]?2**lambda:0);dpTransitions++;if(c<D[q]){D[q]=c;prev[q]=j;widths[q]=Math.max(widths[S],lambda)}}}let ord=[],S=all;while(S){const j=prev[S];ord.push(j);S^=1<<j}ord.reverse();S=0;let cost=0,peak=0;for(const j of ord){let l=R[S]+R[all^S]-R[all];peak=Math.max(peak,l);cost+=C[j]?2**l:0;S|=1<<j}ok(cost===D[all]);return {nodes:cost,order:ord,maxRank:peak,rank:R[all]}}
  function clauses(G){const inc=Array.from({length:G.n},(_,v)=>G.E.flatMap((e,i)=>e.includes(v)?[i]:[]));ok(inc.every(r=>r.length===3));const rows=[];for(let v=0;v<G.n;v++){const charge=+(v===G.n-1);for(let u=0;u<8;u++)if((pc(u)&1)!==charge){let mask=0,pat=0;inc[v].forEach((e,j)=>{mask|=1<<e;if(u>>j&1)pat|=1<<e});rows.push({v,mask,pat})}}return {inc,rows}}
  function reduced(S,m,order,manager){const A=new Uint8Array(1<<m);for(const x of S)A[x]=1;function rec(j,x){if(j===m)return A[x];const i=order[j],lo=rec(j+1,x),hi=rec(j+1,x|(1<<i));if(lo===hi)return lo;const key=i+","+lo+","+hi;if(!manager.map.has(key)){manager.map.set(key,manager.nodes.length+2);manager.nodes.push([i,lo,hi])}return manager.map.get(key)}const root=rec(0,0),reach=new Set();function walk(q){if(q<2||reach.has(q))return;reach.add(q);const [i,l,h]=manager.nodes[q-2];walk(l);walk(h)}walk(root);return {nodes:reach.size,root,reach}}
  function generic(S,m){const L=1<<m,all=L-1,D=new Float64Array(L),P=new Uint8Array(L);D.fill(Infinity);D[0]=0;
    const lowMasks=Array.from({length:m+1},(_,r)=>Array.from({length:r},(_,p)=>{let w=0n;for(let i=0;i<(1<<r);i++)if(!(i>>p&1))w|=1n<<BigInt(i);return w}));
    const compress=(x,M)=>{let z=0,j=0;for(let B=M;B;B&=B-1,j++)if(x&(B&-B))z|=1<<j;return z};
    for(let T=0;T<L;T++){const U=all^T,by=new Map(),r=pc(U);for(const x of S){cofactorVisits++;const a=x&T,b=compress(x,U);by.set(a,(by.get(a)||0n)|(1n<<BigInt(b)))}const distinct=new Set(by.values());let p=0;for(let B=U;B;B&=B-1,p++){const b=B&-B,j=31-Math.clz32(b);let d=0;for(const f of distinct)if(((f^(f>>BigInt(1<<p)))&lowMasks[r][p])!==0n)d++;dpTransitions++;const q=T|b;if(D[T]+d<D[q]){D[q]=D[T]+d;P[q]=j}}}
    let q=all,ord=[];while(q){let j=P[q];ord.push(j);q^=1<<j}return {nodes:D[all],order:ord.reverse()}}
  const result=[];
  for(const G of graphs){
    const m=G.E.length,L=1<<m,{inc,rows}=clauses(G),C=G.E.map(([u,v])=>(1<<u)|(1<<v)),fixed=Array.from({length:m},(_,i)=>i),manager={map:new Map(),nodes:[]},union=new Set(),aff=[],each=[];
    let S=Array.from({length:L},(_,i)=>i),lastCount=L,live=[],maxLive=0,chargeWork=0;
    for(let j=0;j<=rows.length;j++){
      if(j){const c=rows[j-1];S=S.filter(a=>(a&c.mask)!==c.pat)}
      ok(S.length<=lastCount);lastCount=S.length;
      const f=reduced(S,m,fixed,manager);for(const q of f.reach)union.add(q);maxLive=Math.max(maxLive,f.nodes);chargeWork+=f.nodes;
      const e={clauses:j,solutions:S.length,fixedNodes:f.nodes,persistentUniqueNodes:union.size};
      let a=null;
      if(j%4===0&&j<rows.length){const r=j/4;a=affine(C.map(x=>x&((1<<r)-1)),r);ok(S.length===2**(m-r));aff.push({equations:r,clauses:j,solutions:S.length,minNodes:a.nodes,maxRank:a.maxRank,order:a.order})}
      if(j===rows.length-1){const r=G.n-1,D=C.map(x=>x&((1<<r)-1));inc[G.n-1].forEach((i,q)=>D[i]|=1<<(r+q));a=affine(D,r+3);ok(S.length===2**(m-G.n-1));aff.push({equations:"all-but-one-clause",clauses:j,solutions:S.length,minNodes:a.nodes,maxRank:a.maxRank,order:a.order})}
      if(j===rows.length){ok(S.length===0);a={nodes:0,order:fixed,maxRank:0};aff.push({equations:G.n,clauses:j,solutions:0,minNodes:0,maxRank:0,order:fixed})}
      if(a){const z=reduced(S,m,a.order,{map:new Map(),nodes:[]});ok(z.nodes===a.nodes);e.minNodes=a.nodes;e.minOrder=a.order}
      if(m<=9){const b=generic(S,m),z=reduced(S,m,b.order,{map:new Map(),nodes:[]});ok(z.nodes===b.nodes);if(a)ok(a.nodes===b.nodes);e.minNodes=b.nodes}
      each.push(e);
    }
    // Independently test minimal UNSAT property: removing ANY one clause has a model.
    for(let j=0;j<rows.length;j++){let witness=-1;for(let x=0;x<L;x++)if(rows.every((c,i)=>i===j||(x&c.mask)!==c.pat)){witness=x;break}ok(witness>=0)}
    ok(manager.nodes.length===union.size);
    result.push({name:G.name,vertices:G.n,variables:m,totalClauses:rows.length,affineStages:aff,clauseStages:each,peakFixedNodes:maxLive,fixedSharedNodeCreations:union.size,sumFixedSnapshotNodes:chargeWork,minimalUnsatDeletionChecks:rows.length});
  }
  // tiny graph independent exhaustive permutation verification at last complete proper equation group, K4.
  const {rows}=clauses(K4),S=Array.from({length:64},(_,x)=>x).filter(x=>rows.slice(0,12).every(c=>(x&c.mask)!==c.pat));let count=0,lo=Infinity;function perm(P,R){if(!R.length){count++;lo=Math.min(lo,reduced(S,6,P,{map:new Map(),nodes:[]}).nodes);return}for(const x of R)perm([...P,x],R.filter(y=>x!==y))}perm([], [0,1,2,3,4,5]);ok(lo===result[0].affineStages.find(x=>x.clauses===12).minNodes);
  return {assertions,rankOps,dpTransitions,cofactorVisits,exhaustiveOrderCheck:{orders:count,minNodes:lo},graphs:result}
})(),null,2));
