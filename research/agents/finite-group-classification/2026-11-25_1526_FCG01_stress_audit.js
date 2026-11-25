function fcg01(){
 const assert=(b,m)=>{if(!b)throw Error(m)};
 const key=a=>a.slice().sort().join("|");
 const ek=(a,b)=>key([a,b]);
 const uniq=a=>[...new Set(a)];
 const add=(a,b)=>a.map((x,i)=>x+b[i]);
 const sub=(a,b)=>a.map((x,i)=>x-b[i]);
 const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
 const dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0);
 function choose(a,k){if(k===0)return [[]];let out=[];for(let i=0;i<=a.length-k;i++)for(const r of choose(a.slice(i+1),k-1))out.push([a[i],...r]);return out}
 function graph(n,edges){let A=Array.from({length:n},()=>new Set());for(let [u,v] of edges){assert(u!==v,"loop");A[u].add(v);A[v].add(u)}return A}
 function connected(A,omit=[]){let O=new Set(omit),start=A.findIndex((_,i)=>!O.has(i));if(start<0)return true;let q=[start],S=new Set(q);for(let i=0;i<q.length;i++)for(let v of A[q[i]])if(!O.has(v)&&!S.has(v)){q.push(v);S.add(v)}return S.size===A.length-O.size}
 function source(L){
  let T=new Map();for(let a of [-1,1])for(let b of [-1,1])for(let c of [-1,1]){
   let p=(i,j)=>[a*i,b*j,c*(L-i-j)];function put(t){let n=cross(sub(t[1],t[0]),sub(t[2],t[0]));if(dot(n,add(add(t[0],t[1]),t[2]))<0)[t[1],t[2]]=[t[2],t[1]];T.set(key(t.map(v=>v.join(","))),t)}
   for(let i=0;i<L;i++)for(let j=0;j<L-i;j++){put([p(i,j),p(i+1,j),p(i,j+1)]);if(i+j+2<=L)put([p(i+1,j),p(i+1,j+1),p(i,j+1)])}
  }
  let E=new Map(),edgeEnds=[],endTri=[],V=[],arcs=[];
  for(let t of T.values()){
   let es=[];for(let j=0;j<3;j++){let a=t[j],b=t[(j+1)%3],k=ek(a.join(","),b.join(","));if(!E.has(k)){E.set(k,E.size);edgeEnds.push([a,b]);endTri.push([])}let e=E.get(k);es.push(e);endTri[e].push(V.length)}
   V.push(es);for(let j=0;j<3;j++)arcs.push([es[j],es[(j+1)%3]]);
  }
  let n=E.size;assert(n===12*L*L&&V.length===8*L*L&&endTri.every(t=>t.length===2),"triangulation size");
  let pc=v=>(Math.abs(v[0])+2*Math.abs(v[1]))%3,colors=edgeEnds.map(([a,b])=>{assert(pc(a)!==pc(b),"proper primal coloring");return 3-pc(a)-pc(b)});
  let O=Array.from({length:n},()=>[]);arcs.forEach(([u,v],i)=>O[u].push(i));assert(O.every(a=>a.length===2),"outdegree");
  let clauses=arcs.map(([u,v],i)=>[i,...O[v]]),part=arcs.map(([u])=>colors[u]);
  let occ=Array.from({length:arcs.length},()=>[]);clauses.forEach((c,j)=>c.forEach(v=>occ[v].push(j)));
  assert(occ.every(a=>a.length===3&&new Set(a.map(i=>part[i])).size===3),"partition certificate");
  assert(new Set(occ.map(a=>key(a))).size===occ.length,"no duplicate occurrence signatures");
  let G0=graph(2*arcs.length,clauses.flatMap((c,j)=>c.map(v=>[v,arcs.length+j])));assert(G0.every(a=>a.size===3)&&connected(G0),"source incidence");
  if(L===1){for(let S of [...choose([...G0.keys()],1),...choose([...G0.keys()],2)])assert(connected(G0,S),"3-connected incidence")}
  let mixed=O.map((a,e)=>[e,...a.map(i=>arcs[i][1])]);assert(mixed.every(t=>new Set(t.map(v=>colors[v])).size===3),"mixed rainbow");
  let G=graph(n,mixed.flatMap(t=>choose(t,2)));assert(G.every(a=>a.size<=6&&a.size>=5),"degree");
  assert(V.every(t=>choose(t,2).every(([u,v])=>G[u].has(v))),"line graph contained");
  let w=Array(n).fill(0);mixed.forEach(t=>t.forEach(v=>w[v]++));let w2=Array(n).fill(0);V.forEach(t=>t.forEach(v=>w2[v]+=3));assert(w.every((x,i)=>x===3&&w2[i]===2*x)&&3*V.length===2*n,"exact rational clique cover");
  return {G,clauses,arcs,colors,mixed,endpoint:V,sourceVertices:arcs.length};
 }
 function solveRegion(G,T){
  const incidence=new Map(),adj=Array.from({length:T.length},()=>new Set());for(let i=0;i<T.length;i++)for(let p of choose(T[i],2)){let k=key(p);if(incidence.has(k)){let j=incidence.get(k);adj[i].add(j);adj[j].add(i)}else incidence.set(k,i)}
  let q=[0],parent=new Map([[0,-1]]);for(let i=0;i<q.length;i++)for(let j of adj[q[i]])if(!parent.has(j)){parent.set(j,q[i]);q.push(j)}
  assert(q.length===T.length,"triangle region connected");
  let solutions=[];for(let p of T[0]){let x=new Map(T[0].map(v=>[v,+(v===p)])),ok=true;for(let j of q.slice(1)){let prev=T[parent.get(j)],s=T[j].filter(v=>prev.includes(v)),v=T[j].find(v=>!prev.includes(v));assert(s.length===2&&v!==undefined,"pair overlap");let b=1-x.get(s[0])-x.get(s[1]);if(b<0||b>1||(x.has(v)&&x.get(v)!==b)){ok=false;break}x.set(v,b)}
   if(ok&&x.size===G.length&&T.every(t=>t.reduce((s,v)=>s+x.get(v),0)===1)&&G.every((a,v)=>!x.get(v)||[...a].every(u=>!x.get(u))))solutions.push([...G.keys()].filter(v=>x.get(v)))
  }
  return solutions;
 }
 function claw(G,v,S){let N=[...G[v]].filter(u=>S.has(u));for(let i=0;i<N.length;i++)for(let j=i+1;j<N.length;j++)for(let k=j+1;k<N.length;k++)if(!G[N[i]].has(N[j])&&!G[N[i]].has(N[k])&&!G[N[j]].has(N[k]))return [v,N[i],N[j],N[k]];return null}
 function run(L){
  let {G,clauses,arcs,colors,mixed,endpoint,sourceVertices}=source(L),n=G.length,T=[...new Map([...mixed,...endpoint].map(t=>[key(t),t])).values()];
  let solutions=solveRegion(G,T);assert(solutions.length===3,"three exact regions");
  for(let I of solutions){let S=new Set(I),x=arcs.map(([u,v])=>+S.has(v));assert(I.length===n/3&&clauses.every(t=>t.reduce((s,v)=>s+x[v],0)===1),"source witness")}
  let triangles=[];for(let i=0;i<n;i++)for(let j of G[i])if(j>i)for(let k of G[j])if(k>j&&G[i].has(k))triangles.push([i,j,k]);
  assert(G.every((a,i)=>[...a].every(j=>colors[i]!==colors[j])),"3-color certificate");
  let cliques=[...G.keys()].map(i=>[i]);for(let i=0;i<n;i++)for(let j of G[i])if(j>i)cliques.push([i,j]);cliques.push(...triangles);
  let separators=cliques.filter(C=>!connected(G,C)).length;assert(!separators,"clique atom");
  let d=Math.max(...G.map(a=>a.size)),modules=0;
  for(let u=0;u<n;u++)for(let v=u+1;v<n;v++){let S=new Set([u,v]),Q=[v];for(let i=0;i<Q.length&&S.size<=d;i++){let a=Q[i];for(let x of uniq([...G[u],...G[a]]))if(!S.has(x)&&G[u].has(x)!==G[a].has(x)){S.add(x);Q.push(x)}}if(S.size<=d)modules++}
  assert(!modules,"prime graph");
  let all=new Set(G.keys());assert(G.every((_,v)=>claw(G,v,all)),"persistent claw at every center");let S=new Set(all),p=0;for(;;){let C=null;for(let v of S)if((C=claw(G,v,S)))break;if(!C)break;p++;for(let v of C){S.delete(v);for(let u of G[v])S.delete(u)}}
  return {L,sourceVariables:sourceVertices,phaseVertices:n,originalGroups:mixed.length,certifiedTriangleRows:T.length,allTriangles:triangles.length,exactSolutions:solutions.length,cliqueSeparators:separators,properModulePairs:modules,anticompleteClawPacking:p,maxDegree:d};
 }
 let result=[1,2,3,4,5].map(run);
 let K4=graph(4,choose([0,1,2,3],2)),tri=choose([0,1,2,3],3);assert(solveRegion(K4,tri).length===0,"fractional but integral UNSAT control");
 return {sourceStress:result,abstractK4:{fractionalSolution:[1/3,1/3,1/3,1/3],integralSolutions:0}};
}
console.log(JSON.stringify(fcg01(),null,2));
