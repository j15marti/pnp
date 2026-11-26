function audit(){
const seq=n=>Array.from({length:n},(_,i)=>i),key=x=>x.join(';');let checks=0;const A=(x,m)=>{checks++;if(!x)throw Error(m)};
function mesh(k){
 let F=[];for(let sx of [-1,1])for(let sy of [-1,1])for(let sz of [-1,1]){const v=(i,j)=>[sx*i,sy*j,sz*(k-i-j)].join(',');for(let i=0;i<k;i++)for(let j=0;j<k-i;j++){let fs=[[v(i,j),v(i+1,j),v(i,j+1)]];if(i+j<k-1)fs.push([v(i+1,j),v(i+1,j+1),v(i,j+1)]);for(let f of fs)F.push(sx*sy*sz===1?f:[f[0],f[2],f[1]])}}
 let E=new Map();F.forEach((f,i)=>f.forEach((a,j)=>{let e=key([a,f[(j+1)%3]].sort());if(!E.has(e))E.set(e,[]);E.get(e).push(i)}));A([...E.values()].every(x=>x.length===2),'mesh edge incidence');
 let B=[],W=[],wid=new Map(),sizes=[0,0,0];const color=v=>{let [x,y]=v.split(',').map(Number);return (Math.abs(x)+2*Math.abs(y))%3};
 F.forEach((f,i)=>f.forEach((a,j)=>{let b=f[(j+1)%3];B.push([i,a,b]);W.push([i,b,a]);let c=color(a);wid.set(key([i,b,a]),[c,sizes[c]++])}));
 A(sizes.every(x=>x===F.length),'balanced colors');
 const wi=new Map(W.map((w,j)=>[key(w),j])),m=B.length,rotation=seq(2*m).map(()=>[]),T=[],truth=[];
 for(let t=0;t<m;t++){let [i,a,b]=B[t],c=F[i].find(v=>v!==a&&v!==b),j=E.get(key([a,b].sort())).find(v=>v!==i);let w=[[i,b,a],[i,a,c],[j,a,b]],ids=w.map(x=>wi.get(key(x)));A(ids.every(x=>x!==undefined),'missing white');rotation[t]=ids.map(x=>m+x);ids.forEach((x,q)=>{rotation[m+x][q]=t});let z=w.map(x=>wid.get(key(x))).sort((u,v)=>u[0]-v[0]);A(z.every((x,q)=>x[0]===q),'source color');T.push(z.map(x=>x[1]));truth.push(color(b))}
 for(let i=m;i<2*m;i++)rotation[i].reverse();
 let seen=new Set(),faces=0;for(let u=0;u<2*m;u++)for(let v of rotation[u]){if(seen.has(key([u,v])))continue;faces++;let a=u,b=v;while(!seen.has(key([a,b]))){seen.add(key([a,b]));let ix=rotation[b].indexOf(a);A(ix>=0,'not reciprocal');[a,b]=[b,rotation[b][(ix+1)%3]]}A(a===u&&b===v,'bad face walk')}
 A(2*m-3*m+faces===2&&seen.size===6*m,'not sphere');A(new Set(T.map(key)).size===m,'duplicate source');
 return {T,n:F.length,truth,faces}
}
function owners(T,n){let O=seq(3*n).map(()=>[]);T.forEach((t,i)=>t.forEach((v,c)=>O[c*n+v].push(i)));return O}
function cover(T,n,S){return S.length===n&&seq(3).every(c=>new Set(S.map(i=>T[i][c])).size===n)}
function close(T,n,guard){
 let p=Array(T.length).fill(-1),O=owners(T,n),calls=0;for(let [i,b] of guard)p[i]=b;
 function match(a,b){
  calls++;let adj=seq(n).map(()=>new Set());T.forEach((t,i)=>{if(p[i]!==0)adj[t[a]].add(t[b])});let r=Array(n).fill(-1);
  function aug(x,seen){for(let y of adj[x])if(!seen.has(y)){seen.add(y);if(r[y]<0||aug(r[y],seen)){r[y]=x;return true}}return false}
  for(let x=0;x<n;x++)if(!aug(x,new Set()))return false;
  let D=adj.map(v=>[...v].map(y=>r[y])),R=seq(n).map(()=>[]);D.forEach((v,x)=>v.forEach(y=>R[y].push(x)));
  let vis=new Set(),ord=[];function dfs(x){if(vis.has(x))return;vis.add(x);for(let y of D[x])dfs(y);ord.push(x)}seq(n).forEach(dfs);
  let comp=Array(n).fill(-1);function rev(x,c){if(comp[x]>=0)return;comp[x]=c;for(let y of R[x])rev(y,c)}ord.reverse().forEach((x,c)=>rev(x,c));
  for(let i=0;i<T.length;i++)if(p[i]!==0&&comp[T[i][a]]!==comp[r[T[i][b]]]){if(p[i]===1)return false;p[i]=0}return true
 }
 while(true){let before=p.join(',');for(let q of O){let live=q.filter(i=>p[i]!==0),yes=q.filter(i=>p[i]===1);if(!live.length||yes.length>1)return {no:true,p,calls};if(yes.length){for(let i of live)if(i!==yes[0])p[i]=0}else if(live.length===1)p[live[0]]=1}
 for(let [a,b] of [[0,1],[0,2],[1,2]])if(!match(a,b))return {no:true,p,calls};if(before===p.join(','))return {no:false,p,calls}}
}
function acquire(T,n){let O=owners(T,n),D=seq(T.length).map(()=>new Set()),rows=new Set(O.map(x=>key(x.slice().sort((a,b)=>a-b))));O.forEach(q=>q.forEach(i=>q.forEach(j=>{if(i!==j)D[i].add(j)})));let C=[];for(let a=0;a<T.length;a++)for(let b of D[a])if(b>a)for(let c of D[b])if(c>b&&D[a].has(c)&&!rows.has(key([a,b,c])))C.push([a,b,c]);let count=Array(T.length).fill(0);C.forEach(q=>q.forEach(i=>count[i]++));return C.length===n&&count.every(x=>x===1)?C:null}
function terminal(T,n,C,p){
 let loc=Array(T.length),edges=new Map(),adj=C.map(()=>[]);C.forEach((q,i)=>q.forEach((t,s)=>loc[t]=[i,s]));
 for(let q of owners(T,n)){let G=[...new Set(q.map(t=>loc[t][0]))].sort((a,b)=>a-b);if(G.length>2)return {status:'UNKNOWN',reason:'three-group owner'};if(G.length===1){if(q.length!==3)return {status:'UNKNOWN',reason:'noncubic owner'};continue}let [i,j]=G,k=key(G);if(!edges.has(k))edges.set(k,{i,j,R:seq(3).flatMap(a=>seq(3).map(b=>[a,b]))});let e=edges.get(k);e.R=e.R.filter(([a,b])=>q.reduce((s,t)=>s+Number(loc[t][0]===i?loc[t][1]===a:loc[t][1]===b),0)===1)}
 for(let e of edges.values()){if(!e.R.length)return {status:'NO',sols:[]};if(new Set(e.R.map(x=>x[0])).size===e.R.length&&new Set(e.R.map(x=>x[1])).size===e.R.length){adj[e.i].push([e.j,new Map(e.R)]);adj[e.j].push([e.i,new Map(e.R.map(([a,b])=>[b,a]))])}}
 let Q=[0],seen=new Set(Q);for(let a of Q)for(let [b] of adj[a])if(!seen.has(b)){seen.add(b);Q.push(b)}if(Q.length!==C.length)return {status:'UNKNOWN',reason:'disconnected permutation graph'};
 let sols=[];for(let s=0;s<3;s++){let d=Array(C.length).fill(-1),Q=[0];d[0]=s;let ok=true;for(let a of Q)for(let [b,M] of adj[a]){let x=M.get(d[a]);if(x===undefined){ok=false;continue}if(d[b]<0){d[b]=x;Q.push(b)}else if(d[b]!==x)ok=false}if(!ok||d.includes(-1))continue;if(![...edges.values()].every(e=>e.R.some(([a,b])=>d[e.i]===a&&d[e.j]===b)))continue;let S=C.map((q,i)=>q[d[i]]),set=new Set(S);if(p.some((b,i)=>b!==-1&&Number(set.has(i))!==b))continue;A(cover(T,n,S),'incorrect lift');sols.push(S)}
 return {status:sols.length?'YES':'NO',roots:3,sols,blocks:C.length,relations:edges.size}
}

let out=[];
function quotient(T,n,C){
 let rows=owners(T,n).concat(C||[]),p=seq(T.length),unions=0,passes=0;
 function root(a){while(p[a]!==a){p[a]=p[p[a]];a=p[a]}return a}
 while(true){let changed=false;passes++;let map=new Map();for(let q of rows){let r=q.map(root).sort((a,b)=>a-b);A(new Set(r).size===3&&r.length===3,'unexpected repeated class');for(let i=0;i<3;i++){let a=r[i],k=key(r.filter((_,j)=>i!==j));if(map.has(k)){let b=root(map.get(k)),c=root(a);if(b!==c){p[b]=c;unions++;changed=true;break}}else map.set(k,a)}if(changed)break}if(!changed)break}
 let roots=[...new Set(seq(T.length).map(root))];A(roots.length===3,'not three classes');let S=roots.map(r=>seq(T.length).filter(i=>root(i)===r));A(S.every(s=>cover(T,n,s)),'quotient invalid');
 return {classes:roots.length,unions,passes,covers:S}
}
for(let k of [1,2,4,8]){let {T,n}=mesh(k),C=acquire(T,n),q=quotient(T,n,C);out.push({family:'flag',k,triples:T.length,unions:q.unions,passes:q.passes,classes:q.classes})}
for(let m of [12,24,48,96,192,384,768,1536]){
 let T=seq(m).map(i=>[(i+m-1)%m,i,(i+1)%m].sort((a,b)=>a%3-b%3).map(x=>Math.floor(x/3))),n=m/3;
 A(new Set(T.map(key)).size===m,'duplicate prism');
 let C=acquire(T,n);A(C===null,'prism nonowner cover unexpectedly recognized');
 let c=close(T,n,[]);A(!c.no&&c.p.every(b=>b===-1),'prism closure changed');
 let q=quotient(T,n,[]);A(q.covers.every(s=>s.every(i=>i%3===s[0]%3)),'not periodic');
 let g=[[0,0],[Math.floor(m/2)+1,0],[m-1,0]];A(new Set(g.map(x=>x[0]%3)).size===3,'bad guards');let bad=close(T,n,g);let good=close(T,n,[[0,0]]);
 A(!good.no,'SAT neighbor lost');A(q.covers.filter(s=>!s.includes(0)).length===2,'wrong guarded SAT count');A(q.covers.every(s=>g.some(x=>s.includes(x[0]))),'wrong guarded NO count');
 out.push({family:'prism',triples:m,classes:q.classes,unions:q.unions,passes:q.passes,baseMatchingCalls:c.calls,nonownerCover:false,guardedSAT:2,guardedNO:0,negativeClosureNO:bad.no,negativeGuard:g})
}
return {checks,rows:out}
}
console.log(JSON.stringify(audit(),null,2));