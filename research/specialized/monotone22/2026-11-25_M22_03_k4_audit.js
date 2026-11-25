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
function solve2(h,C){
 const g=Array.from({length:2*h},()=>[]),r=g.map(()=>[]);function edge(a,b){g[a].push(b);r[b].push(a)}
 for(const [a,b] of C){edge(a^1,b);edge(b^1,a)}
 const seen=Array(2*h).fill(false),order=[];function dfs(v){seen[v]=true;for(const w of g[v])if(!seen[w])dfs(w);order.push(v)}
 for(let i=0;i<2*h;i++)if(!seen[i])dfs(i);const comp=Array(2*h).fill(-1);function rev(v,k){comp[v]=k;for(const w of r[v])if(comp[w]<0)rev(w,k)}
 let k=0;for(const v of order.reverse())if(comp[v]<0)rev(v,k++);
 const ans=[];for(let i=0;i<h;i++){if(comp[2*i]===comp[2*i+1])return null;ans.push(Number(comp[2*i+1]>comp[2*i]))}
 assert(C.every(([a,b])=>ans[a>>1]===(a&1)||ans[b>>1]===(b&1)),"2sat lift");return ans
}
// Explicit local basis lists; deterministic unweighted matroid intersection.
function matroidPortfolio(charts,S){
 let bad=null;
 for(const chart of charts){
 const E=chart.boundary,keys=[...chart.projected.keys()],set=new Set(keys),rank=Array.from(keys[0]).filter(v=>v==="1").length;
 assert(keys.every(p=>Array.from(p).filter(v=>v==="1").length===rank),"constant boundary weight");
 for(const a of keys)for(const b of keys)for(let i=0;i<E.length;i++)if(a[i]==="1"&&b[i]==="0"){
 S.matroidExchangeChecks++;let ok=false;
 for(let j=0;j<E.length;j++)if(a[j]==="0"&&b[j]==="1"){
 const c=Array.from(a);c[i]="0";c[j]="1";if(set.has(c.join(""))){ok=true;break}
 }
 if(!ok&&!bad)bad={edges:E,bases:keys,a,b,i}
 }
 }
 if(bad)return {status:"NONMATROID",bad};
 const E=charts.flatMap(c=>c.boundary),labels=new Set(E.map(e=>e>>1));
 assert(E.length===2*labels.size&&new Set(E).size===E.length,"boundary label pairing");
 const rank=charts.reduce((s,c)=>s+Array.from(c.projected.keys().next().value).filter(v=>v==="1").length,0);
 assert(rank===labels.size,"boundary rank total");
 function independent1(I){S.matroidIndependenceQueries++;return new Set([...I].map(e=>e>>1)).size===I.size}
 function independent2(I){S.matroidIndependenceQueries++;return charts.every(c=>[...c.projected.keys()].some(p=>c.boundary.every((e,i)=>!I.has(e)||p[i]==="1")))}
 const plus=(I,e)=>new Set([...I,e]);function swap(I,x,y){const J=new Set(I);J.delete(x);J.add(y);return J}
 let I=new Set();
 while(I.size<labels.size){
 const outside=E.filter(e=>!I.has(e)),q=[],parent=new Map();
 for(const e of outside)if(independent1(plus(I,e))){q.push(e);parent.set(e,null)}
 let end=null;
 for(let j=0;j<q.length;j++){
 const v=q[j];if(!I.has(v)&&independent2(plus(I,v))){end=v;break}
 if(I.has(v)){for(const w of outside)if(!parent.has(w)&&independent1(swap(I,v,w))){parent.set(w,v);q.push(w)}}
 else for(const w of I)if(!parent.has(w)&&independent2(swap(I,w,v))){parent.set(w,v);q.push(w)}
 }
 if(end===null)return {status:"NO"};
 const J=new Set(I);for(let v=end;v!==null;v=parent.get(v)){if(J.has(v))J.delete(v);else J.add(v)}
 assert(J.size===I.size+1&&independent1(J)&&independent2(J),"intersection augmentation");I=J;S.matroidAugments++;
 }
 assert(charts.every(c=>c.projected.has(c.boundary.map(e=>Number(I.has(e))).join(""))),"base lift");
 return {status:"YES",selected:[...I]}
}
function terminal(F,n,inc,D,root,cap=16){
 const S=stats();assert(D.length===n/3&&new Set(D).size===D.length,"D guard");
 let p=root.slice(),G,A,base;
 while(true){S.rounds++;p=closure(F,p,n,S);if(!p)return {status:"NO",why:"source-guard",S};
 G=graph(F,n,inc,D,p);base=pm(G.vertices,G.edges,[],[],S);if(!base)return {status:"NO",why:"ordinary matching",S};
 A=[];const used=new Set(base);
 for(const e of G.edges){S.allowedQueries++;if(used.has(e.id)||pm(G.vertices,G.edges,[e.id],[],S))A.push(e)}
 const aid=new Set(A.map(e=>e.id));let change=false;
 for(const v of D){const a=aid.has(2*v),b=aid.has(2*v+1);if(!a&&!b)return {status:"NO",why:"missing label",S};if(a!==b){const s=Number(b);assert(p[v]===-1||p[v]===s,"forced sign");if(p[v]===-1){p[v]=s;change=true}}}
 if(!change)break
 }
 const adj=new Map(G.vertices.map(v=>[v,[]]));for(const e of A){adj.get(e.a).push(e.b);adj.get(e.b).push(e.a)}
 const seen=new Set(),parts=[];for(const v of G.vertices)if(!seen.has(v)){const q=[v];seen.add(v);for(let i=0;i<q.length;i++)for(const w of adj.get(q[i]))if(!seen.has(w)){seen.add(w);q.push(w)}const vs=new Set(q);parts.push({vertices:q,edges:A.filter(e=>vs.has(e.a))})}
 S.componentCount=parts.length;
 const bits=G.pairIds,pos=new Map(bits.map((v,i)=>[v,i])),C=[],allowed=new Set(A.map(e=>e.id)),details=[];let allBij=true,nonBij=null;const charts=[];
 const unit=(i,b)=>C.push([2*i+b,2*i+b]);
 for(const v of D){const i=pos.get(2*v),j=pos.get(2*v+1);C.push([2*i+1,2*j+1],[2*i,2*j]);for(const k of [2*v,2*v+1])if(!allowed.has(k))unit(pos.get(k),0)}
 for(const P of parts){
 const E=P.edges.filter(e=>e.pair).map(e=>e.id);if(!E.length)continue;
 const R=[],force=[],ban=[],pat=[];let over=false;
 function enumerate(i){if(over)return;if(i===E.length){R.push(pat.join(""));if(R.length>cap)over=true;return}for(let b=0;b<2;b++){const ar=b?force:ban;ar.push(E[i]);S.patternQueries++;if(pm(P.vertices,P.edges,force,ban,S)){pat.push(b);enumerate(i+1);pat.pop()}ar.pop();if(over)return}}
 enumerate(0);assert(R.length>0,"local nonempty");let bij=!over;
 const fullPatterns=R.length;let interfaceSize=E.length;
 if(!over){
 const ep=new Map(E.map((id,i)=>[id,i]));
 const internal=E.filter(id=>ep.has(id^1)||!allowed.has(id^1));
 const boundary=E.filter(id=>!internal.includes(id));interfaceSize=boundary.length;
 const projected=new Map();for(const pat of R){
 if(!internal.every(id=>Number(pat[ep.get(id)])+(ep.has(id^1)?Number(pat[ep.get(id^1)]):0)===1))continue;
 const key=boundary.map(id=>pat[ep.get(id)]).join("");if(!projected.has(key))projected.set(key,pat)
 }
 if(!projected.size)return {status:"NO",why:"local exact-label obstruction",S,allBij:false,details,nonBij};
 charts.push({E:E.slice(),boundary,projected});
 E.splice(0,E.length,...boundary);R.splice(0,R.length,...projected.keys());
 const set=new Set(R);outer:for(const a of R)for(const b of R)for(const c of R){S.majorityTests++;const z=Array.from(a,(v,i)=>Number(Number(v)+Number(b[i])+Number(c[i])>=2)).join("");if(!set.has(z)){bij=false;if(!nonBij)nonBij={edges:E,patterns:R,a,b,c,majority:z};break outer}}
 // Exact unary and binary projections. They are necessary even if R is not bijunctive.
 for(let i=0;i<E.length;i++)for(let b=0;b<2;b++)if(!R.some(r=>Number(r[i])===b))unit(pos.get(E[i]),1-b);
 for(let i=0;i<E.length;i++)for(let j=i+1;j<E.length;j++)for(let a=0;a<2;a++)for(let b=0;b<2;b++)if(!R.some(r=>Number(r[i])===a&&Number(r[j])===b))C.push([2*pos.get(E[i])+1-a,2*pos.get(E[j])+1-b]);
 }else{
 // Do not derive exclusions from an incomplete enumeration.
 // Only query binary projections on small interfaces; cap controls practical cost.
 if(E.length<=16)for(let i=0;i<E.length;i++)for(let j=i+1;j<E.length;j++)for(let a=0;a<2;a++)for(let b=0;b<2;b++){
 const f=[],bans=[];(a?f:bans).push(E[i]);(b?f:bans).push(E[j]);S.patternQueries++;if(!pm(P.vertices,P.edges,f,bans,S))C.push([2*pos.get(E[i])+1-a,2*pos.get(E[j])+1-b])
 }
 }
 allBij&&=bij;details.push({vertices:P.vertices.length,interface:interfaceSize,fullPatterns,patterns:R.length,capped:over,bij});
 }
 let matroid=null,word;
 if(!details.some(d=>d.capped)){
 matroid=matroidPortfolio(charts,S);
 if(matroid.status==="NO")return {status:"NO",why:"matroid intersection",S,allBij,details,nonBij,matroid};
 if(matroid.status==="YES"){const chosen=new Set(matroid.selected);word=bits.map(e=>Number(chosen.has(e)))}
 }
 if(!word)word=solve2(bits.length,C);
 if(!word)return {status:"NO",why:"binary projection",S,allBij,details,nonBij,matroid};
 for(const chart of charts){
 const key=chart.boundary.map(id=>word[pos.get(id)]).join("");const pat=chart.projected.get(key);
 if(pat===undefined){assert(!allBij,"certified projection failed");return {status:"UNKNOWN",why:"non-bijunctive boundary",S,allBij,details,nonBij,matroid}}
 chart.E.forEach((id,i)=>{word[pos.get(id)]=Number(pat[i])});
 }
 const f=bits.filter((_,i)=>word[i]),b=bits.filter((_,i)=>!word[i]);const M=pm(G.vertices,A,f,b,S);
 if(!M){assert(!allBij,"certified bijunctive lift failed");return {status:"UNKNOWN",why:"non-bijunctive residual",S,allBij,details,nonBij,matroid}}
 const x=Array(n).fill(-1),labels=new Set(),byId=new Map(A.map(e=>[e.id,e]));for(const id of M){const e=byId.get(id);assert(!labels.has(e.v),"duplicate label");labels.add(e.v);x[e.v]=e.s}
 assert(labels.size===n&&sat(F,x)&&p.every((v,i)=>v===-1||x[i]===v),"source lift");
 return {status:"YES",why:"verified",x,S,allBij,details,nonBij,matroid}
}
// Independent reference: all sign choices of the prescribed double labels,
// then a plain bipartite augmenting matching of the remaining clauses.
function ref(F,n,inc,D){
 for(let mask=0;mask<2**D.length;mask++){
 const dc=new Set(),ds=new Set(D);let ok=true;for(let i=0;i<D.length;i++){const v=D[i],s=(mask>>i)&1;for(const c of inc[v].filter(i=>Number(F[i][0]>0)===s)){if(dc.has(c))ok=false;dc.add(c)}}if(!ok)continue;
 const match=Array(n).fill(-1);
 function dfs(c,seen){for(const l of F[c]){const v=Math.abs(l)-1;if(ds.has(v)||seen.has(v))continue;seen.add(v);if(match[v]===-1||dfs(match[v],seen)){match[v]=c;return true}}return false}
 if(F.every((_,i)=>dc.has(i)||dfs(i,new Set())))return true
 }return false
}
function combinations(n,k,fn){const a=[];function go(i){if(a.length===k){fn(a.slice());return}for(let j=i;j<=n-(k-a.length);j++){a.push(j);go(j+1);a.pop()}}go(0)}
function small(F,n){
 const inc=compile(F,n),st=stats(),root=closure(F,Array(n).fill(-1),n,st);assert(root,"small source");let models=0;for(let m=0;m<2**n;m++)if(sat(F,Array.from({length:n},(_,i)=>(m>>i)&1)))models++;
 let result={models,root:st,tracks:0,refYes:0,refNo:0,yes:0,no:0,unknown:0,nonBij:0,certifiedBij:0,maxComponents:0,maxPatterns:0,matroidYes:0,matroidNo:0,matroidFail:0,matroidExample:null,totals:stats(),example:null,exampleNo:null,exampleUnknown:null};
 combinations(n,n/3,D=>{const truth=ref(F,n,inc,D),r=terminal(F,n,inc,D,root,80);result.tracks++;result[truth?"refYes":"refNo"]++;result[r.status.toLowerCase()]++;assert(r.status==="UNKNOWN"||(r.status==="YES")===truth,"reference mismatch");
 if(r.matroid){if(r.matroid.status==="YES")result.matroidYes++;else if(r.matroid.status==="NO")result.matroidNo++;else{result.matroidFail++;if(!result.matroidExample)result.matroidExample={D,r,truth}}}if(r.allBij)result.certifiedBij++;if(r.nonBij){result.nonBij++;if(!result.example)result.example={D,r,truth}}if(r.status==="NO"&&!result.exampleNo)result.exampleNo={D,r};if(r.status==="UNKNOWN"&&!result.exampleUnknown)result.exampleUnknown={D,r,truth};
 if(r.details){result.maxComponents=Math.max(result.maxComponents,r.S.componentCount);for(const q of r.details)result.maxPatterns=Math.max(result.maxPatterns,q.fullPatterns??q.patterns)}
 for(const k of Object.keys(result.totals))result.totals[k]+=r.S[k];
 });return result
}
function normalize(F,n,inc,x){assert(sat(F,x),"seed");const r=F.map(c=>Math.abs(c.find(l=>x[Math.abs(l)-1]===Number(l>0)))-1);
 while(true){const cnt=Array(n).fill(0);r.forEach(v=>cnt[v]++);const root=cnt.indexOf(0);if(root<0)return cnt.map((c,v)=>c===2?v:-1).filter(v=>v>=0);
 const q=[root],seen=new Set(q),par=new Map();let end=null;for(let i=0;i<q.length&&!end;i++){const v=q[i];for(const c of inc[v]){const w=r[c];if(cnt[w]===2){end=[v,c];break}if(!seen.has(w)){seen.add(w);q.push(w);par.set(w,[v,c])}}}assert(end,"normalize");let [v,c]=end;while(true){r[c]=v;if(v===root)break;[v,c]=par.get(v)}
 }}
function greedy(F,n,inc){const D=[],cs=new Set();for(let v=0;v<n;v++){for(let s=0;s<2;s++){const e=inc[v].filter(i=>Number(F[i][0]>0)===s);if(e.some(i=>cs.has(i)))continue;D.push(v);e.forEach(i=>cs.add(i));break}if(D.length===n/3)return D}throw Error("greedy")}
let seed=20261125;function rand(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/2**32}
function brute(vertices,edges,force,ban){const rem=new Set(vertices),f=new Set(force),b=new Set(ban);for(const id of f){const e=edges.find(e=>e.id===id);if(!e||b.has(id)||!rem.has(e.a)||!rem.has(e.b))return false;rem.delete(e.a);rem.delete(e.b)}function rec(R){if(!R.size)return true;const v=R.values().next().value;for(const e of edges){if(b.has(e.id))continue;const w=e.a===v?e.b:e.b===v?e.a:-1;if(w<0||!R.has(w))continue;const T=new Set(R);T.delete(v);T.delete(w);if(rec(T))return true}return false}return rec(rem)}
// Connected strict counterexample to universal boundary-matroid or boundary-bijunctive structure.
const n=18,D=[0,1,2,3,4,5];
const pos=[];for(const off of [0,6,12])for(const c of [[1,2,3],[1,4,5],[2,4,6],[3,5,6]])pos.push(c.map(v=>v+off));
let attempts=0;
for(let trial=0;trial<100;trial++){
 attempts++;
 const order=Array.from({length:12},(_,i)=>i+7);for(let i=order.length-1;i>0;i--){const j=Math.floor(rand()*(i+1));[order[i],order[j]]=[order[j],order[i]]}
 const neg=Array.from({length:12},(_,i)=>[-(1+(i>>1)),-order[i],-order[(i+11)%12]]);
 const F=pos.concat(neg),inc=compile(F,n),S=stats(),root=closure(F,Array(n).fill(-1),n,S);
 if(!root||!ref(F,n,inc,D))continue;
 const r=terminal(F,n,inc,D,root,512);
 if(r.matroid?.status!=="NONMATROID"||!r.nonBij)continue;
 const b=r.matroid.bad;
 if(b.edges.length!==6||!b.edges.every(id=>id%2===1))continue;
 // Independent complete enumeration of the three K4 perfect pairings.
 const E=b.edges.map(id=>({id,a:inc[id>>1].filter(i=>F[i][0]>0)[0],b:inc[id>>1].filter(i=>F[i][0]>0)[1]}));
 const exact=[];for(let mask=0;mask<64;mask++){
 const seen=new Set(),bits=E.map((_,j)=>(mask>>j)&1);let ok=true;
 for(let j=0;j<6;j++)if(bits[j]){const e=E[j];if(seen.has(e.a)||seen.has(e.b))ok=false;seen.add(e.a);seen.add(e.b)}
 if(ok&&seen.size===4)exact.push(bits.join(""))
 }
 assert(exact.length===3&&exact.every(p=>b.bases.includes(p))&&b.bases.every(p=>exact.includes(p)),"K4 pattern completeness");
 // Independent source enumeration and guarded exact-track sign counts.
 let models=0,witness=null;for(let mask=0;mask<2**n;mask++){const x=Array.from({length:n},(_,i)=>(mask>>i)&1);if(sat(F,x)){models++;if(!witness)witness=x}}
 const st=stats(),G=graph(F,n,inc,D,root);const allowed=G.edges.filter(e=>pm(G.vertices,G.edges,[e.id],[],st));
 assert(D.every(v=>allowed.some(e=>e.id===2*v)&&allowed.some(e=>e.id===2*v+1)),"all boundary signs allowed");
 // Source connectivity from variable co-occurrence, all 18 connected.
 const Q=[0],seen=new Set(Q);for(let j=0;j<Q.length;j++)for(const i of inc[Q[j]])for(const l of F[i]){const v=Math.abs(l)-1;if(!seen.has(v)){seen.add(v);Q.push(v)}}assert(seen.size===n,"connected");
 return {attempts,F,D,root:S,models,witness,track:r,exactK4Patterns:exact,independentAllowedCheck:st.matchCalls};
}
throw Error("no strict counterexample");
}
console.log(JSON.stringify(audit(U,W),null,2));
