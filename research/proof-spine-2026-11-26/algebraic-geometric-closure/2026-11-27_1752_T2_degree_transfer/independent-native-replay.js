
function check(compiler,corpus,registry,shaCode,traces){
 const compile=Function(compiler.slice(compiler.indexOf("function compile"),compiler.indexOf("function auditLocal"))+";return compile")();
 const sha=Function(shaCode.slice(0,shaCode.indexOf("function compile"))+";return sha")();
 const X=JSON.parse(corpus),Reg=JSON.parse(registry),T=JSON.parse(traces),enc=x=>JSON.stringify(x)+"\n";
 const out=[];
 for(const r of T){
  const x=X.instances.find(i=>i.id===r.name),e=Reg.instances.find(i=>i.alias==="EB-"+r.name),G=compile(x),net=G.network,m=G.source_map,N=net.types.length*4;
  if(sha(enc(net))!==e.sha256||enc(net).length*8!==e.N_bits||sha(x.dimacs)!==e.source_cnf.sha256||x.dimacs.length*8!==e.source_cnf.N_bits||sha(enc(m))!==e.source_map_sha256)throw Error("hash");
  const root=new Int32Array(N).fill(-1),phase=new Uint8Array(N),adj=Array.from({length:N},()=>[]),deg=new Uint8Array(N),pairs=new Set();
  function edge(a,b,s){adj[a].push([b,s]);adj[b].push([a,s])}
  for(const [a,b,s] of net.edges){if(a<0||b<0||a>=N||b>=N||a>>2===b>>2||![0,1].includes(s))throw Error("edge");if(++deg[a]!==1||++deg[b]!==1)throw Error("port degree");let u=a>>2,v=b>>2,k=Math.min(u,v)+":"+Math.max(u,v);if(pairs.has(k))throw Error("parallel");pairs.add(k);edge(a,b,s)}
  if(deg.some(d=>d!==1))throw Error("missing edge");
  for(let v=0;v<net.types.length;v++){if(net.types[v]==="E")for(let j=1;j<4;j++)edge(4*v,4*v+j,0);else if(net.types[v]!=="B")throw Error("type")}
  let traversals=0,components=0;
  for(let v=0;v<N;v++)if(root[v]===-1){components++;let q=[v];root[v]=v;for(let k=0;k<q.length;k++)for(const [u,s] of adj[q[k]]){traversals++;let b=phase[q[k]]^s;if(root[u]===-1){root[u]=v;phase[u]=b;q.push(u)}else if(root[u]!==v||phase[u]!==b)throw Error("affine inconsistency")}}
  const F=m.ternary_clauses,expected=new Map(),real=new Map(),seenCopies=new Set();
  const L=x=>["x"+Math.abs(x),+(x<0)];
  let checkedPorts=0;
  for(let v=0;v<net.types.length;v++)if(net.types[v]==="B"){
   const [kind,parent,i,j,k]=m.vertex_provenance[v];if(kind!=="clause"||parent!==m.original_clause_ids[i]||![0,1].includes(j)||![0,1].includes(k)||seenCopies.has(i+":"+j+":"+k))throw Error("owner");seenCopies.add(i+":"+j+":"+k);
   const [a,b,c]=F[i],z="z"+i,tuple=j?[[z,1],L(c),["f",0],["w"+i+"_1",0]]:[L(a),L(b),[z,0],["w"+i+"_0",0]];
   for(let h=0;h<4;h++){const [id,s]=tuple[h],p=4*v+h,value=[root[p],phase[p]^s];if(expected.has(id)){let a=expected.get(id);if(a[0]!==value[0]||a[1]!==value[1])throw Error("carrier mismatch")}else expected.set(id,value);
    if(real.has(value[0])&&real.get(value[0])!==id)throw Error("different groups merged");real.set(value[0],id);checkedPorts++}
  }
  if(seenCopies.size!==4*F.length)throw Error("copies");
  // Exact original clause vs local ternary split, independent enumeration on each bounded original scope.
  const orig=x.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1));let splitChecks=0,clauseWords=0;const globalAux=new Set();
  for(let i=0;i<orig.length;i++){
   const src=orig[i],parts=F.filter((_,j)=>m.original_clause_ids[j]===i+1),V=[...new Set(src.map(Math.abs))].sort((a,b)=>a-b),U=[...new Set(parts.flat().map(Math.abs))].filter(v=>!V.includes(v));if(V.length+U.length>16||U.some(v=>v<=x.nvars||globalAux.has(v)))throw Error("split scope");for(const v of U)globalAux.add(v);
   const sat=(c,as)=>c.some(l=>as.get(Math.abs(l))===+(l>0));
   for(let w=0;w<2**V.length;w++){clauseWords++;let as=new Map(V.map((v,j)=>[v,w>>j&1])),b=sat(src,as),hit=false;for(let t=0;t<2**U.length;t++){for(let j=0;j<U.length;j++)as.set(U[j],t>>j&1);splitChecks++;if(parts.every(c=>sat(c,as)))hit=true}if(b!==hit)throw Error("split")}
  }
  let truth=0;for(let f=0;f<2;f++)for(let w=0;w<8;w++){let a=(w&1)^f,b=(w>>1&1)^f,c=(w>>2&1)^f,hit=false;for(let z=0;z<2;z++)for(let u=0;u<2;u++)for(let t=0;t<2;t++){truth++;if(a+b+z+u===2&&1-z+c+f+t===2)hit=true}if(hit!==Boolean(w))throw Error("gadget")}
  // Reverse-list propagation with explicit assignment consistency, not the discovery routine.
  let reads=0;function conflict(C,pins){const vals=new Map();for(const l of pins){const v=Math.abs(l),b=l>0;if(vals.has(v)&&vals.get(v)!==b)return true;vals.set(v,b)}
   for(;;){let changed=false;for(let i=C.length-1;i>=0;i--){let satisfied=false,un=[];for(const l of C[i]){reads++;let v=Math.abs(l);if(!vals.has(v))un.push(l);else if(vals.get(v)===(l>0)){satisfied=true;break}}if(satisfied)continue;if(!un.length)return true;if(un.length===1){vals.set(Math.abs(un[0]),un[0]>0);changed=true}}if(!changed)return false}}
  const C=orig.slice(),trace=r.direct.trace;if(!r.direct.no)throw Error("no contradiction asserted");for(const c of trace){if(!conflict(C,c.map(x=>-x)))throw Error("learned row");C.push(c)}if(!conflict(C,[]))throw Error("terminal");
  out.push({name:r.name,instance:e.short_id,instance_id:e.instance_id,N:e.N_bits,cnf:e.source_cnf,guard_id:"EMPTY",residual_id:"ROOT",source_pin:"registry 0c14cdc57925788cf7a451dcd5aa171dce860f2c; corpus e315349cd6c1fe3fa696504859f28312f6aab69a; compiler 21b9d53fb8166c819b24e708656c742cd3c24f10",original_ids:{vertices:[0,net.types.length-1],ports:[0,N-1],edges:[0,net.edges.length-1],clauses:[1,orig.length]},components,traversals,checkedPorts,groupCount:expected.size,splitChecks,clauseWords,gadgetTruthChecks:truth,traceLength:trace.length,reverseUPReads:reads,rootPhaseHash:sha(enc({root:Array.from(root),phase:Array.from(phase)})),groupMapHash:sha(enc([...expected])),trace,sourceOnlyCNFDiscovery:r.direct.work,nativeDiscovery:r.local.work})
 }
 return out
}
if(typeof module!=="undefined"){module.exports=check;if(require.main===module){const fs=require("fs");console.log(JSON.stringify(check(...process.argv.slice(2).map(p=>fs.readFileSync(p,"utf8"))),null,2))}}
