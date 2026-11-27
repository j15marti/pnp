const fs=require('fs');
function verify(inputs,results){
 const [co,corpus,reg,base,...parents]=inputs, A=(x,m)=>{if(!x)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const compile=new Function(co.slice(co.indexOf("function compile("),co.indexOf("function auditLocal"))+";return compile;")();
 const {sha,normalize,independentNormalize,eliminate,verifyTrace,gauge}=new Function(base.slice(0,base.indexOf("function runCase"))+";return {sha,normalize,independentNormalize,eliminate,verifyTrace,gauge};")();
 const registry=JSON.parse(reg),entries=registry.instances||registry.native_instances||Object.values(registry).find(x=>Array.isArray(x)&&x.some(y=>y.alias==="EB-JOINT-24")),d=JSON.parse(corpus);
 function pin(F,v){return F.map(f=>{let j=f.vs.indexOf(v);if(j<0)return f;return {...f,vs:f.vs.filter(x=>x!==v),ok:f.ok.filter(w=>!(w>>j&1)).map(w=>(w&((1<<j)-1))|((w>>(j+1))<<j))}})}
 function clause(c,id){let vs=[...new Set(c.map(Math.abs))].sort((a,b)=>a-b),ok=[];for(let w=0;w<2**vs.length;w++)if(c.some(l=>(w>>vs.indexOf(Math.abs(l))&1)===+(l>0)))ok.push(w);return {id,vs,ok}}
 function check(F,events){
  const V=[...new Set(F.flatMap(f=>f.vs))].sort((a,b)=>a-b),n=V.length,idx=new Map(V.map((x,i)=>[x,i])),b=i=>1n<<BigInt(i);
  let M=new Map(),D=n+1;for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)M.set(i+","+j,D++);
  const p=(i,j)=>i===j?i+1:M.get(Math.min(i,j)+","+Math.max(i,j));
  let stats={rowScans:0,localChecks:0,eliminationXors:0,products:0,closureCalls:0,guardChecks:0},root=new Map(),F0=F.map(f=>({vs:f.vs.map(v=>idx.get(v)),ok:f.ok}));
  // Row elimination with explicit column loops (different from discovery's highest-pivot dictionary).
  function rref(rows,k){let R=[...new Set(rows)].filter(v=>v!==0n),r=0,piv=[];for(let j=k-1;j>=0;j--){let i=R.findIndex((w,i)=>i>=r&&!!(w&b(j)));if(i<0)continue;[R[r],R[i]]=[R[i],R[r]];let a=R[r];for(let t=0;t<R.length;t++)if(t!==r&&(R[t]&b(j))){R[t]^=a;stats.eliminationXors++}piv.push(j);r++}return {rows:R.slice(0,r),piv}}
  function parity(w){let q=0;while(w){q^=1;w&=w-1n}return q}
  function close(a){stats.closureCalls++;for(;;){
   let rows=[],changed=false,R=[];
   for(let f of F0){let ok=[];for(let w of f.ok){stats.rowScans++;if(f.vs.every((v,i)=>!a.has(v)||a.get(v)===(w>>i&1)))ok.push(w)}if(!ok.length)return true;R.push(ok);for(let j=0;j<f.vs.length;j++){let v=f.vs[j],z=ok[0]>>j&1;if(!a.has(v)&&ok.every(w=>(w>>j&1)===z)){a.set(v,z);changed=true}}}
   if(changed)continue;
   for(let [i,v]of a)rows.push(b(i+1)^(v?1n:0n));
   for(let fi=0;fi<F0.length;fi++){let f=F0[fi],free=f.vs.map((v,i)=>[v,i]).filter(([v])=>!a.has(v)),k=free.length,cols=[0,...free.map(x=>x[0]+1)],pairs=[];
    for(let i=0;i<k;i++)for(let j=i+1;j<k;j++){pairs.push([i,j]);cols.push(p(free[i][0],free[j][0]))}
    let E=R[fi].map(w=>{let z=1n;for(let i=0;i<k;i++)if(w>>free[i][1]&1)z|=b(i+1);for(let t=0;t<pairs.length;t++){let [i,j]=pairs[t];if((w>>free[i][1]&1)&&(w>>free[j][1]&1))z|=b(k+1+t)}return z});
    let L=rref(E,cols.length);
    for(let j=0;j<cols.length;j++)if(!L.piv.includes(j)){let z=b(j);for(let i=0;i<L.rows.length;i++)if(L.rows[i]&b(j))z|=b(L.piv[i]);for(let w of E){stats.localChecks++;A(!parity(z&w),"annihilator invalid")}let g=0n;for(let i=0;i<cols.length;i++)if(z&b(i))g|=b(cols[i]);rows.push(g)}
   }
   let Q=rref(rows,D),done=new Set();
   for(let e=0;e<=n+1;e++){if(Q.rows.includes(1n))return true;let add=[];
    for(let z of Q.rows)if(z<(1n<<BigInt(n+1))&&!done.has(z)){done.add(z);for(let j=0;j<n;j++)if(!a.has(j)){let q=0n;if(z&1n)q^=b(j+1);for(let i=0;i<n;i++)if(z&b(i+1))q^=b(p(i,j));stats.products++;add.push(q)}}
    if(!add.length)break;let old=Q.rows.length;Q=rref([...Q.rows,...add],D);if(old===Q.rows.length)break;
   }
   if(Q.rows.includes(1n))return true;
   for(let i=0;i<n;i++)if(!a.has(i)){let x=b(i+1);if(Q.rows.includes(x)||Q.rows.includes(x^1n)){a.set(i,+(Q.rows.includes(x^1n)));changed=true}}
   if(!changed)return false;
  }}
  for(let ev of events){if(close(root))return {valid:true,early:true,stats};let [v,bit]=ev.pin,i=idx.get(v);A(i!==undefined,"unknown guard");if(root.has(i)){A(root.get(i)!==bit,"guard already forced opposite of claim");continue}let a=new Map(root);a.set(i,bit);stats.guardChecks++;A(close(a),"conditional contradiction failed "+JSON.stringify(ev));root.set(i,1-bit)}
  return {valid:close(root),early:false,stats};
 }
 let out=[],artifacts=[];
 for(let k=0;k<2;k++){let s=results.shared[k],entry=entries.find(e=>e.alias==="EB-"+s.id),x=d.instances.find(x=>x.id===s.id),g=compile(x),native=JSON.stringify(g.network)+"\n";A(sha(native)===entry.sha256&&native.length*8===entry.N_bits&&sha(x.dimacs)===entry.source_cnf.sha256&&sha(JSON.stringify(g.source_map)+"\n")===entry.source_map_sha256,"hash");
  let N=independentNormalize(g.network),D=normalize(g.network);A(eq(N.fs,D.fs),"quotient");let v=gauge(D.fs),E=eliminate(pin(D.fs,v),false),B=verifyTrace(pin(N.fs,v),E.trace),parent=JSON.parse(parents[k]);A(eq(E.trace,parent.trace)&&sha(parents[k])===s.peer.digest&&parent.gauge===v,"parent mismatch");
  // Independent table-domain check of full parent RUP sequence, using table constraints directly plus exact clause factors.
  let F=B.fs.slice(),checks=0;
  function conflict(F,a){for(;;){let ch=false;for(let f of F){let S=[];for(let w of f.ok){checks++;if(f.vs.every((v,i)=>!a.has(v)||a.get(v)===(w>>i&1)))S.push(w)}if(!S.length)return true;for(let i=0;i<f.vs.length;i++){let v=f.vs[i],z=S[0]>>i&1;if(!a.has(v)&&S.every(w=>(w>>i&1)===z)){a.set(v,z);ch=true}}}if(!ch)return false}}
  for(let j=0;j<parent.proof.length;j++){let r=parent.proof[j];A(r.kind==="UP"&&conflict(F,new Map(r.clause.map(l=>[Math.abs(l),+(l<0)]))),"parent RUP via table closure");F.push(clause(r.clause,-j-1))}
  A(parent.proof.at(-1).clause.length===0,"parent incomplete");
  let lane=k===0?s.quad:s.hybridQuad,pre=k===0?[]:parent.proof.slice(0,3).map((r,j)=>clause(r.clause,-j-1)),C=[...B.fs,...pre],ver=check(C,lane.events);A(ver.valid,"final replay failed");
  let corrupt=JSON.parse(JSON.stringify(lane.events));corrupt[0].pin[0]=99999999;let rejected=false;try{check(C,corrupt)}catch(e){rejected=true}A(rejected,"bad guard accepted");
  let art={problem_id:"STRICT-EB4-v1",instance:entry.short_id,instance_id:entry.instance_id,original_N_bits:entry.N_bits,source_pin:{registry:"0c14cdc57925788cf7a451dcd5aa171dce860f2c",corpus:"e315349cd6c1fe3fa696504859f28312f6aab69a",compiler:"21b9d53fb8166c819b24e708656c742cd3c24f10"},guard_id:"EMPTY",residual_id:"ROOT",original_ids:{vertices:[0,g.network.types.length-1],ports:[0,4*g.network.types.length-1],edges:[0,g.network.edges.length-1],carrier_namespace:"minimum original port + 1"},parents:k===0?[]:["CERT-v1:sha256:"+s.peer.digest],claim:"UNSAT by exact signed quotient, complement orbit representative, complete bounded bucket projection and singleton-guard GAC plus degree-two Boolean polynomial annihilator closure",gauge:v,trace:E.trace,prefix:k===0?[]:parent.proof.slice(0,3),events:lane.events,checker:"verify.js; exact row-space kernel replay with local annihilator validation; pinned experiment.js (T1 normalization and projection); input hashes checked",cost:{discovery:lane.stats,independent:ver.stats,parentTableRowChecks:checks}};
  artifacts.push(art);out.push({id:s.id,ver,parentTableRowChecks:checks,rejected,certificateDigest:sha(JSON.stringify(art)+"\n")});
 }
 return {out,artifacts};
}
const files=process.argv.slice(2);if(files.length!==7)throw Error('six pinned inputs from experiment.js then results.json');const result=verify(files.slice(0,6).map(p=>fs.readFileSync(p,'utf8')),JSON.parse(fs.readFileSync(files[6],'utf8')).result);console.log(JSON.stringify(result,null,2));
