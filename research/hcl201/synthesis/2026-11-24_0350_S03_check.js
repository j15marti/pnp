const experiment = function experiment(){
 const assert=(x,m)=>{if(!x)throw Error(m)};
 const mk=(n,edges)=>{const adj=Array.from({length:n},()=>new Set());for(const [u,v] of edges){assert(u!==v,"loop");adj[u].add(v);adj[v].add(u)}return adj};
 const edges=g=>g.flatMap((s,u)=>[...s].filter(v=>v>u).map(v=>[u,v]));
 const valid=(g,x)=>x!==null&&x.length===g.length&&x.every(c=>[1,2,3].includes(c))&&edges(g).every(([u,v])=>x[u]!==x[v]);
 const subset=(a,b)=>[...a].every(x=>b.has(x));
 const inter=(a,b)=>new Set([...a].filter(x=>b.has(x)));
 const induced=(g,B)=>{const bs=new Set(B);return g.map(s=>inter(s,bs))};
 function cert(g,a,B){
  const bs=new Set(B), P=g.map((_,v)=>v).filter(v=>v!==a&&!bs.has(v));if(P.some(p=>P.some(q=>g[p].has(q))))return null;
  const bg=induced(g,B), A=[...g[a]], p=new Map(), T=new Set();
  for(const v of B){const w=A.find(w=>subset(bg[v],bg[w]));if(w!==undefined){p.set(v,w);T.add(v)}}
  const r=new Map(B.map(v=>[v,v]));for(const w of P){const v=B.find(v=>(!g[a].has(w)||T.has(v))&&subset(bg[w],bg[v]));if(v===undefined)return null;r.set(w,v)}
  if(!A.every(w=>T.has(r.get(w))))return null;
  assert(edges(g).filter(([u,v])=>u!==a&&v!==a).every(([u,v])=>bg[r.get(u)].has(r.get(v))),"retraction");
  return {a,B,bs,P,bg,T,p,r};
 }
 function brute(g,allowed){
  let c=Array(g.length).fill(0);
  function dfs(){let v=-1,d=null;for(let u=0;u<g.length;u++)if(!c[u]){let a=allowed[u].filter(k=>![...g[u]].some(w=>c[w]===k));if(!a.length)return false;if(d===null||a.length<d.length){v=u;d=a}}if(v<0)return true;for(const k of d){c[v]=k;if(dfs())return true}c[v]=0;return false}
  return dfs()?c:null;
 }
 function bip(bg,verts,removed){const c=Array(bg.length).fill(0);for(const v of verts){if(removed.has(v)||c[v])continue;c[v]=1;const q=[v];for(let j=0;j<q.length;j++){const u=q[j];for(const w of bg[u]){if(removed.has(w))continue;if(!c[w]){c[w]=3-c[u];q.push(w)}else if(c[w]===c[u])return null}}}return c}
 function solve(g,a,B){
  const z=cert(g,a,B);if(!z)return {recognized:false};const {bg,T,r}=z,U=B.filter(v=>!T.has(v)), us=new Set(U), C=new Set();
  for(const u of U)for(const v of bg[u])if(us.has(v)&&!C.has(u)&&!C.has(v)){C.add(u);C.add(v)}
  const cv=[...C];let visits=0,why="",bc=null;
  function lift(c){const x=g.map((_,i)=>i===a?3:c[r.get(i)]);assert(valid(g,x),"invalid lift");return x}
  // Unconditional terminal closure: induced restricted core must be bipartite; all-binary witness is enough.
  if(!bip(bg,B,us)){why="restricted-core-odd";return {recognized:true,x:null,k:cv.length,u:U.length,visits,why,z}}
  bc=bip(bg,B,new Set());if(bc){why="binary";return {recognized:true,x:lift(bc),k:cv.length,u:U.length,visits,why,z}}
  function rec(i,K){
   if(i===cv.length){visits++;const I=new Set(K);for(const u of U)if(!C.has(u)&&![...bg[u]].some(v=>K.has(v)))I.add(u);
    assert([...I].every(u=>![...bg[u]].some(v=>I.has(v))),"not independent");
    const c=bip(bg,B,I);if(!c)return null;for(const u of I)c[u]=3;return lift(c)}
   let x=rec(i+1,K);if(x)return x;const v=cv[i];if(![...bg[v]].some(w=>K.has(w))){K.add(v);x=rec(i+1,K);K.delete(v)}return x;
  }
  const x=rec(0,new Set());return {recognized:true,x,k:cv.length,u:U.length,visits,why:"cover",z};
 }
 function forward(g,z,x){const c=x.slice();for(const v of z.T)if(x[v]===3)c[v]=x[z.p.get(v)];assert([...z.T].every(v=>c[v]!==3),"forward list");assert(z.B.every(v=>[...z.bg[v]].every(w=>c[v]!==c[w])),"forward edges");return c}
 function tagged(g,x){let s=0n;const es=edges(g);for(let j=0;j<es.length;j++){const [u,v]=es[j],d=x[u]^x[v];assert(d>0&&d<=3,"tag nonzero");s^=BigInt(x[u])<<BigInt(2*j);s^=BigInt(x[v])<<BigInt(2*j);s^=BigInt(d)<<BigInt(2*j)}
 // Each nonzero choice corresponds to one of three K4 perfect matchings, star neighbor = value.
 assert(s===0n,"tag target");return g.length+es.length;
 }
 function make(n,be,T,extra=[]){const bg=mk(n,be);const E=be.slice();const a=2*n+extra.length;for(let v=0;v<n;v++){for(const w of bg[v])E.push([n+v,w]);if(T.has(v))E.push([a,n+v])}for(let j=0;j<extra.length;j++){const [v,ns,anchor]=extra[j];for(const w of ns)E.push([2*n+j,w]);if(anchor)E.push([a,2*n+j])}return {g:mk(a+1,E),a,B:Array.from({length:n},(_,i)=>i)}}
 let seed=20261124;const rand=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)/4294967296};
 const stats={exhaustive:0,random:0,sat:0,unsat:0,forward:0,taggedFactors:0,coverLeaves:0,independentU:0,scale:[],negative:[]};
 function test(n,be,T,extra,kind){const {g,a,B}=make(n,be,T,extra), out=solve(g,a,B);assert(out.recognized,"recognition");const ref=brute(g,g.map((_,v)=>v===a?[3]:[1,2,3]));
  const bg=mk(n,be), base=brute(bg,bg.map((_,v)=>T.has(v)?[1,2]:[1,2,3]));
  // Extra auxiliaries are constrained to be retraction-compatible with the original T.
  assert(!!out.x===!!ref&&!!ref===!!base,"decision disagreement");if(ref){forward(g,out.z,ref);stats.forward++;stats.taggedFactors+=tagged(g,out.x);stats.sat++}else stats.unsat++;
  stats[kind]++;stats.coverLeaves+=out.visits;if(out.k===0)stats.independentU++;
 }
 for(let n=1;n<=4;n++){const all=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)all.push([u,v]);for(let mask=0;mask<2**all.length;mask++){const be=all.filter((_,j)=>mask>>j&1);for(let t=0;t<2**n;t++)test(n,be,new Set(Array.from({length:n},(_,i)=>i).filter(i=>t>>i&1)),[],"exhaustive")}}
 for(let i=0;i<160;i++){const n=3+Math.floor(rand()*5),be=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(rand()<.36)be.push([u,v]);const T=new Set(Array.from({length:n},(_,i)=>i).filter(()=>rand()<.6)),bg=mk(n,be),extra=[];for(let j=0;j<3;j++){const v=Math.floor(rand()*n);extra.push([v,[...bg[v]].filter(()=>rand()<.6),T.has(v)&&rand()<.5])}test(n,be,T,extra,"random")}
 // RT03 grid paired controls, with source certificate B and anchor. Two more controls with many free independent vertices.
 for(const s of [3,4,6,8,12,16,32]){const n=s*s,be=[];for(let i=0;i<s;i++)for(let j=0;j<s;j++){const v=i*s+j;if(i+1<s)be.push([v,v+s]);if(j+1<s)be.push([v,v+1])}be.push([0,2*s+2]);
  const many=Array.from({length:n},(_,v)=>v).filter(v=>(Math.floor(v/s)+v%s)%2===0&&v!==2*s+2);
  const far=many.filter(v=>v!==0&&v!==2&&v!==2*s&&v!==2*s+2); // retain odd cycle 0,1,2,s+2,2s+2
  for(const [kind,U,expect] of [["full",[],false],["one-hole",[0],true],["many-free-sat",many,true],["many-free-unsat",far,false]]){
   const us=new Set(U),T=new Set(Array.from({length:n},(_,i)=>i).filter(v=>!us.has(v))),{g,a,B}=make(n,be,T);
   const out=solve(g,a,B);assert(out.recognized&&!!out.x===expect,"scaling");
   if(out.x)tagged(g,out.x);stats.scale.push({s,kind,vertices:g.length,edges:edges(g).length,original_free:U.length,recognized_free:out.u,cover:out.k,coverLeaves:out.visits,sat:!!out.x,why:out.why})
  }
 }
 // Missing one necessary shadow edge can invalidate the necessary reduction; verify actual counterexample.
 const bad=make(3,[[0,1],[1,2],[0,2]],new Set([0,1,2]));bad.g[3].delete(1);bad.g[1].delete(3);
 assert(cert(bad.g,bad.a,bad.B)===null || !cert(bad.g,bad.a,bad.B).T.has(0),"unverified shadow accepted");
 assert(!!brute(bad.g,bad.g.map((_,v)=>v===bad.a?[3]:[1,2,3])),"negative should be SAT");
 stats.negative.push("triangle, missing cross-edge: full base two-color reduction invalid; source SAT");
 // No lift certificate: extra edges create K4 on auxiliary vertices; B bipartite and forward necessity alone not sufficient.
 const ng=mk(7,[[0,1],[2,1],[3,0],[6,2],[6,3],[2,3],[2,4],[2,5],[3,4],[3,5],[4,5]]);
 assert(cert(ng,6,[0,1])===null&&!brute(ng,ng.map((_,v)=>v===6?[3]:[1,2,3])),"negative lift");
 stats.negative.push("bipartite base plus auxiliary K4: forward-only inference cannot certify SAT");
 return stats;
};
console.log(JSON.stringify(experiment(), null, 2));
