function audit(){
const ok=(x,m)=>{if(!x)throw Error(m)},CAP=65536;
const C=(a,b,c)=>new Set([a,b,c]).size===3&&[0,1,2,3,4].some(i=>[a,b,c].every(x=>[i,(i+1)%5,(i+2)%5].includes(x)));
const R=(a,b,c)=>new Set([a,b,c]).size===3&&([1,3].includes((b-a+5)%5)!==[1,3].includes((c-a+5)%5));
let tables=0;for(let a=0;a<5;a++)for(let b=0;b<5;b++)for(let c=0;c<5;c++){ok(C(a,b,c)===(R(a,b,c)&&R(b,a,c)),"C/R");tables++}
function graph(q,hostile=false){let t=q,U=Array(q).fill(6),V=Array(q).fill(0),arcs=[],paths=[],M=Array.from({length:q},(_,i)=>i);function path(a,b,L,optimal=false){let v=[a];for(let l=1;l<L;l++){v.push(t);U.push(L-l);V.push(l-L);M.push(t);t++}v.push(b);for(let i=0;i<L;i++){arcs.push([v[i],v[i+1]]);if(optimal)M[v[i]]=v[i+1]}paths.push({a,b,L,v})}
for(let i=0;i<q;i++){path(i,i,6,true);path(i,i,4);if(hostile&&i===0)path(i,i,5)}
for(let i=0;i<q;i++)for(let j=0;j<q;j++)if(i!==j)path(i,j,5);
return {q,t,U,V,arcs,paths,M,k:6*q-1}}
function source(G){let {t,k}=G,E=[],O=Array.from({length:3*(t+k)},()=>[]),h=2166136261;
function add(a,b,c){let id=E.length;E.push([a,b,c]);[a,b,c].forEach((v,i)=>{O[i*(t+k)+v].push(id);h=Math.imul(h^v,16777619)>>>0})}
for(let i=0;i<t;i++){add(i,i,i);for(let a=0;a<k;a++)for(let b=0;b<k;b++)add(i,t+a,t+b)}
for(let [i,j] of G.arcs)for(let c=0;c<k;c++)add(t+c,i,j);
return {E,O,hash:h.toString(16),t,k}}
function search(F){let {E,O,t,k}=F,h=t+k,used=new Uint8Array(O.length),order=O.map((_,i)=>i).sort((a,b)=>O[a].length-O[b].length),work=0,cut=false;
function go(depth){if(depth===h)return true;let a=order.find(i=>!used[i]);for(let z of O[a]){if(work===CAP){cut=true;return false}work++;let e=E[z],b=e[0],c=h+e[1],d=2*h+e[2];if(used[b]||used[c]||used[d])continue;used[b]=used[c]=used[d]=1;if(go(depth+1))return true;used[b]=used[c]=used[d]=0;if(cut)return false}return false}
let ans=go(0);return {status:ans?"YES":cut?"UNKNOWN":"NO",work}}
function gap(G){let {t,U,V,arcs,M}=G,inv=Array(t),W=0,checks=0;M.forEach((j,i)=>inv[j]=i);ok(new Set(M).size===t,"M perm");const actual=new Set(arcs.map(e=>e.join(",")));for(let i=0;i<t;i++){let j=M[i],w=+(i!==j);ok(!w||actual.has([i,j].join(",")),"M edge");ok(U[i]+V[j]===w,"tight M");W+=w}ok(W===6*G.q,"opt");
let edges=arcs.map(([i,j])=>[i,inv[j],U[i]+V[j]-1]);for(let i=0;i<t;i++)edges.push([i,inv[i],U[i]+V[i]]);
let D=Array.from({length:t},(_,i)=>Array.from({length:t},(_,j)=>i===j?0:Infinity));
for(let [i,j,s] of edges){ok(s>=0,"dual");D[i][j]=Math.min(D[i][j],s);checks++}
for(let k=0;k<t;k++)for(let i=0;i<t;i++)for(let j=0;j<t;j++){D[i][j]=Math.min(D[i][j],D[i][k]+D[k][j]);checks++}
let d=Infinity,one=0;for(let [i,j,s] of edges)if(s>0){d=Math.min(d,s+D[j][i]);if(s===1){one++;ok(G.k===W-1,"target")}}
return {W,d,slackOneEdges:one,checks}}
function reference(G){let {q,paths}=G,choices=Array.from({length:q},(_,i)=>[null,...paths.filter(p=>p.a===i)]),inc=Array(q).fill(0),out=Array(q).fill(0),S=new Set(),visits=0,stop=false;
function go(i,s){if(i===q){if(inc.every((x,j)=>x===out[j]))S.add(s);return}
for(let p of choices[i]){if(visits===CAP){stop=true;return}visits++;if(!p){go(i+1,s)}else if(inc[p.b]===0){inc[p.b]++;out[i]=1;go(i+1,s+p.L);inc[p.b]--;out[i]=0}if(stop)return}}
go(0,0);return {visits,complete:!stop,support:[...S].sort((a,b)=>a-b)}}
function projection(F,a,b){let h=F.t+F.k,adj=Array.from({length:h},()=>new Set()),scans=0;F.E.forEach(e=>adj[e[a]].add(e[b]));let M=Array(h).fill(-1);function dfs(i,seen){for(let j of adj[i]){scans++;if(seen[j])continue;seen[j]=1;if(M[j]<0||dfs(M[j],seen)){M[j]=i;return true}}return false}for(let i=0;i<h;i++)ok(dfs(i,new Uint8Array(h)),"projection");return scans}
let jobs=[];for(let q of [3,4,5,6]){let G=graph(q),F=source(G),A=search(F),B=gap(G),CC=reference(G);ok(A.status!=="YES"&&B.d===2&&!CC.support.includes(G.k),"NO");if(CC.complete)ok(CC.support.at(-1)===B.W&&CC.support.at(-2)===B.W-B.d,"exact support");
let minDegree=Math.min(...F.O.map(o=>o.length));ok(minDegree>=2,"raw GAC");
let e=F.E.length,o=F.O.length,n=64*e-20*o+5,m=78*e-24*o+5,N=n+1+2*Math.floor(Math.log2(m+1))+1+3*m*Math.ceil(Math.log2(n+1));jobs.push({q,t:G.t,k:G.k,e,o,n,m,N,hash:F.hash,minDegree,A,B,C:CC,projection:[[0,1],[0,2],[1,2]].map(([a,b])=>projection(F,a,b))})}
let H=graph(3,true),F=source(H),B=gap(H),CC=reference(H);ok(B.d===1&&CC.support.includes(H.k),"hostile gap");
// Lift explicit packing: use length5 at junction0 and length6 at others.
let selected=H.paths.filter(p=>(p.a===0&&p.b===0&&p.L===5)||(p.a>0&&p.a===p.b&&p.L===6)),active=selected.flatMap(p=>p.v.slice(0,-1));ok(active.length===H.k,"hostile size");
let idx=new Map(active.map((v,i)=>[v,i])),w=[];for(let i=0;i<H.t;i++){if(!idx.has(i))w.push([i,i,i]);else w.push([i,H.t+idx.get(i),H.t+idx.get(i)])}
for(let p of selected)for(let j=0;j<p.L;j++)w.push([H.t+idx.get(p.v[j]),p.v[j],p.v[j+1]]);
let set=new Set(F.E.map(e=>e.join(","))),counts=Array(F.O.length).fill(0);w.forEach(e=>{ok(set.has(e.join(",")),"hostile edge");e.forEach((v,i)=>counts[i*(F.t+F.k)+v]++)});ok(counts.every(v=>v===1),"hostile cover");
return {tables,CAP,jobs,hostile:{B,C:CC,verifiedCover:w.length}}
}
console.log(JSON.stringify(audit(),null,2));
