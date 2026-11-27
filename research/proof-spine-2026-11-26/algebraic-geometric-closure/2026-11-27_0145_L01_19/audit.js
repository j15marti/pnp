function check(x,m="assertion"){if(!x)throw Error(m)}

function bits(x){let z=0;while(x){x&=x-1n;z++}return z}

function affine(rows,rhs,n){let a=rows.map((v,i)=>v|(BigInt(rhs[i])<<BigInt(n))), piv=[],r=0;for(let j=0;j<n;j++){let k=r;while(k<a.length&&!(a[k]&(1n<<BigInt(j))))k++;if(k===a.length)continue;[a[r],a[k]]=[a[k],a[r]];for(let i=0;i<a.length;i++)if(i!==r&&(a[i]&(1n<<BigInt(j))))a[i]^=a[r];piv.push(j);r++}for(let i=r;i<a.length;i++)if(a[i])return null;let x=0n;for(let i=0;i<r;i++)if(a[i]>>BigInt(n)&1n)x|=1n<<BigInt(piv[i]);let P=new Set(piv),basis=[];for(let j=0;j<n;j++)if(!P.has(j)){let v=1n<<BigInt(j);for(let i=0;i<r;i++)if(a[i]>>BigInt(j)&1n)v|=1n<<BigInt(piv[i]);basis.push(v)}return {x,basis,rank:r}}

function project(A,J){let map=v=>J.reduce((z,j,k)=>z|(((v>>BigInt(j))&1n)<<BigInt(k)),0n),base=map(A.x),span=new Set([0n]);for(let v of A.basis){let w=map(v);if(!span.has(w)){for(let s of [...span])span.add(s^w)}}return [...span].map(v=>v^base)}

function instance(b){let F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],T=[];for(let i=0;i<b;i++)for(let j=0;j<7;j++)T.push(F[j].map(e=>7*(j===0&&e===0?(i+1)%b:j===3&&e===1?(i+b-1)%b:i)+e));return T}

function rowsFor(T,m){let rows=Array(m).fill(0n);T.forEach((a,j)=>{check(new Set(a).size===3);for(let e of a)rows[e]|=1n<<BigInt(j)});return rows}

function ref(T,m,cap=200000){let adj=Array.from({length:m},()=>[]);T.forEach((a,j)=>a.forEach(e=>adj[e].push(j)));let ms=T.map(a=>a.reduce((z,e)=>z|(1n<<BigInt(e)),0n)),full=(1n<<BigInt(m))-1n,visits=0;function go(u){if(++visits>cap)throw Error("reference cap");if(u===full)return true;let best=null;for(let e=0;e<m;e++)if(!(u>>BigInt(e)&1n)){let cand=adj[e].filter(j=>!(ms[j]&u));if(best===null||cand.length<best.length)best=cand;if(!best.length)return false}return best.some(j=>go(u|ms[j]))}return {sat:go(0n),visits}}

function native(T,m){let occ=Array.from({length:m},()=>[]);T.forEach((a,j)=>a.forEach(e=>occ[e].push(j)));let center=[],group=T.map(()=>[]),pairs=[],s=0;for(let e=0;e<m;e++){let a=s++,L=occ[e].map(j=>[j,s++]),c=s++;center.push([a,c]);for(let [j,v] of L.slice().reverse()){let w=s++;group[j].push(v,w);pairs.push([v,w,j])}}let p=Array.from({length:s},(_,i)=>(i+1)%s),g=Array.from({length:s},(_,i)=>i),k=g.slice();for(let [a,b] of center)[p[a],p[b]]=[p[b],p[a]];for(let [a,b,j] of pairs){k[a]=b;k[b]=a}for(let L of group)for(let i=0;i<L.length;i++)g[L[i]]=L[(i+1)%L.length];let owner=Array(s).fill(-1);group.forEach((L,j)=>L.forEach(i=>owner[i]=j));let E=new Set(),add=(i,j)=>E.add(i*(3*s)+j);for(let i=0;i<s;i++){let u=s+2*i,v=u+1;add(i,u);add(u,v);add(v,p[i]);if(owner[i]>=0){add(g[i],v);add(v,u);add(u,p[k[g[i]]])}}
function lift(x){let perm=Array(3*s).fill(-1);for(let i=0;i<s;i++){let u=s+2*i,v=u+1,on=owner[i]>=0&&(x>>BigInt(owner[i])&1n);if(on){perm[g[i]]=v;perm[v]=u;perm[u]=p[k[g[i]]]}else{perm[i]=u;perm[u]=v;perm[v]=p[i]}}check(new Set(perm).size===3*s&&perm.every((v,i)=>E.has(i*(3*s)+v)),"lift");let seen=new Set(),c=0;for(let i=0;i<3*s;i++)if(!seen.has(i)){c++;let j=i;while(!seen.has(j)){seen.add(j);j=perm[j]}}return {perm,c}}
return {s,n:3*s,E,lift}}

function audit(b){let T=instance(b),m=7*b,t=T.length,rows=rowsFor(T,m),A=affine(rows,Array(m).fill(1),t);check(A&&A.basis.length===b+2,"dimension");check(rows.every(r=>bits(r)===3),"regular");check(T.every((_,j)=>A.basis.some(v=>v>>BigInt(j)&1n)),"affine forced bit");
let adj=T.map((a,j)=>T.map((z,k)=>k).filter(k=>T[k].some(e=>a.includes(e))));let visited=new Set([0]),todo=[0];while(todo.length)for(let j of adj[todo.pop()])if(!visited.has(j)){visited.add(j);todo.push(j)}check(visited.size===t,"connected");
let rowWords=0;for(let r of rows){let J=Array.from({length:t},(_,j)=>j).filter(j=>r>>BigInt(j)&1n),W=project(A,J);check(W.length===4&&W.every(v=>bits(v)%2===1),"row projection");rowWords+=W.length}
let cand=new Map(),probes=0;for(let J of adj){if(J.length>7)continue;let key=J.join(",");if(cand.has(key))continue;let W=project(A,J),lo=Math.min(...W.map(bits));probes+=W.length;cand.set(key,{J,lo,words:W.length})}
let used=new Set(),chosen=[],lb=0;for(let p of [...cand.values()].filter(x=>x.J.length===7&&x.lo>=3).sort((a,b)=>a.J[0]-b.J[0]))if(p.J.every(j=>!used.has(j))){p.J.forEach(j=>used.add(j));chosen.push(p);lb+=p.lo}
check(used.size===t&&lb===3*b,"patch cover");let W=project(A,[0,1,2,3,4,5,6]);check(W.length===8&&W.every(x=>bits(x)===3||bits(x)===7));
let F= native(T,m),full=(1n<<BigInt(t))-1n;let src=new Set(),liftChecks=0;
for(let x of [full,...Array.from({length:t-1},(_,j)=>full^(1n<<BigInt(j+1))^1n)]){let z=F.lift(x);let d=Array(m).fill(0);T.forEach((a,j)=>{if(x>>BigInt(j)&1n)a.forEach(e=>d[e]++)});check(z.c===1+d.reduce((sum,v)=>sum+Math.abs(v-1),0)&&z.c%2===1);z.perm.forEach((v,i)=>src.add(i*F.n+v));liftChecks++}
check(src.size===F.E.size,"target support");let out=Array.from({length:F.n},()=>[]),rev=out.map(()=>[]);for(let x of F.E){let i=Math.floor(x/F.n),j=x%F.n;out[i].push(j);rev[j].push(i)}for(let G of [out,rev]){let S=new Set([0]),L=[0];while(L.length)for(let j of G[L.pop()])if(!S.has(j)){S.add(j);L.push(j)}check(S.size===F.n,"native SCC")}
let exact=null;if(b<=6){exact=ref(T,m);check(!exact.sat)}
let minWitness=null;for(let x of W)if(bits(x)===3){let z=0n;for(let i=0;i<b;i++)z|=x<<BigInt(7*i);if(rows.every(r=>bits(r&z)%2)){minWitness=bits(z);break}}check(minWitness===3*b);
return {b,m,t,n:F.n,arcs:F.E.size,dimension:A.basis.length,affineWords:(1n<<BigInt(A.basis.length)).toString(),signWords:(1n<<BigInt(t-1)).toString(),rowWords,patchCandidates:cand.size,projectionWords:probes,patches:chosen.map(p=>p.J),bound:lb,required:m/3,minWitness,liftChecks,reference:exact,allTargetSupported:true,connected:true}}

function run(){let scales=[3,6,12,24,48].map(audit);let T=[[0,1,2]],A=affine(rowsFor(T,3),[1,1,1],1);check(A&&A.x===1n&&!A.basis.length&&native(T,3).lift(1n).c===1,"minimal YES control");return {scales,control:"single triple admits tour; weight bound equals target, no NO",execution:"serial JS; independent exact-cover DFS on b=3,6; all native lifts checked; no general matching, LP, or Lean build"}}
console.log(JSON.stringify(run(),null,2));
