function audit(){
 const assert=(p,m="assert")=>{if(!p)throw Error(m)}, bit=i=>1n<<BigInt(i), mask=C=>C.reduce((a,i)=>a^bit(i),0n), parity=x=>{let p=0;while(x){p^=1;x&=x-1n}return p};
 class Lin{
  constructor(n,base){this.n=n;this.b=base?base.b.slice():Array(n).fill(null)}
  red(a,t=0){for(let i=this.n-1;i>=0;i--)if(this.b[i]&&(a&bit(i))){a^=this.b[i][0];t^=this.b[i][1]}return[a,t]}
  add(a,t=0){[a,t]=this.red(a,t);if(!a)return t?-1:0;let i=a.toString(2).length-1;this.b[i]=[a,t];return 1}
  rank(){return this.b.filter(Boolean).length}
  witness(){let x=0n;for(let i=0;i<this.n;i++)if(this.b[i]&&parity(this.b[i][0]&x)!==this.b[i][1])x|=bit(i);return x}
 }
 function init(n,F,eq){const L=new Lin(n);for(const C of F)assert(L.add(mask(C),0)>=0);for(const [a,t]of eq)if(L.add(a,t)<0)return null;return L}
 function closure(F,L){if(!L)return null;for(;;){let change=false;const P=[];
  for(const C of F){let[a,s]=L.red(bit(C[0])^bit(C[1])),[b,t]=L.red(bit(C[0])^bit(C[2]));
   if((!a&&s)||(!b&&t)||(a===b&&s!==t))continue;
   if(!a||!b||a===b){const [v,r]=a?[a,s]:[b,t];const z=L.add(v,r^1);if(z<0)return null;change||=z>0}
   else P.push([a,b,a^b]);
  }if(!change)return P;
 }}
 function greedy(n,P){const W=new Lin(n);let packed=0;for(const V of P)if(V.every(v=>W.red(v)[0]!==0n)){assert(W.add(V[0])===1);assert(W.add(V[1])===1);packed++}return{W,packed}}
 function opt(n,P,k,W=new Lin(n),stats={nodes:0}){stats.nodes++;const V=P.find(v=>v.every(a=>W.red(a)[0]!==0n));if(!V)return W;if(!k)return null;
  for(const a of V){const X=new Lin(n,W);assert(X.add(a)===1);const z=opt(n,P,k-1,X,stats);if(z)return z}return null}
 function solve(n,F,eq=[],cap=20){const L=init(n,F,eq),P=closure(F,L);if(P===null)return{status:"NO",rank:0,leaves:0};const {W,packed}=greedy(n,P),r=W.rank();if(r>cap)return{status:"UNKNOWN",rank:r,packed,leaves:0};const B=W.b.filter(Boolean).map(x=>x[0]);let leaves=0;for(let i=0;i<2**r;i++){leaves++;const M=new Lin(n,L);let ok=true;for(let j=0;j<r;j++)if(M.add(B[j],(i>>j)&1)<0){ok=false;break}if(!ok)continue;const Q=closure(F,M);if(Q===null)continue;assert(Q.length===0,"nonlinear leaf");const x=M.witness();assert(valid(F,x,eq));return{status:"YES",rank:r,packed,leaves,x}}return{status:"NO",rank:r,packed,leaves}}
 function valid(F,x,eq=[]){return F.every(C=>C.reduce((s,i)=>s+Number(!!(x&bit(i))),0)===2)&&eq.every(([a,t])=>parity(a&x)===t)}
 function brute(n,F,eq){for(let i=0;i<2**n;i++)if(valid(F,BigInt(i),eq))return true;return false}
 function gadget(boundary,start){const C=boundary.map(i=>[i]);let n=start;for(let i=0;i<4;i++)for(let j=i+1;j<4;j++){C[i].push(n);C[j].push(n++)}return{C,n}}
 function project(n,F){const occ=Array.from({length:n},()=>[]);F.forEach((C,i)=>C.forEach(v=>occ[v].push(i)));const used=new Set(),G=[],eq=[];
  for(let i=0;i<F.length;i++){if(used.has(i))continue;const A=[i,...F[i].filter(v=>occ[v].length===2).map(v=>occ[v].find(j=>j!==i))];if(A.length!==4||new Set(A).size!==4||A.some(j=>used.has(j)))continue;const S=new Set(A),B=[],I=[];let ok=true;
   for(const j of A){const neighbors=[],outside=[];for(const v of F[j]){if(occ[v].length===2&&occ[v].every(t=>S.has(t))){neighbors.push(occ[v].find(t=>t!==j));if(!I.includes(v))I.push(v)}else outside.push(v)}if(neighbors.length!==3||new Set(neighbors).size!==3||outside.length!==1){ok=false;break}B.push(outside[0])}
   if(!ok||new Set(B).size!==4||I.length!==6)continue;
   A.forEach(j=>used.add(j));G.push({A,B,I});eq.push([mask(B),0]);
  }return{F:F.filter((_,i)=>!used.has(i)),G,eq}}
 function lift(F,G,x){for(const {A,I}of G){let found=false;for(let b=0;b<64;b++){let y=x&~mask(I);I.forEach((v,j)=>{if((b>>j)&1)y|=bit(v)});if(valid(A.map(i=>F[i]),y)){x=y;found=true;break}}assert(found,"lift failure")}assert(valid(F,x));return x}
 let seed=20261126;const rng=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 const random={tests:0,SAT:0,NO:0,leaves:0,exactAcquisition:0}, wheel=[],even=[],grid=[];
 for(let t=0;t<200;t++){const n=4+rng(7),F=[],seen=new Set();for(let i=0,m=1+rng(15);i<m;i++){let C=[];while(C.length<4){let v=rng(n);if(!C.includes(v))C.push(v)}C.sort((a,b)=>a-b);if(!seen.has(C.join())){F.push(C);seen.add(C.join())}}
  const eq=[];for(let i=0;i<n;i++)if(rng(8)===0)eq.push([bit(i),rng(2)]);const expected=brute(n,F,eq),s=solve(n,F,eq);assert(s.status!=="UNKNOWN"&&(s.status==="YES")===expected);random.tests++;random[expected?"SAT":"NO"]++;random.leaves+=s.leaves;
  const L=init(n,F,eq),P=closure(F,L);if(P!==null){const g=greedy(n,P);let found=null;for(let k=0;k<=g.W.rank();k++){found=opt(n,P,k);if(found){assert(found.rank()>=g.packed&&g.W.rank()<=2*found.rank());break}}assert(found!==null);random.exactAcquisition++}
 }
 const one=gadget([0,1,2,3],4);let gadgetWords=0;for(let w=0;w<16;w++){let exists=false;for(let b=0;b<64;b++)if(valid(one.C,BigInt(w+16*b)))exists=true;assert(exists===(parity(BigInt(w))===0));gadgetWords+=Number(exists)}
 function wheelSource(k,no){const F=[];let n=3*k;for(let i=0;i<k;i++)F.push([k+2*i,k+2*i+1,i,(i+1)%k]);for(let i=0;i<k;i++){const j=(i+1)%k,g=gadget([k+2*i,k+2*i+1,k+2*j,k+2*j+1],n);F.push(...g.C);n=g.n}if(no)F.push([0,2,4,n++]);return{n,F}}
 function linear(F){let S=new Set();for(const C of F)for(let i=0;i<4;i++)for(let j=i+1;j<4;j++){const p=[C[i],C[j]].sort((a,b)=>a-b).join();assert(!S.has(p),"not linear");S.add(p)}}
 for(const k of [7,15,31,63,127]){const R={k};for(const no of [false,true]){const{n,F}=wheelSource(k,no);linear(F);const raw=init(n,F,[]),h=raw.red(bit(k)^bit(k+1));assert(h[0]===0n&&h[1]===0,"virtual hub parity");const rawP=closure(F,raw);if(no)assert(rawP===null);const P=project(n,F);assert(P.G.length===k);const s=solve(n,P.F,P.eq);assert(s.status===(no?"NO":"YES"));if(!no)lift(F,P.G,s.x);
  R[no?"NO":"SAT"]={n,clauses:F.length,gadgets:P.G.length,rank:s.rank,leaves:s.leaves,rawClosureContradiction:rawP===null};
 }wheel.push(R)}
 for(const k of [8,16,32]){const{n,F}=wheelSource(k,false);linear(F);const P=project(n,F),L=init(n,P.F,P.eq),Q=closure(P.F,L);assert(Q!==null&&Q.length===k);const g=greedy(n,Q),h=opt(n,Q,1);assert(h&&h.rank()===1&&g.W.rank()===2);const s=solve(n,P.F,P.eq);assert(s.status==="YES");lift(F,P.G,s.x);even.push({k,n,greedyRank:g.W.rank(),optRank:h.rank(),leaves:s.leaves})}
 for(const k of [4,8,16,24]){let n=k*k+1,F=[],edges=[];for(let i=0;i<k;i++)for(let j=0;j<k;j++){let a=1+i*k+j;for(const b of [...(i+1<k?[a+k]:[]),...(j+1<k?[a+1]:[])]){F.push([0,a,b,n++]);edges.push([a,b])}}
  const L=init(n,F,[]),P=closure(F,L);assert(P&&P.length===F.length);const g=greedy(n,P);let x=0n;for(let i=1;i<=k*k;i++)x|=bit(i);assert(valid(F,x));const lower=k*Math.floor(k/2);assert(g.W.rank()>=lower);grid.push({k,n,clauses:F.length,greedyRank:g.W.rank(),certifiedLower:lower,explicitSAT:true})
 }
 return{seed:20261126,random,gadgetWords,wheel,even,grid};
}
console.log(JSON.stringify(audit(),null,2));
