function run(compiler,corpus,registry,syndrome,replayCode,parent){
 const compile=Function(compiler.slice(compiler.indexOf("function compile("),compiler.indexOf("function auditLocal"))+";return compile;")();
 const prior=Function("const module={exports:{}};"+syndrome+";return module.exports;")();
 const chart=Function(syndrome.slice(0,syndrome.indexOf("module.exports")).replace("const m=forms.length,par=","return {H,edges,m:forms.length,counts,forced,parityRank,carriers:roots.size}; const m=forms.length,par=")+";return analyze;")();
 const replay=Function("const module={exports:{}};"+replayCode+";return module.exports.replay;")();
 const sha=prior.sha,reg=JSON.parse(registry),cor=JSON.parse(corpus),p=JSON.parse(parent);
 if(sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"||sha("")!=="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"||sha(parent)!=="800c5f2d6babf1adfc41cb2cced70a7c7451b7cc1414521dd8ef712d999462c1")throw Error("hash");
 function assess(D,t){
  let c={rankTests:0,xors:0,coordTests:0,coordXors:0,ownerProbes:0,projectionWords:0,replayPairs:0,periodChecks:0,quotientWords:0,cuts:0,graphIncidences:0};
  let b=t,A=D.map((x,i)=>{let S=x.S.map(y=>BigInt("0x"+y)),a=S[0];b^=a;return {i,id:x.id,S:S.map(y=>y^a)}});
  const add=(B,x)=>{while(x){c.rankTests++;let k=x&-x;if(!B.has(k)){B.set(k,x);return}x^=B.get(k);c.xors++}};
  const span=S=>{let B=new Map();for(let x of S)add(B,x);return B};
  let G=new Map(),owners=[],basis=[],masks=Array(A.length).fill(0n);
  for(let F of A)for(let x of span(F.S).values()){let y=x,z=0n;while(y){c.coordTests++;let k=y&-y;if(!G.has(k)){let bit=1n<<BigInt(owners.length);owners.push(F.i);basis.push(x);masks[F.i]|=bit;G.set(k,[y,z^bit]);break}let [v,u]=G.get(k);y^=v;z^=u;c.coordXors++}}
  const coord=x=>{let z=0n;while(x){c.coordTests++;let k=x&-x;if(!G.has(k))throw Error("span");let [v,u]=G.get(k);x^=v;z^=u;c.coordXors++}return z};
  const inverse=z=>{let x=0n;while(z){let k=z&-z;z^=k;x^=basis[k.toString(2).length-1];c.coordXors++}return x};
  let q=coord(b),F=A.map(x=>({i:x.i,id:x.id,S:x.S.map(s=>{let z=coord(s);if(inverse(z)!==s)throw Error("inverse");return z})}));
  function width(X){
   let L=span(X.flatMap(x=>x.S)),n=A.length,pre=new Map(),suf=Array(n+1);suf[n]=new Map();let by=Array.from({length:n},()=>[]);for(let x of X)by[x.i].push(...x.S);
   for(let i=n-1;i>=0;i--){let B=new Map(suf[i+1]);for(let x of by[i])add(B,x);suf[i]=B}
   let w=0,sum=0;for(let i=0;i<n;i++){for(let x of by[i])add(pre,x);let l=pre.size+suf[i+1].size-L.size;c.cuts++;w=Math.max(w,l);sum+=l}return {rank:L.size,width:w,cutSum:sum}
  }
  function comps(X){
   // exact coordinate-factor hypergraph; every factor touches all its nonzero coordinate bits.
   let par=owners.map((_,i)=>i);const find=i=>{while(par[i]!==i)i=par[i];return i};let unused=0n;
   for(let x of X){let u=x.S.reduce((a,b)=>a|b,0n);unused|=u;let first=-1;while(u){let k=u&-u;u^=k;let i=k.toString(2).length-1;c.graphIncidences++;if(first<0)first=i;else par[find(i)]=find(first)}}
   let sizes=new Map();for(let i=0;i<owners.length;i++)if(unused&(1n<<BigInt(i))){let r=find(i);sizes.set(r,(sizes.get(r)||0)+1)}
   return [...sizes.values()].sort((a,b)=>b-a)
  }
  let before=width(F),beforeComp=comps(F),splitTrace=[],factors=[];
  for(let f of F){let S=f.S.slice();let order=[f.i,...masks.map((_,j)=>j).filter(j=>j!==f.i)];let original=new Set(S);
   for(let j of order){let M=masks[j];if(!M)continue;let U=S.reduce((a,b)=>a|b,0n);if(!(U&M)||!(U&~M))continue;c.ownerProbes++;
    let P=[...new Set(S.map(x=>x&M))],R=[...new Set(S.map(x=>x&~M))];c.projectionWords+=2*S.length;
    if(P.length*R.length!==S.length)continue;
    // independent product replay against pre-split exact support, not only cardinality.
    let W=new Set(S);for(let x of P)for(let y of R){c.replayPairs++;if(!W.has(x^y))throw Error("bad product")}
    factors.push({i:f.i,id:f.id,S:P});splitTrace.push({block:f.id,owner:j,before:S.length,left:P.length,right:R.length});S=R;
   }
   factors.push({i:f.i,id:f.id,S});
   // Independent direct reconstruction of each original local support (bounded by original size).
   let words=[0n];for(let v of factors.filter(x=>x.i===f.i)){words=words.flatMap(x=>v.S.map(y=>x^y));if(words.length>original.size)throw Error("reconstruction growth")}
   if(words.length!==original.size||words.some(x=>!original.has(x)))throw Error("reconstruction");
  }
  let afterSplit=width(factors),splitComp=comps(factors);if(JSON.stringify(before)!==JSON.stringify(afterSplit))throw Error("grouped cut changed under exact split");
  // Period absorption, in tagged coordinates, with exact closure check and reverse correction.
  function quotient(X,target){
   X=X.map(x=>({...x,S:x.S.slice()}));let trace=[];
   for(;;){let chosen=null;outer:for(let i=0;i<X.length;i++){let S=X[i].S,W=new Set(S);for(let p of S){if(!p)continue;let ok=true;for(let s of S){c.periodChecks++;if(!W.has(s^p)){ok=false;break}}if(ok){chosen={i,p};break outer}}}if(!chosen)break;
    let {i,p}=chosen,k=p&-p,pi=x=>x&k?x^p:x;
    for(let s of X[i].S){c.periodChecks++;if(!X[i].S.includes(s^p))throw Error("period replay")}
    let old=width(X);let oldS=X[i].S.slice();target=pi(target);X=X.map(x=>{c.quotientWords+=x.S.length;return {...x,S:[...new Set(x.S.map(pi))]}});let now=width(X);
    if(now.rank!==old.rank-1||now.width>old.width)throw Error("cut monotonicity");
    trace.push({owner:X[i].id,p:p.toString(16),pivot:k.toString(16),ownerOptions:oldS.map(x=>x.toString(16)),old,now});
   }return {X,target,trace};
  }
  let baseline=quotient(F,q),hybrid=quotient(factors,q),post=width(hybrid.X),postComp=comps(hybrid.X);
  if(width(baseline.X).rank!==post.rank)throw Error("period rank disagreement");
  return {blocks:A.length,options:A.reduce((n,x)=>n+x.S.length,0),ownerRank:owners.length,before,beforeComp,splitTrace,afterSplit,splitComp,baselinePeriods:baseline.trace,hybridPeriods:hybrid.trace,post,postComp,factors:factors.length,count:c,target:q.toString(16),scope:"exact support splits and local periods; grouped original cuts; no native terminal claimed"};
 }
 let cases=[];
 for(let cert of p.certs){
  let e=reg.instances.find(x=>x.alias===cert.entry.alias),x=cor.instances.find(x=>x.id===e.source_cnf.alias),g=compile(x),bytes=JSON.stringify(g.network)+"\n",map=JSON.stringify(g.source_map)+"\n";
  let hashes={native:sha(bytes),map:sha(map),cnf:sha(x.dimacs),N:bytes.length*8,cnfN:x.dimacs.length*8};
  if(hashes.native!==e.sha256||hashes.map!==e.source_map_sha256||hashes.cnf!==e.source_cnf.sha256||hashes.N!==e.N_bits||hashes.cnfN!==e.source_cnf.N_bits)throw Error("authentication "+e.alias);
  let C=chart(g.network);if(!C.H)throw Error("chart");
  let R=replay(C.H,C.edges,C.m,[],false),P=replay(C.H,C.edges,C.m,cert.trace,false),L=replay(C.H,C.edges,C.m,cert.trace.slice(0,-1),false);
  cases.push({entry:e,hashes,closure:{counts:C.counts,forced:C.forced,rank:C.parityRank,carriers:C.carriers},parent:{steps:cert.trace.length,replay:P.stats,lastStepRemoved:L.stats},source:assess(R.finalDictionaries,BigInt("0x"+R.target)),hybrid:assess(P.finalDictionaries,BigInt("0x"+P.target)),ablation:assess(L.finalDictionaries,BigInt("0x"+L.target)),companion:prior.cnfSolve(x.dimacs)});
 }
 // Native both-label regression; prior analyzer directly verifies YES witnesses.
 let controls=[];for(let clauses of [[[1,2,3],[-1,2,-3]],[[1],[-1]]]){
 let dimacs="p cnf 3 "+clauses.length+"\n"+clauses.map(x=>x.join(" ")+" 0").join("\n")+"\n",g=compile({nvars:3,dimacs}),s=JSON.stringify(g.network)+"\n",C=chart(g.network),v=prior.analyze(g.network);
 let a=C.H?replay(C.H,C.edges,C.m,[],false):null;controls.push({dimacs,instance:"STRICT-EB4-v1:sha256:"+sha(s),N:s.length*8,expected:prior.cnfSolve(dimacs).decision,native:v,owner:a?assess(a.finalDictionaries,BigInt("0x"+a.target)):null});
 }
 return {cases,controls,scope:"serial source/peer/last-step ablation, named events not aggregate bit clock, no new five-way or feedback experiment, chart normalization and replay reused, exact owner coordinate projection/reconstruction checked",parent:"CERT-v1:sha256:800c5f2d6babf1adfc41cb2cced70a7c7451b7cc1414521dd8ef712d999462c1"};
}
module.exports={run};
