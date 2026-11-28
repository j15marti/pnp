function hostile(s){
 let C=Function(s.compiler.slice(s.compiler.indexOf("function compile("),s.compiler.indexOf("function auditLocal("))+";return compile")(),H=Function(s.hybrid.split('if(typeof require==="function"')[0]+";return {sha,norm,closure,affine,solve,unique,lift}")(),assert=(a,b)=>{if(!a)throw Error(b)};
 let fast=Function(s.index.slice(s.index.indexOf("function fast("),s.index.indexOf("function canon("))+";return fast")(); // fast's assertions refer to global? inject
 fast=Function("const assert=(a,b)=>{if(!a)throw Error(b)};"+s.index.slice(s.index.indexOf("function fast("),s.index.indexOf("function canon("))+";return fast")();
 let lines=[];for(let a=1;a<=7;a++)for(let b=a+1;b<=7;b++){let c=a^b;if(c>b)lines.push([a,b,c])}
 assert(lines.length===7,"Fano");
 let controls=[];for(let q of [1,2,4,8,16]){
  let F=[],n=1+6*q;for(let i=0;i<q;i++){for(let l of lines){let c=l.map(v=>v===1?1:6*i+v);F.push(c,c.map(v=>-v))}}
  let dimacs=`p cnf ${n} ${F.length}\n`+F.map(c=>c.join(" ")+" 0\n").join(""),G=C({nvars:n,dimacs}),raw=JSON.stringify(G.network)+"\n",S=H.norm(G.network),P=new Map(),M={n:0,cap:2000000},cl=H.closure(S.factors,P,M),ge=H.affine(S),A=fast(S.factors),Q=[];
  for(let f of A.fs)for(let w=0;w<2**f.vs.length;w++)if(!f.ok.includes(w))Q.push(f.vs.map((v,i)=>w>>i&1?-v:v));Q=H.unique(Q);let solve;try{let z=H.solve(Q,2000000);solve={status:"UNSAT",nodes:z.nodes,reads:z.scans}}catch(e){solve={status:"UNKNOWN",error:String(e)}}
  let remaining= new Set(A.fs.flatMap(f=>f.vs));let occ=new Map();for(let f of A.fs)for(let v of f.vs)occ.set(v,(occ.get(v)||0)+1);
  let eligible=[...occ].filter(([v,c])=>c<=2&&new Set(A.fs.filter(f=>f.vs.includes(v)).flatMap(f=>f.vs)).size<=7).length;

  let hub=[...occ].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0],vlist=[...remaining].filter(v=>v!==hub),parent=new Map(vlist.map(v=>[v,v]));const root=v=>{while(parent.get(v)!==v)v=parent.get(v);return v};
  for(let f of A.fs){let V=f.vs.filter(v=>v!==hub);for(let i=1;i<V.length;i++)parent.set(root(V[i]),root(V[0]))}
  let groups=new Map();for(let v of vlist){let r=root(v);if(!groups.has(r))groups.set(r,[]);groups.get(r).push(v)}
  let buckets=[...groups.values()].map(V=>({V,F:A.fs.filter(f=>f.vs.some(v=>V.includes(v)))})),only=A.fs.filter(f=>f.vs.every(v=>v===hub)),wordTests=0,valid=[];
  for(let b=0;b<2;b++){let counts=[];for(let {V,F} of buckets){assert(V.length<=10,"component cap");let ct=0;for(let w=0;w<2**V.length;w++){wordTests++;let val=v=>v===hub?b:(w>>V.indexOf(v)&1);if(F.every(f=>f.ok.includes(f.vs.reduce((u,v,i)=>u+(val(v)<<i),0))))ct++}counts.push(ct)}valid.push({b,counts,hubOnly:only.every(f=>f.ok.includes(f.vs.length?b:0))})}
  assert(valid.every(x=>!x.hubOnly||x.counts.some(c=>!c)),"hub refutation");
  let separator={hub,componentSizes:buckets.map(x=>x.V.length),wordTests,valid};
  let L=H.lift(F),bits="1".repeat(L.n)+"0",gamma=(L.m+1).toString(2);bits+="0".repeat(gamma.length-1)+gamma;let width=Math.ceil(Math.log2(L.n+1));for(let c of L.R)for(let v of c)bits+=v.toString(2).padStart(width,"0");assert(bits.length===L.N,"T5 bit size");let packed="";for(let i=0;i<bits.length;i+=8)packed+=String.fromCharCode(parseInt(bits.slice(i,i+8).padEnd(8,"0"),2)); // H.sha handles bytes in JS chars.
  controls.push({q,n,dimacs,cnfSha:H.sha(dimacs),cnfN:dimacs.length*8,nativeSha:H.sha(raw),nativeN:raw.length*8,vertices:G.network.types.length,edges:G.network.edges.length,local:{status:cl?"UNKNOWN":"UNSAT",pins:P.size,checks:M.n},affine:ge,grammar:{retired:A.trace.length,remainingFactors:A.fs.length,remainingVariables:remaining.size,eligible,entries:A.entries,counts:A.counts},nativeBranch:solve,separator,t5:{n:L.n,m:L.m,logicalN:L.N,packedBytes:packed.length,packedSha:H.sha(packed)}})
 }
 let yes=0;for(let w=0;w<128;w++)if(lines.every(l=>{let a=l.map(v=>w>>(v-1)&1);return a.some(x=>x===0)&&a.some(x=>x===1)}))yes++;assert(yes===0,"Fano exhaust");
 return {lines,controls,exhaustiveBaseWords:128,satisfying:yes}
}
if(typeof require==='function'){let fs=require('fs'),keys=['compiler','hybrid','index'];console.log(JSON.stringify(hostile(Object.fromEntries(keys.map((k,i)=>[k,fs.readFileSync(process.argv[i+2],'utf8')]))),null,2));}
