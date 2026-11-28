const fs=require('node:fs');
const pins={"registry":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"compiler":["research/coordination/shared-eb-2026-11-27/compile.js","21b9d53fb8166c819b24e708656c742cd3c24f10"],"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"syndrome":["research/coordination/2026-11-28_0300_UCAC_review/syndrome.js","77f2a7224d75dd9c08b733cf6879733c92c80775"],"native":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_native_transport_replay/native.js","303d735ba73855b69b47df734d4d3686f760b215"],"peer":["research/proof-spine-2026-11-26/closure-exceptional-syndrome/2026-11-28_0316_T3_period_quotient/verified-contractions.json","dffc6eba18448a73075ff99a92ee7626d0c5e3ec"],"overlap":["research/agents/ground-up-unsat-bounds/2026-11-28_T3_constructive_overlap/overlap.js","309310f39fd740326e85600ec9b3eb2036fc1637"],"results":["research/agents/ground-up-unsat-bounds/2026-11-28_T3_constructive_overlap/overlap-results.json","0c45a7bc4d5da20790c28e95bf860267689dfeb2"]};
const data=Object.fromEntries(Object.keys(pins).map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));
const run=function run(data){
 const A=(x,m)=>{if(!x)throw Error(m)},enc=x=>JSON.stringify(x)+"\n";
 const compile=new Function("return function compile"+data.compiler.split("function compile")[1].split("function auditLocal")[0])();
 const {sha}=new Function(data.native+";return {sha};")();
 const chart=new Function(data.syndrome.slice(0,data.syndrome.indexOf(" const m=forms.length")).replace("function analyze(g)","function chart(g)")+"\n return {H,forms,edges,port,basis,counts};\n}; return chart;")();
 // Reconstruct the actual ordered conflict blocks using sorted BFS, rather than importing any response table.
 function solve(g,cert,ablate=false,mode="source"){
  let t=chart(g),{H,forms,edges}=t,n=forms.length,cols=Array(n).fill(0n),target=0n;
  for(let j=0;j<H.length;j++){let p=1n<<BigInt(j);if(H[j]&1n)target|=p;for(let i=0;i<n;i++)if(H[j]&(1n<<BigInt(i+1)))cols[i]|=p}
  A(target.toString(16)===cert.check.target,"target chart");
  let adj=Array.from({length:n},()=>[]);for(let [a,b] of edges){adj[a].push(b);adj[b].push(a)}
  let seen=new Set(),B=[],work={xor:0,pivot:0,products:0,filters:0,options:0,steps:0,transitions:0,score:0};
  for(let i=0;i<n;i++){if(seen.has(i))continue;let V=[i];seen.add(i);for(let k=0;k<V.length;k++)for(let v of adj[V[k]])if(!seen.has(v)){seen.add(v);V.push(v)}V.sort((a,b)=>a-b);A(V.length<=12,"block cap");let S=new Set();for(let j=0;j<2**V.length;j++){work.options++;let active=V.filter((_,k)=>j>>k&1),a=new Set(active);if(active.some(v=>adj[v].some(w=>a.has(w))))continue;S.add(active.reduce((x,v)=>x^cols[v],0n))}B.push({id:B.length,S})}
  A(B.length===cert.check.initialBlocks&&B.reduce((s,b)=>s+b.S.size,0)===cert.check.initialOptions,"source blocks");
  // Independent low-pivot basis; peer checker uses high pivots.
  function add(M,x){while(x){work.pivot++;let p=x&-x;if(!M.has(p)){M.set(p,x);return}x^=M.get(p);work.xor++}}
  function member(M,x){while(x){work.pivot++;let p=x&-x;if(!M.has(p))return false;x^=M.get(p);work.xor++}return true}
  function hull(list){let M=new Map(),o=0n;for(let c of list){let a=c.S.values().next().value;A(a!==undefined,"empty block");o^=a;for(let v of c.S)add(M,v^a)}return {M,o}}
  let initial=B.length,K=64,d=H.length,phi=()=> (B.length+d)*(initial*K+1)+B.reduce((n,b)=>n+b.S.size,0),initialPhi=phi(),prev=initialPhi;
  let trace=ablate?cert.trace.slice(0,-1):cert.trace;
  for(let e of trace){work.steps++;if(e.kind==="fuse"){let i=B.findIndex(c=>c.id===e.a),j=B.findIndex(c=>c.id===e.b);A(i>=0&&j>=0&&i!==j&&!B.some(c=>c.id===e.id),"fuse ID");let S=new Set();for(let u of B[i].S)for(let v of B[j].S){work.products++;S.add(u^v)}A(S.size===e.size&&S.size<=K,"fuse exact");B=B.filter((_,k)=>k!==i&&k!==j);B.splice(Math.min(i,j),0,{id:e.id,S})}
   else if(e.kind==="filter"){let i=B.findIndex(c=>c.id===e.id);A(i>=0&&B[i].S.size===e.from,"filter ID");let {M,o}=hull(B.filter((_,j)=>j!==i)),S=new Set();for(let v of B[i].S){work.filters++;if(member(M,target^o^v))S.add(v)}A(S.size===e.to&&S.size>0&&S.size<e.from,"filter exact");B[i]={id:e.id,S}}
   else throw Error("unsupported parent");
   A(phi()<prev,"credit");prev=phi()
  }
  if(!ablate)A(B.length===cert.check.finalBlocks&&B.reduce((s,b)=>s+b.S.size,0)===cert.check.finalOptions&&phi()===cert.check.phi,"final summary");
  let replayWork={...work};let rank=[];
  if(mode==="greedy"){
   // Order using affine hull variation support, not common offsets.
   let supports=B.map(c=>{let a=c.S.values().next().value,u=0n;for(let v of c.S)u|=v^a;return u}), rows=Array.from({length:H.length},()=>[]);
   supports.forEach((x,i)=>{while(x){let p=x&-x;rows[p.toString(2).length-1].push(i);x^=p}});
   let br=B.map(()=>[]);rows.forEach((r,j)=>r.forEach(i=>br[i].push(j)));let left=rows.map(r=>r.length),used=rows.map(()=>0),rem=new Set(B.map((_,i)=>i)),order=[];
   while(rem.size){let best=-1,bscore=Infinity,bt=-1;for(let i of rem){let s=0,t=0;for(let j of br[i]){work.score++;if(used[j]&&left[j]===1)s--;else if(!used[j]&&left[j]>1)s++;if(used[j])t++}if(s<bscore||(s===bscore&&t>bt)){best=i;bscore=s;bt=t}}order.push(best);rem.delete(best);for(let j of br[best]){left[j]--;used[j]++}}
   B=order.map(i=>B[i]);
  }
  const suf=Array(B.length+1);suf[B.length]={M:new Map(),o:0n};for(let i=B.length-1;i>=0;i--){let a=B[i].S.values().next().value,M=new Map(suf[i+1].M);for(let v of B[i].S)add(M,v^a);suf[i]={M,o:suf[i+1].o^a}}
  let pre=new Map(),r=suf[0].M.size;rank.push(0);for(let i=0;i<B.length;i++){let a=B[i].S.values().next().value;for(let v of B[i].S)add(pre,v^a);rank.push(pre.size+suf[i+1].M.size-r)}
  let S=new Set([0n]),peak=1,stop=null,decision="UNKNOWN";outer:for(let i=0;i<B.length;i++){let Q=new Set(),{M,o}=suf[i+1];for(let u of S)for(let v of B[i].S){work.transitions++;let w=u^v;if(member(M,target^w^o))Q.add(w);if(Q.size>2048){stop=i;peak=2049;break outer}}S=Q;peak=Math.max(peak,S.size);if(!S.size){decision="NO";break}}
  if(stop===null&&decision!=="NO")decision=S.has(target)?"YES":"NO";
  return {ablate,mode,initial,finalBlocks:B.length,finalOptions:B.reduce((n,b)=>n+b.S.size,0),initialPhi,finalPhi:prev,replayWork,work,rankWidth:Math.max(...rank),peak,stop,decision,order:B.map(c=>c.id)};
 }
 let peer=JSON.parse(data.peer),peerSha=sha(data.peer);A(peerSha==="800c5f2d6babf1adfc41cb2cced70a7c7451b7cc1414521dd8ef712d999462c1","parent digest");
 let out=[];for(let cert of peer.certs){let reg=JSON.parse(data.registry).instances.find(x=>x.alias===cert.entry.alias),s=JSON.parse(data.corpus).instances.find(x=>"EB-"+x.id===reg.alias),g=compile({nvars:s.nvars,dimacs:s.dimacs});A(sha(enc(g.network))===reg.sha256&&enc(g.network).length*8===reg.N_bits&&sha(s.dimacs)===reg.source_cnf.sha256&&sha(enc(g.source_map))===reg.source_map_sha256,"auth");let arms=[solve(g.network,cert),solve(g.network,cert,false,"greedy"),solve(g.network,cert,true,"greedy")];out.push({source:reg,parent:peerSha,initialId:cert.ids.initial,finalId:cert.ids.final,arms})}
 return out;
};
console.log(JSON.stringify(run(data),null,2));
