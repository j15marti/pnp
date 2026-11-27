function audit(){
 const assert=(b,msg)=>{if(!b)throw Error(msg)};
 let seed=307;
 const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 const perm=n=>{let a=Array.from({length:n},(_,i)=>i);for(let i=n-1;i>0;i--){let j=rnd(i+1);[a[i],a[j]]=[a[j],a[i]]}return a};
 // Factor M over Z/4: unit elimination, then GF(2) elimination of even tail.
 function factor(A,d){
  let M=A.map(a=>Uint8Array.from(a)),r=M.length,t=0,ops=[],ops2=[],piv=[],piv2=[],scans=0,updates=0;
  for(let j=0;j<d&&t<r;j++){
   let i=t;while(i<r&&!(M[i][j]&1)){i++;scans++}if(i===r)continue;
   if(i!==t){[M[i],M[t]]=[M[t],M[i]];ops.push([0,i,t,0])}
   if(M[t][j]===3){for(let l=0;l<d;l++)M[t][l]=(3*M[t][l])&3;ops.push([1,t,0,3]);updates+=d}
   for(i=t+1;i<r;i++){let c=M[i][j];scans++;if(c){for(let l=0;l<d;l++)M[i][l]=(M[i][l]-c*M[t][l])&3;ops.push([2,i,t,c]);updates+=d}}
   piv.push(j);t++;
  }
  for(let i=t;i<r;i++)for(let j=0;j<d;j++){assert(!(M[i][j]&1),"odd tail");M[i][j]>>=1}
  let u=t;
  for(let j=0;j<d&&u<r;j++){
   let i=u;while(i<r&&!M[i][j]){i++;scans++}if(i===r)continue;
   if(i!==u){[M[i],M[u]]=[M[u],M[i]];ops2.push([0,i,u,0])}
   for(i=u+1;i<r;i++){scans++;if(M[i][j]){for(let l=0;l<d;l++)M[i][l]^=M[u][l];ops2.push([2,i,u,1]);updates+=d}}
   piv2.push(j);u++;
  }
  function solve(b){
   let h=Uint8Array.from(b);
   for(let [a,i,j,c] of ops){if(a===0){[h[i],h[j]]=[h[j],h[i]]}else if(a===1)h[i]=(c*h[i])&3;else h[i]=(h[i]-c*h[j])&3}
   for(let i=t;i<r;i++){if(h[i]&1)return null;h[i]>>=1}
   for(let [a,i,j] of ops2){if(a===0){[h[i],h[j]]=[h[j],h[i]]}else h[i]^=h[j]}
   for(let i=u;i<r;i++)if(h[i])return null;
   let x=new Uint8Array(d);
   for(let i=u-1;i>=t;i--){let s=h[i];for(let j=0;j<d;j++)s^=M[i][j]&(x[j]&1);x[piv2[i-t]]=s}
   for(let i=t-1;i>=0;i--){let s=h[i];for(let j=0;j<d;j++)s=(s-M[i][j]*x[j])&3;x[piv[i]]=s}
   return x;
  }
  return {solve,unitRank:t,evenRank:u-t,scans,updates,ops:ops.length+ops2.length}
 }
 function verify(A,x,b){return A.every((a,i)=>a.reduce((s,v,j)=>s+v*x[j],0)%4===b[i])}
 let controls=0;
 for(let q=0;q<300;q++){
  let d=1+rnd(5),r=1+rnd(7),A=Array.from({length:r},()=>Array.from({length:d},()=>rnd(4))),b=Array.from({length:r},()=>rnd(4));
  let f=factor(A,d),x=f.solve(b),possible=false;
  for(let k=0;k<4**d;k++){let y=Array.from({length:d},(_,i)=>(k>>(2*i))&3);if(verify(A,y,b)){possible=true;break}}
  assert((x!==null)===possible&&(!x||verify(A,x,b)),"brute solver mismatch");controls++;
 }
 function gen(k,stage,n=12,def=true){
  let q=k*n,raw=[],add=(a,b,c,active=true)=>raw.push({id:raw.length,a,b,c,active});
  for(let h=0;h<k;h++)for(let i=0;i<n;i++)for(let j=0;j<n;j++)add(h*n+i,h*n+j,h*n+(i+j)%n);
  if(def)for(let h=0;h<k;h++)for(let j=0;j<n;j++)add(h*n,h*n+j,h*n+(j+1)%n);
  if(def)for(let h=0;h<k;h++)for(let i=0;i<n;i++)add(h*n+i,h*n+i,h*n+(2*i+4)%n,i<stage);
  for(let h=0;h<k-1;h++){let a=h*n,b=(h+1)*n;add(a,b,a);add(a,b,b);add(b,a,a);add(b,a,b)}
  // same permutations for all release stages
  let old=seed;seed=4321+k*97+n;let P=[perm(q),perm(q),perm(q)];seed=old;
  let E=raw.filter(e=>e.active).map(e=>({id:e.id,a:P[0][e.a],b:P[1][e.b],c:P[2][e.c]}));
  let hash=2166136261;for(let e of E)for(let v of [e.id,e.a,e.b,e.c])hash=Math.imul(hash^v,16777619)>>>0;
  return {q,n,k,raw,E,P,hash:hash.toString(16).padStart(8,"0")};
 }
 function incidence(E,q){let A=Array.from({length:3*q},()=>new Uint8Array(E.length));E.forEach((e,j)=>{A[e.a][j]=A[q+e.b][j]=A[2*q+e.c][j]=1});return A}
 function potentialCheck(F){
  let {q,n,E,P}=F,p=new Uint8Array(3*q);
  for(let i=0;i<n;i++){p[P[0][i]]=(-i)&3;p[q+P[1][i]]=(-i)&3;p[2*q+P[2][i]]=i&3}
  let delta=p.reduce((s,x)=>s+x,0)&3,star=P[0][0],bad=0;
  for(let e of E){let w=(p[e.a]+p[q+e.b]+p[2*q+e.c])&3;assert(w===0||(w===1&&e.a===star),"potential");bad+=w}
  assert(delta===2,"delta");return {delta,nonzero:bad,star}
 }
 function signedCheck(F){
  let {q,n,k,raw,E,P}=F,by=new Map(raw.filter(e=>e.active).map(e=>[[e.a,e.b,e.c].join(","),e.id])),v=new Map();
  const add=(a,b,c,t)=>{let j=by.get([a,b,c].join(","));assert(j!==undefined,"signed edge missing");v.set(j,(v.get(j)||0)+t)};
  for(let h=0;h<k;h++){let a=h*n;
   for(let i=0;i<n;i++)add(a+i,a+(n-i)%n,a,1);
   let K=n*(n-1)/2;add(a,a,a,-K);add(a,a,a+1,K);
   for(let c=0;c<n-2;c++){let t=(n-1-c)*(n-2-c)/2;
    add(a,a+c+1,a+c+1,-t);add(a+1,a+c,a+c+1,-t);
    add(a,a+c,a+c,t);add(a+1,a+c+1,a+c+2,t);
   }
  }
  let sums=new Array(3*q).fill(0);
  for(let e of E){let x=v.get(e.id)||0;sums[e.a]+=x;sums[q+e.b]+=x;sums[2*q+e.c]+=x}
  assert(sums.every(x=>x===1),"signed integer solution");return Math.max(...Array.from(v.values(),Math.abs))
 }
 function oldNullity(F){
  let {q,E}=F,cells=new Map();
  for(let e of E){let s=e.a*q+e.b;cells.set(s,(cells.get(s)||0)+1)}
  let sing=E.filter(e=>cells.get(e.a*q+e.b)===1);
  let A=sing.map(e=>{let a=new Uint8Array(3*q);a[e.a]=a[q+e.b]=a[2*q+e.c]=1;return a});
  return 3*q-factor(A,3*q).unitRank
 }
 function projectedMatch(E,q,e){
  let adj=Array.from({length:q},()=>[]);
  for(let f of E)if(f.a!==e.a&&f.b!==e.b)adj[f.a].push(f.b);
  let match=new Int32Array(q).fill(-1);match[e.b]=e.a;
  function dfs(a,seen){for(let b of adj[a])if(!seen[b]){seen[b]=1;if(match[b]===-1||dfs(match[b],seen)){match[b]=a;return true}}return false}
  for(let a=0;a<q;a++)if(a!==e.a&&!dfs(a,new Uint8Array(q)))return false;return true
 }
 function starScan(F,all=false){
  let {q,E}=F,groups=Array.from({length:3*q},()=>[]);
  for(let e of E){groups[e.a].push(e);groups[q+e.b].push(e);groups[2*q+e.c].push(e)}
  let order=Array.from({length:q},(_,i)=>i).sort((a,b)=>groups[b].length-groups[a].length||a-b);
  let stats={stars:0,patterns:0,modRejected:0,matchingRejected:0,updates:0,scans:0,ops:0,feasibleStars:0,cert:null};
  for(let a of order){let S=groups[a],rest=E.filter(e=>e.a!==a),A=incidence(rest,q),f=factor(A,rest.length);stats.stars++;stats.updates+=f.updates;stats.scans+=f.scans;stats.ops+=f.ops;let pass=0,failed=[];
   for(let e of S){stats.patterns++;let b=new Uint8Array(3*q).fill(1);b[e.a]=b[q+e.b]=b[2*q+e.c]=0;let x=f.solve(b);let pm=projectedMatch(E,q,e);if(!pm)stats.matchingRejected++;if(!x)stats.modRejected++;else assert(verify(A,x,b),"star witness");if(x&&pm)pass++;else failed.push(e.id)}
   if(!pass){stats.cert={owner:a,ids:failed};if(!all)break}else stats.feasibleStars++;
  }
  return stats
 }
 let results=[];
 for(let k of [1,2,4,8,12])for(let s of [0,12]){
  let F=gen(k,s),p=potentialCheck(F),signed=signedCheck(F),nu=oldNullity(F),m=F.E.length,q=F.q;
  let deg=Array(3*q).fill(0);for(let e of F.E){deg[e.a]++;deg[q+e.b]++;deg[2*q+e.c]++}
  assert(Math.min(...deg)>=12,"initial forced closure");
  let A=incidence(F.E,q),b=new Uint8Array(3*q).fill(1),strict=factor(A,m).solve(b);assert(strict&&verify(A,strict,b),"global consistency");
  let st=starScan(F);assert(st.cert&&st.matchingRejected===0,"hybrid star result");
  // independently replay all failures using original coordinates for the acquired row.
  let original=F.P[0].indexOf(st.cert.owner);assert(original%12===0,"acquired star identity");
  let h=original/12,p2=new Uint8Array(3*q);for(let i=0;i<12;i++){let z=h*12+i;p2[F.P[0][z]]=(-i)&3;p2[q+F.P[1][z]]=(-i)&3;p2[2*q+F.P[2][z]]=i&3}
  let delta=p2.reduce((s,x)=>s+x,0)&3;assert(delta===2,"independent delta");
  let nonzero=0;for(let e of F.E){let w=(p2[e.a]+p2[q+e.b]+p2[2*q+e.c])&3;assert(w===0||(w===1&&e.a===st.cert.owner),"independent star");nonzero+=w}
  assert(st.cert.ids.length===F.E.filter(e=>e.a===st.cert.owner).length,"coverage");
  results.push({k,stage:s,q,m,fingerprint:F.hash,oldNullity:nu,nominalBinaryCandidates:"2^"+nu,maxSignedCoefficient:signed,globalMod4Feasible:true,minOwnerDegree:Math.min(...deg),...st,verifiedNonzero:nonzero})
 }
 // Minimal SAT soundness check: odd cyclic square has explicit diagonal exact cover.
 let yes=gen(1,0,3,false),ys=starScan(yes,true);assert(ys.cert===null,"false reject");
 // Independent modular counterexample candidate: even cyclic order 8, known NO mod8.
 let hostile=gen(1,0,8,false),hs=starScan(hostile,true);
 return {controls,results,hostile:{q:8,authentication:"sum(c-a-b)=4 mod8 for a cover, 0 for every edge",...hs},minimalYes:{q:3,feasibleStars:ys.feasibleStars,cert:ys.cert},execution:"sequential; operation counts are partial, not equal bit-clock benchmarks"}
}
console.log(JSON.stringify(audit(),null,2));
