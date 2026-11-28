// Node 20+: node run.js DIR; populate DIR files by pin keys.
const fs=require('node:fs');
const pins={"compiler":["research/coordination/shared-eb-2026-11-27/compile.js","21b9d53fb8166c819b24e708656c742cd3c24f10"],"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"registry":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"chart":["research/proof-spine-2026-11-26/algebraic-geometric-closure/2026-11-27_1552_T2_hall_syzygy/native-chart.js","52cae4a54513a67dd9468c7e3ee597cf317d67a3"],"peer":["research/proof-spine-2026-11-26/closure-finite-groups/2026-11-27_1800_T3_cross_scope/owner-cert.js","faf453592a9c63182fe941dd79d4ef62ba606cef"]};
const data=Object.fromEntries(Object.keys(pins).map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));
const run=function(data,pins){
 const L=new Function(data.peer.slice(0,data.peer.indexOf("function compile("))+"\nreturn {sha,quotient,gauge,project,clauses,canon,up,tree,replay,importPrefix}")();
 const {sha,canon}=L;
 const cs=data.compiler.slice(data.compiler.indexOf("function compile("),data.compiler.indexOf("function auditLocal"));
 const compile=new Function(cs+"\nreturn compile")();
 const ps=data.chart.slice(data.chart.indexOf("const key="),data.chart.indexOf("function up("));
 const {project,verifyProjection}=new Function(ps+"\nreturn {project,verifyProjection}")();
 const i=data.peer.indexOf("function study("),j=data.peer.indexOf("\nfunction ",i+15);
 const study=new Function(data.peer.slice(i,j)+"\nreturn study")();
 const enc=x=>JSON.stringify(x)+"\n",assert=(b,m)=>{if(!b)throw Error(m)},pop=x=>{let k=0;while(x){k++;x&=x-1}return k};
 assert(sha("abc")==="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","sha");
 const reg=JSON.parse(data.registry),corp=JSON.parse(data.corpus);
 function compress(F){
  let tested=0,verified=0;
  let D=F.map(f=>{let n=f.s.length;for(let p=0;p<2**n;p++){let counts=0;for(let t of f.a){tested++;counts|=1<<pop(t^p)}let ok=true;for(let t=0;t<2**n;t++){tested++;if(f.a.includes(t)!==!!(counts&(1<<pop(t^p)))){ok=false;break}}if(ok)return {id:f.id,s:f.s,p,counts}}return {id:f.id,s:f.s,a:f.a}});
  for(let z=0;z<F.length;z++){let f=F[z],d=D[z];for(let t=0;t<2**f.s.length;t++){verified++;assert(f.a.includes(t)===(d.a?d.a.includes(t):!!(d.counts&(1<<pop(t^d.p)))),"decode")}}
  return{D,tested,verified,tableWords:F.reduce((n,f)=>n+f.s.length+f.a.length,0),encodedWords:D.reduce((n,f)=>n+f.s.length+(f.a?f.a.length:2),0),compressed:D.filter(f=>!f.a).length}
 }
 function closure(F,h,extra=[]){
  let A=new Map(h.map(l=>[Math.abs(l),+(l>0)])),trace=[],work=0,change=true;
  while(change){change=false;for(let f of F){let n=f.s.length,can0=[],can1=[],allowed=0;
    if(!f.a){let t=0,u=0;for(let j=0;j<n;j++){work++;let b=A.get(f.s[j]);if(b===undefined)u++;else t+=b^((f.p>>j)&1)}
      let has=(a,b)=>{for(let k=a;k<=b;k++){work++;if(f.counts&(1<<k))return true}return false};
      if(!has(t,t+u))return{bad:true,trace,work,conflict:f.id,forced:A.size-h.length};
      if(u){let z=has(t,t+u-1),o=has(t+1,t+u);for(let j=0;j<n;j++)if(!A.has(f.s[j])){work++;if(!z||!o){let b=(!z?1:0)^((f.p>>j)&1);A.set(f.s[j],b);trace.push([f.s[j],b,f.id]);change=true}}}
    }else{for(let a of f.a){work++;let ok=true;for(let j=0;j<n;j++){work++;if(A.has(f.s[j])&&A.get(f.s[j])!==(a>>j&1)){ok=false;break}}if(ok){allowed++;for(let j=0;j<n;j++){work++;if(a>>j&1)can1[j]=true;else can0[j]=true}}}
      if(!allowed)return{bad:true,trace,work,conflict:f.id,forced:A.size-h.length};
      for(let j=0;j<n;j++)if(!A.has(f.s[j])&&(!can0[j]||!can1[j])){let b=+!!can1[j];A.set(f.s[j],b);trace.push([f.s[j],b,f.id]);change=true}
    }
   }
   for(let f of extra){let lo=0,hi=0;for(let [v,c] of f.a){work++;if(A.has(v)){lo+=c*A.get(v);hi+=c*A.get(v)}else{lo+=Math.min(c,0);hi+=Math.max(c,0)}}if(f.b<lo||f.b>hi)return{bad:true,trace,work,conflict:f.id,forced:A.size-h.length};for(let [v,c] of f.a)if(!A.has(v)){work++;let l=lo-Math.min(c,0),h=hi-Math.max(c,0),z=l<=f.b&&f.b<=h,o=l+c<=f.b&&f.b<=h+c;if(!z&&!o)return{bad:true,trace,work,conflict:f.id,forced:A.size-h.length};if(!z||!o){A.set(v,+!z);trace.push([v,+!z,f.id]);change=true;break}}}
  }
  return{bad:false,trace,work,forced:A.size-h.length,pins:[...A].sort((a,b)=>a[0]-b[0])}
 }
 function sums(D){let eq=[];for(let f of D)if(!f.a&&pop(f.counts)===1)eq.push({id:f.id,a:f.s.map((v,j)=>[v,(f.p>>j&1)?-1:1]),b:Math.log2(f.counts)-pop(f.p)});
  let out=[],same=[],attempts=0,seen=new Set();for(let i=0;i<eq.length;i++)for(let j=i+1;j<eq.length;j++){let e=eq[i],f=eq[j],a=e.a.map(x=>x[0]),b=f.a.map(x=>x[0]);if(!a.some(v=>b.includes(v)))continue;for(let sign of [-1,1]){attempts++;let m=new Map(e.a);for(let [v,c] of f.a)m.set(v,(m.get(v)||0)+sign*c);let r=[...m].filter(x=>x[1]).sort((a,b)=>a[0]-b[0]);if(r.length>=new Set(a.concat(b)).size||r.length>6)continue;let rhs=e.b+sign*f.b,k=JSON.stringify([r,rhs]);if(seen.has(k))continue;seen.add(k);let z={id:"sum"+(out.length+same.length),a:r,b:rhs,parents:[e.id,f.id,sign]};(a.join()===b.join()?same:out).push(z)}}return{eq,out,same,attempts}}
 function local(C,cl){let a=new Map(cl.map(l=>[Math.abs(l),+(l<0)])),why=new Map(),scans=0,hit=-1,change=true;
  while(change&&hit<0){change=false;for(let i=0;i<C.length;i++){let c=C[i],u=[],sat=false;for(let l of c){scans++;let b=a.get(Math.abs(l));if(b===undefined)u.push(l);else if(b===+(l>0)){sat=true;break}}if(sat)continue;if(!u.length){hit=i;break}if(u.length===1){let v=Math.abs(u[0]);a.set(v,+(u[0]>0));why.set(v,i);change=true}}}
  if(hit<0)return{ok:false,scans};let deps=new Set(),queue=[hit];for(let k=0;k<queue.length;k++){let i=queue[k];if(deps.has(i))continue;deps.add(i);for(let l of C[i]){let j=why.get(Math.abs(l));if(j!==undefined&&j!==i)queue.push(j)}}
  let ids=[...deps].sort((a,b)=>a-b),base=ids.map(i=>C[i]),replay=L.replay(base,[cl]),ablation=[];for(let z=0;z<ids.length;z++){let counter={visits:0};let t=L.up(base.filter((_,i)=>i!==z),cl.map(l=>-l),counter,1e7);ablation.push({omitted:ids[z],conflict:t.bad,visits:counter.visits})}
  return{ok:true,scans,ids,base,replay,ablation}
 }
 let out=[];
 for(let name of ["JOINT-24","RANDOM-3CNF-40"]){let x=corp.instances.find(y=>y.id===name),r=reg.instances.find(y=>y.alias==="EB-"+name),G=compile(x);
  assert(sha(enc(G.network))===r.sha256&&enc(G.network).length*8===r.N_bits&&sha(x.dimacs)===r.source_cnf.sha256&&x.dimacs.length*8===r.source_cnf.N_bits&&sha(enc(G.source_map))===r.source_map_sha256,"auth");
  let q=L.quotient(G.network),g=L.gauge(q.F),early=study(L,G.network,q,g,null,[],[],"EARLY_ONLY",[],name);
  let p=project(G.network),verification=verifyProjection(G.network,p),C=p.clauses.map(c=>canon(c)),cnf=x.dimacs.trimEnd().split("\n").slice(1).map(l=>canon(l.trim().split(/\s+/).map(Number).slice(0,-1))),F=p.final.map(f=>({id:f.id,s:f.s.map(v=>v+1),a:f.a})),D=compress(F),S=sums(D.D);
  let guard=[[p.anchor,0]],gid="GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",r.instance_id,"EB-PORT-PINS-v1",sha(enc(guard))])),chart={anchor:p.anchor,clauses:p.clauses,raw:p.raw,cond:p.cond,steps:p.steps,final:p.final},map={root:p.root,phase:p.phase},rid="RESIDUAL-v1:sha256:"+sha(enc(["PNP-RESIDUAL-v1",r.instance_id,gid,"EB-CHART-SYZYGY-v1",sha(enc(chart)),sha(enc(map))]));
  let vars=[...new Set(F.flatMap(f=>f.s))].sort((a,b)=>a-b),co=new Set();for(let f of F)for(let i=0;i<f.s.length;i++)for(let j=i+1;j<f.s.length;j++)co.add([f.s[i],f.s[j]].join());
  let pairs=[];for(let i=0;i<vars.length;i++)for(let j=i+1;j<vars.length;j++)pairs.push([vars[i],vars[j],co.has([vars[i],vars[j]].join())]);pairs.sort((a,b)=>Number(b[2])-Number(a[2])||a[0]-b[0]||a[1]-b[1]);
  let arms={};for(let [mode,fs,ex] of [["table",F,[]],["compressed",D.D,[]],["same",D.D,S.same],["cross",D.D,S.out]]){let start=Date.now(),root=closure(fs,[],ex),rows=[],work=root.work,tests=0;for(let [a,b,c] of pairs.slice(0,160))for(let x of [-a,a])for(let y of [-b,b]){let h=[x,y],z=closure(fs,h,ex);tests++;work+=z.work;if(z.bad)rows.push({h,co:c,conflict:z.conflict})}arms[mode]={root,rows,work,tests,ms:Date.now()-start}}
  assert(JSON.stringify(arms.table.rows.map(z=>z.h))===JSON.stringify(arms.compressed.rows.map(z=>z.h)),"matched conflicts");
  let old=new Set(arms.table.rows.map(z=>z.h.join())),newRows=arms.cross.rows.filter(z=>!old.has(z.h.join())),extraReplay=[];for(let z of newRows){let t=closure(F,z.h,S.out);assert(t.bad,"hybrid replay");extraReplay.push({h:z.h,t})}
  let blind=arms.compressed.rows.slice(0,8).map(z=>{let cl=canon(z.h.map(l=>-l));return{cl,local:local(C,cl)}});
  let peerTests=[],base=C.slice();if(name==="RANDOM-3CNF-40")for(let cl of [[362,34],[362,-33],[362,298]]){let z=local(base,cl);peerTests.push({cl,local:z});if(z.ok)base.push(cl)}
  let five=study(L,G.network,q,g,{F},C,[],[],cnf,name);
  out.push({name,registry:r,source_pin:pins,guard_id:gid,residual_id:rid,guard,chartHash:sha(enc(chart)),mapHash:sha(enc(map)),original_ids:{vertices:[0,G.network.types.length-1],ports:[0,4*G.network.types.length-1],edges:[0,G.network.edges.length-1]},early,projection:{carriers:p.carriers,eliminated:p.steps.length,vars:vars.length,verification,cost:p.cost},F,C,compression:D,sums:S,arms,extraReplay,blind,peerTests,five});
 }
 return out
};
console.log(JSON.stringify(run(data,pins)));
