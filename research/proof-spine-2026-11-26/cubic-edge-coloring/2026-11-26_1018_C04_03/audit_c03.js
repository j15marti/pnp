function runAudit(){
 const P=[ [0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0] ];
 let checks=0;function ck(x){checks++;if(!x)throw Error("assert "+checks)}
 function pole(n,L,E,S){return {n,L,E,S}}
 function verify(H,w,c){if(!c||c.length!==H.E.length)return false;let a=Array.from({length:H.n},()=>[]);H.E.forEach(([u,v],i)=>{a[u].push(c[i]);a[v].push(c[i])});H.S.forEach((u,i)=>a[u].push(w[i]));return a.every(v=>v.length===3&&new Set(v).size===3&&v.every(c=>c>=0&&c<3))}
 function exact(H,w){let mask=Array(H.n).fill(0),c=Array(H.E.length).fill(-1);for(let i=0;i<w.length;i++){let u=H.S[i],b=1<<w[i];if(mask[u]&b)return null;mask[u]|=b}function rec(k){if(k===H.E.length)return c.slice();let j=-1,best=8,dm=0;for(let i=0;i<c.length;i++)if(c[i]<0){let[u,v]=H.E[i],d=7&~(mask[u]|mask[v]),cnt=(d&1)+((d>>1)&1)+((d>>2)&1);if(cnt<best){best=cnt;j=i;dm=d}}if(!dm)return null;let[u,v]=H.E[j];for(let t=0;t<3;t++)if(dm&(1<<t)){c[j]=t;mask[u]|=1<<t;mask[v]|=1<<t;let r=rec(k+1);if(r)return r;mask[u]^=1<<t;mask[v]^=1<<t;c[j]=-1}return null}return rec(0)}
 function balanced(H,w){let d=[0,0,0],s=H.L.reduce((a,b)=>a+(b?1:-1),0);H.S.forEach((u,i)=>d[w[i]]+=H.L[u]?1:-1);return d.every(x=>x===s)}
 function match(H,w,a){let D=new Set();for(let i=0;i<w.length;i++)if(w[i]===a){let v=H.S[i];if(D.has(v))return null;D.add(v)}let adj=Array.from({length:H.n},()=>[]);H.E.forEach(([u,v],i)=>{if(D.has(u)||D.has(v))return;if(!H.L[u])[u,v]=[v,u];adj[u].push([v,i])});let rv=Array(H.n).fill(-1),re=Array(H.n).fill(-1);function aug(u,seen){for(let[v,i]of adj[u])if(!seen.has(v)){seen.add(v);if(rv[v]<0||aug(rv[v],seen)){rv[v]=u;re[v]=i;return true}}return false}for(let u=0;u<H.n;u++)if(H.L[u]&&!D.has(u)&&!aug(u,new Set()))return null;for(let v=0;v<H.n;v++)if(!H.L[v]&&!D.has(v)&&rv[v]<0)return null;return {D,M:new Set(re.filter(i=>i>=0))}}
 function lift(H,w,a,m){let c=Array(H.E.length).fill(-1),adj=Array.from({length:H.n},()=>[]),pins=Array.from({length:H.n},()=>[]),bs=[0,1,2].filter(i=>i!==a);H.E.forEach(([u,v],i)=>{if(m.M.has(i))c[i]=a;else{adj[u].push(i);adj[v].push(i)}});H.S.forEach((u,i)=>{if(w[i]!==a)pins[u].push(w[i])});function set(i,t){if(c[i]>=0)return c[i]===t;c[i]=t;q.push(i);return true}let q=[];for(let u=0;u<H.n;u++){if(adj[u].length+pins[u].length!==2)return null;if(pins[u].length===2&&pins[u][0]===pins[u][1])return null;if(pins[u].length===1&&!set(adj[u][0],bs.find(x=>x!==pins[u][0])))return null}
 function flush(){while(q.length){let i=q.pop();for(let u of H.E[i])for(let j of adj[u])if(i!==j&&!set(j,bs.find(x=>x!==c[i])))return false}return true}if(!flush())return null;for(let i=0;i<c.length;i++)if(c[i]<0){set(i,bs[0]);if(!flush())return null}return verify(H,w,c)?c:null}
 function easy(H,w){if(!balanced(H,w))return {status:"NO"};let cnt=[0,0,0];for(let x of w)cnt[x]++;let a=cnt.indexOf(Math.max(...cnt));let m=match(H,w,a);if(!m)return {status:"NO"};let c=lift(H,w,a,m);if(c)return {status:"YES",c};if(w.length-cnt[a]<=2)return {status:"NO"};for(let b=0;b<3;b++)if(!match(H,w,b))return {status:"NO"};return {status:"UNKNOWN"}}
 function decomp(H,w,a,cap=12){let m=match(H,w,a);if(!m)return {status:"NO",width:0,maxPorts:0,blocks:0};let first=lift(H,w,a,m);if(first)return {status:"YES",c:first,width:0,maxPorts:0,blocks:0,quick:true};
 let D=m.D,pair=Array(H.n).fill(-1),pairs=[];for(let i of m.M){let [u,v]=H.E[i];pair[u]=pair[v]=pairs.length;pairs.push([u,v])}
 let k=pairs.length,adj=Array.from({length:k},()=>[]),rev=Array.from({length:k},()=>[]);
 H.E.forEach(([u,v])=>{if(D.has(u)||D.has(v))return;if(!H.L[u])[u,v]=[v,u];let x=pair[u],y=pair[v];if(x!==y){adj[x].push(y);rev[y].push(x)}});
 let seen=new Set(),order=[];function dfs(u){seen.add(u);for(let v of adj[u])if(!seen.has(v))dfs(v);order.push(u)}for(let i=0;i<k;i++)if(!seen.has(i))dfs(i);let group=Array(k).fill(-1),groups=[];function rdfs(u,j){group[u]=j;groups[j].push(u);for(let v of rev[u])if(group[v]<0)rdfs(v,j)}for(let u of order.reverse())if(group[u]<0){groups.push([]);rdfs(u,groups.length-1)}
 let g=Array(H.n).fill(-1),blocks=groups.map(ps=>{let V=ps.flatMap(i=>pairs[i]),idx=new Map(V.map((v,i)=>[v,i]));let b={V,idx,E:[],ei:[],S:[],ids:[]};return b});blocks.forEach((b,j)=>b.V.forEach(v=>g[v]=j));
 let bs=[0,1,2].filter(x=>x!==a),fixedBase=new Map(),Dinc=new Map([...D].map(v=>[v,[]])),cross=[];
 H.S.forEach((u,i)=>{let id=H.E.length+i;fixedBase.set(id,w[i]);if(D.has(u))Dinc.get(u).push(id);else{blocks[g[u]].S.push(blocks[g[u]].idx.get(u));blocks[g[u]].ids.push(id)}});
 H.E.forEach(([u,v],i)=>{if(D.has(u))Dinc.get(u).push(i);if(D.has(v))Dinc.get(v).push(i);if(D.has(u)&&D.has(v))return;if(D.has(u)||D.has(v)){let t=D.has(u)?v:u,b=blocks[g[t]];b.S.push(b.idx.get(t));b.ids.push(i);return}if(g[u]===g[v]){let b=blocks[g[u]];b.E.push([b.idx.get(u),b.idx.get(v)]);b.ei.push(i)}else{if(!H.L[u])[u,v]=[v,u];ck(g[u]<g[v]);cross.push([i,g[u],g[v]]);for(let t of[u,v]){let b=blocks[g[t]];b.S.push(b.idx.get(t));b.ids.push(i)}}});
 let width=0,maxPorts=Math.max(0,...blocks.map(b=>b.S.length)),boundR=0;H.S.forEach(u=>{if(!D.has(u)&&!H.L[u])boundR++});H.E.forEach(([u,v])=>{if(D.has(u)&&!D.has(v)&&!H.L[v])boundR++;if(D.has(v)&&!D.has(u)&&!H.L[u])boundR++});for(let j=0;j<blocks.length;j++){let q=cross.filter(([,s,t])=>s<=j&&j<t).length;width=Math.max(width,q)}ck(width<=boundR);ck(maxPorts<=2*boundR);ck(boundR<=4);
 let unknown=false,bc=0,states=0,rows=0;
 for(let mask=0;mask<(1<<D.size);mask++){let fixed=new Map(fixedBase),ok=true,di=0;for(let [u,inc]of Dinc){let j=inc.filter(i=>!(i>=H.E.length&&w[i-H.E.length]===a));if(j.length!==2){ok=false;break}let flip=(mask>>di++)&1;for(let t=0;t<2;t++){let val=bs[t^flip];if(fixed.has(j[t])&&fixed.get(j[t])!==val)ok=false;fixed.set(j[t],val)}}if(!ok)continue;
 let dp=[{f:new Map(),cs:new Map(fixed)}];for(let j=0;j<blocks.length;j++){let b=blocks[j],h=pole(b.V.length,b.V.map(v=>H.L[v]),b.E,b.S),next=new Map(),out=cross.filter(([,s,t])=>s<=j&&j<t).map(x=>x[0]).sort((a,b)=>a-b);let table=[];for(let t=0;t<(1<<b.ids.length);t++){let word=b.ids.map((id,i)=>bs[(t>>i)&1]);if(b.ids.some((id,i)=>fixed.has(id)&&fixed.get(id)!==word[i]))continue;rows++;let r=easy(h,word);if(r.status==="UNKNOWN"&&h.n<=cap){bc++;let c=exact(h,word);r=c?{status:"YES",c}:{status:"NO"}}if(r.status==="UNKNOWN"){unknown=true;continue}if(r.status==="YES")table.push({word,c:r.c})}
 for(let st of dp)for(let r of table){if(b.ids.some((id,i)=>st.f.has(id)&&st.f.get(id)!==r.word[i]))continue;let f=new Map(st.f),cs=new Map(st.cs);b.ids.forEach((id,i)=>{f.set(id,r.word[i]);cs.set(id,r.word[i])});b.ei.forEach((id,i)=>cs.set(id,r.c[i]));let nf=new Map(out.map(id=>[id,f.get(id)]));let key=out.map(id=>nf.get(id)).join("");if(!next.has(key))next.set(key,{f:nf,cs});}dp=[...next.values()];states+=dp.length;if(!dp.length)break}
 if(dp.length){let c=H.E.map((_,i)=>dp[0].cs.get(i));ck(verify(H,w,c));return {status:"YES",c,width,maxPorts,blocks:blocks.length,states,rows,bc,boundR}}}
 return {status:unknown?"UNKNOWN":"NO",width,maxPorts,blocks:blocks.length,states,rows,bc,boundR}
 }
 function words(H){let r=[];for(let i=0;i<3**H.S.length;i++){let t=i,w=[];for(let j=0;j<H.S.length;j++){w.push(t%3);t=Math.floor(t/3)}if(balanced(H,w))r.push(w)}return r}

return {pole,verify,exact,balanced,match,easy,decomp,words};}
const audit = function audit(){
let checks=0;const A=(v,msg)=>{checks++;if(!v)throw Error(msg)};
const ints=Array.from({length:10},(_,i)=>i);
const internal=ints.filter(i=>i!==4).map(i=>[i,(i+1)%10]).concat([[4,7],[5,8],[6,9]]);
function localColor(p){let mask=Array(10).fill(0);for(let i=0;i<4;i++)mask[i]=1<<p[i];mask[4]=mask[5]=8;let c=[];
function rec(k){if(k===internal.length)return true;let [u,v]=internal[k];for(let i=1;i<=3;i++){let b=1<<i;if((mask[u]|mask[v])&b)continue;mask[u]|=b;mask[v]|=b;c[k]=i;if(rec(k+1))return true;mask[u]^=b;mask[v]^=b;}return false;}
A(rec(0),"patch coloring");return c.slice();}
let table={};for(let p of [[3,3,3,3],[1,1,3,3],[2,2,3,3],[3,1,1,3],[3,2,2,3]])table[p.join("")]=localColor(p);
function compile(F){
const r=F.length+4,events=[];
for(let j=0;j<r-1;j++)for(let k=0;k<2;k++)events.push({i:j,j:j+1,key:"p"+j,zero:false});
F.forEach((cl,h)=>{for(let z=0;z<3;z++)events.push({i:z,j:z+1,key:"x"+Math.abs(cl[z]),zero:cl[z]>0});events.push({swap:[3,4+h]});for(let z=2;z>=0;z--)events.push({i:z,j:z+1,key:"x"+Math.abs(cl[z]),zero:cl[z]>0});});
let G=[],group=new Map(),ends=[],count=0;const edge=(u,v,a,b,col)=>G.push({u,v,a,b,col});
for(let cp=0;cp<2;cp++){
let inits=Array(r).fill(-1),tails=Array(r).fill(-1);
for(let ev of events){if(ev.swap){let [i,j]=ev.swap;[tails[i],tails[j]]=[tails[j],tails[i]];continue;}
let base=10*count++,i=ev.i,j=ev.j,p=[i,j],q=ev.zero?[j,i]:[i,j];
if(i===0&&ev.zero){p.reverse();q.reverse();}
let ports=[p[0],q[0],p[1],q[1]],pc=ports.map(x=>x===0?cp+1:3),c=table[pc.join("")];A(!!c,"local port color");
for(let [k,[u,v]] of internal.entries())edge(base+u,base+v,k<9?1:0,k<9?(u%2===0?1:0):1,c[k]);
if(!group.has(ev.key))group.set(ev.key,[]);group.get(ev.key).push(base);
for(let k of [0,2]){let z=ports[k],u=base+k;if(tails[z]===-1)inits[z]=u;else edge(tails[z],u,0,1,pc[k]);}
for(let k of [1,3])tails[ports[k]]=base+k;
}
ends.push([inits,tails]);
}
for(let gs of group.values())for(let i=0;i<gs.length;i++)edge(gs[i]+5,gs[(i+1)%gs.length]+4,1,1,3);
let s=10*count,t=s+1,n=t+1;
for(let k=1;k<r;k++){edge(ends[0][0][k],ends[1][0][k],0,1,3);edge(ends[0][1][k],ends[1][1][k],0,1,3);}
for(let cp=0;cp<2;cp++){edge(s,ends[cp][0][0],0,1,cp+1);edge(t,ends[cp][1][0],0,1,cp+1);}edge(s,t,0,0,3);
let adj=Array.from({length:n},()=>[]),uniq=new Set();for(let [k,e] of G.entries()){A(e.u!==e.v,"loop");let id=Math.min(e.u,e.v)+":"+Math.max(e.u,e.v);A(!uniq.has(id),"duplicate");uniq.add(id);adj[e.u].push(k);adj[e.v].push(k);}
let comp=new Int32Array(n).fill(-1),sz=[],component=0;
const other=(e,u)=>e.u===u?e.v:e.u;
for(let u=0;u<n;u++){let es=adj[u].map(i=>G[i]);A(es.length===3,"cubic");A(new Set(es.map(e=>e.col)).size===3,"proper witness");A(es.reduce((z,e)=>z^e.a,0)===0&&es.reduce((z,e)=>z^e.b,0)===0,"flow");
if(comp[u]>=0)continue;let todo=[u],cnt=0;comp[u]=component;
for(let v of todo){cnt++;for(let i of adj[v])if(G[i].a){let w=other(G[i],v);if(comp[w]<0){comp[w]=component;todo.push(w);}}}sz.push(cnt);component++;}
let seen=new Set([0]),todo=[0];for(let u of todo)for(let i of adj[u]){let v=other(G[i],u);if(!seen.has(v)){seen.add(v);todo.push(v);}}A(seen.size===n,"connected");
let cls=new Map();for(let [key,bases] of group){let c=comp[bases[0]];A(!cls.has(c)&&sz[c]===10*bases.length,"class size");for(let base of bases)for(let z=0;z<10;z++)A(comp[base+z]===c,"physical equality");cls.set(c,key);}
A(sz.filter(z=>z===1).length===2&&sz[comp[s]]===1&&sz[comp[t]]===1,"isolates");
A(G.filter(e=>!e.a&&!e.b).length===1&&!G.at(-1).b,"defect");
return {G,adj,n,s,t,comp,cls,sz,other,group};
}
function evaluate(R,word){let {G,adj,n,s,t,comp,cls,other}=R;
let bit=G.map(e=>e.a?e.b^(word[cls.get(comp[e.u])]||0):e.b);
let visited=new Uint8Array(n),good=true,same=false,odd=0;
for(let u=0;u<n;u++){A(adj[u].reduce((a,k)=>a+bit[k],0)===2,"2-factor");if(visited[u])continue;let todo=[u];visited[u]=1;for(let v of todo)for(let k of adj[v])if(bit[k]){let w=other(G[k],v);if(!visited[w]){visited[w]=1;todo.push(w);}}
if(todo.length%2){good=false;odd++;}if(todo.includes(s))same=todo.includes(t);}
A(good===same,"terminal parity");A(odd===(good?0:2),"odd count");return good;}

return {compile,evaluate,internal};};

console.log(JSON.stringify((function patchAudit(runAudit,audit){
 let {pole,verify,exact,balanced,match,easy,decomp,words}=runAudit(),{compile,evaluate,internal}=audit();
 let H=pole(10,Array.from({length:10},(_,i)=>1-i%2),internal,[0,1,2,3,4,5]);let mask=[],all=words(H),noMarginal=0,dp=0,unknown=0,colors=[];
 for(let w of all){let ref=exact(H,w),r=easy(H,w);if(r.status==="UNKNOWN"){if(!ref)noMarginal++;for(let a=0;a<3;a++){dp++;let z=decomp(H,w,a);if(z.status!=="UNKNOWN"){r=z;break}}}if(r.status==="UNKNOWN")unknown++;else if((r.status==="YES")!==!!ref)throw Error("patch mismatch");if(ref){if(!verify(H,w,ref))throw Error("bad patch lift");mask.push(w.join(""));colors.push(ref)}}
 let clauses=Array.from({length:8},(_,i)=>[1,2,3].map((v,j)=>(i>>j&1)?v:-v));let rows=[];for(let F of[clauses,clauses.slice(0,7).concat([clauses[0]])]){let R=compile(F),accepted=0;for(let m=0;m<8;m++){let w={x1:m&1,x2:m>>1&1,x3:m>>2&1};if(evaluate(R,w))accepted++}
 let c=R.G.map(e=>e.col-1),G=pole(R.n,Array(R.n).fill(0),R.G.map(e=>[e.u,e.v]),[]);if(!verify(G,[],c))throw Error("source coloring");let sites=(R.n-2)/10;
 let chosen=[];for(let j=0;j<sites;j++){let base=j*10,inside=[],w=[];for(let u=0;u<6;u++){let e=R.adj[base+u].map(i=>R.G[i]).find(e=>e.u<base||e.u>=base+10||e.v<base||e.v>=base+10);if(!e)throw Error("missing port");w.push(e.col-1)}let id=mask.indexOf(w.join(""));if(id<0)throw Error("unattained");chosen.push(id);for(let [i,[u,v]]of internal.entries()){let z=R.adj[base+u].find(i=>R.other(R.G[i],base+u)===base+v);c[z]=colors[id][i]}}if(!verify(G,[],c))throw Error("lift failure");rows.push({F,n:R.n,edges:R.G.length,sites,chartAccepted:accepted,originalEdges:G.E,a:R.G.map(e=>e.a),b:R.G.map(e=>e.b),liftedColors:c,tableRows:chosen})}
 return {H,balanceWords:all.length,accepted:mask.length,noMarginal,dp,unknown,mask,colors,rows}
})(runAudit,audit),null,2));
