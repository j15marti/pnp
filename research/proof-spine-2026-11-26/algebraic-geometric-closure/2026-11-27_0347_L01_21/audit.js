function check(x,m="assertion"){if(!x)throw Error(m)}

function bit(x,j){return Number((x>>BigInt(j))&1n)}

function parity(x){let p=0;while(x){p^=1;x&=x-1n}return p}

function weight(x){let n=0;while(x){n++;x&=x-1n}return n}

function fixture(k=0){let T=[[2,4,6],[3,7,8],[1,2,3],[5,6,7],[1,2,5],[2,3,7],[2,5,8],[0,3,7],[6,7,8],[0,3,6],[4,5,8],[1,4,8]],m=9;for(let j=0;j<k;j++){T.push(...[[0,1,2],[3,4,5],[0,3,4],[1,2,5]].map(a=>a.map(i=>i+m)));m+=6}return {T,m,q:m/3}}

function chart(F,pins=[]){let t=F.T.length,R=Array.from({length:F.m},()=>1n<<BigInt(t));for(let j=0;j<t;j++)for(let i of F.T[j])R[i]|=1n<<BigInt(j);for(let [j,b] of pins)R.push((1n<<BigInt(j))|(BigInt(b)<<BigInt(t)));let P=[],r=0;for(let j=0;j<t;j++){let i=r;while(i<R.length&&!bit(R[i],j))i++;if(i===R.length)continue;[R[i],R[r]]=[R[r],R[i]];for(let l=0;l<R.length;l++)if(l!==r&&bit(R[l],j))R[l]^=R[r];P.push(j);r++}if(R.some(x=>x===1n<<BigInt(t)))return null;let x0=0n;for(let i=0;i<r;i++)if(bit(R[i],t))x0|=1n<<BigInt(P[i]);let B=[];for(let j=0;j<t;j++)if(!P.includes(j)){let v=1n<<BigInt(j);for(let i=0;i<r;i++)if(bit(R[i],j))v|=1n<<BigInt(P[i]);B.push(v)}return {x0,B,t}}

function rows(F){let R=Array.from({length:F.m},()=>[]);F.T.forEach((C,j)=>C.forEach(i=>R[i].push(j)));return R}

function defect(R,x){let D=R.map(a=>a.reduce((s,j)=>s+bit(x,j),0));return {w:weight(x),Q:D.reduce((s,d)=>s+d*(d-1)/2,0),odd:D.every(d=>d%2===1),cycles:1+D.reduce((s,d)=>s+Math.abs(d-1),0)}}

function words(A){check(A.B.length<=16,"reference dimension cap");let W=[A.x0];for(let v of A.B)W.push(...W.map(x=>x^v));return W}

function gcd(a,b){a=Math.abs(a);b=Math.abs(b);while(b)[a,b]=[b,a%b];return a}

function mod(x,p){return ((x%p)+p)%p}

function addTerm(A,k,v,p){let a=mod((A.get(k)||0)+v,p);if(a)A.set(k,a);else A.delete(k)}

function add(A,B,p,c=1){let C=new Map(A);for(let [k,v] of B)addTerm(C,k,c*v,p);return C}

function mul(A,B,p,L){let C=new Map();for(let [a,u] of A)for(let [b,v] of B){check(++L.ops<=L.cap,"dictionary cap");addTerm(C,a^b,u*v,p)}L.peak=Math.max(L.peak,C.size);return C}

function pow(A,n,p,L){let B=new Map([[0n,1]]);for(let i=0;i<n;i++)B=mul(B,A,p,L);return B}

function indicator(A,p,L){return add(new Map([[0n,1]]),pow(A,p-1,p,L),p,-1)}

function spectral(F,A,p,cap=1000000){let L={ops:0,peak:0,cap},X=[];let inv=(p+1)/2;for(let j=0;j<A.t;j++){let u=0n;A.B.forEach((v,i)=>{if(bit(v,j))u|=1n<<BigInt(i)});let f=new Map([[0n,inv]]);addTerm(f,u,bit(A.x0,j)?inv:-inv,p);X.push(f)}let W=new Map([[0n,mod(-F.q,p)]]);if(!W.get(0n))W.clear();for(let f of X)W=add(W,f,p);let Q=new Map();for(let a of rows(F))for(let i=0;i<a.length;i++)for(let j=i+1;j<a.length;j++)Q=add(Q,mul(X[a[i]],X[a[j]],p,L),p);let IW=indicator(W,p,L),IQ=indicator(Q,p,L),J=mul(IW,IQ,p,L);return {W,Q,IW,IQ,J,L}}

function evalPoly(A,z,p){let n=0;for(let [k,v] of A)n+=parity(k&z)?-v:v;return mod(n,p)}

function native(F){let R=rows(F),Cen=[],leaves=F.T.map(()=>[]),s=0;for(let a of R){let c=s++,L=a.map(j=>[j,s++]),e=s++;Cen.push([c,e]);for(let [j,u] of L.reverse())leaves[j].push([u,s++])}let p=Array.from({length:s},(_,i)=>(i+1)%s),g=Array.from({length:s},(_,i)=>i),K=g.slice(),owner=Array(s).fill(-1);for(let [u,v] of Cen)[p[u],p[v]]=[p[v],p[u]];leaves.forEach((L,j)=>{let V=L.flat();V.forEach((u,k)=>{g[u]=V[(k+1)%V.length];owner[u]=j});for(let [u,v] of L){K[u]=v;K[v]=u}});let E=Array.from({length:3*s},()=>[]);for(let i=0;i<s;i++){let u=s+2*i,v=u+1;E[i].push(u);E[u].push(v);E[v].push(p[i]);if(owner[i]>=0){E[g[i]].push(v);E[v].push(u);E[u].push(p[K[g[i]]])}}return {s,p,g,K,owner,E}}

function lift(G,x){let P=Array(3*G.s).fill(-1);for(let i=0;i<G.s;i++){let u=G.s+2*i,v=u+1;if(G.owner[i]>=0&&bit(x,G.owner[i])){P[G.g[i]]=v;P[v]=u;P[u]=G.p[G.K[G.g[i]]]}else{P[i]=u;P[u]=v;P[v]=G.p[i]}}return P}

function cycles(P){let S=new Set();check(P.every(v=>v>=0&&v<P.length)&&new Set(P).size===P.length,"not permutation");let k=0;for(let i=0;i<P.length;i++)if(!S.has(i)){k++;let j=i;while(!S.has(j)){S.add(j);j=P[j]}}return k}

function strongly(G){for(let rev of [false,true]){let A=G.E;if(rev){A=G.E.map(()=>[]);G.E.forEach((L,i)=>L.forEach(j=>A[j].push(i)))}let seen=new Set([0]),todo=[0];while(todo.length){let i=todo.pop();for(let j of A[i])if(!seen.has(j)){seen.add(j);todo.push(j)}}if(seen.size!==A.length)return false}return true}

function verifyLift(G,R,x){let P=lift(G,x),c=cycles(P);check(P.every((v,i)=>G.E[i].includes(v)),"native arc");check(c===defect(R,x).cycles,"Cohn-Lempel lift");return {P,c}}

function support(G,F){let R=rows(F),S=G.E.map(()=>new Set());let t=F.T.length;for(let j=0;j<t;j++){let x=1n<<BigInt(j);if(F.m%2===0)x|=1n<<BigInt((j+1)%t);let {P,c}=verifyLift(G,R,x);check(c%2===1);P.forEach((v,i)=>S[i].add(v))}check(strongly(G));check(G.E.every((L,i)=>L.every(v=>S[i].has(v))),"unsupported arc");return t}

function coeff(A){return [...A].map(([k,v])=>[k.toString(),v]).sort((a,b)=>a[0].localeCompare(b[0]))}

function desc(S){return {W:coeff(S.W),Q:coeff(S.Q),IW:coeff(S.IW),IQ:coeff(S.IQ),J:coeff(S.J),pairOperations:S.L.ops,peakOutputTerms:S.L.peak}}

function audit(){let F=fixture(),A=chart(F),R=rows(F),G=native(F);check(A.B.length===3);let numerator=[1,0,0,1,1,0,1,2,0,1,0,2];check(R.every(a=>a.reduce((s,j)=>s+numerator[j],0)===3));let V=words(A).map(x=>({x:x.toString(),...defect(R,x)}));check(V.every(v=>v.odd&&v.w>F.q));let g=V.reduce((s,v)=>gcd(s,v.w-V[0].w),0);check((F.q-V[0].w)%g===0);let tests=[];for(let p of [3,5,7]){let S=spectral(F,A,p);for(let z=0;z<2**A.B.length;z++){let v=V[z];check(evalPoly(S.W,BigInt(z),p)===mod(v.w-F.q,p));check(evalPoly(S.Q,BigInt(z),p)===mod(v.Q,p));check(evalPoly(S.J,BigInt(z),p)===Number(mod(v.w-F.q,p)===0&&mod(v.Q,p)===0))}check(S.J.size===0);tests.push({p,...desc(S)})}check(tests[0].IW.length&&tests[0].IQ.length);let guards=[];for(let j=0;j<A.t;j++)for(let b of [0,1]){let H=chart(F,[[j,b]]);check(H);let S=spectral(F,H,3);check(!S.J.size);let W=words(H);check(W.every(x=>bit(x,j)===b&&defect(R,x).odd&&defect(R,x).w>F.q));guards.push({j,b,dimension:H.B.length,ops:S.L.ops})}
let hc=0,hist={};for(let x=0;x<2**A.t;x++){let {c}=verifyLift(G,R,BigInt(x));hist[c]=(hist[c]||0)+1;if(c===1)hc++}check(hc===0);let supported=support(G,F);let scale=[];for(let k of [0,1,4,16,64,128]){let F=fixture(k),A=chart(F),G=native(F),S=spectral(F,A,3);check(A.B.length===k+3&&S.J.size===0&&S.IW.size>0&&S.IQ.size>0);let lifts=support(G,F);scale.push({k,vertices:G.E.length,arcs:G.E.reduce((s,L)=>s+L.length,0),dimension:A.B.length,affineWords:(1n<<BigInt(A.B.length)).toString(),nativeSupportLifts:lifts,W:S.W.size,Q:S.Q.size,IW:S.IW.size,IQ:S.IQ.size,J:S.J.size,ops:S.L.ops,peak:S.L.peak})}
let seed=27021;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}let random=0;for(let i=0;i<200;i++){let t=3+rnd(8),d=1+rnd(6),m=3*(1+rnd(3)),T=[];for(let j=0;j<t;j++){let a=new Set();while(a.size<3)a.add(rnd(m));T.push([...a])}let F={T,m,q:m/3},A={t,x0:BigInt(rnd(2**t)),B:Array.from({length:d},()=>BigInt(rnd(2**t)))},R=rows(F),V=words(A);for(let p of [3,5,7]){let S=spectral(F,A,p);let count=0;for(let z=0;z<V.length;z++){let v=defect(R,V[z]),b=Number(mod(v.w-F.q,p)===0&&mod(v.Q,p)===0);check(evalPoly(S.J,BigInt(z),p)===b);count+=b;random++}check((S.J.size>0)===(count>0))}}
let L={ops:0,peak:0,cap:10000},x=new Map([[0n,2],[1n,1]]),y=new Map([[0n,2],[2n,1]]),I=indicator(mul(x,y,3,L),3,L);check(!I.has(0n)&&I.size===3);let yes={T:[[0,1,2]],m:3,q:1},YA=chart(yes);check(spectral(yes,YA,3).J.size===1&&cycles(lift(native(yes),1n))===1);
let hostile=[];for(let p of [3,5,7]){let b=3*p,T=[];for(let i=0;i<b;i++)T.push(...[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map(a=>a.map(z=>z+7*i)));let F={T,m:7*b,q:7*b/3},x=0n;for(let i=0;i<b;i++)x|=7n<<BigInt(7*i);let v=defect(rows(F),x);check(v.odd&&v.w===3*b&&mod(v.w-F.q,p)===0&&mod(v.Q,p)===0);hostile.push({p,b,weight:v.w,required:F.q,Q:v.Q,commonResidueWitness:x.toString(),proof:"each disjoint 7-point block has no exact cover by triples"})}
return {fixture:F,affine:{x0:A.x0.toString(),B:A.B.map(String)},values:V,gcd:g,fractionalNumerator:numerator,fractionalDenominator:3,tests,guards,native:{vertices:G.E.length,arcs:G.E.reduce((s,L)=>s+L.length,0),phaseChecks:2**A.t,hist,supportLifts:supported},scale,randomPointChecks:random,zeroCountControl:coeff(I),hostile,execution:"serial; fixed dictionary cap 1000000 per spectral query, reference cap 16 directions; no general HC oracle"}}
console.log(JSON.stringify(audit(),null,2));
