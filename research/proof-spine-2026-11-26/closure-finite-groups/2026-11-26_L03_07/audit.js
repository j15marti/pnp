function audit(){
  let checks=0,matchCalls=0,closureScans=0,gridEvals=0;
  const ck=(x)=>{checks++;if(!x)throw Error("assertion "+checks)};
  const pc=x=>{let s=0;while(x){x&=x-1;s++}return s};
  const mask=f=>{let z=0;for(let w=0;w<16;w++)if(f(w>>3&1,w>>2&1,w>>1&1,w&1))z|=1<<w;return z};
  const B=mask((N,E,S,W)=>N===S&&E===W),INC=1<<6;
  function matching(a,n){
    matchCalls++;const right=new Int32Array(n).fill(-1);
    function dfs(i,v){for(let j=0;j<n;j++)if(a[i*n+j]&&!v[j]){v[j]=1;if(right[j]<0||dfs(right[j],v)){right[j]=i;return true}}return false}
    let size=0;for(let i=0;i<n;i++)if(dfs(i,new Uint8Array(n)))size++;
    let left=new Int32Array(n).fill(-1);for(let j=0;j<n;j++)if(right[j]>=0)left[right[j]]=j;
    return {size,left,right};
  }
  const verifyPM=(a,n,p)=>p.length===n&&new Set(p).size===n&&Array.from(p).every((j,i)=>j>=0&&j<n&&a[i*n+j]===1);
  function grid(a,n){let k=n+2,g=[];for(let i=0;i<k;i++)for(let j=0;j<k;j++)g.push(i<n&&j>0&&j<=n?B|(a[i*n+j-1]?INC:0):j===0?mask((N,E,S,W)=>E===0&&(i===k-1?S===1:N===S)):j===k-1?mask((N,E,S,W)=>W===(i<n?1:0)&&(i===k-1?S===1:N===S)):B);return g}
  function witness(p,n){let k=n+2,inv=new Int32Array(n),z=[];p.forEach((j,i)=>inv[j]=i);for(let i=0;i<k;i++)for(let j=0;j<k;j++){let N=0,E=0,S=0,W=0;if(i<n&&j>0&&j<=n){let c=j-1;N=+(inv[c]<i);S=+(inv[c]<=i);W=+(p[i]<c);E=+(p[i]<=c)}else if(j===0||j===k-1){W=+(j===k-1&&i<n);S=+(i===k-1)}else{N=S=1}z.push(8*N+4*E+2*S+W)}return z}
  function verify(g,z,k){return z.every((w,t)=>{let i=Math.floor(t/k),j=t%k;return !!(g[t]>>w&1)&&(!i?!(w>>3&1):(z[t-k]>>1&1)===(w>>3&1))&&(i!==k-1||!!(w>>1&1))&&(!j||(z[t-1]>>2&1)===(w&1))})}
  function close(g,k){let d=g.slice(),Q=Array.from({length:g.length},(_,i)=>i),live=new Uint8Array(g.length).fill(1),scans=0,removed=0;const sup=(m,p)=>{let s=0;for(let w=0;w<16;w++)if(m>>w&1)s|=1<<(w>>p&1);return s};for(let h=0;h<Q.length;h++){let t=Q[h],i=Math.floor(t/k),j=t%k;live[t]=0;scans++;if(scans>65*g.length)throw Error("closure cap");let nb=[i?t-k:-1,j<k-1?t+1:-1,i<k-1?t+k:-1,j?t-1:-1],a=[i?sup(d[t-k],1):1,j<k-1?sup(d[t+1],0):3,i<k-1?sup(d[t+k],3):2,j?sup(d[t-1],2):3],m=d[t];for(let w=0;w<16;w++)if(m>>w&1)if(!a.every((s,p)=>s>>(w>>(3-p)&1)&1))m&=~(1<<w);if(m!==d[t]){removed+=pc(d[t])-pc(m);d[t]=m;if(!m){closureScans+=scans;return {ok:false,scans,removed}}for(let s of nb)if(s>=0&&!live[s]){live[s]=1;Q.push(s)}}}closureScans+=scans;return {ok:true,scans,removed,d}}
  function sha(g){
    const K=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
    let H=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19],len=2*g.length,b=new Uint8Array(Math.ceil((len+9)/64)*64);g.forEach((m,i)=>{b[2*i]=m&255;b[2*i+1]=m>>>8});b[len]=128;let dv=new DataView(b.buffer);dv.setUint32(b.length-4,len*8);
    let W=new Uint32Array(64),rot=(x,n)=>(x>>>n)|(x<<(32-n));for(let off=0;off<b.length;off+=64){for(let j=0;j<16;j++)W[j]=dv.getUint32(off+4*j);for(let j=16;j<64;j++){let x=W[j-15],y=W[j-2];W[j]=(W[j-16]+(rot(x,7)^rot(x,18)^(x>>>3))+W[j-7]+(rot(y,17)^rot(y,19)^(y>>>10)))>>>0}let [a,c,d,e,f,h,i,j]=H;for(let t=0;t<64;t++){let T1=(j+(rot(f,6)^rot(f,11)^rot(f,25))+((f&h)^(~f&i))+K[t]+W[t])>>>0,T2=((rot(a,2)^rot(a,13)^rot(a,22))+((a&c)^(a&d)^(c&d)))>>>0;j=i;i=h;h=f;f=(e+T1)>>>0;e=d;d=c;c=a;a=(T1+T2)>>>0}H=H.map((v,t)=>(v+[a,c,d,e,f,h,i,j][t])>>>0)}return H.map(v=>v.toString(16).padStart(8,"0")).join("");
  }
  const hall=(n)=>{let a=Uint8Array.from({length:n*n},(_,p)=>+(Math.floor(p/n)>=3||p%n<2)),b=a.slice();b[2*n+2]=1;return {a,b}};
  const rect=(n,S,T)=>{let z=new Uint8Array(n*n);for(let i of S)for(let j of T)z[i*n+j]=1;return z};
  function directHallLift(n,S,T,i,j){let p=new Int32Array(n).fill(-1),A=Array.from({length:n},(_,v)=>v).filter(v=>!S.includes(v)),D=Array.from({length:n},(_,v)=>v).filter(v=>!T.includes(v));p[i]=j;S.filter(v=>v!==i).forEach((v,t)=>p[v]=D[t]);A.forEach((v,t)=>p[v]=T.filter(w=>w!==j)[t]);return p}
  function Fknown(g,baselineNo){gridEvals++;if(g.some(m=>pc(m)<4))return false;if(g.some(m=>pc(m)>4))return true;if(!baselineNo)throw Error("unpaid G call");return false}
  const qHall=(a,C,n)=>grid(Uint8Array.from(a,(x,i)=>x&C[i]),n);
  const qDef=(a,id,base)=>{let g=base.slice();g[1]=(B&~1)|(a[id]?((1<<1)|(1<<2)):0);return g};
  // A and C separately: exact Hall conjunctive representation, independent permutations and maximality.
  const small=[];
  for(let n=2;n<=4;n++){let M=1<<(n*n),clauses=[],perms=[];for(let s=1;s<(1<<n);s++)for(let t=1;t<(1<<n);t++)if(pc(s)+pc(t)===n+1){let z=0;for(let i=0;i<n;i++)for(let j=0;j<n;j++)if((s>>i&1)&&(t>>j&1))z|=1<<(i*n+j);clauses.push(z)}
    function rec(i,used,z){if(i===n){perms.push(z);return}for(let j=0;j<n;j++)if(!(used>>j&1))rec(i+1,used|1<<j,z|1<<(i*n+j))}rec(0,0,0);
    let labels=new Uint8Array(M),positive=0;for(let a=0;a<M;a++){labels[a]=+perms.some(p=>(a&p)===p);positive+=labels[a];ck(clauses.every(C=>!!(C&a))===!!labels[a])}
    let maxima=[];for(let a=0;a<M;a++)if(!labels[a]){let maximal=true;for(let i=0;i<n*n;i++)if(!(a>>i&1)&&!labels[a|1<<i]){maximal=false;break}if(maximal)maxima.push(a)}
    let seen=new Set();for(let a of maxima){let rejects=clauses.filter(C=>!(C&a));ck(rejects.length===1);seen.add(rejects[0])}ck(seen.size===clauses.length);
    small.push({n,allInputs:M,positive,maximalNO:maxima.length,clauses:clauses.length});
  }
  // B: exact zero-certificate restriction via matching and minimum vertex cover.
  function kill(n,Z){let avoid=Uint8Array.from(Z,x=>1-x),p=matching(avoid,n);if(p.size<n)return {admitted:false};
    let mz=matching(Z,n),rl=new Uint8Array(n),rr=new Uint8Array(n),Q=[];for(let i=0;i<n;i++)if(mz.left[i]<0){rl[i]=1;Q.push(i)}
    for(let h=0;h<Q.length;h++){let i=Q[h];for(let j=0;j<n;j++)if(Z[i*n+j]&&mz.left[i]!==j&&!rr[j]){rr[j]=1;let v=mz.right[j];if(v>=0&&!rl[v]){rl[v]=1;Q.push(v)}}}
    let cl=Array.from(rl,x=>1-x),cr=Array.from(rr),cover=cl.reduce((s,x)=>s+x,0)+cr.reduce((s,x)=>s+x,0);ck(cover===mz.size);
    for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(Z[i*n+j])ck(cl[i]||cr[j]);
    ck(verifyPM(avoid,n,p.left));let gone=[],rows=[],cols=[];for(let i=0;i<n;i++){if(cl[i]||cr[p.left[i]])gone.push(i);else{rows.push(i);cols.push(p.left[i])}}ck(gone.length<=cover);
    function embed(x){let a=new Uint8Array(n*n);for(let i of gone)a[i*n+p.left[i]]=1;for(let i=0;i<rows.length;i++)for(let j=0;j<cols.length;j++)a[rows[i]*n+cols[j]]=x[i*cols.length+j];ck(Z.every((v,t)=>!v||!a[t]));return a}
    return {admitted:true,cover,removed:gone.length,m:rows.length,embed};
  }
  const oldHashes=[
    ["7e83ab6f2764c2bedaa35682bde2f98c40f74625775b564346d832f02c71d233","ebddeb27fd9d5145278a51086b8ba8179d17f8654179ed5f7b852b57f579c6b7"],
    ["cd679e6596dda7b7c260c8ce4cfbd1f06aac689262e9c597320742a0d3a27181","0107602e2c0c2b8deeae8b2b4c12befb626b485d015f708f287df92b5c17c9be"],
    ["27473838dfb0216cd20a0806a5bfe3ef5e42ee65acbbb02df3d4caeeeda52c69","21571134145b36ae02f677a307304218ec7f95e3b10d65ac9f6a2d5e07ec5bef"],
    ["9fb9b0a717405da5f6ecf35858726fcf05af0729ca719b895e7a4648aef5fa90","f7512a8e6a4bb3820d275f3a52b17c799ee1d2d3fdfc9b3e7c1d997311496d35"],
    ["dc19c8eac7e9ceb0cf7394d6f5d56f9ea38458487d1756d138837a71dd68c4dc","2b6578ef431a10d192535b443aa8eb539cdfb422ee30672f3f0a59680c4fbb61"]];
  const large=[],ns=[14,16,32,64,128];let qTrials=0,paddedLabels=0,adversarialNeighbors=0;
  const binom=(n,k)=>{let x=1n;for(let i=1;i<=k;i++)x=x*BigInt(n-i+1)/BigInt(i);return x.toString()};
  for(let ni=0;ni<ns.length;ni++){let n=ns[ni],k=n+2,{a,b}=hall(n),ga=grid(a,n),gb=grid(b,n),hashes=[sha(ga),sha(gb)];ck(hashes.every((h,i)=>h===oldHashes[ni][i]));let ca=close(ga,k),cb=close(gb,k);ck(ca.ok&&cb.ok);ck(close(ca.d,k).removed===0);ck(close(cb.d,k).removed===0);
    let p=matching(b,n);ck(matching(a,n).size<n&&p.size===n&&verifyPM(b,n,p.left)&&verify(gb,witness(p.left,n),k));
    const base=grid(new Uint8Array(n*n),n);ck(base.every(m=>pc(m)===4));ck(!close(base,k).ok);
    let S=[0,1,2],T=Array.from({length:n-2},(_,i)=>i+2),C=rect(n,S,T);ck(!Fknown(qHall(a,C,n),true)&&Fknown(qHall(b,C,n),true));qTrials+=2;
    for(const [i,j] of [[0,2],[1,n-1],[2,2]]){let x=a.slice();x[i*n+j]=1;let w=directHallLift(n,S,T,i,j);ck(verifyPM(x,n,w)&&verify(grid(x,n),witness(w,n),k));adversarialNeighbors++}
    // Explicit incomplete conjunctive query: choose cyclic matching avoiding its pin.
    let id=2*n+2,shift=1,cyc=Uint8Array.from({length:n*n},(_,t)=>+(t%n===(Math.floor(t/n)+shift)%n));let cp=Int32Array.from({length:n},(_,i)=>(i+shift)%n);
    ck(verifyPM(cyc,n,cp)&&verify(grid(cyc,n),witness(cp,n),k));ck(!Fknown(qDef(cyc,id,base),true));qTrials++;
    const cases=[];for(let kind of ["small","star","isolating"]){let Z=new Uint8Array(n*n),ids=[];
      if(kind==="small"){for(let i=0;i<Math.max(1,Math.floor(n/26));i++)ids.push(i*n+(i+3)%n)}
      else for(let j=0;j<(kind==="star"?n-1:n);j++)ids.push(j);
      ids.forEach(id=>Z[id]=1);let z=kill(n,Z);
      // Same initial pair, independent query evaluation before sharing restriction.
      for(let x of [a,b])for(let id of ids){ck(Fknown(qDef(x,id,base),true)===!!x[id]);qTrials++}
      if(kind==="isolating"){ck(!z.admitted);cases.push({kind,queries:ids.length,admitted:false});continue}
      ck(z.admitted);if(kind==="star")ck(z.cover===1&&z.m>=n-1);
      let {a:u,b:v}=hall(z.m),zero=new Uint8Array(z.m*z.m),diag=Uint8Array.from({length:z.m*z.m},(_,i)=>+(Math.floor(i/z.m)===i%z.m));
      for(const [x,label] of [[u,false],[v,true],[zero,false],[diag,true]]){let y=z.embed(x),p=matching(y,n);ck((p.size===n)===label);ck((matching(x,z.m).size===z.m)===label);
        for(let id of ids){ck(!Fknown(qDef(y,id,base),true));qTrials++}
        let g=grid(y,n),c=close(g,k);if(label){ck(c.ok&&verifyPM(y,n,p.left)&&verify(g,witness(p.left,n),k))}if(c.ok)ck(close(c.d,k).removed===0);paddedLabels++;
      }cases.push({kind,queries:ids.length,admitted:true,cover:z.cover,removed:z.removed,retained:z.m});
    }
    large.push({n,gridCells:k*k,encodedBits:16*k*k,hashes,noSurvivesClosure:ca.ok,exactConjunctiveBound:binom(2*n,n+1),cases});
  }
  return {checks,matchCalls,closureScans,gridEvals,qTrials,paddedLabels,adversarialNeighbors,small,large,scope:"Three independently written interleaved methods in one JS execution; same L03-06 original indexed Hall pairs and masks authenticated by SHA256. Fknown only calls G on certified all-zero baseline NO, or short-circuits A/B; no general F oracle. All guards restricted copies only. Large Hall query family not enumerated; exact count symbolic. No arbitrary circuit synthesis, TM simulation or Lean build."};
}
console.log(JSON.stringify(audit(),null,2));
