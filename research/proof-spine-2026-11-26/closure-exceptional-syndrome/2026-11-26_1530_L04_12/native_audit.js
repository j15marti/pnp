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


const min=mn,add=ad;
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

function groups(){let {q,E}=modeGraph(1,2,2,1),G=new Set();for(let [i,j,t] of E)for(let k=0;k<5;k++)G.add([0,t,k,i,k>=3?j:i].join(","));for(let i=0;i<q;i++){for(let fl of [1,2])for(let k=0;k<5;k++)if(i+1<q)G.add([fl,fl===1?1:0,k,i,k>=3?i+1:i].join(","));G.add(["Z",i].join(","))}return{q,G}}
function H(m,n){let pc=0n,x=n;while(x){pc+=x&1n;x>>=1n}return 4n*((1n<<BigInt(m))-1n-n)-BigInt(m)+2n*pc+1n}
const label=(d,t)=>d===null||d>t?"NO":"YES";
let records=[],mutants=0,summary={A:{YES:0,NO:0,UNKNOWN:0},B:{YES:0,NO:0,UNKNOWN:0},C:{YES:0,NO:0,UNKNOWN:0},I:{YES:0,NO:0,UNKNOWN:0}};
for(let m of [2,4,6,8,12,16,24,32,48]){
 let {q,G}=groups(),rows=build(q,G),n=0n,x="0".repeat(m),d=2n*BigInt(m)+3n+H(m,n)+H(m,0n),N=encode(rows,x,d).length;while(BigInt(N)**4n<d)N++;
 for(let t of [d-1n,d]){let word=encode(rows,x,t,N),F=decode(word,4),J=decode(word,4),K=decode(word,4),I=decode(word,4);ck(F.w===J.w&&J.w===K.w&&K.w===I.w);
 let a=nativeAcquire(F,q),b=nativeAcquire(J,q),z=nativeAcquire(I,q);ck(a&&b&&z);
 const pack=o=>[o.A,o.B,o.TA,o.TB,o.Z],str=o=>JSON.stringify(pack(o),(k,v)=>typeof v==="bigint"?String(v):v);
 ck(str(a)===str(b)&&str(a)===str(z));
 let cap=10000,setup=BigInt(2*m+2),g=grid(...pack(a),cap),A=g.unknown?"UNKNOWN":label(add(setup,g.distance),t);
 let B=label(2n*BigInt(J.m)+3n+H(J.m,J.n)+H(J.m,0n),t)==="NO"?"NO":"UNKNOWN";
 let ref=replay(K,cap),C=ref.unknown?"UNKNOWN":label(ref.distance,t);if(!ref.unknown)ck(ref.distance===d,"native ref");
 let ir=solve(...pack(z)),distance=add(setup,ir.distance),Il=label(distance,t);ck(distance===d,"native formula");
 for(let [k,v] of Object.entries({A,B,C,I:Il})){ck(v==="UNKNOWN"||v===label(d,t));summary[k][v]++}
 records.push({m,N,deadline:String(t),distance:String(distance),A,B,C,I:Il,refSteps:ref.steps,...ir.st})
 }
 let mut=rows.slice();mut.splice(6,1);ck(nativeAcquire(decode(encode(mut,x,0n),4),q)===null);mutants++;
}
return {checks,records,summary,mutants,scope:"Native explicit U_4 source. Four sequential copies; byte equality and exact acquired matrix equality. A and C cap 10000 records (different record units, not equal bit work). B counts physical compulsory work only. q supplied to recognizer. Two distinct slopes and acyclic tail derived from actual matrices."};

}
console.log(JSON.stringify(run(),null,2));
