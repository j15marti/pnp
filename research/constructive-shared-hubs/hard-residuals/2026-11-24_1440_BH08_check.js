function run(){
const L={closureScans:0,closureTrials:0,forcedPins:0,planCandidates:0,orderTrials:0,transitions:0,merges:0,peakStates:0,sumStates:0,referenceWords:0,verifiedWitnesses:0,assertions:0};
function ok(x){L.assertions++;if(!x)throw Error("assertion "+L.assertions)}
function legal(f,x){let a=f.v.map((v,i)=>x[v]*f.s[i]);return !(a.every(t=>t===-1)&&(f.b&1)||a.every(t=>t===1)&&(f.b&2))}
function close(n,F,p){
p=p.slice();while(true){let change=false;for(const f of F){L.closureScans++;let sup=f.v.map(()=>new Set()),cnt=0;
for(let a=0;a<8;a++){L.closureTrials++;let x=Array(n).fill(0);for(let i=0;i<3;i++)x[f.v[i]]=(a>>i&1)?1:-1;if(f.v.some(v=>p[v]&&p[v]!==x[v])||!legal(f,x))continue;cnt++;f.v.forEach((v,i)=>sup[i].add(x[v]))}
if(!cnt)return null;for(let i=0;i<3;i++)if(!p[f.v[i]]&&sup[i].size===1){p[f.v[i]]=[...sup[i]][0];L.forcedPins++;change=true;break}if(change)break}if(!change)return p}}
function solve(n,F,p=Array(n).fill(0),cap=12){
p=close(n,F,p);if(!p)return {count:0n,closed:true};
let J=Array.from({length:n},()=>Array(n).fill(0)), hard=[], m=0;
for(const f of F){if(f.b===3){m++;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let a=f.v[i],b=f.v[j];J[a][b]+=f.s[i]*f.s[j];J[b][a]=J[a][b]}}else if(f.b)hard.push(f)}
let vals=new Set([0]);for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)vals.add(J[i][j]);
let best=null;
for(const lam of vals){L.planCandidates++;let adj=Array.from({length:n},()=>new Set()),edges=[];
for(let a=0;a<n;a++)for(let b=a+1;b<n;b++)if(J[a][b]!==lam){adj[a].add(b);adj[b].add(a);edges.push([a,b,J[a][b]-lam])}
for(const f of hard)for(let a of f.v)for(let b of f.v)if(a!==b)adj[a].add(b);
let order=[],used=new Set();function front(U){return [...U].filter(v=>[...adj[v]].some(w=>!U.has(w))).sort((a,b)=>a-b)}
for(let i=0;i<n;i++){let pick=-1,score=Infinity;for(let v=0;v<n;v++)if(!used.has(v)){L.orderTrials++;used.add(v);let k=front(used).length;used.delete(v);if(k<score){score=k;pick=v}}used.add(pick);order.push(pick)}
for(const ord of [order,Array.from({length:n},(_,i)=>i)]){let U=new Set(),fr=[[]];for(const v of ord){U.add(v);fr.push(front(U))}let w=Math.max(...fr.map(x=>x.length));if(!best||w<best.w)best={lam,ord,fr,w,edges}}
}
let {lam,ord,fr,w,edges}=best;if(w>cap)return {unknown:true,w,lam};
let pos=Array(n);ord.forEach((v,i)=>pos[v]=i);
let ep=Array.from({length:n},()=>[]),hp=Array.from({length:n},()=>[]);
for(const [a,b,c] of edges){if(pos[a]>pos[b])ep[pos[a]].push([b,c]);else ep[pos[b]].push([a,c])}
for(const f of hard)hp[Math.max(...f.v.map(v=>pos[v]))].push(f);
let D=new Map([["0|",{sum:0,word:"",e:0,count:1n,history:""}]]),localPeak=1;
for(let i=0;i<n;i++){let next=new Map(),v=ord[i];for(const st of D.values())for(const b of p[v]?[p[v]]:[-1,1]){L.transitions++;let x=Array(n).fill(0);fr[i].forEach((u,j)=>x[u]=st.word[j]==="1"?1:-1);x[v]=b;if(hp[i].some(f=>!legal(f,x)))continue;
let e=st.e+ep[i].reduce((s,[u,c])=>s+c*x[u]*b,0),sum=st.sum+b,word=fr[i+1].map(u=>x[u]===1?"1":"0").join(""),key=sum+"|"+word,old=next.get(key),hist=st.history+(b===1?"1":"0");
if(!old||e<old.e)next.set(key,{sum,word,e,count:st.count,history:hist});else if(e===old.e){old.count+=st.count;L.merges++}}
D=next;L.sumStates+=D.size;localPeak=Math.max(localPeak,D.size);L.peakStates=Math.max(L.peakStates,D.size)}
let count=0n,witness=null,min=Infinity;for(const st of D.values()){let energy=m+st.e+lam*(st.sum*st.sum-n)/2;ok(energy>=0&&energy%4===0);min=Math.min(min,energy/4);if(energy===0){count+=st.count;if(!witness){witness=Array(n);ord.forEach((v,i)=>witness[v]=st.history[i]==="1"?1:-1)}}}
if(witness){ok(F.every(f=>legal(f,witness))&&p.every((b,i)=>!b||b===witness[i]));L.verifiedWitnesses++}return {count,w,lam,peak:localPeak,min:Number.isFinite(min)?min:null};
}
function ref(n,F,p=Array(n).fill(0)){let c=0n;for(let a=0;a<2**n;a++){L.referenceWords++;let x=Array.from({length:n},(_,i)=>(a>>i&1)?1:-1);if(p.every((b,i)=>!b||b===x[i])&&F.every(f=>legal(f,x)))c++}return c}
function factor(v,b=3,s=[1,1,1]){return {v,b,s}}
function sts(k){let n=2**k-1,F=[];for(let a=1;a<=n;a++)for(let b=a+1;b<=n;b++){let c=a^b;if(c>b)F.push(factor([a-1,b-1,c-1]))}return F}
let groups={},scales=[];
function test(group,n,F,p=Array(n).fill(0),expected=null,cap=12){let r=solve(n,F,p,cap);let g=groups[group]??={sat:0,unsat:0,unknown:0};if(r.unknown){g.unknown++;return r}let target=expected===null?ref(n,F,p):expected;ok(r.count===target);g[r.count?"sat":"unsat"]++;return r}
let F=sts(3);for(let a=0;a<128;a++)test("Fano all edge subsets",7,F.filter((_,i)=>a>>i&1));
for(let i=0;i<7;i++)for(let b of [1,2])test("Fano single owner",7,F.map((f,j)=>i===j?{...f,b}:f),Array(7).fill(0),5n);
let seed=20261124;function rng(k){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%k}
for(let t=0;t<100;t++){let n=7,H=[],p=Array(n).fill(0);for(let j=0;j<4+t%11;j++){let v=[];while(v.length<3){let q=rng(n);if(!v.includes(q))v.push(q)}H.push(factor(v,1+rng(3),Array.from({length:3},()=>rng(2)?1:-1)))}if(t%3===0)p[rng(n)]=rng(2)?1:-1;test("signed guarded random",n,H,p)}
for(let k=3;k<=6;k++){let n=2**k-1,H=sts(k);for(let b of [3,1]){let G=H.map((f,i)=>i===0?{...f,b}:f);let r=test("Steiner scales",n,G,Array(n).fill(0),b===1&&k===3?5n:0n);scales.push({family:"Steiner",n,m:G.length,mask:b,...r,count:r.count?.toString()})}}
for(let k of [5,12,24,48]){let n=2*k,H=Array.from({length:k},(_,i)=>factor([i,(i+1)%k,k+i]));let expected=3n**BigInt(k)+(-1n)**BigInt(k); // trace [[1,2],[2,1]]^k
let r=test("Berge cycles",n,H,Array(n).fill(0),expected);scales.push({family:"Berge cycle",n,m:k,...r,count:r.count?.toString()});
let p=Array(n).fill(0);H[0].v.forEach(v=>p[v]=1);test("Berge cycle guarded UNSAT",n,H,p,0n)}
return {groups,scales,ledger:L,seed:20261124};
}
console.log(JSON.stringify(run(),null,2));
