function run(){
 const compile=F=>{
  const types=[],used=[],edges=[],groups=new Map(),reps={};
  const V=t=>{types.push(t);used.push(0);return types.length-1};
  const P=v=>{if(used[v]===4)throw Error("port overflow");return 4*v+used[v]++};
  const E=(a,b,s=0)=>edges.push([a,b,s]);
  const wire=(a,b,s)=>{let v=Array.from({length:5},()=>V("E"));for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)if(i!==0||j!==1)E(P(v[i]),P(v[j]));E(a,P(v[0]),s);E(b,P(v[1]));};
  const occ=(id,s,p)=>{if(!groups.has(id))groups.set(id,[]);groups.get(id).push([p,s])};
  for(let i=0;i<F.length;i++){let [a,b,c]=F[i],z="z"+i,L=x=>["x"+Math.abs(x),+(x<0)],T=[[L(a),L(b),[z,0]],[[z,1],L(c),["f",0]]];for(let j=0;j<2;j++)for(let r=0;r<2;r++){let v=V("B");for(let [id,s] of T[j])occ(id,s,P(v));occ("w"+i+"_"+j,0,P(v));}}
  for(let [id,O] of groups){if(O.length%2||O.length<2)throw Error("occurrence parity");reps[id]=O[0];if(O.length===2){wire(O[0][0],O[1][0],O[0][1]^O[1][1]);continue;}let a=Array.from({length:(O.length-2)/2},()=>V("E"));for(let i=1;i<a.length;i++)wire(P(a[i-1]),P(a[i]),0);let k=0;for(let v of a)while(used[v]<4){let [p,s]=O[k++];wire(P(v),p,s);}if(k!==O.length)throw Error("fanout");}
  let seen=new Set(),ports=new Set();for(let [a,b,s] of edges){let u=a>>2,v=b>>2,k=Math.min(u,v)+":"+Math.max(u,v);if(u===v||seen.has(k)||ports.has(a)||ports.has(b))throw Error("graph simplicity");seen.add(k);ports.add(a);ports.add(b);}
  if(used.some(x=>x!==4)||ports.size!==4*types.length)throw Error("degree");return {types,edges,reps};
 };
 const decode=G=>{
  let n=4*G.types.length,A=Array.from({length:n},()=>[]);
  const edge=(a,b,s)=>{A[a].push([b,s]);A[b].push([a,s]);};
  for(let [a,b,s] of G.edges)edge(a,b,s);
  for(let i=0;i<G.types.length;i++)if(G.types[i]==="E")for(let j=1;j<4;j++)edge(4*i,4*i+j,0);
  let C=Array(n).fill(-1),S=Array(n).fill(0),k=0;
  for(let i=0;i<n;i++)if(C[i]===-1){let q=[i];C[i]=k;for(let j=0;j<q.length;j++){let a=q[j];for(let [b,s] of A[a])if(C[b]===-1){C[b]=k;S[b]=S[a]^s;q.push(b);}else if(S[b]!== (S[a]^s))throw Error("inconsistent wiring");}k++;}
  let R=[];for(let i=0;i<G.types.length;i++)if(G.types[i]==="B")R.push(Array.from({length:4},(_,j)=>[C[4*i+j],S[4*i+j]]));
  let calls=0;
  const solve=f=>{
   let a=Array(k).fill(-1);for(let [id,b] of Object.entries(f)){if(!(id in G.reps))continue;let [p,s]=G.reps[id],v=b^s^S[p];if(a[C[p]]!==-1&&a[C[p]]!==v)return false;a[C[p]]=v;}
   function rec(a){if(++calls>100000)throw Error("reference budget");let change=true;while(change){change=false;for(let r of R){let U=[...new Set(r.filter(([i])=>a[i]<0).map(([i])=>i))],valid=[];for(let m=0;m<(1<<U.length);m++){let sum=0;for(let [i,s] of r)sum+=(a[i]<0?((m>>U.indexOf(i))&1):a[i])^s;if(sum===2)valid.push(m);}if(!valid.length)return null;for(let j=0;j<U.length;j++){let v=(valid[0]>>j)&1;if(valid.every(m=>((m>>j)&1)===v)){a[U[j]]=v;change=true;}}}}
    let i=a.indexOf(-1);if(i<0)return a;for(let b=0;b<2;b++){let c=a.slice();c[i]=b;let w=rec(c);if(w)return w;}return null;}
   let w=rec(a);if(!w)return false;let B=C.map((i,p)=>w[i]^S[p]);for(let [p,q,s] of G.edges)if((B[p]^B[q])!==s)throw Error("edge witness");for(let i=0;i<G.types.length;i++){let z=B.slice(4*i,4*i+4).reduce((x,y)=>x+y,0);if(G.types[i]==="B"?z!==2:z!==0&&z!==4)throw Error("node witness");}for(let [id,b] of Object.entries(f))if(id in G.reps){let [p,s]=G.reps[id];if((B[p]^s)!==b)throw Error("fixed witness");}return true;
  };return {solve,calls:()=>calls};
 };
 let seed=20261124;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n);};
 const sat=(F,m)=>F.every(c=>c.some(l=>Boolean((m>>(Math.abs(l)-1))&1)===(l>0)));
 const Fgen=(n,m)=>Array.from({length:m},()=>Array.from({length:3},()=> (1+rnd(n))*(rnd(2)?1:-1)));
 let checks=0,yes=0,no=0,vertices=0,dfsCalls=0;
 for(let t=0;t<48;t++){let n=2+rnd(3),F=Fgen(n,1+rnd(4)),G=compile(F),D=decode(G);vertices+=G.types.length;for(let m=0;m<(1<<n);m++)for(let a=0;a<2;a++){let f={f:a};for(let j=1;j<=n;j++)f["x"+j]=((m>>(j-1))&1)^a;let got=D.solve(f);if(got!==sat(F,m))throw Error("pointwise mismatch");checks++;yes+=+got;no+=+!got;}dfsCalls+=D.calls();}
 let gdChecks=0,gdSat=0,gdDfsCalls=0;
 for(let t=0;t<12;t++){let n=3,F=Fgen(n,1+rnd(3)),s=4,u=5,Q=[[s,s,s],[-u,-u,-u]];for(let j=0;j<F.length;j++){let a=6+2*j,b=a+1,[l1,l2,l3]=F[j];Q.push([l1,-s,a],[l2,-a,b],[l3,-b,u]);}let D=decode(compile(Q));for(let m=0;m<8;m++){let f={f:0};for(let j=1;j<=n;j++)f["x"+j]=(m>>(j-1))&1;let g=D.solve(f);if(g!==sat(F,m))throw Error("GD mismatch");gdChecks++;gdSat+=+g;}gdDfsCalls+=D.calls();}
 let scaling=[];for(let n of [4,8,16,32,64,128]){let F=[[1,1,1]];for(let j=1;j<n;j++)F.push([-j,j+1,j+1]);F.push([-n,-n,-n]);let G=compile(F),H=F.slice();H[H.length-1]=[n,n,n];let K=compile(H),D=decode(K),f={f:0};for(let j=1;j<=n;j++)f["x"+j]=1;if(!D.solve(f))throw Error("SAT neighbor");let smallUnsat=null;if(n<=4){let U=decode(G);smallUnsat=!U.solve({f:0});if(!smallUnsat)throw Error("UNSAT chain");}scaling.push({n,clauses:F.length,vertices:G.types.length,edges:G.edges.length,smallUnsat,verifiedSatNeighbor:true});}
 return {seed:20261124,randomGraphs:48,randomGraphVertices:vertices,pointwiseChecks:checks,yes,no,dfsCalls,guardedGraphs:12,gdChecks,gdSat,gdUnsat:gdChecks-gdSat,gdDfsCalls,scaling,errors:0};
}
console.log(JSON.stringify(run(),null,2));
