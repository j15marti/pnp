const fs=require('node:fs');
const pins={"registry":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"compiler":["research/coordination/shared-eb-2026-11-27/compile.js","21b9d53fb8166c819b24e708656c742cd3c24f10"],"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"syndrome":["research/coordination/2026-11-28_0300_UCAC_review/syndrome.js","77f2a7224d75dd9c08b733cf6879733c92c80775"],"native":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_native_transport_replay/native.js","303d735ba73855b69b47df734d4d3686f760b215"]};
const data=Object.fromEntries(Object.keys(pins).map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));
const run=function run(data){
 const A=(x,m)=>{if(!x)throw Error(m)}, enc=x=>JSON.stringify(x)+"\n";
 const compile=new Function("return function compile"+data.compiler.split("function compile")[1].split("function auditLocal")[0])();
 const {sha,norm,project,replay,up,canon,key,check}=new Function(data.native+";return {sha,norm,project,replay,up,canon,key,check};")();
 const chartCode=data.syndrome.slice(0,data.syndrome.indexOf(" const m=forms.length")).replace("function analyze(g)","function chart(g)")+"\n return {H,forms,edges,port,basis,counts,carriers:roots.size,parityRank,forced};\n}";
 const chart=new Function(chartCode+";return chart;")();
 function solver(g,mode,cap=2048){
  const t=chart(g);if(t.decision)return {decision:t.decision,reason:t.reason,counts:t.counts};
  const {H,edges,forms,port,basis}=t,m=forms.length,cols=Array(m).fill(0n);let target=0n;
  for(let j=0;j<H.length;j++){let b=1n<<BigInt(j);if(H[j]&1n)target|=b;for(let i=0;i<m;i++)if(H[j]&(1n<<BigInt(i+1)))cols[i]|=b}
  let parent=Array.from({length:m},(_,i)=>i),root=i=>{while(parent[i]!==i)i=parent[i];return i};
  for(let [a,b] of edges)parent[root(a)]=root(b);
  let map=new Map();for(let i=0;i<m;i++){let r=root(i);if(!map.has(r))map.set(r,[]);map.get(r).push(i)}
  const blocks=[...map.values()],B=blocks.length,blockOf=new Map();blocks.forEach((b,i)=>b.forEach(v=>blockOf.set(v,i)));
  const meter={rank:0,rankXor:0,score:0,optionTests:0,transitions:0,checks:0,verification:0};
  function add(M,x){while(x){meter.rank++;let p=x&-x;if(!M.has(p)){M.set(p,x);return}x^=M.get(p);meter.rankXor++}}
  function member(M,x){while(x){meter.rank++;let p=x&-x;if(!M.has(p))return false;x^=M.get(p);meter.rankXor++}return true}
  let opts=blocks.map(V=>{if(V.length>12)return null;let ix=new Map(V.map((v,j)=>[v,j])),E=edges.filter(([a])=>ix.has(a)),o=new Map();for(let q=0;q<2**V.length;q++){meter.optionTests++;if(E.some(([a,b])=>(q>>ix.get(a)&1)&&(q>>ix.get(b)&1)))continue;let u=0n,z=0n;for(let j=0;j<V.length;j++)if(q>>j&1){u^=cols[V[j]];z|=1n<<BigInt(V[j]+1)}if(!o.has(u))o.set(u,z)}return o});
  if(opts.some(x=>!x))return {decision:"UNKNOWN",reason:"block cap"};
  // Sparse row adjacency, deterministic traversal minimizing number of live rows (not claimed optimal rank).
  const support=blocks.map(V=>V.reduce((x,v)=>x|cols[v],0n)),rowBlocks=Array.from({length:H.length},()=>[]);
  support.forEach((s,i)=>{while(s){let p=s&-s,j=p.toString(2).length-1;rowBlocks[j].push(i);s^=p}});
  const br=blocks.map(()=>[]);rowBlocks.forEach((bb,j)=>bb.forEach(i=>br[i].push(j)));
  function orderGreedy(){let left=Uint32Array.from(rowBlocks.map(a=>a.length)),used=new Uint32Array(H.length),done=new Set(),order=[];for(let k=0;k<B;k++){let best=-1,sbest=Infinity,tbest=-1;for(let i=0;i<B;i++)if(!done.has(i)){let d=0,touch=0;for(let r of br[i]){meter.score++;if(used[r]&&left[r]===1)d--;else if(!used[r]&&left[r]>1)d++;if(used[r])touch++}if(d<sbest||(d===sbest&&touch>tbest)){sbest=d;tbest=touch;best=i}}done.add(best);order.push(best);for(let r of br[best]){left[r]--;used[r]++}}return order}
  let order=mode==="greedy"?orderGreedy():blocks.map((_,i)=>i);
  const suffix=Array(B+1);suffix[B]=new Map();for(let i=B-1;i>=0;i--){let M=new Map(suffix[i+1]);for(let v of opts[order[i]].keys())add(M,v);suffix[i]=M}
  const pre=new Map(),widths=[0];for(let i=0;i<B;i++){for(let v of opts[order[i]].keys())add(pre,v);widths.push(pre.size+suffix[i+1].size-suffix[0].size)}
  const stats={mode,blocks:B,maxBlock:Math.max(0,...blocks.map(x=>x.length)),maxWidth:Math.max(...widths),order,widths,chart:{carriers:t.carriers,parityRank:t.parityRank,forced:t.forced,forms:m,syndromeRank:H.length,counts:t.counts},meter};
  // Do not pre-reject on rank: measure actual live states; fixed cap, no dropping states.
  let states=new Map([[0n,0n]]),sizes=[1],decision="UNKNOWN",z=null,stop=null;
  outer:for(let i=0;i<B;i++){let next=new Map();for(let [u,x] of states)for(let [v,y] of opts[order[i]]){meter.transitions++;let s=u^v;if(member(suffix[i+1],target^s)&&!next.has(s)){next.set(s,x|y);if(next.size>cap){stop=i;break outer}}}states=next;sizes.push(states.size);if(!states.size){decision="NO";break}}
  if(stop===null&&decision!=="NO"){decision=states.has(target)?"YES":"NO";if(decision==="YES")z=states.get(target)}
  let lifted=null;
  if(z!==null){const M=new Map(basis);function ins(x){while(x&~1n){let p=(x&~1n)&-(x&~1n);if(!M.has(p)){M.set(p,x);return true}x^=M.get(p)}return x===0n}
   for(let i=0;i<m;i++)A(ins(forms[i]^1n^((z>>BigInt(i+1))&1n)),"lift");
   let x=0n;function parity(y){let p=0;while(y){y&=y-1n;p^=1}return p}
   for(let [p,r] of [...M].sort((a,b)=>a[0]>b[0]?-1:1))if(parity(r&x)^Number(r&1n))x|=p;
   lifted=port.map(v=>parity(v&x)^Number(v&1n));A(g.edges.every(([a,b,s])=>{meter.verification++;return (lifted[a]^lifted[b])===s})&&g.types.every((k,i)=>{meter.verification++;let q=lifted.slice(4*i,4*i+4);return k==="E"?q.every(x=>x===q[0]):q.reduce((x,y)=>x+y,0)===2}),"source witness");
  }
  return {...stats,decision,stop,peak:Math.max(...sizes,stop===null?0:cap+1),sizes,witness:z===null?null:z.toString(16),lifted};
 }
 function dpll(C){let meter={scans:0,lits:0,nodes:0,cap:2000000},witness=null;function go(g){meter.nodes++;let r=up(C,g,meter);if(r.conflict)return null;if(r.all){witness=[...r.A];return "SAT"}let v=[...r.score].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0],a=go([...g,[v,0]]);if(witness)return "SAT";let b=go([...g,[v,1]]);return witness?"SAT":[v,a,b]}try{let tree=go([]);return {decision:witness?"YES":"NO",tree,witness,meter,check:witness?null:check(C,tree)}}catch(e){if(e.message!=="cap")throw e;return {decision:"UNKNOWN",meter}}}
 const out=[];
 for(let alias of ["JOINT-24","RANDOM-3CNF-40"]){let s=JSON.parse(data.corpus).instances.find(x=>x.id===alias),reg=JSON.parse(data.registry).instances.find(x=>x.alias==="EB-"+alias),g=compile({nvars:s.nvars,dimacs:s.dimacs});A(sha(enc(g.network))===reg.sha256&&enc(g.network).length*8===reg.N_bits&&sha(s.dimacs)===reg.source_cnf.sha256&&s.dimacs.length*8===reg.source_cnf.N_bits&&sha(enc(g.source_map))===reg.source_map_sha256,"auth");let n=norm(g.network),p=project(n.C,128),r=replay(n.C,p.trace);A(enc(p.C)===enc(r.C),"projection");let cnf=s.dimacs.trim().split("\n").slice(1).map(l=>canon(l.trim().split(/\s+/).map(Number).slice(0,-1)));out.push({alias,source:reg,baseline:dpll(p.C),cnf:dpll(cnf),projection:{scans:p.scans,pairs:p.pairs,replayScans:r.scans,replayPairs:r.pairs},arms:[solver(g.network,"source"),solver(g.network,"greedy")]})}
 // Small compiled opposite-label controls, no reference assignments supplied to solver.
 for(let [name,C] of [["SAT-overlap",[[1,2],[-1,3],[-2,3]]],["NO-overlap",[[1,2],[-1,3],[-2,3],[-3]]]]){let dimacs="p cnf 3 "+C.length+"\n"+C.map(c=>c.join(" ")+" 0").join("\n")+"\n",g=compile({nvars:3,dimacs});out.push({alias:name,hash:sha(enc(g.network)),N:enc(g.network).length*8,dimacs,arms:[solver(g.network,"source"),solver(g.network,"greedy")]})}
 return out;
};
console.log(JSON.stringify(run(data),null,2));
