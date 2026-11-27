// node audit.js -- C08-17 joint cut space and 2SAT audit
function audit(){
let seed=20261126,checks=0,sccCalls=0,gaussAdds=0,guardCalls=0,capProfiles=0;
function ok(v,m){checks++;if(!v)throw Error(m||"check "+checks)}
function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)%n}
function shuffle(a){for(let i=a.length-1;i>0;i--){let j=rnd(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
const bit=(w,i)=>Number((w>>BigInt(i))&1n),eb=i=>1n<<BigInt(i);
function parity(w){let t=0;while(w){w&=w-1n;t^=1}return t}
const nae=(c,x)=>c.some(([v,s])=>(x[v]^s)!==(x[c[0][0]]^c[0][1]));
function gf(n){let P=Array(n).fill(null),r=0;function add(a,b){gaussAdds++;for(let i=n-1;i>=0&&a;i--)if(a&eb(i)){if(P[i]){a^=P[i][0];b^=P[i][1]}else{P[i]=[a,b];r++;return 1}}return b?-1:0}
function space(){let sig=[],x=[];for(let i=0;i<n;i++){if(!P[i]){sig.push(eb(i));x.push(0);continue}let [a,b]=P[i],z=0n;for(let j=0;j<i;j++)if(a&eb(j)){z^=sig[j];b^=x[j]}sig.push(z);x.push(b)}return{sig,x}}
return{add,space,get rank(){return r},P}}
function encode(x){return x.reduce((w,v,i)=>w^(v?eb(i):0n),0n)}
function satB(B,x){return B.every(([a,b])=>x[a>>1]===(a&1)||x[b>>1]===(b&1))}
function satG(G,x){let w=encode(x);return G.every(([a,b])=>parity(w&a)===b)}
function bHull(n,B){sccCalls++;let a=Array.from({length:2*n},()=>[]),rev=Array.from({length:2*n},()=>[]);
function edge(u,v){a[u].push(v);rev[v].push(u)}
for(let [l,r] of B){edge(l^1,r);edge(r^1,l)}
let used=new Uint8Array(2*n),order=[];for(let v=0;v<2*n;v++)if(!used[v]){let st=[[v,0]];used[v]=1;while(st.length){let h=st[st.length-1],u=h[0];if(h[1]<a[u].length){let w=a[u][h[1]++];if(!used[w]){used[w]=1;st.push([w,0])}}else{order.push(u);st.pop()}}}
let c=new Int32Array(2*n).fill(-1),k=0;for(let v of order.reverse())if(c[v]<0){let q=[v];c[v]=k;for(let i=0;i<q.length;i++)for(let w of rev[q[i]])if(c[w]<0){c[w]=k;q.push(w)}k++}
let x=Array(n);for(let i=0;i<n;i++){if(c[2*i]===c[2*i+1])return{bad:true};x[i]=+(c[2*i+1]>c[2*i])}ok(satB(B,x));
let dag=Array.from({length:k},()=>new Set);for(let v=0;v<2*n;v++)for(let w of a[v])if(c[v]!==c[w])dag[c[v]].add(c[w]);
let stamp=0,vis=new Int32Array(k);function reach(u,v){if(u===v)return true;if(u>v)return false;stamp++;let q=[u];vis[u]=stamp;for(let j=0;j<q.length;j++)for(let w of dag[q[j]]){if(w===v)return true;if(w<v&&vis[w]!==stamp){vis[w]=stamp;q.push(w)}}return false}
let rows=[],rep=new Map,forced=[];for(let i=0;i<n;i++){let u=c[2*i],v=c[2*i+1],key=Math.min(u,v);if(reach(u,v)){rows.push([eb(i),1]);forced.push([i,1])}else if(reach(v,u)){rows.push([eb(i),0]);forced.push([i,0])}
if(rep.has(key)){let j=rep.get(key);rows.push([eb(i)^eb(j),+(c[2*i+1]!==c[2*j+1])])}else rep.set(key,i)}
return{bad:false,x,rows,forced,components:k}}
function close(n,B0,G0,trace=false){
let B=[],keys=new Set,rounds=0,addedB=0,addedG=0,log=[],M=gf(n);
function put(l,r){if(l===(r^1))return false;let x=Math.min(l,r),y=Math.max(l,r),k=x+","+y;if(keys.has(k))return false;keys.add(k);B.push([x,y]);return true}
B0.forEach(([l,r])=>put(l,r));for(let [a,b] of G0)if(M.add(a,b)<0)return{status:"UNSAT",why:"initial affine",rounds,addedB,addedG};
for(;;){rounds++;let BH=bHull(n,B);if(BH.bad)return{status:"UNSAT",why:"2SAT SCC",rounds,addedB,addedG,log};let g=M.space();
if(satB(B,g.x))return{status:"SAT",x:g.x,rounds,addedB,addedG,log};
if(M.P.every(z=>!z||parity(encode(BH.x)&z[0])===z[1]))return{status:"SAT",x:BH.x,rounds,addedB,addedG,log};
let dg=0,db=0;for(let [a,b] of BH.rows){let r=M.add(a,b);if(r<0)return{status:"UNSAT",why:"2SAT hull conflicts with affine",rounds,addedB,addedG,log};if(r){dg++;addedG++}}
g=M.space();let R=new Map;for(let i=0;i<n;i++){let v=g.sig[i],b=g.x[i];if(!v){if(put(2*i+b,2*i+b))db++}else if(R.has(v)){let j=R.get(v),t=b^g.x[j];if(put(2*i,2*j+(1^t)))db++;if(put(2*i+1,2*j+t))db++}else R.set(v,i)}
addedB+=db;if(trace)log.push({round:rounds,affineRank:M.rank,importedRows:dg,importedClauses:db});
if(!dg&&!db)return{status:"UNKNOWN",rounds,addedB,addedG,log,B,G:M.P.filter(Boolean),pins:g.sig.flatMap((s,i)=>s?[]:[[i,g.x[i]]])};
ok(rounds<=n+2*n*n+2)
}}
function guarded(n,B0,G0){let B=B0.slice(),keys=new Set(B.map(([a,b])=>[Math.min(a,b),Math.max(a,b)].join(","))),rounds=0,imports=0,failed=0;function put(a,b){if(a===(b^1))return false;let k=[Math.min(a,b),Math.max(a,b)].join(",");if(keys.has(k))return false;keys.add(k);B.push([a,b]);imports++;return true}
for(;;){let a=close(n,B,G0);rounds++;if(a.status!=="UNKNOWN")return{...a,guardRounds:rounds,imports,failed};B=a.B;for(let [l,r] of B)keys.add([Math.min(l,r),Math.max(l,r)].join(","));let change=false;for(let i=0;i<n;i++)for(let v of [0,1]){guardCalls++;let l=2*i+v,z=close(n,B,a.G.concat([[eb(i),v]]));if(z.status==="SAT")return{...z,guardRounds:rounds,imports,failed};if(z.status==="UNSAT"){failed++;change=put(l^1,l^1)||change}else for(let [j,w] of z.pins){change=put(l^1,2*j+w)||change}}
if(!change)return{status:"UNKNOWN",guardRounds:rounds,imports,failed};ok(rounds<=2*n*n+2)
}}
function system(C,n){let E=[],map=new Map,B=[],tri=[];function get(u,v){let k=Math.min(u,v)+","+Math.max(u,v);if(!map.has(k)){map.set(k,E.length);E.push([u,v])}return map.get(k)}
for(let c of C){let L=[];for(let [i,j] of [[0,1],[0,2],[1,2]]){let [u,s]=c[i],[v,t]=c[j];L.push(2*get(u,v)+(1^s^t))}for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)B.push([L[i],L[j]]);tri.push([L.reduce((a,l)=>a^eb(l>>1),0n),0])}
let a=Array.from({length:n},()=>[]);E.forEach(([u,v],i)=>{a[u].push([v,i]);a[v].push([u,i])});let P=Array(n).fill(null),tree=new Set;for(let v=0;v<n;v++)if(P[v]===null){P[v]=0n;let q=[v];for(let i=0;i<q.length;i++)for(let [u,j] of a[q[i]])if(P[u]===null){P[u]=P[q[i]]^eb(j);tree.add(j);q.push(u)}}
let G=E.flatMap(([u,v],i)=>tree.has(i)?[]:[[P[u]^P[v]^eb(i),0]]);
function lift(p){let x=Array(n).fill(-1);for(let v=0;v<n;v++)if(x[v]<0){x[v]=0;let q=[v];for(let i=0;i<q.length;i++)for(let [u,j] of a[q[i]])if(x[u]<0){x[u]=x[q[i]]^p[j];q.push(u)}}ok(E.every(([u,v],i)=>(x[u]^x[v])===p[i]));ok(C.every(c=>nae(c,x)));return x}
return{E,B,G,tri,lift,obs:x=>E.map(([u,v])=>x[u]^x[v])}}
const AG=[[[0,1,2],[3,4,5],[6,7,8]],[[0,3,6],[1,4,7],[2,5,8]],[[0,4,8],[1,5,6],[2,3,7]],[[0,5,7],[1,3,8],[2,4,6]]];
const inside=AG.flatMap((p,j)=>p.filter((_,i)=>j!==0||i===2));
const phaseWords=[0,1].map(b=>Array.from({length:9},(_,i)=>i<3?b:i<6?1^b:(i===8?1:0)));
function dsu(n){let p=Array.from({length:n},(_,i)=>i);function f(v){while(p[v]!==v){p[v]=p[p[v]];v=p[v]}return v}return{f,add(a,b){a=f(a);b=f(b);if(a!==b)p[a]=b}}}
function logical(n,no){let w=Array(n).fill(0);if(no)w[0]=1;return {w,C:Array.from({length:n},(_,i)=>[[i,0],[(i+n-1)%n,w[(i+n-1)%n]],[(i+1)%n,1^w[i]]])}}
function auth(F,n){let D=dsu(n),P=new Set;for(let p of F){let d=new Uint8Array(n);for(let c of p){ok(new Set(c).size===3);for(let v of c){ok(v>=0&&v<n);d[v]++}for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let u=c[i],v=c[j],key=Math.min(u,v)*n+Math.max(u,v);ok(!P.has(key));P.add(key);D.add(u,v)}}ok(d.every(v=>v===1))}ok(Array.from({length:n},(_,i)=>D.f(i)).every(v=>v===D.f(0)))}
function compile(C,n){let F=[[],[],[],[]],cnt=Array.from({length:n},()=>[0,0]);for(let v=0;v<n;v++)for(let s=0;s<4;s++)for(let j=0;j<3;j++)if(s!==0||j===2)F[s].push(AG[s][j].map(u=>9*v+u));
for(let c of C)for(let t of [0,1])F[0].push(c.map(([v,s])=>{let a=s^t;return 9*v+3*a+cnt[v][a]++}));ok(cnt.every(x=>x[0]===3&&x[1]===3));return F}
function acquire(F,n){for(let omit=0;omit<4;omit++){let D=dsu(n);for(let s=0;s<4;s++)if(s!==omit)for(let c of F[s]){D.add(c[0],c[1]);D.add(c[0],c[2])}let M=new Map;for(let v=0;v<n;v++){let r=D.f(v);if(!M.has(r))M.set(r,[]);M.get(r).push(v)}let V=[...M.values()];if(!V.every(a=>a.length===9))continue;let block=Array(n),port=Array(n).fill(null),tables=[],internal=V.map(()=>[]),ext=[];V.forEach((a,i)=>a.forEach(v=>block[v]=i));for(let s=0;s<4;s++)for(let c of F[s])if(c.every(v=>block[v]===block[c[0]]))internal[block[c[0]]].push(c);else ext.push(c);
let good=true;
for(let i=0;i<V.length;i++){let a=V[i],L=internal[i];if(L.length!==10){good=false;break}let set=new Set,idx=new Map(a.map((v,j)=>[v,j]));for(let c of L)for(let j=0;j<3;j++)for(let k=j+1;k<3;k++){let u=idx.get(c[j]),v=idx.get(c[k]);set.add(Math.min(u,v)*9+Math.max(u,v))}if(set.size!==30){good=false;break}
let Q=dsu(9),missing=[],ports=new Set;for(let u=0;u<9;u++)for(let v=u+1;v<9;v++)if(!set.has(u*9+v)){Q.add(u,v);missing.push([u,v]);ports.add(u);ports.add(v)}
let P=new Map;for(let u of ports){let r=Q.f(u);if(!P.has(r))P.set(r,[]);P.get(r).push(u)}let groups=[...P.values()].sort((a,b)=>Math.min(...a)-Math.min(...b));if(groups.length!==2||groups.some(x=>x.length!==3)||missing.length!==6){good=false;break}
let base=Array(9).fill(0);groups[1].forEach(u=>base[u]=1);let privateV=Array.from({length:9},(_,j)=>j).filter(j=>!ports.has(j));base[privateV[2]]=1;
if(!L.every(c=>c.some(v=>base[idx.get(v)]!==base[idx.get(c[0])]))){good=false;break}
for(let u of groups[0])port[a[u]]=0;for(let u of groups[1])port[a[u]]=1;tables.push(base);
}
if(!good||!ext.every(c=>c.every(v=>port[v]!==null)&&new Set(c.map(v=>block[v])).size===3))continue;
let C=ext.map(c=>c.map(v=>[block[v],port[v]])),unique=new Map;for(let c of C){let a=c.slice().sort((a,b)=>a[0]-b[0]),s=a[0][1],key=a.map(([v,t])=>v+":"+(s^t)).join(",");if(!unique.has(key))unique.set(key,c)}
function lift(x){let y=Array(n);V.forEach((a,i)=>a.forEach((v,j)=>y[v]=tables[i][j]^x[i]));ok(F.flat().every(c=>c.some(v=>y[v]!==y[c[0]])));return y}
return{C:[...unique.values()],blocks:V.length,lift,omit}}
return null}
let cap=0;for(let w=0;w<512;w++){capProfiles++;let x=Array.from({length:9},(_,i)=>(w>>i)&1);if(inside.every(c=>c.some(v=>x[v]!==x[c[0]]))){cap++;ok(x.slice(0,3).every(v=>v===x[0])&&x.slice(3,6).every(v=>v!==x[0]))}}ok(cap===12);
let ring=[];for(let n of [6,8,16,32,64,128,256])for(let no of [true,false]){let {C,w}=logical(n,no),F=compile(C,n),N=9*n;auth(F,N);let perm=shuffle(Array.from({length:N},(_,i)=>i)),X=F.map(p=>shuffle(p.map(c=>shuffle(c.map(v=>perm[v])))));auth(X,N);let A=acquire(X,N);ok(A&&A.blocks===n&&A.C.length===n);
let S=system(A.C,n),BH=bHull(S.E.length,S.B);ok(!BH.bad);let G=gf(S.E.length);for(let [a,b] of S.G)ok(G.add(a,b)>=0);ok(satG(S.G,G.space().x));let z=close(S.E.length,S.B,S.G,true);ok(z.status===(no?"UNSAT":"SAT"));
if(z.x)A.lift(S.lift(z.x));
let L=system(C,n),t=L.obs(Array(n).fill(0)); // independent observation witness with all t_i=1, chord chosen to obey triangle; global cycle may fail
let vals=new Map;for(let i=0;i<n;i++){let u=i,v=(i+1)%n;vals.set(Math.min(u,v)+","+Math.max(u,v),w[i]);let a=(i+n-1)%n,b=(i+1)%n;vals.set(Math.min(a,b)+","+Math.max(a,b),w[(i+n-1)%n]^w[i])}
let p=L.E.map(([u,v])=>vals.get(Math.min(u,v)+","+Math.max(u,v)));ok(satB(L.B,p)&&satG(L.tri,p));ok(satG(L.G,p)===!no);
if(no)for(let j=0;j<n;j++){let d=w.map((b,i)=>b^+(i!==(j+n-1)%n)),x=Array(n).fill(0);ok(d.reduce((a,b)=>a^b,0)===0);for(let i=0;i<n-1;i++)x[i+1]=x[i]^d[i];ok(C.every((c,i)=>i===j||nae(c,x))&&!nae(C[j],x))}
ring.push({n:N,phase:n,label:no?"UNSAT":"SAT",status:z.status,why:z.why??"witness",obs:S.E.length,cycleRank:S.G.length,rounds:z.rounds,addedG:z.addedG,addedB:z.addedB,capModels:12,triangleRelaxation:"SAT",deletionWitnesses:no?n:0});
}
let hullCases=0,hullModels=0,random={cases:0,unsat:0,baseNo:0,baseYes:0,baseUnknown:0,guardNo:0,guardYes:0,guardUnknown:0,improved:0};
for(let j=0;j<360;j++){let n=3+rnd(6),B=Array.from({length:1+rnd(2*n)},()=>[rnd(2*n),rnd(2*n)]),M=bHull(n,B),V=[];for(let w=0;w<2**n;w++){let x=Array.from({length:n},(_,i)=>(w>>i)&1);if(satB(B,x))V.push(x)}ok(M.bad===!V.length);if(V.length){let H=gf(n);for(let [a,b] of M.rows)ok(H.add(a,b)>=0);let W=gf(n),u=encode(V[0]);for(let x of V){ok(satG(M.rows,x));W.add(encode(x)^u,0)}ok(n-H.rank===W.rank);hullCases++;hullModels+=V.length}
if(j>=180)continue;let G=[],H=gf(n);for(let a=0;a<1+rnd(n);a++){let x=BigInt(1+rnd(2**n-1)),b=rnd(2);G.push([x,b]);H.add(x,b)}
let ref=V.filter(x=>satG(G,x)),z=close(n,B,G),t=guarded(n,B,G);for(let u of [z,t]){if(u.status==="UNSAT")ok(!ref.length);if(u.status==="SAT")ok(satB(B,u.x)&&satG(G,u.x))}
random.cases++;random.unsat+=!ref.length;random["base"+(z.status==="UNSAT"?"No":z.status==="SAT"?"Yes":"Unknown")]++;random["guard"+(t.status==="UNSAT"?"No":t.status==="SAT"?"Yes":"Unknown")]++;random.improved+=z.status==="UNKNOWN"&&t.status!=="UNKNOWN";
}
let raw=[];for(let [name,F,n] of [["AG9",AG,9],["cyclic15",Array.from({length:4},(_,s)=>Array.from({length:5},(_,i)=>[i,5+(i+s)%5,10+(i+3*s)%5])),15]]){auth(F,n);let C=F.flat().map(c=>c.map(v=>[v,0])),S=system(C,n),a=close(S.E.length,S.B,S.G,true),b=guarded(S.E.length,S.B,S.G);if(a.x)S.lift(a.x);if(b.x)S.lift(b.x);ok(name!=="AG9"||a.status!=="SAT"&&b.status!=="SAT");raw.push({name,obs:S.E.length,base:a.status,baseAddedG:a.addedG,baseAddedB:a.addedB,guard:b.status,guardRounds:b.guardRounds,guardImports:b.imports,failed:b.failed})}
return{seed:20261126,checks,sccCalls,gaussAdds,guardCalls,capProfiles,hullCases,hullModels,ring,random,raw}
}
console.log(JSON.stringify(audit(),null,2));
