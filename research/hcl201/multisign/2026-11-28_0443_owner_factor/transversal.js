function run(compiler,corpus,registry,syndrome,replayCode,parent){
 const compile=Function(compiler.slice(compiler.indexOf("function compile("),compiler.indexOf("function auditLocal"))+";return compile;")();
 const prior=Function("const module={exports:{}};"+syndrome+";return module.exports;")();
 const chart=Function(syndrome.slice(0,syndrome.indexOf("module.exports")).replace("const m=forms.length,par=","return {H,edges,m:forms.length,counts,forced,parityRank,carriers:roots.size}; const m=forms.length,par=")+";return analyze;")();
 const replay=Function("const module={exports:{}};"+replayCode+";return module.exports.replay;")();
 const sha=prior.sha,reg=JSON.parse(registry),cor=JSON.parse(corpus),p=JSON.parse(parent);
 if(sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"||sha(parent)!=="800c5f2d6babf1adfc41cb2cced70a7c7451b7cc1414521dd8ef712d999462c1")throw Error("hash");
 const hx=x=>x.toString(16);
 function match(D,t,cap=20000000){
  let c={rank:0,xor:0,option:0,edges:0,aug:0,check:0,peakQueue:0};let b=t;
  let F=D.map((x,i)=>{let S=x.S.map(y=>BigInt("0x"+y)),a=S[0];b^=a;return {id:x.id,i,a,S:S.map(y=>y^a)}});
  let E=[],by=F.map(f=>{let a=[];for(let v of f.S)if(v){a.push(E.length);E.push({i:f.i,v})}return a});
  function budget(){if(c.rank+c.xor+c.option+c.edges+c.check>=cap)throw Error("cap")}
  // First-pivot discovery; tags encode selected option positions.
  function tag(I){let G=new Map();for(let j=0;j<I.length;j++){let x=E[I[j]].v,y=1n<<BigInt(j);while(x){budget();c.rank++;let k=x&-x;if(!G.has(k)){G.set(k,[x,y]);break}let [a,b]=G.get(k);x^=a;y^=b;c.xor++}if(!x)throw Error("dependent selection")}return G}
  function reduce(G,x){let y=0n;while(x){budget();c.rank++;let k=x&-x;if(!G.has(k))return {outside:true};let [a,b]=G.get(k);x^=a;y^=b;c.xor++}return {outside:false,y}}
  function highBasis(V){let G=new Map();for(let x of V){while(x){budget();c.check++;let k=x.toString(2).length-1;if(!G.has(k)){G.set(k,x);break}x^=G.get(k)}}return G}
  function highMember(G,x){while(x){budget();c.check++;let k=x.toString(2).length-1;if(!G.has(k))return false;x^=G.get(k)}return true}
  let I=[],selected=new Set(),G,reach,trace=[];
  for(;;){
   G=tag(I);selected=new Set(I);let used=new Set(I.map(i=>E[i].i)),queue=[],parent=new Map();
   for(let j=0;j<E.length;j++)if(!used.has(E[j].i)){queue.push(j);parent.set(j,-1)}
   let sink=-1;
   for(let pos=0;pos<queue.length&&sink<0;pos++){
    let j=queue[pos];c.option++;budget();
    if(selected.has(j)){for(let k of by[E[j].i])if(!selected.has(k)&&!parent.has(k)){parent.set(k,j);queue.push(k);c.edges++}}
    else{let a=reduce(G,E[j].v);if(a.outside){sink=j;break}let y=a.y;while(y){let k=y&-y;y^=k;let h=I[k.toString(2).length-1];c.edges++;if(!parent.has(h)){parent.set(h,j);queue.push(h)}}}
   }
   c.peakQueue=Math.max(c.peakQueue,queue.length);
   if(sink<0){reach=parent;break}
   let path=[];for(let k=sink;k!==-1;k=parent.get(k))path.push(k);
   for(let k of path)if(selected.has(k))selected.delete(k);else selected.add(k);
   let next=[...selected].sort((a,b)=>a-b);
   if(next.length!==I.length+1||new Set(next.map(j=>E[j].i)).size!==next.length||highBasis(next.map(j=>E[j].v)).size!==next.length)throw Error("augmentation");
   I=next;c.aug++;trace.push(path);
  }
  // Maximality certificate: reachable original blocks from every unused block.
  // Recompute all closure dependencies (not relying on BFS endpoint coverage).
  let dep=F.map(()=>new Set()),bad=new Set();
  for(let j=0;j<E.length;j++){let a=reduce(G,E[j].v);if(a.outside){bad.add(E[j].i);continue}let y=a.y;while(y){let k=y&-y;y^=k;dep[E[j].i].add(E[I[k.toString(2).length-1]].i);c.edges++}}
  // largest closed subset whose union span is covered by its own selected vectors.
  for(;;){let changed=false;for(let i=0;i<F.length;i++){if(bad.has(i))continue;for(let j of dep[i]){c.edges++;if(bad.has(j)){bad.add(i);changed=true;break}}}if(!changed)break;budget()}
  let good=F.filter(f=>!bad.has(f.i)),goodIds=new Set(good.map(f=>f.i)),J=I.filter(j=>goodIds.has(E[j].i));
  let B=highBasis(J.map(j=>E[j].v));
  if(B.size!==J.length)throw Error("independence");
  for(let f of good)for(let v of f.S)if(!highMember(B,v))throw Error("group closure");
  for(let j of J)if(!F[E[j].i].S.includes(E[j].v)||!F[E[j].i].S.includes(0n))throw Error("choice");
  // Independently verify a Rado min-max obstruction for the entire maximum transversal.
  let R=new Set(F.filter(f=>!I.some(j=>E[j].i===f.i)).map(f=>f.i));
  for(;;){let old=R.size;for(let i of [...R]){if(bad.has(i))throw Error("augmenting reach");for(let j of dep[i])R.add(j)}if(R.size===old)break}
  let rankR=highBasis(F.filter(f=>R.has(f.i)).flatMap(f=>f.S)).size;
  if(rankR+F.length-R.size!==I.length)throw Error("Rado bound");
  const allRank=highBasis(F.flatMap(f=>f.S)).size;
  // Period quotient and exact cut rank at every old cut NOT splitting G.
  let periodRank=B.size,cutChecks=0,cutGain=0,maxGain=0,formulaChecks=0,groupSet=new Set(good.map(f=>f.i));
  function width(U,V){return highBasis(U).size+highBasis(V).size-highBasis([...U,...V]).size}
  function pi(x){let keys=[...B.keys()].sort((a,b)=>b-a);for(let k of keys)if(x&(1n<<BigInt(k))){c.check++;x^=B.get(k)}return x}
  if(periodRank){for(let i=1;i<F.length;i++){
    let l=good.filter(f=>f.i<i).length;if(l&&l<good.length)continue;
    let U=F.slice(0,i).flatMap(f=>f.S),V=F.slice(i).flatMap(f=>f.S),d=width(U,V),z=width(U.map(pi),V.map(pi));
    let opposite=l===good.length?V:U,expected=periodRank+highBasis(opposite).size-highBasis([...J.map(j=>E[j].v),...opposite]).size;
    if(d-z!==expected||z>d)throw Error("cut identity");cutChecks++;formulaChecks++;cutGain+=d-z;maxGain=Math.max(maxGain,d-z);
   }}
  let decision="UNKNOWN",witness=null;if(allRank===periodRank){if(!highMember(B,b))decision="NO";else{
    // Use the independent chosen vectors to reconstruct an actual local tuple.
    let T=new Map();for(let k=0;k<J.length;k++){let x=E[J[k]].v,y=1n<<BigInt(k);while(x){let h=x&-x;if(!T.has(h)){T.set(h,[x,y]);break}let [a,b]=T.get(h);x^=a;y^=b}}
    let x=b,y=0n;while(x){let h=x&-x;let [a,z]=T.get(h);x^=a;y^=z}
    let vals=F.map(f=>f.a);while(y){let h=y&-y;y^=h;let j=J[h.toString(2).length-1];vals[E[j].i]^=E[j].v}
    if(vals.reduce((a,b)=>a^b,0n)!==t||vals.some((v,i)=>!F[i].S.includes(v^F[i].a)))throw Error("witness");
    decision="YES";witness=vals.map(hx);
   }}
  return {blocks:F.length,options:E.length+F.length,rank:allRank,matched:I.length,goodBlocks:good.map(f=>f.id),periodRank,cutChecks,cutGain,maxGain,formulaChecks,decision,witness,selected:I.map(j=>({block:F[E[j].i].id,v:hx(E[j].v)})),rado:{reachable:[...R].map(i=>F[i].id),rank:rankR,upper:rankR+F.length-R.size},count:c,paths:trace};
 }
 let cases=[];
 for(let cert of p.certs){let e=reg.instances.find(x=>x.alias===cert.entry.alias),x=cor.instances.find(x=>x.id===e.source_cnf.alias),g=compile(x),bytes=JSON.stringify(g.network)+"\n",map=JSON.stringify(g.source_map)+"\n";
  if(sha(bytes)!==e.sha256||sha(map)!==e.source_map_sha256||sha(x.dimacs)!==e.source_cnf.sha256||bytes.length*8!==e.N_bits||x.dimacs.length*8!==e.source_cnf.N_bits)throw Error("authentication");
  let C=chart(g.network),R=replay(C.H,C.edges,C.m,[],false),P=replay(C.H,C.edges,C.m,cert.trace,false),L=replay(C.H,C.edges,C.m,cert.trace.slice(0,-1),false);
  cases.push({entry:e,closure:{counts:C.counts,forced:C.forced,rank:C.parityRank,carriers:C.carriers},parent:{steps:cert.trace.length,replay:P.stats,lastRemoved:L.stats},source:match(R.finalDictionaries,BigInt("0x"+R.target)),hybrid:match(P.finalDictionaries,BigInt("0x"+P.target)),ablation:match(L.finalDictionaries,BigInt("0x"+L.target))});
 }
 // Ring family: individual and all pair sumsets odd; full union despite weighted Fourier having no periods.
 let controls=[];for(let n of [3,4,8,16,32,64]){
  let D=Array.from({length:n},(_,i)=>({id:i,S:["0",hx(1n<<BigInt(i)),hx(1n<<BigInt((i+1)%n))]}));
  let a=(1n<<BigInt(n))-1n;
  let yes=match(D,a),no=match(D,a|(1n<<BigInt(n)));
  if(yes.decision!=="YES"||no.decision!=="NO"||yes.periodRank!==n)throw Error("ring decision");
  let pairCounts=new Set();for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){let X=new Set();for(let a of D[i].S)for(let b of D[j].S)X.add(BigInt("0x"+a)^BigInt("0x"+b));if(X.size%2===0)throw Error("pair");pairCounts.add(X.size)}
  controls.push({n,D,yes,no,pairCounts:[...pairCounts]});
 }
 return {cases,controls,scope:"exact independent transversal plus independent Rado upper bound, safe full-subspace group quotient; source/peer/last-step ablation; named operations not aggregate bit clock; serial; native chart root IDs only, not full original witness reconstruction for novel module",parent:"CERT-v1:sha256:800c5f2d6babf1adfc41cb2cced70a7c7451b7cc1414521dd8ef712d999462c1"};
}
module.exports={run};
