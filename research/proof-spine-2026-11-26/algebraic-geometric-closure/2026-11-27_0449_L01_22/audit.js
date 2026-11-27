function check(x,m="assertion"){if(!x)throw Error(m)}

function bit(x,j){return Number(x>>BigInt(j)&1n)}

function parity(x){let p=0;while(x){p^=1;x&=x-1n}return p}

function pivot(x){return x.toString(2).length-1}

function insert(M,v,b=0){while(v){let p=pivot(v),r=M.get(p);if(!r){M.set(p,[v,b]);return true}v^=r[0];b^=r[1]}return !b}

function basis(V){let M=new Map();for(let v of V)insert(M,v);return [...M.values()].map(x=>x[0])}

function intersect(A,B){let M=new Map(),out=[];for(let a of A){let v=a,k=a;while(v&&M.has(pivot(v))){let [u,w]=M.get(pivot(v));v^=u;k^=w}if(v)M.set(pivot(v),[v,k])}for(let b of B){let v=b,k=0n;while(v&&M.has(pivot(v))){let [u,w]=M.get(pivot(v));v^=u;k^=w}if(v)M.set(pivot(v),[v,k]);else if(k)out.push(k)}return basis(out)}

function rows(F){let R=Array.from({length:F.m},()=>[]);F.T.forEach((C,j)=>C.forEach(i=>R[i].push(j)));return R}

function chart(F,pins=[]){let t=F.T.length,R=rows(F).map(a=>a.reduce((s,j)=>s|(1n<<BigInt(j)),1n<<BigInt(t)));for(let [j,b] of pins)R.push((1n<<BigInt(j))|(BigInt(b)<<BigInt(t)));let P=[],r=0;for(let j=0;j<t;j++){let i=r;while(i<R.length&&!bit(R[i],j))i++;if(i===R.length)continue;[R[i],R[r]]=[R[r],R[i]];for(let l=0;l<R.length;l++)if(l!==r&&bit(R[l],j))R[l]^=R[r];P.push(j);r++}if(R.some(x=>x===1n<<BigInt(t)))return null;let x0=0n;for(let i=0;i<r;i++)if(bit(R[i],t))x0|=1n<<BigInt(P[i]);let B=[];for(let j=0;j<t;j++)if(!P.includes(j)){let v=1n<<BigInt(j);for(let i=0;i<r;i++)if(bit(R[i],j))v|=1n<<BigInt(P[i]);B.push(v)}return {x0,B,t}}

function term(M,k,v){v=((v+(M.get(k)||0))%3+3)%3;if(v)M.set(k,v);else M.delete(k)}

function plus(A,B,c=1){let C=new Map(A);for(let [k,v] of B)term(C,k,c*v);return C}

function mul(A,B,L){let C=new Map();for(let [a,u] of A)for(let [b,v] of B){if(++L.ops>L.cap)throw Error("CAP");term(C,a^b,u*v)}L.peak=Math.max(L.peak,C.size);return C}

function factors(F,A){let one=new Map([[0n,1]]),X=[];for(let j=0;j<A.t;j++){let u=0n;A.B.forEach((v,i)=>{if(bit(v,j))u|=1n<<BigInt(i)});let f=new Map([[0n,2]]);term(f,u,bit(A.x0,j)?2:-2);X.push(f)}let L={ops:0,cap:1000000,peak:0};let fs=rows(F).map(a=>{let I=new Map();for(let j of a){let P=X[j];for(let k of a)if(k!==j)P=mul(P,plus(one,X[k],-1),L);I=plus(I,P)}return I});return {fs,L}}

function boundaries(fs){let U=fs.map(f=>basis([...f.keys()])),P=[[]],S=Array(fs.length+1);S[fs.length]=[];for(let a of U)P.push(basis([...P.at(-1),...a]));for(let i=fs.length-1;i>=0;i--)S[i]=basis([...U[i],...S[i+1]]);return P.map((a,i)=>intersect(a,S[i]))}

function restricted(f,A,a,B,b,L){let M=new Map();for(let [V,k] of [[A,a],[B,b]])for(let j=0;j<V.length;j++)if(!insert(M,V[j],(k>>j)&1))return false;let C=new Map();for(let [u,c] of f){if(++L.ops>L.cap)throw Error("CAP");let v=u,s=0;for(let p of [...M.keys()].sort((a,b)=>b-a))if(bit(v,p)){let [w,r]=M.get(p);v^=w;s^=r}term(C,v,s?-c:c)}return C.size>0}

function frontier(fs,cap=65536){let B=boundaries(fs),state=[0],L={ops:0,cap},pairs=0,trace=[1],max=Math.max(...B.map(x=>x.length));if(max>12)return {status:"UNKNOWN_WIDTH",max};try{for(let i=0;i<fs.length;i++){let next=[];for(let b=0;b<2**B[i+1].length;b++)for(let a of state){if(++pairs>cap)throw Error("CAP");if(restricted(fs[i],B[i],a,B[i+1],b,L)){next.push(b);break}}state=next;trace.push(state.length);if(!state.length)break}return {status:state.length?"NONEMPTY":"NO",max,terms:L.ops,pairs,trace,cutRanks:B.map(x=>x.length)}}catch(e){if(e.message!=="CAP")throw e;return {status:"UNKNOWN_CAP",max,terms:L.ops,pairs,trace}}}

function product(fs,cap=65536){let L={ops:0,cap,peak:1},P=new Map([[0n,1]]),trace=[];try{for(let f of fs){P=mul(P,f,L);trace.push(P.size);if(!P.size)break}return {status:P.size?"NONEMPTY":"NO",ops:L.ops,peak:L.peak,trace}}catch(e){if(e.message!=="CAP")throw e;return {status:"UNKNOWN_CAP",ops:L.ops,peak:L.peak,trace}}}

function evalF(f,z){let a=0;for(let [k,v] of f)a+=parity(k&z)?-v:v;return (a%3+3)%3}

function ref(fs,d){check(d<=16,"reference cap");let count=0,individual=fs.map(()=>0),prefix=fs.map(()=>0);for(let i=0;i<2**d;i++){let alive=true;for(let j=0;j<fs.length;j++){let v=evalF(fs[j],BigInt(i));check(v===0||v===1);individual[j]+=v;alive=alive&&v===1;prefix[j]+=Number(alive)}count+=Number(alive)}return {count,individual,prefix,points:2**d}}

function fixture(k){let T=[],m=0;for(let j=0;j<k;j++){T.push(...[[0,1,2],[3,4,5],[0,3,4],[1,2,5],[0,1,5],[2,3,4]].map(a=>a.map(i=>i+m)));m+=6}T.push(...[[2,4,6],[3,7,8],[1,2,3],[5,6,7],[1,2,5],[2,3,7],[2,5,8],[0,3,7],[6,7,8],[0,3,6],[4,5,8],[1,4,8]].map(a=>a.map(i=>i+m)));return {T,m:m+9}}

function fano(b){let T=[];for(let i=0;i<b;i++){let a=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map(a=>a.map(x=>7*i+x));a[0][0]=7*((i+1)%b);a[3][0]=7*((i+b-1)%b)+1;T.push(...a)}return {T,m:7*b}}

function native(F){let Cen=[],leaves=F.T.map(()=>[]),s=0;for(let a of rows(F)){let c=s++,L=a.map(j=>[j,s++]),e=s++;Cen.push([c,e]);for(let [j,u] of L.reverse())leaves[j].push([u,s++])}let p=Array.from({length:s},(_,i)=>(i+1)%s),g=Array.from({length:s},(_,i)=>i),K=g.slice(),owner=Array(s).fill(-1);for(let [u,v] of Cen)[p[u],p[v]]=[p[v],p[u]];leaves.forEach((L,j)=>{let V=L.flat();V.forEach((u,k)=>{g[u]=V[(k+1)%V.length];owner[u]=j});for(let [u,v] of L){K[u]=v;K[v]=u}});let E=Array.from({length:3*s},()=>[]);for(let i=0;i<s;i++){let u=s+2*i,v=u+1;E[i].push(u);E[u].push(v);E[v].push(p[i]);if(owner[i]>=0){E[g[i]].push(v);E[v].push(u);E[u].push(p[K[g[i]]])}}return {s,p,g,K,owner,E}}

function lift(G,x){let P=Array(3*G.s).fill(-1);for(let i=0;i<G.s;i++){let u=G.s+2*i,v=u+1;if(G.owner[i]>=0&&bit(x,G.owner[i])){P[G.g[i]]=v;P[v]=u;P[u]=G.p[G.K[G.g[i]]]}else{P[i]=u;P[u]=v;P[v]=G.p[i]}}return P}

function cycles(P){check(new Set(P).size===P.length&&P.every(v=>v>=0&&v<P.length));let S=new Set(),n=0;for(let i=0;i<P.length;i++)if(!S.has(i)){n++;for(let j=i;!S.has(j);j=P[j])S.add(j)}return n}

function strong(E){for(let rev of [false,true]){let A=E;if(rev){A=E.map(()=>[]);E.forEach((a,i)=>a.forEach(j=>A[j].push(i)))}let S=new Set([0]),q=[0];while(q.length){let i=q.pop();for(let j of A[i])if(!S.has(j)){S.add(j);q.push(j)}}if(S.size!==E.length)return false}return true}

function verify(F,G,x){let P=lift(G,x),c=cycles(P);check(P.every((v,i)=>G.E[i].includes(v)));check(c===1+rows(F).reduce((s,a)=>s+Math.abs(a.reduce((s,j)=>s+bit(x,j),0)-1),0));return {P,c}}

function support(F,G){let S=G.E.map(()=>new Set());for(let j=0;j<F.T.length;j++){let x=1n<<BigInt(j);if(F.m%2===0)x|=1n<<BigInt((j+1)%F.T.length);let {P,c}=verify(F,G,x);check(c%2===1);P.forEach((v,i)=>S[i].add(v))}check(strong(G.E)&&G.E.every((a,i)=>a.every(v=>S[i].has(v))));return F.T.length}

function audit(){let scale=[],base=fixture(0),A=chart(base),G=native(base),f=factors(base,A);let R=ref(f.fs,A.B.length);check(!R.count);let nativeHC=0;for(let i=0;i<4096;i++)nativeHC+=Number(verify(base,G,BigInt(i)).c===1);check(!nativeHC);let guards=[];for(let j=0;j<base.T.length;j++)for(let b=0;b<2;b++){let H=chart(base,[[j,b]]),g=factors(base,H).fs,a=frontier(g),r=ref(g,H.B.length);check(a.status==="NO"&&!r.count);guards.push({j,b,dimension:H.B.length,frontier:a})}
for(let k of [0,1,2,4,8,16,32,64]){let F=fixture(k),A=chart(F),G=native(F),f=factors(F,A),p=product(f.fs),z=frontier(f.fs);check(z.status==="NO");let s=support(F,G);let r=A.B.length<=16?ref(f.fs,A.B.length):null;if(r)check(!r.count);scale.push({k,n:G.E.length,arcs:G.E.reduce((s,a)=>s+a.length,0),dimension:A.B.length,supportLifts:s,factorOps:f.L.ops,product:p,frontier:z,reference:r&&{count:r.count,points:r.points}})}
let connected=[];for(let b of [3,6,12,24]){let F=fano(b),A=chart(F),G=native(F),f=factors(F,A),z=frontier(f.fs),p=product(f.fs);check(z.status==="NO");connected.push({b,n:G.E.length,dimension:A.B.length,supportLifts:support(F,G),frontier:z,product:p,factorOps:f.L.ops})}
let seed=2249;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}let random=0;for(let i=0;i<120;i++){let d=1+rnd(7),fs=[];for(let j=0;j<1+rnd(7);j++){let U=basis(Array.from({length:1+rnd(4)},()=>BigInt(rnd(2**d)))),truth=Array.from({length:2**U.length},()=>rnd(2)),f=new Map();for(let k=0;k<truth.length;k++){let key=0n,c=0;U.forEach((u,j)=>{if((k>>j)&1)key^=u});for(let a=0;a<truth.length;a++)c+=parity(BigInt(a&k))?-truth[a]:truth[a];term(f,key,c*(U.length%2?2:1))}fs.push(f)}let r=ref(fs,d),z=frontier(fs),p=product(fs);check(z.status===(r.count?"NONEMPTY":"NO")&&p.status===z.status);random+=r.points}
let x=new Map([[0n,2],[1n,2]]),y=new Map([[0n,2],[2n,2]]),z=new Map([[0n,2],[3n,1]]);let hostile=[x,y,z];check(ref(hostile,2).count===0&&frontier(hostile).status==="NO");check([0,1,2].every(i=>ref(hostile.filter((_,j)=>i!==j),2).count===1));let yes={T:[[0,1,2]],m:3},Y=chart(yes);check(frontier(factors(yes,Y).fs).status==="NONEMPTY"&&cycles(lift(native(yes),1n))===1);
return {base:{T:base.T,dim:A.B.length,reference:R,nativePhaseChecks:4096,nativeHC},guards,scale,connected,randomPointChecks:random,pairwiseHostile:"x=0,y=0,x+y=1; each pair feasible, global NO",execution:"serial; 65536 coefficient-pair/term and state-pair caps, not equal bit work; factor acquisition separately capped at 1000000"}}
console.log(JSON.stringify(audit(),null,2));
