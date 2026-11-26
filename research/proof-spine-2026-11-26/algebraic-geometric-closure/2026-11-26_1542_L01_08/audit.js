const result = (function audit(){
 const r={hc_position_assignments:0,hc_masks:0,hc_formula_models:[],cnf_signed_coeffs:0,incidence_signed_coeffs:0,bipartite_mask_checks:0,weighted_min_cut_checks:0,neighbor_pairs:[],large_charts:[],failures:0};
 function ck(x){if(!x)throw Error("assertion failed")}
 function permutations(a){if(!a.length)return [[]];return a.flatMap((v,i)=>permutations(a.filter((_,j)=>i!==j)).map(t=>[v,...t]));}
 function hcFormula(n){
  let m=n*n, edges=[],clauses=[],eid={};
  for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(i!==j){eid[i*n+j]=m++;edges.push([i,j]);}
  const ex=xs=>{clauses.push(xs.map(i=>i+1));for(let i=0;i<xs.length;i++)for(let j=i+1;j<xs.length;j++)clauses.push([-xs[i]-1,-xs[j]-1]);};
  for(let k=0;k<n;k++){ex(Array.from({length:n},(_,i)=>k*n+i));ex(Array.from({length:n},(_,i)=>i*n+k));ex(edges.filter(e=>e[0]===k).map(([i,j])=>eid[i*n+j]));}
  clauses.push([1]);
  for(let k=0;k<n;k++)for(const [i,j] of edges)clauses.push([-k*n-i-1,-((k+1)%n)*n-j-1,eid[i*n+j]+1]);
  return {n,m,edges,eid,clauses};
 }
 const sat=(cs,a)=>cs.every(c=>c.some(l=>a[Math.abs(l)-1]===(l>0?1:0)));
 function literalGraph(m,cs){const edges=[];for(let i=0;i<m;i++){edges.push([2*i,2*i+1],[2*i,2*m+i],[2*i+1,2*m+i]);}for(let k=0;k<cs.length;k++)for(const l of new Set(cs[k]))edges.push([2*(Math.abs(l)-1)+(l>0?1:0),3*m+k]);return {v:3*m+cs.length,e:edges};}
 const incidence=g=>({v:g.v+g.e.length,e:g.e.flatMap(([u,v],i)=>[[u,g.v+i],[v,g.v+i]]),left:g.v});
 const independent=(g,s)=>g.e.every(([u,v])=>!((s>>u&1)&&(s>>v&1)));
 const pop=s=>s.toString(2).replace(/0/g,"").length;
 for(let n=2;n<=4;n++){
  const f=hcFormula(n), tours=permutations(Array.from({length:n-1},(_,i)=>i+1)).map(t=>[0,...t]);
  const valid=[];
  for(const t of tours){const a=Array(f.m).fill(0);let mask=0;for(let k=0;k<n;k++){a[k*n+t[k]]=1;const id=f.eid[t[k]*n+t[(k+1)%n]];a[id]=1;mask|=1<<(id-n*n);}ck(sat(f.clauses,a));valid.push(mask);}
  r.hc_formula_models.push({n,normalized:tours.length});
  if(n<=3){let seen=0;for(let s=0;s<1<<f.m;s++){const a=Array.from({length:f.m},(_,i)=>s>>i&1);if(sat(f.clauses,a)){seen++;ck(valid.includes(s>>n*n));}r.hc_position_assignments++;}ck(seen===tours.length);}
  // Independently traverse successor permutations for each availability mask.
  const perms=permutations(Array.from({length:n},(_,i)=>i));
  for(let mask=0;mask<1<<f.edges.length;mask++){
    const expected=valid.filter(v=>(v&mask)===v).length;
    let actual=0;for(const w of perms){if(w.some((j,i)=>i===j||!(mask>>(f.eid[i*n+j]-n*n)&1)))continue;let j=0,k=0;do{j=w[j];k++;}while(j!==0&&k<n);if(k===n&&j===0)actual++;}
    ck(expected===actual);r.hc_masks++;
  }
 }
 // Signed literal gadgets: full independent set enumeration, coefficient by exact assignment.
 const formulas=[[],[[1]],[[1],[-1]],[[1,2],[-1,2]],[[1,2,3],[-1,-2],[2,-3]],[[1,-1],[]]];
 for(const cs of formulas){const m=Math.max(1,...cs.flat().map(Math.abs)),g=literalGraph(m,cs),coeff=Array(1<<m).fill(0);
  for(let s=0;s<1<<g.v;s++)if(independent(g,s)){let k=0;for(let i=0;i<m;i++)if(s>>(2*i+1)&1)k|=1<<i;coeff[k]+=pop(s>>(2*m))%2?-1:1;}
  for(let k=0;k<1<<m;k++){ck(coeff[k]===Number(sat(cs,Array.from({length:m},(_,i)=>k>>i&1))));r.cnf_signed_coeffs++;}
 }
 // Incidence adapter: independent set enumeration on B, aggregate by complement of original-side selection.
 for(let em=0;em<8;em++){const e=[[0,1],[0,2],[1,2]].filter((_,i)=>em>>i&1),g={v:3,e},b=incidence(g),coeff=Array(8).fill(0);
  for(let s=0;s<1<<b.v;s++)if(independent(b,s)){coeff[7^(s&7)]+=pop(s>>3)%2?-1:1;}
  for(let k=0;k<8;k++){ck(coeff[k]===Number(independent(g,k)));r.incidence_signed_coeffs++;}
 }
 // Exact min-cut via Edmonds-Karp, arbitrary signed unary costs and permitted masks.
 function flowOpt(g,masks,cost){let L=g.v,S=L,T=L+1,A=Array.from({length:L+2},()=>Array(L+2).fill(0)),base=0;
  const big=1+cost.reduce((s,c)=>s+Math.abs(c[0]-c[1]),0);
  for(let v=0;v<L;v++){let c= v<g.left?cost[v]:[cost[v][1],cost[v][0]],mask=masks[v];if(v>=g.left)mask=((mask&1)<<1)|((mask&2)>>1);let a=Math.min(...c);base+=a;A[S][v]+=c[0]-a;A[v][T]+=c[1]-a;if(!(mask&1))A[S][v]+=big;if(!(mask&2))A[v][T]+=big;}
  for(const [u,v] of g.e)A[u][v]+=big;
  let f=0;while(true){let p=Array(L+2).fill(-1);p[S]=S;let q=[S];for(let i=0;i<q.length&&p[T]<0;i++)for(let j=0;j<L+2;j++)if(p[j]<0&&A[q[i]][j]>0){p[j]=q[i];q.push(j);}if(p[T]<0)break;let d=Infinity;for(let j=T;j!==S;j=p[j])d=Math.min(d,A[p[j]][j]);for(let j=T;j!==S;j=p[j]){A[p[j]][j]-=d;A[j][p[j]]+=d;}f+=d;}
  return f>=big?Infinity:base+f;
 }
 for(let em=0;em<16;em++){const g={v:4,left:2,e:[[0,2],[0,3],[1,2],[1,3]].filter((_,i)=>em>>i&1)};
  for(let code=0;code<256;code++){let masks=Array.from({length:4},(_,i)=>(code>>(2*i))&3),cost=Array.from({length:4},(_,i)=>[((code+3*i)%11)-5,((em+7*i+code)%13)-6]);let best=Infinity;
   for(let s=0;s<16;s++)if(independent(g,s)&&masks.every((m,i)=>m&(1<<(s>>i&1))))best=Math.min(best,cost.reduce((a,c,i)=>a+c[s>>i&1],0));
   let d=masks.every(Boolean)&&g.e.every(([u,v])=>(masks[u]&1)||(masks[v]&1));ck(d===(best!==Infinity));r.bipartite_mask_checks++;ck(flowOpt(g,masks,cost)===best);r.weighted_min_cut_checks++;
  }
 }
 for(const n of [4,8,16,32,64]){
  const f=hcFormula(n),g=literalGraph(f.m,f.clauses),b=incidence(g);
  // Forcing one adjacent pair in B, then releasing exactly one label gives genuine NO/YES.
  const [u,v]=b.e[0],mask=Array(b.v).fill(3);mask[u]=2;mask[v]=2;
  const d=()=>mask.every(Boolean)&&b.e.every(([a,z])=>(mask[a]&1)||(mask[z]&1));
  ck(!d());mask[v]=3;ck(d());r.neighbor_pairs.push({n,vertices:b.v,edges:b.e.length});
  // Source tour mask versus deletion of one required edge; explicit witness and isolated outgoing row.
  const a=Array(f.m).fill(0);for(let k=0;k<n;k++){a[k*n+k]=1;a[f.eid[k*n+(k+1)%n]]=1;}ck(sat(f.clauses,a));a[f.eid[1]]=0;ck(!sat(f.clauses,a));
  r.large_charts.push({n,variables:f.m,clauses:f.clauses.length,G_vertices:g.v,G_edges:g.e.length,B_vertices:b.v,B_edges:b.e.length});
 }
 return r;
})();
console.log(JSON.stringify(result,null,2));
