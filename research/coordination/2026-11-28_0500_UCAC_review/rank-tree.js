function run(compiler,corpus,registry,syndrome,replayCode,parent){
 const compile=Function(compiler.slice(compiler.indexOf("function compile("),compiler.indexOf("function auditLocal"))+";return compile;")();
 const prior=Function("const module={exports:{}};"+syndrome+";return module.exports;")();
 const chart=Function(syndrome.slice(0,syndrome.indexOf("module.exports")).replace("const m=forms.length,par=","return {H,edges,m:forms.length,counts,forced,parityRank,carriers:roots.size}; const m=forms.length,par=")+";return analyze;")();
 const replay=Function("const module={exports:{}};"+replayCode+";return module.exports.replay;")();
 const sha=prior.sha;
 if(sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"||sha(parent)!=="800c5f2d6babf1adfc41cb2cced70a7c7451b7cc1414521dd8ef712d999462c1")throw Error("hash");
 const reg=JSON.parse(registry),cor=JSON.parse(corpus),p=JSON.parse(parent);
 function assess(D,target){
  const blocks=D.map(x=>({id:x.id,S:x.S.map(y=>BigInt("0x"+y))}));let b=target;
  const n=blocks.length;for(let C of blocks){let a=C.S[0];b^=a;C.S=C.S.map(x=>x^a)}
  let count={rank:0,xor:0,pairs:0,rem:0,spectral:0,cut:0},cap=16000000;
  function tick(k){count[k]++;if(count.rank+count.xor+count.pairs+count.rem+count.spectral+count.cut>cap)throw Error("shared chart event cap")}
  function add(B,x){while(x){tick("rank");let k=x&-x;if(!B.has(k)){B.set(k,x);return}x^=B.get(k);tick("xor")}}
  function merge(...bs){let B=new Map();for(let A of bs)for(let x of A.values())add(B,x);return B}
  function rem(B,x){for(let [k,y] of B){tick("rem");if(x&k)x^=y}return x}
  function canon(B){return new Map([...B].sort((a,b)=>a[0]<b[0]?-1:1))}
  const local=blocks.map(C=>{let B=new Map();for(let x of C.S)add(B,x);return B}), all=merge(...local),r=all.size;
  const seq=Array.from({length:n},(_,i)=>i);
  if(rem(canon(all),b)!==0n)return {rank:r,decision:"NO-affine",count};
  // spectral proxy uses exact incidence of local span generators; proposal only.
  const by=new Map();for(let i=0;i<n;i++)for(let x of local[i].values())while(x){let k=x&-x;x^=k;if(!by.has(k))by.set(k,new Set());by.get(k).add(i);tick("spectral")}
  const adj=Array.from({length:n},()=>new Map());for(let A of by.values()){let a=[...A];for(let i=0;i<a.length;i++)for(let j=i+1;j<a.length;j++){let u=a[i],v=a[j];adj[u].set(v,(adj[u].get(v)||0)+1);adj[v].set(u,(adj[v].get(u)||0)+1);tick("spectral")}}
  const deg=adj.map(x=>[...x.values()].reduce((a,b)=>a+b,0)),md=Math.max(1,...deg);
  let v=seq.map(i=>Math.round(1000000*(2*i-n+1)/Math.max(1,n-1)));
  for(let k=0;k<16;k++){v=v.map((x,i)=>{let z=(2*md-deg[i])*x;for(let [j,w] of adj[i]){z+=w*v[j];tick("spectral")}if(!Number.isSafeInteger(z))throw Error("precision");return Math.trunc(z/(2*md))})}
  let spec=seq.slice().sort((i,j)=>v[i]-v[j]||i-j);
  function attempt(name,order,adaptive){
   let pre={...count},tree=[],maxw=0,sumw=0,peak=0,states=0,decision="UNKNOWN",why="",root;
   const span=a=>merge(...a.map(i=>local[i]));
   function make(a,out,inside){
    let width=inside.size+out.size-r;maxw=Math.max(maxw,width);sumw+=width;
    let id=tree.length,node={id,width,ids:a.map(i=>blocks[i].id),out:canon(out)};tree.push(node);
    if(a.length===1){node.leaf=a[0];return node}
    let candidates=adaptive?[Math.floor(a.length/3),Math.floor(a.length/2),Math.floor(2*a.length/3)]:[Math.floor(a.length/2)];
    let best=null;for(let k of [...new Set(candidates)].filter(k=>k>0&&k<a.length)){tick("cut");let L=a.slice(0,k),R=a.slice(k),l=span(L),rr=span(R),lo=merge(out,rr),ro=merge(out,l),wl=l.size+lo.size-r,wr=rr.size+ro.size-r,score=[Math.max(wl,wr),wl+wr,Math.abs(L.length-R.length),k];if(!best||score.some((x,i)=>x<best.score[i]&&score.slice(0,i).every((z,j)=>z===best.score[j])))best={L,R,l,rr,lo,ro,score}}
    node.left=make(best.L,best.lo,best.l);node.right=make(best.R,best.ro,best.rr);return node
   }
   function solve(t){const T=new Map(), addrow=(x,p)=>{if(!T.has(x)){T.set(x,p);states++;peak=Math.max(peak,T.size);if(T.size>512)throw Error("state cap")}};
    if(t.leaf!==undefined){for(let x of blocks[t.leaf].S){tick("pairs");if(rem(t.out,b^x)===0n)addrow(x,x)}}
    else{let L=solve(t.left),R=solve(t.right),buckets=new Map();for(let y of R.keys()){let k=rem(t.out,y);if(!buckets.has(k))buckets.set(k,[]);buckets.get(k).push(y)}for(let x of L.keys()){let k=rem(t.out,b^x);for(let y of buckets.get(k)||[]){tick("pairs");addrow(x^y,[x,y])}}}
    t.table=T;return T
   }
   let witness=null;
   try{root=make(order,new Map(),all);let T=solve(root);decision=T.has(b)?"YES":"NO";if(decision==="YES"){witness=[];function lift(t,x){let p=t.table.get(x);if(t.leaf!==undefined){if(!blocks[t.leaf].S.includes(p)||x!==p)throw Error("leaf lift");witness.push([blocks[t.leaf].id,p.toString(16)])}else{if((p[0]^p[1])!==x)throw Error("join lift");lift(t.left,p[0]);lift(t.right,p[1])}}lift(root,b);if(witness.length!==n)throw Error("lift count")}}
   catch(e){if(!["state cap","shared chart event cap"].includes(e.message))throw e;why=e.message}
   return {name,decision,why,maxw,sumw,treeNodes:tree.length,peak,states,witness,tree:tree.map(t=>({id:t.id,width:t.width,left:t.left?.id,right:t.right?.id,leaf:t.leaf===undefined?null:blocks[t.leaf].id})),cost:Object.fromEntries(Object.keys(count).map(k=>[k,count[k]-pre[k]]))}
  }
  const arms=[];for(let [name,o,a] of [["source",seq,false],["spectral",spec,false],["rank-source",seq,true],["rank-spectral",spec,true]]){if(Object.values(count).reduce((a,b)=>a+b,0)>cap)break;arms.push(attempt(name,o,a))}
  return {rank:r,blocks:n,arms,count,cap,centeredTarget:b.toString(16)}
 }
 const cases=[];
 for(let cert of p.certs){let e=reg.instances.find(x=>x.alias===cert.entry.alias),x=cor.instances.find(x=>x.id===e.source_cnf.alias),g=compile(x),s=JSON.stringify(g.network)+"\n",map=JSON.stringify(g.source_map)+"\n";
 let hashes={native:sha(s),map:sha(map),cnf:sha(x.dimacs),N:s.length*8,cnfN:x.dimacs.length*8};if(hashes.native!==e.sha256||hashes.map!==e.source_map_sha256||hashes.cnf!==e.source_cnf.sha256||hashes.N!==e.N_bits||hashes.cnfN!==e.source_cnf.N_bits)throw Error("authentication");
 let C=chart(g.network);if(!C.H)throw Error("chart");let root=replay(C.H,C.edges,C.m,[],false),contract=replay(C.H,C.edges,C.m,cert.trace,false),abl=replay(C.H,C.edges,C.m,cert.trace.slice(0,-1),false);
 cases.push({entry:e,hashes,closure:C.counts,forced:C.forced,carriers:C.carriers,parent:{steps:cert.trace.length,replay:contract.stats,ablation:abl.stats},root:assess(root.finalDictionaries,BigInt("0x"+root.target)),contracted:assess(contract.finalDictionaries,BigInt("0x"+contract.target)),ablation:assess(abl.finalDictionaries,BigInt("0x"+abl.target)),companion:prior.cnfSolve(x.dimacs)});
 }
 const controls=[];
 for(let clauses of [[[1,2,3],[-1,2,-3]],[[1],[-1]],[[1,-2,3],[-1,2,-3],[2,3]]]){let dimacs="p cnf 3 "+clauses.length+"\n"+clauses.map(x=>x.join(" ")+" 0").join("\n")+"\n",g=compile({nvars:3,dimacs}),s=JSON.stringify(g.network)+"\n",C=chart(g.network),native=prior.analyze(g.network),a=C.H?replay(C.H,C.edges,C.m,[],false):null;controls.push({dimacs,sha:sha(s),N:s.length*8,native,expected:prior.cnfSolve(dimacs),tree:a?assess(a.finalDictionaries,BigInt("0x"+a.target)):null})}
 return {cases,controls,scope:"serial; same constructor and parent alternate replay, independent tree implementation; chart-local event cap not aggregate bit clock; tree lift to centered dictionary only, native SAT separately checked; no full LOO or native terminal claim from inherited parent"};
}
module.exports={run};
