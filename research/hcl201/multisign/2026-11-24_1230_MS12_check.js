"use strict";
function experiment(){
 const assert=(b)=>{if(!b)throw Error("assertion"); stats.assertions++};
 let seed=20261124;const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 const stats={assertions:0,random:0,sat:0,unsat:0,certified:0,strict:0,unknown:0,weightedQueries:0,localWords:0,convolutionPairs:0,closureScans:0,forcedPins:0,lifts:0,guardSplits:0,referenceWords:0,scales:[]};
 const parity=x=>{let p=0;while(x){p^=1;x&=x-1}return p};
 const sign=(w,x)=>parity(w&x)?-1n:1n;
 const event=(e,x)=>e.rows.reduce((s,[w,b])=>s+(parity(w&x)^b),0)>e.H;
 // Exact signed single-event weight histogram; no joint event enumeration.
 function moment(n,e,w,pins){
  stats.weightedQueries++;let fixed=0, val=0;
  for(const [i,b] of pins){fixed|=1<<i;if(b)val|=1<<i}
  const par=Array.from({length:n},(_,i)=>i);function find(i){while(par[i]!==i)i=par[i];return i}
  const rows=e.rows.map(([m,b])=>[m&~fixed,b^parity(m&val)]);
  for(const [m] of rows){const a=[];for(let i=0;i<n;i++)if(m>>i&1)a.push(i);for(let j=1;j<a.length;j++)par[find(a[j])]=find(a[0])}
  const groups=new Map();for(let i=0;i<n;i++)if(!(fixed>>i&1)){let k=find(i);if(!groups.has(k))groups.set(k,0);groups.set(k,groups.get(k)|(1<<i))}
  let constant=rows.filter(([m])=>!m).reduce((s,[,b])=>s+b,0);
  let hist=new Map([[constant,sign(w,val)]]);
  for(const mask of groups.values()){
   let local=new Map();for(let x=mask;;x=(x-1)&mask){stats.localWords++;let k=0;for(const [m,b] of rows)if(m&&(m&mask))k+=parity(m&x)^b;local.set(k,(local.get(k)||0n)+sign(w,x));if(x===0)break}
   const next=new Map();for(const [a,v] of hist)for(const [b,u] of local){stats.convolutionPairs++;next.set(a+b,(next.get(a+b)||0n)+v*u)}hist=next;
  }let s=0n;for(const [a,v] of hist)if(a>e.H)s+=v;return s;
 }
 const empty={rows:[],H:-1};
 function guarded(n,e,w,pins,guards=[]){let s=0n;for(let i=0;i<(1<<guards.length);i++){let z=w,b=0;for(let j=0;j<guards.length;j++)if(i>>j&1){z^=guards[j][0];b^=guards[j][1]}s+=(b?-1n:1n)*moment(n,e,z,pins)}const d=1n<<BigInt(guards.length);assert(s%d===0n);return s/d}
 function tree(m,edges){let p=Array.from({length:m},(_,i)=>i);function f(x){while(x!==p[x])x=p[x];return x}let out=[];for(const e of edges.slice().sort((a,b)=>a.weight>b.weight?-1:a.weight<b.weight?1:0)){let x=f(e.i),y=f(e.j);if(x!==y){p[x]=y;out.push(e)}}return out}
 function prepare(n,E){const M=1n<<BigInt(n),den=2n*M*M;let masks=[0];for(let i=0;i<n;i++){masks.push(1<<i);for(let j=0;j<i;j++)masks.push((1<<i)|(1<<j))}
  let A=E.map(e=>masks.map(w=>moment(n,e,w,[]))),F=A.map(a=>a[0]);let edges=[];
  for(let i=0;i<E.length;i++)for(let j=0;j<i;j++){let h=A[i].map((a,k)=>a+A[j][k]),h2=new Map();for(let a=0;a<h.length;a++)if(h[a])for(let b=0;b<h.length;b++)if(h[b]){let w=masks[a]^masks[b];h2.set(w,(h2.get(w)||0n)+h[a]*h[b])}
   let sq=h.reduce((s,v)=>s+v*v,0n),psd=M*(sq-M*(F[i]+F[j])),fr=den*(F[i]+F[j]-M);let weight=0n,kind="zero";if(fr>weight){weight=fr;kind="frechet"}if(psd>weight){weight=psd;kind="psd"}edges.push({i,j,h,h2,masks,weight,kind});
  }const T=tree(E.length,edges);return {M,den,F,T,root:den*(M-F.reduce((a,b)=>a+b,0n))+T.reduce((a,e)=>a+e.weight,0n)}
 }
 function credit(n,E,C,pins,guards=[]){const {M,den,T}=C;const N=guarded(n,empty,0,pins,guards),F=E.map(e=>guarded(n,e,0,pins,guards));let d=den*(N-F.reduce((a,b)=>a+b,0n));for(const e of T){if(e.kind==="zero")continue;if(e.kind==="frechet"){d+=den*(F[e.i]+F[e.j]-N);continue}let a=0n,b=0n;for(let k=0;k<e.h.length;k++)if(e.h[k])a+=e.h[k]*(guarded(n,E[e.i],e.masks[k],pins,guards)+guarded(n,E[e.j],e.masks[k],pins,guards));for(const [w,v] of e.h2)if(v)b+=v*guarded(n,empty,w,pins,guards);d+=2n*M*a-b-M*M*(F[e.i]+F[e.j]);}return d}
 function closure(n,E,pins,guards=[]){pins=pins.slice();while(true){stats.closureScans++;let N=guarded(n,empty,0,pins,guards);if(!N||E.some(e=>guarded(n,e,0,pins,guards)===N))return null;let changed=false;for(let i=0;i<n&&!changed;i++)if(!pins.some(([k])=>k===i)){let bad=[0,1].map(b=>{let p=[...pins,[i,b]],N=guarded(n,empty,0,p,guards);return !N||E.some(e=>guarded(n,e,0,p,guards)===N)});if(bad[0]&&bad[1])return null;if(bad[0]||bad[1]){pins.push([i,bad[0]?1:0]);stats.forcedPins++;changed=true}}if(!changed)return pins}}
 function lift(n,E,C,pins,guards=[]){pins=closure(n,E,pins,guards);assert(pins!==null&&credit(n,E,C,pins,guards)>0n);while(pins.length<n){let i=Array.from({length:n},(_,i)=>i).find(i=>!pins.some(([k])=>k===i)),p0=[...pins,[i,0]],p1=[...pins,[i,1]],d0=credit(n,E,C,p0,guards),d1=credit(n,E,C,p1,guards);assert(d0+d1===credit(n,E,C,pins,guards));pins=closure(n,E,d0>0n?p0:p1,guards);assert(pins!==null&&credit(n,E,C,pins,guards)>0n)}let x=pins.reduce((s,[i,b])=>s|(b<<i),0);assert(E.every(e=>!event(e,x))&&guards.every(([m,b])=>parity(m&x)===b));stats.lifts++;return x}
 function reference(n,E,C){const M=1<<n;let words=Array.from({length:M},(_,x)=>x),B=E.map(e=>words.map(x=>event(e,x)?1:0));stats.referenceWords+=M;let good=words.filter(x=>B.every(e=>!e[x]));let dirs=B.map(e=>Array.from({length:n},(_,i)=>{let d=3;for(let x of words)if(!(x>>i&1)){if(e[x]>e[x|1<<i])d&=2;if(e[x]<e[x|1<<i])d&=1}return d}));let edges=[];for(let i=0;i<E.length;i++)for(let j=0;j<i;j++){let a=C.F[i],b=C.F[j],v=C.den*(a+b-C.M);if(v<0n)v=0n;if(dirs[i].every((d,k)=>(d&dirs[j][k])!==0)){let h=2n*C.M*a*b;if(h>v)v=h}edges.push({i,j,weight:v})}
 let old=C.den*(C.M-C.F.reduce((a,b)=>a+b,0n))+tree(E.length,edges).reduce((s,e)=>s+e.weight,0n);
 for(let i=0;i<E.length;i++)assert(BigInt(B[i].reduce((s,x)=>s+x,0))===C.F[i]);
 for(const e of C.T)for(const x of words){let a=BigInt(B[e.i][x]),b=BigInt(B[e.j][x]);let h=e.h.reduce((s,v,k)=>s+v*sign(e.masks[k],x),0n);let p=e.kind==="psd"?2n*C.M*h*(a+b)-h*h-C.M*C.M*(a+b):e.kind==="frechet"?C.den*(a+b-1n):0n;assert(p<=C.den*a*b)}
 assert(C.root<=C.den*BigInt(good.length));return {good,old}
 }
 function run(n,E,label){let p=closure(n,E,[]);let C=prepare(n,E),R=reference(n,E,C);let D=credit(n,E,C,[]);assert(D===C.root);let a=credit(n,E,C,[],[[(1<<n)-1,0]]),b=credit(n,E,C,[],[[(1<<n)-1,1]]);assert(a+b===D);stats.guardSplits++;assert(a<=C.den*BigInt(R.good.filter(x=>!parity(x)).length));assert(b<=C.den*BigInt(R.good.filter(x=>parity(x)).length));
 if(R.good.length)stats.sat++;else stats.unsat++;
 if(D>0n){stats.certified++;assert(p!==null);let x=lift(n,E,C,[]);if(a>0n)lift(n,E,C,[],[[(1<<n)-1,0]]);else if(b>0n)lift(n,E,C,[],[[(1<<n)-1,1]]);if(R.old<=0n)stats.strict++}else stats.unknown++;
 if(label) return {label,n,events:E.length,legal:R.good.length,creditNumerator:String(D),denominator:String(C.den),oldNumerator:String(R.old),guardNumerators:[String(a),String(b)],selectedPSD:C.T.filter(e=>e.kind==="psd").length,closurePins:p?.length??null};
 }
 const E=[{rows:[[1,0],[12,1],[4,1]],H:2},{rows:[[8,0],[1,0],[4,1],[16,0],[48,1],[16,0],[2,1]],H:4},{rows:[[48,1],[8,1],[16,1],[32,0],[48,1],[1,1]],H:3},{rows:[[1,1],[48,1],[3,1],[3,1]],H:2},{rows:[[8,0],[2,0],[12,1],[8,0],[3,0]],H:4}];
 const strict=run(6,E,"strict");assert(BigInt(strict.creditNumerator)>0n&&BigInt(strict.oldNumerator)<=0n);
 const cube=Array.from({length:8},(_,v)=>({rows:[0,1,2].map(i=>[1<<i,1^(v>>i&1)]),H:2}));
 const unsat=run(3,cube,"full cover"),sat=run(3,cube.slice(1),"one deletion");assert(unsat.legal===0&&sat.legal===1);
 for(let k=0;k<60;k++){let n=4+rand(3),E=[];let count=3+rand(5);for(let j=0;j<count;j++){let rows=[];let L=3+rand(5);for(let t=0;t<L;t++){let i=rand(n),m=1<<i;if(rand(3)===0&&((i^1)<n))m|=1<<(i^1);rows.push([m,rand(2)])}E.push({rows,H:Math.floor(L/2)+rand(L-Math.floor(L/2))})}run(n,E);stats.random++}
 return {seed:20261124,stats,strict,unsat,sat,limitations:"one weight threshold, duplicate width-two rows, n<=6; exact joint enumeration reference only; no physical replay, no measured time/space"};
}
console.log(JSON.stringify(experiment(),null,2));
