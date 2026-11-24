'use strict';
function run(){
 const stats={seed:2080955,roots:[],neighborChecks:0,sat:0,unsat:0,searchNodes:0,closurePasses:0,domainDeletions:0,sourceEdgeChecks:0,smallSubsetChecks:0,neighborhoodChecks:0,exactTwRuns:0,twStates:0,affineRankChecks:0,affineGuardCases:0,randomHosts:0,randomCriticalRoots:0};
 let seed=stats.seed;function rnd(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296}
 function assert(x,s){if(!x)throw Error(s)}
 function graph(n,e){const adj=Array.from({length:n},()=>[]);for(const [a,b] of e){adj[a].push(b);adj[b].push(a)}return {n,e,adj}}
 function solve(G){let {n,e,adj}=G;
  function close(d){while(true){stats.closurePasses++;let changed=false;for(let u=0;u<n;u++){let a=d[u];if(!a)return false;if(a&(a-1))continue;for(const v of adj[u])if(d[v]&a){d[v]&=~a;stats.domainDeletions++;if(!d[v])return false;changed=true;break}if(changed)break}if(!changed)return true}}
  function go(d){stats.searchNodes++;if(!close(d))return null;let u=-1,bc=5,bd=-1;for(let i=0;i<n;i++){let c=0;for(let t=d[i];t;t&=t-1)c++;if(c>1&&(c<bc||c===bc&&adj[i].length>bd)){u=i;bc=c;bd=adj[i].length}}if(u<0)return d.map(x=>Math.log2(x));if(!close(d))return null;for(let t=d[u];t;t&=t-1){const z=d.slice();z[u]=t&-t;const a=go(z);if(a)return a}return null}
  const d=Array(n).fill(15);if(!close(d))return null; // unconditional root
  if(n)d[0]=1; // exact global color translation gauge
  const a=go(d);if(a)for(const [u,v] of e){stats.sourceEdgeChecks++;assert(a[u]!==a[v],"bad lift")}return a
 }
 function compact(G){const keep=G.adj.map((a,i)=>a.length?i:-1).filter(i=>i>=0),idx=new Map(keep.map((v,i)=>[v,i]));return graph(keep.length,G.e.map(([a,b])=>[idx.get(a),idx.get(b)]))}
 function critical(G){if(solve(G))return null;let e=G.e.slice();for(let j=0;j<e.length;){const q=e.filter((_,i)=>i!==j);if(!solve(graph(G.n,q)))e=q;else j++}return compact(graph(G.n,e))}
 function cycle(n){return graph(n,Array.from({length:n},(_,i)=>[i,(i+1)%n]))}
 function myc(G){const {n,e}=G;return graph(2*n+1,[...e,...e.flatMap(([a,b])=>[[a,b+n],[b,a+n]]),...Array.from({length:n},(_,i)=>[i+n,2*n])])}
 function girth(G){let best=Infinity;for(let s=0;s<G.n;s++){const d=Array(G.n).fill(-1),p=Array(G.n).fill(-1),q=[s];d[s]=0;for(let j=0;j<q.length;j++){let u=q[j];for(let v of G.adj[u]){if(d[v]<0){d[v]=d[u]+1;p[v]=u;q.push(v)}else if(p[u]!==v&&p[v]!==u)best=Math.min(best,d[u]+d[v]+1)}}}return best}
 function columns(G){const {n,e}=G,p=Array(n).fill(-1),pe=Array(n).fill(-1),q=[0],tree=new Set(),adj=Array.from({length:n},()=>[]);e.forEach(([a,b],i)=>{adj[a].push([b,i]);adj[b].push([a,i])});p[0]=0;for(let j=0;j<q.length;j++)for(const [v,i] of adj[q[j]])if(p[v]<0){p[v]=q[j];pe[v]=i;tree.add(i);q.push(v)}assert(q.length===n,"disconnected");let C=e.map(()=>0n),b=0;for(let i=0;i<e.length;i++)if(!tree.has(i)){let bit=1n<<BigInt(b++);C[i]^=bit;for(let u=e[i][0];u!==0;u=p[u])C[pe[u]]^=bit;for(let u=e[i][1];u!==0;u=p[u])C[pe[u]]^=bit}return [C,b]}
 function rank(vs){stats.affineRankChecks++;const B=new Map();for(let x of vs)while(x){let k=x.toString(2).length;if(B.has(k))x^=B.get(k);else{B.set(k,x);break}}return B.size}
 function affine(G,g){const [C,b]=columns(G);assert(rank(C)===b,"root rank");for(let z=0;z<Math.min(5,G.e.length);z++){const p=Math.min(g-2,z%3);const chosen=new Set();while(chosen.size<p)chosen.add(Math.floor(rnd()*C.length));for(let j=0;j<C.length;j++)if(!chosen.has(j)){assert(rank(C.filter((_,i)=>!chosen.has(i)&&i!==j))===b,"guarded affine support rank");stats.affineGuardCases++}}}
 function pop(x){let n=0;for(;x;x&=x-1)n++;return n}
 function tw(G){const {n,adj}=G;assert(n<=12,"tw test bound");stats.exactTwRuns++;const A=adj.map(a=>a.reduce((s,i)=>s|(1<<i),0)),full=(1<<n)-1,dp=new Uint8Array(1<<n);dp.fill(255);dp[0]=0;for(let S=0;S<full;S++){stats.twStates++;for(let r=full^S;r;r&=r-1){let v=31-Math.clz32(r&-r),N=A[v],seen=0,front=N&S;while(front){let bit=front&-front;front^=bit;if(seen&bit)continue;seen|=bit;let u=31-Math.clz32(bit);N|=A[u];front|=A[u]&S&~seen}const d=pop(N&~S&~(1<<v)),t=S|(1<<v);dp[t]=Math.min(dp[t],Math.max(dp[S],d))}}return dp[full]}
 function local(G,limit){const {n,adj,e}=G,A=adj.map(a=>a.reduce((s,i)=>s|(1<<i),0));let firstBad=null,largestSparse=0,checks=0,nb=0;function visit(mask,k){let ec=0,N=0;for(let t=mask;t;t&=t-1){let v=31-Math.clz32(t&-t);ec+=pop(A[v]&mask);N|=A[v]}ec/=2;checks++;if(2*ec>=3*k&&firstBad===null)firstBad=k;let U=mask,Nout=N&~U;let union=U|Nout;let ec2=0;for(let t=union;t;t&=t-1){let v=31-Math.clz32(t&-t);ec2+=pop(A[v]&union)}if(Math.min(...adj.map(a=>a.length))>=4&&ec2<3*pop(union)){nb++;assert(3*pop(Nout)>k,"small set boundary inequality")}}
 function rec(start,mask,left,k){if(!left){visit(mask,k);return}for(let i=start;i<=n-left;i++)rec(i+1,mask|(1<<i),left-1,k)}
 for(let k=1;k<=limit;k++){rec(0,0,k,k);if(firstBad===null)largestSparse=k}
 stats.smallSubsetChecks+=checks;stats.neighborhoodChecks+=nb;return {largestSparse,firstBad,checks,nb}}
 function control(name,G,all){const n=G.n,m=G.e.length,g=girth(G),d=Math.min(...G.adj.map(a=>a.length));assert(!solve(G),"root SAT");stats.unsat++;assert(d>=4,"critical minimum degree");const l=local(G,Math.min(5,n)),w=n<=12?tw(G):null; if(w!==null)assert(w+1>=Math.floor(l.largestSparse/2)/6,"width lower");
 affine(G,g);let ws=[];let ids=all?G.e.map((_,i)=>i):[0,Math.floor(m/3),Math.floor(2*m/3),m-1];for(let i of ids){const J=graph(n,G.e.filter((_,j)=>i!==j));assert(solve(J),"neighbor UNSAT");stats.sat++;stats.neighborChecks++;if(n<=12){let z=tw(J);assert(z>=w-1,"edge deletion width");ws.push(z)}if(i===ids[0]||i===ids[ids.length-1])affine(J,girth(J))}
 stats.roots.push({name,n,m,girth:g,minDegree:d,maxDegree:Math.max(...G.adj.map(a=>a.length)),neighbors:ids.length,local:l,exactTreewidth:w,neighborWidthRange:ws.length?[Math.min(...ws),Math.max(...ws)]:null})}
 const k5=graph(5,Array.from({length:5},(_,i)=>Array.from({length:i},(_,j)=>[j,i])).flat());control("K5",k5,true);
 control("Mycielski twice C5",myc(myc(cycle(5))),true);
 // New larger control: exact criticalization, then verify selected deletion neighbors.
 const large=critical(myc(myc(cycle(7))));assert(large,"C7 Mycielski root");control("criticalized twice-Mycielski C7",large,false);
 for(let z=0;z<16;z++){let n=10+(z%3),e=[];for(let i=0;i<n;i++)for(let j=0;j<i;j++)if(rnd()<0.58)e.push([j,i]);stats.randomHosts++;let H=critical(graph(n,e));if(H){stats.randomCriticalRoots++;control("random critical "+z,H,false)}}
 return stats
}
console.log(JSON.stringify(run(),null,2));
