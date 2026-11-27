function check(p,m="failure"){if(!p)throw Error(m)}

function graph(k=0){const A=[[1,7],[0,8],[5],[4,6],[0,3],[6,7],[2,3],[2,8],[1,4]],neg=new Set(["7,8","8,1"]);let G={n:9,E:A.flatMap((a,u)=>a.map(v=>[u,v,neg.has(u+","+v)?-1:1]))};for(let i=0;i<k;i++){let b=G.n,c=b+1,d=b+2;G.E=G.E.map(([u,v,s])=>[u===0?d:u,v,s]);G.E.push([0,b,1],[0,c,1],[b,c,1],[c,b,1],[b,d,1],[c,d,1]);G.n+=3}return G}

function det(A){let n=A.length,d=1n,sign=1n;A=A.map(r=>r.slice());for(let k=0;k<n-1;k++){let i=k;while(i<n&&!A[i][k])i++;if(i===n)return 0n;if(i!==k){[A[i],A[k]]=[A[k],A[i]];sign=-sign}let p=A[k][k];for(let i=k+1;i<n;i++){let a=A[i][k];if(!a&&p===d)continue;for(let j=k+1;j<n;j++){let z=A[i][j]*p-a*A[k][j];check(z%d===0n);A[i][j]=z/d}A[i][k]=0n}d=p}return sign*A[n-1][n-1]}

function count(G,pins=[]){let A=Array.from({length:G.n},()=>Array(G.n).fill(0n)),S=A.map(r=>r.slice());for(let [u,v,s] of G.E)if(!pins.some(([a,b])=>(a===u&&b!==v)||(b===v&&a!==u))){A[u][v]=1n;S[u][v]=BigInt(s)}let c=det(S),z=det(A);c=c<0n?-c:c;let b=c+(G.n%2?1n:-1n)*z;check(b>=0n&&b%2n===0n);return [c,b/2n]}

function connected(n,E){for(let rev=0;rev<2;rev++){let seen=new Set([0]),Q=[0];for(let i=0;i<Q.length;i++)for(let e of E)if(e[rev]===Q[i]&&!seen.has(e[1-rev])){seen.add(e[1-rev]);Q.push(e[1-rev])}if(seen.size!==n)return false}return true}

function supports(G,pins=[],which=0){return G.E.filter(e=>count(G,[...pins,e])[which]>0n)}

function run(){
 let rows=[];
 for(let k of [0,1,2,4,8]){
  let G=graph(k),ordinary=[],target=[],calls=0;const root=count(G);calls++;
  for(let e of G.E){let c=count(G,[e]);calls++;check(c[0]>0n&&c[1]>0n);let S=[],T=[];for(let f of G.E){let [a,b]=count(G,[e,f]);calls++;if(a)S.push(f);if(b)T.push(f)}if(!connected(G.n,S))ordinary.push(e.slice(0,2));if(!connected(G.n,T))target.push(e.slice(0,2))}
  check(ordinary.length===0&&target.length===16,"strict guard family");
  // Production-style early discharge: scan until a certified bad target guard.
  let H={n:G.n,E:G.E.map(e=>e.slice())},q=0,removed=null;const cur=count(H)[1];q++;
  for(let e of H.E){let c=count(H,[e])[1];q++;let S=[];if(c)for(let f of H.E){if(count(H,[e,f])[1])S.push(f);q++}if(!c||!connected(H.n,S)){removed=e.slice(0,2);H.E=H.E.filter(f=>f!==e);break}}
  check(removed!==null);let after=count(H)[1];q++;let T=H.E.filter(e=>{q++;return count(H,[e])[1]>0n});check(!connected(H.n,T),"post-deletion closure");
  rows.push({n:G.n,arcs:G.E.length,total:root[0],target:root[1],ordinaryBadGuards:ordinary,targetBadGuards:target,allGuardComparisonPairs:calls,deleted:removed,remaining:after,targetSupportAfter:T.length,dischargePairs:q,refuted:true});
 }
 return rows;
}
console.log(JSON.stringify(run(),(_,v)=>typeof v==='bigint'?v.toString():v,2));
