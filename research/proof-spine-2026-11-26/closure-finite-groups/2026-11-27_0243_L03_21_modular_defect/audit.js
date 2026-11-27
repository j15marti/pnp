function audit(){
 const assert=(a,m)=>{if(!a)throw Error(m)};
 const mod=(x,n)=>(x%n+n)%n;
 const arr=n=>Array.from({length:n},(_,i)=>i);
 function make(n,t){
   const cap=n/2-1, edges=[];
   for(let i=0;i<n;i++)for(let j=0;j<n;j++)edges.push([i,j,(i+j)%n]);
   for(let i=0;i<cap;i++)edges.push([i,mod(-i,n),1]);
   const guard=arr(cap-t).map(i=>n*n+t+i), active=edges.map((e,id)=>({e,id})).filter(({id})=>id<n*n+t);
   const groups=Array.from({length:3*n},()=>[]);
   edges.forEach((e,id)=>e.forEach((v,d)=>groups[d*n+v].push(id)));
   const parentClauses=groups.reduce((s,g)=>s+1+g.length*(g.length-1)/2,0)+guard.length;
   const residual=groups.map(g=>g.filter(id=>id<n*n+t));
   const residualClauses=residual.reduce((s,g)=>s+1+g.length*(g.length-1)/2,0);
   assert(residual.every(g=>g.length>=2),"UP stable after guards");
   let h=2166136261;
   for(const e of edges)for(const v of e)h=Math.imul(h^v,16777619)>>>0;
   for(const id of guard)h=Math.imul(h^id,16777619)>>>0;
   // Exact simple bit encoding: unary-length-prefixed n, t not needed; fixed widths for triples, guard bitmap.
   const k=Math.ceil(Math.log2(n));
   const bits=2*Math.floor(Math.log2(n))+1+2*Math.floor(Math.log2(edges.length))+1+3*k*edges.length+edges.length;
   return {n,t,edges,active,guard,groups,residual,parentClauses,residualClauses,bits,fingerprint:h.toString(16).padStart(8,"0")};
 }
 function verifyMatching(F,ids){
   assert(ids.length===F.n,"matching size");
   const rows=new Set(),cols=new Set(),c=Array(F.n).fill(0);
   for(const id of ids){assert(id>=0&&id<F.n*F.n+F.t,"guard/ID");const [i,j,k]=F.edges[id];rows.add(i);cols.add(j);c[k]++}
   assert(rows.size===F.n&&cols.size===F.n,"matching endpoints");return c;
 }
 const base=(n,c)=>arr(n).map(i=>i*n+mod(c-i,n));
 // Replica A: actual fractional witness, signed integral/field witness from explicit matching differences.
 function relaxation(F){
   const n=F.n, v=Array(F.edges.length).fill(0);
   const mix=Array(n).fill(0);
   for(let c=0;c<n;c++){const w=verifyMatching(F,base(n,c));w.forEach((x,i)=>mix[i]+=x)}
   assert(mix.every(x=>x===n),"fractional witness");
   let verified= n;
   function add(ids,k){verifyMatching(F,ids);verified++;for(const id of ids)v[id]+=k}
   add(base(n,0),1);
   for(let c=0;c<n-2;c++){
     const rest=arr(n).filter(j=>j!==c&&j!==c+1), p=[c,c+1,...rest], q=[c+1,c,...rest];
     const k=(n-1-c)*(n-2-c)/2;
     add(p.map((j,i)=>i*n+j),k); add(q.map((j,i)=>i*n+j),-k);
   }
   if(F.t){const p=base(n,0),q=p.slice();q[0]=n*n;const k=n*(n-1)/2;add(q,k);add(p,-k)}
   const sums=F.groups.map(g=>g.reduce((s,id)=>s+v[id],0));
   assert(sums.every(x=>mod(x,2)===1),"GF2 witness");
   if(F.t)assert(sums.every(x=>x===1),"integer lattice witness");
   assert(F.guard.every(id=>v[id]===0),"signed witness respects guard");
   return {fractional:true,gf2:true,integerWitness:F.t>0,verifiedMatchings:verified,maxAbs:Math.max(...v.map(Math.abs))};
 }
 // Replica B: direct modular constraint check, not range-based matching optimization.
 function rawModular(F){
   const n=F.n, diff=F.active.map(({e:[i,j,c]})=>mod(c-i-j,n));
   return {zeroDefects:diff.every(x=>x===0),target:n/2,defectEdges:diff.filter(x=>x!==0).length};
 }
 // Replica C: enumerate the actual matching set under a fixed cap on original size.
 function enumerate(F){
   const n=F.n;if(n>8)return {status:"NOT_RUN_size_cap"};
   let count=0,min=Infinity,max=-1,found=false,states=new Set(),nodes=0,modSet=new Set();
   const c=Array(n).fill(0);
   function rec(i,used,d){
     if(++nodes>1000000)throw Error("enumeration cap");
     if(i===n){count++;min=Math.min(min,d);max=Math.max(max,d);let mask=0;for(let j=0;j<n;j++)if(c[j]%2)mask|=1<<j;states.add(mask);modSet.add(mod(c.reduce((s,x,j)=>s+x*j,0),n));if(c.every(x=>x===1))found=true;return}
     for(let j=0;j<n;j++)if(!(used>>j&1)){
       const k=(i+j)%n;c[k]++;rec(i+1,used|1<<j,d);c[k]--;
       if(i<F.t&&j===mod(-i,n)){c[1]++;rec(i+1,used|1<<j,d+1);c[1]--}
     }
   }
   rec(0,0,0);assert(!found&&min===0&&max===F.t,"reference NO/range");
   assert([...modSet].every(d=>d<=F.t),"reference modular residues");
   return {status:"NO",count,nodes,syndromes:states.size,min,max,residues:[...modSet].sort((a,b)=>a-b)};
 }
 // Hybrid: transform edges using original label potentials, then verify range with a dual upper certificate
 // (row potentials max edge cost, column potentials zero) and attainable extrema.
 function hybrid(F){
   const n=F.n,w=Array(n).fill(0);
   for(const {e:[i,j,c]} of F.active)w[i]=Math.max(w[i],mod(c-i-j,n));
   const U=w.reduce((a,b)=>a+b,0),L=0,delta=mod(n*(n-1)/2-n*(n-1),n);
   const low=base(n,0),high=low.slice();for(let i=0;i<F.t;i++)high[i]=n*n+i;
   verifyMatching(F,low);verifyMatching(F,high);
   function score(ids){return ids.reduce((s,id)=>{let [i,j,c]=F.edges[id];return s+mod(c-i-j,n)},0)}
   assert(score(low)===L&&score(high)===U,"dual extrema attained");
   assert(delta>U&&L===0,"range contradiction");
   return {L,U,delta,scans:F.active.length,rangeExclusion:true};
 }
 const out=[];
 for(const n of [4,8,16,32,64]){
   for(const t of [...new Set([0,1,n/2-1])]){
     const F=make(n,t),A=relaxation(F),B=rawModular(F),C=enumerate(F),H=hybrid(F);
     out.push({n,t,parentVariables:F.edges.length,activeVariables:F.active.length,guardCount:F.guard.length,parentClauses:F.parentClauses,residualClauses:F.residualClauses,sourceBits:F.bits,fingerprint:F.fingerprint,A,B,C,H});
   }
 }
 // One minimal YES soundness control: odd order n=3 and diagonal permutation (i,i) realizes each color once.
 assert(new Set(arr(3).map(i=>2*i%3)).size===3,"odd order control");
 return out;
}
console.log(JSON.stringify(audit(),null,2));
