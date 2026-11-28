function run(compiler,corpus,registry,syndrome){
 const compile=Function(compiler.slice(compiler.indexOf("function compile("),compiler.indexOf("function auditLocal"))+";return compile;")();
 const prior=Function("const module={exports:{}};"+syndrome+";return module.exports;")();
 const chart=Function(syndrome.slice(0,syndrome.indexOf("module.exports")).replace("const m=forms.length,par=","return {H,edges,m:forms.length,counts,forced,parityRank,carriers:roots.size,port:port.map(String),forms:forms.map(String),basis:[...basis].map(([a,b])=>[String(a),String(b)])}; const m=forms.length,par=")+";return analyze;")();
 const sha=prior.sha,reg=JSON.parse(registry),cor=JSON.parse(corpus);
 if(sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")throw Error("hash");
 function test(C){
  const count={localWords:0,localChecks:0,rankTests:0,rankXor:0,proposals:0,products:0,verifyWords:0,verifyChecks:0,diffusion:0,scopeScans:0};
  const h=C.H.length, m=C.m, cols=Array(m).fill(0n),target=C.H.reduce((a,x,j)=>a|((x&1n)<<BigInt(j)),0n);
  for(let j=0;j<h;j++)for(let i=0;i<m;i++)if(C.H[j]&(1n<<BigInt(i+1)))cols[i]|=1n<<BigInt(j);
  let adj=Array.from({length:m},()=>[]);for(let [a,b] of C.edges){adj[a].push(b);adj[b].push(a)}
  let seen=new Set(),B=[];
  for(let i=0;i<m;i++){if(seen.has(i))continue;let V=[i];seen.add(i);for(let j=0;j<V.length;j++)for(let a of adj[V[j]])if(!seen.has(a)){seen.add(a);V.push(a)}V.sort((a,b)=>a-b);if(V.length>12)return {status:"UNKNOWN",reason:"local block cap",count};
   let S=new Map();for(let q=0;q<2**V.length;q++){count.localWords++;let A=new Set(V.filter((_,j)=>q>>j&1));let valid=true;for(let v of A)for(let w of adj[v]){count.localChecks++;if(A.has(w))valid=false}if(!valid)continue;let t=0n;for(let v of A)t^=cols[v];if(!S.has(t))S.set(t,q)}
   B.push({id:B.length,V,S:[...S.keys()],w:[...S.values()]});
  }
  function add(D,x){while(x){count.rankTests++;let k=x&-x;if(!D.has(k)){D.set(k,x);return}x^=D.get(k);count.rankXor++}}
  function rank(arr){let D=new Map();for(let a of arr)for(let x of a)add(D,x);return D.size}
  function span(b){return b.S.map(x=>x^b.S[0])}
  const U=B.map(span),allRank=rank(U),n=B.length;
  let rowOwners=Array.from({length:h},()=>[]);
  for(let b of B){let support=b.S.reduce((a,x)=>a|x,0n);for(let j=0;j<h;j++){count.scopeScans++;if(support&(1n<<BigInt(j)))rowOwners[j].push(b.id)}}
  let W=Array.from({length:n},()=>new Map());
  for(let owners of rowOwners)for(let a of owners)for(let b of owners)if(a!==b)W[a].set(b,(W[a].get(b)||0)+1);
  let deg=W.map(x=>[...x.values()].reduce((a,b)=>a+b,0)),maxD=Math.max(1,...deg),v=B.map((_,i)=>Math.trunc(1000000*(2*i-n+1)/Math.max(1,n-1)));
  for(let t=0;t<24;t++){v=v.map((x,i)=>{let s=(2*maxD-deg[i])*x;for(let [j,w] of W[i]){s+=w*v[j];count.diffusion++}if(!Number.isSafeInteger(s))throw Error("precision");return Math.trunc(s/(2*maxD))})}
  let spectral=B.map(x=>x.id).sort((a,b)=>v[a]-v[b]||a-b),pos=new Map(spectral.map((x,i)=>[x,i]));
  // The local zero witnesses are valid for all independent-set blocks. A target row with b_j=1 is an actual mismatch.
  const candidates=new Map();
  for(let j=0;j<h;j++){let a=rowOwners[j];if(a.length<2||a.length>5)continue;let k=a.join(",");if(!candidates.has(k))candidates.set(k,{ids:a,rows:[],conflicts:0});let z=candidates.get(k);z.rows.push(j);if(target&(1n<<BigInt(j)))z.conflicts++}
  let cand=[...candidates.values()];
  const costLimit=1500000; // global candidate products + rank tests, no reset per arm; rank loop checks cap between candidates.
  const arms=[];
  function attempt(name,maxArity,order){
   let best=null,records=[],skipped=0;
   for(let c of order){if(c.ids.length>maxArity||!c.conflicts)continue;if(count.rankTests+count.products>=costLimit)break;
    let G=c.ids.map(i=>B[i]),outside=B.filter(b=>!c.ids.includes(b.id)),prod=G.reduce((a,b)=>a*b.S.length,1);
    if(prod>4096){skipped++;continue}count.proposals++;
    let privateRows=0n;for(let j=0;j<h;j++){count.scopeScans++;if(rowOwners[j].length&&rowOwners[j].every(i=>c.ids.includes(i)))privateRows|=1n<<BigInt(j)}
    let full=new Set(),kept=new Map();
    const OB=new Map();let ob=0n;for(const b of outside){ob^=b.S[0];for(let s of span(b))add(OB,s)}
    function remainder(x){while(x){count.rankTests++;let k=x&-x;if(!OB.has(k))return false;x^=OB.get(k);count.rankXor++}return true}
    const AB=new Map();function top(x){return 1n<<BigInt(x.toString(2).length-1)}
    function altAdd(x){while(x){count.verifyChecks++;let k=top(x);if(!AB.has(k)){AB.set(k,x);return}x^=AB.get(k)}}
    for(const b of outside)for(let s of span(b))altAdd(s);
    function altMember(x){while(x){count.verifyChecks++;let k=top(x);if(!AB.has(k))return false;x^=AB.get(k)}return true}
    if(OB.size!==AB.size)throw Error("outside rank mismatch");
    function rec(i,s,w){if(i===G.length){count.products++;full.add(s);if(remainder(s^target^ob)&&!kept.has(s))kept.set(s,w);return}for(let j=0;j<G[i].S.length;j++)rec(i+1,s^G[i].S[j],[...w,j])}
    rec(0,0n,[]);
    if(!kept.size){records.push({ids:c.ids,empty:true,privateRows:privateRows.toString(),product:prod});return {name,records,skipped,terminal:"NO-outside-affine-quotient"}}
    if(kept.size===full.size)continue;
    // Independent replay uses mixed-radix enumeration rather than recursive enumeration.
    const check=new Set();
    for(let z=0;z<prod;z++){count.verifyWords++;let k=z,s=0n;for(let b of G){s^=b.S[k%b.S.length];k=Math.floor(k/b.S.length);count.verifyChecks++}let valid=true;for(let j=0;j<h;j++)if(privateRows&(1n<<BigInt(j))){count.verifyChecks++;if(((s^target)>>BigInt(j))&1n)valid=false}if(altMember(s^target^ob))check.add(s)}
    if(check.size!==kept.size||[...check].some(s=>!kept.has(s)))throw Error("support replay");
    let outU=outside.map(span),oldU=G.map(span),newU=[[...kept.keys()].map(s=>s^[...kept.keys()][0])];
    let ro=rank(outU),rg=rank(oldU),rn=rank(newU),ra=rank([...outU,...newU]);
    let oldCut=ro+rg-allRank,newCut=ro+rn-ra;if(newCut>oldCut)throw Error("cut increased");
    let recd={ids:c.ids,localVariables:G.map(b=>b.V),rows:c.rows,privateRows:privateRows.toString(),product:prod,raw:full.size,kept:kept.size,oldCut,newCut,oldRank:rg,newRank:rn,globalRankBefore:allRank,globalRankAfter:ra,optionsBefore:G.reduce((a,b)=>a+b.S.length,0),optionsAfter:kept.size,keptS:[...kept.keys()].map(String),backpointers:[...kept.values()],parentS:G.map(b=>b.S.map(String)),parentChoices:G.map(b=>b.w)};
    records.push(recd);if(!best||oldCut-newCut>best.oldCut-best.newCut||(oldCut-newCut===best.oldCut-best.newCut&&full.size-kept.size>best.raw-best.kept))best=recd;
    if(records.length>=6)break;
   }
   return {name,records,skipped,best:best?{ids:best.ids,raw:best.raw,kept:best.kept,oldCut:best.oldCut,newCut:best.newCut,oldRank:best.oldRank,newRank:best.newRank,optionsBefore:best.optionsBefore,optionsAfter:best.optionsAfter}:null,terminal:"UNKNOWN"};
  }
  const source=cand.slice().sort((a,b)=>a.ids.length-b.ids.length||a.rows[0]-b.rows[0]);
  const sp=cand.slice().sort((a,b)=>{let spread=c=>Math.max(...c.ids.map(i=>pos.get(i)))-Math.min(...c.ids.map(i=>pos.get(i)));return spread(a)-spread(b)||a.rows[0]-b.rows[0]});
  const hy=cand.slice().sort((a,b)=>b.conflicts-a.conflicts||b.rows.length-a.rows.length||a.ids.length-b.ids.length||a.rows[0]-b.rows[0]);
  arms.push(attempt("pair baseline",2,source),attempt("higher-order source",5,source.filter(x=>x.ids.length>=3)),attempt("spectral higher-order",5,sp.filter(x=>x.ids.length>=3)),attempt("conflict-ranked hybrid",5,hy));
  return {status:"UNKNOWN",blocks:n,rank:allRank,syndromeRows:h,target:target.toString(),options:B.reduce((a,b)=>a+b.S.length,0),candidateCounts:[2,3,4,5].map(k=>[k,cand.filter(x=>x.ids.length===k&&x.conflicts).length]),arms,count,cap:costLimit,scope:"outside affine hull filter, same root candidates; bounded acquisition; no final global solve"};
 }
 let cases=[];
 for(let name of ["JOINT-24","RANDOM-3CNF-40"]){
   let e=reg.instances.find(x=>x.source_cnf.alias===name),x=cor.instances.find(x=>x.id===name),g=compile(x),bytes=JSON.stringify(g.network)+"\n",map=JSON.stringify(g.source_map)+"\n";
   let hashes={native:sha(bytes),map:sha(map),cnf:sha(x.dimacs),N:bytes.length*8,cnfN:x.dimacs.length*8};
   if(hashes.native!==e.sha256||hashes.map!==e.source_map_sha256||hashes.cnf!==e.source_cnf.sha256||hashes.N!==e.N_bits||hashes.cnfN!==e.source_cnf.N_bits)throw Error("auth "+name);
   let C=chart(g.network);if(!C.H)throw Error("chart");
   let artifact=JSON.stringify({H:C.H.map(String),edges:C.edges,m:C.m})+"\n",mapping=JSON.stringify({port:C.port,forms:C.forms,basis:C.basis})+"\n";
   let residual="RESIDUAL-v1:sha256:"+sha(JSON.stringify(["PNP-RESIDUAL-v1",e.instance_id,"EMPTY","SYNDROME-INDEPENDENT-SET-v1",sha(artifact),sha(mapping)])+"\n");
   let record={entry:e,hashes,chart:{sha:sha(artifact),mapSha:sha(mapping),residual,counts:C.counts,forced:C.forced,parityRank:C.parityRank,carriers:C.carriers},result:test(C),companion:prior.cnfSolve(x.dimacs)};
   cases.push(record);
 }
 let controls=[];
 for(let cl of [[[1,2,3],[-1,2,-3]],[[1,-2,3],[-1,2,-3],[2,3]],[[1],[-1]]]){
  let dimacs="p cnf 3 "+cl.length+"\n"+cl.map(x=>x.join(" ")+" 0").join("\n")+"\n",g=compile({nvars:3,dimacs}),bytes=JSON.stringify(g.network)+"\n",C=chart(g.network),native=prior.analyze(g.network);
  controls.push({dimacs,instance_id:"STRICT-EB4-v1:sha256:"+sha(bytes),N:bytes.length*8,native,result:C.H?test(C):{status:"early terminal",C}});
 }
 return {cases,controls,model:"source-only chart; no peer proof or provenance advice",execution:"serial bounded outside-hull diagnostic, not five independent complete lanes; rank and product counters only; no physical memory/time accounting",note:"The rank-test cap is checked between proposals; a proposal may overshoot. No universal clock claim."};
}
module.exports={run};
