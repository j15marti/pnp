
function runTarget(compiler,corpus,registry,prior,baseJ,baseR,peerJ,peerR,pullbackCode){
 const src=pullbackCode.slice(0,pullbackCode.lastIndexOf('if(typeof module')).replace('const out=[];\n for(const [i,name]', 'return {compile,sha,project,experiment,enc,hash,importPeer,probe,key,canon}; const out=[];\n for(const [i,name]');
 const {compile,sha,project,enc,hash,importPeer,key,canon}=Function(src+";return run")()(compiler,corpus,registry,prior,baseJ,baseR,peerJ,peerR);
 const X=JSON.parse(corpus),Reg=JSON.parse(registry),cap=10000000;
 // Fixed-width sound guard learning. Every learned clause is independently checked.
 function solve(F,n,extra=[],mode="overlap",seed=0){
  let C=[...F,...extra],seen=new Set(C.map(key)),trace=[],rounds=[],w=0,checks=0,scans=0,done=false,fail=null;
  const start=Date.now();
  const UP=(A,pins,verify=false)=>{let a=new Int8Array(n+1).fill(-1);for(const l of pins){let i=Math.abs(l),b=+(l>0);if(a[i]!==-1&&a[i]!==b)return true;a[i]=b}let change=true;
    while(change){change=false;for(let j=0;j<A.length;j++){let c=A[verify?A.length-1-j:j],ok=false,u=0,last=0;for(const l of c){if(verify)checks++;else if(++w>cap)throw Error("cap");let b=a[Math.abs(l)];if(b===+(l>0)){ok=true;break}if(b===-1){u++;last=l}}if(ok)continue;if(u===0)return true;if(u===1){a[Math.abs(last)]=+(last>0);change=true}}}return false};
  let rand=seed>>>0;function rng(){rand=(Math.imul(rand,1664525)+1013904223)>>>0;return rand}
  try{for(let t=0;t<=2*n*n+2*n;t++){
   if(UP(C,[])){done=true;break}const snap=C.slice(),next=new Map();let tested=0;
   function trial(pins){let c=canon(pins.map(l=>-l)),k=key(c);if(seen.has(k)||next.has(k))return;tested++;if(UP(snap,pins))next.set(k,c)}
   for(let v=1;v<=n;v++)for(const s of [1,-1])trial([v*s]);
   let phase="unary";
   if(!next.size){phase=mode;const freq=new Map(),pairs=[];for(const c of snap){const a=[...new Set(c.map(Math.abs))].sort((a,b)=>a-b);for(let i=0;i<a.length;i++)for(let j=i+1;j<a.length;j++){scans++;const k=a[i]+","+a[j];freq.set(k,(freq.get(k)||0)+1)}} 
    for(let i=1;i<=n;i++)for(let j=i+1;j<=n;j++){let f=freq.get(i+","+j)||0;if(mode==="all"||f)pairs.push({i,j,f,r:seed?rng():0})}
    pairs.sort((a,b)=>seed?a.r-b.r:b.f-a.f||a.i-b.i||a.j-b.j);
    for(const {i,j} of pairs)for(const a of [1,-1])for(const b of [1,-1])trial([a*i,b*j])
   }
   rounds.push({phase,tested,admitted:next.size,units:[...next.values()].filter(c=>c.length===1).length});
   if(!next.size)break;
   for(const [k,c] of next){seen.add(k);trace.push(c);C.push(c)}
  }}catch(e){fail=String(e)}
  const A=[...F,...extra];for(const c of trace){if(!UP(A,c.map(l=>-l),true))throw Error("RUP");A.push(c)}
  if(done&&!UP(A,[],true))throw Error("terminal");
  return{no:done,fail,work:w,replay:checks,candidateScans:scans,rounds,trace,ms:Date.now()-start,mode,seed};
 }
 const out=[];
 for(const [i,name] of ["JOINT-24","RANDOM-3CNF-40"].entries()){
  const x=X.instances.find(x=>x.id===name),e=Reg.instances.find(x=>x.alias==="EB-"+name),G=compile(x),s=enc(G.network);
  if(sha(s)!==e.sha256||s.length*8!==e.N_bits||sha(x.dimacs)!==e.source_cnf.sha256||x.dimacs.length*8!==e.source_cnf.N_bits||sha(enc(G.source_map))!==e.source_map_sha256)throw Error("identity");
  const p=project(G.network),V=[...new Set(p.clauses.flat().map(Math.abs))].sort((a,b)=>a-b),M=new Map(V.map((v,i)=>[v,i+1])),F=p.clauses.map(c=>c.map(l=>Math.sign(l)*M.get(Math.abs(l))));
  const orig=x.dimacs.trimEnd().split("\n").slice(1).map(l=>l.split(/\s+/).map(Number).slice(0,-1));let a=G.source_map.representative_ports.f,ar=p.root[a[0]],f=p.phase[a[0]]^a[1],mapping=[];
  for(let j=1;j<=x.nvars;j++){let [q,z]=G.source_map.representative_ports["x"+j];mapping.push([j,M.get(p.root[q]+1),p.phase[q]^z^f])}
  let inverse=new Map(mapping.map(([i,j,b])=>[j,[i,b]])),C=F.map(c=>c.map(l=>{let [i,b]=inverse.get(Math.abs(l));return i*Math.sign(l)*(b?-1:1)})),K=new Set(orig.map(key)),J=new Set(C.map(key));if(ar!==p.anchor||K.size!==J.size||[...K].some(k=>!J.has(k))||inverse.size!==V.length)throw Error("adapter");
  const local=solve(F,V.length,[],"overlap"),all=solve(F,V.length,[],"all"),random=solve(F,V.length,[],"overlap",20261127);
  const imp=importPeer(orig,i?baseR:baseJ,i?peerR:peerJ,e.source_cnf,i),mp=new Map(mapping.map(([i,j,b])=>[i,[j,b]])),extra=[...imp.learned,...imp.binary],nativeExtra=extra.map(c=>c.map(l=>{const [j,b]=mp.get(Math.abs(l));return Math.sign(l)*j*(b?-1:1)}));
  const hybrid=solve(F,V.length,nativeExtra,"overlap"),direct=solve(orig,x.nvars,[],"overlap"),directHybrid=solve(orig,x.nvars,extra,"overlap");
  out.push({name,instance:e.short_id,instance_id:e.instance_id,N:e.N_bits,cnf:e.source_cnf,guard_id:"EMPTY",residual_id:"ROOT",projection:{cost:p.cost,steps:p.steps.length,anchor:p.anchor,rootPorts:V.map(v=>v-1),mapping,chartHash:hash(F),mapHash:hash({root:p.root,phase:p.phase,steps:p.steps,cond:p.cond})},local,all,random,hybrid,direct,directHybrid,peer:{ids:imp.ids,truthChecks:imp.truthChecks}})
 }
 return out
}
if(typeof module!=="undefined"){module.exports=runTarget;if(require.main===module){const fs=require("fs");console.log(JSON.stringify(runTarget(...process.argv.slice(2).map(p=>fs.readFileSync(p,"utf8"))),null,2))}}
