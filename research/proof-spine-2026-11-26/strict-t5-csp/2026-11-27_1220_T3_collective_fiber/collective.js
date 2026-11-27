function collectiveRun(src){
 const C=Function(src.compiler.slice(src.compiler.indexOf("function compile("),src.compiler.indexOf("function auditLocal("))+";return compile")();
 const H=Function(src.hybrid.split('if(typeof require==="function"')[0]+";return {sha,norm,closure,affine,compact,reduce,solve,unique}")();
 const B=JSON.parse(src.corpus),R=JSON.parse(src.registry),assert=(x,m)=>{if(!x)throw Error(m)};
 assert(H.sha("abc")==="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","hash");
 const CAP=2000000;
 function bad(f){let a=[];for(let i=0;i<2**f.vs.length;i++)if(!f.ok.includes(i))a.push(i);return a}
 function isAffine(a){if(!a.length)return true;let S=new Set(a.map(x=>x^a[0]));for(let x of S)for(let y of S)if(!S.has(x^y))return false;return true}
 function extract(w,U,V){return V.reduce((a,v,i)=>a+(((w>>U.indexOf(v))&1)<<i),0)}
 function collective(fs){
  fs=fs.map(f=>({...f}));let rounds=[],work=0,next=Math.max(...fs.map(f=>f.id))+1,tries=0,retired=0;
  const tick=()=>{if(++work>CAP)throw Error("collective cap")};
  for(;;){
   let occ=new Map();for(let f of fs)for(let v of f.vs){tick();if(!occ.has(v))occ.set(v,[]);occ.get(v).push(f)}
   let taken=new Set(),steps=[];
   for(let [v,fac] of [...occ].sort((a,b)=>a[0]-b[0])){
    tick();if(fac.length!==2||fac.some(f=>taken.has(f.id)))continue;tries++;
    let U=[...new Set(fac.flatMap(f=>f.vs))].sort((a,b)=>a-b),Y=U.filter(x=>x!==v);
    if(U.length>7)continue;
    let E=fac.map(bad);if(E.some(a=>!a.length||!isAffine(a)))continue;
    if(fac.some((f,j)=>E[j].some(x=>E[j].includes(x^(1<<f.vs.indexOf(v))))))continue;
    let blocked=[];
    for(let w=0;w<2**Y.length;w++){
     tick();let b=fac.map((f,j)=>{let a=0;for(let z=0;z<2;z++){let x=f.vs.reduce((u,t,i)=>u+((t===v?z:((w>>Y.indexOf(t))&1))<<i),0);if(E[j].includes(x))a|=1<<z}return a});
     if((b[0]===1&&b[1]===2)||(b[0]===2&&b[1]===1))blocked.push(w)
    }
    assert(isAffine(blocked),"projected event affine");
    let ok=Array.from({length:2**Y.length},(_,i)=>i).filter(w=>!blocked.includes(w));
    steps.push({v,in:fac.map(f=>f.id),out:next++,vs:Y,ok});fac.forEach(f=>taken.add(f.id));retired++;
   }
   if(!steps.length)break;
   // A simultaneous batch: each factor meets at most one retired coordinate, verified by occurrence map.
   fs=fs.filter(f=>!taken.has(f.id));for(let s of steps)if(s.ok.length!==2**s.vs.length)fs.push({id:s.out,vs:s.vs,ok:s.ok});
   rounds.push(steps)
  }
  return {fs,rounds,work,tries,retired}
 }
 function independentReplay(fs,rounds){
  fs=fs.map(f=>({...f}));let checks=0;
  for(let steps of rounds){let piv=new Set(steps.map(s=>s.v)),used=new Set(),newFs=[];
   assert(piv.size===steps.length,"duplicate pivot");
   for(let s of steps){
    let fac=fs.filter(f=>f.vs.includes(s.v));assert(JSON.stringify(fac.map(f=>f.id))===JSON.stringify(s.in),"scope");
    assert(fac.every(f=>!used.has(f.id)&&f.vs.filter(x=>piv.has(x)).length===1),"batch overlap");fac.forEach(f=>used.add(f.id));
    let U=[...new Set(fac.flatMap(f=>f.vs))].sort((a,b)=>a-b),Y=U.filter(v=>v!==s.v),O=new Set();
    assert(JSON.stringify(Y)===JSON.stringify(s.vs),"surviving IDs");
    for(let w=0;w<2**U.length;w++){checks++;if(checks>CAP)throw Error("verify cap");if(fac.every(f=>f.ok.includes(extract(w,U,f.vs))))O.add(extract(w,U,Y))}
    let ok=[...O].sort((a,b)=>a-b);assert(JSON.stringify(ok)===JSON.stringify(s.ok),"full joint projection");
    if(ok.length!==2**Y.length)newFs.push({id:s.out,vs:Y,ok});
   }
   fs=fs.filter(f=>!used.has(f.id)).concat(newFs)
  }
  return {fs,checks}
 }
 function cnf(fs){let a=[],faces=0,checks=0;for(let f of fs){let e=bad(f);if(!e.length)continue;let fixed=f.vs.map((v,i)=>[v,i,((e[0]>>i)&1)]).filter(([v,i,b])=>e.every(w=>{checks++;return((w>>i)&1)===b}));if(e.length===2**(f.vs.length-fixed.length)){a.push(fixed.map(([v,i,b])=>b?-v:v));faces++}else for(let w of e)a.push(f.vs.map((v,i)=>(w>>i)&1?-v:v))}
  return {F:H.unique(a),faces,checks}}
 function checkTree(F,t){let checks=0,nodes=0;function rec(t,p){nodes++;for(;;){let change=false;for(let c of F){let u=[],sat=false;for(let l of c){if(++checks>CAP)throw Error("verify tree cap");let v=Math.abs(l);if(!p.has(v))u.push(l);else if(p.get(v)===Number(l>0)){sat=true;break}}if(sat)continue;if(!u.length){assert(t===0,"leaf");return}if(u.length===1){p.set(Math.abs(u[0]),Number(u[0]>0));change=true}}if(!change)break}assert(Array.isArray(t)&&t.length===3&&!p.has(t[0])&&F.some(c=>c.some(l=>Math.abs(l)===t[0])),"branch");rec(t[1],new Map([...p,[t[0],0]]));rec(t[2],new Map([...p,[t[0],1]]))}
 rec(t,new Map());return {nodes,checks}}
 function replayDP(F,trace){let checks=0;for(let s of trace){let P=F.filter(c=>c.includes(s.v)),M=F.filter(c=>c.includes(-s.v));assert(JSON.stringify([...P,...M])===JSON.stringify(s.removed),"DP scope");let res=H.unique(P.flatMap(a=>M.map(b=>{checks++;return [...a.filter(x=>x!==s.v),...b.filter(x=>x!==-s.v)]})));assert(JSON.stringify(res)===JSON.stringify(s.added),"DP all resolvents");F=H.unique(F.filter(c=>!c.includes(s.v)&&!c.includes(-s.v)).concat(res))}return {F,checks}}
 let out=[],certs=[];
 for(let id of ["JOINT-24","RANDOM-3CNF-40"]){
  let x=B.instances.find(z=>z.id===id),g=C(x),e=R.instances.find(z=>z.alias==="EB-"+id),raw=JSON.stringify(g.network)+"\n";
  assert(H.sha(raw)===e.sha256&&raw.length*8===e.N_bits&&H.sha(x.dimacs)===e.source_cnf.sha256&&x.dimacs.length*8===e.source_cnf.N_bits,"identity");
  let S=H.norm(g.network),meter={n:0,cap:CAP},p=new Map(),cl=H.closure(S.factors,p,meter),ge=H.affine(S);
  let K=H.compact(S,CAP),A=collective(K.fs),re=independentReplay(K.fs,A.rounds);
  assert(JSON.stringify(re.fs)===JSON.stringify(A.fs),"replay");
  let corrupt=JSON.parse(JSON.stringify(A.rounds));if(corrupt.length&&corrupt[0].length){corrupt[0][0].ok=corrupt[0][0].ok.slice(1);try{independentReplay(K.fs,corrupt);throw Error("not rejected")}catch(e){assert(String(e).includes("full joint projection"),"corruption")}}
  let M={n:0,cap:CAP},post=H.closure(A.fs,new Map(),M),F=cnf(A.fs),D=H.reduce(F.F,CAP),T=H.solve(D.F,CAP),dr=replayDP(F.F,D.trace),tree=checkTree(dr.F,T.tree);
  let prov=H.solve(x.dimacs.trim().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1)),CAP);
  const cert={problem_id:"STRICT-EB4-v1",instance:e.short_id,instance_id:e.instance_id,original_N_bits:e.N_bits,source_pin:"registry 0c14cdc57925788cf7a451dcd5aa171dce860f2c; corpus e315349cd6c1fe3fa696504859f28312f6aab69a; compiler 21b9d53fb8166c819b24e708656c742cd3c24f10",guard_id:"EMPTY",residual_id:"ROOT",affected_original_ids:{vertices:[0,g.network.types.length-1],ports:[0,4*g.network.types.length-1],edges:[0,g.network.edges.length-1]},parents:[],gauge:S.gauge,privateTrace:K.trace,batches:A.rounds,dp:D.trace,tree:T.tree,claim:"UNSAT by checked collective disjoint-scope affine fiber projection, resolution and exhaustive tree"};
  let s=JSON.stringify(cert)+"\n";certs.push({id,content:s,sha:H.sha(s)});
  out.push({id,instance:e.instance_id,N:e.N_bits,roots:S.roots,initialFactors:S.factors.length,initialClosure:{status:cl?"UNKNOWN":"UNSAT",pins:p.size,checks:meter.n},gaussian:ge,privateRetired:K.trace.length,privateEvents:K.events,privateEncodingChecks:K.checks,batchSizes:A.rounds.map(r=>r.length),retired:A.retired,remainingFactors:A.fs.length,batchWork:A.work,candidates:A.tries,independentReplayWords:re.checks,postClosure:{status:post?"UNKNOWN":"UNSAT",checks:M.n},clauses:F.F.length,faces:F.faces,faceChecks:F.checks,dpRetired:D.trace.length,dpScans:D.scans,dpPairs:D.ops,remainingVariables:new Set(D.F.flat().map(Math.abs)).size,treeNodes:T.nodes,treeReads:T.scans,verifyTree:tree,verifyDP:dr.checks,provenanceAudit:{nodes:prov.nodes,reads:prov.scans},certificateSha:H.sha(s),certificateBytes:s.length,corruptedProjectionRejected:true,status:"UNSAT"})
 }
 // generic conditional-parity cycle: every event forbids exactly one parity, gate y_i=0.
 let cycle=[];for(let k of [4,8,12,64,256]){let n=k; // n edge equations, n-1 independent h coords via h0=0; one odd sign
  let checked=0;
  if(n<=12)for(let mask=0;mask<2**n;mask++){let inconsistent=false;let p=Array(n).fill(-1),adj=Array.from({length:n},()=>[]);
   for(let i=0;i<n;i++)if(!(mask>>i&1)){let j=(i+1)%n,b=Number(i===n-1);adj[i].push([j,b]);adj[j].push([i,b])}
   for(let i=0;i<n;i++)if(p[i]<0){p[i]=0;let q=[i];for(let j=0;j<q.length;j++)for(let [v,b] of adj[q[j]]){if(p[v]<0){p[v]=p[q[j]]^b;q.push(v)}else if(p[v]!== (p[q[j]]^b))inconsistent=true}}
   assert(inconsistent===(mask===0),"cycle theorem");checked++}
  cycle.push({events:n,fiberDimension:n-1,dependencyNullity:1,outputEvents:1,checkedBoundaries:checked})
 }
 let planes=[[15,32,47],[13,17,28],[14,36,42],[11,53,62],[10,39,45]],mfc={id:H.sha(JSON.stringify({planes})+"\n"),N:(JSON.stringify({planes})+"\n").length*8,target:29,fiberWords:0,valid:0,intersections:[],minOwnerCover:null};
 let rows=[];for(let x=0;x<1024;x++){let syn=0,viol=0;for(let i=0;i<5;i++){let c=x>>(2*i)&3;if(c)syn^=planes[i][c-1];else viol|=1<<i}if(syn===29){rows.push(viol);if(!viol)mfc.valid++}}
 mfc.fiberWords=rows.length;let hist={};for(let x of rows)hist[x]=(hist[x]||0)+1;mfc.violationMasks=hist;
 for(let u=1;u<32;u++){let c=rows.filter(x=>(x&u)===u).length;if(c)mfc.intersections.push([u,c])}
 let best=6;for(let s=0;s<32;s++)if(rows.every(x=>x&s))best=Math.min(best,s.toString(2).replace(/0/g,"").length);mfc.minOwnerCover=best;assert(mfc.valid===0&&mfc.fiberWords===16&&best===5,"MFC peer");
 return {results:out,cycle,mfc,certs}
}
if(typeof require==='function'){const fs=require('fs');let [compiler,corpus,registry,hybrid]=process.argv.slice(2);let src=Object.fromEntries(Object.entries({compiler,corpus,registry,hybrid}).map(([k,p])=>[k,fs.readFileSync(p,'utf8')]));console.log(JSON.stringify(collectiveRun(src),null,2));}
