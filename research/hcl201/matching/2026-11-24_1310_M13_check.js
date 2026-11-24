// M13 exact BigInt double-cover and clipped S12 graph test. Node >=18.
const assert=(p,msg='assertion')=>{if(!p)throw Error(msg)};
const abs=x=>x<0n?-x:x;
const min=(a,b)=>a<b?a:b,max=(a,b)=>a>b?a:b;
const floor=(a,b)=>a>=0n?a/b:-((-a+b-1n)/b),ceil=(a,b)=>-floor(-a,b);
let stats={random:0,sat:0,unsat:0,lpInfeasible:0,lpFeasibleIntegerUnsat:0,flowAugments:0,matchingCalls:0,referenceWords:0,verifiedLifts:0,fiberChecks:0,closureUpdates:0,closureScans:0,peakGraphVertices:0,peakGraphEdges:0,strictClipCases:0,scales:[]};
function mul(cols,x,n){let b=Array(n).fill(0n);cols.forEach((c,j)=>c.forEach(([i,s])=>b[i]+=BigInt(s)*x[j]));return b}
function eq(a,b){return a.every((v,i)=>v===b[i])}
function dot(a,b){return a.reduce((v,x,i)=>v+x*b[i],0n)}
function valid(cols,b,l,u,x){return x.every((a,i)=>a>=l[i]&&a<=u[i])&&eq(mul(cols,x,b.length),b)}
function close(cols,b,L,U){
 let l=L.slice(),u=U.slice(),m=l.length;
 let A=b.map((_,i)=>cols.map(c=>BigInt(c.reduce((v,[r,s])=>v+(r===i?s:0),0))));
 restart:while(true){stats.closureScans++;
 if(l.some((v,j)=>v>u[j]))return null;
 for(let i=0;i<b.length;i++){
  let a=A[i],lo=a.map((v,j)=>min(v*l[j],v*u[j])),hi=a.map((v,j)=>max(v*l[j],v*u[j]));
  let Ls=lo.reduce((s,v)=>s+v,0n),Us=hi.reduce((s,v)=>s+v,0n);
  if(b[i]<Ls||b[i]>Us)return null;
  let rhs=b[i],g=0n;
  for(let j=0;j<m;j++){if(l[j]===u[j])rhs-=a[j]*l[j];else if(a[j])g=g===0n?abs(a[j]):min(g,abs(a[j]));}
  if(g&&rhs%g!==0n)return null;
  for(let j=0;j<m;j++)if(a[j]){
   let p=b[i]-(Us-hi[j]),q=b[i]-(Ls-lo[j]),v=a[j];
   if(v<0n){[p,q]=[-q,-p];v=-v}
   let nl=max(l[j],ceil(p,v)),nu=min(u[j],floor(q,v));
   if(nl>nu)return null;
   if(nl!==l[j]||nu!==u[j]){l[j]=nl;u[j]=nu;stats.closureUpdates++;continue restart;}
  }
 }return [l,u]}
}
// Exact min-cost double cover via negative-edge presaturation + shortest augmentations.
// This test backend is NOT claimed polynomial in binary capacity; theorem uses standard polynomial min-cost flow.
function anchor(cols,b,l,u,w){
 let n=b.length,m=l.length,R=2*n,S=R+1,T=R+2,V=T+1,g=Array.from({length:V},()=>[]);
 let shifted=mul(cols,l,n),need=Array(V).fill(0n);
 for(let i=0;i<n;i++){need[2*i]=b[i]-shifted[i];need[2*i+1]=-need[2*i]}
 function add(a,b,cap,cost,init=0n){
  assert(a!==b);let e={to:b,rev:g[b].length,cap:cap-init,cost},r={to:a,rev:g[a].length,cap:init,cost:-cost};g[a].push(e);g[b].push(r);return r
 }
 let pair=[],zero=[];
 function arc(a,b,cap,cost){let f=cost<0n?cap:0n;need[a]+=f;need[b]-=f;return add(a,b,cap,cost,f)}
 let node=(i,s)=>2*i+(s===1?0:1);
 for(let j=0;j<m;j++){
  let c=cols[j],cap=u[j]-l[j],cost=w[j];
  if(c.length===0){pair.push(null);zero.push(cost<0n?2n*u[j]:2n*l[j]);continue}
  if(c.length===1){let [i,s]=c[0];pair.push([arc(R,node(i,s),cap,cost),arc(node(i,-s),R,cap,cost)])}
  else{let [[i,s],[k,t]]=c;pair.push([arc(node(k,-t),node(i,s),cap,cost),arc(node(i,-s),node(k,t),cap,cost)])}
  zero.push(null)
 }
 let total=0n;for(let i=0;i<=R;i++){if(need[i]<0n){add(S,i,-need[i],0n);total-=need[i]}else if(need[i]>0n)add(i,T,need[i],0n)}
 while(total>0n){
  let d=Array(V).fill(null),par=Array(V).fill(null);d[S]=0n;
  for(let k=0;k<V-1;k++){let changed=false;for(let i=0;i<V;i++)if(d[i]!==null)for(let j=0;j<g[i].length;j++){let e=g[i][j];if(e.cap>0n&&(d[e.to]===null||d[e.to]>d[i]+e.cost)){d[e.to]=d[i]+e.cost;par[e.to]=[i,j];changed=true}}if(!changed)break}
  if(d[T]===null)return null;
  let v=T,amt=total,k=0;while(v!==S){assert(par[v]&&k++<V,'predecessor cycle');let [i,j]=par[v];amt=min(amt,g[i][j].cap);v=i}
  v=T;while(v!==S){let [i,j]=par[v],e=g[i][j];e.cap-=amt;g[v][e.rev].cap+=amt;v=i}
  total-=amt;stats.flowAugments++
 }
 // Independent optimality check: no negative residual cycle (all-source Bellman-Ford).
 let d=Array(V).fill(0n);for(let k=0;k<V;k++){let ch=false;for(let i=0;i<=R;i++)for(let e of g[i])if(e.to<=R&&e.cap>0n&&d[e.to]>d[i]+e.cost){d[e.to]=d[i]+e.cost;ch=true}if(!ch)break;assert(k<V-1,'negative residual cycle')}
 let x2=pair.map((p,j)=>p?2n*l[j]+p[0].cap+p[1].cap:zero[j]);assert(valid(cols,b.map(v=>2n*v),l.map(v=>2n*v),u.map(v=>2n*v),x2),'anchor');return x2
}
// Edmonds cardinality blossom; simple graph, all vertices required.
function blossom(g){
 let n=g.length,match=Array(n).fill(-1),p,base,used,flower;
 function lca(a,b){let seen=Array(n).fill(false);while(true){a=base[a];seen[a]=true;if(match[a]<0)break;a=p[match[a]]}while(true){b=base[b];if(seen[b])return b;b=p[match[b]]}}
 function mark(v,b,ch){while(base[v]!==b){flower[base[v]]=flower[base[match[v]]]=true;p[v]=ch;ch=match[v];v=p[match[v]]}}
 function find(root){used=Array(n).fill(false);p=Array(n).fill(-1);base=Array.from({length:n},(_,i)=>i);let q=[root];used[root]=true;
 for(let h=0;h<q.length;h++){let v=q[h];for(let u of g[v]){
  if(base[v]===base[u]||match[v]===u)continue;
  if(u===root||(match[u]>=0&&p[match[u]]>=0)){
   let b=lca(v,u);flower=Array(n).fill(false);mark(v,b,u);mark(u,b,v);
   for(let i=0;i<n;i++)if(flower[base[i]]){base[i]=b;if(!used[i]){used[i]=true;q.push(i)}}
  }else if(p[u]<0){p[u]=v;if(match[u]<0)return u;u=match[u];used[u]=true;q.push(u)}
 }}return -1}
 for(let i=0;i<n;i++)if(match[i]<0){let v=find(i);while(v>=0){let pv=p[v],nv=pv<0?-1:match[pv];match[v]=pv;if(pv>=0)match[pv]=v;v=nv}}
 return match
}
function clip(l,u,x2,r){let L=l.map((v,j)=>max(v,floor(x2[j],2n)-r)),U=u.map((v,j)=>min(v,ceil(x2[j],2n)+r));return [L,U]}
function matching(cols,b,l,u){
 let m=l.length,n=b.length,off=mul(cols,l,n),k=b.map((v,i)=>v-off[i]),copies=[],occ=Array(n).fill(0);
 for(let j=0;j<m;j++)for(let h=0n;h<u[j]-l[j];h++){
  if(!cols[j].length)continue;
  copies.push([j,cols[j]]);for(let [i,s] of cols[j]){occ[i]++;if(s<0)k[i]++}
 }
 if(k.some((v,i)=>v<0n||v>BigInt(occ[i])))return null;
 let g=[],optional=[],records=[];function vertex(){g.push([]);return g.length-1}
 function edge(a,b){g[a].push(b);g[b].push(a)}
 let slots=k.map(v=>Array.from({length:Number(v)},vertex)),slotSet=new Set(slots.flat());
 for(let [j,c] of copies){
  let ports=c.map(([i,s])=>{let p=vertex();for(let a of slots[i])edge(p,a);return p});
  records.push([j,ports[0],c[0][1]]);
  if(c.length===1){let a=vertex();optional.push(a);edge(ports[0],a)}
  else if(c[0][1]===c[1][1])edge(...ports);
  else{let a=vertex();edge(ports[0],a);edge(ports[1],a)}
 }
 if(g.length%2)optional.push(vertex());
 for(let i=0;i<optional.length;i++)for(let j=0;j<i;j++)edge(optional[i],optional[j]);
 stats.matchingCalls++;stats.peakGraphVertices=Math.max(stats.peakGraphVertices,g.length);stats.peakGraphEdges=Math.max(stats.peakGraphEdges,g.reduce((s,v)=>s+v.length,0)/2);
 let mat=blossom(g);if(mat.some(v=>v<0))return null;
 let x=l.slice();for(let [j,p,s] of records){let active=slotSet.has(mat[p]);if(s===1?active:!active)x[j]++}
 assert(valid(cols,b,l,u,x),'matching lift');stats.verifiedLifts++;return x
}
function solve(cols,b,L,U){
 let C=close(cols,b,L,U);if(!C)return null;let [l,u]=C;
 let a=anchor(cols,b,l,u,l.map(()=>0n));if(!a){stats.lpInfeasible++;return null}
 let [lo,hi]=clip(l,u,a,8n*BigInt(l.length));if(lo.some((v,j)=>v>l[j]||hi[j]<u[j]))stats.strictClipCases++;
 let x=matching(cols,b,lo,hi);if(!x)stats.lpFeasibleIntegerUnsat++;return x
}
function enumerate(cols,b,l,u,w,half=false){
 let m=l.length, x=l.slice(),out=new Map(),best=null;
 function rec(j){if(j===m){stats.referenceWords++;if(!eq(mul(cols,x,b.length),b))return;let c=dot(w,x);if(best===null||c<best)best=c;let key=x.map(v=>String((v%2n+2n)%2n)).join('');if(!out.has(key)||c<out.get(key))out.set(key,c);return}
 for(let v=l[j];v<=u[j];v++){x[j]=v;rec(j+1)}}
 rec(0);return {best,out}
}
let seed=1302026;function rnd(k){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%k}
for(let it=0;it<100;it++){
 let n=2+rnd(3),m=2+rnd(4),cols=[];
 for(let j=0;j<m;j++){let len=rnd(3),c=[];for(let h=0;h<len;h++)c.push([rnd(n),rnd(2)?1:-1]);if(c.length===2&&c[0][0]===c[1][0]&&c[0][1]!==c[1][1])c=[];cols.push(c)}
 let l=cols.map(()=>BigInt(rnd(3)-1)),u=l.map(v=>v+BigInt(rnd(3))),w=cols.map(()=>BigInt(rnd(7)-3));
 let x=l.map((v,j)=>v+BigInt(rnd(Number(u[j]-v+1n)))),b=mul(cols,x,n);
 if(it%2)b[rnd(n)]+=1n;
 let ref=enumerate(cols,b,l,u,w),y=solve(cols,b,l,u);
 stats.random++;if(ref.best===null)stats.unsat++;else stats.sat++;
 assert((y===null)===(ref.best===null),'decision mismatch');
 let a=anchor(cols,b,l,u,w),half=enumerate(cols,b.map(v=>2n*v),l.map(v=>2n*v),u.map(v=>2n*v),w);
 assert((a===null)===(half.best===null),'half existence');if(!a)continue;
 assert(dot(w,a)===half.best,'weighted anchor');
 let [lo,hi]=clip(l,u,a,8n*BigInt(m)),cl=enumerate(cols,b,lo,hi,w);
 assert(cl.out.size===ref.out.size,'fiber count');for(let [p,v] of ref.out){assert(cl.out.get(p)===v,'weighted fiber mismatch');stats.fiberChecks++}
}
// A genuinely shrinking weighted-fiber control, x+y=1000.
{
 let c=[[[0,1]],[[0,1]]],b=[1000n],l=[0n,0n],u=[1000n,1000n],w=[1n,0n];
 let a=anchor(c,b,l,u,w),[L,U]=clip(l,u,a,16n),ref=new Map();
 for(let x=0n;x<=1000n;x++){let key=String(x%2n)+String((1000n-x)%2n);if(!ref.has(key))ref.set(key,x)}
 let cl=enumerate(c,b,L,U,w);
 assert(U[0]<u[0]&&L[1]>l[1]);for(let [p,v] of ref){assert(cl.out.get(p)===v);stats.fiberChecks++}
 assert(valid(c,b,l,u,[1000n,0n])&&1000n>U[0]); // clipping is NOT unconditional identity or domain preservation
}
for(let bits of [16,64,128,256,512]){
 let L=1n<<BigInt(bits-1),c=[[[0,1],[1,1]],[[1,1],[2,1]],[[2,1],[0,1]]],lo=[0n,0n,0n],up=[4n*L,4n*L,4n*L];
 let b=[2n*L+1n,2n*L+1n,2n*L+1n],a=anchor(c,b,lo,up,[0n,0n,0n]);assert(a&&a.every(v=>v===2n*L+1n));
 assert(solve(c,b,lo,up)===null,'odd triangle');let s=b.slice();s[0]++;let x=solve(c,s,lo,up);assert(x&&valid(c,s,lo,up,x),'even neighbor');
 stats.scales.push({magnitudeBits:bits,unsat:'UNSAT',neighbor:'SAT',anchor2:a.map(String),witness:x.map(String)});
}
console.log(JSON.stringify(stats,null,2));
