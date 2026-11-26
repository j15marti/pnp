// Independent deterministic hash-based sparse recovery and source rotation audit.
const run=()=>{
let checks=0;const ok=x=>{checks++;if(!x)throw Error("assertion "+checks)};
let seed=261126;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
const parity=x=>{let p=0;while(x){x&=x-1;p^=1}return p};
const sign=(a,b)=>parity(a&b)?-1n:1n;
function hashRecovery(d,query,cap){
 let P=[0],C=[query(0)];if(C[0]===0n)return new Map();if(cap<1)return null;
 for(let i=0;i<d;i++){
  const candidates=P.flatMap(p=>[p,p|(1<<i)]),H=[];let D=[];
  for(let u=0;u<candidates.length;u++)for(let v=u+1;v<candidates.length;v++)D.push(candidates[u]^candidates[v]);
  // Derandomize pair-separation by conditional expectation; no unknown support used.
  while(D.length){
   let w=0;
   function score(z,f){let s=0;for(const x of D){if(x&~f)s++;else s+=2*parity(x&z)}return s}
   for(let j=0;j<=i;j++){const f=(1<<(j+1))-1,b=1<<j;if(score(w|b,f)>score(w,f))w|=b}
   const E=D.filter(x=>!parity(x&w));ok(E.length<=Math.floor(D.length/2));H.push(w);D=E;
  }
  const n=1<<H.length,F=Array.from({length:n},(_,j)=>query(H.reduce((s,w,h)=>j>>h&1?s^w:s,0)));
  for(let b=1;b<n;b*=2)for(let j=0;j<n;j+=2*b)for(let h=0;h<b;h++){let a=F[j+h],c=F[j+h+b];F[j+h]=a+c;F[j+h+b]=a-c}
  let V=[],W=[];const used=new Set();
  for(let p of candidates){let h=H.reduce((s,w,j)=>s|(parity(p&w)<<j),0);ok(!used.has(h));used.add(h);ok(F[h]%BigInt(n)===0n);let x=F[h]/BigInt(n);ok(x>=0n);if(x){V.push(p);W.push(x)}}
  for(let j=0;j<n;j++)if(!used.has(j))ok(F[j]===0n);
  if(V.length>cap)return null;P=V;C=W;
 }
 return new Map(P.map((p,i)=>[p,C[i]]));
}
let sparseChecks=0;
for(let t=0;t<160;t++){
 const d=2+rnd(9),k=1+rnd(Math.min(24,1<<d)),S=new Map();while(S.size<k){let p=rnd(1<<d);S.set(p,(BigInt(rnd(1<<24))<<20n)+BigInt(rnd(1<<20))+1n)}
 const q=w=>[...S].reduce((s,[p,v])=>s+v*sign(p,w),0n);const A=hashRecovery(d,q,k);ok(A.size===S.size);for(let [p,v] of S)ok(A.get(p)===v);
 ok(hashRecovery(d,q,k-1)===null);
 const B=new Map([...S].map(([p,v])=>[p,v/BigInt(1+rnd(7))]).filter(([p,v])=>v));
 const V=hashRecovery(d,w=>[...B].reduce((s,[p,v])=>s+v*sign(p,w),0n),k);ok(V.size===B.size);for(let [p,v] of B)ok(V.get(p)===v);sparseChecks++;
}
const B=[[0,0,0],[1,1,1],[0,0,1],[1,1,0],[0,1,0],[1,0,1]];
const R0=[[6,10,8],[7,9,11],[6,8,11],[9,7,10],[10,6,9],[8,7,11],[0,2,4],[5,3,1],[2,0,5],[1,3,4],[3,0,4],[1,2,5]];
function rank(A){const B=new Map();for(let x of A)while(x){let p=x.toString(2).length-1;if(!B.has(p)){B.set(p,x);break}x^=B.get(p)}return B.size}
function connected(R){let S=new Set([0]),Q=[0];while(Q.length){let u=Q.pop();for(let v of R[u])if(!S.has(v)){S.add(v);Q.push(v)}}return S.size===R.length}
function dbl(k){
 let T=[],R=[];for(let i=0;i<k;i++){for(let t of B)T.push(t.map(x=>x+2*i));for(let r of R0)R.push((i%2?r.slice().reverse():r).map(x=>x+12*i))}
 const own=(c,v)=>12*Math.floor(v/2)+2*c+v%2;
 const replace=(x,a,b)=>{const j=R[x].indexOf(a);ok(j>=0);R[x][j]=b};
 const swap=(u,i,v,j,c)=>{let a=6*u+i,b=6*v+j,x=12*u+6+i,y=12*v+6+j,A=own(c,T[a][c]),D=own(c,T[b][c]);replace(x,A,D);replace(A,x,y);replace(y,D,A);replace(D,y,x);[T[a][c],T[b][c]]=[T[b][c],T[a][c]]};
 for(let i=0;i<k-1;i++){swap(i,2,i+1,3,0);swap(i,0,i+1,1,1)}
 ok(new Set(T.map(t=>t.join(","))).size===T.length);
 for(let i=0;i<T.length;i++){let u=12*Math.floor(i/6)+6+i%6;ok(T[i].every((v,c)=>R[u].includes(own(c,v))))}
 for(let u=0;u<R.length;u++){ok(new Set(R[u]).size===3);for(let v of R[u])ok(R[v].includes(u))}
 let seen=new Set(),F=0;for(let u=0;u<R.length;u++)for(let v of R[u])if(!seen.has(u+","+v)){F++;let a=u,b=v;while(!seen.has(a+","+b)){seen.add(a+","+b);let c=R[b][(R[b].indexOf(a)+1)%R[b].length];a=b;b=c}ok(a===u&&b===v)}
 ok(seen.size===36*k&&R.length-seen.size/2+F===2&&connected(R));
 const n=2*k,ranks=[];
 for(let p=0;p<3;p++){let J=T.filter((t,i)=>Math.floor(i%6/2)===p);ok(J.length===n);for(let c=0;c<3;c++)ok(new Set(J.map(t=>t[c])).size===n)}
 for(let [a,b,p,q] of [[0,1,0,1],[0,2,0,2],[1,2,1,2]]){
  const c=3-a-b,G=Array.from({length:2*n},()=>[]),P=T.filter((t,i)=>Math.floor(i%6/2)===p),Q=T.filter((t,i)=>Math.floor(i%6/2)===q);
  for(let t of T){G[t[a]].push(n+t[b]);G[n+t[b]].push(t[a])}ok(connected(G));
  const D=[];for(let t of P){let u=Q.filter(s=>s[a]===t[a]&&s[b]===t[b]);ok(u.length===1);D.push((1n<<BigInt(t[c]))^(1n<<BigInt(u[0][c])))}
  let d=rank(D);ok(d===n-1);ranks.push(d);
 }
 const A=[];for(let c=0;c<3;c++)for(let z=0;z<n;z++){let w=0n;for(let j=0;j<T.length;j++)if(T[j][c]===z)w|=1n<<BigInt(j);A.push(w)}const nullity=T.length-rank(A);ok(nullity===2);
 return {k,triples:T.length,faces:F,ranks,nullity,supportEach:(1n<<BigInt(n-1)).toString()};
}
const double=[2,4,8,16,32,64,128,256].map(dbl);
const U="000 002 010 011 021 022 100 101 111 201 202 221".split(" ").map(t=>[...t].map(Number)),V=U.concat([[1,1,0]]);
function matching(T,a,b){let M=[];for(let x=0;x<T.length;x++)if(T[x][a]===0)for(let y=0;y<T.length;y++)if(T[y][a]===1)for(let z=0;z<T.length;z++)if(T[z][a]===2){let J=[x,y,z];if(new Set(J.map(j=>T[j][b])).size===3)M.push(J)}return M}
for(let T of [U,V]){
 for(let [a,b] of [[0,1],[0,2],[1,2]]){let M=matching(T,a,b);for(let j=0;j<T.length;j++){ok(M.some(s=>s.includes(j)));ok(M.some(s=>!s.includes(j)))}}
 let S=[];for(let x=0;x<1<<T.length;x++){let good=true;for(let a=0;a<3;a++)for(let z=0;z<3;z++){let n=0;for(let j=0;j<T.length;j++)if(x>>j&1&&T[j][a]===z)n++;if(n%2!==1)good=false}if(good)S.push(x)}for(let j=0;j<T.length;j++){ok(S.some(s=>s>>j&1));ok(S.some(s=>!(s>>j&1)))}
 ok(matching(T,0,1).filter(s=>new Set(s.map(j=>T[j][2])).size===3).length===(T===U?0:3));
}
const C=matching(V,0,1).filter(s=>new Set(s.map(j=>V[j][2])).size===3),mf=[];let d=[1n,1n,1n];for(let k=1;k<=64;k++){if([1,2,4,8,16,32,64].includes(k))mf.push({k,count:d.reduce((s,x)=>s+x,0n).toString()});d=C.map(b=>C.reduce((s,a,j)=>s+(a.includes(4)===b.includes(1)?d[j]:0n),0n))}
return {checks,sparseChecks,double,mf};
};
console.log(JSON.stringify(run(),null,2));
