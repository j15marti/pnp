function run(){
let asserts=0,nodes=0,sweeps=0,deletions=0,rankCalls=0,xors=0,seed=20261124;
const check=(b,msg)=>{asserts++;if(!b)throw Error(msg)};
const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n};
const bit=i=>1n<<BigInt(i);
function basis(rows){rankCalls++;let a=new Map();for(let v of rows){while(v){let k=v.toString(2).length-1;if(!a.has(k)){a.set(k,v);break}v^=a.get(k);xors++}}return a}
function reduce(v,a){for(const k of [...a.keys()].sort((x,y)=>y-x))if(v&bit(k)){v^=a.get(k);xors++}return v}
function rank(rows){return basis(rows).size}
function plane(e){let [u,v]=e;return [bit(2*u)^bit(2*v),bit(2*u+1)^bit(2*v+1)]}
function kernel(planes){let rows=new Map(),deps=[],owner=[],r=0;for(let i=0;i<planes.length;i++)for(let v of planes[i]){let z=bit(owner.length);owner.push(i);while(v){let k=v.toString(2).length-1;if(!rows.has(k)){rows.set(k,[v,z]);r++;break}let [w,s]=rows.get(k);v^=w;z^=s;xors++}if(!v)deps.push(z)}
let par=planes.map((_,i)=>i);function find(x){while(par[x]!==x){par[x]=par[par[x]];x=par[x]}return x}
function support(z){let s=[];for(let i=0;i<owner.length;i++)if(z&bit(i))s.push(owner[i]);return s}
for(let z of deps){let s=support(z);for(let j of s)par[find(j)]=find(s[0])}
let groups=new Map();for(let i=0;i<planes.length;i++){let k=find(i);if(!groups.has(k))groups.set(k,{edges:[],delta:0});groups.get(k).edges.push(i)}for(let z of deps)groups.get(find(support(z)[0])).delta++;
return {r,delta:deps.length,groups:[...groups.values()]}
}
function myc(g){let {n,e}=g;return {n:2*n+1,e:[...e,...e.flatMap(([u,v])=>[[u,n+v],[v,n+u]]),...Array.from({length:n},(_,i)=>[i+n,2*n])]}}
function contract(g,j,d){let [a,b]=g.e[j];let map=[],n=0;for(let i=0;i<g.n;i++)if(i!==b)map[i]=n++;map[b]=map[a];return {n,e:g.e.filter((_,i)=>i!==j).map(([u,v])=>[map[u],map[v],u===b||v===b?d:0]),map,a,b,d}}
function solve(g){const {n,e}=g;let adj=Array.from({length:n},()=>[]);for(let [u,v,s=0] of e){adj[u].push([v,s]);adj[v].push([u,s])}
function closure(a){let changed=true;while(changed){sweeps++;changed=false;for(let u=0;u<n;u++){if(!a[u])return false;for(let [v,s] of adj[u])if((a[u]&(a[u]-1))===0){let c=31-Math.clz32(a[u]),b=a[v]&~(1<<(c^s));if(b!==a[v]){a[v]=b;deletions++;changed=true;if(!b)return false}}}}return true}
function visit(a){nodes++;if(!closure(a))return null;let u=-1,best=5;for(let i=0;i<n;i++){let k=[1,2,4,8].filter(t=>a[i]&t).length;if(k>1&&(k<best||k===best&&adj[i].length>adj[u].length)){best=k;u=i}}if(u<0)return a.map(x=>31-Math.clz32(x));for(let c=0;c<4;c++)if(a[u]&(1<<c)){let b=a.slice();b[u]=1<<c;let r=visit(b);if(r)return r}return null}
let a=Array(n).fill(15);if(!closure(a))return null;a[0]=1;return visit(a)}
function verify(g,x){return g.e.every(([u,v,s=0])=>(x[u]^x[v])!==s)}
function params(g){let ps=g.e.map(plane),k=kernel(ps),all=ps.flat();let shared=[];for(let i=0;i<ps.length;i++){let b=basis(ps.filter((_,j)=>j!==i).flat());for(let v of [ps[i][0],ps[i][1],ps[i][0]^ps[i][1]])if(reduce(v,b)===0n)shared.push(v)}return {r:k.r,delta:k.delta,components:k.groups.map(x=>[x.edges.length,x.delta]),primal:rank(shared)}}
let g=myc(myc({n:5,e:[[0,1],[1,2],[2,3],[3,4],[4,0]]}));check(!solve(g),"root UNSAT");let root=params(g),labels=[0,0,0,0],guarded;
for(let j=0;j<g.e.length;j++)for(let d=0;d<4;d++){let h=contract(g,j,d),z=solve(h);check(Boolean(z)===(d===0),"guard label");if(z){labels[d]++;let x=h.map.map((k,i)=>z[k]^(i===h.b?d:0));check((x[h.a]^x[h.b])===d&&g.e.every(([u,v],i)=>i===j||(x[u]^x[v])!==0),"original lift")}
if(d===0){let p=params(h);check(p.r===2*(h.n-1)&&p.primal===p.r&&p.delta===2*(h.e.length-h.n+1)&&p.components.length===1,"rank components");guarded=p}}
let samples=[];for(let t=0;t<48;t++){let rows=[];let p=1+t%5;for(let i=0;i<p;i++){let z=0n;if(t%2===0){for(let k=0;k<2*g.n;k++)if(rand(2))z^=bit(k)}else{for(let k=0;k<1+rand(4);k++)z^=bit(rand(2*g.n))}rows.push(z)}let b=basis(rows);let ps=g.e.map(plane),qs=ps.map(a=>a.map(v=>reduce(v,b)));let good=qs.map((a,i)=>rank(a)===2?i:-1).filter(i=>i>=0);
// This set is rank-preserving, not necessarily retained by stronger closure. Test the algebraic kernel injection only.
let old=kernel(good.map(i=>ps[i])),now=kernel(good.map(i=>qs[i]));check(now.delta>=old.delta,"nullity injection");for(let c of old.groups){let containing=now.groups.find(z=>z.edges.includes(c.edges[0]));check(c.edges.every(i=>containing.edges.includes(i))&&containing.delta>=c.delta,"support component injection")}
samples.push({guardRank:b.size,retainedRank2:good.length,oldMax:Math.max(0,...old.groups.map(c=>c.delta)),newMax:Math.max(0,...now.groups.map(c=>c.delta))})}
let forests=0,forestWords=0;for(let t=0;t<64;t++){let n=2+rand(5),e=[];for(let i=1;i<n;i++)if(rand(3))e.push([i,rand(i),rand(4)]);let graph={n,e},base=null,rows=[];for(let w=0;w<4**n;w++){forestWords++;let x=Array.from({length:n},(_,i)=>(w>>(2*i))&3);if(verify(graph,x)){let z=BigInt(w);if(base===null)base=z;rows.push(z^base)}}check(base!==null&&rank(rows)===2*n,"forest full affine hull");forests++}
let tree={n:8,e:Array.from({length:7},(_,i)=>[i,i+1])};let cycle={n:8,e:[...tree.e,[0,7]]};let treeP=params(tree),cycleP=params(cycle);check(treeP.delta===0&&treeP.primal===0&&cycleP.delta===2&&cycleP.primal===14,"tree/cycle controls");
return {seed:20261124,root:{n:g.n,m:g.e.length,...root},guarded:{n:g.n-1,m:g.e.length-1,...guarded},guardedSAT:labels.reduce((a,b)=>a+b,0),guardedUNSAT:g.e.length*4-labels.reduce((a,b)=>a+b,0),labels,arbitraryRankPreservingSamples:samples,forests,forestWords,tree:treeP,cycle:cycleP,asserts,nodes,sweeps,deletions,rankCalls,xors}
}
console.log(JSON.stringify(run(),null,2));
