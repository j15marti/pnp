const experiment = function experiment(){
  const mod=(x,p)=>((x%p)+p)%p; let seed=2611270549;
  function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
  function perm(n){let a=Array.from({length:n},(_,i)=>i);for(let i=n-1;i>0;i--){let j=rand(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
  function matching(n,edges){
    const adj=Array.from({length:n},()=>[]);for(const [i,j] of edges)adj[i].push(j);
    const m=Array(n).fill(-1);let scans=0;
    function aug(i,seen){for(const j of adj[i]){scans++;if(seen[j])continue;seen[j]=true;if(m[j]<0||aug(m[j],seen)){m[j]=i;return true}}return false}
    for(let i=0;i<n;i++)aug(i,Array(n).fill(false));
    const left=new Set(m.filter(i=>i>=0)),R=new Set(),C=new Set(),q=[];
    for(let i=0;i<n;i++)if(!left.has(i)){R.add(i);q.push(i)}
    for(let t=0;t<q.length;t++){let i=q[t];for(const j of adj[i]){scans++;if(m[j]===i||C.has(j))continue;C.add(j);if(m[j]>=0&&!R.has(m[j])){R.add(m[j]);q.push(m[j])}}}
    const coverR=Array.from({length:n},(_,i)=>i).filter(i=>!R.has(i)),coverC=[...C];
    if(edges.some(([i,j])=>!coverR.includes(i)&&!coverC.includes(j))||coverR.length+coverC.length!==left.size)throw Error("cover");
    return {size:left.size,coverR,coverC,scans};
  }
  function certify(n,T,v){
    const pos=[],neg=[];for(const [i,j,z] of T){let w=mod(v[2*n+z]-v[i]-v[n+j],4);if(w===2)return null;if(w===1)pos.push([i,j]);if(w===3)neg.push([i,j]);}
    let P=matching(n,pos),Q=matching(n,neg),delta=mod(v.slice(2*n).reduce((a,b)=>a+b,0)-v.slice(0,2*n).reduce((a,b)=>a+b,0),4);
    for(let k=-Q.size;k<=P.size;k++)if(mod(k,4)===delta)return null;
    return {v,delta,lo:-Q.size,hi:P.size,P,Q};
  }
  function independentCheck(n,T,cert){
    let {v,delta,lo,hi,P,Q}=cert;
    if(v.length!==3*n||v.some(x=>!Number.isInteger(x)||x<0||x>3))throw Error("v");
    for(const [i,j,z] of T){let w=mod(v[2*n+z]-v[i]-v[n+j],4);
      if(w===2||w===1&&!P.coverR.includes(i)&&!P.coverC.includes(j)||w===3&&!Q.coverR.includes(i)&&!Q.coverC.includes(j))throw Error("edge uncovered");}
    if(hi!==P.coverR.length+P.coverC.length||lo!==-Q.coverR.length-Q.coverC.length||delta!==mod(v.slice(2*n).reduce((a,b)=>a+b,0)-v.slice(0,2*n).reduce((a,b)=>a+b,0),4))throw Error("certificate");
    for(let k=lo;k<=hi;k++)if(mod(k,4)===delta)throw Error("residue");
  }
  function gluing(n,L,T){
    const groups=[];let comparisons=0,maps=0;
    const pair=Array.from({length:n},()=>Array(n).fill(null));
    for(let a=0;a<n;a++)for(let b=0;b<n;b++)if(a!==b){
      const p=[];for(let j=0;j<n;j++)if(L[a][j].length===1&&L[b][j].length===1)p.push([L[a][j][0],L[b][j][0]]);
      if(p.length<=n/2)return {status:"UNKNOWN",maps,comparisons};
      let g=groups.find(g=>{for(const [z,w] of p){comparisons++;if(g[z]!==-1&&g[z]!==w)return false}return true});
      if(!g){g=Array(n).fill(-1);groups.push(g)}
      for(const [z,w] of p)g[z]=w;pair[a][b]=g;maps++;
      if(groups.length>=n)return {status:"UNKNOWN",maps,comparisons};
    }
    if(groups.length!==n-1||groups.some(g=>g.includes(-1)||new Set(g).size!==n))return {status:"UNKNOWN",maps,comparisons};
    let trials=0;
    for(const g of groups){
      let labels=Array(n).fill(-1),z=0,k=0;while(labels[z]===-1){labels[z]=k++;z=g[z]}
      if(k!==n)continue;
      const u=Array(n).fill(0);for(let i=1;i<n;i++)u[i]=mod(labels[pair[0][i][0]]-labels[0],n);
      const v=[];for(let j=0;j<n;j++){let i=L.findIndex(row=>row[j].length===1);if(i<0)return {status:"UNKNOWN",maps,comparisons};v.push(mod(labels[L[i][j][0]]-u[i],n))}
      trials++;let c=certify(n,T,[...u,...v,...labels].map(x=>x%4));if(c)return {status:"UNSAT",maps,comparisons,trials,c};
    }
    return {status:"UNKNOWN",maps,comparisons,trials};
  }
  function algebra(n,L,T){
    const rows=[];const ids=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(L[i][j].length===1){let a=[i,n+j,2*n+L[i][j][0]];ids.push(a);rows.push(a.reduce((s,k)=>s|(1n<<BigInt(k)),0n))}
    const D=3*n;
    // Row operations carried out on RHS as well; solve all binary lifts, cap nullity 3.
    function solve(rhs){
      let A=rows.slice(),B=rhs.slice(),piv=[],r=0,ops=0;
      for(let k=0;k<D;k++){let bit=1n<<BigInt(k),i=r;while(i<A.length&&!(A[i]&bit)){i++;ops++}if(i===A.length)continue;
        [A[r],A[i]]=[A[i],A[r]];[B[r],B[i]]=[B[i],B[r]];
        for(let j=0;j<A.length;j++)if(j!==r){ops++;if(A[j]&bit){A[j]^=A[r];B[j]^=B[r]}}
        piv.push(k);r++;
      }
      const free=Array.from({length:D},(_,i)=>i).filter(i=>!piv.includes(i));
      if(free.length>3)return {free:free.length,ops,solutions:[]};
      if(B.slice(r).some(x=>x))return {free:free.length,ops,solutions:[]};
      const solutions=[];for(let mask=0;mask<(1<<free.length);mask++){let x=Array(D).fill(0);free.forEach((k,i)=>x[k]=(mask>>i)&1);
        for(let i=0;i<r;i++){let b=B[i];for(const k of free)if(A[i]&(1n<<BigInt(k)))b^=x[k];x[piv[i]]=b}solutions.push(x)}
      return {free:free.length,ops,solutions};
    }
    let first=solve(rows.map(()=>0)),ops=first.ops,trials=0,lifts=0;
    for(const x of first.solutions){let rhs=ids.map(([i,j,z])=>mod((x[i]+x[j]-x[z])/2,2));let second=solve(rhs);ops+=second.ops;lifts+=second.solutions.length;
      for(const y of second.solutions){let v=x.map((b,i)=>b+2*y[i]);if(ids.some(([i,j,z])=>mod(v[z]-v[i]-v[j],4)!==0))throw Error("lift");trials++;let c=certify(n,T,v);if(c)return {status:"UNSAT",nullity:first.free,ops,trials,lifts,c}}
    }
    return {status:"UNKNOWN",nullity:first.free,ops,trials,lifts};
  }
  const out=[];for(const n of [12,20,28,36,60]){
    const R=perm(n),C=perm(n),Z=perm(n);const extras=Array.from({length:n},(_,i)=>[i,i,mod(2*i+4,n)]);extras.unshift([0,1,2]);
    const base=Array.from({length:n*n},(_,k)=>[Math.floor(k/n),k%n,mod(Math.floor(k/n)+k%n,n)]);
    for(const t of [0,1,1+Math.floor(n/2),n+1]){
      const T=[...base,...extras.slice(0,t)].map(([i,j,z])=>[R[i],C[j],Z[z]]);
      const L=Array.from({length:n},()=>Array.from({length:n},()=>[]));for(const [i,j,z] of T)L[i][j].push(z);
      const ambiguous=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(L[i][j].length>1)ambiguous.push([i,j]);
      let old=matching(n,ambiguous),A=gluing(n,L,T),B=algebra(n,L,T);
      if(A.status!=="UNSAT"||B.status!=="UNSAT")throw Error("failed "+n+" "+t);
      independentCheck(n,T,A.c);independentCheck(n,T,B.c);
      // independent original-coordinate proof; verify each original ID, no enumeration.
      let odd=0;for(const [i,j,z] of T){let w=mod(Z.indexOf(z)-R.indexOf(i)-C.indexOf(j),4);if(w!==0&&w!==1)throw Error("generator");odd+=w}
      if(odd>1||n%8!==4)throw Error("auth");
      let hash=2166136261;for(const a of T)for(const x of a)hash=Math.imul(hash^x,16777619)>>>0;
      out.push({n,t,triples:T.length,hash,oldCover:old.size,A:{...A,c:{delta:A.c.delta,lo:A.c.lo,hi:A.c.hi}},B:{...B,c:{delta:B.c.delta,lo:B.c.lo,hi:B.c.hi}},independentEdges:3*T.length});
    }
  }
  // Soundness hostile: n=4 with all triples contains explicit cover (i,i,i).
  const n=4,T=Array.from({length:64},(_,k)=>[k>>4,(k>>2)&3,k&3]);let bad=certify(n,T,Array(12).fill(0));if(bad)throw Error("false rejection");
  return {out,hostile:"zero-potential full-cube control not rejected; other candidates not tested",seed:2611270549}
};
console.log(JSON.stringify(experiment(),null,2));
