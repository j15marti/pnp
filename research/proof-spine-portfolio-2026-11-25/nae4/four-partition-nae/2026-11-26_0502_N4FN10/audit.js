// N4FN10: sparse-coordinate correlated cuts and inherited search charts.
let seed=20261126,checks=0,flows=0,nodes=0,conditionalNo=0;
function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)%n}
function ok(x,m=""){checks++;if(!x)throw Error("check "+checks+" "+m)}
function perm(n){let a=Array.from({length:n},(_,i)=>i);for(let i=n-1;i>0;i--){let j=rnd(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
function bit(i){return 1n<<BigInt(i)}
function basis(rows){let a=new Map;for(let x of rows){while(x){let p=x.toString(2).length-1;if(!a.has(p)){a.set(p,x);break}x^=a.get(p)}}return [...a.values()]}
function mask(cols){return cols.reduce((m,i)=>m^bit(i),0n)}
function proj(edges){let col=new Map,off=0n;for(let i=0;i<edges.length;i++){let e=edges[i];if(e.off)off^=bit(i);for(let j of e.cols)col.set(j,(col.get(j)||0n)^bit(i))}
let B=basis([...col.values()]),out=[off];if(B.length>16)throw Error("test profile cap");for(let b of B)out=out.concat(out.map(x=>x^b));return out}
function components(n,edges){let p=Array.from({length:n},(_,i)=>i),used=new Set;function find(x){while(p[x]!==x){p[x]=p[p[x]];x=p[x]}return x}for(let e of edges){let a=find(e.u),b=find(e.v);p[a]=b;used.add(e.u);used.add(e.v)}let m=new Map;for(let v of used){let a=find(v);if(!m.has(a))m.set(a,[]);m.get(a).push(v)}return [...m.values()]}
function support(G){let m=new Map,s=0;for(let e of G.e){s=Math.max(s,e.cols.length);for(let j of e.cols){if(!m.has(j))m.set(j,[]);m.get(j).push(e)}}let H=[],d=0;for(let es of m.values()){let c=components(G.n,es);d=Math.max(d,c.length);H.push(...c)}return {H,s,d,h:Math.max(1,s*d)}}
function cut(G,S,H){let cross=G.e.filter(e=>S.has(e.u)!==S.has(e.v)),r=basis(cross.map(e=>mask(e.cols))).length,w=H.filter(a=>a.some(v=>S.has(v))&&a.some(v=>!S.has(v))).length;return {r,w,cross}}
function mincut(G,H,A,B,alpha,beta){flows++;let n=G.n,ss=n+2*H.length,tt=ss+1,g=Array.from({length:tt+1},()=>[]),M=alpha*H.length+beta*n+1;
function arc(u,v,c){let a={v,c,rev:g[v].length},b={v:u,c:0,rev:g[u].length};g[u].push(a);g[v].push(b)}
H.forEach((a,i)=>{let x=n+2*i,y=x+1;arc(x,y,alpha);for(let v of a){arc(v,x,M);arc(y,v,M)}});for(let v of A)arc(ss,v,M);for(let v of B)arc(v,tt,M);for(let i=0;i<n;i++)arc(i,tt,beta);
let f=0,L;
for(;;){L=Array(g.length).fill(-1);L[ss]=0;let q=[ss];for(let k=0;k<q.length;k++)for(let e of g[q[k]])if(e.c&&L[e.v]<0){L[e.v]=L[q[k]]+1;q.push(e.v)}if(L[tt]<0)break;let it=Array(g.length).fill(0);
function dfs(u,c){if(u===tt)return c;for(;it[u]<g[u].length;it[u]++){let e=g[u][it[u]];if(e.c&&L[e.v]===L[u]+1){let x=dfs(e.v,Math.min(c,e.c));if(x){e.c-=x;g[e.v][e.rev].c+=x;return x}}}return 0}
for(let x;(x=dfs(ss,M));)f+=x}
let S=new Set(Array.from({length:n},(_,i)=>i).filter(i=>L[i]>=0));let {w,r}=cut(G,S,H);ok(A.every(v=>S.has(v))&&B.every(v=>!S.has(v)));ok(f===alpha*w+beta*S.size);return {S,w,r,f}}
function admits(mu,u,r,K){return (1n<<BigInt(r))*BigInt(u)**BigInt(K)<=BigInt(mu)**BigInt(K)}
function discover(G,K){let {H,h}=support(G),mu=G.n-2;if(mu<2)return null;for(let u=1;u<=mu/2;u++)for(let q=0;q<=h*K*Math.floor(Math.log2(mu))+h*K;q++){if(q>0&&!admits(mu,u,Math.ceil(q/h),K))continue;
for(let a=0;a<G.n;a++)for(let b=a+1;b<G.n;b++)for(let c=0;c<G.n;c++)for(let d=c+1;d<G.n;d++){if(c===a||c===b||d===a||d===b)continue;
let R=mincut(G,H,[a,b],[c,d],u,q),u2=Math.min(R.S.size,G.n-R.S.size)-1;if(admits(mu,u2,R.r,4*h*K))return {...R,h}}}return null}
function allCuts(G){let {H,h}=support(G),a=[];for(let i=0;i<2**G.n;i++){let S=new Set(Array.from({length:G.n},(_,j)=>j).filter(j=>(i>>j)&1));if(S.size<2||S.size>G.n-2)continue;let c=cut(G,S,H);ok(c.r<=c.w&&c.w<=h*c.r,"rank bound");a.push({S,...c})}return a}
function randomGraph(n,m,d){let e=[];for(let i=0;i<m;i++){let u=rnd(n),v=rnd(n-1);if(v>=u)v++;let a=rnd(d),b=rnd(d),q=rnd(4);e.push({id:i,u,v,cols:q===0?[]:q===1||a===b?[a]:[a,b],off:rnd(2)})}return {n,e}}
let synthetic={graphs:0,cuts:0,weighted:0,discovery:0,admitted:0,found:0,maxH:0};
for(let i=0;i<100;i++){let G=randomGraph(4+rnd(5),5+rnd(7),4),{H,h}=support(G),cs=allCuts(G);synthetic.graphs++;synthetic.cuts+=cs.length;synthetic.maxH=Math.max(synthetic.maxH,h);let a=1+rnd(4),b=rnd(4),t=mincut(G,H,[0,1],[2,3],a,b),ref=Math.min(...cs.filter(c=>c.S.has(0)&&c.S.has(1)&&!c.S.has(2)&&!c.S.has(3)).map(c=>a*c.w+b*c.S.size));ok(t.f===ref);synthetic.weighted++;
if(i<25){let mu=G.n-2,has=cs.some(c=>admits(mu,Math.min(c.S.size,G.n-c.S.size)-1,c.r,1)),R=discover(G,1);ok(!has||R);if(R){let u=Math.min(R.S.size,G.n-R.S.size)-1;ok(admits(mu,u,R.r,4*h));synthetic.found++}synthetic.admitted+=has;synthetic.discovery++}}
function table(scope,pred){let rows=[];for(let j=0;j<2**scope.length;j++)if(pred(j))rows.push(BigInt(j));return {scope,rows}}
function get(w,id){return w.get(id)||0}
function localWord(f,w){return f.scope.reduce((m,id,i)=>m|(get(w,id)?bit(i):0n),0n)}
function valid(G,w){return G.v.every(f=>f.rows.includes(localWord(f,w)))}
function brute(G,chart=false){if(chart){let ps=proj(G.e);for(let p of ps){let w=new Map(G.e.map((e,i)=>[e.id,Number((p>>BigInt(i))&1n)]));if(valid(G,w))return w}}else{for(let p=0;p<2**G.e.length;p++){let w=new Map(G.e.map((e,i)=>[e.id,(p>>i)&1]));if(valid(G,w))return w}}return null}
function closure(G){let es=new Map(G.e.map(e=>[e.id,e])),v=G.v.map(f=>{let P=new Set(proj(f.scope.map(i=>es.get(i))));return {scope:f.scope,rows:f.rows.filter(r=>P.has(r))}}),D=new Map(G.e.map(e=>[e.id,3]));let change=true;while(change){change=false;for(let f of v){f.rows=f.rows.filter(r=>f.scope.every((id,j)=>D.get(id)&(1<<Number((r>>BigInt(j))&1n))));if(!f.rows.length)return null;for(let j=0;j<f.scope.length;j++){let s=0;for(let r of f.rows)s|=1<<Number((r>>BigInt(j))&1n);let id=f.scope[j],d=D.get(id)&s;if(!d)return null;if(d!==D.get(id)){D.set(id,d);change=true}}}}return {...G,v}}
function child(G,S,rows,boundary){let verts=[...S],ix=new Map(verts.map((v,i)=>[v,i])),cap=verts.length;
let e=G.e.filter(e=>S.has(e.u)||S.has(e.v)).map(e=>({...e,u:ix.has(e.u)?ix.get(e.u):cap,v:ix.has(e.v)?ix.get(e.v):cap}));return {n:cap+1,e,v:[...verts.map(i=>G.v[i]),{scope:boundary.map(e=>e.id),rows}]}}
function solve(G){nodes++;let old=G,chartTruth=brute(G,true),localTruth=brute(G,false);G=closure(G);let w=null;
if(G){if(G.n<=3||G.e.length<=2)w=brute(G);else {let R=discover(G,1);if(!R)w=brute(G);else{let S=R.S;if(S.size>G.n-S.size)S=new Set(Array.from({length:G.n},(_,i)=>i).filter(i=>!S.has(i)));let T=new Set(Array.from({length:G.n},(_,i)=>i).filter(i=>!S.has(i))),boundary=cut(G,S,support(G).H).cross,profiles=proj(boundary),D=new Map;
for(let p of profiles){let A=solve(child(G,S,[p],boundary));if(A)D.set(p,A)}
if(D.size){let B=solve(child(G,T,[...D.keys()],boundary));if(B){let p=localWord({scope:boundary.map(e=>e.id)},B);w=new Map([...D.get(p),...B]);ok(valid(G,w))}}}}}
ok(!chartTruth||w,"lost chart-compatible model");ok(!w||valid(old,w),"spurious witness");if(!w&&localTruth)conditionalNo++;return w}
let sandwich={jobs:0,chartSat:0,localSat:0,accepted:0};
for(let i=0;i<120;i++){let G=randomGraph(4+rnd(3),4+rnd(5),3);G.v=Array.from({length:G.n},(_,j)=>table(G.e.filter(e=>e.u===j||e.v===j).map(e=>e.id),()=>rnd(3)!==0));let a=brute(G,true),b=brute(G),w=solve(G);sandwich.jobs++;sandwich.chartSat+=!!a;sandwich.localSat+=!!b;sandwich.accepted+=!!w}
const P=[[[0,1,2],[3,4,5],[6,7,8]],[[0,3,6],[1,4,7],[2,5,8]],[[0,4,8],[1,5,6],[2,3,7]],[[0,5,7],[1,3,8],[2,4,6]]];
function nae(a){return a.some(x=>x!==a[0])}
function auth(F,n){let pairs=new Set;for(let p of F){let C=Array(n).fill(0);for(let a of p){ok(a.length===3&&new Set(a).size===3);for(let v of a)C[v]++;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let key=[a[i],a[j]].sort((x,y)=>x-y).join(",");ok(!pairs.has(key));pairs.add(key)}}ok(C.every(x=>x===1))}}
function build(k,no){let F=Array.from({length:4},()=>[]),sg=Array.from({length:k},(_,i)=>(i+1)%k);if(no)[sg[0],sg[3]]=[sg[3],sg[0]];for(let i=0;i<k;i++){for(let j=0;j<4;j++)for(let c of (j?P[j]:P[0].slice(2)))F[j].push(c.map(v=>v+9*i));F[0].push([9*i,9*i+1,9*((i+1)%k)+2],[9*i+3,9*i+4,9*sg[i]+5])}let a=perm(9*k),q=0;while((q+1)*q/2<=k)q++;let h=q,guards=[],t=0;for(let i=0;i<h;i++)for(let j=i+1;j<h;j++)guards.push({v:a[9*t+++6],i,j});F=perm(4).map(j=>perm(F[j].length).map(i=>F[j][i].map(v=>a[v])));auth(F,9*k);return {F,n:9*k,h,guards}}
function motifClose(F,n){let cs=F.flat(),inc=Array.from({length:n},()=>[]);cs.forEach((c,i)=>c.forEach(v=>inc[v].push(i)));let p=Array.from({length:n},(_,i)=>i),d=Array(n).fill(0);
function find(x){if(p[x]===x)return [x,0];let [r,b]=find(p[x]);d[x]^=b;p[x]=r;return [r,d[x]]}
function join(x,y,b){let [a,c]=find(x),[e,f]=find(y);if(a===e)return (c^f)===b?0:-1;p[e]=a;d[e]=b^c^f;return 1}
let seen=new Set,mods=0;for(let v=0;v<n;v++){let S=[...new Set([v,...inc[v].flatMap(i=>cs[i])])].sort((a,b)=>a-b),key=S.join(",");if(seen.has(key))continue;seen.add(key);if(S.length!==9)continue;let set=new Set(S),C=[...new Set(S.flatMap(v=>inc[v]))].map(i=>cs[i]).filter(c=>c.every(v=>set.has(v)));if(C.length>=11)return null;if(C.length!==10)continue;let adj=new Map(S.map(v=>[v,new Set]));for(let c of C)for(let a of c)for(let b of c)if(a!==b)adj.get(a).add(b);let miss=v=>S.filter(w=>w!==v&&!adj.get(v).has(w)),a=S.find(v=>miss(v).length===2);if(a===undefined)continue;let A=[a,...miss(a)],B=S.filter(v=>!A.includes(v)&&miss(v).length===2),tri=a=>a.length===3&&a.every(v=>miss(v).length===2&&miss(v).every(w=>a.includes(w)));if(!tri(A)||!tri(B)||S.some(v=>!A.includes(v)&&!B.includes(v)&&miss(v).length))continue;mods++;for(let v of A)if(join(a,v,0)<0)return null;for(let v of B)if(join(a,v,1)<0)return null}
let residual=[];for(;;){let change=0;residual=[];for(let c of cs){let z=c.map(find),drop=false,eq=null;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)if(z[i][0]===z[j][0]){if(z[i][1]!==z[j][1])drop=true;else eq=[i,j]}if(drop)continue;if(eq){let r=join(c[eq[0]],c[3-eq[0]-eq[1]],1);if(r<0)return null;change+=r}else residual.push(c)}if(!change)break}return {find,mods,residual}}
function guardedGraph(src,M){let {F,n,h,guards}=src,cs=F.flat(),G={n:n+cs.length+h+guards.length,e:[]},by=new Map(guards.map(g=>[g.v,g]));function edge(u,v,cols,off=0){G.e.push({id:G.e.length,u,v,cols,off})}
function label(v){if(by.has(v)){let g=by.get(v);return [[g.i,g.j],0]}let [r,b]=M?M.find(v):[v,0];return [[h+r],b]}
cs.forEach((c,i)=>c.forEach(v=>{let [a,b]=label(v);edge(v,n+i,a,b)}));
guards.forEach((g,i)=>{let v=n+cs.length+h+i;edge(g.v,v,[g.i,g.j]);edge(n+cs.length+g.i,v,[g.i]);edge(n+cs.length+g.j,v,[g.j])});return G}
let genuine=[];
for(let k of [6,12,32,64,128,256])for(let no of [false,true]){let src=build(k,no),{F,n,h,guards}=src,M=motifClose(F,n);ok(!!M===!no,"source motif decision");
let rec={k,n,expected:!no,guardCoordinates:h,guardCount:guards.length,decision:M?"SAT":"UNSAT"};
if(M){ok(M.mods===k);let roots=new Map,guardSet=new Set(guards.map(g=>g.v));for(let g of guards){let [r,b]=M.find(g.v);ok(!roots.has(r));roots.set(r,b)}
let used=new Set;for(let c of M.residual){let rr=c.map(M.find);ok(rr.every(([r])=>!used.has(r)));rr.forEach(([r])=>used.add(r));let z=Array.from({length:8},(_,i)=>[i&1,(i>>1)&1,(i>>2)&1]).find(a=>nae(a)&&a.every((v,i)=>!roots.has(rr[i][0])||roots.get(rr[i][0])===(v^rr[i][1])));ok(z);z.forEach((v,i)=>roots.set(rr[i][0],v^rr[i][1]))}
let x=Array.from({length:n},(_,v)=>{let [r,b]=M.find(v);return(roots.get(r)||0)^b});ok(F.flat().every(c=>nae(c.map(v=>x[v]))));ok(guards.every(g=>x[g.v]===0));
let G=guardedGraph(src,M),{H,s,d,h:factor}=support(G);ok(s===2&&d===1);let S=new Set(Array.from({length:n+F.flat().length},(_,i)=>i)),C=cut(G,S,H);ok(C.r===h-1&&C.w===h&&C.cross.length===guards.length);let R=mincut(G,H,[0,1],[G.n-1,G.n-2],1,0);ok(R.r<=R.w&&R.w<=factor*R.r);Object.assign(rec,{mods:M.mods,physicalBoundary:C.cross.length,rank:C.r,proxy:C.w,s,d,acquiredRank:R.r,acquiredProxy:R.w,verifiedWitness:true})}
genuine.push(rec)}
// Full binary projective row set: each nonzero latent coordinate is one in half of the rows.
let dense=[];for(let d=2;d<=10;d++){let rows=Array.from({length:2**d},(_,i)=>BigInt(i));ok(basis(rows).length===d);for(let j=0;j<d;j++)ok(rows.filter(r=>r&bit(j)).length===2**(d-1));dense.push({rank:d,distinctNonzeroRows:2**d-1,minPossibleMaxWeight:Math.ceil(d/2)})}
let recurrence=0;for(let mu=2;mu<=100;mu++)for(let u=1;u<=mu/2;u++)for(let h=1;h<=3;h++){let Q=4*h,c=Q+2;let r=0;while(admits(mu,u,r+1,Q))r++;let v=mu-u;ok((1n<<BigInt(r))*BigInt(u)**BigInt(c)+BigInt(v)**BigInt(c)<=BigInt(mu)**BigInt(c)-1n);recurrence++}
console.log(JSON.stringify({seed:20261126,checks,flows,nodes,conditionalNo,synthetic,sandwich,genuine,dense,recurrence}));