function run(){
let checks=0;const ck=(x,s="")=>{checks++;if(!x)throw Error("check "+checks+" "+s)};
const min=(a,b)=>a===null?b:b===null?a:a<b?a:b,add=(a,b)=>a===null||b===null?null:a+b;
const mat=(q,fn=()=>null)=>Array.from({length:q},(_,i)=>Array.from({length:q},(_,j)=>fn(i,j))),id=q=>mat(q,(i,j)=>i===j?0n:null),eq=(A,B)=>A.every((r,i)=>r.every((x,j)=>x===B[i][j]));
function prod(A,B,st){if(st)st.products++;let q=A.length;return mat(q,(i,j)=>{let z=null;for(let k=0;k<q;k++)z=min(z,add(A[i][k],B[k][j]));return z})}
function vm(v,A){return A[0].map((_,j)=>v.reduce((a,x,i)=>min(a,add(x,A[i][j])),null))}
function union(v,u){return v.map((x,i)=>min(x,u[i]))}
const val=n=>{if(n<=0n)throw Error("valuation guard");let r=0;while((n&1n)===0n){r++;n>>=1n}return r};
const abs=n=>n<0n?-n:n;
function macroSet(m,n,M){let L=(1n<<BigInt(m))-n,q=M[0].length,S=[id(q)];for(let k=0;k<m;k++)S.push(prod(prod(S[k],M[k]),S[k]));return{m,n,L,M,q,S}}
function at(F,i){ck(i>=0n&&i<F.L,"macro index");return i===F.L-1n?F.M[F.m]:F.M[val(F.n+i+1n)]}
function suffix(F,i){if(i===F.L)return id(F.q);let n=F.n+i;function s(k,n){if(k===0)return id(F.q);let d=1n<<BigInt(k-1);return n>=d?s(k-1,n-d):prod(prod(s(k-1,n),F.M[k-1]),F.S[k-1])}return prod(s(F.m,n),F.M[F.m])}
function finish(v,P,terminal){return vm(v,P).reduce((z,x,i)=>min(z,add(x,terminal[i])),null)}
function dyad(lo,hi,m,shifts,small,d,leaf,st){
 let memo=new Map();
 function sig(a,b,k){let z=[k];for(let [l,r] of shifts){let low=a+l,high=a+b-1n+r;let u=((low+b-1n)/b)*b;for(;u<=high;u+=b)z.push(val(u));z.push("|")}return z.join(",")}
 function rec(a,k){let b=1n<<BigInt(k);if(b<=BigInt(small)){let p=id(d);for(let j=0n;j<b;j++){st.rows++;p=prod(p,leaf(a+j),st)}return p}
 let z=sig(a,b,k);if(memo.has(z)){st.hits++;return memo.get(z)}st.nodes++;let p=prod(rec(a,k-1),rec(a+(b>>1n),k-1),st);memo.set(z,p);return p}
 let p=id(d),a=lo;while(a<hi){let k=0;while(k<m&&a%(1n<<BigInt(k+1))===0n&&a+(1n<<BigInt(k+1))<=hi)k++;p=prod(p,rec(a,k),st);a+=1n<<BigInt(k)}
 return p
}
function stats(){return{products:0,nodes:0,rows:0,hits:0}}
function band(A,B,w,terminal,compressed=true,cap=Infinity){
 if(A.L>B.L)return band(B,A,w,terminal,compressed,cap);
 let q=A.q,D=q*(2*w+1),W=BigInt(w),zero=()=>Array(q).fill(null),V=Array.from({length:2*w+1},zero),best=null,st=stats(),tails=new Map();
 V[w][0]=0n;
 const tail=(F,i)=>{let k=(F===A?"A":"B")+i;if(!tails.has(k))tails.set(k,suffix(F,i));return tails.get(k)};
 const row=i=>{let P=mat(D);for(let d=-w;d<=w;d++){let R=id(q);for(let e=d;e<=w;e++){if(e>=-w+1){let C=prod(R,at(A,i),st);for(let u=0;u<q;u++)for(let v=0;v<q;v++)P[(d+w)*q+u][(e-1+w)*q+v]=C[u][v]}
 if(e<w)R=prod(R,at(B,i+BigInt(e)),st)}}return P};
 function explicit(i){if(st.rows>=cap)throw Error("cap");st.rows++;let next=Array.from({length:2*w+1},zero);
 for(let d=-w;d<=w;d++){let j=i+BigInt(d);if(j<0n||j>=B.L)continue;let v=V[d+w];if(v.every(x=>x===null))continue;
 if(d<w){let u=vm(v,at(B,j));if(j+1n===B.L)best=min(best,finish(u,tail(A,i),terminal));else V[d+1+w]=union(V[d+1+w],u)}
 if(d>-w){let u=vm(v,at(A,i));if(i+1n===A.L)best=min(best,finish(u,tail(B,j),terminal));else next[d-1+w]=union(next[d-1+w],u)}
 }V=next}
 try{let K=A.L-W-1n;
 if(compressed&&K>W){for(let i=0n;i<W;i++)explicit(i);
 let P=dyad(W,K,A.m,[[A.n+1n,A.n+1n],[B.n-W+1n,B.n+W]],2*w,D,row,st);
 let y=vm(V.flat(),P);V=Array.from({length:2*w+1},(_,i)=>y.slice(i*q,(i+1)*q));for(let i=K;i<A.L;i++)explicit(i)}
 else{for(let i=0n;i<A.L;i++)explicit(i)}
 }catch(e){if(e.message==="cap")return{unknown:true,st};throw e}
 return{distance:best,st};
}
function grid(A,B,w,terminal){
 let LA=Number(A.L),LB=Number(B.L),q=A.q;let P=Array.from({length:LA+1},()=>Array.from({length:LB+1},()=>Array(q).fill(null)));P[0][0][0]=0n;
 for(let i=0;i<=LA;i++)for(let j=0;j<=LB;j++){
 let v=P[i][j];if(i<LA&&(j===LB||Math.abs(i+1-j)<=w))P[i+1][j]=union(P[i+1][j],vm(v,at(A,BigInt(i))));
 if(j<LB&&(i===LA||Math.abs(j+1-i)<=w))P[i][j+1]=union(P[i][j+1],vm(v,at(B,BigInt(j))))}
 return P[LA][LB].reduce((z,x,i)=>min(z,add(x,terminal[i])),null);
}
function paired(A,B,terminal){if(A.L>B.L)return paired(B,A,terminal);let st=stats(),q=A.q;
 function leaf(i){let a=at(A,i),b=at(B,i),X=prod(a,b,st),Y=prod(b,a,st);return mat(q,(u,v)=>min(X[u][v],Y[u][v]))}
 let P=dyad(0n,A.L-1n,A.m,[[A.n+1n,A.n+1n],[B.n+1n,B.n+1n]],1,q,leaf,st);P=prod(P,leaf(A.L-1n),st);P=prod(P,suffix(B,A.L),st);return{distance:finish(id(q)[0],P,terminal),st}}
let seed=271907;const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
let random={tests:0,finite:0,infinite:0,paired:0,wide:0};
for(let z=0;z<120;z++){let m=1+z%6,q=2+z%2,w=1+z%4,L=2**m;let n1=BigInt(Math.floor(rnd()*L)),n2=BigInt(Math.floor(rnd()*L));let gen=()=>Array.from({length:m+1},()=>mat(q,()=>rnd()<.38?null:BigInt(1+Math.floor(rnd()*9))));let A=macroSet(m,n1,gen()),B=macroSet(m,n2,gen()),t=Array.from({length:q},()=>rnd()<.3?null:BigInt(Math.floor(rnd()*4)));
 let d=grid(A,B,w,t),a=band(A,B,w,t),b=band(A,B,w,t,false);ck(a.distance===d&&b.distance===d,"grid");random.tests++;random[d===null?"infinite":"finite"]++;if(w>1)random.wide++;else{ck(paired(A,B,t).distance===d,"paired");random.paired++}}
let large=[];for(let m of [12,20,32,48,64]){let q=2,n=1n<<BigInt(m-1);n+=0x135n;let n2=(1n<<BigInt(m-2))+0x21n;let M=()=>Array.from({length:m+1},(_,i)=>mat(q,(a,b)=>BigInt((a===b?1:3)+(i%3))));let A=macroSet(m,n,M()),B=macroSet(m,n2,M()),t=[1n,2n],a=band(A,B,1,t),b=paired(A,B,t);ck(a.distance===b.distance,"large independent round recurrence");large.push({m,n:String(n),n2:String(n2),rows:a.st.rows,nodes:a.st.nodes,hits:a.st.hits,products:a.st.products,pairedProducts:b.st.products,distance:String(a.distance)})}
 // Source-native template: two counters, complete increments atomic, lag imposed in actual finite control.
 const f=s=>"1".repeat(s.length)+"0"+s,b=n=>n.toString(2),key=r=>r.join(",");
 function native(w,q){let states=[],map=new Map();for(let fl=0;fl<4;fl++)for(let d=fl===0?-w:0;d<=(fl===0?w:0);d++)for(let a=0;a<5;a++){if(a>0&&(fl&(1<<Math.floor((a-1)/2))))continue;map.set([fl,d,a].join(","),states.length);states.push([fl,d,a])}
 let code=(fl,d,a,i)=>3+q*map.get([fl,d,a].join(","))+i;
 let setup=[[0,1,0,0,1,1,1,1],[0,2,0,0,2,1,1,1],[0,0,0,2,0,0,0,0],[2,1,1,2,1,1,0,0],[2,2,1,2,2,1,0,0],[2,0,0,code(0,0,0,0),0,0,1,1]],catalog=[];
 let sym=(fl,a,t)=>fl&(1<<t)?[0]:a===1+2*t?[0,1,2]:a===2+2*t?[0,1]:[1,2];
 for(let [fl,d,a] of states)for(let x of sym(fl,a,0))for(let y of sym(fl,a,1))for(let i=0;i<q;i++){
  let u=code(fl,d,a,i);
  for(let j=0;j<q;j++)catalog.push({r:[u,x,y,code(fl,d,a,j),x,y,2,2],g:"S,"+i+","+j});
  if(fl===3){catalog.push({r:[u,x,y,1,x,y,2,2],g:"Z,"+i});continue}
  for(let t=0;t<2;t++){if(fl&(1<<t)||a&&Math.floor((a-1)/2)!==t)continue;let s=t?y:x,k=-1,v=s,move=2,na=0,nf=fl,nd=d;
   if(a===0||a===1+2*t){if(s===2){k=0;v=1;move=1;na=1+2*t}else if(s===1){k=1;v=2;move=0;na=2+2*t}else if(a!==0&&s===0){k=4;nf=fl|(1<<t)}}
   else if(a===2+2*t){if(s===1){k=2;move=0;na=a}else if(s===0){k=3;move=1;na=0}}
   if(k<0)continue;
   if(k>=3){if(fl===0){nd=d+(t?1:-1);if(Math.abs(nd)>w)continue}if(nf!==0)nd=0}
   for(let j=0;j<q;j++){let p=code(nf,nd,na,j),r=t?[u,x,y,p,x,v,2,move]:[u,x,y,p,v,y,move,2];catalog.push({r,g:[t,k,i,j].join(",")})}
  }
 }
 return{setup,catalog,code};
 }
 function build(w,q,groups){let C=native(w,q);return [...C.setup,...C.catalog.filter(x=>groups.has(x.g)).map(x=>x.r)]}
 function encode(rows,x,t,N=0){let s=f(rows.map(r=>r.map(v=>f(b(v))).join("")).join(""))+f(x)+f(b(t));return s+"0".repeat(Math.max(0,N-s.length))}
 function decode(w,h){let p=0;function get(s,j){let k=j;while(s[k]==="1")k++;if(s[k]!=="0"||2*k+1-j>s.length)throw Error("frame");return[s.slice(k+1,2*k+1-j),2*k+1-j]}let raw,x,t;[raw,p]=get(w,p);[x,p]=get(w,p);[t,p]=get(w,p);ck(/^[01]+$/.test(x)&&/^0*$/.test(w.slice(p))&&/^(0|1[01]*)$/.test(t));let T=BigInt("0b"+t);ck(T<=BigInt(w.length)**BigInt(h));let rows=[],j=0;while(j<raw.length){let r=[];for(let k=0;k<8;k++){let s;[s,j]=get(raw,j);ck(/^(0|1[01]*)$/.test(s));r.push(parseInt(s,2))}rows.push(r)}let n=0n;for(let i=0;i<x.length;i++)if(x[i]==="1")n|=1n<<BigInt(i);return{w,x,m:x.length,n,rows,T}}
 function acquire(F,w,q){let C=native(w,q),set=new Set(F.rows.map(key)),G=new Set();for(let e of C.catalog)if(set.has(key(e.r)))G.add(e.g);let expected=new Set(build(w,q,G).map(key));if(expected.size!==set.size||[...set].some(x=>!expected.has(x)))return null;
 let D=id(q),R=id(q);for(let i=0;i<q;i++)for(let j=0;j<q;j++)if(G.has("S,"+i+","+j))D[i][j]=min(D[i][j],1n);
 for(let k=0;k<q;k++)for(let i=0;i<q;i++)for(let j=0;j<q;j++)D[i][j]=min(D[i][j],add(D[i][k],D[k][j]));
 for(let i=0;i<q;i++){let todo=[i],d=Array(q).fill(null);d[i]=0n;for(let k=0;k<todo.length;k++)for(let j=0;j<q;j++)if(G.has("S,"+todo[k]+","+j)&&d[j]===null){d[j]=d[todo[k]]+1n;todo.push(j)}R[i]=d}ck(eq(D,R),"stutter BFS");
 let F0=[];for(let t=0;t<2;t++){let L=Array.from({length:5},(_,k)=>prod(D,mat(q,(i,j)=>G.has([t,k,i,j].join(","))?1n:null)));let M=[],P=id(q),Q=id(q);for(let r=0;r<F.m;r++){M.push(prod(prod(prod(P,L[1]),Q),L[3]));P=prod(P,L[0]);Q=prod(Q,L[2])}M.push(prod(P,L[4]));F0.push(macroSet(F.m,t?0n:F.n,M))}
 let z=Array.from({length:q},(_,i)=>D[i].reduce((x,y,j)=>G.has("Z,"+j)?min(x,add(y,1n)):x,null));return {A:F0[0],B:F0[1],z,G}
 }
 function ref(F,limit){let index=new Map();for(let r of F.rows){let k=r.slice(0,3).join(",");if(!index.has(k))index.set(k,[]);index.get(k).push(r)}
 let start=[0,0,0,F.n,0n,0,0],Q=[start],seen=new Set([start.slice(0,6).join(",")]);for(let k=0;k<Q.length;k++){if(k>=limit)return{unknown:true,steps:k};let [s,p1,p2,v1,v2,l,d]=Q[k];if(s===1)return{distance:BigInt(d),steps:k+1};let rd=(p,v,n)=>p<0||p>=n?0:((v>>BigInt(p))&1n)?2:1;
 for(let r of index.get([s,rd(p1,v1,F.m),rd(p2,v2,l)].join(","))||[]){let a=v1,c=v2,L=l;if(p1>=0&&p1<F.m){let z=1n<<BigInt(p1);a=r[4]===2?a|z:a&~z}if(p2===l&&r[5])L++;if(p2>=0&&p2<L){let z=1n<<BigInt(p2);c=r[5]===2?c|z:c&~z}let next=[r[3],p1+[-1,1,0][r[6]],p2+[-1,1,0][r[7]],a,c,L,d+1],k=next.slice(0,6).join(",");if(!seen.has(k)){seen.add(k);Q.push(next)}}
 }return{distance:null,steps:Q.length}}
 const pop=n=>{let p=0n;while(n){p+=n&1n;n>>=1n}return p};
 const H=(m,n)=>4n*((1n<<BigInt(m))-1n-n)-BigInt(m)+2n*pop(n)+1n;
 let G=new Set(["S,0,1","S,1,0","Z,0","Z,1"]);for(let t=0;t<2;t++)for(let k=0;k<5;k++)G.add([t,k,t,k>=3?1-t:t].join(","));
 let nativeTests=[],mutants=0,summary={A:{YES:0,NO:0,UNKNOWN:0},B:{YES:0,NO:0,UNKNOWN:0},C:{YES:0,NO:0,UNKNOWN:0},I:{YES:0,NO:0,UNKNOWN:0}};
 const label=(d,t)=>d===null||d>t?"NO":"YES";
 for(let [m,w] of [[1,1],[2,1],[3,2],[4,1],[6,2],[8,3],[12,1],[16,2],[24,1],[32,3],[48,1]]){
 let n=(1n<<BigInt(m-1))-1n,x=n.toString(2).padStart(m,"0").split("").reverse().join(""),rows=build(w,2,G),d=2n*BigInt(m)+3n+H(m,n)+H(m,0n)+n,N=Math.max(encode(rows,x,d).length,Math.ceil(Number(d)**.25));while(BigInt(N)**4n<d)N++;
 for(let t of [d-1n,d]){let word=encode(rows,x,t,N),F=parseCopy(word),J=parseCopy(word),K=parseCopy(word),I=parseCopy(word);ck(F.w===J.w&&J.w===K.w&&K.w===I.w);
 let a=acquire(F,w,2),c=acquire(I,w,2);ck(a&&c);for(let k=0;k<=m;k++)ck(eq(a.A.M[k],c.A.M[k])&&eq(a.B.M[k],c.B.M[k]));
 let setup=BigInt(2*m+2),cap=2*N,ar=band(a.A,a.B,w,a.z,false,Math.min(cap,4096)),A=ar.unknown?"UNKNOWN":label(add(setup,ar.distance),t);
 // B independently derives physical count only, does not exploit the stronger family-specific stutter formula.
 let B=label(2n*BigInt(J.m)+3n+H(J.m,J.n)+H(J.m,0n),t)==="NO"?"NO":"UNKNOWN";
 let r=ref(K,Math.min(cap,50000)),C=r.unknown?"UNKNOWN":label(r.distance,t);
 let ir=band(c.A,c.B,w,c.z),distance=add(setup,ir.distance),Ilabel=label(distance,t);ck(distance===d,"native formula");if(!r.unknown)ck(r.distance===d,"native reference");if(w===1)ck(paired(c.A,c.B,c.z).distance===ir.distance,"native round");
 for(let [k,v] of Object.entries({A,B,C,I:Ilabel})){ck(v==="UNKNOWN"||v===label(d,t));summary[k][v]++}
 nativeTests.push({m,w,N,n:String(n),t:String(t),distance:String(d),A,B,C,I:Ilabel,explicitRows:ar.st.rows,referenceStates:r.steps,...ir.st,cap:Math.min(cap,4096)});
 }
 let mut=rows.slice();mut.splice(6,1);ck(acquire(decode(encode(mut,x,0n),4),w,2)===null,"missing template context");mutants++;
 }
 function parseCopy(x){return decode(x,4)}
 // fixed alphabet subsequence -> shuffle DFA control, independently exhaustive on words <=4
 function sub(a,b){let i=0;for(let c of b)if(c===a[i])i++;return i===a.length}
 function shuf(a,b){let seen=new Set(),Q=[[0,0,"none"]];for(let k=0;k<Q.length;k++){let [i,j,s]=Q[k];if(i===a.length&&j===b.length)return true;let next=[];if(j<b.length)next.push([i,j+1,b[j]]);if(i<a.length&&s===a[i])next.push([i+1,j,"none"]);for(let n of next){let z=n.join(",");if(!seen.has(z)){seen.add(z);Q.push(n)}}}return false}
 let words=[""];for(let k=1;k<=4;k++)for(let i=0;i<2**k;i++)words.push(i.toString(2).padStart(k,"0"));for(let a of words)for(let b of words)ck(sub(a,b)===shuf(a,b),"subsequence reduction");
 return{checks,random,large,nativeTests,summary,mutants,subsequencePairs:words.length**2,scope:"sequential separate copies; cap explicit rows min(2N,4096), reference states min(2N,50000), not equal bit-work comparisons; no full path extraction"};
}
console.log(JSON.stringify(run(),null,2));
