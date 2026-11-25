function audit(){
const assert=(x,m)=>{if(!x)throw Error(m)};
const key=(a,b)=>a<b?`${a},${b}`:`${b},${a}`;
function graph(n,E){let es=[...new Set(E.map(([a,b])=>key(a,b)))].map(s=>s.split(",").map(Number)),adj=Array.from({length:n},()=>[]);es.forEach(([a,b],i)=>{adj[a].push([b,i]);adj[b].push([a,i]);});assert(adj.every(a=>a.length===3),"cubic");return {n,es,adj};}
function gp(n,k){return graph(2*n,Array.from({length:n},(_,i)=>[[i,(i+1)%n],[i,n+i],[n+i,n+(i+k)%n]]).flat());}
function prism(n){return gp(n,1)}
function matchings(G){let out=[],used=Array(G.n).fill(false),cur=[];function rec(){let v=used.indexOf(false);if(v<0){out.push(cur.slice().sort((a,b)=>a-b));return}used[v]=true;for(const [u,e] of G.adj[v])if(!used[u]){used[u]=true;cur.push(e);rec();cur.pop();used[u]=false}used[v]=false}rec();return out;}
function comps(G,es){let a=Array.from({length:G.n},()=>[]);for(const e of es){let [u,v]=G.es[e];a[u].push(v);a[v].push(u)}let id=Array(G.n).fill(-1),sizes=[];for(let v=0;v<G.n;v++)if(id[v]<0){let q=[v];id[v]=sizes.length;for(let i=0;i<q.length;i++)for(let u of a[q[i]])if(id[u]<0){id[u]=id[v];q.push(u)}sizes.push(q.length)}return {id,sizes}}
function complement(G,M){let s=new Set(M);return G.es.map((_,i)=>i).filter(e=>!s.has(e))}
function even(G,M){return comps(G,complement(G,M)).sizes.every(s=>s%2===0)}
function cyclesDiff(G,M,Q){let a=new Set(M),b=new Set(Q),d=G.es.map((_,i)=>i).filter(e=>a.has(e)!==b.has(e));let {id}=comps(G,d), groups=new Map();for(let e of d){let c=id[G.es[e][0]];if(!groups.has(c))groups.set(c,[]);groups.get(c).push(e)}return [...groups.values()].sort((a,b)=>a[0]-b[0]);}
function flip(M,C){let s=new Set(M);for(let e of C){if(s.has(e))s.delete(e);else s.add(e)}return [...s].sort((a,b)=>a-b)}
function parity(G,M,squares){let fixed=new Set(M);for(let C of squares)for(let e of C)fixed.delete(e);return comps(G,G.es.map((_,i)=>i).filter(e=>!fixed.has(e))).sizes.every(s=>s%2===0)}
function solve(G,M,squares){if(!parity(G,M,squares))return null;let R=M.slice();while(true){let {id}=comps(G,complement(G,R));let C=squares.find(C=>new Set(C.flatMap(e=>G.es[e]).map(v=>id[v])).size>1);if(!C){assert(even(G,R),"parity invariant");return R}let before=comps(G,complement(G,R)).sizes.length;R=flip(R,C);assert(comps(G,complement(G,R)).sizes.length===before-1,"merge");}}
function brute(G,M,C){for(let b=0;b<2**C.length;b++){let R=M;for(let i=0;i<C.length;i++)if((b>>i)&1)R=flip(R,C[i]);if(even(G,R))return true}return false}
function verifyColor(G,M){let col=Array(G.es.length).fill(-1);for(let e of M)col[e]=0;let rem=complement(G,M);for(let root of rem)if(col[root]<0){let [v,u]=G.es[root],e=root,c=1;while(col[e]<0){col[e]=c;let [w,ne]=G.adj[u].find(([w,ne])=>ne!==e&&col[ne]!==0);v=u;u=w;e=ne;c=3-c}assert(e===root&&c===1,"cycle alternation")}assert(G.adj.every(a=>new Set(a.map(([v,e])=>col[e])).size===3),"color verification")}
let data=[], checks=0,guardChecks=0, lifts=0, longCounter=null, localCounter=null, girthCounter=null;
let graphs=[["K4",graph(4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]])],["K3,3",graph(6,[0,1,2].flatMap(a=>[3,4,5].map(b=>[a,b])))],...Array.from({length:6},(_,i)=>[`prism${i+3}`,prism(i+3)]),["Petersen",gp(5,2)],["dodecahedral",gp(10,2)],["G(7,2)",gp(7,2)],["G(8,3)",gp(8,3)]];
for(let [name,G] of graphs){let MS=matchings(G), good=MS.filter(M=>even(G,M));let cnt=0,succ=0,maxSq=0;for(let i=0;i<MS.length;i++){let M=MS[i],odd=comps(G,complement(G,M)).sizes.filter(s=>s%2).length;let sqMap=new Map(),neighbors=[];for(let j=0;j<MS.length;j++){let Q=MS[j],C=cyclesDiff(G,M,Q);if(C.length===1){neighbors.push(Q);if(C[0].length===4)sqMap.set(C[0].join(","),C[0]);if(!longCounter&&C[0].length>4&&parity(G,M,C)&&!brute(G,M,C))longCounter={name,edges:G.es,M,Q,cycles:C,hostSizes:comps(G,G.es.map((_,i)=>i).filter(e=>!M.includes(e)||C[0].includes(e))).sizes,complementM:comps(G,complement(G,M)).sizes,complementQ:comps(G,complement(G,Q)).sizes};}}
if(good.length&&odd>0&&!sqMap.size&&!girthCounter)girthCounter={name,edges:G.es,M,good:good[0],complement:comps(G,complement(G,M)).sizes};
if(good.length&&odd>0&&!localCounter&&neighbors.every(Q=>comps(G,complement(G,Q)).sizes.filter(s=>s%2).length>=odd))localCounter={name,edges:G.es,M,good:good[0],odd,neighbors:neighbors.length};
let sq=[...sqMap.values()];function rec(idx,pack,used){if(idx===sq.length){cnt++;checks++;maxSq=Math.max(maxSq,pack.length);let expected=brute(G,M,pack),result=solve(G,M,pack);assert(Boolean(result)===expected,"square chart");if(result){succ++;lifts++;verifyColor(G,result)}for(let C of pack){let others=pack.filter(D=>D!==C);for(let z=0;z<2;z++){let R=z?flip(M,C):M;assert(parity(G,R,others)===brute(G,R,others),"guard");guardChecks++}}return}rec(idx+1,pack,used);let C=sq[idx],vs=new Set(C.flatMap(e=>G.es[e]));if([...vs].every(v=>!used.has(v)))rec(idx+1,[...pack,C],new Set([...used,...vs]));}rec(0,[],new Set());}
data.push({name,vertices:G.n,matchings:MS.length,evenMatchings:good.length,charts:cnt,satisfiableCharts:succ,maxSquares:maxSq});}
return {data,checks,guardChecks,lifts,longCounter,localCounter,girthCounter};
}
console.log(JSON.stringify(audit(),null,2));
