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

 const range=n=>Array.from({length:n},(_,i)=>i),zeros=n=>new Uint8Array(n*n),ones=n=>zeros(n).fill(1);
 const permGraph=(p,n)=>{let a=zeros(n);p.forEach((j,i)=>a[i*n+j]=1);return a};
 function brute(a,n){function f(i,used){if(i===n)return true;for(let j=0;j<n;j++)if(a[i*n+j]&&!(used>>j&1)&&f(i+1,used|1<<j))return true;return false}return f(0,0)}
 // B: positive cover padding.
 function cover(Z,n){let mz=matching(Z,n),rl=new Uint8Array(n),rr=new Uint8Array(n),Q=[];for(let i=0;i<n;i++)if(mz.left[i]<0){rl[i]=1;Q.push(i)}
 for(let h=0;h<Q.length;h++){let i=Q[h];for(let j=0;j<n;j++)if(Z[i*n+j]&&mz.left[i]!==j&&!rr[j]){rr[j]=1;let u=mz.right[j];if(u>=0&&!rl[u]){rl[u]=1;Q.push(u)}}}
 let R=range(n).filter(i=>!rl[i]),C=range(n).filter(j=>rr[j]);ck(R.length+C.length===mz.size);return {R,C}}
 function pad(Z,n,R,C){let rs=new Set(R),cs=new Set(C);ck(Z.every((v,id)=>!v||rs.has(Math.floor(id/n))||cs.has(id%n)));
 let V=range(n).filter(j=>!cs.has(j)).slice(0,R.length),U=range(n).filter(i=>!rs.has(i)).slice(0,C.length);
 ck(V.length===R.length&&U.length===C.length);let vr=new Set(V),ur=new Set(U),rows=range(n).filter(i=>!rs.has(i)&&!ur.has(i)),cols=range(n).filter(j=>!cs.has(j)&&!vr.has(j));ck(rows.length===cols.length);
 return {m:rows.length,embed:x=>{let y=Z.slice();R.forEach((i,k)=>y[i*n+V[k]]=1);U.forEach((i,k)=>y[i*n+C[k]]=1);rows.forEach((i,k)=>cols.forEach((j,l)=>y[i*n+j]=x[k*cols.length+l]));ck(Z.every((v,id)=>!v||y[id]));return y}}}
 // C: independently exhaust cover and matching labels.
 let exhaustive=0,coverChecks=0;
 for(let n=1;n<=3;n++)for(let z=0;z<1<<(n*n);z++){let Z=Uint8Array.from({length:n*n},(_,i)=>z>>i&1),{R,C}=cover(Z,n),best=2*n;
 for(let r=0;r<1<<n;r++)for(let c=0;c<1<<n;c++)if(Z.every((v,id)=>!v||((r>>Math.floor(id/n)&1)||(c>>(id%n)&1))))best=Math.min(best,pc(r)+pc(c));ck(best===R.length+C.length);coverChecks++;
 let w=pad(Z,n,R,C),m=w.m;for(let b=0;b<1<<(m*m);b++){let x=Uint8Array.from({length:m*m},(_,i)=>b>>i&1);ck(brute(w.embed(x),n)===brute(x,m));exhaustive++}}
 let bad=zeros(3);bad[1]=bad[3]=bad[8]=1;ck(brute(bad,3));ck(!brute(Uint8Array.from([0,0,0,1]),2));let pin=zeros(3);pin[1]=pin[3]=1;let pad0=pad(pin,3,[0],[0]);ck(pad0.m===1&&!brute(pad0.embed(Uint8Array.of(0)),3)&&brute(pad0.embed(Uint8Array.of(1)),3));
 // A: explicitly encoded CNF block queries, each <=13 literal clause is one local table.
 let queryEvals=0,totalMapCells=0;
 const fixed=t=>[...Array(t).fill(-2),...Array(16-t).fill(-1)];
 function map(n,p,trigger){let cells=[],groups=[];for(let i=0;i<n;i+=6){let rs=range(Math.min(6,n-i)).map(j=>i+j),cs=rs.map(j=>p[j]),s=rs.length;groups.push({rs,cs});for(let u=1;u<1<<s;u++)for(let v=1;v<1<<s;v++)if(pc(u)+pc(v)===s+1){let ids=[];rs.forEach((r,j)=>{if(u>>j&1)cs.forEach((c,l)=>{if(v>>l&1)ids.push(r*n+c)})});ck(ids.length<=13);cells.push([-2,-2,-2,...ids,...Array(13-ids.length).fill(-1)])}}
 // Impossible north cell makes G=0 on every query. Fixed overflow or literal-trigger overflow.
 let c=Array(16).fill(-1);[8,9,10,11].forEach(w=>c[w]=-2);cells.unshift(c);let overflowCell=cells.length;
 let t=fixed(trigger===null?5:4);if(trigger!==null)t[4]=trigger;cells.push(t);let k=Math.ceil(Math.sqrt(cells.length));while(cells.length<k*k)cells.push(fixed(4));totalMapCells+=cells.length;return {cells,k,groups,overflowCell}}
 function evalMap(M,a){queryEvals++;let g=M.cells.map(row=>row.reduce((v,id,w)=>v|((id===-2||(id>=0&&a[id]))?1<<w:0),0));let A=g.every(m=>pc(m)>=4),B=g.some(m=>pc(m)>4);return {g,A,B,F:A&&B}}
 function rowLists(M,n){let top=evalMap(M,ones(n)),E=new Set;ck(top.F&&pc(top.g[M.overflowCell])>=5);M.cells[M.overflowCell].filter(id=>id!==-1).slice(0,5).filter(id=>id>=0).forEach(id=>E.add(Math.floor(id/n)));let lists=[];for(let i=0;i<n;i++){let y=ones(n);for(let j=0;j<n;j++)y[i*n+j]=0;let u=evalMap(M,y);ck(!u.F);if(E.has(i))continue;ck(u.B&&!u.A);let c=u.g.findIndex(m=>pc(m)<4);let z=range(16).filter(w=>!(u.g[c]>>w&1)).slice(0,13).map(w=>M.cells[c][w]).filter(id=>id>=0);ck(z.every(id=>Math.floor(id/n)===i));lists.push({i,js:[...new Set(z.map(id=>id%n))]})}return {E,lists}}
 const oldHashes=[
 ["7e83ab6f2764c2bedaa35682bde2f98c40f74625775b564346d832f02c71d233","ebddeb27fd9d5145278a51086b8ba8179d17f8654179ed5f7b852b57f579c6b7"],
 ["cd679e6596dda7b7c260c8ce4cfbd1f06aac689262e9c597320742a0d3a27181","0107602e2c0c2b8deeae8b2b4c12befb626b485d015f708f287df92b5c17c9be"],
 ["27473838dfb0216cd20a0806a5bfe3ef5e42ee65acbbb02df3d4caeeeda52c69","21571134145b36ae02f677a307304218ec7f95e3b10d65ac9f6a2d5e07ec5bef"],
 ["9fb9b0a717405da5f6ecf35858726fcf05af0729ca719b895e7a4648aef5fa90","f7512a8e6a4bb3820d275f3a52b17c799ee1d2d3fdfc9b3e7c1d997311496d35"],
 ["dc19c8eac7e9ceb0cf7394d6f5d56f9ea38458487d1756d138837a71dd68c4dc","2b6578ef431a10d192535b443aa8eb539cdfb422ee30672f3f0a59680c4fbb61"]];
 let large=[],actualLifts=0,paddedLabels=0,permutationTrials=0;
 for(let [ni,n] of [14,16,32,64,128].entries()){
 let {a,b}=hall(n),ga=grid(a,n),gb=grid(b,n),hashes=[sha(ga),sha(gb)];ck(hashes.every((h,i)=>h===oldHashes[ni][i]));let ca=close(ga,n+2),cb=close(gb,n+2);ck(ca.ok&&cb.ok);ck(close(ca.d,n+2).removed===0&&close(cb.d,n+2).removed===0);
 let pm=matching(b,n);ck(matching(a,n).size<n&&pm.size===n&&verifyPM(b,n,pm.left)&&verify(gb,witness(pm.left,n),n+2));actualLifts++;
 let maps=[];for(let trigger of [null,pm.left[0]]){let M=map(n,pm.left,trigger),L=rowLists(M,n);ck(!evalMap(M,a).F&&evalMap(M,b).F);ck(L.E.size<=(trigger===null?0:1));let maxList=Math.max(...L.lists.map(x=>x.js.length));ck(maxList<=13);
 for(let shift=0;shift<12;shift++){let p=Array.from(pm.left);for(let {rs,cs} of M.groups)rs.forEach((i,j)=>p[i]=cs[(j+shift)%cs.length]);let x=permGraph(p,n),v=evalMap(M,x);ck(verifyPM(x,n,p)&&verify(grid(x,n),witness(p,n),n+2));actualLifts++;if(v.F)ck(L.lists.every(({i,js})=>js.includes(p[i])));if(trigger===null)ck(v.F);let y=x.slice();y[p[0]]=0;ck(!evalMap(M,y).F&&matching(y,n).size<n);permutationTrials+=2}
 maps.push({cells:M.cells.length,exceptionRows:L.E.size,maxList,rowsCertified:L.lists.length,trigger})}
 let restrictions=[];for(let kind of ["star","cross","dispersed"]){let Z=zeros(n);if(kind==="star"||kind==="cross")for(let j=0;j<n;j++)Z[j]=1;if(kind==="cross")for(let i=0;i<n;i++)Z[i*n]=1;if(kind==="dispersed")for(let i=0;i<Math.floor(n/4);i++)Z[i*n+i]=1;
 let {R,C}=cover(Z,n),w=pad(Z,n,R,C);ck(w.m===n-R.length-C.length);if(kind==="star")ck(w.m===n-1);if(kind==="cross")ck(w.m===n-2);let {a:x,b:y}=hall(w.m);
 for(let [v,label] of [[x,false],[y,true]]){let g=w.embed(v),mm=matching(g,n);ck((mm.size===n)===label);ck((matching(v,w.m).size===w.m)===label);let ng=grid(g,n),cc=close(ng,n+2);if(label){ck(cc.ok&&verifyPM(g,n,mm.left)&&verify(ng,witness(mm.left,n),n+2));actualLifts++}if(cc.ok)ck(close(cc.d,n+2).removed===0);paddedLabels++}
 restrictions.push({kind,pins:Z.reduce((s,v)=>s+v,0),cover:R.length+C.length,retained:w.m})}
 large.push({n,nativeCells:(n+2)**2,hashes,maps,restrictions})}
 return {checks,matchCalls,closureScans,queryEvals,totalMapCells,exhaustive,coverChecks,paddedLabels,actualLifts,permutationTrials,large,scope:"Sequential replicas. Initial attempt assertion 7888 failed: selected first overflowing clause rather than designated low-support overflow cell; fixed witness selection and reran. Inherited source grid and closure, independent exhaustive cover and permutation checks. No general F oracle: query G always NO due fixed north cell, F evaluated with A and B. No independent Lean build."}
}

console.log(JSON.stringify(audit(),null,2));
