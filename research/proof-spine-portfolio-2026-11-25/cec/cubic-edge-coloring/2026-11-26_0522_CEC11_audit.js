function audit(){
const assert=(x,m)=>{if(!x)throw Error(m)},edge=(a,b)=>a<b?[a,b]:[b,a],key=e=>e.join(","),make=(n,E)=>({n,E:E.map(e=>edge(...e)).sort((a,b)=>a[0]-b[0]||a[1]-b[1])});
const K=make(4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]);
function prism(step){return make(10,[...Array.from({length:5},(_,i)=>[i,(i+1)%5]),...Array.from({length:5},(_,i)=>[i+5,(i+step)%5+5]),...Array.from({length:5},(_,i)=>[i,i+5])])}
const P=prism(2),Q=prism(1);
function adj(G){let a=Array.from({length:G.n},()=>[]);G.E.forEach(([u,v],i)=>{a[u].push([v,i]);a[v].push([u,i])});return a}
function validate(G){const A=adj(G);assert(A.every(a=>a.length===3)&&new Set(G.E.map(key)).size===G.E.length&&G.E.every(([u,v])=>u!==v),"simple cubic");let seen=new Set([0]),q=[0],tin=Array(G.n).fill(-1),low=Array(G.n),clock=0,bridges=0;
 // iterative DFS, to avoid stack overflow on expanded graphs
 const stack=[[0,-1,0]];tin[0]=low[0]=clock++;
 while(stack.length){let f=stack[stack.length-1],u=f[0];if(f[2]===A[u].length){stack.pop();if(stack.length){let p=stack[stack.length-1][0];low[p]=Math.min(low[p],low[u]);if(low[u]>tin[p])bridges++}continue}
 const [v,i]=A[u][f[2]++];if(i===f[1])continue;if(tin[v]>=0){low[u]=Math.min(low[u],tin[v]);continue}tin[v]=low[v]=clock++;stack.push([v,i,0])}
 assert(clock===G.n&&!bridges,"connected bridgeless")}
function pms(G){let A=adj(G),out=[];function rec(S,m){if(!S.size){out.push(m.slice());return}let u=Math.min(...S);for(const [v,i] of A[u])if(S.has(v)){const R=new Set(S);R.delete(u);R.delete(v);rec(R,[...m,i])}}rec(new Set(Array.from({length:G.n},(_,i)=>i)),[]);return out}
function cycles(G,M){const m=new Set(M),A=adj(G),seen=new Set(),out=[];for(let i=0;i<G.n;i++)if(!seen.has(i)){let seq=[],u=i,p=-1;do{seq.push(u);seen.add(u);let [v]=A[u].find(([v,j])=>!m.has(j)&&v!==p);p=u;u=v}while(u!==i);out.push(seq)}return out}
function verifyPM(G,M){const d=Array(G.n).fill(0);for(const i of M)for(const v of G.E[i])d[v]++;assert(d.every(x=>x===1),"perfect matching")}
function defects(G,x){return G.E.map(([u,v],i)=>x[u]===x[v]?i:-1).filter(i=>i>=0)}
function testCut(G,x){
 const D=defects(G,x),free=Array(G.n).fill(true);for(const i of D){const [u,v]=G.E[i];if(!free[u]||!free[v])return {ok:false,reason:"overlap",d:D.length};free[u]=free[v]=false}
 const A=adj(G),L=Array.from({length:G.n},(_,i)=>i).filter(i=>free[i]&&x[i]===0),R=Array.from({length:G.n},(_,i)=>i).filter(i=>free[i]&&x[i]===1),mate=Array(G.n).fill(-1),mi=Array(G.n).fill(-1);
 // augment via BFS, with actual edge IDs
 for(const s of L){let q=[s],seen=new Set([s]),pred=new Map(),end=-1;for(let p=0;p<q.length&&end<0;p++){let u=q[p];for(const [v,i] of A[u])if(free[v]&&x[v]===1&&mate[u]!==v&&!pred.has(v)){pred.set(v,[u,i]);if(mate[v]<0){end=v;break}let w=mate[v];if(!seen.has(w)){seen.add(w);q.push(w)}}}if(end>=0){let v=end;while(v>=0){let [u,i]=pred.get(v),old=mate[u];mate[u]=v;mate[v]=u;mi[u]=mi[v]=i;v=old}}}
 const matched=L.filter(u=>mate[u]>=0).length;
 if(matched!==L.length||matched!==R.length){
  // Hall witness on deficient side; start with every unmatched left (or swap)
  const side=matched<L.length?0:1,roots=(side===0?L:R).filter(u=>mate[u]<0),S=new Set(roots),T=new Set(),q=roots.slice();
  for(let p=0;p<q.length;p++)for(const [v] of A[q[p]])if(free[v]&&x[v]!==side&&!T.has(v)){T.add(v);if(mate[v]>=0&&!S.has(mate[v])){S.add(mate[v]);q.push(mate[v])}}
  const actual=new Set([...S].flatMap(u=>A[u].filter(([v])=>free[v]).map(([v])=>v)));
  assert(actual.size===T.size&&[...actual].every(v=>T.has(v))&&S.size>T.size,"Hall witness");
  return {ok:false,reason:"Hall",d:D.length,side,S:[...S],T:[...T]};
 }
 const M=[...D,...L.map(u=>mi[u])];verifyPM(G,M);const C=cycles(G,M);assert(C.every(c=>c.length%2===0),"even");
 const Aids=new Map(G.E.map((e,i)=>[key(e),i])),color=Array(G.E.length).fill(-1);M.forEach(i=>color[i]=2);C.forEach(c=>c.forEach((u,j)=>color[Aids.get(key(edge(u,c[(j+1)%c.length])))]=j%2));assert(color.every(v=>v>=0)&&A.every(l=>new Set(l.map(([v,i])=>color[i])).size===3),"full source coloring");
 return {ok:true,d:D.length,M,color};
}
function expand(G){let A=adj(G),vport=new Map(),E=[];A.forEach((a,v)=>{a.forEach(([u,i],j)=>vport.set(v+","+i,3*v+j));E.push([3*v,3*v+1],[3*v+1,3*v+2],[3*v,3*v+2])});G.E.forEach(([u,v],i)=>E.push([vport.get(u+","+i),vport.get(v+","+i)]));let H=make(3*G.n,E),ix=new Map(H.E.map((e,i)=>[key(e),i]));return {H,vport,ix,A}}
function liftPM(G,X,M){let s=new Set(M),out=[];G.E.forEach(([u,v],i)=>{if(s.has(i))out.push(X.ix.get(key(edge(X.vport.get(u+","+i),X.vport.get(v+","+i)))))});
 X.A.forEach((a,v)=>{let p=a.filter(([u,i])=>!s.has(i)).map(([u,i])=>X.vport.get(v+","+i));assert(p.length===2,"liftPM");out.push(X.ix.get(key(edge(...p))))});verifyPM(X.H,out);return out}
function optimalCut(G,X,M){let x=Array(X.H.n).fill(-1),idx=new Map(G.E.map((e,i)=>[key(e),i]));function direct(u,v,i){x[X.vport.get(u+","+i)]=0;x[X.vport.get(v+","+i)]=1}cycles(G,M).forEach(c=>c.forEach((u,j)=>{let v=c[(j+1)%c.length];direct(u,v,idx.get(key(edge(u,v))))}));M.forEach(i=>direct(...G.E[i],i));assert(x.every(v=>v>=0)&&defects(X.H,x).length===G.n&&x.reduce((a,b)=>a+b,0)*2===X.H.n,"maximum cut proof");return x}
function liftCut(G,X,x,M){let m=new Set(M),y=Array(X.H.n);X.A.forEach((a,v)=>a.forEach(([u,i])=>y[X.vport.get(v+","+i)]=x[v]^+m.has(i)));return y}
function exhaustive(G){let ms=pms(G),sets=ms.map(m=>new Set(m)),even=ms.filter(m=>cycles(G,m).every(c=>c.length%2===0)),min=Infinity,balanced=0,maxCount=0,maxCompatible=0,minCompatible=null,success=0,hall=0,overlap=0,checks=0;for(let k=0;k<2**(G.n-1);k++){let x=Array.from({length:G.n},(_,i)=>k>>i&1),D=defects(G,x),r=testCut(G,x),expected=sets.some(s=>D.every(i=>s.has(i)));assert(r.ok===expected,"cut vs direct pms");checks++;if(r.ok){success++;minCompatible=minCompatible===null?D.length:Math.min(minCompatible,D.length)}else if(r.reason==="Hall")hall++;else overlap++;if(D.length<min){min=D.length;balanced=maxCount=maxCompatible=0}if(D.length===min){maxCount++;balanced+=+(x.reduce((a,b)=>a+b,0)*2===G.n);maxCompatible+=+r.ok}}
 return {n:G.n,perfectMatchings:ms.length,evenMatchings:even.length,checks,success,hall,overlap,min,maxCount,balanced,maxCompatible,minCompatible}}
let exact=[K,P,Q,expand(K).H].map(exhaustive);
assert(exact[3].min===4&&exact[3].maxCompatible===0&&exact[3].balanced===exact[3].maxCount&&exact[3].minCompatible===6,"truncated tetrahedron");
const scale=[];for(const [name,base] of [["K4",K],["Petersen",P],["prism",Q]]){
 let G=base,ms=pms(G),M=ms.find(m=>cycles(G,m).every(c=>c.length%2===0))??ms[0],positive=cycles(G,M).every(c=>c.length%2===0),x=Array(G.n).fill(-1);if(positive)cycles(G,M).forEach(c=>c.forEach((v,j)=>x[v]=j%2));for(let k=1;k<=5;k++){
  let X=expand(G),opt=optimalCut(G,X,M),bad=testCut(X.H,opt);validate(X.H);assert(!bad.ok&&bad.reason==="Hall","max cut fails");let row={name,k,n:X.H.n,minDefects:bad.d,maxCutHall:[bad.S.length,bad.T.length],compatibleDefects:null};
  if(positive){let y=liftCut(G,X,x,M),r=testCut(X.H,y);assert(r.ok,"compatible lift");row.compatibleDefects=r.d;row.coloredEdges=r.color.length;x=y}
  M=liftPM(G,X,M);G=X.H;scale.push(row);
 }
}
return {exact,scale,fixtureEdges:expand(K).H.E};
}
console.log(JSON.stringify(audit(),null,2));
