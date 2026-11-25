function compilerAudit(){
const assert=(x,m)=>{if(!x)throw Error(m)},key=(a,b)=>a<b?`${a},${b}`:`${b},${a}`;
function graph(n,es){let adj=Array.from({length:n},()=>[]),keys=new Set();es.forEach(([u,v],i)=>{assert(u!==v&&!keys.has(key(u,v)),"simple");keys.add(key(u,v));adj[u].push([v,i]);adj[v].push([u,i])});assert(adj.every(a=>a.length===3),"cubic");return{n,es,adj}}
function gp(n,k){return graph(2*n,Array.from({length:n},(_,i)=>[[i,(i+1)%n],[i,n+i],[n+i,n+(i+k)%n]]).flat())}
function matches(G){let a=[],u=Array(G.n).fill(false),p=[];function rec(){let v=u.indexOf(false);if(v<0){a.push(p.slice());return}u[v]=true;for(const [w,e] of G.adj[v])if(!u[w]){u[w]=true;p.push(e);rec();p.pop();u[w]=false}u[v]=false}rec();return a}
function oddness(G,M){let s=new Set(M);assert(G.adj.every(a=>a.filter(([v,e])=>s.has(e)).length===1),"matching");let seen=new Set(),odd=0;for(let v=0;v<G.n;v++)if(!seen.has(v)){let q=[v];seen.add(v);for(let i=0;i<q.length;i++)for(const [u,e] of G.adj[q[i]])if(!s.has(e)&&!seen.has(u)){seen.add(u);q.push(u)}odd+=q.length%2}return odd}
function girthAtLeast6(G){for(let v=0;v<G.n;v++){let dist=Array(G.n).fill(-1),parent=Array(G.n).fill(-1),q=[v];dist[v]=0;for(let i=0;i<q.length;i++){let a=q[i];if(dist[a]>=2)continue;for(const [b] of G.adj[a])if(dist[b]<0){dist[b]=dist[a]+1;parent[b]=a;q.push(b)}else if(parent[a]!==b&&parent[b]!==a&&dist[a]+dist[b]+1<6)return false;}for(let a of q)if(dist[a]===2)for(const [b] of G.adj[a])if(dist[b]===2)return false;}return true;}
const H=graph(14,Array.from({length:7},(_,i)=>[0,1,3].map(d=>[i,7+(i+d)%7])).flat());
const e0=0;assert(H.es[e0][0]===0&&H.es[e0][1]===7,"gadget endpoints");assert(girthAtLeast6(H),"H girth");
const colorH=H.es.map(([u,v])=>[0,1,3].indexOf((v-7-u+7)%7));assert(H.adj.every(a=>new Set(a.map(([v,e])=>colorH[e])).size===3),"H color");
function compile(G){let E=[],maps=[];G.es.forEach(([u,v],i)=>{let o=G.n+14*i,local=[];H.es.forEach(([a,b],j)=>{if(j===e0)return;local.push([j,E.length]);E.push([o+a,o+b])});let ports=[E.length,E.length+1];E.push([u,o],[v,o+7]);maps.push({local,ports})});return{graph:graph(G.n+14*G.es.length,E),maps}}
function liftM(G,C,M){let s=new Set(M),R=[];for(let i=0;i<G.es.length;i++){let {local,ports}=C.maps[i],is=s.has(i);if(is)R.push(...ports);for(const [old,e] of local)if(colorH[old]===(is?0:1))R.push(e)}return R;}
let results=[],tests=0,lifts=0;for(const [name,G] of [["prism3",gp(3,1)],["Petersen",gp(5,2)],["dodecahedron",gp(10,2)],["prism8",gp(8,1)]]){let C=compile(G);assert(girthAtLeast6(C.graph),"expanded girth");let MS=matches(G),odd=[];for(let M of MS){let old=oddness(G,M),next=oddness(C.graph,liftM(G,C,M));assert(old===next,"oddness lift");tests++;if(!old)lifts++;odd.push(old);}results.push({name,sourceVertices:G.n,compiledVertices:C.graph.n,matchings:MS.length,sourceOddnessValues:[...new Set(odd)].sort(),evenMatchingLifts:odd.filter(x=>!x).length})}
return{results,tests,lifts,templateEdges:H.es,templateColors:colorH};
}
console.log(JSON.stringify(compilerAudit(),null,2));
