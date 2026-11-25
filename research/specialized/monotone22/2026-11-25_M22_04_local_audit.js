// Dependency-free Node.js. Source fixtures copied from M22-02 audit; seed 20261125.
const U=[[-193,-196,-198],[194,196,197],[1,2,197],[-2,-3,-194],[-2,-4,-194],[-3,-5,-6],[-4,-5,-6],[5,7,8],[6,7,8],[-7,-18,-19],[-7,-20,-21],[-8,-18,-19],[-8,-20,-21],[3,9,10],[3,11,12],[4,13,14],[4,15,16],[9,12,15],[10,13,17],[11,16,17],[-9,-13,-16],[-9,-14,-17],[-10,-11,-14],[-10,-12,-16],[-11,-13,-15],[-12,-15,-17],[2,24,32],[18,23,25],[18,28,29],[19,23,25],[19,28,29],[20,22,26],[20,30,31],[21,22,31],[21,26,27],[24,27,30],[-1,-22,-23],[-1,-24,-25],[-22,-25,-32],[-23,-24,-26],[-26,-28,-30],[-27,-28,-31],[-27,-29,-31],[-29,-30,-32],[33,34,196],[-34,-35,-195],[-34,-36,-198],[-35,-37,-38],[-36,-37,-38],[37,39,40],[38,39,40],[-39,-50,-51],[-39,-52,-53],[-40,-50,-51],[-40,-52,-53],[35,41,42],[35,43,44],[36,45,46],[36,47,48],[41,44,47],[42,45,49],[43,48,49],[-41,-45,-48],[-41,-46,-49],[-42,-43,-46],[-42,-44,-48],[-43,-45,-47],[-44,-47,-49],[34,56,64],[50,55,57],[50,60,61],[51,55,57],[51,60,61],[52,54,58],[52,62,63],[53,54,63],[53,58,59],[56,59,62],[-33,-54,-55],[-33,-56,-57],[-54,-57,-64],[-55,-56,-58],[-58,-60,-62],[-59,-60,-63],[-59,-61,-63],[-61,-62,-64],[65,66,193],[-66,-67,-195],[-66,-68,-197],[-67,-69,-70],[-68,-69,-70],[69,71,72],[70,71,72],[-71,-82,-83],[-71,-84,-85],[-72,-82,-83],[-72,-84,-85],[67,73,74],[67,75,76],[68,77,78],[68,79,80],[73,76,79],[74,77,81],[75,80,81],[-73,-77,-80],[-73,-78,-81],[-74,-75,-78],[-74,-76,-80],[-75,-77,-79],[-76,-79,-81],[66,88,96],[82,87,89],[82,92,93],[83,87,89],[83,92,93],[84,86,90],[84,94,95],[85,86,95],[85,90,91],[88,91,94],[-65,-86,-87],[-65,-88,-89],[-86,-89,-96],[-87,-88,-90],[-90,-92,-94],[-91,-92,-95],[-91,-93,-95],[-93,-94,-96],[-97,-98,-197],[98,99,195],[98,100,195],[99,101,102],[100,101,102],[-101,-103,-104],[-102,-103,-104],[103,114,115],[103,116,117],[104,114,115],[104,116,117],[-99,-105,-106],[-99,-107,-108],[-100,-109,-110],[-100,-111,-112],[-105,-108,-111],[-106,-109,-113],[-107,-112,-113],[105,109,112],[105,110,113],[106,107,110],[106,108,112],[107,109,111],[108,111,113],[-98,-120,-128],[-114,-119,-121],[-114,-124,-125],[-115,-119,-121],[-115,-124,-125],[-116,-118,-122],[-116,-126,-127],[-117,-118,-127],[-117,-122,-123],[-120,-123,-126],[97,118,119],[97,120,121],[118,121,128],[119,120,122],[122,124,126],[123,124,127],[123,125,127],[125,126,128],[-129,-130,-196],[130,131,193],[130,132,194],[131,133,134],[132,133,134],[-133,-135,-136],[-134,-135,-136],[135,146,147],[135,148,149],[136,146,147],[136,148,149],[-131,-137,-138],[-131,-139,-140],[-132,-141,-142],[-132,-143,-144],[-137,-140,-143],[-138,-141,-145],[-139,-144,-145],[137,141,144],[137,142,145],[138,139,142],[138,140,144],[139,141,143],[140,143,145],[-130,-152,-160],[-146,-151,-153],[-146,-156,-157],[-147,-151,-153],[-147,-156,-157],[-148,-150,-154],[-148,-158,-159],[-149,-150,-159],[-149,-154,-155],[-152,-155,-158],[129,150,151],[129,152,153],[150,153,160],[151,152,154],[154,156,158],[155,156,159],[155,157,159],[157,158,160],[-161,-162,-193],[162,163,198],[162,164,198],[163,165,166],[164,165,166],[-165,-167,-168],[-166,-167,-168],[167,178,179],[167,180,181],[168,178,179],[168,180,181],[-163,-169,-170],[-163,-171,-172],[-164,-173,-174],[-164,-175,-176],[-169,-172,-175],[-170,-173,-177],[-171,-176,-177],[169,173,176],[169,174,177],[170,171,174],[170,172,176],[171,173,175],[172,175,177],[-162,-184,-192],[-178,-183,-185],[-178,-188,-189],[-179,-183,-185],[-179,-188,-189],[-180,-182,-186],[-180,-190,-191],[-181,-182,-191],[-181,-186,-187],[-184,-187,-190],[161,182,183],[161,184,185],[182,185,192],[183,184,186],[186,188,190],[187,188,191],[187,189,191],[189,190,192],[1,33,65],[-97,-129,-161],[5,37,69],[-101,-133,-165],[6,38,70],[-102,-134,-166],[14,46,78],[-110,-142,-174],[32,64,96],[-128,-160,-192]];
const W="001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101";
function audit(U,W){
const assert=(b,m)=>{if(!b)throw Error(m)};
const X=[[2,6,11],[3,8,9],[3,7,9],[4,5,10],[1,5,10],[1,2,7],[4,8,12],[6,11,12],[-1,-10,-12],[-2,-6,-11],[-6,-7,-9],[-4,-5,-10],[-1,-3,-4],[-8,-11,-12],[-5,-7,-9],[-2,-3,-8]];
const Y=[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]];
const V=U.map(c=>c.slice());[V[2][2],V[44][2]]=[V[44][2],V[2][2]];
const sat=(F,x)=>F.every(c=>c.some(l=>x[Math.abs(l)-1]===Number(l>0)));
function compile(F,n){
const inc=Array.from({length:n},()=>[]),keys=new Set();assert(F.length*3===4*n,"clause count");
F.forEach((c,i)=>{assert(c.length===3&&new Set(c.map(Math.abs)).size===3&&c.every(l=>Number.isInteger(l)&&l&&Math.abs(l)<=n&&Math.sign(l)===Math.sign(c[0])),"grammar");const k=c.slice().sort((a,b)=>a-b).join();assert(!keys.has(k),"duplicate");keys.add(k);for(const l of c)inc[Math.abs(l)-1].push(i)});
for(const cs of inc)assert(cs.length===4&&cs.filter(i=>F[i][0]>0).length===2,"multiplicity");return inc
}
function up(F,p,n){const a=p.slice();while(true){let change=false;for(const c of F){let yes=false,k=0,last=0;for(const l of c){const x=a[Math.abs(l)-1];if(x===Number(l>0)){yes=true;break}if(x===-1){k++;last=l}}if(yes)continue;if(k===0)return null;if(k===1){a[Math.abs(last)-1]=Number(last>0);change=true}}if(!change)return a}}
function closure(F,p,n,S){let a=up(F,p,n);while(a){let change=false;for(let v=0;v<n;v++)if(a[v]===-1){for(let b=0;b<2;b++){const q=a.slice();q[v]=b;S.probes++;if(!up(F,q,n)){a[v]=1-b;S.forces++;a=up(F,a,n);change=true;break}}if(change)break}if(!change)return a}return null}
function stats(){return {probes:0,forces:0,matchCalls:0,patternQueries:0,rounds:0,allowedQueries:0,majorityTests:0,componentCount:0,matroidExchangeChecks:0,matroidIndependenceQueries:0,matroidAugments:0}}
/* Standard Edmonds augmenting-path blossom search on simple adjacency.
   Edge IDs retained by wrapper, including parallel choices. */
function blossom(g){
const n=g.length,match=Array(n).fill(-1);
function search(root){
 const p=Array(n).fill(-1),base=Array.from({length:n},(_,i)=>i),used=Array(n).fill(false),q=[root];used[root]=true;
 function lca(a,b){const u=Array(n).fill(false);while(true){a=base[a];u[a]=true;if(match[a]===-1)break;a=p[match[a]]}while(true){b=base[b];if(u[b])return b;b=p[match[b]]}}
 function mark(v,b,c,flag){while(base[v]!==b){flag[base[v]]=flag[base[match[v]]]=true;p[v]=c;c=match[v];v=p[match[v]]}}
 for(let h=0;h<q.length;h++){const v=q[h];for(const u of g[v]){if(base[v]===base[u]||match[v]===u)continue;
 if(u===root||(match[u]!==-1&&p[match[u]]!==-1)){const b=lca(v,u),flag=Array(n).fill(false);mark(v,b,u,flag);mark(u,b,v,flag);for(let i=0;i<n;i++)if(flag[base[i]]){base[i]=b;if(!used[i]){used[i]=true;q.push(i)}}}
 else if(p[u]===-1){p[u]=v;if(match[u]===-1){let z=u;while(z!==-1){const w=p[z],next=w===-1?-1:match[w];match[z]=w;if(w!==-1)match[w]=z;z=next}return true}const w=match[u];used[w]=true;q.push(w)}
 }}return false
}
for(let i=0;i<n;i++)if(match[i]===-1)search(i);
return match
}
function pm(vertices,edges,force,ban,S){
 S.matchCalls++;const removed=new Set(),forced=new Set(force),banned=new Set(ban),byId=new Map(edges.map(e=>[e.id,e]));
 for(const id of forced){const e=byId.get(id);if(!e||banned.has(id)||removed.has(e.a)||removed.has(e.b))return null;removed.add(e.a);removed.add(e.b)}
 const rem=vertices.filter(v=>!removed.has(v));if(rem.length%2)return null;const pos=new Map(rem.map((v,i)=>[v,i])),g=rem.map(()=>[]),ids=new Map();
 for(const e of edges){if(banned.has(e.id)||removed.has(e.a)||removed.has(e.b))continue;const i=pos.get(e.a),j=pos.get(e.b);assert(i!==undefined&&j!==undefined&&i!==j,"edge endpoints");const key=Math.min(i,j)+":"+Math.max(i,j);if(!ids.has(key)){g[i].push(j);g[j].push(i);ids.set(key,e.id)}}
 const M=blossom(g);if(M.some(v=>v<0))return null;const out=[...forced];for(let i=0;i<M.length;i++){assert(M[M[i]]===i,"symmetric");if(i<M[i])out.push(ids.get(i+":"+M[i]))}
 const seen=new Set();for(const id of out){const e=byId.get(id);assert(e&&!banned.has(id)&&!seen.has(e.a)&&!seen.has(e.b),"matching verification");seen.add(e.a);seen.add(e.b)}assert(seen.size===vertices.length,"perfect");return out
}
function graph(F,n,inc,D,p){
const ds=new Set(D),m=F.length,vertices=Array.from({length:m},(_,i)=>i),edges=[],pairIds=[];
for(const v of D){for(let s=0;s<2;s++){const e=inc[v].filter(i=>Number(F[i][0]>0)===s);const id=2*v+s;pairIds.push(id);if(p[v]===-1||p[v]===s)edges.push({id,a:e[0],b:e[1],v,s,pair:true})}}
let id=2*n;for(let v=0;v<n;v++)if(!ds.has(v)){vertices.push(m+v);for(const i of inc[v]){const s=Number(F[i][0]>0);if(p[v]===-1||p[v]===s)edges.push({id:id++,a:i,b:m+v,v,s,pair:false})}}
return {vertices,edges,pairIds}
}
function ref(F,n,inc,D){
 for(let mask=0;mask<2**D.length;mask++){
 const dc=new Set(),ds=new Set(D);let ok=true;for(let i=0;i<D.length;i++){const v=D[i],s=(mask>>i)&1;for(const c of inc[v].filter(i=>Number(F[i][0]>0)===s)){if(dc.has(c))ok=false;dc.add(c)}}if(!ok)continue;
 const match=Array(n).fill(-1);
 function dfs(c,seen){for(const l of F[c]){const v=Math.abs(l)-1;if(ds.has(v)||seen.has(v))continue;seen.add(v);if(match[v]===-1||dfs(match[v],seen)){match[v]=c;return true}}return false}
 if(F.every((_,i)=>dc.has(i)||dfs(i,new Set())))return true
 }return false
}
function combinations(n,k,fn){const a=[];function go(i){if(a.length===k){fn(a.slice());return}for(let j=i;j<=n-(k-a.length);j++){a.push(j);go(j+1);a.pop()}}go(0)}
function normalize(F,n,inc,x){assert(sat(F,x),"seed");const r=F.map(c=>Math.abs(c.find(l=>x[Math.abs(l)-1]===Number(l>0)))-1);
 while(true){const cnt=Array(n).fill(0);r.forEach(v=>cnt[v]++);const root=cnt.indexOf(0);if(root<0)return cnt.map((c,v)=>c===2?v:-1).filter(v=>v>=0);
 const q=[root],seen=new Set(q),par=new Map();let end=null;for(let i=0;i<q.length&&!end;i++){const v=q[i];for(const c of inc[v]){const w=r[c];if(cnt[w]===2){end=[v,c];break}if(!seen.has(w)){seen.add(w);q.push(w);par.set(w,[v,c])}}}assert(end,"normalize");let [v,c]=end;while(true){r[c]=v;if(v===root)break;[v,c]=par.get(v)}
 }}
function greedy(F,n,inc){const D=[],cs=new Set();for(let v=0;v<n;v++){for(let s=0;s<2;s++){const e=inc[v].filter(i=>Number(F[i][0]>0)===s);if(e.some(i=>cs.has(i)))continue;D.push(v);e.forEach(i=>cs.add(i));break}if(D.length===n/3)return D}throw Error("greedy")}

// M22-04: conservative cycle-space syndrome hull + actual-witness lower hull.
// Exact Lovasz backend is a theorem import; not implemented here.
function bit(i){return 1n<<BigInt(i)}
function add(B,x){for(const [p,y] of B)if(x&bit(p))x^=y;if(!x)return false;let p=x.toString(2).length-1;B.set(p,x);return true}
function reduce(B,x){for(const [p,y] of B)if(x&bit(p))x^=y;return x}
function rank(B){return B.size}
function pivots(B){return [...B.keys()]}
function syndrome(M,emap,dp){let z=0n;for(const id of M){const e=emap.get(id);if(e.pair)z^=bit(dp.get(e.v))}return z}
function upperHull(G,A,D){
 // Column elimination with incidence equations and per-component fixed edge-count parity.
 // Every difference of actual perfect matchings is in this kernel.
 const dp=new Map(D.map((v,i)=>[v,i])), vp=new Map(G.vertices.map((v,i)=>[v,i]));
 const par=G.vertices.map((_,i)=>i);function root(i){while(par[i]!==i)i=par[i];return i}
 for(const e of A){const a=root(vp.get(e.a)),b=root(vp.get(e.b));if(a!==b)par[b]=a}
 const aux=new Map(),B=new Map();let offset=G.vertices.length;
 const cp=new Map(),qp=new Map();for(let i=0;i<par.length;i++){const r=root(i);if(!cp.has(r)){cp.set(r,offset++);qp.set(r,offset++)}}
 for(const e of A){const a=vp.get(e.a),b=vp.get(e.b),r=root(a);let x=bit(a)^bit(b)^bit(cp.get(r)),z=e.pair?bit(dp.get(e.v)):0n;if(e.pair)x^=bit(qp.get(r));
 for(const [p,[y,t]] of aux)if(x&bit(p)){x^=y;z^=t}
 if(x){aux.set(x.toString(2).length-1,[x,z])}else add(B,z)
 }return B
}
function stat(){return {...stats(),rankCalls:0,basisBranches:0,referencePatterns:0,referenceQueries:0}}
function prep(F,n,inc,D,p,S){
 p=p.slice();let G,A,M,lower;
 while(true){S.rounds++;p=closure(F,p,n,S);if(!p)return null;
 G=graph(F,n,inc,D,p);M=pm(G.vertices,G.edges,[],[],S);if(!M)return null;
 const emap=new Map(G.edges.map(e=>[e.id,e])),dp=new Map(D.map((v,i)=>[v,i]));const z=syndrome(M,emap,dp);
 A=[];lower=new Map();const used=new Set(M);
 for(const e of G.edges){S.allowedQueries++;const Q=used.has(e.id)?M:pm(G.vertices,G.edges,[e.id],[],S);if(Q){A.push(e);add(lower,syndrome(Q,emap,dp)^z)}}
 const allowed=new Set(A.map(e=>e.id));let change=false;
 for(const v of D){const a=allowed.has(2*v),b=allowed.has(2*v+1);if(!a&&!b)return null;if(a!==b&&p[v]===-1){p[v]=Number(b);change=true}}
 if(!change)return {G,A,M,p,lower,z,dp,emap}
 }}
function lift(F,n,D,p,R,M){const x=Array(n).fill(-1);for(const id of M){const e=R.emap.get(id);assert(e&&x[e.v]===-1,"label unique");x[e.v]=e.s}assert(x.every(v=>v>=0)&&sat(F,x)&&p.every((v,i)=>v===-1||x[i]===v),"lift");return x}
function solveRank(F,n,inc,D,p,cap,S){
 const R=prep(F,n,inc,D,p,S);if(!R)return {status:"NO",why:"matching/guard"};
 const {G,A,M,lower,z,dp,emap}=R;const target=(1n<<BigInt(D.length))-1n, delta=target^z;
 const B=upperHull(G,A,D);S.rankCalls++;for(const t of lower.values())assert(!reduce(B,t),"lower subset upper");
 const info={upper:rank(B),lower:rank(lower),certified:rank(B)===rank(lower),hull:!reduce(B,delta)};
 if(!info.hull)return {status:"NO",why:"syndrome exclusion",...info};
 if(!delta)return {status:"YES",why:"anchor",x:lift(F,n,D,R.p,R,M),...info};
 if(rank(B)>cap)return {status:"UNKNOWN",why:"rank cap",...info};
 // Pivot coordinates separate the whole upper affine hull. Enforce odd parity only there.
 const P=pivots(B),allowed=new Set(A.map(e=>e.id));
 function walk(i,f,b){if(i===P.length){S.basisBranches++;const Q=pm(G.vertices,A,f,b,S);if(!Q)return null;assert(syndrome(Q,emap,dp)===target,"rank lift");return lift(F,n,D,R.p,R,Q)}
 const v=D[P[i]];for(let s=0;s<2;s++){const e=2*v+s;if(!allowed.has(e))continue;const q=walk(i+1,f.concat([e]),b.concat([e^1]));if(q)return q}return null}
 const x=walk(0,[],[]);return x?{status:"YES",why:"rank basis",x,...info}:{status:"NO",why:"rank basis exhausted",...info}
}
function exactSmallHull(F,n,inc,D,p,S){
 const R=prep(F,n,inc,D,p,S);if(!R)return null;
 const {G,A,M,dp,emap,z}=R,ids=A.filter(e=>e.pair).map(e=>e.id),Q=new Map(),B=new Map(),target=(1n<<BigInt(D.length))-1n;
 // Exponential reference only: enumerate all realized edge-indicator patterns, not all matchings.
 function go(i,f,b){if(i===ids.length){S.referencePatterns++;let v=syndrome(f,emap,dp);Q.set(v.toString(),v);add(B,v^z);return}
 for(let k=0;k<2;k++){const ff=k?f.concat([ids[i]]):f,bb=k?b:b.concat([ids[i]]);S.referenceQueries++;if(pm(G.vertices,A,ff,bb,S))go(i+1,ff,bb)}}
 go(0,[],[]);const U=upperHull(G,A,D);assert([...B.values()].every(v=>!reduce(U,v)),"exact subset");
 return {actual:Q.has(target.toString()),hull:!reduce(B,target^z),rank:rank(B),upper:rank(U),lower:rank(R.lower),syndromes:[...Q.keys()].sort(),z:z.toString()}
}
function small(F,n){const inc=compile(F,n),S=stat(),p=closure(F,Array(n).fill(-1),n,S);assert(p,"root");
 const out={tracks:0,yes:0,no:0,unknown:0,exactRanks:{},upperRanks:{},sandwichExact:0,spuriousHulls:0,hullExample:null,rankSavings:0,initialNo:0,stats:S};
 combinations(n,n/3,D=>{const truth=ref(F,n,inc,D);const R=solveRank(F,n,inc,D,p,8,S);assert(R.status!=="UNKNOWN"&&(R.status==="YES")===truth,"rank reference mismatch");
 out.tracks++;out[R.status.toLowerCase()]++;
 const E=exactSmallHull(F,n,inc,D,p,S);if(!E){out.initialNo++;assert(!truth,"initial no");return}
 assert(E.actual===truth,"exact hull reference");out.exactRanks[E.rank]=(out.exactRanks[E.rank]||0)+1;out.upperRanks[E.upper]=(out.upperRanks[E.upper]||0)+1;
 if(E.lower===E.upper)out.sandwichExact++;if(E.upper<D.length)out.rankSavings++;
 if(E.hull&&!E.actual){out.spuriousHulls++;if(!out.hullExample)out.hullExample={D,E}}
 });return out}

function localPortfolio(F,n,inc,D,p,cap,S){
 const R=prep(F,n,inc,D,p,S);if(!R)return {status:"NO",why:"guard/matching"};
 const {G,A,dp,emap}=R,target=(1n<<BigInt(D.length))-1n;
 const adj=new Map(G.vertices.map(v=>[v,[]]));for(const e of A){adj.get(e.a).push(e.b);adj.get(e.b).push(e.a)}
 const seen=new Set(),parts=[];for(const v of G.vertices)if(!seen.has(v)){const q=[v];seen.add(v);for(let i=0;i<q.length;i++)for(const w of adj.get(q[i]))if(!seen.has(w)){seen.add(w);q.push(w)}const vs=new Set(q);parts.push({vertices:q,edges:A.filter(e=>vs.has(e.a))})}
 const tables=[],details=[];
 for(const P of parts){
 const M=pm(P.vertices,P.edges,[],[],S);assert(M,"component");const z=syndrome(M,emap,dp),B=upperHull(P,P.edges,D),r=B.size;
 if(r>cap){details.push({vertices:P.vertices.length,rank:r,capped:true});continue}
 const piv=pivots(B),table=new Map();
 function go(i,f,b){if(i===piv.length){S.basisBranches++;const Q=pm(P.vertices,P.edges,f,b,S);if(Q){const y=syndrome(Q,emap,dp);table.set(y.toString(),Q)}return}
 const ids=P.edges.filter(e=>e.pair&&e.v===D[piv[i]]).map(e=>e.id);assert(ids.length<=2,"two local edges");
 for(let mask=0;mask<2**ids.length;mask++)go(i+1,f.concat(ids.filter((_,j)=>mask&(1<<j))),b.concat(ids.filter((_,j)=>!(mask&(1<<j)))))}
 go(0,[],[]);assert(table.size>0&&table.has(z.toString()),"local complete");
 const H=new Map();for(const y of table.keys())add(H,BigInt(y)^z);
 assert(H.size<=r,"actual rank");
 const affine=BigInt(table.size)===(1n<<BigInt(H.size));
 tables.push({z,H,affine,table});details.push({vertices:P.vertices.length,rank:r,actualRank:H.size,syndromes:table.size,affine});
 }
 if(details.some(d=>d.capped))return {status:"UNKNOWN",why:"local rank cap",details};
 const affine=tables.filter(t=>t.affine),non=tables.filter(t=>!t.affine);
 const k=non.reduce((s,t)=>s+t.H.size,0);
 if(k>12)return {status:"UNKNOWN",why:"nonaffine combination cap",details,k};
 const origin=affine.reduce((s,t)=>s^t.z,0n),vectors=affine.flatMap((t,i)=>[...t.H.values()].map(v=>({v,i})));
 const B=new Map();for(let i=0;i<vectors.length;i++){let z=vectors[i].v,c=bit(i);for(const [p,[y,d]] of B)if(z&bit(p)){z^=y;c^=d}if(z)B.set(z.toString(2).length-1,[z,c])}
 function combine(want){let x=want^origin,c=0n;for(const [p,[y,d]] of B)if(x&bit(p)){x^=y;c^=d}if(x)return null;const z=affine.map(t=>t.z);for(let i=0;i<vectors.length;i++)if(c&bit(i))z[vectors[i].i]^=vectors[i].v;return z.map((v,i)=>{const M=affine[i].table.get(v.toString());assert(M,"affine preimage");return M})}
 function choose(i,z,M){if(i===non.length){const Q=combine(target^z);return Q?M.concat(Q.flat()):null}for(const [y,N] of non[i].table){const Q=choose(i+1,z^BigInt(y),M.concat(N));if(Q)return Q}return null}
 const M=choose(0,0n,[]);if(!M)return {status:"NO",why:"exact syndrome join",details,k};
 assert(syndrome(M,emap,dp)===target,"target");return {status:"YES",why:"exact syndrome join",x:lift(F,n,D,R.p,R,M),details,k}
}
function localSmall(F,n){const inc=compile(F,n),S=stat(),p=closure(F,Array(n).fill(-1),n,S);const out={yes:0,no:0,unknown:0,allAffine:0,nonaffine:0,example:null,maxRank:0,stats:S};combinations(n,n/3,D=>{const r=localPortfolio(F,n,inc,D,p,8,S),t=ref(F,n,inc,D);assert(r.status!=="UNKNOWN"&&(r.status==="YES")===t,"local reference");out[r.status.toLowerCase()]++;if(r.details){out.maxRank=Math.max(out.maxRank,...r.details.map(d=>d.rank));if(r.details.every(d=>d.affine))out.allAffine++;else{out.nonaffine++;if(!out.example)out.example={D,r}}}});return out}
const sy=localSmall(Y,6),sx=localSmall(X,12),K={"F":[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[7,8,9],[7,10,11],[8,10,12],[9,11,12],[13,14,15],[13,16,17],[14,16,18],[15,17,18],[-1,-7,-12],[-1,-18,-7],[-2,-9,-18],[-2,-15,-9],[-3,-8,-15],[-3,-10,-8],[-4,-17,-10],[-4,-11,-17],[-5,-16,-11],[-5,-14,-16],[-6,-13,-14],[-6,-12,-13]],"D":[0,1,2,3,4,5]};
const sk=stat(),ik=compile(K.F,18),pk=closure(K.F,Array(18).fill(-1),18,sk),rk=localPortfolio(K.F,18,ik,K.D,pk,8,sk);
assert(rk.status==="YES","K4");
const iv=compile(V,198),sv=stat(),rv=closure(V,Array(198).fill(-1),198,sv),D=normalize(V,198,iv,Array.from(W,Number)),largeV=localPortfolio(V,198,iv,D,rv,8,sv);
return {Y6:sy,X12:sx,K4:{track:rk,stats:sk},V198:{D,track:largeV,stats:sv}}
}
console.log(JSON.stringify(audit(U,W),null,2));
