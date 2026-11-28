function controls(sha){
 const cycles=[],native=[];
 // Explicit versioned signed binary energy: E=sum_i [x_i XOR x_(i+1) != s_i].
 for(const n of [3,5,7,9,16,32,64,128]){
  let G={format:"SIGNED-PAIR-ENERGY-v1",variables:n,edges:Array.from({length:n},(_,i)=>[i,(i+1)%n,Number(i===n-1)])},bytes=JSON.stringify(G)+"\n",h=sha(bytes);
  // Relaxation: each unpinned incidence has independent bit; only edges with both endpoints pinned can incur a defect.
  let tests=0,collisions=0,fullMin=null;
  if(n<=9)for(let mask=0;mask<2**n;mask++){let vs=Array.from({length:n},(_,i)=>i).filter(i=>mask>>i&1),min=Infinity;for(let w=0;w<2**vs.length;w++){let E=0;for(let [a,b,s] of G.edges)if((mask>>a&1)&&(mask>>b&1))E+=Number((((w>>vs.indexOf(a))&1)^((w>>vs.indexOf(b))&1))!==s);min=Math.min(min,E);tests++}if(min!==Number(mask===2**n-1))throw Error("sync counterexample check");if(mask!==2**n-1)collisions++;else fullMin=min}
  // Independent GF2 cycle cancellation: XOR of all lhs=0, RHS=1. Explicit witness x=0 achieves energy1.
  let deg=Array(n).fill(0),rhs=0;for(let [a,b,s] of G.edges){deg[a]^=1;deg[b]^=1;rhs^=s}if(deg.some(Boolean)||rhs!==1)throw Error("cycle check");
  cycles.push({problem_id:G.format,instance:"PAIR-CYCLE-NO-"+n+"@"+h.slice(0,12),instance_id:G.format+":sha256:"+h,original_N_bits:bytes.length*8,guard_id:"EMPTY",residual_id:"ROOT",original_ids:{variables:[0,n-1],edges:[0,n-1]},parents:[],exactMin:1,splitPlan:"all variable occurrences cloned independently",properSyncSubsetsZero:collisions,enumeratedAssignments:tests,fullMin,graph:G,proof:"XOR of all edges inconsistent; all-zero witness cost1. For proper synchronized S, induced subgraph on S is a forest, assign each path consistently; every edge with an unpinned endpoint can use a private incidence bit. All S proper have relaxed min0; full S restores exact min1. Affine elimination bypasses this restricted plan."})
 }
 function make(r,yes){let types=[],edges=[];for(let c=0;c<r;c++){const base=5*c,next=Array(5).fill(0);types.push("B","E","E","E","E");for(let i=0;i<5;i++)for(let j=i+1;j<5;j++){let a=4*(base+i)+next[i]++,b=4*(base+j)+next[j]++,s=Number(yes&&i===0&&j<=2);edges.push([a,b,s])}}return {format:"STRICT-EB4-v1",types,edges}}
 for(let n of [1,2,4,8,16])for(let yes of [false,true]){
   let G=make(n,yes),bytes=JSON.stringify(G)+"\n",h=sha(bytes),bits=Array(4*G.types.length).fill(0),deg=Array(bits.length).fill(0),vs=new Set();for(let [a,b,s] of G.edges){if(++deg[a]!==1||++deg[b]!==1)throw Error("port");let k=[Math.floor(a/4),Math.floor(b/4)].join(",");if(vs.has(k))throw Error("parallel");vs.add(k);if(G.types[Math.floor(a/4)]==="B")bits[a]=s;else if(G.types[Math.floor(b/4)]==="B")bits[b]=s;else if(s)throw Error("E sign")}
   if(deg.some(d=>d!==1))throw Error("dangling");for(let [a,b,s] of G.edges)if((bits[a]^bits[b])!==s)throw Error("edge");let cost=0;for(let v=0;v<G.types.length;v++){let a=bits.slice(4*v,4*v+4);if(G.types[v]==="E"){if(a.some(x=>x!==a[0]))throw Error("E")}else cost+=Number(a.reduce((s,x)=>s+x,0)!==2)}if(cost!==(yes?0:n))throw Error("cost");
   // Per connected K4 of E vertices, signs zero and equality force one common bit. Both gauge choices checked.
   let checked=0;for(let c=0;c<n;c++)for(let b of [0,1]){let x=Array(20).fill(b);for(let [a,q,s] of G.edges.slice(10*c,10*c+10)){if(G.types[Math.floor(a/4)]==="B")x[a-20*c]=b^s;if((x[a-20*c]^x[q-20*c])!==s)throw Error("bad local")};let k=x.slice(0,4).reduce((s,x)=>s+x,0);if(Number(k!==2)!==Number(!yes))throw Error("bad min");checked++}
   native.push({problem_id:G.format,instance:"FP58-K5-"+(yes?"YES":"NO")+"-"+n+"@"+h.slice(0,12),instance_id:G.format+":sha256:"+h,original_N_bits:bytes.length*8,guard_id:"EMPTY",residual_id:"ROOT",original_ids:{vertices:[0,G.types.length-1],ports:[0,bits.length-1],edges:[0,G.edges.length-1]},parents:[],exactMin:cost,checkedLocalGauges:checked,graph:G,witness:bits,proof:"Each component is K5 with one B and four E. K4 of E vertices forces common bit; signs into B fix occupancy to 0/4 (NO) or exactly2 (YES), both gauges. Independent components add costs. Unscaled integer energy required for odd instances."})
 }
 return {cycles,native};
}
if(typeof module!=="undefined")module.exports={controls};
