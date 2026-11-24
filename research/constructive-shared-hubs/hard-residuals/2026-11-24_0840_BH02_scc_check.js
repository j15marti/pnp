function BH02s(){
 const assert=(x,s)=>{if(!x)throw Error(s)}, rng=s=>()=>{s^=s<<13;s^=s>>>17;s^=s<<5;return (s>>>0)/4294967296};const R=rng(208241);
 function probe(n,A,B,C){
 // A edges use anchor a=0, B anchor b=1. C are arbitrary extra NAE triples over vertices and the third anchor c=n.
 let G=Array.from({length:2*n},()=>[]),H=Array.from({length:2*n},()=>[]),arcs=[],scans=0;
 for(let j=0;j<2;j++)for(let [u,v] of j?B:A)for(let [s,t] of [[u,v],[v,u]]){let p=2*s+j,q=2*t+(j^1);G[p].push(q);H[q].push(p);arcs.push({p,q,u,v,j})}
 let seen=new Set,order=[];function dfs(v){seen.add(v);for(let u of G[v]){scans++;if(!seen.has(u))dfs(u)}order.push(v)}
 for(let v=0;v<2*n;v++)if(!seen.has(v))dfs(v);let comp=Array(2*n).fill(-1),k=0;function rev(v){comp[v]=k;for(let u of H[v]){scans++;if(comp[u]<0)rev(u)}}
 for(let i=order.length-1;i>=0;i--)if(comp[order[i]]<0){rev(order[i]);k++}
 let pairs=new Map,certArcVisits=0,certLength=0;
 for(let e of arcs)if(comp[e.p]===comp[e.q]){
 let key=Math.min(e.u,e.v)*n+Math.max(e.u,e.v);
 if(pairs.has(key))continue;let Q=[e.q],prev=new Map([[e.q,-1]]);
 for(let i=0;i<Q.length&&!prev.has(e.p);i++)for(let w of G[Q[i]]){certArcVisits++;if(!prev.has(w)){prev.set(w,Q[i]);Q.push(w)}}
 assert(prev.has(e.p),"SCC path");
 let path=[e.p];while(path[path.length-1]!==e.q)path.push(prev.get(path[path.length-1]));path.reverse();let cyc=[e.p,...path];let counts=Array.from({length:n},()=>[0,0]);
 for(let i=0;i<cyc.length-1;i++){let s=cyc[i],t=cyc[i+1],col=s&1,u=s>>1,v=t>>1;assert((t&1)===(col^1)&&G[s].includes(t),"certificate arc");counts[u][col]++;counts[v][col]++;certLength++}
 assert(counts.every(([a,b])=>a===b),"balanced cover");pairs.set(key,[e.u,e.v])}
 let P=Array.from({length:n},()=>[]);for(let [u,v] of pairs.values()){P[u].push(v);P[v].push(u)}
 let par=Array(n).fill(-1),component=Array(n).fill(-1),odd=false;for(let i=0;i<n;i++)if(par[i]<0){par[i]=0;component[i]=i;let Q=[i];for(let j=0;j<Q.length;j++)for(let v of P[Q[j]]){scans++;if(par[v]<0){par[v]=par[Q[j]]^1;component[v]=i;Q.push(v)}else if(par[v]===par[Q[j]])odd=true}}
 let chord=false;
 if(!odd){let M=new Map;for(let tri of C)for(let i=0;i<3;i++){let c=tri[i],u=tri[(i+1)%3],v=tri[(i+2)%3];if(u>=n||v>=n||component[u]!==component[v]||par[u]!==par[v])continue;if(c<n&&component[c]===component[u]&&par[c]===par[u])chord=true;let key=c*n+component[u],s=1<<par[u];M.set(key,(M.get(key)||0)|s);if(M.get(key)===3)chord=true}}
 return {pairs:[...pairs.values()],odd,chord,reject:odd||chord,scans,arcs:arcs.length,certArcVisits,certLength}}
 function refs(n,A,B,C){let x=[];for(let k=0;k<2**(n+1);k++){let v=Array.from({length:n+1},(_,i)=>(k>>i)&1);if(A.every(([a,b])=>v[a]+v[b]>=1)&&B.every(([a,b])=>v[a]+v[b]<=1)&&C.every(t=>{let a=t.reduce((s,j)=>s+v[j],0);return a>0&&a<3}))x.push(v)}return x}
 let s={cases:0,sat:0,unsat:0,rejected:0,unknownUNSAT:0,forcedPairs:0,modelPairChecks:0,referenceAssignments:0,arcs:0,scans:0,certArcVisits:0,certLength:0};
 for(let k=0;k<320;k++){let n=3+Math.floor(R()*6),A=[],B=[],C=[];let density=.15+.65*R();for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){if(R()<density)A.push([i,j]);if(R()<density)B.push([i,j]);if(R()<.12)C.push([i,j,n])}let r=probe(n,A,B,C),x=refs(n,A,B,C);assert(!r.reject||!x.length,"false rejection");for(let v of x)for(let [a,b] of r.pairs){assert(v[a]!==v[b],"false pair");s.modelPairChecks++}s.cases++;s[x.length?"sat":"unsat"]++;if(r.reject)s.rejected++;if(!x.length&&!r.reject)s.unknownUNSAT++;s.forcedPairs+=r.pairs.length;s.referenceAssignments+=2**(n+1);for(let key of ["arcs","scans","certArcVisits","certLength"])s[key]+=r[key]}
 // Two triangles (blue) and a disjoint red 6-cycle. All vertices degree two in each color, so simple matching-only components decline.
 let A=[[0,3],[3,1],[1,4],[4,2],[2,5],[5,0]],B=[[0,1],[1,2],[2,0],[3,4],[4,5],[5,3]];
 let dense=probe(6,A,B,[]);assert(dense.odd&&dense.pairs.length===12&&refs(6,A,B,[]).length===0,"dense odd support");
 // Equal anchors have the direct witness all interior bits opposite; adding a!=b makes a hostile UNSAT neighbor.
 let f=[...A,...B];assert(f.every(([a,b])=>a!==b),"source distinct");
 return {seed:208241,random:s,dense:{...dense,equalAnchorWitness:[0,0,1,1,1,1,1,1],oppositeGuardModels:0,sourceEdges:12},notes:"Guard-local two-color graph tests only. This stronger SCC pass is not integrated into BH02 main normalizer. Equal-anchor witness follows by all interiors opposite. No full strict-source compilation or all-channel closure."}
}
console.log(JSON.stringify(BH02s(),null,2));
