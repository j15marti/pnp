function audit(){
 const A=(x,m)=>{if(!x)throw Error(m)},key=(a,b)=>a<b?a+","+b:b+","+a;
 function graph(n,E){E=E.map(([u,v])=>u<v?[u,v]:[v,u]).sort((a,b)=>a[0]-b[0]||a[1]-b[1]);let adj=Array.from({length:n},()=>[]);E.forEach(([u,v],i)=>{adj[u].push([v,i]);adj[v].push([u,i])});A(adj.every(l=>l.length===3)&&new Set(E.map(e=>key(...e))).size===E.length&&E.every(([u,v])=>u!==v),"simple cubic");return {n,E,adj}}
 function expand(G){let p=new Map(),E=[];G.adj.forEach((l,v)=>{l.forEach(([u,i],k)=>p.set(v+","+i,3*v+k));E.push([3*v,3*v+1],[3*v+1,3*v+2],[3*v,3*v+2])});G.E.forEach(([u,v],i)=>E.push([p.get(u+","+i),p.get(v+","+i)]));return graph(3*G.n,E)}
 function base(G){let x=Array(G.E.length).fill(-1),nodes=0;function rec(i){nodes++;if(i===x.length)return true;let [u,v]=G.E[i],used=new Set([...G.adj[u],...G.adj[v]].map(([w,j])=>x[j]));for(let c=0;c<3;c++)if(!used.has(c)){x[i]=c;if(rec(i+1))return true;x[i]=-1}return false}return {color:rec(0)?x:null,nodes}}
 function verify(G,c){A(c.length===G.E.length&&G.adj.every(l=>new Set(l.map(([v,i])=>c[i])).size===3)&&c.every(x=>x>=0&&x<3),"coloring")}
 function solve(G,log){
  if(G.n<=10){let b=base(G);log.base={n:G.n,nodes:b.nodes,result:b.color!==null};return b.color}
  let tr=new Map();for(let u=0;u<G.n;u++){let v=G.adj[u].map(e=>e[0]);for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)if(G.adj[v[i]].some(e=>e[0]===v[j])){let t=[u,v[i],v[j]].sort((a,b)=>a-b);tr.set(t.join(","),t)}}
  let groups=[...tr.values()],part=Array(G.n).fill(-1);for(let i=0;i<groups.length;i++)for(let u of groups[i]){if(part[u]>=0)return undefined;part[u]=i}if(part.some(x=>x<0))return undefined;
  let ext=G.E.map(([u,v],i)=>[part[u],part[v],i]).filter(([u,v])=>u!==v);if(new Set(ext.map(([u,v])=>key(u,v))).size!==ext.length)return undefined;
  let H=graph(groups.length,ext.map(([u,v])=>[u,v]));log.steps.push({n:G.n,child:H.n,triangles:groups.length});let c=solve(H,log);if(!c)return c;
  let ix=new Map(H.E.map((e,i)=>[key(...e),i])),out=Array(G.E.length).fill(-1),port=Array(G.n).fill(-1);
  for(let [u,v,i] of ext){let col=c[ix.get(key(u,v))];out[i]=col;for(let w of G.E[i])port[w]=col}
  G.E.forEach(([u,v],i)=>{if(part[u]===part[v]){A(port[u]!==port[v],"triangle distinct seams");out[i]=3-port[u]-port[v]}});verify(G,out);return out;
 }
 const E=step=>[...Array.from({length:5},(_,i)=>[i,(i+1)%5]),...Array.from({length:5},(_,i)=>[i+5,(i+step)%5+5]),...Array.from({length:5},(_,i)=>[i,i+5])];
 let result=[];for(let [name,G] of [["K4",graph(4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]])],["Petersen",graph(10,E(2))],["prism",graph(10,E(1))]])for(let k=1;k<=5;k++){G=expand(G);for(let reverse of [false,true]){let H=reverse?graph(G.n,G.E.map(e=>e.map(v=>G.n-1-v))):G,log={steps:[]};let c=solve(H,log);A(c!==undefined&&(c!==null)===(name!=="Petersen"),"exact decision");if(c)verify(H,c);result.push({name,k,reverse,n:H.n,result:c!==null,...log})}}
 return result;
}
console.log(JSON.stringify(audit(),null,2));
