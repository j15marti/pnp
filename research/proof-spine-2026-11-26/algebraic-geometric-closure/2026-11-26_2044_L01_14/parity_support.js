function check(x,m="check failed"){if(!x)throw Error(m)}

function make(A){return {n:A.length,E:A.flatMap((r,u)=>r.map(v=>[u,v]))}}

function fixture(id){return make(id==="nonsignable"?[[2,6],[4,6,8],[4,5],[1,7,9],[5,8],[0,2,3],[1,3],[0,6,9],[3,6,7,9],[1,4,5,7]]:[[1,7],[0,8],[5],[4,6],[0,3],[6,7],[2,3],[2,8],[1,4]])}

function restrict(G,P){return {n:G.n,E:G.E.filter(([u,v])=>!P.some(([a,b])=>(u===a&&v!==b)||(v===b&&u!==a)))}}

function cycles(p){let S=new Set(),C=[];for(let i=0;i<p.length;i++)if(!S.has(i)){let a=[],j=i;while(!S.has(j)){S.add(j);a.push(j);j=p[j]}C.push(a)}return C}

function match(G){let A=Array.from({length:G.n},()=>[]);for(let [u,v] of G.E)A[u].push(v);let M=Array(G.n).fill(-1);function dfs(u,S){for(let v of A[u])if(!S.has(v)){S.add(v);if(M[v]<0||dfs(M[v],S)){M[v]=u;return true}}return false}for(let u=0;u<G.n;u++)if(!dfs(u,new Set()))return null;let p=[];for(let v=0;v<G.n;v++)p[M[v]]=v;return p}

function evenCycle(G,p){let inv=[],A=Array.from({length:G.n},()=>[]);for(let u=0;u<G.n;u++)inv[p[u]]=u;for(let [u,v] of G.E)if(inv[v]!==u)A[u].push(inv[v]);let visits=0;for(let s=0;s<G.n;s++){let L=[s],S=new Set(L);function dfs(u){check(++visits<=1000000,"cycle audit cap");for(let v of A[u]){if(v===s&&L.length%2===0)return L.slice();if(v<=s||S.has(v))continue;S.add(v);L.push(v);let q=dfs(v);if(q)return q;L.pop();S.delete(v)}return null}let q=dfs(s);if(q)return q}return null}

function parity(G,odd){let p=match(G);if(!p)return false;if(Boolean(cycles(p).length%2)===odd)return true;let c=evenCycle(G,p);if(!c)return false;let q=p.slice();for(let i=0;i<c.length;i++)q[c[i]]=p[c[(i+1)%c.length]];check(Boolean(cycles(q).length%2)===odd&&q.every((v,u)=>G.E.some(e=>e[0]===u&&e[1]===v)),"flip lift");return true}

function ref(G){let A=Array.from({length:G.n},()=>[]);for(let [u,v] of G.E)A[u].push(v);let p=[],S=new Set(),R=[],calls=0;function dfs(u){check(++calls<=1000000,"reference cap");if(u===G.n){R.push({p:p.slice(),cycles:cycles(p)});return}for(let v of A[u])if(!S.has(v)){S.add(v);p[u]=v;dfs(u+1);S.delete(v)}}dfs(0);return {R,calls}}

function sc(n,E){for(let rev=0;rev<2;rev++){let S=new Set([0]),L=[0];for(let i=0;i<L.length;i++)for(let e of E)if(e[rev]===L[i]&&!S.has(e[1-rev])){S.add(e[1-rev]);L.push(e[1-rev])}if(S.size!==n)return false}return true}

function contradiction(G,R){let I=new Map(G.E.map((e,i)=>[e.join(","),i])),M=new Map();for(let j=0;j<R.length;j++){let x=R[j].p.reduce((z,v,u)=>z|(1n<<BigInt(I.get(u+","+v))),0n),rhs=(G.n-R[j].cycles.length)%2,trace=1n<<BigInt(j);while(x){let i=x.toString(2).length-1;if(!M.has(i)){M.set(i,[x,rhs,trace]);break}let [y,b,t]=M.get(i);x^=y;rhs^=b;trace^=t}if(!x&&rhs){let ids=R.map((_,i)=>i).filter(i=>trace&(1n<<BigInt(i)));let xor=0n,z=0;for(let i of ids){let a=R[i];xor^=a.p.reduce((x,v,u)=>x|(1n<<BigInt(I.get(u+","+v))),0n);z^=(G.n-a.cycles.length)%2}check(xor===0n&&z===1&&ids.length%2===0,"sign obstruction");return ids}}return null}

function auditFixture(id){let G=fixture(id),{R,calls}=ref(G),T=R.filter(x=>x.cycles.length%2),queries=0;
 function P(H){queries++;let z=parity(H,true),a=ref(H).R.some(c=>c.cycles.length%2);check(z===a,"parity/reference");return z}
 check(!R.some(x=>x.cycles.length===1)&&T.length>0);
 let bad=[],ordinaryBad=[];for(let e of G.E){let F=restrict(G,[e]);let S=G.E.filter(f=>P(restrict(F,[f]))),O=G.E.filter(f=>match(restrict(F,[f]))!==null); // exclude nonexistent f from pin domain below
 // restrict() by itself cannot force absent edge if no matching can use its row/col; absence yields empty row, verified via ref.
 if(!sc(G.n,S))bad.push(e);if(!sc(G.n,O))ordinaryBad.push(e)}
 check(ordinaryBad.length===0&&bad.length>0);
 let H=G,steps=[];for(let r=0;r<=G.E.length;r++){if(!P(H)){steps.push({terminal:"no-target-cover"});break}let S=H.E.filter(e=>P(restrict(H,[e])));if(!sc(G.n,S)){steps.push({terminal:"target-support-disconnected",arcs:S.length});break}H={n:H.n,E:S};let found=null;for(let e of H.E){let F=restrict(H,[e]),T=F.E.filter(f=>P(restrict(F,[f])));if(!sc(H.n,T)){found=e;break}}if(!found){steps.push({terminal:"UNKNOWN"});break}steps.push({delete:found});H={n:H.n,E:H.E.filter(e=>e!==found)}}
 let c=contradiction(G,R);check(id!=="nonsignable"||c!==null,"nonsignability");check(steps.at(-1).terminal!=="UNKNOWN");return {id,n:G.n,arcs:G.E.length,referenceCalls:calls,covers:R.length,target:T.length,allTargetSupported:G.E.every(([u,v])=>T.some(x=>x.p[u]===v)),ordinaryBad,targetBad:bad,parityQueries:queries,steps,signingInconsistencyCoverIds:c,signingWitness:c?.map(i=>R[i]),coversList:R}}

function run(){let tests=0,masks=0,guards=0;for(let n=2;n<=4;n++){let E=[];for(let u=0;u<n;u++)for(let v=0;v<n;v++)if(u!==v)E.push([u,v]);for(let m=0;m<2**E.length;m++){let G={n,E:E.filter((_,i)=>m&2**i)};masks++;for(let P of [[],...G.E.map(e=>[e])]){if(P.length)guards++;let F=restrict(G,P),R=ref(F).R;for(let odd of [false,true]){check(parity(F,odd)===R.some(c=>Boolean(c.cycles.length%2)===odd));tests++}}}}return {masks,guards,tests,fixtures:[auditFixture("signable"),auditFixture("nonsignable")],scope:"Even simple cycle DFS used only as capped reference on small graphs; polynomial production step supplied by RST theorem, not implemented."}}
console.log(JSON.stringify(run(),null,2));
