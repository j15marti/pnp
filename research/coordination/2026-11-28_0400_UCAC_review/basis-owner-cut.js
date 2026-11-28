function run(compiler,corpus,registry,syndrome,replayCode,parent){
 const compile=Function(compiler.slice(compiler.indexOf("function compile("),compiler.indexOf("function auditLocal"))+";return compile;")();
 const prior=Function("const module={exports:{}};"+syndrome+";return module.exports;")();
 const chart=Function(syndrome.slice(0,syndrome.indexOf("module.exports")).replace("const m=forms.length,par=","return {H,edges,m:forms.length,counts,forced,parityRank,carriers:roots.size}; const m=forms.length,par=")+";return analyze;")();
 const replay=Function("const module={exports:{}};"+replayCode+";return module.exports.replay;")();
 const sha=prior.sha;
 if(sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"||sha(parent)!=="800c5f2d6babf1adfc41cb2cced70a7c7451b7cc1414521dd8ef712d999462c1")throw Error("hash");
 const reg=JSON.parse(registry),cor=JSON.parse(corpus),p=JSON.parse(parent);
 function assess(D,target){
  const count={tests:0,xors:0,pairs:0,terms:0};let b=target;
  let blocks=D.map(x=>{let a=BigInt("0x"+x.S[0]);b^=a;return {id:x.id,S:x.S.map(y=>BigInt("0x"+y)^a)}});
  const add=(B,x)=>{while(x){count.tests++;const k=x&-x;if(!B.has(k)){B.set(k,x);return}x^=B.get(k);count.xors++}};
  const member=(B,x)=>{while(x){count.tests++;const k=x&-x;if(!B.has(k))return false;x^=B.get(k);count.xors++}return true};
  const local=blocks.map(C=>{let B=new Map();for(let x of C.S)add(B,x);return [...B.values()]});
  const n=blocks.length,seq=Array.from({length:n},(_,i)=>i),all=new Map();for(let L of local)for(let x of L)add(all,x);
  if(!member(all,b))return {rank:all.size,decision:"NO-affine-hull",count};
  // Basis-owner graph, exact coordinate tags in the selected global basis.
  const G=new Map(),owners=[];
  count.tagTests=0;count.tagXors=0;
  for(let i=0;i<n;i++)for(let x of local[i]){
    let y=x,t=0n;
    while(y){count.tagTests++;let k=y&-y;if(!G.has(k)){let tag=1n<<BigInt(owners.length);owners.push(i);G.set(k,[y,t^tag]);break}let [v,u]=G.get(k);y^=v;t^=u;count.tagXors++}
  }
  if(owners.length!==all.size)throw Error("basis rank");
  function coord(x){let t=0n;while(x){count.tagTests++;let k=x&-x;if(!G.has(k))throw Error("coordinate");let [v,u]=G.get(k);x^=v;t^=u;count.tagXors++}return t}
  const W=Array.from({length:n},()=>new Map());
  for(let i=0;i<n;i++)for(let x of local[i]){let z=coord(x);while(z){let k=z&-z;z^=k;let h=k.toString(2).length-1,j=owners[h];if(i===j)continue;W[i].set(j,(W[i].get(j)||0)+1);W[j].set(i,(W[j].get(i)||0)+1);count.pairs++}}
  const deg=W.map(x=>[...x.values()].reduce((a,b)=>a+b,0));let maxD=Math.max(1,...deg);
  let v=seq.map(i=>Math.round(1000000*(2*i-(n-1))/Math.max(1,n-1)));
  for(let t=0;t<48;t++){let u=v.map((x,i)=>{let s=(2*maxD-deg[i])*x;for(let [j,w] of W[i]){s+=w*v[j];count.terms++}if(!Number.isSafeInteger(s))throw Error("precision");return Math.trunc(s/(2*maxD))});let avg=Math.trunc(u.reduce((a,x)=>a+x,0)/Math.max(1,n));u=u.map(x=>x-avg);let mx=Math.max(1,...u.map(Math.abs));v=u.map(x=>Math.trunc(x*1000000/mx))}
  let spectral=seq.slice().sort((i,j)=>v[i]-v[j]||i-j);
  function attempt(name,order){
   const before={...count};let suffix=Array(n+1);suffix[n]=new Map();
   for(let i=n-1;i>=0;i--){let B=new Map(suffix[i+1]);for(let x of local[order[i]])add(B,x);suffix[i]=B}
   let pre=new Map(),width=0;for(let i=0;i<n;i++){for(let x of local[order[i]])add(pre,x);width=Math.max(width,pre.size+suffix[i+1].size-all.size)}
   let states=new Set([0n]),peak=1,transitions=0,completed=0,decision="UNKNOWN",reason="";
   outer:for(let i=0;i<n;i++){let next=new Set();for(let u of states)for(let x of blocks[order[i]].S){if(transitions>=250000){reason="transition cap";break outer}transitions++;let z=u^x;if(member(suffix[i+1],b^z)){next.add(z);if(next.size>4096){peak=Math.max(peak,next.size);reason="state cap";break outer}}}states=next;completed++;peak=Math.max(peak,states.size);if(!states.size){decision="NO";break}}
   if(completed===n&&decision!=="NO")decision=states.has(b)?"YES":"NO";
   return {name,order:order.map(i=>blocks[i].id),width,completed,peak,transitions,decision,reason,tests:count.tests-before.tests,xors:count.xors-before.xors};
  }
  const arms=[attempt("source",seq),attempt("spectral",spectral),attempt("reverse-spectral",spectral.slice().reverse())];
  return {blocks:n,options:blocks.reduce((a,x)=>a+x.S.length,0),rank:all.size,arms,count};
 }
 const cases=[];
 for(let cert of p.certs){
  let e=reg.instances.find(x=>x.alias===cert.entry.alias),x=cor.instances.find(x=>x.id===e.source_cnf.alias),g=compile(x),bytes=JSON.stringify(g.network)+"\n",map=JSON.stringify(g.source_map)+"\n";
  let hashes={native:sha(bytes),map:sha(map),cnf:sha(x.dimacs),N:bytes.length*8,cnfN:x.dimacs.length*8};
  if(hashes.native!==e.sha256||hashes.map!==e.source_map_sha256||hashes.cnf!==e.source_cnf.sha256||hashes.N!==e.N_bits||hashes.cnfN!==e.source_cnf.N_bits)throw Error("authentication "+e.alias);
  let C=chart(g.network);if(!C.H)throw Error("chart");
  let root=replay(C.H,C.edges,C.m,[],false),contracted=replay(C.H,C.edges,C.m,cert.trace,false),ablate=replay(C.H,C.edges,C.m,cert.trace.slice(0,-1),false);
  cases.push({entry:e,hashes,closure:{counts:C.counts,forced:C.forced,rank:C.parityRank,carriers:C.carriers},parent:{steps:cert.trace.length,replay:contracted.stats,ablation:ablate.stats,phi0:contracted.phi0,phi:contracted.phi},source:assess(root.finalDictionaries,BigInt("0x"+root.target)),contracted:assess(contracted.finalDictionaries,BigInt("0x"+contracted.target)),ablation:assess(ablate.finalDictionaries,BigInt("0x"+ablate.target)),companion:prior.cnfSolve(x.dimacs)});
 }
 const controls=[];
 for(let i=0;i<3;i++){
  let clauses=i===0?[[1,2,3],[-1,2,-3]]:i===1?[[1],[-1]]:[[1,-2,3],[-1,2,-3],[2,3]];
  let dimacs="p cnf 3 "+clauses.length+"\n"+clauses.map(x=>x.join(" ")+" 0").join("\n")+"\n",g=compile({nvars:3,dimacs}),s=JSON.stringify(g.network)+"\n",C=chart(g.network),native=prior.analyze(g.network);
  let a=C.H?replay(C.H,C.edges,C.m,[],false):null;
  controls.push({dimacs,instance:"STRICT-EB4-v1:sha256:"+sha(s),N:s.length*8,expected:prior.cnfSolve(dimacs).decision,native,order:a?assess(a.finalDictionaries,BigInt("0x"+a.target)):null});
 }
 return {cases,controls,precision:"48 deterministic fixed-point diffusion steps, magnitude 10^6, checked safe integer numerator; no spectral inference",scope:"root chart, replayed parent trace with same chart constructor; not independent native proof; last step removed (not full LOO); no new witness lift in DP, YES control checked by prior terminal",clock:"per-arm state and transition caps; event proxies not unified bit clock; serial"};
}
module.exports={run};
