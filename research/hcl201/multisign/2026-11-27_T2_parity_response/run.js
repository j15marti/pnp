const fs=require('node:fs');
const specs=[
  [
    "research/coordination/shared-eb-2026-11-27/compile.js",
    "21b9d53fb8166c819b24e708656c742cd3c24f10"
  ],
  [
    "research/coordination/shared-unsat-2026-11-27/benchmarks.json",
    "e315349cd6c1fe3fa696504859f28312f6aab69a"
  ],
  [
    "research/coordination/shared-eb-2026-11-27/instance-registry-v1.json",
    "0c14cdc57925788cf7a451dcd5aa171dce860f2c"
  ],
  [
    "research/hcl201/guarded-dag/2026-11-27_T4_branch_credit/independent_checker.js",
    "5214a4fa84961675b8f44d68b106603a938a4b57"
  ],
  [
    "research/hcl201/synthesis/2026-11-27_T4_nogood_credit/RANDOM-3CNF-40.certificate.json",
    "c026f057f013229265e0e8c2fd2fa53c50eb2177"
  ],
  [
    "research/hcl201/synthesis/2026-11-27_T4_nogood_credit/gauge_check.js",
    "75fd881d231419ee5cbe2d4ae46d630b3a42d624"
  ]
];
function run(raws){
const [compiler,corpus,registry,helper,peerraw,peercheck]=raws;
const compile=Function(compiler.slice(compiler.indexOf("function compile"),compiler.indexOf("function auditLocal"))+";return compile")();
const H=Function(helper.slice(0,helper.indexOf('const fs=require("node:fs"),[compiler'))+";return {sha,independentNormalize,verifyTrace}")();
const P=Function(peercheck.slice(0,peercheck.indexOf('const fs=require("node:fs"),[compiler'))+";return {specialize,checkLearn}")();
const sha=H.sha,eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),assert=(a,m)=>{if(!a)throw Error(m)},B=JSON.parse(corpus),R=JSON.parse(registry);
assert(sha("")==="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","sha empty");assert(sha("abc")==="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","sha abc");
const parity=x=>{let p=0;while(x){x&=x-1;p^=1}return p};
function normalize(G){
 const n=G.types.length*4,A=Array.from({length:n},()=>[]),root=new Int32Array(n).fill(-1),phase=new Uint8Array(n),ports=new Set(),edges=new Set();let arcs=0;
 function add(a,b,s){A[a].push([b,s]);A[b].push([a,s]);arcs+=2}
 for(let [a,b,s]of G.edges){let u=a>>2,v=b>>2,k=Math.min(u,v)+":"+Math.max(u,v);assert(a>=0&&b>=0&&a<n&&b<n&&u!==v&&!ports.has(a)&&!ports.has(b)&&!edges.has(k)&&[0,1].includes(s),"strict input");ports.add(a);ports.add(b);edges.add(k);add(a,b,s)}
 assert(ports.size===n,"ports");for(let v=0;v<G.types.length;v++){assert(["E","B"].includes(G.types[v]),"type");if(G.types[v]==="E")for(let j=1;j<4;j++)add(4*v,4*v+j,0)}
 for(let i=0;i<n;i++)if(root[i]===-1){root[i]=i;let q=[i];for(let j=0;j<q.length;j++){let u=q[j];for(let[v,s]of A[u]){let t=phase[u]^s;if(root[v]===-1){root[v]=i;phase[v]=t;q.push(v)}else assert(root[v]===i&&phase[v]===t,"signed contradiction")}}}
 let M=new Map(),local=0;
 for(let v=0;v<G.types.length;v++)if(G.types[v]==="B"){let l=Array.from({length:4},(_,j)=>(root[4*v+j]+1)*(phase[4*v+j]?-1:1)).sort((a,b)=>a-b),rev=l.map(x=>-x).reverse();if(rev.join(",")<l.join(","))l=rev;let k=l.join(",");if(!M.has(k))M.set(k,{l,ids:[]});M.get(k).ids.push(v)}
 let fs=[...M.values()].map(({l,ids},id)=>{let vs=[...new Set(l.map(Math.abs))].sort((a,b)=>a-b),ok=[];for(let w=0;w<2**vs.length;w++){local++;if(l.reduce((s,x)=>s+((w>>vs.indexOf(Math.abs(x))&1)^Number(x<0)),0)===2)ok.push(w)}return{id,vs,ok,ids,l}});
 return{fs,root,phase,arcs,local};
}
function basis(f){
 let n=f.vs.length,S=new Set(f.ok),period=[],forms=[],piv=new Map();
 for(let d=0;d<2**n;d++)if(f.ok.every(w=>S.has(w^d)))period.push(d);
 for(let a=1;a<2**n;a++)if(period.every(d=>parity(a&d)===0)){let v=a;while(v){let h=31-Math.clz32(v);if(piv.has(h))v^=piv.get(h);else{piv.set(h,v);forms.push(a);break}}}
 let code=w=>forms.reduce((s,a,i)=>s|(parity(a&w)<<i),0),ok=[...new Set(f.ok.map(code))].sort((a,b)=>a-b),T=new Set(ok);
 for(let w=0;w<2**n;w++)assert(S.has(w)===T.has(code(w)),"basis exact");
 return{forms,ok,periodSize:period.length,old:f.ok.length};
}
function project(fs,cap=10000000){
 let F=fs.map(f=>({...f})),trace=[],next=F.length,checks=0,scans=0,privateParity=0,privateOther=0,dual=0,peak=F.reduce((s,f)=>s+f.ok.length,0);
 const pr=(w,U,V)=>V.reduce((s,v,i)=>s|((w>>U.indexOf(v)&1)<<i),0);
 while(true){let occ=new Map();for(let f of F)for(let v of f.vs){scans++;if(!occ.has(v))occ.set(v,[]);occ.get(v).push(f)}
 let cand=[...occ].filter(([v,fs])=>fs.length<=2&&new Set(fs.flatMap(f=>f.vs)).size<=5).sort((a,b)=>a[1].length-b[1].length||a[0]-b[0]);if(!cand.length)break;
 let[v,fs]=cand[0],U=[...new Set(fs.flatMap(f=>f.vs))].sort((a,b)=>a-b),V=U.filter(x=>x!==v),ok=[],lift=[],isParity=fs.length===1&&fs[0].l&&fs[0].l.filter(x=>Math.abs(x)===v).length===1;
 for(let w=0;w<2**V.length;w++){let hit=[];for(let b=0;b<2;b++){let word=U.reduce((z,u,i)=>z|((u===v?b:w>>V.indexOf(u)&1)<<i),0);if(isParity){let f=fs[0],p=f.l.reduce((z,x)=>z^Number(x<0),0);for(let x of f.l)if(Math.abs(x)!==v)p^=w>>V.indexOf(Math.abs(x))&1;if(b!==p)continue}
 checks++;if(fs.every(f=>f.ok.includes(pr(word,U,f.vs))))hit.push(b)}
 if(hit.length){ok.push(w);lift.push([w,hit[0]])}}
 if(isParity)privateParity++;else if(fs.length===1)privateOther++;else dual++;
 trace.push({v,in:fs.map(f=>f.id),out:next,vs:V,ok,lift,mode:isParity?"parity":"enumerated"});F=F.filter(f=>!fs.includes(f));if(ok.length!==2**V.length)F.push({id:next,vs:V,ok});next++;peak=Math.max(peak,F.reduce((s,f)=>s+f.ok.length,0));if(checks+scans>cap)throw Error("projection cap");if(ok.length===0)break;
 }
 return{fs:F,trace,checks,scans,privateParity,privateOther,dual,peak};
}
function replayProjection(fs,trace){
 let F=fs.map(f=>({...f})),checks=0;for(let t of trace){let bucket=F.filter(f=>f.vs.includes(t.v)),V=[...new Set(bucket.flatMap(f=>f.vs))].filter(v=>v!==t.v).sort((a,b)=>a-b);assert(eq(bucket.map(f=>f.id),t.in)&&eq(V,t.vs),"bucket");let ok=[],l=new Map(t.lift);
 for(let w=0;w<2**V.length;w++){let hit=[];for(let b=0;b<2;b++){checks++;if(bucket.every(f=>f.ok.includes(f.vs.reduce((s,v,i)=>s|((v===t.v?b:w>>V.indexOf(v)&1)<<i),0))))hit.push(b)}if(hit.length){ok.push(w);assert(hit.includes(l.get(w)),"lift")}}
 assert(eq(ok,t.ok),"projection");F=F.filter(f=>!bucket.includes(f));if(ok.length!==2**V.length)F.push({id:t.out,vs:V,ok});}return{fs:F,checks};
}
function specialize(F,g){let a=[],seen=new Set();for(let f of F){let i=f.vs.indexOf(g),vs=f.vs.filter(v=>v!==g),ok=i<0?f.ok.slice():f.ok.filter(w=>!(w>>i&1)).map(w=>(w&((1<<i)-1))|((w>>(i+1))<<i));let k=JSON.stringify([vs,ok]);if(ok.length!==2**vs.length&&!seen.has(k)){seen.add(k);a.push({vs,ok})}}return a}
function learn(F,cap=10000000){
 let vars=[...new Set(F.flatMap(f=>f.vs))].sort((a,b)=>a-b),fs=F.map(f=>({...f})),idx=new Map(),tests=0,probes=0,steps=[],pins=new Map(),seen=new Set(),rootClosure=0;
 function index(f,i){for(let v of f.vs){if(!idx.has(v))idx.set(v,[]);idx.get(v).push(i)}}fs.forEach(index);
 function close(a){let q=fs.map((_,i)=>i),queued=new Set(q);while(q.length){let j=q.pop();queued.delete(j);let f=fs[j],and=2**f.vs.length-1,or=0,hit=false;
 for(let w of f.ok){if(++tests>cap)throw Error("CAP");if(f.vs.every((v,i)=>!a.has(v)||a.get(v)===(w>>i&1))){hit=true;and&=w;or|=w}}if(!hit)return null;
 for(let i=0;i<f.vs.length;i++){let v=f.vs[i];if(!a.has(v)&&(and>>i&1)===(or>>i&1)){a.set(v,and>>i&1);for(let j of idx.get(v))if(!queued.has(j)){queued.add(j);q.push(j)}}}}
 return a}
 try{for(;;){rootClosure++;pins=close(new Map(pins));if(!pins)return{status:"UNSAT",steps,tests,probes,rootClosure};let left=vars.filter(v=>!pins.has(v)),changed=false;
 outer:for(let k=1;k<=2;k++){let groups=k===1?left.map(v=>[v]):left.flatMap((v,i)=>left.slice(i+1).map(u=>[v,u]));for(let vs of groups)for(let w=0;w<2**k;w++){let key=JSON.stringify([vs,w]);if(seen.has(key))continue;let a=new Map(pins);vs.forEach((v,i)=>a.set(v,w>>i&1));probes++;if(close(a)===null){let f={vs,ok:Array.from({length:2**k},(_,i)=>i).filter(i=>i!==w)};index(f,fs.length);fs.push(f);steps.push({vs,w});seen.add(key);changed=true;break outer}}}if(!changed)return{status:"UNKNOWN",steps,tests,probes,rootClosure};}}
 catch(e){if(String(e).includes("CAP"))return{status:"UNKNOWN_CAP",steps,tests,probes,rootClosure};throw e}
}
function cnfTables(x){return x.dimacs.trim().split("\n").slice(1).map(s=>{let l=s.split(/\s+/).map(Number).slice(0,-1),vs=[...new Set(l.map(Math.abs))].sort((a,b)=>a-b),ok=[];for(let w=0;w<2**vs.length;w++)if(l.some(x=>(w>>vs.indexOf(Math.abs(x))&1)===Number(x>0)))ok.push(w);return{vs,ok}})}
let outputs=[],certs=[];
for(let id of ["JOINT-24","RANDOM-3CNF-40"]){
 let e=R.instances.find(x=>x.alias==="EB-"+id),x=B.instances.find(x=>x.id===id),g=compile(x),bytes=JSON.stringify(g.network)+"\n",mapBytes=JSON.stringify(g.source_map)+"\n";
 assert(sha(bytes)===e.sha256&&bytes.length*8===e.N_bits&&sha(x.dimacs)===e.source_cnf.sha256&&x.dimacs.length*8===e.source_cnf.N_bits&&sha(mapBytes)===e.source_map_sha256,"identity");
 let N=normalize(g.network),D=H.independentNormalize(g.network);assert(eq(N.fs.map(({id,vs,ok,ids})=>({id,vs,ok,ids})),D.fs),"independent normalizer mismatch");
 let bs=N.fs.map(basis),pr=project(N.fs),replay=replayProjection(N.fs,pr.trace);assert(eq(pr.fs,replay.fs),"projection replay");
 let freq=new Map();for(let f of pr.fs)for(let v of f.vs)freq.set(v,(freq.get(v)||0)+1);let gauge=[...freq].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0]?.[0];
 assert(pr.fs.every(f=>f.ok.every(w=>f.ok.includes(w^(2**f.vs.length-1)))),"gauge complement");let F=gauge===undefined?pr.fs:specialize(pr.fs,gauge),post=F.map(basis),native=learn(F);
 let verify=native.status==="UNSAT"?P.checkLearn(F,null,native.steps):null;if(verify)assert(verify.verified,"native check");
 let direct=learn(cnfTables(x)),directCheck=direct.status==="UNSAT"?P.checkLearn(cnfTables(x),null,direct.steps):null;if(directCheck)assert(directCheck.verified,"CNF check");
 let peer=null;if(id==="RANDOM-3CNF-40"){let q=JSON.parse(peerraw);assert(sha(peerraw)==="08e7d9e121b42a3191acf20d072ec38b67071458fababed8a76c85dfa01684b1"&&q.instance_id===e.instance_id&&q.original_N_bits===e.N_bits&&q.guard_id==="EMPTY"&&q.residual_id==="ROOT","peer ID");
 let pv=H.verifyTrace(D.fs,q.trace);assert(pv.fs.every(f=>f.ok.every(w=>f.ok.includes(w^(2**f.vs.length-1)))),"peer gauge");let pc=P.checkLearn(P.specialize(pv.fs,q.gauge).fs,null,q.nogoods);assert(pc.verified,"peer replay");peer={projectionTests:pv.tests,scans:pv.scans,...pc};}
 let cert={schema:"EB-T2-PARITY-RESPONSE-v1",instance_id:e.instance_id,original_N_bits:e.N_bits,source_pin:{registry:"0c14cdc57925788cf7a451dcd5aa171dce860f2c",compiler:"21b9d53fb8166c819b24e708656c742cd3c24f10",corpus:"e315349cd6c1fe3fa696504859f28312f6aab69a"},guard_id:"EMPTY",residual_id:"ROOT",original_ids:{vertices:[0,g.network.types.length-1],ports:[0,4*g.network.types.length-1],edges:[0,g.network.edges.length-1]},parents:[],claim:native.status==="UNSAT"?"Native UNSAT by exact parity/private response projection, complement gauge and bounded nogoods":"Scoped exact projection and bounded probe result "+native.status,trace:pr.trace,gauge,steps:native.steps};
 let certBytes=JSON.stringify(cert)+"\n";certs.push({id,bytes:certBytes,hash:sha(certBytes),status:native.status});
 outputs.push({id,instance_id:e.instance_id,N:e.N_bits,cnf_id:e.source_cnf.instance_id,cnfN:e.source_cnf.N_bits,hashesVerified:true,arcs:N.arcs,localWords:N.local,roots:new Set(N.root).size,initialFactors:N.fs.length,initialRows:N.fs.reduce((s,f)=>s+f.ok.length,0),localBasisRows:bs.reduce((s,f)=>s+f.ok.length,0),localBasisRank:bs.reduce((s,f)=>s+f.forms.length,0),initialArity:N.fs.reduce((s,f)=>s+f.vs.length,0),privateParity:pr.privateParity,privateOther:pr.privateOther,dual:pr.dual,projectionChecks:pr.checks,projectionScans:pr.scans,projectionReplay:replay.checks,peakRows:pr.peak,projectedFactors:pr.fs.length,gauge,finalVars:new Set(F.flatMap(f=>f.vs)).size,finalFactors:F.length,finalRows:F.reduce((s,f)=>s+f.ok.length,0),finalBasisRows:post.reduce((s,f)=>s+f.ok.length,0),native:{...native,steps:native.steps.length},verify,direct:{...direct,steps:direct.steps.length},directCheck,peer});
}
return{outputs,certs};
}
const raws=process.argv.slice(2).map(p=>fs.readFileSync(p,'utf8'));if(raws.length!==specs.length)throw Error('six pinned inputs in order');let r=run(raws);console.log(JSON.stringify(r.outputs,null,2));for(let c of r.certs)fs.writeFileSync(c.id+'.certificate.json',c.bytes);
