// Run: node file.js
function main(){
const Z=0n, rng={s:20261124}, rand=n=>{rng.s=(Math.imul(1664525,rng.s)+1013904223)>>>0;return rng.s%n}, assert=(x,m)=>{if(!x)throw Error(m)};
const stats=()=>({closureScans:0,deleted:0,affine:0,flow:0,flowScans:0,countCells:0,dagEdges:0,dagHits:0,peakDag:0,branches:0,queries:0,cutTrials:0,cutScans:0,cutRegions:0});
const min=a=>a.reduce((x,y)=>x<y?x:y), max=a=>a.reduce((x,y)=>x>y?x:y);
const sum=a=>a.reduce((x,y)=>x+y,Z), xor=a=>a.reduce((x,y)=>x^y,Z);
function basis(rows){const b=new Map();for(let [x,w] of rows){while(x){let p=x.toString(2).length-1;if(!b.has(p)){b.set(p,[x,w]);break}let [y,z]=b.get(p);x^=y;w^=z}}return b}
function express(b,x){let w=0n;while(x){let p=x.toString(2).length-1;if(!b.has(p))return null;let [y,z]=b.get(p);x^=y;w^=z}return w}
function verify(B,K,t,w){if(!w||w.length!==B.length)return false;let a=B.map((b,i)=>b.find(r=>r.id===w[i]));return a.every(Boolean)&&xor(a.map(r=>r.t))===t&&K.every((k,j)=>sum(a.map(r=>r.c[j]))<=k)}
function close(B,K,t,s){B=B.map(b=>b.slice());if(K.some(k=>k<Z))return null;
while(true){s.closureScans++;if(B.some(b=>!b.length))return null;
let m=K.map((_,j)=>B.map(b=>min(b.map(r=>r.c[j])))), M=m.map(sum);
if(M.some((v,j)=>v>K[j]))return null;
let changed=false;
outer:for(let i=0;i<B.length;i++){let other=B.filter((_,j)=>j!==i),base=xor(other.map(b=>b[0].t)),bs=basis(other.flatMap(b=>b.map(r=>[r.t^b[0].t,Z])));
for(let r of B[i])if(K.some((k,j)=>M[j]-m[j][i]+r.c[j]>k)||express(bs,t^base^r.t)===null){
B[i]=B[i].filter(q=>q!==r);s.deleted++;changed=true;break outer}}
if(!changed)return B}}
function affine(B,t,s){let g=[],by=[],base=xor(B.map(b=>b[0].t));
for(let b of B){let local=basis(b.map(r=>[r.t^b[0].t,Z])),d=local.size, tags=new Set(b.map(r=>String(r.t)));if((1n<<BigInt(d))!==BigInt(tags.size))return undefined;let start=g.length;for(let [x] of local.values())g.push(x);by.push([start,g.length])}
let bs=basis(g.map((x,i)=>[x,1n<<BigInt(i)])),v=express(bs,t^base);s.affine++;if(v===null)return null;
return B.map((b,i)=>{let y=b[0].t;for(let j=by[i][0];j<by[i][1];j++)if((v>>BigInt(j))&1n)y^=g[j];return b.find(r=>r.t===y).id})}
// Unit-capacity assignment to owner categories (capacitated bipartite matching).
function flow(good,cap,s){s.flow++;if(cap.some(k=>k<Z))return null;let n=good.length,m=cap.length+1, N=n+m+2,S=N-2,T=N-1,adj=Array.from({length:N},()=>[]);
function edge(u,v,c){let a={v,c,rev:adj[v].length},b={v:u,c:0,rev:adj[u].length};adj[u].push(a);adj[v].push(b);return a}
let refs=good.map((opts,i)=>{edge(S,i,1);return opts.map(([j,id])=>[id,edge(i,n+j,1)])});
cap.concat([BigInt(n)]).forEach((c,j)=>edge(n+j,T,Number(c>BigInt(n)?BigInt(n):c)));
for(let f=0;f<n;f++){let p=Array(N).fill(null),q=[S];p[S]=[-1,-1];for(let h=0;h<q.length&&!p[T];h++){let u=q[h];for(let j=0;j<adj[u].length;j++){s.flowScans++;let e=adj[u][j];if(e.c&&!p[e.v]){p[e.v]=[u,j];q.push(e.v)}}}if(!p[T])return null;for(let v=T;v!==S;){let [u,j]=p[v],e=adj[u][j];e.c--;adj[v][e.rev].c++;v=u}}
return refs.map(a=>a.find(([id,e])=>e.c===0)[0])}
function hybrid(B,K,t,s,limit=256){let m=K.length,mins=B.map(b=>K.map((_,j)=>min(b.map(r=>r.c[j])))),C=K.map((k,j)=>k-sum(mins.map(a=>a[j])));if(C.some(k=>k<Z))return null;
let gcd=(a,b)=>{while(b){let r=a%b;a=b;b=r}return a}, scales=K.map((_,j)=>B.reduce((d,b,i)=>b.reduce((v,r)=>gcd(v,r.c[j]-mins[i][j]),d),Z)||1n);
let good=[],gi=[],groups=new Map(),base=Z;
for(let i=0;i<B.length;i++){let b=B[i],a=b.map(r=>r.c.map((x,j)=>x-mins[i][j])),cats=a.map(c=>{let nz=c.map((v,j)=>v?j:-1).filter(j=>j>=0);return nz.length===0?m:nz.length===1&&c[nz[0]]===scales[nz[0]]?nz[0]:-1});
if(cats.every(j=>j>=0)&&b.every(r=>r.t===b[0].t)){good.push(cats.map((j,h)=>[j,b[h].id]));gi.push(i);base^=b[0].t}
else if(b.length===2){let d=a[1].map((v,j)=>v-a[0][j]),e=b[0].t^b[1].t,key=d.join(",")+"|"+e;let g=groups.get(key)||{d,e,ids:[]};g.ids.push(i);groups.set(key,g);base^=b[0].t;C=C.map((v,j)=>v-a[0][j])}else return undefined}
let gs=[...groups.values()],P=gs.reduce((p,g)=>p*BigInt(g.ids.length+1),1n);if(P>BigInt(limit))return undefined;
function walk(k,c,v,w){if(k===gs.length){s.countCells++;if(v!==t||c.some(x=>x<Z))return null;let f=flow(good,c.map((x,j)=>x/scales[j]),s);if(!f)return null;let out=w.slice();gi.forEach((i,h)=>out[i]=f[h]);return out}
let g=gs[k];for(let z=0;z<=g.ids.length;z++){let out=w.slice();g.ids.forEach((i,h)=>out[i]=B[i][h<z?1:0].id);let r=walk(k+1,c.map((x,j)=>x-BigInt(z)*g.d[j]),v^(z%2?g.e:Z),out);if(r)return r}return null}
return walk(0,C,base,Array(B.length))}
function dag(B,K,t,s,limit=2048){let D=new Map([["0|"+K.map(()=>0).join(","),{v:Z,c:K.map(()=>Z),w:[]}]]);
for(let i=0;i<B.length;i++){let rest=B.slice(i+1),mn=K.map((_,j)=>sum(rest.map(b=>min(b.map(r=>r.c[j]))))),mx=K.map((_,j)=>sum(rest.map(b=>max(b.map(r=>r.c[j]))))),base=xor(rest.map(b=>b[0].t)),bs=basis(rest.flatMap(b=>b.map(r=>[r.t^b[0].t,Z]))),E=new Map();
for(let a of D.values())for(let r of B[i]){s.dagEdges++;let c=a.c.map((x,j)=>x+r.c[j]),v=a.v^r.t;
if(c.some((x,j)=>x+mn[j]>K[j])||express(bs,t^v^base)===null)continue;
// Canonicalize by retaining only residual capacity relevant to the suffix.
c=c.map((x,j)=>x<K[j]-mx[j]?K[j]-mx[j]:x);
let key=v+"|"+c.join(",");if(E.has(key)){s.dagHits++;continue}E.set(key,{v,c,w:a.w.concat(r.id)});if(E.size>limit)return undefined}
D=E;s.peakDag=Math.max(s.peakDag,D.size);if(!D.size)return null}return D.values().next().value.w}
function local(B,K,t,s){s.queries++;B=close(B,K,t,s);if(!B)return null;
if(K.every((k,j)=>sum(B.map(b=>max(b.map(r=>r.c[j]))))<=k)){let a=affine(B,t,s);if(a!==undefined)return a}
let f=hybrid(B,K,t,s);if(f!==undefined)return f;
let d=dag(B,K,t,s);if(d!==undefined)return d;
s.branches++;let i=B.findIndex(b=>b.length>1);assert(i>=0,"nonterminal singleton");for(let r of B[i]){let C=B.slice();C[i]=[r];let w=local(C,K,t,s);if(w)return w}return null}
function regions(B,K,omit,s){let p=B.map((_,i)=>i),find=i=>{while(p[i]!==i){p[i]=p[p[i]];i=p[i]}return i},join=(a,b)=>{p[find(a)]=find(b)}, first=new Map();
for(let i=0;i<B.length;i++){let tags=B[i].reduce((v,r)=>v|r.t,Z);let keys=[];for(let j=0;j<K.length;j++){s.cutScans++;if(j!==omit&&B[i].some(r=>r.c[j]>Z))keys.push("c"+j)}
for(let j=0;tags;tags>>=1n,j++)if(tags&1n)keys.push("t"+j);
for(let k of keys){if(first.has(k))join(i,first.get(k));else first.set(k,i)}}
let g=new Map();B.forEach((_,i)=>{let k=find(i),a=g.get(k)||[];a.push(i);g.set(k,a)});return [...g.values()]}
function solve(B,K,t,s){B=close(B,K,t,s);if(!B)return null;if(!B.length)return t===Z?[]:null;
let G=regions(B,K,-1,s),cut=-1;
if(G.length===1)for(let j=0;j<K.length;j++){s.cutTrials++;let g=regions(B,K,j,s);if(g.length>G.length){G=g;cut=j}}
if(G.length===1)return local(B,K,t,s);
let w=Array(B.length),tot=Z;s.cutRegions+=G.length;
for(let idx of G){let A=idx.map(i=>B[i]), mask=A.reduce((a,b)=>a|b.reduce((v,r)=>v|r.t,Z),Z),target=t&mask,C=K.slice(),ans;
if(cut<0)ans=local(A,C,target,s);
else {let lo=Z,hi=sum(A.map(b=>max(b.map(r=>r.c[cut]))));C[cut]=hi;ans=local(A,C,target,s);if(!ans)return null;
while(lo<hi){let mid=(lo+hi)/2n;C[cut]=mid;let q=local(A,C,target,s);if(q){ans=q;hi=mid}else lo=mid+1n}tot+=lo;if(tot>K[cut])return null}
if(!ans)return null;idx.forEach((i,h)=>w[i]=ans[h])}
return verify(B,K,t,w)?w:(()=>{throw Error("glue witness")})()}
function cnf(n,clauses){return [Array.from({length:n},(_,i)=>[0,1].map(v=>({id:v,t:Z,c:clauses.map(c=>BigInt(c.filter(l=>Math.abs(l)===i+1&&(l>0?v===0:v===1)).length))}))),clauses.map(c=>BigInt(c.length-1)),Z]}
function brute(B,K,t){let c=0,models=0;function rec(w){if(w.length===B.length){c++;if(verify(B,K,t,w))models++;return}for(let r of B[w.length])rec(w.concat(r.id))}rec([]);return [models,c]}
function check(B,K,t){let s=stats(),w=solve(B,K,t,s),[models,c]=brute(B,K,t);assert(!!w===!!models,"decision");if(w)assert(verify(B,K,t,w),"witness");return {sat:!!w,models,tuples:c,...s}}
let random=[], fano=[],scale=[],special=[];
for(let q=0;q<120;q++){let n=3+rand(5),m=1+rand(18),C=Array.from({length:m},()=>Array.from({length:1+rand(3)},()=> (1+rand(n))*(rand(7)<3?-1:1)));if(q%15===0)C.push([]);random.push(check(...cnf(n,C)))}
for(let q=0;q<100;q++){let n=2+rand(5),m=1+rand(4),B=Array.from({length:n},()=>Array.from({length:2+rand(2)},(_,id)=>({id,c:Array.from({length:m},()=>BigInt(rand(4))),t:BigInt(rand(8))}))),K=Array.from({length:m},()=>BigInt(rand(2*n+1))),t=BigInt(rand(8));random.push(check(B,K,t))}
let E=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]],C=E.flatMap(e=>[e,e.map(v=>-v)]);for(let i=-1;i<14;i++){let [B,K,t]=cnf(7,C);if(i>=0)K[i]++;fano.push({relax:i,...check(B,K,t)})}
function star(g,cap){let C=[];for(let i=0;i<g;i++){let e=[3*i+1,3*i+2,3*i+3];C.push(e,e.map(v=>-v))}let [B,K,t]=cnf(3*g,C);B.forEach(b=>b.forEach(r=>r.c.push(BigInt(r.id))));K.push(BigInt(cap));return [B,K,t]}
for(let g of [2,4,8,16,32,64])for(let delta of [-1,0]){let [B,K,t]=star(g,g+delta),s=stats(),w=solve(B,K,t,s);assert(!!w===(delta===0),"star decision");if(w)assert(verify(B,K,t,w),"star witness");scale.push({g,delta,sat:!!w,rawCountExponent:3*g,...s})}
// Connected cut with 80-bit shared owner; compare all tuples.
let [B,K,t]=star(3,3);B.forEach(b=>b.forEach(r=>r.c[r.c.length-1]*=1n<<80n));K[K.length-1]=3n<<80n;special.push({name:"wide owner",...check(B,K,t)});K[K.length-1]--;special.push({name:"wide owner unsat",...check(B,K,t)});
// Flow, affine and nonlinear DAG controls; one tag bit crossing cut prevents false split.
let F=Array.from({length:8},(_,i)=>[0,1].map(id=>({id,c:[BigInt(id===0),BigInt(id===1)],t:Z})));special.push({name:"flow sat",...check(F,[4n,4n],Z)},{name:"flow unsat",...check(F,[3n,4n],Z)});
let A=Array.from({length:5},(_,i)=>[0,1].map(id=>({id,c:[],t:BigInt(id)<<BigInt(i)})));special.push({name:"affine",...check(A,[],19n)});
let D=Array.from({length:3},()=>[0,1,2].map(id=>({id,c:[],t:BigInt(id)})));special.push({name:"nonaffine",...check(D,[],3n)});
let agg=a=>{let o={cases:a.length,sat:a.filter(x=>x.sat).length};for(let k of Object.keys(stats()))o[k]=k==="peakDag"?Math.max(...a.map(x=>x[k])):a.reduce((v,x)=>v+x[k],0);o.tuples=a.reduce((v,x)=>v+(x.tuples||0),0);return o};
return {random:agg(random),fano,scale,special,totals:agg([...random,...fano,...scale,...special]),rawRandom:random}
}
console.log(JSON.stringify(main(),null,2));
