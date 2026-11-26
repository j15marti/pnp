// N4FN08: source-only signed/free cut profiles. Generator prefix adapted from ES12 and DP from FN07.
let checks=0;function ok(b){checks++;if(!b)throw Error("check "+checks)}
const P=[[[0,1,2],[3,4,5],[6,7,8]],[[0,3,6],[1,4,7],[2,5,8]],[[0,4,8],[1,5,6],[2,3,7]],[[0,5,7],[1,3,8],[2,4,6]]], C=P.flat(), Z=[0,0,0], E=[[0,1,1],[0,0,0],[0,1,1],[0,0,1],[0,0,1],[0,1,0],[0,0,1],[0,1,1],[0,1,0],[0,1,0],[0,0,0],[0,1,1]], ag=[1,0,1,0,0,1,0,1,0,1,1,0,1,0,0,0,1,0],mod=[0,0,0,1,1,1,1,0,0];
function nae(a){return a.some(v=>v!==a[0])}
function valid(rows,w){return rows.every(([p,c])=>nae(c.map(v=>w[v])))}
function components(rows,n){let g=Array.from({length:n},()=>[]),id=new Int32Array(n).fill(-1),parts=[];for(let [,c] of rows)for(let v of c)for(let u of c)if(v!==u)g[v].push(u);for(let i=0;i<n;i++)if(id[i]<0){let q=[i];id[i]=parts.length;for(let j=0;j<q.length;j++)for(let u of g[q[j]])if(id[u]<0){id[u]=id[i];q.push(u)}parts.push(q)}return {id,parts}}
function auth(rows,n,connected=true){ok(rows.length===4*n/3);let counts=Array.from({length:4},()=>new Uint8Array(n)),pairs=new Set;for(let [p,c] of rows){ok(p>=0&&p<4&&c.length===3&&new Set(c).size===3);for(let v of c){ok(Number.isInteger(v)&&v>=0&&v<n);counts[p][v]++}for(let i=0;i<3;i++)for(let j=0;j<i;j++){let key=Math.min(c[i],c[j])+":"+Math.max(c[i],c[j]);ok(!pairs.has(key));pairs.add(key)}}ok(counts.every(a=>a.every(x=>x===1)));if(connected)ok(components(rows,n).parts.length===1)}
function ring(k,neg=false){let rows=[],w=[],ports=[];for(let i=0;i<k;i++){let o=27*i;for(let j=0;j<12;j++)if(j!==2)rows.push([Math.floor(j/3),C[j].map(v=>o+v),neg?Z:E[j]]);for(let h=1;h<=2;h++)for(let j=2;j<12;j++)rows.push([Math.floor(j/3),C[j].map(v=>o+9*h+v),Z]);rows.push([0,[o+9,o+19,o+20],[1,0,0]],[0,[o+18,o+10,o+11],Z],[0,[o+6,o+22,o+8],neg?Z:E[2]],[0,[o+12,o+7,o+23],Z]);ports.push(rows.length);rows.push([0,[27*((i+1)%k)+21,o+13,o+14],Z]);w.push(...ag,...mod.flatMap(v=>[v,v]),...mod.flatMap(v=>[v^1,v^1]))}return {rows,w,ports}}
function lift(rows){return rows.flatMap(([p,c,e])=>[0,1].map(t=>[p,c.map((v,i)=>2*v+(t^e[i]))]))}
function compile(F,n){let rows=[],pool=[],splice=[],component=components(F,n);for(let i=0;i<3*n;i++)for(let j=2;j<12;j++)rows.push([Math.floor(j/3),C[j].map(v=>v+9*i),Z]);for(let i=0;i<n;i++){let a=27*i,b=a+9,c=a+18;rows.push([0,[a,a+1,b+3],Z],[0,[c+3,c+4,b],Z]);pool.push([[a+2,b+1,b+2,c,c+1,c+2],[a+3,a+4,a+5,b+4,b+5,c+5]])}for(let [j,c] of F)for(let r=0;r<3;r++){let s=(j<2?r===2:r!==0)?1:0;if(r===0&&splice[component.id[c[0]]]===undefined)splice[component.id[c[0]]]=rows.length;rows.push([0,c.map(i=>pool[i][s].pop()),Z])}ok(pool.every(p=>p.every(a=>a.length===0)));return {rows,splice,component}}
function hard(F,n,w){let c=compile(F,n),q=ring(n),o=27*n,rows=c.rows.concat(q.rows.map(([p,a,e])=>[p,a.map(v=>v+o),e]));let mask=Array(o).fill(0).concat(q.w.filter((_,i)=>i%2===0).map((v,i)=>v^q.w[2*i+1]));if(w){w=[...w];for(let h=0;h<c.splice.length;h++){let v=rows[c.splice[h]][1][0],i=Math.floor(v/27),sign=(v%9>=3&&v%9<6)?1:0;if((w[i]^sign)!==1)for(let j of c.component.parts[h])w[j]^=1}ok(valid(F,w))}
for(let h=0;h<c.splice.length;h++){let a=rows[c.splice[h]][1],b=rows[c.rows.length+q.ports[h]][1];[a[0],b[1]]=[b[1],a[0]]}
let W=w?w.flatMap(z=>Array.from({length:3},()=>[z,z,z,1-z,1-z,1-z,0,0,1]).flat().flatMap(v=>[v,v])).concat(q.w):null;
auth(rows,54*n);let phys=lift(rows);auth(phys,108*n);
if(W){ok(valid(phys,W));ok(mask.every((d,i)=>d===(W[2*i]^W[2*i+1])));ok(valid(F,Array.from({length:n},(_,i)=>W[54*i])))}
return {rows,mask,phys,W}}
function closure(rows,d){let adj=Array.from({length:d.length},()=>[]),uniform=[];for(let [p,c,e] of rows){let b=c.map(v=>d[v]);if(b.every(x=>x===b[0])){uniform.push([p,c,e]);continue}let [i,j]=[[0,1],[0,2],[1,2]].find(([i,j])=>b[i]===b[j]);let s=1^(e[i]&b[i])^(e[j]&b[j]);adj[c[i]].push([c[j],s]);adj[c[j]].push([c[i],s])}let rep=new Int32Array(d.length).fill(-1),phase=new Uint8Array(d.length);for(let i=0;i<d.length;i++)if(rep[i]<0){rep[i]=i;let q=[i];for(let j=0;j<q.length;j++){let u=q[j];for(let [v,s] of adj[u]){let b=phase[u]^s;if(rep[v]<0){rep[v]=i;phase[v]=b;q.push(v)}else ok(phase[v]===b)}}}return {adj,uniform,rep,phase}}
function word(i,n){return Array.from({length:n},(_,j)=>(i>>j)&1)}

function solve(rows,n,cap=16){let f=Array.from({length:n},()=>new Set),g=Array.from({length:n},()=>new Set),D=new Uint8Array(n).fill(3),live=new Uint8Array(n).fill(1),hist=[],maxwidth=0,work=0,forced=0;
function add(s,T){let a={s,T};for(let v of s)f[v].add(a);return a}
function del(a){for(let v of a.s)f[v].delete(a)}
let initial=[];for(let [p,s,sg] of rows){initial.push(add(s,Uint8Array.from({length:8},(_,i)=>Number(nae(sg.map((d,j)=>d^((i>>j)&1)))))));for(let v of s)for(let u of s)if(u!==v)g[v].add(u)}
function closure(queue){for(let t=0;t<queue.length;t++){let a=queue[t],sup=new Uint8Array(a.s.length);let any=false;for(let i=0;i<a.T.length;i++)if(a.T[i]){work++;if(a.s.some((v,j)=>!(D[v]&(1<<((i>>j)&1)))))continue;any=true;for(let j=0;j<a.s.length;j++)sup[j]|=1<<((i>>j)&1)}if(!any)return false;for(let j=0;j<a.s.length;j++){let v=a.s[j],d=D[v]&sup[j];if(!d)return false;if(d!==D[v]){D[v]=d;forced++;for(let b of f[v])queue.push(b)}}}return true}
D[0]=1;if(!closure(initial))return {answer:false,maxwidth,work,forced};
for(let step=0;step<n;step++){let v=-1,d=n+1;for(let i=0;i<n;i++)if(live[i]&&g[i].size<d){v=i;d=g[i].size;if(d===0)break}if(d>cap)return {answer:null,maxwidth,work,forced};maxwidth=Math.max(maxwidth,d);let ns=[...g[v]].sort((a,b)=>a-b),old=[...f[v]],idx=new Map(ns.map((x,j)=>[x,j])),maps=old.map(a=>a.s.map(x=>x===v?-1:idx.get(x))),T=new Uint8Array(2**d),choice=new Uint8Array(T.length).fill(2);
for(let i=0;i<T.length;i++){if(ns.some((u,j)=>!(D[u]&(1<<((i>>j)&1)))))continue;for(let b=0;b<2;b++)if(D[v]&(1<<b)){let good=true;for(let h=0;h<old.length;h++){let key=0;for(let j=0;j<maps[h].length;j++){let r=maps[h][j];key|=(r<0?b:(i>>r)&1)<<j}work++;if(!old[h].T[key]){good=false;break}}if(good){T[i]=1;choice[i]=b;break}}}
if(!T.some(x=>x))return {answer:false,maxwidth,work,forced};for(let a of old)del(a);for(let u of ns){g[u].delete(v);for(let z of ns)if(u!==z)g[u].add(z)}live[v]=0;g[v].clear();hist.push({v,ns,choice});if(ns.length&&!closure([add(ns,T)]))return {answer:false,maxwidth,work,forced}}
let w=new Uint8Array(n);for(let h=hist.length-1;h>=0;h--){let {v,ns,choice}=hist[h],j=ns.reduce((a,u,k)=>a|(w[u]<<k),0);ok(choice[j]<2);w[v]=choice[j]}ok(rows.every(([p,c,sg])=>nae(c.map((v,j)=>w[v]^sg[j])))&&w[0]===0);return {answer:true,maxwidth,work,forced,w}}


let seed=20261126;
function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
function perm(n){let a=Array.from({length:n},(_,i)=>i);for(let i=n-1;i>0;i--){let j=rnd(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
function get(s){return [0,1].filter(d=>s&(1<<d))}
function maskxor(a,b){let s=0;for(let x of get(a))for(let y of get(b))s|=1<<(x^y);return s}
function verify(G,W){if(!W)return;for(let r of G.rows){let y=W.y.get(r.id);ok(!!y&&nae(y));for(let j=0;j<3;j++)ok(!!(r.s[j]&(1<<(W.x.get(r.c[j])^y[j]))))}}
function raw(F,n){let a=perm(n),p=perm(4);return {vs:Array.from({length:n},(_,i)=>i),rows:perm(F.length).map((i,id)=>({id,p:p[F[i][0]],c:F[i][1].map(v=>a[v]),s:[1,1,1]})),a}}
function findCut(G,stats){let n=G.vs.length,ix=new Map(G.vs.map((v,i)=>[v,i])),N=n+G.rows.length,adj=Array.from({length:N},()=>[]),E=[];
for(let i=0;i<G.rows.length;i++)for(let j=0;j<3;j++){let v=ix.get(G.rows[i].c[j]),u=n+i,id=E.length;E.push([v,u,i,j]);adj[v].push(id);adj[u].push(id)}
let par=new Int32Array(N).fill(-2),pe=new Int32Array(N).fill(-1),q=[0];par[0]=-1;for(let i=0;i<q.length;i++){let u=q[i];for(let e of adj[u]){let v=E[e][0]^E[e][1]^u;if(par[v]===-2){par[v]=u;pe[v]=e;q.push(v)}}}ok(q.length===N);
let sig=new Int32Array(E.length),acc=new Int32Array(N),tree=new Set(pe);function hash(i){i=(i+1)|0;i=Math.imul(i^(i>>>16),0x45d9f3b);i=Math.imul(i^(i>>>16),0x45d9f3b);return i^(i>>>16)}
for(let i=0;i<E.length;i++)if(!tree.has(i)){let [v,u]=E[i];sig[i]=hash(i);acc[v]^=sig[i];acc[u]^=sig[i]}
for(let i=q.length-1;i>0;i--){let u=q[i];sig[pe[u]]=acc[u];acc[par[u]]^=acc[u]}
let groups=new Map;for(let i=0;i<E.length;i++){if(!groups.has(sig[i]))groups.set(sig[i],[]);groups.get(sig[i]).push(i)}
let best=null;for(let group of groups.values())if(group.length>=2)for(let i=0;i<group.length;i++)for(let j=i+1;j<group.length;j++){let a=group[i],b=group[j];stats.cutTests++;let vis=new Uint8Array(N),Q=[0];vis[0]=1;for(let k=0;k<Q.length;k++){let u=Q[k];for(let e of adj[u])if(e!==a&&e!==b){let v=E[e][0]^E[e][1]^u;if(!vis[v]){vis[v]=1;Q.push(v)}}}if(Q.length===N)continue;let sz=Math.min(Q.length,N-Q.length);if(!best||sz>best.sz){if(Q.length>N-Q.length)vis=vis.map(x=>1-x);best={sz,vis,a:E[a],b:E[b]}}// do not enumerate every actual cut on huge rings
if(best&&best.sz>=Math.min(200,N/4))return best;
}return best}
function split(G,C){let n=G.vs.length,[a,b]=[C.a,C.b];if(!C.vis[a[0]])[a,b]=[b,a];ok(C.vis[a[0]]&&!C.vis[a[1]]&&!C.vis[b[0]]&&C.vis[b[1]]);
let rA=G.rows[b[2]],rB=G.rows[a[2]],u=G.vs[a[0]],v=G.vs[b[0]],sa=rB.s[a[3]],sb=rA.s[b[3]];ok(rA.p===rB.p);
let side=(d,rr,j,w)=>({vs:G.vs.filter((_,i)=>C.vis[i]===d),rows:G.rows.filter((_,i)=>C.vis[n+i]===d).map(r=>r.id===rr.id?{...r,c:r.c.map((x,k)=>k===j?w:x),s:[...r.s]}:r)});
let A=side(1,rA,b[3],u),B=side(0,rB,a[3],v);
let aa=A.rows.find(r=>r.id===rA.id),bb=B.rows.find(r=>r.id===rB.id);
return {A,B,aa,bb,u,v,ja:b[3],jb:a[3],sa,sb}}
function normal(G,stats){let n=G.vs.length,idx=new Map(G.vs.map((v,i)=>[v,i])),rows=G.rows.filter(r=>r.s.every(s=>s!==3)).map(r=>[r.p,r.c.map(v=>idx.get(v)),r.s.map(s=>s===2?1:0)]);
let p=Array.from({length:n},(_,i)=>i),d=new Uint8Array(n),sz=new Uint32Array(n).fill(1);
function find(x){if(p[x]===x)return [x,0];let [u,t]=find(p[x]);d[x]^=t;p[x]=u;return [u,d[x]]}
function join(x,y,b){let [a,c]=find(x),[u,v]=find(y);if(a===u)return (c^v)===b?0:-1;if(sz[a]<sz[u])[a,u]=[u,a];p[u]=a;d[u]=b^c^v;sz[a]+=sz[u];stats.joins++;return 1}
let incident=Array.from({length:n},()=>[]);for(let i=0;i<rows.length;i++)if(rows[i][2].every(x=>x===0)&&new Set(rows[i][1]).size===3)for(let v of rows[i][1])incident[v].push(i);
let seen=new Set;
for(let v=0;v<n;v++){let S=[...new Set([v,...incident[v].flatMap(i=>rows[i][1])])].sort((a,b)=>a-b);if(S.length!==9)continue;let key=S.join(",");if(seen.has(key))continue;seen.add(key);let ss=new Set(S),ri=[...new Set(S.flatMap(u=>incident[u]))].filter(i=>rows[i][1].every(w=>ss.has(w)));if(ri.length<10)continue;let ix=new Map(S.map((u,i)=>[u,i])),E=new Set;let dup=false;for(let i of ri)for(let j=0;j<3;j++)for(let k=j+1;k<3;k++){let [a,b]=[ix.get(rows[i][1][j]),ix.get(rows[i][1][k])].sort((x,y)=>x-y),e=a*9+b;if(E.has(e))dup=true;E.add(e)}if(dup)continue;if(ri.length>=11)return null;
let M=Array.from({length:9},()=>[]);for(let i=0;i<9;i++)for(let j=i+1;j<9;j++)if(!E.has(i*9+j)){M[i].push(j);M[j].push(i)}let a=M.findIndex(x=>x.length===2);if(a<0)continue;let L=[a,...M[a]],R=M.map((x,i)=>x.length===2&&!L.includes(i)?i:-1).filter(i=>i>=0);let tri=A=>A.length===3&&A.every(i=>M[i].length===2&&A.every(j=>j===i||M[i].includes(j)));if(!tri(L)||!tri(R)||M.some((x,i)=>x.length&&!L.includes(i)&&!R.includes(i)))continue;for(let i of L)if(join(S[a],S[i],0)<0)return null;for(let i of R)if(join(S[a],S[i],1)<0)return null;stats.modules++}
let res;for(;;){res=[];let changed=0,pairs=new Map;for(let [c,v,s] of rows){let w=v.map((x,i)=>{let [r,b]=find(x);return [r,b^s[i]]});let drop=false,eq=null;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)if(w[i][0]===w[j][0]){if(w[i][1]!==w[j][1])drop=true;else eq=[i,j]}if(drop)continue;if(eq){let i=eq[0],j=3-eq[0]-eq[1],r=join(w[i][0],w[j][0],1^w[i][1]^w[j][1]);if(r<0)return null;changed+=r;continue}res.push([c,w.map(x=>x[0]),w.map(x=>x[1])]);}
// opposite-pivot pair: normalize by first sign, compare same triple; each two different relative sign patterns forces a pair
if(!changed){for(let [c,v,s] of res){let t=v.map((x,i)=>[x,s[i]]).sort((a,b)=>a[0]-b[0]),k=t.map(x=>x[0]).join(","),z=t.map(x=>x[1]^t[0][1]),prev=pairs.get(k)||[];for(let a of prev){let diff=z.map((b,i)=>b^a[i]);if(diff.every(x=>x===0))continue;let ij=[[0,1],[0,2],[1,2]].find(([i,j])=>diff[i]===diff[j]),[i,j]=ij;let q=join(t[i][0],t[j][0],1^z[i]^z[j]);if(q<0)return null;changed+=q}prev.push(z);pairs.set(k,prev)}}
if(!changed)break}
let roots=[...new Set(G.vs.map((_,i)=>find(i)[0]))],rid=new Map(roots.map((r,i)=>[r,i]));let unique=new Map;for(let [c,v,s] of res){let t=v.map((x,i)=>[rid.get(x),s[i]]).sort((a,b)=>a[0]-b[0]),z=t.map(x=>x[1]^t[0][1]),key=t.map((x,i)=>x[0]+":"+z[i]).join(",");unique.set(key,[c,t.map(x=>x[0]),z])}
return {rows:[...unique.values()],roots,rid,find}}
function terminal(G,R,stats,cap){stats.terminals++;let w=solve(R.rows,R.roots.length,cap);stats.maxwidth=Math.max(stats.maxwidth,w.maxwidth);stats.tableWork+=w.work||0;if(w.answer===null)return undefined;if(!w.answer)return null;let x=new Map(G.vs.map((v,i)=>{let [r,b]=R.find(i);return [v,w.w[R.rid.get(r)]^b]})),y=new Map;
for(let r of G.rows){let a=r.c.map((v,j)=>x.get(v)^(r.s[j]===2?1:0));if(!nae(a)){let j=r.s.indexOf(3);ok(j>=0);a[j]^=1}y.set(r.id,a)}let W={x,y};verify(G,W);return W}
function rec(G,stats,cap){stats.calls++;let size=G.vs.length+G.rows.length;stats.mass+=size;stats.squares+=size*size;
let R=normal(G,stats);if(!R)return null;
// exact independent terminal when no nonlinear rows remain; else discover cuts before attempting wider terminal
if(!R.rows.length)return terminal(G,R,stats,cap);
let C=findCut(G,stats);if(!C)return terminal(G,R,stats,cap);
stats.splits++;let {A,B,aa,bb,u,v,ja,jb,sa,sb}=split(G,C),as=A.vs.length+A.rows.length,bs=B.vs.length+B.rows.length;ok(as<=bs&&2*as*as+bs*bs<=size*size-1);
let W=[],unknown=false,allowed=0;for(let t=0;t<2;t++){aa.s[ja]=1<<t;let w=rec(A,stats,cap);W[t]=w;if(w===undefined)unknown=true;else if(w)allowed|=maskxor(maskxor(1<<t,sa),sb)}
if(unknown)return undefined;stats.profiles[allowed]++;if(!allowed)return null;bb.s[jb]=allowed;let z=rec(B,stats,cap);if(!z)return z;let tB=z.x.get(v)^z.y.get(bb.id)[jb],dA=-1,s1=-1;for(let t=0;t<2;t++)if(W[t])for(let i of get(sa))for(let j of get(sb))if((t^i^j)===tB){dA=t;s1=i}
ok(dA>=0);let a=W[dA],flip=a.x.get(u)^z.y.get(bb.id)[jb]^s1;for(let [k,w] of a.x)z.x.set(k,w^flip);for(let [k,w] of a.y)z.y.set(k,w.map(x=>x^flip));verify(G,z);return z}
function run(name,F,n,expected,cap=16){auth(F,n,false);let G=raw(F,n),stats={calls:0,splits:0,cutTests:0,modules:0,joins:0,terminals:0,maxwidth:0,tableWork:0,mass:0,squares:0,profiles:[0,0,0,0]};let w=rec(G,stats,cap),answer=w===undefined?null:!!w;if(answer!==null)ok(answer===expected);if(w){let a=G.a.map(v=>w.x.get(v));ok(valid(F,a))}
return {name,n,expected,answer,...stats}}

let profileChecks=0;for(let A=0;A<4;A++)for(let e=1;e<=3;e++)for(let f=1;f<=3;f++)for(let x=0;x<2;x++)for(let y=0;y<2;y++){
let direct=false;for(let u=0;u<2;u++)for(let v=0;v<2;v++)if((A&(1<<(u^v)))&&(e&(1<<(u^y)))&&(f&(1<<(x^v))))direct=true;
ok(direct===!!(maskxor(maskxor(A,e),f)&(1<<(x^y))));profileChecks++}
function cyclicGrid(p){let L=Math.floor(Math.sqrt(p));return [0,1,L,L+1].flatMap((s,j)=>Array.from({length:p},(_,i)=>[j,[i,p+(i+s)%p,2*p+(i+2*s)%p]]))}
function ternary(G){let n=G.vs.length,bas=new Map,ops=0;
for(let r of G.rows){let z=new Map(r.c.map(v=>[v,1]));while(z.size){let k=Infinity;for(let t of z.keys())if(t<k)k=t;let b=z.get(k);if(!bas.has(k)){if(b===2)for(let [j,v] of z)z.set(j,2*v%3);bas.set(k,z);break}for(let [j,v] of bas.get(k)){let w=((z.get(j)||0)-b*v+6)%3;if(w)z.set(j,w);else z.delete(j);ops++}}}
let free=G.vs.filter(v=>!bas.has(v)),order=[...bas.keys()].sort((a,b)=>b-a);let wit=null;for(let f of free){let w=new Uint8Array(n);w[f]=1;for(let k of order){let t=0;for(let [j,v] of bas.get(k))if(j!==k)t=(t+v*w[j])%3;w[k]=(3-t)%3}if(G.rows.every(r=>new Set(r.c.map(v=>w[v])).size===3)){wit=Array.from(w,x=>Number(x===0));break}}
if(wit)ok(G.rows.every(r=>nae(r.c.map(v=>wit[v]))));return {nullity:free.length,witness:!!wit,ops}}
let out=[];for(let neg of [false,true]){let q=ring(8,neg),F=lift(q.rows),H=hard(F,432,neg?null:q.w);out.push(run("ES12-8"+(neg?"-NO":"-YES"),H.phys,46656,!neg))}
let prime=[];for(let p of [29,101,401,1601]){let F=cyclicGrid(p),n=3*p;auth(F,n);let G=raw(F,n),stats={cutTests:0,joins:0,modules:0};let N=normal(G,stats);ok(N&&N.roots.length===n&&!findCut(G,stats));let z=ternary(G);ok(z.nullity===2&&z.witness);let r=solve(N.rows,N.roots.length,16);if(r.answer!==null)ok(r.answer);prime.push({p,n,L:Math.floor(Math.sqrt(p)),twoCut:false,phaseJoins:stats.joins,ternary:z,cap16Answer:r.answer,maxwidth:r.maxwidth,tableWork:r.work})}
console.log(JSON.stringify({seed:20261126,checks,profileChecks,out,prime}));