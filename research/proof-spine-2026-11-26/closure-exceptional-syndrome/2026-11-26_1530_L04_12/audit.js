function run(){
let checks=0;const ck=(v,s="")=>{checks++;if(!v)throw Error("assert "+checks+" "+s)};
const mn=(a,b)=>a===null?b:b===null?a:a<b?a:b,ad=(a,b)=>a===null||b===null?null:a+b;
const mat=(q,f=()=>null)=>Array.from({length:q},(_,i)=>Array.from({length:q},(_,j)=>f(i,j)));
const id=q=>mat(q,(i,j)=>i===j?0n:null),vm=(v,A)=>A[0].map((_,j)=>v.reduce((z,x,i)=>mn(z,ad(x,A[i][j])),null)),merge=(a,b)=>a.map((x,i)=>mn(x,b[i]));
function prod(A,B,st){if(st)st.products++;let q=A.length,P=mat(q);for(let i=0;i<q;i++)for(let k=0;k<q;k++)if(A[i][k]!==null)for(let j=0;j<q;j++)if(B[k][j]!==null)P[i][j]=mn(P[i][j],A[i][k]+B[k][j]);return P}
function val(x){if(x<=0n)throw Error("valuation");let k=0;while((x&1n)===0n){x>>=1n;k++}return k}
function stream(m,n,M){return{m,n,M,L:(1n<<BigInt(m))-n,q:M[0].length}}
function at(F,i){if(i<0n||i>=F.L)throw Error("stream index");return i===F.L-1n?F.M[F.m]:F.M[val(F.n+i+1n)]}
function graph(A,B,normal=true){let E=[],q=A.q;for(let [t,F] of [[0,A],[1,B]])for(let u=0;u<q;u++)for(let v=0;v<q;v++)if(F.M.slice(0,normal?F.m:F.m+1).some(M=>M[u][v]!==null))E.push([u,v,t]);return E}
function scc(q,E,start=null){let R=mat(q,(i,j)=>i===j);for(let [u,v] of E)R[u][v]=true;for(let k=0;k<q;k++)for(let i=0;i<q;i++)if(R[i][k])for(let j=0;j<q;j++)R[i][j]||=R[k][j];let groups=[],owner=Array(q).fill(-1);for(let i=0;i<q;i++)if(owner[i]===-1&&(start===null||R[start][i])){let a=[];for(let j=0;j<q;j++)if(R[i][j]&&R[j][i]){owner[j]=groups.length;a.push(j)}groups.push(a)}return{groups,owner,R}}
function pot(q,E,S){let F=E.filter(([u,v])=>S.includes(u)&&S.includes(v));for(let p=1;p<=q;p++)for(let r=1;r<=q;r++){let H=Array(q).fill(null);H[S[0]]=0;for(let k=0;k<S.length;k++)for(let [u,v,t] of F)if(H[u]!==null&&H[v]===null)H[v]=H[u]+(t?r:-p);if(S.every(u=>H[u]!==null)&&F.every(([u,v,t])=>H[v]-H[u]===(t?r:-p)))return{S,H,p,r}}return null}
function tailCap(F){let E=graph(F,F,false).filter(e=>e[2]===0),q=F.q,C=scc(q,E);if(C.groups.some(S=>S.length>1)||E.some(([u,v])=>u===v))return null;return q-1}
function acquire(A,B,TA,TB){let E=graph(A,B),C=scc(A.q,E,0),P=C.groups.map(S=>pot(A.q,E,S)),a=tailCap(TA),b=tailCap(TB);if(P.length>2||P.some(x=>!x)||a===null||b===null)return null;if(P.length===2&&P[0].p*P[1].r===P[1].p*P[0].r)return null;return{...C,E,P,a,b}}
function point(A,B,C,sa,sb,I,J,u,v,st,compress=true){
 if(I<0n||J<0n||sa+I>=A.L||sb+J>=B.L)return null;
 let {p,r,H,S}=C,q=S.length,ui=S.indexOf(u),vi=S.indexOf(v);
 if(ui<0||vi<0||BigInt(r)*J-BigInt(p)*I!==BigInt(H[v]-H[u]))return null;
 let P=BigInt(p),R=BigInt(r),s=p+r,T=BigInt(s),K=I+J;if(!K)return u===v?0n:null;
 let w=Math.max(1,Math.ceil(Math.max(...S.map(x=>Math.abs(H[x]-H[u])))/s)),W=BigInt(w),c=k=>R*k/T,b=k=>k-c(k);
 function coords(k,x){let n=R*k-BigInt(H[x]-H[u]);if(n%T!==0n)return null;let i=n/T,j=k-i;return i<0n||j<0n||i>I||j>J?null:[i,j]}
 function row(k){st.rows++;let M=mat(q);for(let x=0;x<q;x++){let z=coords(k,S[x]);if(!z)continue;let [i,j]=z;for(let t=0;t<2;t++){if(t?j>=J:i>=I)continue;let X=at(t?B:A,t?sb+j:sa+i);for(let y=0;y<q;y++){let d=coords(k+1n,S[y]);if(d&&d[0]===i+BigInt(t===0)&&d[1]===j+BigInt(t===1))M[x][y]=mn(M[x][y],X[S[x]][S[y]])}}}return M}
 function first(f){let a=0n,b=K;while(a<b){let k=(a+b)>>1n;if(f(k))b=k;else a=k+1n}return a}
 let lo=first(k=>c(k)>=W&&b(k)>=W),hi=first(k=>c(k)+W>=I||b(k)+W>=J);
 let V=id(q)[ui];function explicit(a,b){for(let k=a;k<b;k++){st.explicit++;V=vm(V,row(k))}}
 if(!compress||lo>=hi){explicit(0n,K);return V[vi]}
 explicit(0n,lo);let l=(lo+T-1n)/T,h=hi/T;
 if(l>=h)explicit(lo,hi);else{
 explicit(lo,l*T);let F=1n;while(F<=BigInt(Math.max(p,r)+2*w+2))F*=2n;let memo=new Map();
 function block(a,k){let B0=1n<<BigInt(k),mod=F*B0,key=[k,String((a/B0)%F)];
 let ranges=[[A.n+sa+R*a-W+1n,A.n+sa+R*(a+B0)+W],[B.n+sb+P*a-W+1n,B.n+sb+P*(a+B0)+W]];
 for(let [x,y] of ranges){ck(x>0n);let z=((x+mod-1n)/mod)*mod;key.push(z<=y?val(z):"-");ck(z>y||z+mod>y)}
 let sig=key.join(":");if(memo.has(sig)){st.hits++;return memo.get(sig)}
 st.nodes++;let Q=id(q);if(k===0){for(let z=0n;z<T;z++)Q=prod(Q,row(a*T+z),st)}else Q=prod(block(a,k-1),block(a+B0/2n,k-1),st);memo.set(sig,Q);return Q}
 let a=l;while(a<h){let k=0;while(a%(1n<<BigInt(k+1))===0n&&a+(1n<<BigInt(k+1))<=h)k++;V=vm(V,block(a,k));a+=1n<<BigInt(k)}
 explicit(h*T,hi)}
 explicit(hi,K);return V[vi]
}
function stats(){return{rows:0,nodes:0,hits:0,products:0,explicit:0,interfaces:0,integral:0,pointQueries:0}}
function solve(A,B,TA,TB,Z,compressed=true){
 let C=acquire(A,B,TA,TB),st=stats();if(!C)return{unknown:true,st};let {P,owner,E}=C,q=A.q,cache=new Map();
 function pt(sa,sb,I,J,u,v){let key=[sa,sb,I,J,u,v].join(":");if(cache.has(key))return cache.get(key);st.pointQueries++;let d=point(A,B,P[owner[u]],sa,sb,I,J,u,v,st,compressed);cache.set(key,d);return d}
 function prefix(I,J,z){if(owner[z]<0)return null;if(owner[z]===owner[0])return pt(0n,0n,I,J,0,z);let U=P[owner[0]],V=P[owner[z]],best=null;
 for(let [u,v,t] of E){if(owner[u]!==owner[0]||owner[v]!==owner[z])continue;st.interfaces++;let a=BigInt(t===0),b=BigInt(t===1),p=BigInt(U.p),r=BigInt(U.r),p2=BigInt(V.p),r2=BigInt(V.r),d1=BigInt(U.H[u]-U.H[0]),d2=r2*(J-b)-p2*(I-a)-BigInt(V.H[z]-V.H[v]),den=p*r2-p2*r,num=r*d2-r2*d1;if(num%den)continue;let x=num/den;if((d1+p*x)%r)continue;let y=(d1+p*x)/r;if(x<0n||y<0n||x+a>I||y+b>J)continue;st.integral++;let edge=at(t?B:A,t?y:x)[u][v];if(edge===null)continue;let l=pt(0n,0n,x,y,0,u),h=pt(x+a,y+b,I-x-a,J-y-b,v,z);best=mn(best,ad(ad(l,edge),h))}
 return best}
 let best=null;for(let t=0;t<2;t++){let other=t?A:B,tail=t?TA:TB,cap=t?C.a:C.b;for(let l=1;l<=cap&&BigInt(l)<=other.L;l++){let I=t?A.L-BigInt(l):A.L-1n,J=t?B.L-1n:B.L-BigInt(l),M=(t?B:A).M[A.m],V=Z.slice();for(let k=other.L-1n;k>=other.L-BigInt(l);k--){let X=at(tail,k);V=X.map(row=>row.reduce((z,c,v)=>mn(z,ad(c,V[v])),null))}
 for(let u=0;u<q;u++){let suffix=M[u].reduce((z,c,v)=>mn(z,ad(c,V[v])),null);if(suffix===null)continue;best=mn(best,ad(prefix(I,J,u),suffix))}
 }}return{distance:best,st,C}
}
function grid(A,B,TA,TB,Z,cap=1000000){let I=Number(A.L),J=Number(B.L),q=A.q;if(!Number.isSafeInteger(I)||!Number.isSafeInteger(J)||(I+1)*(J+1)>cap)return{unknown:true};let P=Array.from({length:I+1},()=>Array.from({length:J+1},()=>Array(q).fill(null)));P[0][0][0]=0n;for(let i=0;i<=I;i++)for(let j=0;j<=J;j++){let v=P[i][j];if(i<I)P[i+1][j]=merge(P[i+1][j],vm(v,at(j===J?TA:A,BigInt(i))));if(j<J)P[i][j+1]=merge(P[i][j+1],vm(v,at(i===I?TB:B,BigInt(j))))}return{distance:P[I][J].reduce((z,c,u)=>mn(z,ad(c,Z[u])),null),cells:(I+1)*(J+1)}}
function independent(A,B,TA,TB,Z,cap=1000000){let q=A.q,Q=[[0n,0n,0]],D=new Map([["0,0,0",0n]]),best=null;for(let k=0;k<Q.length;k++){if(k>=cap)return{unknown:true};let [i,j,u]=Q[k],x=D.get([i,j,u].join(","));if(i===A.L&&j===B.L){best=mn(best,ad(x,Z[u]));continue}for(let t=0;t<2;t++){if(t?j===B.L:i===A.L)continue;let F=t?(i===A.L?TB:B):(j===B.L?TA:A),X=at(F,t?j:i),a=i+BigInt(t===0),b=j+BigInt(t===1);for(let v=0;v<q;v++)if(X[u][v]!==null){let key=[a,b,v].join(","),d=x+X[u][v];if(!D.has(key)){Q.push([a,b,v]);D.set(key,d)}else if(d<D.get(key))D.set(key,d)}}}return{distance:best,states:Q.length}}
let seed=218441;const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
function modeGraph(p1,r1,p2,r2){let words=[[...Array(r1).fill(0),...Array(p1).fill(1)],[...Array(r2).fill(0),...Array(p2).fill(1)]],q=words[0].length+words[1].length+4,E=[],starts=[0,words[0].length];for(let z=0;z<2;z++){let W=words[z],s=starts[z];for(let i=0;i<W.length;i++)E.push([s+i,s+(i+1)%W.length,W[i]])}E.push([0,starts[1],0]);return{q,E,starts}}
function abstract(m,n1,n2,rand=true,p1=1,r1=2,p2=2,r2=1){let {q,E}=modeGraph(p1,r1,p2,r2);let build=t=>Array.from({length:m+1},(_,k)=>mat(q,(u,v)=>E.some(e=>e[0]===u&&e[1]===v&&e[2]===t)&&(k===0||!rand||rnd()<.8)?BigInt(rand?1+Math.floor(rnd()*5):1):null));let tail=()=>Array.from({length:m+1},()=>mat(q,(u,v)=>v===u+1&&(!rand||rnd()<.9)?BigInt(rand?1+Math.floor(rnd()*3):1):null));return[stream(m,n1,build(0)),stream(m,n2,build(1)),stream(m,n1,tail()),stream(m,n2,tail()),Array.from({length:q},()=>!rand||rnd()<.9?1n:null)]}
let random={tests:0,finite:0,infinite:0,integral:0,maxCandidates:0};
for(let z=0;z<100;z++){let m=2+z%5,L=2**m,pairs=[[1,2,2,1],[1,1,2,3],[3,2,1,2]][z%3],args=abstract(m,BigInt(Math.floor(rnd()*L)),BigInt(Math.floor(rnd()*L)),true,...pairs),a=grid(...args),b=independent(...args),c=solve(...args),d=solve(...args,false);ck(!c.unknown&&!d.unknown&&a.distance===b.distance&&b.distance===c.distance&&c.distance===d.distance,"random equality");random.tests++;random[a.distance===null?"infinite":"finite"]++;random.integral+=c.st.integral;random.maxCandidates=Math.max(random.maxCandidates,c.st.integral)}
let large=[];for(let m of [12,20,32,48,64]){let args=abstract(m,0n,0n,false),C=solve(...args);ck(C.distance===2n*(1n<<BigInt(m))+1n,"large");large.push({m,distance:String(C.distance),...C.st})}
let obstruction=[];for(let m of [4,8,16,32,48,64]){let L=(1n<<BigInt(m))-1n,max=(L-1n)/3n;for(let u of [0n,max/2n,max]){let v=u,t=L-1n-3n*u;ck(t>=0n&&2n*u+t+v+1n===L&&u+t+2n*v+1n===L)}obstruction.push({m,target:String(L),distinctFirstInterfaces:String(max+1n)})}
return{checks,random,large,obstruction,scope:"abstract weighted counter macro inputs, four exact evaluations; no native encoding experiment in this audit; sequential methods; large cases use deterministic cycle construction and unit costs"}
}
console.log(JSON.stringify(run(),null,2));
