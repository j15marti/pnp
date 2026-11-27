function audit(){
 const out=[],mod=(a,n)=>((a%n)+n)%n,check=(x,m)=>{if(!x)throw Error(m)};
 let seed=2611270347>>>0;function rnd(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed}
 function perm(n){let a=Array.from({length:n},(_,i)=>i);for(let i=n-1;i>0;i--){let j=rnd()%(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
 function parent(n,kind){
  let R=perm(n),C=perm(n),Z=perm(n),e=[],add=(i,j,k)=>e.push([e.length,R[i],C[j],Z[k]]);
  for(let i=0;i<n;i++)for(let j=0;j<n;j++)add(i,j,(i+j)%n);
  if(kind==="diagonal"){for(let i=0;i<n/2-1;i++)add(i,mod(-i,n),1)}
  if(kind==="boundary"){for(let i=0;i<n/2;i++)add(i,i,(2*i+1)%n)}
  if(kind==="cross"){for(let j=0;j<n-2;j++)add(0,j,(j+1)%n);for(let i=1;i<n-2;i++)add(i,0,(i+1)%n);for(let j=n-2;j<n;j++)add(0,j,(j+1)%n);for(let i=n-2;i<n;i++)add(i,0,(i+1)%n)}
  let order=perm(e.length);return {n,kind,R,C,Z,edges:order.map(i=>e[i])}
 }
 function input(p,t){let e=p.edges.filter(x=>x[0]<p.n*p.n+t),n=p.n;let h=2166136261;for(let x of [n,t,...p.edges.flat()])h=Math.imul(h^x,16777619)>>>0;return {n,t,e,hash:h.toString(16).padStart(8,"0"),N:32+Math.ceil(Math.log2(n))*3*p.edges.length+p.edges.length}}
 function closure(F){let g=Array.from({length:3},()=>Array(F.n).fill(0));for(let e of F.e)for(let k=0;k<3;k++)g[k][e[k+1]]++;return g.every(a=>a.every(x=>x>=2))}
 // Constructive lane A: source-only candidate chart, elementary row/column capacities.
 // Hybrid H: import verified chart into positive-edge matching and dual cover.
 function search(F,erase,match){
  let n=F.n,stats={pairs:0,cycles:0,charts:0,edgeScans:0,augScans:0,erasures:0};let best=null;
  for(let transpose of [false,true]){
   let E=F.e.map(([id,r,c,z])=>[id,transpose?c:r,transpose?r:c,z]),T=Array.from({length:n},()=>Array.from({length:n},()=>[]));
   for(let [,r,c,z] of E)T[r][c].push(z);
   for(let omit of (erase?[-1,...Array.from({length:n},(_,i)=>i)]:[-1])){
    stats.erasures++;
    let rows=[];
    for(let i=0;i<n;i++){
     let a=Array(n).fill(-1),used=new Set(),ok=true;
     for(let j=0;j<n;j++)if(j!==omit){if(T[i][j].length!==1||used.has(T[i][j][0])){ok=false;break}a[j]=T[i][j][0];used.add(a[j])}
     if(ok&&omit>=0){let missing=Array.from({length:n},(_,k)=>k).find(k=>!used.has(k));if(!T[i][omit].includes(missing))ok=false;else a[omit]=missing}
     if(ok)rows.push([i,a]);
    }
    for(let [i,a] of rows)for(let [j,b] of rows)if(i!==j){
     stats.pairs++;
     let s=Array(n);for(let k=0;k<n;k++)s[a[k]]=b[k];
     let L=Array(n).fill(-1),cur=0,k=0;while(L[cur]===-1){L[cur]=k++;cur=s[cur]}
     if(k!==n||cur!==0)continue;
     stats.cycles++;
     let V=a.map(z=>L[z]),D=Array.from({length:n},()=>new Set());
     for(let [,r,c,z] of E){stats.edgeScans++;D[r].add(mod(L[z]-V[c],n))}
     let U=[],valid=true;
     for(let d of D){let a=[...d];if(a.length===1)U.push(a[0]);else if(a.length===2&&mod(a[1]-a[0],n)===1)U.push(a[0]);else if(a.length===2&&mod(a[0]-a[1],n)===1)U.push(a[1]);else{valid=false;break}}
     if(!valid)continue;
     stats.charts++;
     let A=Array.from({length:n},()=>new Set()),cols=new Set();
     for(let [,r,c,z] of E){stats.edgeScans++;let w=mod(L[z]-U[r]-V[c],n);check(w===0||w===1,"bad residual");if(w){A[r].add(c);cols.add(c)}}
     let delta=mod(L.reduce((a,b)=>a+b,0)-U.reduce((a,b)=>a+b,0)-V.reduce((a,b)=>a+b,0),n);
     let R=A.map((a,r)=>a.size?r:-1).filter(r=>r>=0),C=[...cols],simple=Math.min(R.length,C.length),bound=simple;
     let coverR=R,coverC=[];if(C.length<R.length){coverR=[];coverC=C}
     if(match&&simple>=delta&&delta!==0){
      // Maximum matching of positive-cost support, then Konig cover.
      let mr=Array(n).fill(-1),mc=Array(n).fill(-1);
      function aug(r,seen){for(let c of A[r]){stats.augScans++;if(seen[c])continue;seen[c]=true;if(mc[c]===-1||aug(mc[c],seen)){mc[c]=r;mr[r]=c;return true}}return false}
      for(let r=0;r<n;r++)aug(r,Array(n).fill(false));
      let zr=new Set(),zc=new Set(),queue=[];for(let r=0;r<n;r++)if(mr[r]===-1){zr.add(r);queue.push(r)}
      for(let q=0;q<queue.length;q++){let r=queue[q];for(let c of A[r]){stats.augScans++;if(mr[r]===c||zc.has(c))continue;zc.add(c);if(mc[c]>=0&&!zr.has(mc[c])){zr.add(mc[c]);queue.push(mc[c])}}}
      coverR=Array.from({length:n},(_,r)=>r).filter(r=>!zr.has(r));coverC=[...zc];bound=coverR.length+coverC.length;
      check(bound===mr.filter(r=>r>=0).length,"matching cover mismatch");
     }
     if(!best||bound<best.bound)best={bound,delta,simple,rows:R.length,cols:C.length};
     if(bound<delta){
      let cert={transpose,omit,pair:[i,j],L,U,V,coverR,coverC,bound,delta,simple,rows:R.length,cols:C.length};
      // Independent certificate replay on source IDs (no reconstructed table).
      let RR=new Set(coverR),CC=new Set(coverC);
      for(let [id,rr,cc,z] of F.e){stats.edgeScans++;let r=transpose?cc:rr,c=transpose?rr:cc,w=mod(L[z]-U[r]-V[c],n);check(w<=1&&(!w||RR.has(r)||CC.has(c)),"cover replay "+id)}
      check(coverR.length+coverC.length===bound&&bound<delta,"residue replay");
      return {status:"NO",stats,cert}
     }
    }
   }
  }
  return {status:"UNKNOWN",stats,best}
 }
 // Independent lane B: original-coordinate check, no learned chart and no matching routine.
 function planted(p,F){
  let n=F.n,R=Array(n),C=Array(n),Z=Array(n);
  p.R.forEach((x,i)=>R[x]=i);p.C.forEach((x,i)=>C[x]=i);p.Z.forEach((x,i)=>Z[x]=i);
  let rr=new Set(),cc=new Set(),positives=0;
  for(let [id,r,c,z] of F.e){let w=mod(Z[z]-R[r]-C[c],n);check(w===0||w===1,"planted weights");if(w){positives++;rr.add(r);cc.add(c);if(p.kind==="cross")check(R[r]===0||C[c]===0,"cross cover")}}
  let bound=p.kind==="cross"?Math.min(2,positives):positives;
  return {positives,rowBound:rr.size,colBound:cc.size,bound,delta:n/2,status:bound<n/2?"NO":"UNKNOWN",edgeScans:F.e.length}
 }
 // Independent lane C: direct labeled matching recursion, no modular data.
 function reference(F){
  if(F.n>8)return {status:"NOT_RUN",nodes:0};
  let n=F.n,A=Array.from({length:n},()=>[]);for(let e of F.e)A[e[1]].push(e);
  let nodes=0,cap=1000000,matchings=0,yes=null;
  function rec(r,cm,zm,ids){if(++nodes>cap)return;if(r===n){matchings++;if(zm===(1<<n)-1&&!yes)yes=ids.slice();return}for(let [id,,c,z] of A[r])if(!(cm>>c&1)){ids.push(id);rec(r+1,cm|(1<<c),zm|(1<<z),ids);ids.pop();if(nodes>cap)return}}
  rec(0,0,0,[]);return {status:yes?"YES":nodes>cap?"UNKNOWN":"NO",nodes,matchings,witness:yes}
 }
 for(let n of [8,12,16,32,64]){
  for(let kind of ["diagonal","cross"]){
   let p=parent(n,kind),ts=kind==="diagonal"?[0,n/2-1]:[0,n-2,2*n-5,2*n-1];
   for(let t of ts){
    let F=input(p,t);check(closure(F),"initial closure");
    let A=search(F,false,false),B=planted(p,F),C=reference(F),H=search(F,false,true),H1=H.status==="NO"?null:search(F,true,true);
    let cert=H.status==="NO"?H.cert:H1?.cert;
    check(B.status==="NO"&&(C.status==="NO"||C.status==="NOT_RUN")&&cert,"expected NO");
    check(closure(F),"closure after import");
    out.push({n,kind,t,edges:F.e.length,parentEncodedBits:F.N,hash:F.hash,A,B,C,H,H1});
   }
  }
 }
 for(let n of [8,16]){
  let p=parent(n,"boundary"),F=input(p,n/2),A=search(F,false,false),H=search(F,true,true),C=reference(F);
  let witness=[];for(let i=0;i<n;i++)witness.push(i<n/2?n*n+i:i*n+i);
  let ws=witness.map(id=>F.e.find(e=>e[0]===id));check([1,2,3].every(k=>new Set(ws.map(e=>e[k])).size===n),"YES witness");
  check(A.status==="UNKNOWN"&&H.status==="UNKNOWN","false reject");
  out.push({n,kind:"boundary",t:n/2,edges:F.e.length,hash:F.hash,A,H,C,witness});
 }
 // Padded permutation witness family: every source row, column and symbol is independently relabeled.
 return {seed:2611270347,results:out};
}
console.log(JSON.stringify(audit(),null,2));
