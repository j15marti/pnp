function main(){
 const stats={closure_scans:0,closure_deletions:0,branch_nodes:0,cut_candidates:0,cut_splits:0,lift_edge_checks:0,subset_join_attempts:0,signed_quotient_checks:0,critical_direction_checks:0,source_checks:0};
 const assert=(x,msg)=>{if(!x)throw Error(msg)};
 const complete=n=>Array.from({length:n},(_,i)=>Array.from({length:n-i-1},(_,j)=>[i,i+j+1,0])).flat();
 const comps=(n,E,skip=new Set())=>{const a=Array.from({length:n},()=>[]);E.forEach(([u,v],i)=>{if(!skip.has(i)){a[u].push(v);a[v].push(u)}});let id=Array(n).fill(-1),k=0;for(let i=0;i<n;i++)if(id[i]<0){id[i]=k;let q=[i];for(let j=0;j<q.length;j++)for(let v of a[q[j]])if(id[v]<0){id[v]=k;q.push(v)}k++}return [id,k]};
 const check=(E,x)=>{stats.source_checks+=E.length;return E.every(([u,v,s])=>(x[u]^x[v])!==s)};
 // Guard-local arc consistency before each branch, immediately repeat after deletions.
 function exact(n,E){const a=Array.from({length:n},()=>[]);for(let [u,v,s] of E){if(u===v){if(s===0)return null;continue}a[u].push([v,s]);a[v].push([u,s])}
 function solve(D){stats.branch_nodes++;let changed=true;while(changed){changed=false;for(let u=0;u<n;u++)for(let [v,s] of a[u]){stats.closure_scans++;let z=0;for(let c=0;c<4;c++)if((D[u]>>c&1)&&(D[v]&~(1<<(c^s))))z|=1<<c;if(z!==D[u]){stats.closure_deletions++;D[u]=z;if(!z)return null;changed=true}}}
 let u=-1,best=-1;for(let i=0;i<n;i++)if(D[i]&(D[i]-1)){let score=16*a[i].filter(([v])=>!(D[v]&(D[v]-1))).length+a[i].length;if(score>best){best=score;u=i}}
 if(u<0)return D.map(d=>Math.log2(d));for(let c=0;c<4;c++)if(D[u]>>c&1){let d=D.slice();d[u]=1<<c;let r=solve(d);if(r)return r}return null}
 let D=Array(n).fill(15),[id,k]=comps(n,E);for(let j=0;j<k;j++)D[id.indexOf(j)]=1;const x=solve(D);if(x)assert(check(E,x),"exact lift");return x}
 // Exact split by a cut of at most three signed edges; never reuse under external hard pins.
 function cutSolve(n,E){let [id,k]=comps(n,E);let part=k>1?id.map(v=>v===0):null;
 // In an unpinned graph no single vertex color is forced (translation symmetry). 
 // Parallel-edge masks: four distinct forbidden shifts on one pair are unconditional UNSAT.
 const masks=new Map();for(let [u,v,s] of E){if(u===v){if(s===0)return null;continue}let key=[Math.min(u,v),Math.max(u,v)].join(",");let mask=(masks.get(key)||0)|(1<<s);masks.set(key,mask);if(mask===15)return null}
 if(!part){const find=(k,from,S)=>{if(k===0){stats.cut_candidates++;let [a,c]=comps(n,E,new Set(S));return c>1?a.map(v=>v===0):null}for(let i=from;i<=E.length-k;i++){let q=find(k-1,i+1,[...S,i]);if(q)return q}return null};if(n>1)for(let k=1;k<=3&&!part;k++)part=find(k,0,[])}
 if(!part)return exact(n,E);stats.cut_splits++;let A=[],B=[];for(let i=0;i<n;i++)(part[i]?A:B).push(i);assert(A.length&&B.length,"proper split");
 const ia=new Map(A.map((v,i)=>[v,i])),ib=new Map(B.map((v,i)=>[v,i]));let EA=[],EB=[],cross=[];for(let [u,v,s] of E){if(part[u]&&part[v])EA.push([ia.get(u),ia.get(v),s]);else if(!part[u]&&!part[v])EB.push([ib.get(u),ib.get(v),s]);else cross.push([u,v,s])}assert(cross.length<=3,"cut size");
 let x=cutSolve(A.length,EA);if(!x)return null;let y=cutSolve(B.length,EB);if(!y)return null;
 let out=Array(n);A.forEach((v,i)=>out[v]=x[i]);B.forEach((v,i)=>out[v]=y[i]);let mask=0;for(let [u,v,s] of cross){stats.lift_edge_checks++;mask|=1<<(out[u]^out[v]^s)}let t=[0,1,2,3].find(i=>!(mask>>i&1));assert(t!==undefined,"lift shift");B.forEach(v=>out[v]^=t);assert(check(E,out),"cut lift");return out}
 function columns(n,E){let adj=Array.from({length:n},()=>[]),parent=Array.from({length:n},(_,i)=>i),find=x=>{while(parent[x]!==x)x=parent[x];return x},ch=[];E.forEach(([u,v],i)=>{if(find(u)!==find(v)){parent[find(u)]=find(v);adj[u].push([v,i]);adj[v].push([u,i])}else ch.push([u,v,i])});let C=Array(E.length).fill(0);ch.forEach(([u,v,i],j)=>{C[i]|=1<<j;function path(a,p){if(a===v)return true;for(let [b,k] of adj[a])if(b!==p&&path(b,a)){C[k]|=1<<j;return true}return false}assert(path(u,-1),"cycle path")});assert(ch.length<=15,"small explicit tag");return [C,ch.length]}
 function rank(v){let B=[];for(let x of v){while(x){let j=31-Math.clz32(x);if(B[j])x^=B[j];else{B[j]=x;break}}}return B.filter(Boolean).length}
 let seed=2080325;const rnd=n=>{seed=(Math.imul(1664525,seed)+1013904223)>>>0;return seed%n};
 function analyze(n,E,critical,deleted=null){let [C,b]=columns(n,E),m=E.length,tag=(i,d)=>((d&1)?C[i]:0)^((d&2)?C[i]<<b:0);let all=1<<m,dp=Array(all);dp[0]=new Set([0]);let satGroups=0,properSat=0,sepSat=0,nonsepSat=0,greedyCertified=0,signedChecks=0;let maxSupport=0;
 for(let S=1;S<all;S++){let i=31-Math.clz32(S&-S),P=S^(1<<i),R=new Set();for(let t of dp[P])for(let d=1;d<4;d++){stats.subset_join_attempts++;R.add(t^tag(i,d))}dp[S]=R;let ids=Array.from({length:m},(_,i)=>i).filter(i=>S>>i&1);let r=rank(ids.map(i=>C[i]));let saturated=R.size===4**r;let [co,k]=comps(n,E,new Set(ids));let qE=ids.map(i=>[co[E[i][0]],co[E[i][1]],0]);if(saturated){satGroups++;if(S!==all-1)properSat++;if(deleted){if(co[deleted[0]]!==co[deleted[1]])sepSat++;else nonsepSat++}}
 if(critical)assert(!saturated,"critical group saturation");if(deleted&&saturated)assert(co[deleted[0]]!==co[deleted[1]],"neighbor saturation without separation");
 // A 3-degenerate loopless quotient is a polynomial certificate for saturation.
 let live=new Set(Array.from({length:k},(_,i)=>i));let greedy=!qE.some(([u,v])=>u===v);while(greedy&&live.size){let v=[...live].find(v=>qE.filter(([a,b])=>live.has(a)&&live.has(b)&&(a===v||b===v)).length<=3);if(v===undefined){greedy=false;break}live.delete(v)}if(greedy){greedyCertified++;assert(saturated,"greedy certificate")}
 // Independent quotient coloring test: arbitrary syndrome representative a on S.
 // Sample four representative words for every group, including zero.
 for(let j=0;j<4;j++){let target=0;let q=qE.map(([u,v],h)=>{let d=j===0?0:rnd(4);target^=tag(ids[h],d);return [u,v,d]});let x=exact(k,q);stats.signed_quotient_checks++;signedChecks++;assert(!!x===R.has(target),"group coloring iff target attained")}
 maxSupport=Math.max(maxSupport,R.size)
 }
 let full=dp[all-1];if(critical){assert(!full.has(0),"critical zero");for(let i=0;i<m;i++){let x=exact(n,E.filter((_,j)=>j!==i));assert(x&&((x[E[i][0]]^x[E[i][1]])===0),"critical witness");for(let d=1;d<4;d++){stats.critical_direction_checks++;assert(full.has(tag(i,d)),"critical direction")}}}
 let direct=exact(n,E),cut=cutSolve(n,E);assert(!!direct===!!cut&&!!direct===full.has(0),"source decision");return {n,m,cycle_rank:b,decision:!!direct,groups:all-1,saturated_groups:satGroups,proper_saturated_groups:properSat,saturated_separating_deleted_edge:sepSat,saturated_nonseparating_deleted_edge:nonsepSat,greedy_certified_groups:greedyCertified,signed_quotient_checks:signedChecks,full_support:full.size,full_ambient:4**b,max_support:maxSupport};
 }
 let E=complete(5);let k5=analyze(5,E,true);let neighbors=E.map((e,i)=>analyze(5,E.filter((_,j)=>i!==j),false,e));
 let small=[analyze(4,complete(4),false),analyze(5,[[0,1,0],[1,2,0],[2,3,0],[3,4,0],[4,0,0]],false)];
 // Arbitrary signed cut instances, compare independent full search and cut solver.
 let signed={sat:0,unsat:0};for(let j=0;j<100;j++){let n=5+rnd(2),E=complete(n).filter(()=>rnd(7)<4).map(([u,v])=>[u,v,rnd(4)]);let x=exact(n,E),y=cutSolve(n,E);assert(!!x===!!y,"signed cut control");signed[x?"sat":"unsat"]++}
 // Four parallel exclusions are the sharp failure of a uniform four-edge gluing rule.
 let four=Array.from({length:4},(_,s)=>[0,1,s]);assert(!exact(2,four)&&!cutSolve(2,four),"four cut hostile");assert(!!cutSolve(2,four.slice(0,3)),"three cut neighbor");
 // Fano paired CNF controls, independent reference only.
 let F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],clauses=F.flatMap(e=>[[e,1],[e,0]]);let counts=Array.from({length:15},(_,k)=>{let count=0;for(let w=0;w<128;w++)if(clauses.every(([e,b],i)=>i===k-1||e.some(v=>(w>>v&1)===b)))count++;return count});assert(counts[0]===0&&counts.slice(1).every(x=>x===5),"Fano");
 return {seed:2080325,k5,neighbors,small,signed,four_parallel:{full:"UNSAT",deletion:"SAT"},fano_counts:counts,stats};
}
console.log(JSON.stringify(main(),null,2));
