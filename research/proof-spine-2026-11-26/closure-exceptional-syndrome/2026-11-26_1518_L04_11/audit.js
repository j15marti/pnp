function run(){
let checks=0;const ck=(v,s="")=>{checks++;if(!v)throw Error("assert "+checks+" "+s)};
const min=(a,b)=>a===null?b:b===null?a:a<b?a:b,add=(a,b)=>a===null||b===null?null:a+b;
const mat=(q,fn=()=>null)=>Array.from({length:q},(_,i)=>Array.from({length:q},(_,j)=>fn(i,j))),id=q=>mat(q,(i,j)=>i===j?0n:null),eq=(A,B)=>A.every((r,i)=>r.every((x,j)=>x===B[i][j]));
function prod(A,B,st){if(st)st.products++;let q=A.length,P=mat(q);for(let i=0;i<q;i++)for(let k=0;k<q;k++)if(A[i][k]!==null)for(let j=0;j<q;j++)if(B[k][j]!==null)P[i][j]=min(P[i][j],A[i][k]+B[k][j]);return P}
const vm=(v,A)=>A[0].map((_,j)=>v.reduce((z,x,i)=>min(z,add(x,A[i][j])),null)),merge=(a,b)=>a.map((x,i)=>min(x,b[i]));
function val(x){if(x<=0n)throw Error("valuation");let k=0;while((x&1n)===0n){x>>=1n;k++}return k}
function stream(m,n,M){let q=M[0].length,S=[id(q)];for(let k=0;k<m;k++)S.push(prod(prod(S[k],M[k]),S[k]));return{m,n,M,S,L:(1n<<BigInt(m))-n,q}}
function at(F,i){if(i<0n||i>=F.L)throw Error("stream index");return i===F.L-1n?F.M[F.m]:F.M[val(F.n+i+1n)]}
function suffix(F,i){if(i===F.L)return id(F.q);if(i<0n||i>F.L)throw Error("tail index");function s(k,n){if(!k)return id(F.q);let h=1n<<BigInt(k-1);return n>=h?s(k-1,n-h):prod(prod(s(k-1,n),F.M[k-1]),F.S[k-1])}return prod(s(F.m,F.n+i),F.M[F.m])}
function edges(A,B){let q=A.q,E=[];for(let [t,F] of [[0,A],[1,B]])for(let i=0;i<q;i++)for(let j=0;j<q;j++)if(F.M.some(X=>X[i][j]!==null))E.push([i,j,t]);return E}
function reach(q,E){let R=new Set([0]),Q=[0];for(let k=0;k<Q.length;k++)for(let [i,j] of E)if(i===Q[k]&&!R.has(j)){R.add(j);Q.push(j)}return R}
function acquire(q,E){let R=reach(q,E),F=E.filter(e=>R.has(e[0])),tries=0;
for(let p=1;p<=q;p++)for(let r=1;r<=q;r++){tries++;let lo=Array(q).fill(Infinity),hi=Array(q).fill(-Infinity);lo[0]=hi[0]=0;
for(let z=0;z<q-1;z++){let a=lo.slice(),b=hi.slice();for(let [i,j,t] of F){let d=t?r:-p;a[j]=Math.min(a[j],lo[i]+d);b[j]=Math.max(b[j],hi[i]+d)}lo=a;hi=b}
if(F.some(([i,j,t])=>lo[j]>lo[i]+(t?r:-p)||hi[j]<hi[i]+(t?r:-p)))continue;
let M=Math.max(...[...R].flatMap(i=>[Math.abs(lo[i]),Math.abs(hi[i])])),w=Math.max(1,Math.ceil(M/(p+r)));return{p,r,w,M,lo,hi,tries}}
return null}
function verify(q,E,C){if(!C)return false;let R=reach(q,E);return C.lo[0]===0&&C.hi[0]===0&&[...R].every(i=>Number.isFinite(C.lo[i])&&Number.isFinite(C.hi[i])&&Math.abs(C.lo[i])<=C.M&&Math.abs(C.hi[i])<=C.M)&&E.filter(e=>R.has(e[0])).every(([i,j,t])=>C.lo[j]-C.lo[i]<=(t?C.r:-C.p)&&C.hi[j]-C.hi[i]>=(t?C.r:-C.p))&&C.w>=Math.ceil(C.M/(C.p+C.r))}
function cycleCheck(q,E){let R=reach(q,E),ratios=[],bad=false;function walk(start,u,seen,a,b){for(let [i,j,t] of E)if(i===u){let x=a+(t===0?1:0),y=b+(t===1?1:0);if(j===start){if(!x||!y)bad=true;else ratios.push([y,x])}else if(!seen.has(j)){let S=new Set(seen);S.add(j);walk(start,j,S,x,y)}}}for(let i of R)walk(i,i,new Set([i]),0,0);return !bad&&ratios.every(([a,b])=>a*ratios[0][1]===b*ratios[0][0])}
function finish(v,P,Z){return vm(v,P).reduce((z,x,i)=>min(z,add(x,Z[i])),null)}
function grid(A,B,TA,TB,Z,cap=Infinity){let a=Number(A.L),b=Number(B.L),q=A.q;if(!Number.isSafeInteger(a)||!Number.isSafeInteger(b)||(a+1)*(b+1)>cap)return{unknown:true};let F=Array.from({length:a+1},()=>Array.from({length:b+1},()=>Array(q).fill(null)));F[0][0][0]=0n;
for(let i=0;i<=a;i++)for(let j=0;j<=b;j++){let v=F[i][j];if(i<a)F[i+1][j]=merge(F[i+1][j],vm(v,at(j===b?TA:A,BigInt(i))));if(j<b)F[i][j+1]=merge(F[i][j+1],vm(v,at(i===a?TB:B,BigInt(j))))}return{distance:F[a][b].reduce((z,x,i)=>min(z,add(x,Z[i])),null),cells:(a+1)*(b+1)}}
function strip(A,B,TA,TB,Z,C,compress=true,cap=Infinity){let {p,r,w}=C,q=A.q,s=p+r,P=BigInt(p),R=BigInt(r),S=BigInt(s),W=BigInt(w),D=q*(2*w+1),tot=A.L+B.L,center=k=>R*k/S,other=k=>k-center(k);
let st={products:0,rows:0,nodes:0,hits:0,explicit:0},V=Array(D).fill(null);V[w*q]=0n;let best=null,tails=new Map();
function tail(F,i){let key=(F===TA?"A":"B")+i;if(!tails.has(key))tails.set(key,suffix(F,i));return tails.get(key)}
function explicit(k){if(st.explicit>=cap)throw Error("cap");st.explicit++;st.rows++;let next=Array(D).fill(null),c=center(k),c1=center(k+1n);
for(let d=-w;d<=w;d++){let i=c+BigInt(d),j=k-i;if(i<0n||j<0n||i>=A.L||j>=B.L)continue;let v=V.slice((d+w)*q,(d+w+1)*q);if(v.every(x=>x===null))continue;
for(let t=0;t<2;t++){let ni=i+BigInt(t===0),nj=j+BigInt(t===1),e=ni-c1;if(e< -W||e>W)continue;let u=vm(v,at(t?B:A,t?j:i));if(ni===A.L)best=min(best,finish(u,tail(TB,nj),Z));else if(nj===B.L)best=min(best,finish(u,tail(TA,ni),Z));else{let at0=(Number(e)+w)*q;for(let a=0;a<q;a++)next[at0+a]=min(next[at0+a],u[a])}}}
V=next}
function row(k){st.rows++;let c=center(k),c1=center(k+1n),M=mat(D);for(let d=-w;d<=w;d++){let i=c+BigInt(d),j=k-i;for(let t=0;t<2;t++){let e=i+BigInt(t===0)-c1;if(e< -W||e>W)continue;let X=at(t?B:A,t?j:i),a=(d+w)*q,b=(Number(e)+w)*q;for(let u=0;u<q;u++)for(let v=0;v<q;v++)M[a+u][b+v]=min(M[a+u][b+v],X[u][v])}}return M}
function first(pred){let a=0n,b=tot;while(a<b){let c=(a+b)>>1n;if(pred(c))b=c;else a=c+1n}return a}
let stop=first(k=>center(k)-W>=A.L||other(k)-W>=B.L),lo=first(k=>center(k)>=W&&other(k)>=W),hi=first(k=>center(k)+W>=A.L-1n||other(k)+W>=B.L-1n);if(hi>stop)hi=stop;
if(lo>stop)lo=stop;
try{
if(!compress||lo>=hi){for(let k=0n;k<stop;k++)explicit(k);return{distance:best,st}}
for(let k=0n;k<lo;k++)explicit(k);
let zlo=(lo+S-1n)/S,zhi=hi/S;
if(zlo>=zhi){for(let k=lo;k<hi;k++)explicit(k)}
else{
for(let k=lo;k<zlo*S;k++)explicit(k);
let F=1n;while(F<=BigInt(Math.max(p,r)+2*w+2))F*=2n;
let memo=new Map();
function block(a,k){let B0=1n<<BigInt(k),H=a/B0,mod=B0*F,key=[k,String(H%F)];
let ranges=[[A.n+R*a-W+1n,A.n+R*(a+B0)-1n+W+1n],[B.n+P*a-W+1n,B.n+P*(a+B0)-1n+W+1n]];
for(let [l,u] of ranges){ck(l>0n,"positive cluster");let x=((l+mod-1n)/mod)*mod;key.push(x<=u?val(x):"-");ck(x>u||x+mod>u,"one exception")}
let sig=key.join(":");if(memo.has(sig)){st.hits++;return memo.get(sig)}
st.nodes++;let Q=id(D);if(!k){for(let u=0n;u<S;u++)Q=prod(Q,row(a*S+u),st)}
else Q=prod(block(a,k-1),block(a+B0/2n,k-1),st);memo.set(sig,Q);return Q}
let a=zlo;while(a<zhi){let k=0;while(a%(1n<<BigInt(k+1))===0n&&a+(1n<<BigInt(k+1))<=zhi)k++;V=vm(V,block(a,k));a+=1n<<BigInt(k)}
for(let k=zhi*S;k<hi;k++)explicit(k);
}
for(let k=hi;k<stop;k++)explicit(k);
return{distance:best,st}
}catch(e){if(e.message==="cap")return{unknown:true,st};throw e}}
let seed=19781;const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
let graphs=0,admit=0;for(let z=0;z<180;z++){let q=2+z%4,E=[];for(let i=0;i<q;i++)for(let j=0;j<q;j++)for(let t=0;t<2;t++)if(rnd()<.15)E.push([i,j,t]);let C=acquire(q,E);ck(!!C===cycleCheck(q,E),"cycle criterion");if(C){ck(verify(q,E,C));admit++}graphs++}
let random={tests:0,finite:0,infinite:0,slopes:{}};
function modes(p,r){let q=p+r,word=[...Array(r).fill(0),...Array(p).fill(1)],H=[0];for(let t of word.slice(0,-1))H.push(H.at(-1)+(t?r:-p));return{q,H,word}}
for(let z=0;z<100;z++){let [p,r]=[[1,2],[2,1],[3,2],[2,3],[1,1]][z%5],{q,H}=modes(p,r),m=1+z%6,L=2**m,gen=t=>Array.from({length:m+1},()=>mat(q,(i,j)=>H[j]-H[i]===(t?r:-p)&&rnd()<.82?BigInt(1+Math.floor(rnd()*8)):null)),tail=()=>Array.from({length:m+1},()=>mat(q,()=>rnd()<.78?BigInt(1+Math.floor(rnd()*7)):null));
let a=BigInt(Math.floor(rnd()*L)),b=BigInt(Math.floor(rnd()*L)),A=stream(m,a,gen(0)),B=stream(m,b,gen(1)),TA=stream(m,a,tail()),TB=stream(m,b,tail()),Z=Array.from({length:q},()=>rnd()<.9?1n:null),E=edges(A,B),C=acquire(q,E);ck(C&&verify(q,E,C),"acquire");let G=grid(A,B,TA,TB,Z),F=strip(A,B,TA,TB,Z,C),X=strip(A,B,TA,TB,Z,C,false);ck(F.distance===G.distance&&X.distance===G.distance,"grid equality");random.tests++;random[G.distance===null?"infinite":"finite"]++;let k=C.p+"/"+C.r;random.slopes[k]=(random.slopes[k]||0)+1}
let large=[];for(let m of [12,20,32,48,64]){let p=2,r=1,{q,H}=modes(p,r),a=(1n<<BigInt(m-1))-17n,b=37n,gen=t=>Array.from({length:m+1},(_,k)=>mat(q,(i,j)=>H[j]-H[i]===(t?r:-p)?BigInt(k%4+1):null)),tail=()=>Array.from({length:m+1},(_,k)=>mat(q,(i,j)=>i===j?BigInt(k%3+1):null)),A=stream(m,a,gen(0)),B=stream(m,b,gen(1)),TA=stream(m,a,tail()),TB=stream(m,b,tail()),Z=Array(q).fill(1n),C=acquire(q,edges(A,B)),F=strip(A,B,TA,TB,Z,C);ck(F.distance!==null);large.push({m,p:C.p,r:C.r,w:C.w,distance:String(F.distance),...F.st})}
// Counterexample to guessed strips: A* then B*, true accepting path requires huge drift.
{let m=4,q=2,A=stream(m,0n,Array.from({length:m+1},()=>mat(q,(i,j)=>i===0&&j===0?1n:null))),B=stream(m,0n,Array.from({length:m+1},()=>mat(q,(i,j)=>j===1?1n:null))),Z=[null,1n];ck(acquire(q,edges(A,B))===null);ck(grid(A,B,A,B,Z).distance!==null);ck(strip(A,B,A,B,Z,{p:1,r:1,w:1}).distance===null)}
// Native U_h: no explicit lag in control; only atomic progress + actual mode graph.
const f=s=>"1".repeat(s.length)+"0"+s,b=n=>n.toString(2),key=r=>r.join(",");
function catalogue(q){let states=[],map=new Map();for(let fl=0;fl<4;fl++)for(let a=0;a<5;a++){if(a>0&&(fl&(1<<Math.floor((a-1)/2))))continue;map.set([fl,a].join(","),states.length);states.push([fl,a])}
let code=(fl,a,i)=>3+q*map.get([fl,a].join(","))+i;
let setup=[[0,1,0,0,1,1,1,1],[0,2,0,0,2,1,1,1],[0,0,0,2,0,0,0,0],[2,1,1,2,1,1,0,0],[2,2,1,2,2,1,0,0],[2,0,0,code(0,0,0),0,0,1,1]],cat=[];
let sym=(fl,a,t)=>fl&(1<<t)?[0]:a===1+2*t?[0,1,2]:a===2+2*t?[0,1]:[1,2];
for(let [fl,a] of states)for(let x of sym(fl,a,0))for(let y of sym(fl,a,1))for(let i=0;i<q;i++){
let u=code(fl,a,i);for(let j=0;j<q;j++)cat.push({r:[u,x,y,code(fl,a,j),x,y,2,2],g:[fl,"S",i,j].join(",")});
if(fl===3){cat.push({r:[u,x,y,1,x,y,2,2],g:["Z",i].join(",")});continue}
for(let t=0;t<2;t++){if(fl&(1<<t)||a&&Math.floor((a-1)/2)!==t)continue;let s=t?y:x,k=-1,v=s,d=2,na=0,nf=fl;
if(a===0||a===1+2*t){if(s===2){k=0;v=1;d=1;na=1+2*t}else if(s===1){k=1;v=2;d=0;na=2+2*t}else if(a!==0&&s===0){k=4;nf=fl|(1<<t)}}else if(a===2+2*t){if(s===1){k=2;d=0;na=a}else if(s===0){k=3;d=1;na=0}}
if(k<0)continue;for(let j=0;j<q;j++){let dst=code(nf,na,j);cat.push({r:t?[u,x,y,dst,x,v,2,d]:[u,x,y,dst,v,y,d,2],g:[fl,t,k,i,j].join(",")})}}
}return{setup,cat}}
function build(q,G){let C=catalogue(q);return [...C.setup,...C.cat.filter(x=>G.has(x.g)).map(x=>x.r)]}
function encode(rows,x,t,N=0){let z=f(rows.map(r=>r.map(v=>f(b(v))).join("")).join(""))+f(x)+f(b(t));return z+"0".repeat(Math.max(0,N-z.length))}
function decode(w,h){let p=0;function get(s,j){let k=j;while(s[k]==="1")k++;if(s[k]!=="0"||2*k+1-j>s.length)throw Error("frame");return[s.slice(k+1,2*k+1-j),2*k+1-j]}let raw,x,t;[raw,p]=get(w,p);[x,p]=get(w,p);[t,p]=get(w,p);ck(/^[01]+$/.test(x)&&/^0*$/.test(w.slice(p))&&/^(0|1[01]*)$/.test(t));let T=BigInt("0b"+t);ck(T<=BigInt(w.length)**BigInt(h));let rows=[],j=0;while(j<raw.length){let a=[];for(let k=0;k<8;k++){let s;[s,j]=get(raw,j);ck(/^(0|1[01]*)$/.test(s));a.push(parseInt(s,2))}rows.push(a)}let n=0n;for(let i=0;i<x.length;i++)if(x[i]==="1")n|=1n<<BigInt(i);return{w,rows,x,n,m:x.length,T}}
function nativeAcquire(F,q){let C=catalogue(q),set=new Set(F.rows.map(key)),G=new Set();for(let e of C.cat)if(set.has(key(e.r)))G.add(e.g);let expect=new Set(build(q,G).map(key));if(expect.size!==set.size||[...set].some(x=>!expect.has(x)))return null;
let D=[];for(let fl=0;fl<4;fl++){let X=id(q);for(let i=0;i<q;i++)for(let j=0;j<q;j++)if(G.has([fl,"S",i,j].join(",")))X[i][j]=min(X[i][j],1n);for(let k=0;k<q;k++)for(let i=0;i<q;i++)for(let j=0;j<q;j++)X[i][j]=min(X[i][j],add(X[i][k],X[k][j]));D.push(X);
for(let i=0;i<q;i++){let ds=Array(q).fill(null),Q=[i];ds[i]=0n;for(let k=0;k<Q.length;k++)for(let j=0;j<q;j++)if(G.has([fl,"S",Q[k],j].join(","))&&ds[j]===null){ds[j]=ds[Q[k]]+1n;Q.push(j)}ck(ds.every((v,j)=>v===X[i][j]),"local BFS")}}
function mk(fl,t){let L=Array.from({length:5},(_,k)=>prod(D[fl],mat(q,(i,j)=>G.has([fl,t,k,i,j].join(","))?1n:null))),P=id(q),Q=id(q),M=[];for(let k=0;k<F.m;k++){M.push(prod(prod(prod(P,L[1]),Q),L[3]));P=prod(P,L[0]);Q=prod(Q,L[2])}M.push(prod(P,L[4]));return stream(F.m,t?0n:F.n,M)}
let Z=Array.from({length:q},(_,i)=>D[3][i].reduce((a,b,j)=>G.has(["Z",j].join(","))?min(a,add(b,1n)):a,null));return {A:mk(0,0),B:mk(0,1),TA:mk(2,0),TB:mk(1,1),Z}}
function replay(F,cap){let idx=new Map();for(let r of F.rows){let k=r.slice(0,3).join(",");if(!idx.has(k))idx.set(k,[]);idx.get(k).push(r)}let start=[0,0,0,F.n,0n,0,0],Q=[start],seen=new Set([start.slice(0,6).join(",")]);for(let k=0;k<Q.length;k++){if(k>=cap)return{unknown:true,steps:k};let [s,p1,p2,v1,v2,l,d]=Q[k];if(s===1)return{distance:BigInt(d),steps:k+1};let rd=(p,v,L)=>p<0||p>=L?0:((v>>BigInt(p))&1n)?2:1;for(let r of idx.get([s,rd(p1,v1,F.m),rd(p2,v2,l)].join(","))||[]){let a=v1,c=v2,L=l;if(p1>=0&&p1<F.m){let bit=1n<<BigInt(p1);a=r[4]===2?a|bit:a&~bit}if(p2===L&&r[5])L++;if(p2>=0&&p2<L){let bit=1n<<BigInt(p2);c=r[5]===2?c|bit:c&~bit}let z=[r[3],p1+[-1,1,0][r[6]],p2+[-1,1,0][r[7]],a,c,L,d+1],key=z.slice(0,6).join(",");if(!seen.has(key)){seen.add(key);Q.push(z)}}}return{distance:null,steps:Q.length}}
function makeGroups(p,r){let {q,word}=modes(p,r),G=new Set();for(let i=0;i<q;i++){let t=word[i];for(let k=0;k<5;k++)G.add([0,t,k,i,k>=3?(i+1)%q:i].join(","));for(let fl of [1,2])for(let k=0;k<5;k++)G.add([fl,fl===1?1:0,k,i,i].join(","));G.add(["Z",i].join(","))}return{q,G}}
function H(m,n){let pc=0n,x=n;while(x){pc+=x&1n;x>>=1n}return 4n*((1n<<BigInt(m))-1n-n)-BigInt(m)+2n*pc+1n}
const label=(d,t)=>d===null||d>t?"NO":"YES";let records=[],mutants=0,summary={A:{YES:0,NO:0,UNKNOWN:0},B:{YES:0,NO:0,UNKNOWN:0},C:{YES:0,NO:0,UNKNOWN:0},I:{YES:0,NO:0,UNKNOWN:0}};
for(let [m,p,r] of [[1,1,2],[2,2,1],[3,3,2],[4,2,3],[6,2,1],[8,1,2],[12,2,1],[16,3,2],[24,2,1],[32,1,2],[48,2,1]]){
let {q,G}=makeGroups(p,r),rows=build(q,G),n=(1n<<BigInt(m-1))-1n,x=n.toString(2).padStart(m,"0").split("").reverse().join(""),d=2n*BigInt(m)+3n+H(m,n)+H(m,0n),N=encode(rows,x,d).length;while(BigInt(N)**4n<d)N++;
for(let t of [d-1n,d]){let word=encode(rows,x,t,N),F=decode(word,4),J=decode(word,4),K=decode(word,4),I=decode(word,4);ck(F.w===J.w&&J.w===K.w&&K.w===I.w);
let a=nativeAcquire(F,q),z=nativeAcquire(I,q);ck(a&&z);for(let k=0;k<=m;k++)ck(eq(a.A.M[k],z.A.M[k])&&eq(a.B.M[k],z.B.M[k])&&eq(a.TA.M[k],z.TA.M[k])&&eq(a.TB.M[k],z.TB.M[k]));
let E=edges(a.A,a.B),c=acquire(q,E),c2=acquire(q,edges(z.A,z.B));ck(c&&c2&&verify(q,E,c)&&verify(q,edges(z.A,z.B),c2)&&c.p===c2.p&&c.r===c2.r&&c.w===c2.w);ck(cycleCheck(q,E));
let ar=grid(a.A,a.B,a.TA,a.TB,a.Z,4096),setup=BigInt(2*m+2),A=ar.unknown?"UNKNOWN":label(add(setup,ar.distance),t);
let B=label(2n*BigInt(J.m)+3n+H(J.m,J.n)+H(J.m,0n),t)==="NO"?"NO":"UNKNOWN";
let ref=replay(K,20000),C=ref.unknown?"UNKNOWN":label(ref.distance,t);if(!ref.unknown)ck(ref.distance===d,"native ref");
let ir=strip(z.A,z.B,z.TA,z.TB,z.Z,c2),distance=add(setup,ir.distance),Il=label(distance,t);ck(distance===d,"native formula");
for(let [k,v] of Object.entries({A,B,C,I:Il})){ck(v==="UNKNOWN"||v===label(d,t));summary[k][v]++}
records.push({m,N,n:String(n),deadline:String(t),distance:String(distance),p:c.p,r:c.r,w:c.w,M:c.M,A,B,C,I:Il,refSteps:ref.steps,...ir.st})
}
let mut=rows.slice();mut.splice(6,1);ck(nativeAcquire(decode(encode(mut,x,0n),4),q)===null,"missing rule");mutants++;
}
return{checks,graphs,admit,random,large,nativePairs:11,records,summary,mutants,scope:"sequential copied sources; separate explicit-grid cap 4096 cells and native replay cap 20000 configurations, not equivalent bit time; q supplied to native recognizer, exact template match; source lower-bound lane uses compulsory physical count, no exclusive synergy asserted"};
}
console.log(JSON.stringify(run(),null,2));
