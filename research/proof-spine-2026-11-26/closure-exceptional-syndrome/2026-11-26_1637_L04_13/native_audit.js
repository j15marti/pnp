function run(){

let checks=0;const ck=(v,s="")=>{checks++;if(!v)throw Error("assert "+checks+" "+s)};
const mn=(a,b)=>a===null?b:b===null?a:a<b?a:b,ad=(a,b)=>a===null||b===null?null:a+b;
const mat=(q,f=()=>null)=>Array.from({length:q},(_,i)=>Array.from({length:q},(_,j)=>f(i,j)));
const id=q=>mat(q,(i,j)=>i===j?0n:null),vm=(v,A)=>A[0].map((_,j)=>v.reduce((z,x,i)=>mn(z,ad(x,A[i][j])),null)),merge=(a,b)=>a.map((x,i)=>mn(x,b[i]));
function prod(A,B,st){if(st)st.products++;let q=A.length,P=mat(q);for(let i=0;i<q;i++)for(let k=0;k<q;k++)if(A[i][k]!==null)for(let j=0;j<q;j++)if(B[k][j]!==null)P[i][j]=mn(P[i][j],A[i][k]+B[k][j]);return P}
function val(x){if(x<=0n)throw Error("valuation");let k=0;while((x&1n)===0n){x>>=1n;k++}return k}
function stream(m,n,M){return{m,n,M,L:(1n<<BigInt(m))-n,q:M[0].length}}
function at(F,i){if(i<0n||i>=F.L)throw Error("stream index");return i===F.L-1n?F.M[F.m]:F.M[val(F.n+i+1n)]}
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

 const E=[[0,1,0],[1,2,0],[2,0,1],[0,3,0],[3,4,0],[4,3,1],[3,5,1],[5,6,0],[6,7,1],[7,5,1]];
 function pref(m,w,x){let z=0n;for(let r=0;r<m;r++)z+=w[r]*((x>>BigInt(r))-(x>>BigInt(r+1)));return z}
 function coefficients(m,w){return Array.from({length:m},(_,j)=>pref(m,w,1n<<BigInt(j)))}
 function direct(m,W,u){let L=(1n<<BigInt(m))-1n,t=L-1n-3n*u,i=0n,j=0n,c=0n;const step=e=>{let a=E[e][2]?++j:++i;c+=W[e][val(a)]};for(let a=0n;a<u;a++){step(0);step(1);step(2)}step(3);for(let a=0n;a<t;a++){step(4);step(5)}step(6);for(let a=0n;a<u;a++){step(7);step(8);step(9)}ck(i===L&&j===L,"endpoint");return c}
 function construct(m,W){let L=(1n<<BigInt(m))-1n,U=(L-1n)/3n;let A=Array.from({length:m},(_,k)=>W[k===0?0:1][k]),B=Array.from({length:m},(_,k)=>W[k===0?9:8][k]);const plus=(a,b)=>a.map((x,k)=>x+b[k]),neg=a=>a.map(x=>-x);let forms=[[2,0n,A],[1,0n,plus(W[2],neg(W[5]))],[-1,L,plus(W[4],neg(W[7]))],[2,1n,neg(W[4])],[-2,L-1n,W[5]],[-2,L,neg(B)],[-1,U,Array(m).fill(0n)]];let constant=W[3][0]+W[6][0]+pref(m,W[7],L)+pref(m,B,L);return{forms,constant,U}}
 function arithmetic(m,W,u){let {forms,constant}=construct(m,W);return constant+forms.reduce((a,[b,c,w])=>a+pref(m,w,BigInt(b)*u+c),0n)}
 function digit(m,W){let {forms,constant,U}=construct(m,W),co=forms.map(f=>coefficients(m,f[2]));let M=new Map([["0,0,0,0,0,0,0",{c:Array(7).fill(0),cost:0n,u:0n}]]),peak=1,trans=0;for(let k=0;k<m;k++){let N=new Map();for(let v of M.values())for(let d=0;d<2;d++){trans++;let cost=v.cost,c=forms.map(([a,b],i)=>{let s=v.c[i]+a*d+Number((b>>BigInt(k))&1n),bit=(s%2+2)%2;cost+=BigInt(bit)*co[i][k];return (s-bit)/2});let key=c.join(","),u=v.u+(BigInt(d)<<BigInt(k)),old=N.get(key);if(!old||cost<old.cost)N.set(key,{c,cost,u})}M=N;peak=Math.max(peak,M.size)}let z=M.get("0,0,0,0,0,0,0");ck(z&&z.u<=U);return{cost:z.cost+constant,u:z.u,peak,trans}}
 function brute(m,W,kind){let U=construct(m,W).U,best=null,at=0n;for(let u=0n;u<=U;u++){let c=kind==="word"?direct(m,W,u):arithmetic(m,W,u);if(best===null||c<best){best=c;at=u}}return{cost:best,u:at}}

function groups(){let q=9,G=new Set();for(let [i,j,t] of E)for(let k=0;k<5;k++)G.add([0,t,k,i,k>=3?j:i].join(","));for(let k=0;k<5;k++)G.add([1,1,k,6,k>=3?8:6].join(","));G.add("Z,8");return {q,G}}
function getW(a,m,P){let W=E.map(([i,j,t])=>Array.from({length:m},(_,k)=>(t?a.B:a.A).M[k][i][j]??P));let allowed=new Set(E.map(([i,j,t])=>[i,j,t].join(",")));for(let [t,F] of [[0,a.A],[1,a.B]])for(let k=0;k<m;k++)for(let i=0;i<F.q;i++)for(let j=0;j<F.q;j++)if(F.M[k][i][j]!==null&&!allowed.has([i,j,t].join(",")))return null;
 if(a.A.M[m][5][6]===null||a.TB.M[m][6][8]===null||a.Z[8]===null)return null;
 for(let i=0;i<a.A.q;i++){if(i!==8&&a.Z[i]!==null)return null;for(let j=0;j<a.A.q;j++)for(let k=0;k<=m;k++){if(a.TA.M[k][i][j]!==null)return null;if(a.TB.M[k][i][j]!==null&&(i!==6||j!==8))return null}}
 for(let i=0;i<a.A.q;i++)if(i!==5&&a.A.M[m][i][6]!==null)return null;
 return{W,tail:a.A.M[m][5][6]+a.TB.M[m][6][8]+a.Z[8]}}
function H(m){return 4n*((1n<<BigInt(m))-1n)-BigInt(m)+1n}
let nativeTests=[],mutants=0;
for(let m of [2,4,6,8,12,16,24,32,48]){let {q,G}=groups(),rows=build(q,G),x="0".repeat(m),distance=2n*BigInt(m)+3n+2n*H(m),N=encode(rows,x,distance).length;
 // No loop over the expanded clock. The framing here already dominates fourth root through m48.
 ck(BigInt(N)**4n>=distance,"clock");
 for(let t of [distance-1n,distance]){let word=encode(rows,x,t,N),F=decode(word,4),J=decode(word,4),K=decode(word,4);ck(F.w===J.w&&J.w===K.w);let a=nativeAcquire(F,q),b=nativeAcquire(J,q);ck(a&&b);let P=t+1n,aa=getW(a,m,P),bb=getW(b,m,P);ck(aa&&bb);ck(aa.W.every((row,i)=>row.every((v,j)=>v===bb.W[i][j]))&&aa.tail===bb.tail);
 let d=digit(m,aa.W),cost=d.cost+aa.tail+BigInt(2*m+2);ck(cost===distance,"native distance");
 let ar=m<=6?brute(m,aa.W,"word"):null,br=m<=8?brute(m,bb.W,"arithmetic"):null,ref=replay(K,10000);if(ar)ck(ar.cost===d.cost);if(br)ck(br.cost===d.cost);if(!ref.unknown)ck(ref.distance===distance);
 nativeTests.push({m,N,t:String(t),label:cost<=t?"YES":"NO",cost:String(cost),u:String(d.u),peak:d.peak,trans:d.trans,A:ar===null?"UNKNOWN":ar.cost+aa.tail+BigInt(2*m+2)<=t?"YES":"NO",B:br===null?"UNKNOWN":br.cost+bb.tail+BigInt(2*m+2)<=t?"YES":"NO",C:ref.unknown?"UNKNOWN":ref.distance!==null&&ref.distance<=t?"YES":"NO",refSteps:ref.steps})}
 let mut=rows.slice();mut.splice(6,1);ck(nativeAcquire(decode(encode(mut,x,0n),4),q)===null);mutants++}
return{checks,nativeTests,mutants,scope:"native U4 exact original rules, q supplied, zero offsets, fixed three-cycle graph; A direct expansion only m<=6, B arithmetic enumeration only m<=8, C native BFS cap10000; distinct caps, no bit-equivalence; no general native flat SCC recognizer executed"}
}
console.log(JSON.stringify(run(),null,2));
