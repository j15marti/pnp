// P3FG04: standalone Node.js audit. No external dependencies.
function audit(){
  const out={seed:20261125,checks:0,signingChecks:0,determinants:0,smallSourceJobs:0,smallTargetJobs:0,yes:0,no:0,unknown:0,sourceYes:0,sourceNo:0,sourceUnknown:0,neighbor:[],ladder:[]};
  let seed=out.seed;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)}
  function check(x,msg){out.checks++;if(!x)throw Error(msg)}
  const bit=i=>1n<<BigInt(i);
  function parity(x){let p=0;while(x){x&=x-1n;p^=1}return p}
  function reduce(x,B){for(let i=B.length-1;i>=0;i--)if(B[i]&&(x&bit(i)))x^=B[i];return x}
  function add(x,B){x=reduce(x,B);if(!x)return false;let i=x.toString(2).length-1;B[i]=x;return true}
  function rk(B){return B.filter(Boolean).length}
  function basis(xs){let B=[];for(let x of xs)add(x,B);return B}
  function maskSum(ids,L){let x=0n;for(let i of ids)x^=L[i];return x}
  function matching(n,E,live){let mate=Array(n).fill(-1),adj=Array.from({length:n},()=>[]);for(let i of live)adj[E[i][0]].push(i);
    function aug(x,seen){for(let i of adj[x]){let y=E[i][1];if(seen[y])continue;seen[y]=true;if(mate[y]<0||aug(E[mate[y]][0],seen)){mate[y]=i;return true}}return false}
    for(let x=0;x<n;x++)if(!aug(x,Array(n).fill(false)))return null;return mate.sort((i,j)=>E[i][0]-E[j][0])}
  function force(E,live,i){let [a,b]=E[i];return live.filter(j=>j===i||E[j][0]!==a&&E[j][1]!==b)}
  function allPM(n,E,live){let A=Array.from({length:n},()=>[]);for(let i of live)A[E[i][0]].push(i);let R=[];function rec(x,used,M){if(x===n){R.push(M.slice());return}for(let i of A[x]){let y=E[i][1];if(!(used&bit(y))){M.push(i);rec(x+1,used|bit(y),M);M.pop()}}}rec(0,0n,[]);return R}
  function invParity(M,E){let p=0;for(let i=0;i<M.length;i++)for(let j=i+1;j<M.length;j++)p^=+(E[M[i]][1]>E[M[j]][1]);return p}
  // Directed paths and actual M-alternating simple-cycle basis, no rotation oracle.
  function prepare(n,E,live,L){
    let M=matching(n,E,live);if(!M)return null;
    let Y=Array(n);for(let i=0;i<n;i++)Y[E[M[i]][1]]=i;
    let arcs=live.filter(i=>M[E[i][0]]!==i).map(i=>({id:i,u:E[i][0],v:Y[E[i][1]]}));
    let A=Array.from({length:n},()=>[]);for(let a of arcs)A[a.u].push(a);
    function paths(s){let P=Array(n).fill(null);P[s]=[];let Q=[s];for(let u of Q)for(let a of A[u])if(P[a.v]===null){P[a.v]=P[u].concat(a);Q.push(a.v)}return P}
    let P=Array.from({length:n},(_,i)=>paths(i)),C=[],rows=[],rhs=[],seen=new Set();
    function consume(W){if(!W.length)return;let vs=[W[0].u],es=[];for(let a of W){check(vs[vs.length-1]===a.u,"walk");let k=vs.indexOf(a.v);es.push(a);if(k>=0){let cyc=es.slice(k),v=0n;for(let b of cyc)v^=bit(b.id)^bit(M[b.u]);let z=reduce(v,C);if(z){add(v,C);let p=(cyc.length-1)%2;for(let j=rows.length-1;j>=0;j--)if(rows[j]&&(v&bit(j))){v^=rows[j];p^=rhs[j]}check(v!==0n,"independent signing");let j=v.toString(2).length-1;rows[j]=v;rhs[j]=p}vs=vs.slice(0,k+1);es=es.slice(0,k)}else vs.push(a.v)}check(es.length===0,"closed walk decomposition")}
    for(let r=0;r<n;r++){if(seen.has(r))continue;let S=[];for(let v=0;v<n;v++)if(P[r][v]!==null&&P[v][r]!==null){S.push(v);seen.add(v);consume(P[r][v].concat(P[v][r]))}let ss=new Set(S);for(let a of arcs)if(ss.has(a.u)&&ss.has(a.v))consume(P[r][a.u].concat(a,P[a.v][r]))}
    let s=0n;for(let j=0;j<rows.length;j++)if(rows[j]&&(parity(rows[j]&s)^rhs[j]))s|=bit(j);
    let sign=invParity(M,E)^parity(maskSum(M,E.map((_,i)=>bit(i)))&s);
    let W=[];for(let c of C.filter(Boolean)){let v=0n;for(let i of live)if(c&bit(i))v^=L[i];add(v,W)}
    return {M,C,W,s,sign,a:maskSum(M,L)}
  }
  function determinant(A){out.determinants++;let n=A.length;if(!n)return 1n;A=A.map(r=>r.slice());let prev=1n,sgn=1n;for(let k=0;k<n-1;k++){let r=k;while(r<n&&!A[r][k])r++;if(r===n)return 0n;if(r!==k){[A[r],A[k]]=[A[k],A[r]];sgn=-sgn}let p=A[k][k];for(let i=k+1;i<n;i++){for(let j=k+1;j<n;j++){let v=A[i][j]*p-A[i][k]*A[k][j];check(v%prev===0n,"Bareiss division");A[i][j]=v/prev}A[i][k]=0n}prev=p}return sgn*A[n-1][n-1]}
  function charts(n,E,live,L){let pairs=new Map();for(let i of live){let k=E[i][0]+","+E[i][1];if(!pairs.has(k))pairs.set(k,[]);pairs.get(k).push(i)}let usedX=new Set(),usedY=new Set(),H=[],blocks=[];for(let ids of pairs.values()){let [x,y]=E[ids[0]];if(usedX.has(x)||usedY.has(y))continue;let found=null;for(let i of ids)for(let j of ids)if(i<j&&reduce(L[i]^L[j],H)&&found===null)found=[i,j];if(found){add(L[found[0]]^L[found[1]],H);blocks.push(found);usedX.add(x);usedY.add(y)}}
    let keep=new Set(blocks.flat());let F=live.filter(i=>keep.has(i)||!usedX.has(E[i][0])&&!usedY.has(E[i][1]));return {H,blocks,F}}
  function solve(n,E,live,L,t,cap,ref=null){
    let P=prepare(n,E,live,L);if(!P)return {status:"NO",r:0,h:0,w:0};
    if(ref){let W0=basis(ref.map(M=>maskSum(M,L)^P.a));check(rk(W0)===rk(P.W)&&W0.filter(Boolean).every(v=>!reduce(v,P.W)),"actual variation span");for(let M of ref){check((invParity(M,E)^parity(maskSum(M,E.map((_,i)=>bit(i)))&P.s))===P.sign,"coherent signing");out.signingChecks++}}
    if(reduce(t^P.a,P.W))return {status:"NO",r:rk(P.W),h:0,w:rk(P.W)};
    let C=charts(n,E,live,L);
    // Only retain chart if forced skeleton extends to an actual perfect matching.
    if(!matching(n,E,C.F))C={H:[],blocks:[],F:live};
    for(let h of C.H.filter(Boolean))check(!reduce(h,P.W),"chart direction in actual span");
    let Q=basis(P.W.filter(Boolean).map(v=>reduce(v,C.H))),piv=[];for(let j=0;j<Q.length;j++)if(Q[j])piv.push(j);
    function coord(v){v=reduce(v,C.H);let a=0n;for(let k=piv.length-1;k>=0;k--){let j=piv[k];if(v&bit(j)){v^=Q[j];a|=bit(k)}}return a}
    let w=piv.length,r=rk(P.W),h=rk(C.H);check(r===h+w,"rank decomposition");
    let meta={r,h,w,blocks:C.blocks.length};if(w>cap)return {status:"UNKNOWN",reason:"rank-cap",...meta};
    let tag=L.map(coord),target=coord(t);
    function cnt(F){if(w===0)return matching(n,E,F)?1n:0n;let total=0n;for(let c=0;c<(1<<w);c++){let A=Array.from({length:n},()=>Array(n).fill(0n));for(let i of F){let [x,y]=E[i];A[x][y]+= (parity(P.s&bit(i))^parity(BigInt(c)&tag[i]))?-1n:1n}let sign=P.sign^parity(BigInt(c)&target);let d=determinant(A);total+=sign?-d:d}check(total>=0n&&total%bit(w)===0n,"positive exact Walsh count");return total/bit(w)}
    let unrestricted=cnt(live),restricted=cnt(C.F);
    if(ref){let qcount=ref.filter(M=>coord(maskSum(M,L))===target).length;let ff=new Set(C.F),fcount=ref.filter(M=>M.every(i=>ff.has(i))&&coord(maskSum(M,L))===target).length;if(w>0){check(unrestricted===BigInt(qcount),"unrestricted Fourier");check(restricted===BigInt(fcount),"restricted Fourier")}else{check(!!unrestricted===!!qcount,"unrestricted rank0");check(!!restricted===!!fcount,"restricted rank0")}}
    if(!unrestricted)return {status:"NO",...meta};if(!restricted)return {status:"UNKNOWN",reason:"chart misses fiber",...meta};
    let F=C.F.slice(),M;
    if(w===0)M=matching(n,E,F);else{for(let i of C.F)if(F.includes(i)){let G=F.filter(j=>j!==i);if(cnt(G))F=G}M=matching(n,E,F)}
    check(M&&coord(maskSum(M,L))===target,"quotient lift");
    let d=t^maskSum(M,L),B=[],comb=[];for(let j=0;j<C.blocks.length;j++){let [i,k]=C.blocks[j],v=L[i]^L[k],c=bit(j);for(let a=B.length-1;a>=0;a--)if(B[a]&&(v&bit(a))){v^=B[a];c^=comb[a]}check(v!==0n,"independent blocks");let a=v.toString(2).length-1;B[a]=v;comb[a]=c}
    let pick=0n;for(let j=B.length-1;j>=0;j--)if(B[j]&&(d&bit(j))){d^=B[j];pick^=comb[j]}check(!d,"target residual in chart span");
    for(let j=0;j<C.blocks.length;j++)if(pick&bit(j)){let [i,k]=C.blocks[j];let a=M.indexOf(i),b=M.indexOf(k);check((a>=0)!==(b>=0),"one choice per block");if(a>=0)M[a]=k;else M[b]=i}
    check(maskSum(M,L)===t&&new Set(M.map(i=>E[i][0])).size===n&&new Set(M.map(i=>E[i][1])).size===n,"actual full lift");return {status:"YES",...meta,M};
  }
  const lanes=[[0,1,2],[0,2,1],[1,2,0]];
  function lane(T,l){return T.map(t=>[t[l[0]],t[l[1]],t[l[2]]])}
  function pmSource(n,T,M){return M&&[0,1,2].every(a=>new Set(M.map(i=>T[i][a])).size===n)}
  function closure(n,T){let live=T.map((_,i)=>i),L=T.map(t=>t.reduce((a,v,j)=>a^bit(j*n+v),0n)),t=bit(3*n)-1n;while(true){let old=live.length;for(let a=0;a<3;a++)for(let x=0;x<n;x++){let J=live.filter(i=>T[i][a]===x);if(!J.length)return null;if(J.length===1){let k=J[0];live=live.filter(i=>i===k||T[i].every((v,b)=>v!==T[k][b]))}}
    for(let l of lanes){let E=lane(T,l);if(!matching(n,E,live))return null;live=live.filter(i=>matching(n,E,force(E,live,i)))}
    if(reduce(t,basis(live.map(i=>L[i]))))return null;
    for(let i of live.slice()){let B=basis(live.filter(j=>j!==i).map(j=>L[j]));if(reduce(t^L[i],B))live=live.filter(j=>j!==i);else if(reduce(t,B))live=live.filter(j=>j===i||T[j].every((v,a)=>v!==T[i][a]))}
    if(live.length===old)return live}}
  function ladder(n){let T=[];for(let i=0;i<n;i++){let j=(i+1)%n;T.push([i,i,i],[i,j,i],[j,i,i])}return T}
  function support(n,E,live){let L=E.map(t=>bit(t[2]));return new Set(allPM(n,E,live).map(M=>maskSum(M,L)))}
  function periodRank(S){let a=S.values().next().value,B=[];for(let b of S){let p=a^b;if([...S].every(x=>S.has(x^p)))add(p,B)}return rk(B)}
  function isTileable(p,n){if(!p||p===bit(n)-1n)return true;let start=0;while(p&bit(start))start++;let run=0;for(let j=1;j<=n;j++){let k=(start+j)%n;if(p&bit(k))run++;else{if(run%2)return false;run=0}}return true}
  // All random sources are subgraphs of a provably planar circular ladder; two prior q=3 fixtures.
  const U=[[0,1,1],[0,2,2],[1,0,1],[1,2,0],[2,0,0],[2,1,2],[2,2,0],[2,2,2]];
  const V=U.map(t=>t.slice());V[1]=[0,1,2];
  function sourceJob(n,T,neighbor=false){let live0=T.map((_,i)=>i),E0=lane(T,lanes[0]),truth=allPM(n,E0,live0).some(M=>pmSource(n,T,M));let live=closure(n,T),status="UNKNOWN";if(!live)status="NO";else for(let l of lanes){let E=lane(T,l),L=E.map(t=>bit(t[2])),ref=allPM(n,E,live);let R=solve(n,E,live,L,bit(n)-1n,4,ref);if(R.status==="YES"){check(pmSource(n,T,R.M),"source witness");status="YES";break}if(R.status==="NO"){status="NO";break}}
    check(status==="UNKNOWN"||(status==="YES")===truth,"source label");out.smallSourceJobs++;out[status==="YES"?"sourceYes":status==="NO"?"sourceNo":"sourceUnknown"]++;if(neighbor)out.neighbor.push({truth,status,tuples:T.length});
    if(live)for(let l of lanes){let E=lane(T,l),L=E.map(t=>bit(t[2])|(BigInt(rnd(4))<<BigInt(n))),ref=allPM(n,E,live),S=new Set(ref.map(M=>maskSum(M,L)));for(let j=0;j<5;j++){let t=j===0&&S.size?[...S][rnd(S.size)]:j===1?(bit(n)-1n)|(BigInt(rnd(4))<<BigInt(n)):BigInt(rnd(1<<(n+2)));let R=solve(n,E,live,L,t,4,ref);check(R.status==="UNKNOWN"||(R.status==="YES")===S.has(t),"guarded exact label");out.smallTargetJobs++;out[R.status.toLowerCase()]++}}}
  sourceJob(3,U,true);sourceJob(3,V,true);
  for(let j=0;j<100;j++){let n=4+2*(j%2),T=ladder(n).filter(()=>rnd(10)<8);sourceJob(n,T)}
  for(let n of [6,8,10,12]){let T=ladder(n),live=T.map((_,i)=>i),E=lane(T,lanes[0]),S=support(n,E,live),all=bit(n)-1n;for(let p=0n;p<=all;p++)check(S.has(p)===isTileable(p^all,n),"ladder support characterization");check(periodRank(S)===0,"aperiodic XY support");let P=prepare(n,E,live,E.map(t=>bit(t[2])));check(rk(P.W)===n-1,"linear rank");let E2=lane(T,lanes[1]),R=solve(n,E2,live,E2.map(t=>bit(t[2])),all,4,allPM(n,E2,live));check(R.status==="YES"&&R.h===n-1&&R.w===0&&pmSource(n,T,R.M),"alternate lane");out.ladder.push({n,tuples:T.length,xySupport:S.size,xyRank:n-1,xyPeriodRank:0,xzChartRank:R.h,xzResidualRank:R.w})}
  for(let n of [16,32,64,128]){let T=ladder(n),live=T.map((_,i)=>i),E=lane(T,lanes[1]),R=solve(n,E,live,E.map(t=>bit(t[2])),bit(n)-1n,4);check(R.status==="YES"&&R.h===n-1&&R.w===0&&pmSource(n,T,R.M),"large alternate lane");let m0=[],m1=[],m2=[];for(let i=0;i<n;i++){m0.push(3*i);m1.push(3*i+1);m2.push(3*i+2)}check([m0,m1,m2].every(M=>pmSource(n,T,M))&&new Set([...m0,...m1,...m2]).size===T.length,"all triples actually extendible");out.ladder.push({n,tuples:T.length,xySupport:"exponential, theorem",xyRank:n-1,xyPeriodRank:0,xzChartRank:R.h,xzResidualRank:R.w})}
  {let n=6,T=ladder(n),E=lane(T,lanes[1]),live=T.map((_,i)=>i),L=E.map((t,i)=>bit(t[2])^(i===2?bit(n):0n)),t=bit(n+1)-1n,ref=allPM(n,E,live),R=solve(n,E,live,L,t,4,ref);check(ref.some(M=>maskSum(M,L)===t)&&R.status==="UNKNOWN"&&R.reason==="chart misses fiber","guarded chart must not reject");out.guardMiss={n,actual:"YES",returned:R.status,r:R.r,h:R.h,w:R.w,reason:R.reason}}
  return out;
}
console.log(JSON.stringify(audit(),null,2));
