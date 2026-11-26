function run(){
 let assertions=0;const check=(v,msg="")=>{assertions++;if(!v)throw Error("assert "+assertions+" "+msg)};
 const q=3,inf=null, mat=(n,fn=()=>null)=>Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>fn(i,j))),id=n=>mat(n,(i,j)=>i===j?0n:null);
 const min=(a,b)=>a===null?b:b===null?a:a<b?a:b;
 const add=(a,b,cap=null)=>{if(a===null||b===null)return null;let z=a+b;return cap!==null&&z>cap?null:z};
 function mul(A,B,cap=null,tick=()=>{}){tick();let n=A.length;return mat(n,(i,j)=>{let v=null;for(let k=0;k<n;k++)v=min(v,add(A[i][k],B[k][j],cap));return v})}
 const le=(A,B)=>A.every((r,i)=>r.every((a,j)=>B[i][j]===null||(a!==null&&a<=B[i][j])));
 const eq=(A,B)=>le(A,B)&&le(B,A);
 const clip=(A,t)=>A.map(r=>r.map(x=>x!==null&&x>t?null:x));
 function direction(A,B,t=null){let X=A.flatMap(a=>B.map(b=>[mul(a,b,t),mul(b,a,t)]));return {ab:X.every(([a,b])=>le(a,b)),ba:X.every(([a,b])=>le(b,a)),strict:X.some(([a,b])=>!eq(a,b))}}
 function shuffleDP(U,V,n,cap=null,tick=()=>{}){let prev;for(let i=0;i<=U.length;i++){let cur=[];for(let j=0;j<=V.length;j++){if(i===0&&j===0){cur.push(id(n));continue}let a=i?mul(prev[j],U[i-1],cap,tick):mat(n),b=j?mul(cur[j-1],V[j-1],cap,tick):mat(n);cur.push(mat(n,(x,y)=>min(a[x][y],b[x][y])))}prev=cur}return prev[V.length]}
 const product=(w,n,cap=null,tick=()=>{})=>w.reduce((p,a)=>mul(p,a,cap,tick),id(n));
 let seed=912763;function rnd(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296}
 let abstract={tests:0,admitted:0,cappedOnly:0,strict:0,neither:0};
 for(let z=0;z<500;z++){let n=2+z%2,gen=()=>mat(n,()=>rnd()<.35?null:BigInt(1+Math.floor(rnd()*7))),A=[gen(),gen()],B=[gen(),gen()];
  if(z%5===0)A=B=[gen()];let U=Array.from({length:1+z%4},()=>A[Math.floor(rnd()*A.length)]),V=Array.from({length:1+(z+2)%4},()=>B[Math.floor(rnd()*B.length)]);
  let d=direction(A,B),t=BigInt(1+z%16),c=direction(A.map(x=>clip(x,t)),B.map(x=>clip(x,t)),t),D=shuffleDP(U,V,n),C=shuffleDP(U,V,n,t);
  check(eq(C,clip(D,t)),"capping");if(d.ab||d.ba){abstract.admitted++;if(d.strict)abstract.strict++;check(eq(D,product(d.ab?[...U,...V]:[...V,...U],n)),"dominance")}
  else abstract.neither++;
  if(c.ab||c.ba){check(eq(C,product(c.ab?[...U,...V]:[...V,...U],n,t)),"capped dominance");if(!d.ab&&!d.ba)abstract.cappedOnly++}
  abstract.tests++;
 }
 // Native U_h: input on tape1, tape2 blank. Fixed q=3 shared control.
 // phases 0 increment, 1 return, 2 done. Native phase/read contexts.
 const Ctx=[[0,0],[0,1],[0,2],[1,0],[1,1],[2,0]];
 const letters=[{p:0,s:2,np:0,w:1,d:1},{p:0,s:1,np:1,w:2,d:0},{p:1,s:1,np:1,w:1,d:0},{p:1,s:0,np:0,w:0,d:1},{p:0,s:0,np:2,w:0,d:2}];
 const code=(a,b,i)=>3+(a*3+b)*q+i;
 function init(){return [[0,1,0,0,1,1,1,1],[0,2,0,0,2,1,1,1],[0,0,0,2,0,0,0,0],[2,1,1,2,1,1,0,0],[2,2,1,2,2,1,0,0],[2,0,0,code(0,0,0),0,0,1,1]]}
 function generate(st,A,B,accept){
  let rows=init();for(let [a,x] of Ctx)for(let [b,y] of Ctx)for(let [i,j] of st)rows.push([code(a,b,i),x,y,code(a,b,j),x,y,2,2]);
  for(let t=0;t<2;t++)for(let l=0;l<5;l++)for(let [i,j] of (t?B:A)[l])for(let [b,y] of Ctx){
   let {p,s,np,w,d}=letters[l];rows.push(t===0?[code(p,b,i),s,y,code(np,b,j),w,y,d,2]:[code(b,p,i),y,s,code(b,np,j),y,w,2,d]);
  }for(let i of accept)rows.push([code(2,2,i),0,0,1,0,0,2,2]);return rows;
 }
 const f=s=>"1".repeat(s.length)+"0"+s,b=n=>n.toString(2);
 function encode(rows,x,t,N=0){let w=f(rows.map(r=>r.map(v=>f(b(v))).join("")).join(""))+f(x)+f(b(t));return w+"0".repeat(Math.max(0,N-w.length))}
 function parse(w,h){let p=0;function read(s,j){let k=j;while(s[k]==="1")k++;if(s[k]!=="0"||2*k+1-j>s.length)throw Error("frame");return[s.slice(k+1,2*k+1-j),2*k+1-j]}
 let raw,x,t;[raw,p]=read(w,p);[x,p]=read(w,p);[t,p]=read(w,p);if(!/^[01]+$/.test(x)||!/^0*$/.test(w.slice(p))||!/^(0|1[01]*)$/.test(t))throw Error("frame");let T=BigInt("0b"+t);if(T>BigInt(w.length)**BigInt(h))throw Error("clock");
 let rows=[],j=0;while(j<raw.length){let a=[];for(let k=0;k<8;k++){let z;[z,j]=read(raw,j);if(!/^(0|1[01]*)$/.test(z))throw Error("field");let v=Number.parseInt(z,2);if(!Number.isSafeInteger(v))throw Error("id");a.push(v)}rows.push(a)}
 return {w,rows,x,T,m:x.length}}
 const key=r=>r.join(",");
 function acquire(F){
  // Extract one canonical copy of each rule from original IDs, regenerate all copies to prove exact coverage.
  let set=new Set(F.rows.map(key)),st=[],A=Array.from({length:5},()=>[]),B=Array.from({length:5},()=>[]),acc=[];
  for(let i=0;i<q;i++){for(let j=0;j<q;j++){
   if(set.has(key([code(0,0,i),0,0,code(0,0,j),0,0,2,2])))st.push([i,j]);
   for(let l=0;l<5;l++){let {p,s,np,w,d}=letters[l];if(set.has(key([code(p,0,i),s,0,code(np,0,j),w,0,d,2])))A[l].push([i,j]);if(set.has(key([code(0,p,i),0,s,code(0,np,j),0,w,2,d])))B[l].push([i,j]);}
  }if(set.has(key([code(2,2,i),0,0,1,0,0,2,2])))acc.push(i);}
  let expected=new Set(generate(st,A,B,acc).map(key));if(set.size!==expected.size||[...set].some(k=>!expected.has(k)))return null;
  let S=id(q);for(let [i,j] of st)S[i][j]=min(S[i][j],1n);
  for(let k=0;k<q;k++)for(let i=0;i<q;i++)for(let j=0;j<q;j++)S[i][j]=min(S[i][j],add(S[i][k],S[k][j]));
  let D=mat(q);for(let i=0;i<q;i++){let ds=Array(q).fill(null),queue=[i];ds[i]=0n;for(let k=0;k<queue.length;k++)for(let [u,v] of st)if(u===queue[k]&&ds[v]===null){ds[v]=ds[u]+1n;queue.push(v)}D[i]=ds}
  check(eq(D,S),"independent stutter distances");let cv=edges=>{let P=mat(q);for(let [i,j] of edges)P[i][j]=1n;return mul(S,P)};
  return {A:A.map(cv),B:B.map(cv),S,acc,st,rawA:A,rawB:B};
 }
 function value(x){let n=0n;for(let i=0;i<x.length;i++)if(x[i]==="1")n|=1n<<BigInt(i);return n}
 function count(m,n){let p=0n,u=n;while(u){p+=u&1n;u>>=1n}return 4n*((1n<<BigInt(m))-1n-n)-BigInt(m)+2n*p+1n}
 function expand(m,n){let L=1n<<BigInt(m),w=[];for(let i=n;i<L-1n;i++){let u=i,r=0;while(u&1n){r++;u>>=1n}for(let j=0;j<r;j++)w.push(0);w.push(1);for(let j=0;j<r;j++)w.push(2);w.push(3)}for(let j=0;j<m;j++)w.push(0);w.push(4);return w}
 function grammar(m,n,A,t,tick){
  let P=id(q),Q=id(q),M=[],S=[id(q)];for(let r=0;r<m;r++){M.push(mul(mul(mul(P,A[1],t,tick),Q,t,tick),A[3],t,tick));P=mul(P,A[0],t,tick);Q=mul(Q,A[2],t,tick);S.push(mul(mul(S[r],M[r],t,tick),S[r],t,tick))}
  function suf(j,n){if(!j)return id(q);let v=1n<<BigInt(j-1);return n>=v?suf(j-1,n-v):mul(mul(suf(j-1,n),M[j-1],t,tick),S[j-1],t,tick)}
  return mul(mul(suf(m,n),P,t,tick),A[4],t,tick);
 }
 function finish(P,L){let v=null;for(let j=0;j<q;j++)for(let a of L.acc)v=min(v,add(P[0][j],add(L.S[j][a],1n)));return v}
 function exactRef(F,limit){let index=new Map();for(let r of F.rows){let k=r.slice(0,3).join(",");if(!index.has(k))index.set(k,[]);index.get(k).push(r)}
  let u=[0,0,0,value(F.x),0n,0,0],queue=[u],seen=new Set(),steps=0; // tape2 occupancy mask required during initialization
  // tuple q,head1,head2,value1,value2, initialized mask (low initialized prefix length), distance
  seen.add(u.slice(0,6).join(","));
  for(let k=0;k<queue.length;k++){if(steps>=limit)return {unknown:true,steps};steps++;let [s,p1,p2,v1,v2,initlen,d]=queue[k];if(s===1)return {distance:BigInt(d),steps};
   const read=(p,v,len)=>p<0||p>=len?0:((v>>BigInt(p))&1n)?2:1;
   let a=read(p1,v1,F.m),b=read(p2,v2,initlen);
   for(let r of index.get([s,a,b].join(","))||[]){let w1=v1,w2=v2,l=initlen; if(p1>=0&&p1<F.m){let bit=1n<<BigInt(p1);w1=r[4]===2?v1|bit:v1&~bit;}
    if(r[5]!==0&&p2===l)l++;
    if(p2>=0&&p2<l){let bit=1n<<BigInt(p2);w2=r[5]===2?v2|bit:v2&~bit}
    let next=[r[3],p1+[-1,1,0][r[6]],p2+[-1,1,0][r[7]],w1,w2,l,d+1],key=next.slice(0,6).join(",");
    if(!seen.has(key)){seen.add(key);queue.push(next)}
   }
  }return {distance:null,steps};
 }
 const label=(d,t)=>d===null||d>t?"NO":"YES";
 const st=[[0,2],[1,2]],edgeA=[[0,1],[1,1],[2,1]],edgeB=[[1,1],[2,0]],repeat=e=>Array.from({length:5},()=>e);
 let rows=generate(st,repeat(edgeA),repeat(edgeB),[2]),records=[],summary={A:{YES:0,NO:0,UNKNOWN:0},B:{YES:0,NO:0,UNKNOWN:0},C:{YES:0,NO:0,UNKNOWN:0},I:{YES:0,NO:0,UNKNOWN:0}},synergy=0,mutants=0;
 for(let m of [1,2,3,4,5,6,8,12,16,24,32,40,48]){
  let x="0".repeat(m),d=8n*(1n<<BigInt(m))-2n,N=encode(rows,x,d).length;while(BigInt(N)**4n<d)N++;
  for(let t of [d-1n,d]){
   let w=encode(rows,x,t,N),FA=parse(w,4),FB=parse(w,4),FC=parse(w,4),FI=parse(w,4);check(FA.w===FB.w&&FB.w===FC.w&&FC.w===FI.w);
   let L=acquire(FA),LI=acquire(FI);check(L&&LI);for(let i=0;i<5;i++)check(eq(L.A[i],LI.A[i])&&eq(L.B[i],LI.B[i]));
   let n=value(FA.x),m0=FA.m,ca=count(m0,n),cb=count(m0,0n),prefix=BigInt(2*m0+2),cap=2*w.length,truth=label(d,t),A="UNKNOWN",aops=0;
   if(2n*(ca+1n)*(cb+1n)<=BigInt(cap)){
    let P=shuffleDP(expand(m0,n).map(i=>L.A[i]),expand(m0,0n).map(i=>L.B[i]),q,null,()=>aops++),z=finish(P,L);A=label(add(prefix,z),t);check(add(prefix,z)===d,"native shuffle");
   }
   let B=BigInt(2*FB.m+3)+count(FB.m,value(FB.x))+count(FB.m,0n)>FB.T?"NO":"UNKNOWN";
   let C=exactRef(FC,cap),cl=C.unknown?"UNKNOWN":label(C.distance,t);if(!C.unknown)check(C.distance===d,"native BFS");
   let D=direction(LI.A,LI.B);check(D.ab&&!D.ba&&D.strict,"strict direction");
   let ops=0,pa=grammar(FI.m,value(FI.x),LI.A,null,()=>ops++),pb=grammar(FI.m,0n,LI.B,null,()=>ops++),z=add(prefix,finish(mul(pa,pb,null,()=>ops++),LI));check(z===d,"native grammar");let I=label(z,t);
   for(let [k,v] of Object.entries({A,B,C:cl,I})){check(v==="UNKNOWN"||v===truth,"decision");summary[k][v]++}
   if([A,B,cl].every(s=>s==="UNKNOWN"))synergy++;
   records.push({m,N,deadline:String(t),distance:String(z),A,B,C:cl,I,aops,cops:C.steps,integratedProducts:ops,cap});
  }
  let mut=rows.slice();mut.splice(6,1);check(acquire(parse(encode(mut,x,0n),4))===null,"missing context");mutants++;
 }
 // Actual native counterexample: alternating local actions, both serial orders impossible.
 let alt=generate([],repeat([[0,1]]),repeat([[1,0]]),[0]),x="00",d=BigInt(2*x.length+3)+2n*count(x.length,0n);
 let F=parse(encode(alt,x,d),4),L=acquire(F),D=direction(L.A,L.B),a=grammar(2,0n,L.A,null,()=>{}),b0=grammar(2,0n,L.B,null,()=>{});check(!D.ab&&!D.ba);check(finish(mul(a,b0),L)===null&&finish(mul(b0,a),L)===null);check(exactRef(F,1e6).distance===d,"alternation reference");
 let no=parse(encode(alt,x,d-1n,F.w.length),4);check(label(exactRef(no,1e6).distance,no.T)==="NO"); 
 return {assertions,abstract,summary,synergy,mutants,nativePairs:13,alternationPair:1,records,scope:"Sequential independent copies; common 2N global update cap, matrix multiply and graph expansion not equivalent bit operations. Fixed q=3 native adapter, exact byte comparisons; no production bit-machine benchmark."};
}
console.log(JSON.stringify(run(),null,2));
