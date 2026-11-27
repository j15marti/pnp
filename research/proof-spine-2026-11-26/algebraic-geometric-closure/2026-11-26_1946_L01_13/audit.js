function ck(x,m="assert"){if(!x)throw Error(m)}

function base(yes=false){const L=[[2,3,5],[6,7],[3,5],[1,4,6],[3,6,8],[0,8],[2,7],[1,6],[0,2,4]];if(yes)L[0].push(4);const neg=new Set(["2,5","6,7","7,6","8,2","8,4"]);return {n:9,E:L.flatMap((a,i)=>a.map(j=>[i,j,neg.has(i+","+j)?-1:1]))}}

function expand(k,yes=false){let G=base(yes);const groups=Array.from({length:9},(_,i)=>[i]);for(let t=0;t<k;t++)for(let a=0;a<9;a++){let b=G.n++,c=G.n++,d=G.n++;G.E=G.E.map(([u,v,s])=>[u===a?d:u,v,s]);G.E.push([a,b,1],[a,c,1],[b,c,1],[c,b,1],[b,d,1],[c,d,1]);groups[a].push(b,c,d)}return {...G,groups}}

function det(A){let n=A.length,d=1n,s=1n;if(!n)return 1n;for(let k=0;k<n-1;k++){let j=k;while(j<n&&!A[j][k])j++;if(j===n)return 0n;if(j!==k){[A[k],A[j]]=[A[j],A[k]];s=-s}let p=A[k][k];for(let i=k+1;i<n;i++){let z=A[i][k];if(!z&&p===d)continue;for(let j=k+1;j<n;j++){let x=A[i][j]*p-z*A[k][j];ck(x%d===0n,"division");A[i][j]=x/d}A[i][k]=0n}d=p}return s*A[n-1][n-1]}

function cycles(p){let out=[],seen=new Set();for(let i=0;i<p.length;i++)if(!seen.has(i)){let c=[],j=i;while(!seen.has(j)){seen.add(j);c.push(j);j=p[j]}out.push(c)}return out}

function ref(G){const adj=Array.from({length:G.n},()=>[]);for(let [u,v,s] of G.E)adj[u].push([v,s]);let out=[],p=[],calls=0;function dfs(i,mask,s){ck(++calls<=1000000,"reference cap");if(i===G.n){let cy=cycles(p);out.push({p:p.slice(),cy,sg:s*((G.n-cy.length)%2?-1:1)});return}for(let [v,z] of adj[i])if(!(mask&(1n<<BigInt(v)))){p.push(v);dfs(i+1,mask|(1n<<BigInt(v)),s*z);p.pop()}}dfs(0,0n,1);return {out,calls}}

function matching(G,pin=null){const A=Array.from({length:G.n},()=>[]);for(let [u,v] of G.E)if(!pin||(u===pin[0]?v===pin[1]:v!==pin[1]))A[u].push(v);let M=Array(G.n).fill(-1);function dfs(u,S){for(let v of A[u])if(!S.has(v)){S.add(v);if(M[v]<0||dfs(M[v],S)){M[v]=u;return true}}return false}return A.every((_,u)=>dfs(u,new Set()))}

function close(G){return {...G,E:G.E.filter(e=>matching(G,e))}}

function sc(G){for(let rev of [0,1]){let seen=new Set([0]),q=[0];while(q.length){let u=q.pop();for(let e of G.E)if(e[rev]===u&&!seen.has(e[1-rev])){seen.add(e[1-rev]);q.push(e[1-rev])}}if(seen.size!==G.n)return false}return true}

function combos(n,k,fn){function rec(i,L){if(L.length===k){fn(L);return}for(let j=i;j<=n-(k-L.length);j++)rec(j+1,[...L,j])}rec(0,[])}

function runSolver(G,d=3,qcap=12,paircap=50000){
  let F=close(G),E=F.E,n=F.n,cuts=[],pairs=0,cache=new Map(),trace=[],certificateCalls=0,supportProbes=0,extractProbes=0;const adj=Array.from({length:n},()=>[]);E.forEach(([u,v])=>adj[u].push(v));adj.forEach(a=>a.sort((a,b)=>a-b));
  const cutmask=S=>S.reduce((m,v)=>m|(1n<<BigInt(v)),0n);
  function count(pins,J){let key=pins.join(",")+"|"+J.join(",");if(cache.has(key))return cache.get(key);if(++pairs>paircap)throw Error("pair cap");let A=Array.from({length:n},()=>Array(n).fill(0n)),B=Array.from({length:n},()=>Array(n).fill(0n));let used=new Set(pins.filter(v=>v>=0));if(used.size!==pins.filter(v=>v>=0).length)return 0n;
    for(let [u,v,s] of E){if(pins[u]>=0?pins[u]!==v:used.has(v))continue;let U=1n<<BigInt(u),V=1n<<BigInt(v);if(J.some(j=>(cuts[j]&U)&&!(cuts[j]&V)))continue;A[u][v]=1n;B[u][v]=BigInt(s)}
    let z=det(B),a=det(A),C=z<0n?-z:z,h=n%2?1n:-1n;ck((C+h*a)%2n===0n&&C+h*a>=0n);let r=(C+h*a)/2n;cache.set(key,r);return r;
  }
  function remaining(pins){let z=0n;for(let k=0;k<=Math.min(d,cuts.length);k++)combos(cuts.length,k,J=>{let v=count(pins,J);z+=k%2?-v:v});ck(z>=0n,"negative remaining");return z}
  const empty=Array(n).fill(-1);let B=count(empty,[]);let initial=B;
  // Under each current guard exact retained support closure; use it for subsequent acquisition.
  // The global overlap check uses the *root* parity fiber, not only the uncovered residual.
  try{
    if(!B||!sc(F))return {status:"NO",initial,pairs,trace,removed:G.E.length-E.length};
    while(true){
      let R=remaining(empty);if(!R)return {status:"NO",initial,pairs,trace,cuts:cuts.map(x=>Array.from({length:n},(_,i)=>i).filter(i=>x&(1n<<BigInt(i)))),supportProbes,extractProbes,certificateCalls,removed:G.E.length-E.length};
      if(cuts.length>=qcap)return {status:"UNKNOWN-cut-cap",initial,pairs,trace,supportProbes,extractProbes,certificateCalls};
      // Reclose exact uncovered target support. Delete only in the uncovered chart; keep original for counts.
      const live=[];for(let e of E){let pins=empty.slice();pins[e[0]]=e[1];supportProbes++;if(remaining(pins)>0n)live.push(e)}
      // Don't use disconnected-support shortcut in this audit: record it and acquire a concrete cut anyway.
      let supportSC=sc({n,E:live});let allowed=Array.from({length:n},()=>[]);for(let [u,v] of live)allowed[u].push(v);allowed.forEach(a=>a.sort((a,b)=>a-b));
      let pins=empty.slice(),used=new Set();
      for(let u=0;u<n;u++){let ok=false;for(let v of allowed[u])if(!used.has(v)){pins[u]=v;extractProbes++;if(remaining(pins)>0n){used.add(v);ok=true;break}pins[u]=-1}ck(ok,"uncovered lift")}
      let cy=cycles(pins);ck(cy.length%2===1);if(cy.length===1)return {status:"NOT-REFUTED",initial,pairs,trace,uncovered:R,witness:pins,supportProbes,extractProbes,certificateCalls};
      let S=cy.filter(c=>!c.includes(0)).sort((a,b)=>a.length-b.length||a[0]-b[0])[0].sort((a,b)=>a-b);let m=cutmask(S);ck(!cuts.includes(m));let old=cuts.length;cuts.push(m);
      let overlap=false;combos(old,d,J=>{certificateCalls++;if(count(empty,[...J,old])>0n)overlap=true});
      if(overlap)return {status:"UNKNOWN-overlap-cap",initial,pairs,trace,attempted:S,supportProbes,extractProbes,certificateCalls};
      let R2=remaining(empty);ck(R2<R,"strict progress");trace.push({before:R,after:R2,cut:S,coverCycles:cy,uncoveredSupportArcs:live.length,supportSC,pairs});
    }
  }catch(e){if(String(e).includes("pair cap"))return {status:"UNKNOWN-pair-cap",initial,pairs,trace};throw e}
}

function run(){let G=base(),R=ref(G),T=R.out.filter(x=>x.cy.length%2);ck(R.out.length===9&&T.length===5&&T.every(x=>x.cy.length===3)&&new Set(R.out.map(x=>x.sg)).size===1);ck(close(G).E.length===G.E.length&&sc(G));let tests=[];
for(let k of [0,1,2]){let X=expand(k);let r=runSolver(X);ck(r.status==="NO"&&r.initial===5n*2n**BigInt(9*k));let minCycle=2*(1+3*k);ck(r.trace.every(t=>t.cut.length>=minCycle));for(let t of r.trace){let members=new Set(t.cut);ck(X.groups.every(g=>g.every(v=>members.has(v))||g.every(v=>!members.has(v))));}tests.push({k,n:X.n,arcs:X.E.length,minCoverCycleLength:minCycle,staticSize3:k?"NO EVENTS (proved)":"prior certificate",...r})}
let Y=base(true),RY=ref(Y);ck(new Set(RY.out.map(x=>x.sg)).size===1&&RY.out.filter(x=>x.cy.length===1).length===1);let y=runSolver(Y);ck(y.status==="NOT-REFUTED");let low=runSolver(G,1);ck(low.status.startsWith("UNKNOWN")||low.status==="NO");let zero=runSolver(G,3,1);ck(zero.status==="UNKNOWN-cut-cap");let guarded=[];for(let [u,v] of G.E)for(let pin of [false,true]){let F={...G,E:G.E.filter(([a,b])=>pin?(a===u?b===v:b!==v):!(a===u&&b===v))};let r=runSolver(F);ck(r.status==="NO");guarded.push({u,v,pin,status:r.status,pairs:r.pairs,rounds:r.trace.length})}
return {baseReference:{calls:R.calls,covers:R.out},tests,neighbor:{refCalls:RY.calls,...y},lowOverlap:low,cutCap:zero,guarded,mode:"serial; exact BigInt; capped reference only base/neighbor; signing proof by base exhaustive check and exact gadget extension; no general signing recognizer"}}
console.log(JSON.stringify(run(),(_,v)=>typeof v==='bigint'?v.toString():v,2));
