function runM05(){
  let seed=0x201505; const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
  const bit=i=>1n<<BigInt(i), parity=x=>{let p=0;while(x){p^=1;x&=x-1n}return p};
  const pop=x=>{let n=0;while(x){n++;x&=x-1n}return n};
  const stats={seed:"0x201505",random_graphs:0,exhaustive_subsets:0,tag_optima:0,finite_optima:0,infinite_optima:0,witness_checks:0,basis_controls:0,empty_fibers:0,basis_probes:0,disagreements:0,scaling:[],hostile:[]};
  const insist=(x,msg)=>{if(!x)throw Error(msg)};
  function basis(m){const a=Array(m).fill(0n);return {a,add(x){for(let i=m-1;i>=0;i--)if(x&bit(i)){if(a[i])x^=a[i];else{a[i]=x;return true}}return false},has(x){for(let i=m-1;i>=0;i--)if(x&bit(i)){if(!a[i])return false;x^=a[i]}return !x},rank(){return a.filter(Boolean).length},orth(){const b=[];for(let j=0;j<m;j++)if(!a[j]){let x=bit(j);for(let i=0;i<m;i++)if(a[i]&&parity(a[i]&x))x^=bit(i);b.push(x)}return b}}}
  const put=(a,i,c,x)=>{if(c< (a[i]?.c??Infinity))a[i]={c,x}};
  function merge(A,B,Q){const C=Array(Q).fill(null);for(let i=0;i<Q;i++)if(A[i])for(let j=0;j<Q;j++)if(B[j])put(C,i^j,A[i].c+B[j].c,A[i].x^B[j].x);return C}
  function solve(n,E,T,q){
    const Q=1<<q,adj=Array.from({length:n},()=>[]);
    for(let i=0;i<E.length;i++){const [u,v,w,g]=E[i];adj[u].push([v,w,g,i]);adj[v].push([u,w,g,i])}
    const comp=[];let seen=new Set();for(let v=0;v<n;v++)if(!seen.has(v)){const a=[v];seen.add(v);for(let j=0;j<a.length;j++)for(const [u] of adj[a[j]])if(!seen.has(u)){seen.add(u);a.push(u)}comp.push(a)}
    const C=Array(Q).fill(null);C[0]={c:0,x:0n};let P=C.slice();
    function distances(v){
      const size=n*Q,d=Array(size).fill(Infinity),x=Array(size).fill(0n),heap=[];
      function push(a){let i=heap.length;heap.push(a);while(i){let p=(i-1)>>1;if(heap[p][0]<=a[0])break;heap[i]=heap[p];i=p;heap[i]=a}}
      function take(){const a=heap[0],b=heap.pop();if(heap.length){let i=0;heap[0]=b;for(;;){let j=i*2+1;if(j>=heap.length)break;if(j+1<heap.length&&heap[j+1][0]<heap[j][0])j++;if(heap[j][0]>=b[0])break;heap[i]=heap[j];i=j;heap[i]=b}}return a}
      d[v*Q]=0;push([0,v*Q]);while(heap.length){const [z,i]=take();if(z!==d[i])continue;const u=Math.floor(i/Q),g=i%Q;for(const [w,c,h,e] of adj[u]){const j=w*Q+(g^h),nd=z+c;if(nd<d[j]){d[j]=nd;x[j]=x[i]^bit(e);push([nd,j])}}}
      return {d,x};
    }
    for(const a of comp){
      const t=a.filter(v=>T&bit(v));if(t.length%2)return Array(Q).fill(null);
      if(t.length>20)throw Error("test implementation only: component terminal limit 20");
      const terminalDist=new Map();
      for(const v of a){if(!q&&!t.includes(v))continue;const r=distances(v);if(t.includes(v))terminalDist.set(v,r);for(let g=1;g<Q;g++)if(Number.isFinite(r.d[v*Q+g]))put(C,g,r.d[v*Q+g],r.x[v*Q+g])}
      const memo=new Map([[0,Array.from({length:Q},(_,i)=>i?null:{c:0,x:0n})]]);
      function dp(s){if(memo.has(s))return memo.get(s);const i=31-Math.clz32(s&-s),out=Array(Q).fill(null),r=terminalDist.get(t[i]);for(let j=i+1;j<t.length;j++)if(s&(1<<j)){const sub=dp(s^(1<<i)^(1<<j));for(let g=0;g<Q;g++){const k=t[j]*Q+g;if(!Number.isFinite(r.d[k]))continue;for(let h=0;h<Q;h++)if(sub[h])put(out,g^h,r.d[k]+sub[h].c,r.x[k]^sub[h].x)}}memo.set(s,out);return out}
      P=merge(P,dp((1<<t.length)-1),Q);
    }
    let cycles=Array.from({length:Q},(_,i)=>i?null:{c:0,x:0n});for(let j=0;j<q;j++)cycles=merge(cycles,C,Q);
    return merge(P,cycles,Q);
  }
  function inspect(E,x){let T=0n,g=0,c=0;for(let i=0;i<E.length;i++)if(x&bit(i)){const [u,v,w,h]=E[i];T^=bit(u)^bit(v);g^=h;c+=w}return {T,g,c}}
  function verify(E,T,A){for(let g=0;g<A.length;g++)if(A[g]){const z=inspect(E,A[g].x);insist(z.T===T&&z.g===g&&z.c===A[g].c,"bad reconstructed join");stats.witness_checks++}}
  function affine(n,E,T,K){
    const m=E.length,plain=E.map(([u,v,w])=>[u,v,w,0]),base=solve(n,plain,T,0)[0];if(!base||base.c>K)return null;
    const W=basis(m),U=basis(m),witnesses=[base.x];let probes=0;
    while(W.rank()+U.rank()<m){const p=W.orth().find(x=>!U.has(x));insist(p!==undefined,"dual selection");const tagged=E.map(([u,v,w],i)=>[u,v,w,Number(Boolean(p&bit(i)))]),g=parity(p&base.x)^1,A=solve(n,tagged,T,1);verify(tagged,T,A);probes++;if(A[g]&&A[g].c<=K){insist(W.add(A[g].x^base.x),"nonprogress witness");witnesses.push(A[g].x)}else insist(U.add(p),"nonprogress identity")}
    stats.basis_probes+=probes;return {W,U,base:base.x,witnesses,probes}
  }
  for(let k=0;k<160;k++){
    const n=2+rnd(6),E=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(rnd(100)<46&&E.length<12)E.push([u,v,rnd(5),rnd(8)]);
    if(k%7===0&&E.length<12)E.push([0,1,rnd(5),rnd(8)]);
    let T=0n;if(k%2===0){for(let i=0;i<E.length;i++)if(rnd(3)===0)T^=bit(E[i][0])^bit(E[i][1])}else for(let i=0;i<n;i++)if(rnd(3)===0)T^=bit(i);
    const q=3,A=solve(n,E,T,q),ref=Array(8).fill(null),K=rnd(13),feasible=[];
    for(let mask=0;mask<2**E.length;mask++){const x=BigInt(mask),z=inspect(E,x);stats.exhaustive_subsets++;if(z.T===T){put(ref,z.g,z.c,x);if(z.c<=K)feasible.push(x)}}
    verify(E,T,A);for(let g=0;g<8;g++){insist((A[g]?.c??Infinity)===(ref[g]?.c??Infinity),"optimum discrepancy");stats.tag_optima++;if(A[g])stats.finite_optima++;else stats.infinite_optima++}
    const F=affine(n,E,T,K);stats.basis_controls++;if(!feasible.length){insist(F===null,"false feasible");stats.empty_fibers++}else{insist(F!==null,"false empty");const R=basis(E.length);for(const x of feasible)R.add(x^feasible[0]);insist(F.W.rank()===R.rank()&&R.has(F.base^feasible[0]),"affine rank");for(const x of F.witnesses){const z=inspect(E,x);insist(z.T===T&&z.c<=K,"affine witness");insist(R.has(x^feasible[0]),"false span")}for(const x of feasible)insist(F.W.has(x^F.base),"missed span")}
    stats.random_graphs++;
  }
  const E1=[[0,1,1,0],[2,3,1,1],[3,4,1,0],[4,2,1,0]];
  let A=solve(5,E1,3n,1);verify(E1,3n,A);insist(A[1].c===4,"disconnected cycle");stats.hostile.push({case:"odd closed walk in different component",optimum:A[1].c});
  const E2=[[0,1,1,1],[1,2,1,0],[2,0,1,0],[3,4,1,2],[4,5,1,0],[5,3,1,0]];
  A=solve(6,E2,0n,2);verify(E2,0n,A);insist(A[3].c===6,"two independent cycle tags");stats.hostile.push({case:"two cycles necessary for two-bit target",optimum:A[3].c});
  for(const k of [4,8,12,16]){
    const E=[];for(let u=0;u<=k;u++)for(let v=u+1;v<=k;v++)E.push([u,v,1,0]);for(let i=0;i<k;i++)E.push([i?k+i:0,k+i+1,1,0]);
    const n=2*k+1,T=bit(0)^bit(2*k),lo=affine(n,E,T,k-1),tight=affine(n,E,T,k+2),loose=affine(n,E,T,k+3),r=k*(k-1)/2;
    insist(!lo&&tight.W.rank()===0&&loose.W.rank()===r,"scaling ranks");
    stats.scaling.push({k,vertices:n,edges:E.length,dictionary_nullity:r,unsat_budget:k-1,tight_budget:k+2,tight_rank:0,loose_budget:k+3,loose_rank:r,probes:tight.probes+loose.probes});
  }
  return stats;
}
console.log(JSON.stringify(runM05(),null,2));
