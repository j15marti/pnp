function run(){
 let assertions=0;const ck=x=>{assertions++;if(!x)throw Error("assert "+assertions)};
 const f=s=>"1".repeat(s.length)+"0"+s,b=n=>n.toString(2);
 function enc(rows,x,t,N=0){let w=f(rows.map(r=>r.map(z=>f(b(z))).join("")).join(""))+f(x)+f(b(t));return w+"0".repeat(Math.max(0,N-w.length))}
 function parse(w,h){
  let pos=0;function read(s,p){let z=p;while(s[z]==="1")z++;if(s[z]!=="0"||2*z+1-p>s.length)throw Error("frame");return[s.slice(z+1,2*z+1-p),2*z+1-p]}
  let a,x,t;[a,pos]=read(w,pos);[x,pos]=read(w,pos);[t,pos]=read(w,pos);
  if(!/^[01]+$/.test(x)||!/^0*$/.test(w.slice(pos))||!/^(0|1[01]*)$/.test(t))throw Error("frame");
  let T=BigInt("0b"+t);if(T>BigInt(w.length)**BigInt(h))throw Error("clock");
  let rows=[],p=0;while(p<a.length){let r=[];for(let k=0;k<8;k++){let z;[z,p]=read(a,p);if(!/^(0|1[01]*)$/.test(z))throw Error("field");let v=Number.parseInt(z,2);if(!Number.isSafeInteger(v))throw Error("id");r.push(v)}rows.push(r)}
  let q=1;for(let r of rows)for(let v of [r[0],r[3]])if(v!==1)q=Math.max(q,Math.floor(v/2)+(v%2===0?1:0));
  if(q>2*rows.length+1)throw Error("template");
  const phase=v=>v===1?"H":v%2===0?"I":"R",idx=v=>v%2===0?v/2:(v-3)/2;
  let letters={A:[],B:[],C:[],D:[],E:[]},st={I1:[],I2:[],I0:[],R1:[],R0:[]};
  for(let [id,r] of rows.entries()){
   const [u,s,x2,v,w1,w2,move,move2]=r,P=phase(u),Q=phase(v);
   if(P==="H"||x2!==0||w2!==0||move2!==2)throw Error("template");
   const i=idx(u),j=v===1?0:idx(v);
   if(P===Q&&s===w1&&move===2&&st[P+s])st[P+s].push([i,j,id]);
   else if(P==="I"&&s===2&&w1===1&&move===1&&Q==="I")letters.A.push([i,j,id]);
   else if(P==="I"&&s===1&&w1===2&&move===0&&Q==="R")letters.B.push([i,j,id]);
   else if(P==="R"&&s===1&&w1===1&&move===0&&Q==="R")letters.C.push([i,j,id]);
   else if(P==="R"&&s===0&&w1===0&&move===1&&Q==="I")letters.D.push([i,j,id]);
   else if(P==="I"&&s===0&&w1===0&&move===2&&Q==="H")letters.E.push([i,0,id]);
   else throw Error("template");
  }
  let n=0n;for(let i=0;i<x.length;i++)if(x[i]==="1")n|=1n<<BigInt(i);
  return{rows,x,n,m:x.length,q,T,letters,st,w};
 }
 const mat=(q,fn=()=>null)=>Array.from({length:q},(_,i)=>Array.from({length:q},(_,j)=>fn(i,j)));
 const id=q=>mat(q,(i,j)=>i===j?0n:null);
 function mul(A,B,meter=()=>{}){meter();let q=A.length;return mat(q,(i,j)=>{let z=null;for(let k=0;k<q;k++)if(A[i][k]!==null&&B[k][j]!==null){let v=A[i][k]+B[k][j];if(z===null||v<z)z=v}return z})}
 const equal=(A,B)=>A.every((r,i)=>r.every((z,j)=>z===B[i][j]));
 const contexts={A:"I2",B:"I1",C:"R1",D:"R0",E:"I0"};
 function local(F){let out={};for(let [letter,edges] of Object.entries(F.letters)){
   let q=F.q,D=id(q);
   for(let [i,j] of F.st[contexts[letter]])if(i!==j)D[i][j]=1n;
   for(let k=0;k<q;k++)for(let i=0;i<q;i++)for(let j=0;j<q;j++)if(D[i][k]!==null&&D[k][j]!==null){let v=D[i][k]+D[k][j];if(D[i][j]===null||v<D[i][j])D[i][j]=v}
   let X=mat(q);for(let [a,j] of edges)for(let i=0;i<q;i++)if(D[i][a]!==null){let z=D[i][a]+1n;if(X[i][j]===null||z<X[i][j])X[i][j]=z}
   out[letter]=X;
  }return out}
 function localIndependent(F){let out={};for(let [letter,edges] of Object.entries(F.letters)){
   let q=F.q,X=mat(q);for(let i=0;i<q;i++){let d=Array(q).fill(-1),Q=[i];d[i]=0;for(let h=0;h<Q.length;h++)for(let [a,b] of F.st[contexts[letter]])if(a===Q[h]&&d[b]<0){d[b]=d[a]+1;Q.push(b)}
   for(let [a,j] of edges)if(d[a]>=0){let z=BigInt(d[a]+1);if(X[i][j]===null||z<X[i][j])X[i][j]=z}}
   out[letter]=X;
  }return out}
 function macros(F,L,meter=()=>{}){let P=id(F.q),Q=id(F.q),fs=[];for(let r=0;r<F.m;r++){
  fs.push(mul(mul(mul(P,L.B,meter),Q,meter),L.D,meter));
  P=mul(P,L.A,meter);Q=mul(Q,L.C,meter)
 }return{fs,overflow:mul(P,L.E,meter)}}
 function structured(F,mac,meter=()=>{}){let S=[id(F.q)];for(let j=0;j<F.m;j++)S.push(mul(mul(S[j],mac.fs[j],meter),S[j],meter));
  function suff(j,n){if(!j)return id(F.q);let half=1n<<BigInt(j-1);
  if(n>=half)return suff(j-1,n-half);return mul(mul(suff(j-1,n),mac.fs[j-1],meter),S[j-1],meter)}
  return mul(suff(F.m,F.n),mac.overflow,meter)[0][0];
 }
 function sequential(F,mac,meter){let P=id(F.q),L=1n<<BigInt(F.m);for(let n=F.n;n<L-1n;n++){let y=n+1n,r=0;while((y&1n)===0n){r++;y>>=1n}P=mul(P,mac.fs[r],meter)}return mul(P,mac.overflow,meter)[0][0]}
 function brute(F,cap=Infinity){
  let Q=[[0,0,F.n,0]],seen=new Set(["0,0,"+F.n]),steps=0;
  for(let k=0;k<Q.length;k++){if(steps>=cap)return{unknown:true,steps};steps++;let [u,p,n,d]=Q[k];if(u===1)return{distance:BigInt(d),steps};let sym=p<0||p>=F.m?0:((n>>BigInt(p))&1n)?2:1;
   for(let r of F.rows){if(r[0]!==u||r[1]!==sym)continue;let y=n;if(p>=0&&p<F.m){let bit=1n<<BigInt(p);y=r[4]===2?y|bit:y&~bit;}let z=p+[-1,1,0][r[6]],v=r[3],key=v+","+z+","+y;if(!seen.has(key)){seen.add(key);Q.push([v,z,y,d+1])}}
  }return{distance:null,steps}
 }
 function base(F){let p=0;for(let x of F.x)p+=Number(x);return 4n*((1n<<BigInt(F.m))-1n-F.n)-BigInt(F.m)+2n*BigInt(p)+1n}
 function label(d,T){return d===null||d>T?"NO":"YES"}
 function budget(N){let used=0;return{tick(){if(used>=4*N)throw Error("cap");used++},used:()=>used}}
 let seed=17777;function rand(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296}
 const records=[],counts={A:{YES:0,NO:0,UNKNOWN:0},B:{YES:0,NO:0,UNKNOWN:0},C:{YES:0,NO:0,UNKNOWN:0},I:{YES:0,NO:0,UNKNOWN:0}};
 let checksLocal=0,mutation=0,pairs=0,hostile=0,randoms=0,synergy=0;
 function audit(rows,x,h,t,truth,N,refD,kind){
  let w=enc(rows,x,t,N);let Fa=parse(w,h),Fb=parse(w,h),Fc=parse(w,h),Fi=parse(w,h);
  ck(Fa.w===Fb.w&&Fb.w===Fc.w&&Fc.w===Fi.w);
  let La=local(Fa),Lc=localIndependent(Fc);for(let k of Object.keys(La)){ck(equal(La[k],Lc[k]));checksLocal+=Fa.q*Fa.q}
  let ma=macros(Fa,La);let ba=budget(w.length),bi=budget(w.length),A;
  try{A=label(sequential(Fa,ma,ba.tick),Fa.T)}catch(e){if(e.message!=="cap")throw e;A="UNKNOWN"}
  let B=base(Fb)>Fb.T?"NO":"UNKNOWN";let cb=brute(Fc,4*w.length),C=cb.unknown?"UNKNOWN":label(cb.distance,Fc.T);
  // source-exact import; independent closure on all five letters
  let Li=localIndependent(Fi);for(let k of Object.keys(La))ck(equal(La[k],Li[k]));
  let d=structured(Fi,ma,bi.tick),I=label(d,Fi.T);
  if(refD!==undefined)ck(d===refD);for(let [k,v] of Object.entries({A,B,C,I})){counts[k][v]++;ck(v===truth||v==="UNKNOWN")}
  ck(I===truth);if(A==="UNKNOWN"&&B==="UNKNOWN"&&C==="UNKNOWN")synergy++;
  records.push({kind,h,m:Fi.m,q:Fi.q,N:w.length,deadline:String(t),distance:d===null?null:String(d),A,B,C,I,globalOps:[ba.used(),0,cb.steps,bi.used()],localMatrices:5});
  let alt=La.B.map(r=>r.slice());alt[0][0]=alt[0][0]===null?0n:alt[0][0]+1n;ck(!equal(alt,Lc.B));mutation++;
 }
 function randomRows(q){let rows=[];const add=(u,s,v,w,m)=>rows.push([u,s,0,v,w,0,m,2]);
 for(let i=0;i<q;i++){let I=2*i,R=2*i+3;for(let j=0;j<q;j++){let J=2*j,S=2*j+3;
 for(let s of [0,1,2])if(rand()<.22)add(I,s,J,s,2);
 for(let s of [0,1])if(rand()<.22)add(R,s,S,s,2);
 if(rand()<.43)add(I,2,J,1,1);
 if(rand()<.43)add(I,1,S,2,0);
 if(rand()<.43)add(R,1,S,1,0);
 if(rand()<.43)add(R,0,J,0,1);
 }if(rand()<.45)add(I,0,1,0,2)}return rows}
 for(let i=0;i<90;i++){let q=2+i%3,m=1+i%6,x=Array.from({length:m},()=>rand()<.5?"0":"1").join(""),rows=randomRows(q);
  let w=enc(rows,x,0n),F=parse(w,2),d=brute(F).distance;randoms++;
  if(d===null){let t=100n,N=enc(rows,x,t).length;audit(rows,x,2,t,"NO",N,null,"random unreachable")}
  else{let N=enc(rows,x,d).length;audit(rows,x,2,d,"YES",N,d,"random neighbor");audit(rows,x,2,d-1n,"NO",N,d,"random neighbor");pairs++}
 }
 // Two modes: an extra stationary step is required before every carry after the first increment.
 const special=[[0,1,0,3,2,0,0,2],[2,1,0,3,2,0,0,2],[0,2,0,0,1,0,1,2],[2,2,0,0,2,0,2,2],[3,1,0,3,1,0,0,2],[3,0,0,2,0,0,1,2],[0,0,0,1,0,0,2,2]];
 for(let m of [2,4,8,12,16,20,24,32,40,48]){
  let x="0".repeat(m),L=1n<<BigInt(m),d=4n*L-BigInt(m)-3n+L/2n,N=enc(special,x,d).length;
  while(BigInt(N)**4n<d)N++;
  if(m<=8)ck(brute(parse(enc(special,x,d,N),4)).distance===d);
  audit(special,x,4,d,"YES",N,d,"state-delay counter");audit(special,x,4,d-1n,"NO",N,d,"state-delay counter");pairs++;hostile++;
  let mut=special.map(r=>r.slice());mut[0][4]=1;let rejected=false;try{parse(enc(mut,x,d,N),4)}catch(e){rejected=e.message==="template"}ck(rejected);
 }
 return{assertions,checksLocal,mutation,pairs,hostile,randoms,synergy,counts,records,scope:"sequential independent source copies, finite Floyd/BFS local verification, same 4N global-update cap (one composition or one visited config), primitive work unequal, all acquisition separately charged in theorem; no measured bit runtime"};
}
console.log(JSON.stringify(run(),null,2));
