function run(){
 const assert=(v,m)=>{if(!v)throw Error(m)};
 const out={seed:"deterministic",graphs:[],guarded_decisions:0,colour_search_nodes:0,closure_passes:0,domain_deletions:0,forest_count_checks:0,cluster_count_checks:0,path_countermodels:0,critical_repair_witnesses:0,one_event_affine_closure_checks:0,failures:0};
 const pairs=n=>Array.from({length:n},(_,i)=>i).flatMap(i=>Array.from({length:n-i-1},(_,j)=>[i,i+j+1]));
 const cycle=n=>({n,E:Array.from({length:n},(_,i)=>[i,(i+1)%n])});
 function myc(G){const {n,E}=G;return {n:2*n+1,E:[...E,...E.flatMap(([u,v])=>[[u,n+v],[v,n+u]]),...Array.from({length:n},(_,i)=>[n+i,2*n])]}}
 function girth({n,E}){let g=Infinity;for(let k=0;k<E.length;k++){let [s,t]=E[k],dist=Array(n).fill(-1),q=[s];dist[s]=0;for(let i=0;i<q.length;i++)for(let j=0;j<E.length;j++)if(j!==k){let [u,v]=E[j];let w=u===q[i]?v:v===q[i]?u:-1;if(w>=0&&dist[w]<0){dist[w]=dist[q[i]]+1;q.push(w)}}if(dist[t]>=0)g=Math.min(g,dist[t]+1)}return g}
 function* subsets(n,k,start=0,a=[]){yield a;if(k)for(let i=start;i<n;i++)yield* subsets(n,k-1,i+1,[...a,i])}
 // XOR constraints exact solution count and actual representative via graph traversal.
 function affine(n,eq){const A=Array.from({length:n},()=>[]);for(const [u,v,d] of eq){A[u].push([v,d]);A[v].push([u,d])}let x=Array(n).fill(-1),c=0;for(let s=0;s<n;s++)if(x[s]<0){c++;x[s]=0;let q=[s];for(let i=0;i<q.length;i++)for(const [v,d] of A[q[i]]){let z=x[q[i]]^d;if(x[v]<0){x[v]=z;q.push(v)}else if(x[v]!==z)return {count:0n,x:null}}}return {count:4n**BigInt(c),x}}
 const bits=m=>[0,1,2,3].filter(c=>m&(1<<c));
 function solve(n,E,e,d){
  let [u,v]=e,initial=Array(n).fill(15);initial[u]=1;initial[v]=1<<d;
  const adj=Array.from({length:n},()=>[]);for(const [a,b] of E){adj[a].push(b);adj[b].push(a)}
  function rec(D){out.colour_search_nodes++;let change=true;while(change){change=false;out.closure_passes++;for(const [a,b] of E)for(const [i,j] of [[a,b],[b,a]]){if(D[j]===0)return null;if((D[j]&(D[j]-1))===0&&(D[i]&D[j])){D[i]&=~D[j];out.domain_deletions++;change=true;if(!D[i])return null}}}
   let z=-1;for(let i=0;i<n;i++)if(bits(D[i]).length>1&&(z<0||bits(D[i]).length<bits(D[z]).length||(bits(D[i]).length===bits(D[z]).length&&adj[i].length>adj[z].length)))z=i;
   if(z<0)return D.map(m=>bits(m)[0]);for(const c of bits(D[z])){let next=D.slice();next[z]=1<<c;let w=rec(next);if(w)return w}return null}
  let x=rec(initial);out.guarded_decisions++;if(x)assert((x[u]^x[v])===d&&E.every(([a,b])=>x[a]!==x[b]),"witness");return x
 }
 function check(name,H,critical,selected,clusterSize){
  const g=girth(H),n=H.n,record={name,n,m:H.E.length,girth:g,guarded_sat:0,guarded_unsat:0,deleted_edges:[],group_sizes:null};out.graphs.push(record);
  for(const k of selected){const e=H.E[k],E=H.E.filter((_,i)=>i!==k),bound=g-2;const ws=[];
   for(const d of [0,1,2,3]){const w=solve(n,E,e,d);ws.push(w);if(w)record.guarded_sat++;else record.guarded_unsat++;if(critical)assert(!!w===(d===0),"critical guard label")}
   record.deleted_edges.push({index:k,guard_sat:ws.map(Boolean)});
   // Full forest-intersection counts for the first selected deletion only; no sample masquerading as full graph testing.
   if(k===selected[0])for(const d of [0,1,2,3])for(const J of subsets(E.length,bound)){
    const z=affine(n,[[...e,d],...J.map(j=>[...E[j],0])]);assert(z.count===4n**BigInt(n-1-J.length),"forest count");out.forest_count_checks++;
    if(J.length===1){assert(z.count*4n===4n**BigInt(n-1),"one-event closure");out.one_event_affine_closure_checks++}
   }
   if(critical&&k===selected[0]){ // each retained edge f has a witness after its deletion, with e nonzero fixed to 1.
    for(let j=0;j<E.length;j++){let w=solve(n,E.filter((_,i)=>i!==j),e,1);assert(w&&w[E[j][0]]===w[E[j][1]],"critical repair witness");out.critical_repair_witnesses++}
   }
   if(clusterSize&&k===selected[0]){
    let C=[];for(let i=0;i<E.length;i+=clusterSize)C.push(Array.from({length:Math.min(clusterSize,E.length-i)},(_,j)=>i+j));record.group_sizes=C.map(c=>c.length);
    assert(C.length>=6&&Math.max(2*clusterSize,clusterSize+2)<=bound,"cluster precondition");
    for(let d=0;d<4;d++){
     const M=4n**BigInt(n-1);
     function avoid(J){let sum=0n;for(const K of subsets(J.length,J.length)){let x=affine(n,[[...e,d],...K.map(k=>[...E[J[k]],0])]).count;sum+=K.length%2?-x:x}return sum}
     const p=C.map(J=>M-avoid(J));
     for(let i=0;i<C.length;i++)for(let j=i+1;j<C.length;j++){const pij=M-avoid(C[i])-avoid(C[j])+avoid([...C[i],...C[j]]);assert(pij*M===p[i]*p[j],"cluster independence");out.cluster_count_checks++}
     // Check every ordered triple of distinct clusters can violate path convexity, retaining the guard.
     for(let i=0;i<C.length;i++)for(let j=0;j<C.length;j++)for(let h=0;h<C.length;h++)if(i!==j&&i!==h&&j!==h){const a=E[C[i][0]],b=E[C[j][0]],mid=C[h].map(z=>E[z]);let x=affine(n,[[...e,d],[...a,0],[...b,0],...mid.map(z=>[...z,1])]).x;assert(x&&(x[e[0]]^x[e[1]])===d&&x[a[0]]===x[a[1]]&&x[b[0]]===x[b[1]]&&mid.every(([u,v])=>x[u]!==x[v]),"path countermodel");out.path_countermodels++}
     const mx=p.reduce((a,b)=>a>b?a:b),s=p.reduce((a,b)=>a+b,0n)-mx;
     assert(mx*M+(M-mx)*s>M*M,"Hunter fails");
    }
   }
  }
 }
 check("K5",{n:5,E:pairs(5)},true,[0,1,2,3,4,5,6,7,8,9],0);
 const G=myc(myc(cycle(5)));check("Mycielski^2(C5)",G,true,[0,1,2,3,4,5,6,7],0);
 check("C13 (noncritical control)",cycle(13),false,[0],2);
 return out
}
console.log(JSON.stringify(run(),null,2));
