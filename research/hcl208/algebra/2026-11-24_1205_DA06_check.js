/* Run: node 2026-11-24_1205_DA06_check.js */
const experiment = function experiment(){
 const L={rootClosures:0,fiberClosures:0,closureSweeps:0,edgeRowTests:0,guardRowTests:0,deletions:0,parityScans:0,connectivityScans:0,verifiedLifts:0,referenceBWords:0,assertions:0}, results={};
 function check(v){L.assertions++;if(!v)throw Error("assertion "+L.assertions)}
 function make(n,clauses,mode){
  const forms=[],edges=[];const node=(f=0)=>{forms.push(f);return forms.length-1};
  // Form 0 is constant a=0. Literal l denotes a=truth(l) in parallel;
  // series uses a=NOT truth(l) by flipping sign.
  const good=(u,v)=>edges.push([u,v,1]);
  function leaf(c,parallel){
   const s=node(),t=node();
   if(parallel){let p=s;for(const l of c){const v=node(l);good(p,v);p=v}good(p,t)}
   else for(const l of c){const v=node(-l);good(s,v);good(v,t)}
   return [s,t];
  }
  function par(cs){if(cs.length===1)return leaf(cs[0],true);const k=cs.length>>1, a=par(cs.slice(0,k)),b=par(cs.slice(k)),s=node(),t=node();for(const p of [a,b]){good(s,p[0]);good(p[1],t)}return [s,t]}
  let ends;
  if(mode==="parallel")ends=par(clauses);
  else {let first,last;for(const c of clauses){const p=leaf(c,false);if(last!==undefined)good(last,p[0]);else first=p[0];last=p[1]}ends=[first,last]}
  edges.push([ends[0],ends[1],0]);
  const degree=Array(forms.length).fill(0),keys=new Set();for(const [u,v] of edges){const key=[Math.min(u,v),Math.max(u,v)].join(",");check(u!==v&&!keys.has(key));keys.add(key);degree[u]++;degree[v]++}
  check(Math.max(...degree)<=4);
  return {n,forms,edges,ends}
 }
 const truth=(l,z)=>((z>>(Math.abs(l)-1))&1)^Number(l<0);
 const aval=(f,z)=>f===0?0:truth(f,z);
 function closure(G,z,base){
  if(z===null)L.rootClosures++;else L.fiberClosures++;
  const D=base?base.map(a=>a.slice()):G.forms.map(()=>[0,1,2,3]);
  const groups=Array.from({length:G.n},()=>[]);
  G.forms.forEach((f,v)=>{if(f)groups[Math.abs(f)-1].push(v)});
  let changed=true;
  function restrict(v,p){const old=D[v],newD=[];for(const c of old){L.guardRowTests++;if(p(c))newD.push(c)}if(newD.length!==old.length){L.deletions+=old.length-newD.length;changed=true;D[v]=newD}}
  while(changed){changed=false;L.closureSweeps++;
   for(let v=0;v<D.length;v++){const f=G.forms[v];if(!f||z!==null)restrict(v,c=>(c>>1)===aval(f,z??0))}
   if(z===null)for(const vs of groups){let possible=[0,1];for(const v of vs){const f=G.forms[v];possible=possible.filter(b=>D[v].some(c=>((c>>1)^Number(f<0))===b))}for(const v of vs)restrict(v,c=>possible.includes((c>>1)^Number(G.forms[v]<0)))}
   for(const [u,v,s] of G.edges)for(const [a,b] of [[u,v],[v,u]]){const old=D[a],next=[];for(const x of old){let ok=false;for(const y of D[b]){L.edgeRowTests++;if((x^y)!==s){ok=true;break}}if(ok)next.push(x)}if(next.length!==old.length){L.deletions+=old.length-next.length;D[a]=next;changed=true}}
   if(D.some(d=>!d.length))return null;
  }
  return D
 }
 function parity(G,z,D){
  if(!D)return null;
  const a=G.forms.map(f=>aval(f,z)),adj=a.map(()=>[]);
  for(const [u,v,s] of G.edges){L.parityScans++;if((a[u]^a[v])===(s>>1)){const q=1^(s&1);adj[u].push([v,q]);adj[v].push([u,q])}}
  const b=a.map(()=>-1);
  for(let v=0;v<b.length;v++)if(b[v]<0){b[v]=0;const Q=[v];for(let i=0;i<Q.length;i++){const u=Q[i];for(const [w,q] of adj[u]){L.parityScans++;const t=b[u]^q;if(b[w]<0){b[w]=t;Q.push(w)}else if(b[w]!==t)return null}}}
  const color=a.map((x,i)=>2*x+b[i]);check(G.edges.every(([u,v,s])=>(color[u]^color[v])!==s));check(color.every((c,i)=>D[i].includes(c)));L.verifiedLifts++;return color
 }
 function connected(G,z){
  const a=G.forms.map(f=>aval(f,z)),adj=a.map(()=>[]);
  for(let i=0;i<G.edges.length-1;i++){const [u,v]=G.edges[i];L.connectivityScans++;if(a[u]===a[v]){adj[u].push(v);adj[v].push(u)}}
  const Q=[G.ends[0]],seen=new Set(Q);for(let i=0;i<Q.length;i++)for(const v of adj[Q[i]]){L.connectivityScans++;if(!seen.has(v)){seen.add(v);Q.push(v)}}return seen.has(G.ends[1])
 }
 function brute(G,z){
  const a=G.forms.map(f=>aval(f,z));for(let b=0;b<2**a.length;b++){L.referenceBWords++;if(G.edges.every(([u,v,s])=>((2*(a[u]^a[v]))+(((b>>u)^(b>>v))&1))!==s))return true}return false
 }
 function run(n,cs,mode,words=null,br=false){
  const G=make(n,cs,mode),root=closure(G,null,null);check(root!==null);const expectedDomains=G.forms.map(f=>f?[0,1,2,3]:[0,1]);check(root.every((d,i)=>d.join()===expectedDomains[i].join()));
  let yes=0,no=0;
  for(const z of words??Array.from({length:2**n},(_,i)=>i)){
   const expected=cs.every(c=>c.some(l=>truth(l,z)));
   const D=closure(G,z,root),w=parity(G,z,D),bad=connected(G,z);
   check(Boolean(w)===!bad);check(Boolean(w)===(mode==="parallel"?expected:!expected));if(br)check(Boolean(w)===brute(G,z));if(w)yes++;else no++;
  }return {yes,no,vertices:G.forms.length,edges:G.edges.length};
 }
 const cube=Array.from({length:8},(_,i)=>[1,2,3].map((v,j)=>i>>j&1?-v:v));
 const fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]].flatMap(c=>[c,c.map(x=>-x)]);
 results.cube={};for(const mode of ["series","parallel"]){let roots=0,neighbors=0;const root=run(3,cube,mode);check(root.yes===(mode==="series"?8:0));roots++;for(let i=0;i<8;i++){const x=run(3,cube.filter((_,j)=>j!==i),mode);check(x.yes===(mode==="series"?7:1));neighbors++}results.cube[mode]={root,neighbors}}
 results.fano={};for(const mode of ["series","parallel"]){const root=run(7,fano,mode);check(root.yes===(mode==="series"?128:0));for(let i=0;i<14;i++){const x=run(7,fano.filter((_,j)=>j!==i),mode);check(x.yes===(mode==="series"?123:5))}results.fano[mode]={root,neighbors:14}}
 let seed=20806;const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 results.random={systems:0,fibers:0};for(let j=0;j<80;j++){const n=3+rand(3),m=1+rand(6),cs=[];for(let k=0;k<m;k++){const c=[];for(let t=0;t<3;t++){let v=1+rand(n);while(c.some(l=>Math.abs(l)===v))v=v%n+1;c.push(rand(2)?v:-v)}cs.push(c)}for(const mode of ["series","parallel"]){const r=run(n,cs,mode,null,m===1);results.random.systems++;results.random.fibers+=r.yes+r.no}}
 results.cover=[];for(let k=1;k<=7;k++){const cs=Array.from({length:k},(_,j)=>[2*j+1,2*j+2]);const r=run(2*k,cs,"series");check(r.no===3**k);results.cover.push({k,...r,affineMax:2**k,lower:Math.ceil((3/2)**k)})}
 results.scaling=[];for(const k of [16,64,128]){const cs=Array.from({length:k},(_,j)=>[1,2,3].map(v=>j%2?-v:v));for(const mode of ["parallel","series"])results.scaling.push({k,mode,...run(3,cs,mode)})}
 return {results,ledger:L,seed:20806}
};
console.log(JSON.stringify(experiment(),null,2));
