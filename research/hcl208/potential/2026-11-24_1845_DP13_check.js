function run(){
const A=(x)=>{if(!x)throw Error("assertion")};
let stats={assertions:0,counts:0,slices:0,treePairs:0,closureScans:0,necessaryPins:0};
function check(x){stats.assertions++;A(x)}
const sum=a=>a.reduce((x,y)=>x+y,0n);
const dot=(a,b,w)=>sum(a.map((x,i)=>x*b[i]*w[i]));
const d=x=>x?[0n,1n]:[1n,0n], one=[1n,1n];
function rank2(a){let b=a.find(r=>r.some(x=>x!==0n));if(!b)return 0;return a.some(r=>r[0]*b[1]!==r[1]*b[0])?2:1}
function prep(n,weights,edges){
 const adj=Array.from({length:n},()=>[]);let rank1=0;
 for(let [i,e] of edges.entries()){e.id=i;e.r=Math.min(rank2(e.a),rank2(e.b));check(e.r>0);if(e.r===1){rank1++;continue}adj[e.u].push(i);adj[e.v].push(i)}
 let t=0,disc=Array(n).fill(0),low=Array(n).fill(0),stack=[],blocks=[];
 function dfs(v,p){disc[v]=low[v]=++t;for(let id of adj[v]){if(id===p)continue;let e=edges[id],u=e.u===v?e.v:e.u;if(!disc[u]){stack.push(id);dfs(u,id);low[v]=Math.min(low[v],low[u]);if(low[u]>=disc[v]){let b=[];while(true){let j=stack.pop();b.push(j);if(j===id)break}blocks.push(b)}}else if(disc[u]<disc[v]){stack.push(id);low[v]=Math.min(low[v],disc[u])}}}
 for(let v=0;v<n;v++)if(!disc[v])dfs(v,-1);
 let inc=Array.from({length:n},()=>[]), info=blocks.map((ids,b)=>{let vs=[...new Set(ids.flatMap(i=>[edges[i].u,edges[i].v]))];vs.forEach(v=>inc[v].push(b));let p=Array.from({length:n},(_,i)=>i);function f(v){while(p[v]!==v)v=p[v];return v}let tree=[],cut=[];for(let id of ids){let {u,v}=edges[id];if(f(u)===f(v))cut.push(id);else{p[f(u)]=f(v);tree.push(id)}}return {vs,tree,cut}});
 let globalSlices=info.reduce((x,b)=>x*(2n**BigInt(b.cut.length)),1n), blockSlices=sum(info.map(b=>2n**BigInt(b.cut.length)));
 return {n,weights,edges,inc,info,rank1,globalSlices,blockSlices};
}
function count(P,query={}){
 stats.counts++;
 let {n,weights,edges,inc,info}=P, base=weights.map(r=>r.slice()),den=1n;
 let w=edges.map(e=>query[e.id]||one),K=[];
 for(let e of edges){let {a,b,u,v,id,r}=e;if(r===1){let flip=rank2(a)!==1,l=flip?b:a,h=flip?a:b,i=flip?v:u,j=flip?u:v,anchor=l.find(row=>row.some(x=>x!==0n)),p=anchor[0]!==0n?0:1;den*=anchor[p];base[i]=base[i].map((x,t)=>x*l[t][p]);base[j]=base[j].map((x,t)=>x*dot(anchor,h[t],w[id]));}else K[id]=a.map(x=>b.map(y=>dot(x,y,w[id])))}
 let seen=new Set();
 function vertex(v,parent){seen.add(v);let r=base[v].slice();for(let b of inc[v])if(b!==parent){let z=block(b,v);r=r.map((x,i)=>x*z[i])}return r}
 function block(b,p){let {vs,tree,cut}=info[b],loc={};for(let v of vs)loc[v]=v===p?base[v].map(()=>1n):vertex(v,b);let adj={};vs.forEach(v=>adj[v]=[]);for(let id of tree){let e=edges[id];adj[e.u].push(id);adj[e.v].push(id)}
 let res=loc[p].map(()=>0n);let M=2**cut.length;A(Number.isSafeInteger(M)&&M<=65536);
 for(let s=0;s<M;s++){stats.slices++;let vals={};vs.forEach(v=>vals[v]=loc[v].slice());cut.forEach((id,j)=>{let e=edges[id],bit=(s>>j)&1;vals[e.u]=vals[e.u].map((x,t)=>x*e.a[t][bit]);vals[e.v]=vals[e.v].map((x,t)=>x*e.b[t][bit]*w[id][bit])});
 function rec(v,prev){let ans=vals[v].slice();for(let id of adj[v])if(id!==prev){let e=edges[id],u=e.u===v?e.v:e.u,r=rec(u,id);ans=ans.map((x,i)=>{stats.treePairs+=r.length;return x*sum(r.map((y,j)=>y*(v===e.u?K[id][i][j]:K[id][j][i])))})}return ans}
 let z=rec(p,-1);res=res.map((x,i)=>x+z[i]);}
 return res;
 }
 let z=1n;for(let v=0;v<n;v++)if(!seen.has(v))z*=sum(vertex(v,-1));check(z%den===0n);return z/den;
}
const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
function fanoNet(skip){let weights=Array.from({length:7},()=>[1n,1n]),edges=[],rep=[];fano.forEach((line,i)=>{let kinds=[-1,0,1].filter(k=>k===-1||2*i+k!==skip);weights.push(kinds.map(k=>k===-1?1n:-1n));for(let v of line){if(rep[v]===undefined)rep[v]=edges.length;edges.push({u:v,v:7+i,a:[d(0),d(1)],b:kinds.map(k=>k===-1?one:d(k))})}});return {P:prep(14,weights,edges),rep}}
function clauses(skip){return fano.flatMap((l,i)=>[0,1].filter(b=>2*i+b!==skip).map(b=>l.map(v=>[v,1-b])))}
function satisfies(x,cs){return cs.every(c=>c.some(([v,b])=>((x>>v)&1)===b))}
function closure(p,cs){p={...p};for(;;){stats.closureScans++;let change=false;for(let c of cs){if(c.some(([v,b])=>p[v]===b))continue;let free=c.filter(([v])=>p[v]===undefined);if(!free.length)return null;if(free.length===1){let [v,b]=free[0];p[v]=b;stats.necessaryPins++;change=true;break}}if(!change)return p}}
function guard(p,rep){let q={};for(let [v,b] of Object.entries(p))q[rep[v]]=d(b);return q}
let fanoRows=[];
for(let skip=-1;skip<14;skip++){
 let {P,rep}=fanoNet(skip),cs=clauses(skip),models=Array.from({length:128},(_,i)=>i).filter(x=>satisfies(x,cs)),p=closure({},cs);check(p!==null);
 let z=count(P,guard(p,rep));check(z===BigInt(models.length));check(z===(skip===-1?0n:5n));
 let witness=null, forced=[];
 if(z>0n){
  // Probe all single original coordinates under the unconditioned source.
  for(let v=0;v<7;v++){let a=count(P,{[rep[v]]:d(0)});check(a===BigInt(models.filter(x=>!(x>>v&1)).length));if(a===0n)forced.push([v,1]);if(a===z)forced.push([v,0])}
  // Guarded reconstruction, closure restarted after each chosen pin.
  for(let v=0;v<7;v++)if(p[v]===undefined){p=closure(p,cs);let trial={...p,[v]:0};let zz=count(P,guard(trial,rep));p=closure({...p,[v]:zz>0n?0:1},cs);check(p!==null)}
  witness=Object.entries(p).reduce((x,[v,b])=>x+(b<<Number(v)),0);check(satisfies(witness,cs));
 }
 // A single full original-coordinate parity scan, using character weights and exact counts.
 let affineRows=null;
 if(skip===0){affineRows=[];for(let mask=1;mask<128;mask++){let q={};for(let v=0;v<7;v++)if(mask>>v&1)q[rep[v]]=[1n,-1n];let c=count(P,q);let ref=sum(models.map(x=>{let a=x&mask,b=0;while(a){b^=1;a&=a-1}return b?-1n:1n}));check(c===ref);if(c===z||c===-z)affineRows.push([mask,c===z?0:1])}}
 fanoRows.push({skip,count:String(z),witness,forced,affineRows,blockSlices:String(P.blockSlices)});
}
function bouquet(m,odd,dense){let n=2*m+1,weights=Array.from({length:n},()=>[1n,1n]),edges=[];function add(u,v,sign){edges.push({u,v,a:[d(0),d(1)],b:[d(sign),d(1^sign)]})}
 for(let i=0;i<m;i++){let a=2*i+1,b=a+1;add(0,a,0);add(a,b,0);add(b,0,odd&&i===m-1?1:0)}
 if(dense)for(let i=1;i<n;i++)for(let j=i+1;j<n;j++)if((i-1>>1)!==(j-1>>1))edges.push({u:i,v:j,a:[d(0),d(0)],b:[d(0),d(0)]});
 return prep(n,weights,edges)}
let scale=[];for(let m of [2,8,32,64])for(let odd of [false,true]){let P=bouquet(m,odd,true),z=count(P);check(z===(odd?0n:2n));if(!odd){check(count(P,{0:d(0)})===1n);check(count(P,{0:d(1)})===1n)}scale.push({m,odd,edges:P.edges.length,rank1:P.rank1,blocks:P.info.length,globalSlices:String(P.globalSlices),blockSlices:String(P.blockSlices),count:String(z)})}
// Actual K rank can increase after a coordinate pin: h=(1,chi_y), g=(1,chi_(x+y)).
let h=[[1n,1n,1n,1n],[1n,-1n,1n,-1n]],g=[[1n,1n,1n,1n],[1n,-1n,-1n,1n]];
let k0=h.map(a=>g.map(b=>dot(a,b,[1n,1n,1n,1n]))),kp=h.map(a=>g.map(b=>dot(a,b,[1n,1n,0n,0n])));check(rank2(k0)===1&&rank2(kp)===2);
// Seeded signed-label kernel: compare exact block contraction with direct label enumeration.
let seed=1901;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}let random=[];
for(let j=0;j<60;j++){let n=3+rand(4),weights=Array.from({length:n},()=>[1n,BigInt(rand(3)-1)]),edges=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(rand(3)!==0){let f=()=>{let a=[BigInt(rand(3)-1),BigInt(rand(3)-1)];if(a.every(x=>x===0n))a[0]=1n;return a};edges.push({u,v,a:[f(),f()],b:[f(),f()]})}let P=prep(n,weights,edges),q={};for(let e of edges)if(rand(3)===0)q[e.id]=[1n,-1n];let z=count(P,q),ref=0n;for(let x=0;x<2**n;x++){let r=1n;for(let v=0;v<n;v++)r*=weights[v][x>>v&1];for(let e of edges)r*=dot(e.a[x>>e.u&1],e.b[x>>e.v&1],q[e.id]||one);ref+=r}check(z===ref);random.push({n,edges:edges.length,count:String(z)})}
return {stats,fano:fanoRows,scale,random,queryRankCounterexample:{before:k0.map(r=>r.map(String)),after:kp.map(r=>r.map(String))}};
}
console.log(JSON.stringify(run(),null,2));
