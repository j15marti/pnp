function ok(x,m="assertion"){if(!x)throw Error(m)}

function fixture(type="hostile"){
 const A=type==="hostile"?[[1,7],[0,8],[5],[4,6],[0,3],[6,7],[2,3],[2,8],[1,4]]:[[2,3,5],[6,7],[3,5],[1,4,6],[3,6,8],[0,8],[2,7],[1,6],[0,2,4]];
 if(type==="yes")A[0].push(4);
 const neg=new Set(type==="hostile"?["7,8","8,1"]:["2,5","6,7","7,6","8,2","8,4"]);
 return {n:9,E:A.flatMap((a,u)=>a.map(v=>[u,v,neg.has(u+","+v)?-1:1]))};
}

function expand(k){let G=fixture();for(let i=0;i<k;i++){let b=G.n,c=b+1,d=b+2;G.E=G.E.map(([u,v,s])=>[u===0?d:u,v,s]);G.E.push([0,b,1],[0,c,1],[b,c,1],[c,b,1],[b,d,1],[c,d,1]);G.n+=3}return G}

function det(A){A=A.map(a=>a.slice());let n=A.length,d=1n,sg=1n;for(let k=0;k<n-1;k++){let r=k;while(r<n&&!A[r][k])r++;if(r===n)return 0n;if(r!==k){[A[r],A[k]]=[A[k],A[r]];sg=-sg}let p=A[k][k];for(let i=k+1;i<n;i++){let a=A[i][k];if(!a&&p===d)continue;for(let j=k+1;j<n;j++){let x=A[i][j]*p-a*A[k][j];ok(x%d===0n,"Bareiss");A[i][j]=x/d}A[i][k]=0n}d=p}return sg*A[n-1][n-1]}

function reference(G){let adj=Array.from({length:G.n},()=>[]);for(let [u,v,s] of G.E)adj[u].push([v,s]);let p=[],out=[],calls=0;function dfs(u,used,sg){ok(++calls<=1000000,"ref cap");if(u===G.n){let seen=new Set(),cycles=[];for(let i=0;i<G.n;i++)if(!seen.has(i)){let C=[],j=i;while(!seen.has(j)){C.push(j);seen.add(j);j=p[j]}cycles.push(C)}out.push({p:p.slice(),cycles,sign:sg*((G.n-cycles.length)%2?-1:1)});return}for(let [v,s] of adj[u])if(!used.has(v)){p[u]=v;used.add(v);dfs(u+1,used,sg*s);used.delete(v)}}dfs(0,new Set(),1);return {out,calls}}

function match(G,pin){let adj=Array.from({length:G.n},()=>[]);for(let [u,v] of G.E)if(!pin||(u===pin[0]?v===pin[1]:v!==pin[1]))adj[u].push(v);let M=Array(G.n).fill(-1);function dfs(u,S){for(let v of adj[u])if(!S.has(v)){S.add(v);if(M[v]===-1||dfs(M[v],S)){M[v]=u;return true}}return false}return adj.every((_,u)=>dfs(u,new Set()))}

function close(G){return {n:G.n,E:G.E.filter(e=>match(G,e))}}

function engine(G,cap=50000){let calls=0;const n=G.n;function raw(pins=[],cuts=[]){if(calls>=cap)throw Error("CAP");calls++;let A=Array.from({length:n},()=>Array(n).fill(0n)),S=A.map(x=>x.slice());for(let [u,v,s] of G.E){if(pins.some(([a,b])=>(u===a&&v!==b)||(v===b&&u!==a))||cuts.some(X=>X.has(u)&&!X.has(v)))continue;A[u][v]=1n;S[u][v]=BigInt(s)}let d=det(A),z=det(S),C=z<0n?-z:z,h=n%2?1n:-1n;ok((C+h*d)%2n===0n&&C+h*d>=0n,"parity");return (C+h*d)/2n}
 function IE(pins,cuts,extra=[],d=3){let z=0n;function rec(i,J){z+=(J.length%2?-1n:1n)*raw(pins,[...extra,...J]);if(J.length===d)return;for(let j=i;j<cuts.length;j++)rec(j+1,[...J,cuts[j]])}rec(0,[]);ok(z>=0n,"negative");return z}
 function overlap(cuts,newcut,d=3){let safe=true;function rec(i,J){if(J.length===d){if(raw([], [...J,newcut])!==0n)safe=false;return}for(let j=i;j<cuts.length;j++)rec(j+1,[...J,cuts[j]])}if(cuts.length>=d)rec(0,[]);return safe}
 return {raw,IE,overlap,calls:()=>calls}}

function capacities(G,en,pins,cuts){let B=en.IE(pins,cuts),W=Array.from({length:G.n},()=>Array(G.n).fill(0n));if(B)for(let [u,v] of G.E)W[u][v]=en.IE([...pins,[u,v]],cuts);for(let u=0;u<G.n;u++){ok(W[u].reduce((a,b)=>a+b,0n)===B,"row conservation");ok(W.reduce((a,r)=>a+r[u],0n)===B,"col conservation")}return {B,W}}

function mincut(W){let n=W.length,best=null;for(let t=1;t<n;t++){let R=W.map(r=>r.slice()),flow=0n,seen;while(true){let p=Array(n).fill(-1),Q=[0];p[0]=0;for(let i=0;i<Q.length&&p[t]<0;i++){let u=Q[i];for(let v=0;v<n;v++)if(p[v]<0&&R[u][v]>0n){p[v]=u;Q.push(v)}}if(p[t]<0){seen=new Set(Q);break}let a=null;for(let v=t;v!==0;v=p[v])a=a===null||R[p[v]][v]<a?R[p[v]][v]:a;for(let v=t;v!==0;v=p[v]){R[p[v]][v]-=a;R[v][p[v]]+=a}flow+=a}
 let S=new Set(Array.from({length:n},(_,i)=>i).filter(i=>!seen.has(i))),val=0n;for(let u of S)for(let v=0;v<n;v++)if(!S.has(v))val+=W[u][v];ok(val===flow,"cut flow");if(best===null||val<best.val)best={S,val};if(!val)break}return best}

function exactSmall(W){let n=W.length,lo=null;ok(n<=12);for(let mask=1;mask<2**(n-1);mask++){let z=0n;for(let i=1;i<n;i++)if(mask&2**(i-1))for(let j=0;j<n;j++)if(j===0||!(mask&2**(j-1)))z+=W[i][j];if(lo===null||z<lo)lo=z}return lo}

function solve(G,mode,cap=50000){let en=engine(G,cap),cuts=[],rounds=[],guardTests=0;const N=BigInt(G.n*(G.n-1));try{for(let r=0;r<12;r++){let {B,W}=capacities(G,en,[],cuts);if(!B)return {status:"NO",rounds,guardTests,pairs:en.calls()};let cut=mincut(W),root=cut.val;if(G.n<=12)ok(root===exactSmall(W),"mincut vs exhaustive");let pick=null;if((B-cut.val)*N>=B)pick={S:cut.S,guard:[],gap:B-cut.val,guardB:B,cap:cut.val};
 if(!pick&&mode==="conditioned"){for(let e of G.E){let [u,v]=e;if(W[u][v]*N<B)continue;guardTests++;let C=capacities(G,en,[[u,v]],cuts);ok(C.B===W[u][v]);let c=mincut(C.W);if(G.n<=12)ok(c.val===exactSmall(C.W));if((C.B-c.val)*N>=B){pick={S:c.S,guard:[[u,v]],gap:C.B-c.val,guardB:C.B,cap:c.val};break}}}
 if(!pick)return {status:"UNKNOWN-gap",rootB:B,rootMin:root,rounds,guardTests,pairs:en.calls()};
 if(!en.overlap(cuts,pick.S))return {status:"UNKNOWN-overlap",rounds,guardTests,pairs:en.calls()};let removed=en.IE([],cuts,[pick.S]);ok(removed>=pick.gap&&removed>0n);cuts.push(pick.S);let after=en.IE([],cuts);ok(after===B-removed,"exact disjoint exclusion");rounds.push({before:B,rootMin:root,guard:pick.guard,guardB:pick.guardB,guardMin:pick.cap,lower:pick.gap,removed,after,cut:[...pick.S],pairs:en.calls()});if(!after)return {status:"NO",rounds,guardTests,pairs:en.calls()};
 }return {status:"UNKNOWN-cut-cap",rounds,guardTests,pairs:en.calls()}}catch(e){if(e.message==="CAP")return {status:"UNKNOWN-count-cap",rounds,guardTests,pairs:en.calls()};throw e}}

function run(){const tests=[];for(let [name,G] of [["hostile",fixture()],["previous",fixture("previous")],["YES-control",fixture("yes")],...([1,2,4,8].map(k=>["expanded-"+k,expand(k)]))]){
 let F=close(G);ok(F.E.length===G.E.length,"initial support");let R=G.n<=15?reference(F):null,ref=null;
 if(R){let T=R.out.filter(x=>x.cycles.length%2);ok(new Set(R.out.map(x=>x.sign)).size===1,"signing");let C=capacities(F,engine(F),[],[]);ok(C.B===BigInt(T.length));for(let [u,v] of F.E)ok(C.W[u][v]===BigInt(T.filter(x=>x.p[u]===v).length));ref={calls:R.calls,covers:R.out.length,target:T.length,tours:T.filter(x=>x.cycles.length===1).length,allTargetSupported:F.E.every(([u,v])=>T.some(x=>x.p[u]===v)),targetCovers:G.n===9?T:undefined};}
 let A=solve(F,"unconditioned"),I=solve(F,"conditioned");if(name==="YES-control"){ok(ref.tours===1&&A.status!=="NO"&&I.status!=="NO")}else{ok(!ref||ref.tours===0);ok(I.status==="NO","hybrid did not refute");if(name!=="previous"){ok(A.status==="UNKNOWN-gap"&&A.rootB===A.rootMin,"expected mean obstruction")}}
 tests.push({name,n:G.n,m:G.E.length,closureRemoved:0,ref,unconditioned:A,hybrid:I});
 }return {tests,scope:"serial, exact BigInt, cap50000 pairs per lane, 12 cuts, overlap3; reference cap1M DFS nodes; no general signing recognition executed"}}
console.log(JSON.stringify(run(),(_,v)=>typeof v==='bigint'?v.toString():v,2));
