'use strict';
// Independent audit: unsigned ternary incidence, no tree projection or binary-flow solver.
// Run node 2026-11-25_FP08_independent_audit.js
function auditFP08(){
 const mod=x=>(x%3+3)%3;
 const E0=[[0,2],[0,6],[0,9],[1,3],[1,7],[1,10],[2,10],[2,11],[3,8],[3,11],[4,5],[4,9],[4,11],[5,6],[5,10],[6,7],[7,8],[8,9]];
 const PE=Array.from({length:5},(_,i)=>[i,(i+1)%5]).concat(Array.from({length:5},(_,i)=>[i+5,5+(i+2)%5]),Array.from({length:5},(_,i)=>[i,i+5]));
 const Q=[[2,3],[2,7],[3,4],[3,8],[4,9],[5,7],[5,8],[6,8],[6,9],[7,9]], ports=[4,5,2,6];
 function assert(x,m){if(!x)throw Error(m);}
 function kernel(M,m){
   const A=M.map(r=>Uint8Array.from(r));let r=0;const piv=[];
   for(let j=0;j<m&&r<A.length;j++){
     let i=r;while(i<A.length&&!A[i][j])i++;if(i===A.length)continue;
     [A[i],A[r]]=[A[r],A[i]];
     if(A[r][j]===2)for(let k=j;k<m;k++)A[r][k]=mod(2*A[r][k]);
     for(let t=0;t<A.length;t++)if(t!==r&&A[t][j]){let q=A[t][j];for(let k=j;k<m;k++)A[t][k]=mod(A[t][k]-q*A[r][k]);}
     piv.push(j);r++;
   }
   const P=new Set(piv), B=[];
   for(let j=0;j<m;j++)if(!P.has(j)){
     const x=new Uint8Array(m);x[j]=1;for(let i=0;i<r;i++)x[piv[i]]=mod(-A[i][j]);B.push(x);
   }
   return {B,rank:r};
 }
 function independent(n,E){
   const inc=Array.from({length:n},()=>[]);for(let i=0;i<E.length;i++)for(const v of E[i])inc[v].push(i);
   assert(inc.every(a=>a.length===3),"degree");
   const M=inc.map(a=>{const row=new Uint8Array(E.length);for(const e of a)row[e]=1;return row;});
   const {B,rank}=kernel(M,E.length);
   const H=inc.map(a=>Uint8Array.from(B,x=>mod(x[a[1]]-x[a[0]])));
   return {inc,M,B,H,rank};
 }
 function norm(a){let s=0;for(const x of a)if(x){s=x;break;}return [s?Array.from(a,x=>mod(s*x)).join(""):"",s];}
 function low(H,max=4){
   const n=H.length,d=H[0].length,T=new Map(),pairs=new Map(),R=[new Set(),new Set(),new Set(),new Set(),new Set()];
   function add(ids,cs){const p=ids.map((id,i)=>[id,cs[i]]).sort((a,b)=>a[0]-b[0]);const t=p[0][1];R[p.length].add(p.map(([id,c])=>id+":"+mod(c*t)).join(","));}
   for(let i=0;i<n;i++){
     const [k,s]=norm(H[i]);if(!s){add([i],[1]);continue;}
     for(const [j,t] of T.get(k)||[])add([i,j],[1,mod(-s*t)]);
     if(!T.has(k))T.set(k,[]);T.get(k).push([i,s]);
   }
   for(let i=0;i<n;i++)for(let j=0;j<i;j++)for(const b of [1,2]){
     const a=new Uint8Array(d);for(let k=0;k<d;k++)a[k]=mod(H[i][k]+b*H[j][k]);
     const [key,s]=norm(a);if(!s)continue;
     for(const [k,t] of T.get(key)||[])if(k!==i&&k!==j)add([i,j,k],[1,b,mod(-s*t)]);
     if(max>=4){for(const [k,l,c,t] of pairs.get(key)||[])if(k!==i&&k!==j&&l!==i&&l!==j)add([i,j,k,l],[1,b,mod(-s*t),mod(-s*t*c)]);
       if(!pairs.has(key))pairs.set(key,[]);pairs.get(key).push([i,j,b,s]);}
   }
   return R.map(r=>[...r].sort());
 }
 function rawCount(n,E){
   const {inc,B,H,rank}=independent(n,E), m=E.length;
   let proper=0;const slopes=new Set();
   for(let i=0;i<3**B.length;i++){
     let q=i;const y=new Uint8Array(m);
     for(const b of B){const a=q%3;q=Math.floor(q/3);if(a)for(let e=0;e<m;e++)y[e]=mod(y[e]+a*b[e]);}
     assert(inc.every(a=>mod(a.reduce((s,e)=>s+y[e],0))===0),"kernel");
     if(inc.every(a=>new Set(a.map(e=>y[e])).size===3)){
       proper++;slopes.add(inc.map(a=>mod(y[a[1]]-y[a[0]])).join(""));
     }
   }
   const R=low(H,4);
   const adj=Array.from({length:n},()=>[]);for(const row of R[3]){
     const p=row.split(",").map(x=>x.split(":").map(Number));for(let i=1;i<3;i++){let a=p[0],b=p[i],s=mod(a[1]*b[1]);adj[a[0]].push([b[0],s,row]);adj[b[0]].push([a[0],s,row]);}
   }
   let contradiction=null;const val=new Uint8Array(n);
   for(let v=0;v<n&&!contradiction;v++)if(!val[v]){val[v]=1;const queue=[v];for(const u of queue){for(const [w,s,row] of adj[u]){const d=mod(val[u]*s);if(val[w]&&val[w]!==d){contradiction={u,w,row};break;}if(!val[w]){val[w]=d;queue.push(w);}}if(contradiction)break;}}
   return {n,incidenceRank:rank,edgeKernelDimension:B.length,proper,distinctSlopes:slopes.size,lowRowCounts:R.slice(1).map(a=>a.length),tripleSignConflict:contradiction,triples:R[3]};
 }
 function expanded(L){
   let n=12,E=E0.map(e=>e.slice());
   for(let v=0;v<12;v++)if(v!==1&&v!==10)for(let t=1;t<L;t+=2){
     const ids=E.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0),vv=[v,n,n+1];n+=2;
     ids.forEach((i,j)=>{const e=E[i];E[i]=e.map(x=>x===v?vv[j]:x);});E.push([vv[0],vv[1]],[vv[1],vv[2]],[vv[2],vv[0]]);
   }
   let nn=2*n,H=[];
   for(let i=0;i<E.length;i++){const [u,v]=E[i];if(i===5){H.push([u,v],[u+n,v+n]);continue;}
     const q=nn;nn+=8;for(const [a,b] of Q)H.push([q+a-2,q+b-2]);
     [u,v,u+n,v+n].forEach((a,j)=>H.push([a,q+ports[j]-2]));
   }
   return {n:nn,E:H};
 }
 const out={core:rawCount(12,E0),petersen:rawCount(10,PE),coupled:[]};
 assert(out.core.proper===12&&out.petersen.proper===0,"reference counts");
 assert(out.petersen.tripleSignConflict,"Petersen certificate");
 for(const L of [1,3]){const {n,E}=expanded(L);const {H,rank,B}=independent(n,E);const R=low(H,4);
   const counts=R.slice(1).map(x=>x.length);assert(counts.every(x=>x===0),"low-support barrier");
   out.coupled.push({L,n,incidenceRank:rank,edgeKernelDimension:B.length,lowRowCounts:counts});}
 return out;
}
console.log(JSON.stringify(auditFP08(),null,2));
