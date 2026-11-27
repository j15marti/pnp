function check(b,m){if(!b)throw Error(m||"assertion")}

function pop(x){let k=0;for(;x;x&=x-1n)k++;return k}

function bit(i){return 1n<<BigInt(i)}

function gf(rows,t){let a=rows.map(r=>[r[0],r[1]]),p=[],r=0;for(let j=0;j<t;j++){let k=a.findIndex((z,i)=>i>=r&&(z[0]&bit(j)));if(k<0)continue;[a[k],a[r]]=[a[r],a[k]];for(k=0;k<a.length;k++)if(k!==r&&(a[k][0]&bit(j))){a[k][0]^=a[r][0];a[k][1]^=a[r][1]}p.push(j);r++}if(a.some(z=>!z[0]&&z[1]))return null;let x=0n,B=[];for(let i=0;i<r;i++)if(a[i][1])x|=bit(p[i]);for(let j=0;j<t;j++)if(!p.includes(j)){let v=bit(j);for(let i=0;i<r;i++)if(a[i][0]&bit(j))v|=bit(p[i]);B.push(v)}return {x,B,t}}

function chart(T,m,pins=[]){let t=T.length,rows=Array.from({length:m},(_,i)=>[T.reduce((r,e,j)=>e.includes(i)?r|bit(j):r,0n),1]);return gf([...rows,...pins.map(([j,b])=>[bit(j),b])],t)}

function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b)[a,b]=[b,a%b];return a}

function mod(a,m){return (a%m+m)%m}

function egcd(a,b){let x=1n,y=0n,u=0n,v=1n;while(b){let q=a/b;[a,b]=[b,a-q*b];[x,u]=[u,x-q*u];[y,v]=[v,y-q*v]}return a<0n?[-a,-x,-y]:[a,x,y]}

function orbit(A){let {t,x,B}=A,n=t+1,M=1n;for(let i=2;i<=n;i++)M*=BigInt(i);M*=2n;let H=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i===j?M:0n)),inserts=0;
 function insert(w){inserts++;w=w.map(z=>mod(z,M));for(let i=0;i<n;i++){let a=H[i][i],b=w[i];if(!b)continue;let [g,s,u]=egcd(a,b),R=H[i].slice(),V=w.slice();for(let j=i;j<n;j++){H[i][j]=s*R[j]+u*V[j];w[j]=(-b/g)*R[j]+(a/g)*V[j]}check(H[i][i]===g&&!w[i]);for(let j=i+1;j<n;j++){H[i][j]=mod(H[i][j],M);w[j]=mod(w[j],M)}}}
 insert([1n,...Array.from({length:t},(_,i)=>x&bit(i)?1n:0n)]);
 for(const b of B){let old=H.map(r=>r.slice());for(let r of old){for(let j=0;j<t;j++)if(b&bit(j))r[j+1]=r[0]-r[j+1];insert(r)}}
 let w0=BigInt(pop(x)),g=0n;for(let r of H)g=gcd(g,r.slice(1).reduce((a,b)=>a+b,0n)-w0*r[0]);return {w0:Number(w0),g:g===M?0:Number(g),inserts,modulus:String(M)}}

function mod4(A){let {x,B}=A;let w=pop(x),linear=B.map(v=>pop(v)-2*pop(v&x)),oddPairs=0;for(let i=0;i<B.length;i++)for(let j=0;j<i;j++)if(pop(B[i]&B[j])%2)oddPairs++;return {w,linear,oddPairs,constant:linear.every(z=>z%4===0)&&oddPairs===0}}

function all(A){check(A.B.length<=16,"cap");let W=[A.x];for(let b of A.B)W=W.concat(W.map(v=>v^b));return W}

function brute(A){let W=all(A),weights=[...new Set(W.map(pop))].sort((a,b)=>a-b),g=0n;for(let w of weights)g=gcd(g,BigInt(w-pop(A.x)));return {count:W.length,weights,g:Number(g)}}

function occupancy(T,m,x){return Array.from({length:m},(_,i)=>T.reduce((s,e,j)=>s+(e.includes(i)&&x&bit(j)?1:0),0))}

function native(T,m){let labels=[],C=[],centers=[],leaf=Array.from({length:T.length},()=>[]);for(let i=0;i<m;i++){let inc=T.map((e,j)=>e.includes(i)?j:-1).filter(j=>j>=0),a=labels.length;labels.push([i,"center",0]);let first=[];for(let j of inc){first.push(labels.length);labels.push([i,j,0])}let b=labels.length;labels.push([i,"center",1]);centers.push([a,b]);for(let k=inc.length-1;k>=0;k--){leaf[inc[k]].push([first[k],labels.length]);labels.push([i,inc[k],1])}}
 let s=labels.length,p=Array.from({length:s},(_,i)=>(i+1)%s);for(let [a,b] of centers)[p[a],p[b]]=[p[b],p[a]];
 let owner=Array(s).fill(-1),k=Array.from({length:s},(_,i)=>i),g=k.slice();for(let j=0;j<leaf.length;j++){let L=leaf[j].flat();check(L.length===6);for(let z=0;z<6;z++){owner[L[z]]=j;g[L[z]]=L[(z+1)%6]}for(let [a,b] of leaf[j]){k[a]=b;k[b]=a}}
 let E=new Set(),edge=(a,b)=>{check(a!==b);E.add(a*3*s+b)};for(let i=0;i<s;i++){let u=s+2*i,v=u+1;edge(i,u);edge(u,v);edge(v,p[i]);if(owner[i]>=0){edge(g[i],v);edge(v,u);edge(u,p[k[g[i]]])}}
 function lift(x){let out=Array(3*s).fill(-1);for(let i=0;i<s;i++){let u=s+2*i,v=u+1,on=owner[i]>=0&&!!(x&bit(owner[i]));if(on){out[g[i]]=v;out[v]=u;out[u]=p[k[g[i]]]}else{out[i]=u;out[u]=v;out[v]=p[i]}}
 check(new Set(out).size===3*s&&out.every((v,i)=>E.has(i*3*s+v)),"native map");let seen=new Set(),cycles=0;for(let i=0;i<out.length;i++)if(!seen.has(i)){cycles++;let v=i;while(!seen.has(v)){seen.add(v);v=out[v]}}return {out,cycles}}
 function strong(){for(let rev of [false,true]){let adj=Array.from({length:3*s},()=>[]);for(let e of E){let a=Math.floor(e/(3*s)),b=e%(3*s);adj[rev?b:a].push(rev?a:b)}let seen=new Set([0]),stack=[0];while(stack.length){for(let v of adj[stack.pop()])if(!seen.has(v)){seen.add(v);stack.push(v)}}if(seen.size!==3*s)return false}return true}
 return {s,E,lift,strong}}

function ring(b){const F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],T=[];for(let i=0;i<b;i++)for(let j=0;j<7;j++)T.push(F[j].map(z=>7*((j===0&&z===0)?(i+1)%b:(j===3&&z===1)?(i+b-1)%b:i)+z));return T}

function patch(A,J){let basis=[];for(let v of A.B){let w=0n;J.forEach((j,i)=>{if(v&bit(j))w|=bit(i)});for(let b of basis){let high=1n<<BigInt(b.toString(2).length-1);if(w&high)w^=b}if(w){basis.push(w);basis.sort((a,b)=>a>b?-1:1)}}let x=0n;J.forEach((j,i)=>{if(A.x&bit(j))x|=bit(i)});let W=all({x,B:basis});return {rank:basis.length,min:Math.min(...W.map(pop)),words:W.length}}

function run(){let T=[[0,7,8],[0,2,8],[0,3,4],[5,6,7],[1,3,5],[0,1,5],[3,4,8],[1,6,7],[3,5,6],[3,6,8],[1,2,7],[2,6,8]],m=9,A=chart(T,m),O=orbit(A),F=mod4(A),R=brute(A);check(O.g===R.g&&O.g===4&&F.constant&&R.weights.join(",")==="5,9");
 let frac=[0,0,1,1,0,1,1,0,0,0,1,1],signed=[-2,8,-1,1,3,-4,2,6,1,-4,-4,-3];for(let i=0;i<m;i++){check(T.reduce((s,e,j)=>s+(e.includes(i)?frac[j]:0),0)===2);check(T.reduce((s,e,j)=>s+(e.includes(i)?signed[j]:0),0)===1)}check(A.B.reduce((v,b)=>v|b,0n)===(bit(T.length)-1n));
 let G=native(T,m),hist={},support=new Set(),tours=0,ref=0;for(let x=0n;x<bit(T.length);x++){let d=occupancy(T,m,x),c=1+d.reduce((s,v)=>s+Math.abs(v-1),0),r=G.lift(x);check(r.cycles===c);hist[c]=(hist[c]||0)+1;ref++;if(c===1)tours++;if(c%2)r.out.forEach((v,i)=>support.add(i*3*G.s+v))}check(!tours&&support.size===G.E.size&&G.strong());
 let guardTests=[];for(let j=0;j<T.length;j++)for(let b of [0,1]){let C=chart(T,m,[[j,b]]),o=orbit(C),r=brute(C);check(o.g===r.g&&(o.g?(3-o.w0)%o.g!==0:3!==o.w0));guardTests.push({j,b,dimension:C.B.length,g:o.g,weights:r.weights})}
 let scale=[];for(let b of [3,6,9,12,21,48]){let U=ring(b),C=chart(U,7*b),f=mod4(C),q=7*b/3;check(C.B.length===b+2&&f.constant);let min=0,words=0;for(let i=0;i<b;i++){let p=patch(C,Array.from({length:7},(_,j)=>7*i+j));min+=p.min;words+=p.words}check(min===3*b&&min>q);let o=b<=6?orbit(C):null;if(o)check(o.g===4);let nativeG=native(U,7*b);check(nativeG.strong());let sup=new Set(),base=bit(U.length)-1n;for(let i=-1;i<U.length-1;i++){let x=i<0?base:base^bit(i)^bit(U.length-1),r=nativeG.lift(x);check(r.cycles===1+occupancy(U,7*b,x).reduce((s,v)=>s+Math.abs(v-1),0)&&r.cycles%2===1);r.out.forEach((v,j)=>sup.add(j*3*nativeG.s+v))}check(sup.size===nativeG.E.size);scale.push({b,n:3*nativeG.s,arcs:nativeG.E.size,dimension:C.B.length,words:2**Math.min(C.B.length,52),mod4Residue:mod(BigInt(f.w),4n).toString(),q,modularNO:(q-f.w)%4!==0,patchMin:min,patchWords:words,orbit:o,signSupport:sup.size})}
 let seed=2701;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}let random=0;for(let t=1;t<=10;t++)for(let z=0;z<20;z++){let x=BigInt(rand(2**t)),B=Array.from({length:rand(Math.min(t,7)+1)},()=>BigInt(rand(2**t))),C={x,B,t};let a=orbit(C),r=brute(C),f=mod4(C);check(a.g===r.g&&f.constant===r.weights.every(w=>(w-f.w)%4===0));random++}
 let yes=chart([[0,1,2]],3),o=orbit(yes);check(o.g===0&&o.w0===1&&native([[0,1,2]],3).lift(1n).cycles===1);
 return {fixture:{T,m,t:T.length,dimension:A.B.length,x:A.x.toString(),basis:A.B.map(String),orbit:O,mod4:F,reference:R,fractionalNumerators:frac,signedInteger:signed,n:3*G.s,arcs:G.E.size,referencePhaseWords:ref,cycleHistogram:hist,tours,signSupport:support.size},guardTests,scale,random,yes:{weight:o.w0,g:o.g},mode:"serial exact integer audit; finite reference cap 2^16, full-rank modular lattice implementation on small charts, mod4 polynomial test on scales"}}
console.log(JSON.stringify(run(),null,2));
