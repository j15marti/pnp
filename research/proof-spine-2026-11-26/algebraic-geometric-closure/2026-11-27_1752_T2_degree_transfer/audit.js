
function run(compiler,corpus,registry,prior,baseJ,baseR,peerJ,peerR){
 const compile=Function(compiler.slice(compiler.indexOf("function compile"),compiler.indexOf("function auditLocal"))+";return compile")();
 const cut=prior.lastIndexOf("const fs=require('node:fs');");
 const {sha,project,experiment}=Function(prior.slice(0,cut)+";return {sha,project,experiment}")();
 const enc=x=>JSON.stringify(x)+"\n",hash=x=>sha(enc(x));
 const X=JSON.parse(corpus),Reg=JSON.parse(registry);
 if(sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")throw Error("SHA");
 // Sparse squarefree polynomials in the Boolean ring F2.
 const one=new Set([0n]),zero=new Set(),varp=i=>new Set([1n<<BigInt(i-1)]);
 const xor=(...a)=>{const z=new Set();for(const s of a)for(const m of s){if(z.has(m))z.delete(m);else z.add(m)}return z};
 const mul=(a,b)=>{const z=new Set();for(const x of a)for(const y of b){const k=x|y;if(z.has(k))z.delete(k);else z.add(k)}return z};
 const inv=a=>xor(one,a),eq=(a,b)=>a.size===b.size&&[...a].every(x=>b.has(x));
 const pop=x=>{let n=0;while(x){x&=x-1n;n++}return n};
 const degree=a=>Math.max(0,...[...a].map(pop));
 const lit=l=>l>0?varp(l):inv(varp(-l));
 const cf=c=>c.reduce((z,l)=>mul(z,inv(lit(l))),one);
 const defect=a=>{let z=one;for(let i=0;i<4;i++)for(let j=i+1;j<4;j++){z=xor(z,mul(a[i],a[j]));for(let k=j+1;k<4;k++)z=xor(z,mul(mul(a[i],a[j]),a[k]))}return z};
 function localPullback(G){
  const net=G.network,F=G.source_map.ternary_clauses,owners=G.source_map.vertex_provenance;
  const groups=new Map([["f",zero]]),port=new Array(4*net.types.length),fail=[],group=(id,p)=>groups.set(id,p);
  for(let i=0;i<F.length;i++){const [a,b,c]=F[i].map(lit),z=mul(inv(a),inv(b));group("z"+i,z);group("w"+i+"_0",xor(a,b,z));group("w"+i+"_1",xor(inv(z),c));for(const l of F[i])group("x"+Math.abs(l),varp(Math.abs(l)))}
  const put=(v,a)=>{for(let j=0;j<4;j++)port[4*v+j]=a[j]};
  for(let v=0;v<owners.length;v++){const o=owners[v];if(o[0]==="clause"){
   const [a,b,c]=F[o[2]].map(lit),z=groups.get("z"+o[2]),t=o[3],p=t?[inv(z),c,zero,groups.get("w"+o[2]+"_1")]:[a,b,z,groups.get("w"+o[2]+"_0")];put(v,p);
   const d=defect(p),expected=t?cf(F[o[2]]):zero;if(!eq(d,expected))throw Error("B failure substitution "+v);fail.push([v,o[2],t,d.size])
  }else if(o[0]==="carrier"){const a=groups.get(o[1]);if(!a)throw Error("group");put(v,[a,a,a,a])}}
  for(let v=0;v<owners.length;v++){const o=owners[v];if(o[0]==="wire"){const b=port[o[2]];if(!b)throw Error("wire endpoint");put(v,[b,b,b,b])}}
  let deg=0,terms=0,booleans=0,ec=0,es=0;for(const a of port){if(!a)throw Error("missing port");deg=Math.max(deg,degree(a));terms+=a.size;if(!eq(mul(a,a),a))throw Error("boolean");booleans++}
  for(let v=0;v<net.types.length;v++)if(net.types[v]==="E")for(let j=1;j<4;j++){if(!eq(port[4*v],port[4*v+j]))throw Error("E");ec++}
  for(const [a,b,s] of net.edges){if(!eq(xor(port[a],port[b]),s?one:zero))throw Error("edge");es++}
  // Independent local truth check on every ternary clause, both B copies by shared construction.
  let wordChecks=0;for(let i=0;i<F.length;i++){let V=[...new Set(F[i].map(Math.abs))];for(let w=0;w<2**V.length;w++){let [a,b,c]=F[i].map(l=>((w>>V.indexOf(Math.abs(l)))&1)^Number(l<0));let z=(1-a)*(1-b),u=(a+b+z)%2,t=(1-z+c)%2;wordChecks++;if(a+b+z+u!==2||(Number(1-z+c+t!==2)!==Number(!(a||b||c))))throw Error("local word")}}
  return{ports:port.length,maxDegree:deg,totalMonomialOccurrences:terms,booleanChecks:booleans,Echecks:ec,edgeChecks:es,Bchecks:fail.length,nonzeroB:fail.filter(a=>a[3]).length,ternaryClauses:F.length,wordChecks,portMapHash:hash(port.map(a=>[...a].map(String).sort())),BmapHash:hash(fail)}
 }
 const key=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b).join(",");
 const canon=c=>key(c).split(",").filter(Boolean).map(Number);
 function res(A,B,p){if(!A.includes(p)||!B.includes(-p)){if(A.includes(-p)&&B.includes(p))p=-p;else throw Error("pivot")}
  const c=canon([...A.filter(l=>l!==p),...B.filter(l=>l!==-p)]);if(c.some(l=>c.includes(-l)))throw Error("tautology");return c}
 function importPeer(orig,bbytes,pbytes,identity,i){
  const expected=[["1fa975b996a099502de9dc341978351ba1794f36ba36f83f285d9ba33fbca9b8","1cc41f02399a48de33a082052bf49fee0e5948774926d13fb5b1f4aa026a801a"],["eccf41c3f945d5a82013c4afc0cb2bffb5d9af1ff2b83596a876395b02aba077","e0c84e02a3ea25cd5129112b3326720f02162467b0bba2bc18cdf0ee9e675965"]][i];
  if(sha(bbytes)!==expected[0]||sha(pbytes)!==expected[1])throw Error("certificate identity");
  const b=JSON.parse(bbytes),p=JSON.parse(pbytes);
  for(const q of [b,p])if(q.instance_id!==identity.instance_id||q.original_N_bits!==identity.N_bits||q.guard_id!=="EMPTY"||q.residual_id!=="ROOT")throw Error("wrong source");
  const learned=[];let truthChecks=0;
  function verify(A,B,C,p){if(key(res(A,B,p))!==key(C))throw Error("resolution");const V=[...new Set([...A,...B,...C].map(Math.abs))];if(V.length>10)throw Error("cap");for(let w=0;w<2**V.length;w++){truthChecks++;let sat=c=>c.some(l=>Number(l>0)===((w>>V.indexOf(Math.abs(l)))&1));if(sat(A)&&sat(B)&&!sat(C))throw Error("semantic")}}
  for(const q of b.proof.learned){let [a,c]=q.parents.map(i=>orig[i-1]);verify(a,c,q.c,q.pivot);learned.push(q.c)}
  const binary=[];for(const q of p.proof.learned){verify(learned[q.import-1],orig[q.original-1],q.c,q.pivot);binary.push(q.c)}
  return{learned,binary,truthChecks,ids:expected.map(x=>"CERT-v1:sha256:"+x)}
 }
 // All-literal probing with batched implication admission, no branching search.
 // Soundness independently checked with reverse-clause RUP for each admission.
 function probe(F,n,extra=[],limit=20000000){
  let C=[...F,...extra],seen=new Set(C.map(key)),trace=[],work=0,rounds=[],done=false;
  function UP(C,pins,reverse=false,counter=null){let a=new Int8Array(n+1).fill(-1),trail=[];for(const l of pins){let v=Math.abs(l),b=+(l>0);if(a[v]!==-1&&a[v]!==b)return{no:true,trail};a[v]=b}let change=true;
   while(change){change=false;for(let k=0;k<C.length;k++){let c=C[reverse?C.length-1-k:k],s=false,u=0,last=0;for(const l of c){if(counter)counter.n++;else if(++work>limit)throw Error("cap");let b=a[Math.abs(l)];if(b===+(l>0)){s=true;break}if(b===-1){u++;last=l}}if(s)continue;if(u===0)return{no:true,trail};if(u===1){a[Math.abs(last)]=+(last>0);trail.push(last);change=true}}}return{no:false,trail}}
  try{for(let t=0;t<=2*n*n+2*n;t++){let a=UP(C,[]);if(a.no){done=true;break}let next=new Map(),probes=0;for(let v=1;v<=n;v++)for(const sign of [1,-1]){let l=sign*v;probes++;let z=UP(C,[l]);let add=c=>{let k=key(c);if(!seen.has(k)&&!next.has(k))next.set(k,canon(c))};if(z.no)add([-l]);else for(const m of z.trail)if(Math.abs(m)!==v)add([-l,m])}
   rounds.push({probes,admitted:next.size,units:[...next.values()].filter(c=>c.length===1).length});if(!next.size)break;
   for(const [k,c] of next){trace.push(c);seen.add(k);C.push(c)} }
  }catch(e){if(String(e)!=="Error: cap")throw e}
  const W={n:0},V=[...F,...extra];for(const c of trace){if(!UP(V,c.map(l=>-l),true,W).no)throw Error("bad RUP");V.push(c)}
  if(done&&!UP(V,[],true,W).no)throw Error("bad root");
  return{no:done,work,replayWork:W.n,rounds,trace,stalled:!done}
 }
 const out=[];
 for(const [i,name] of ["JOINT-24","RANDOM-3CNF-40"].entries()){
  const x=X.instances.find(x=>x.id===name),e=Reg.instances.find(x=>x.alias==="EB-"+name),G=compile(x),s=enc(G.network),map=enc(G.source_map);
  if(sha(s)!==e.sha256||s.length*8!==e.N_bits||sha(x.dimacs)!==e.source_cnf.sha256||x.dimacs.length*8!==e.source_cnf.N_bits||sha(map)!==e.source_map_sha256)throw Error("identity");
  const pp=project(G.network),V=[...new Set(pp.clauses.flat().map(Math.abs))].sort((a,b)=>a-b),M=new Map(V.map((v,i)=>[v,i+1])),F=pp.clauses.map(c=>c.map(l=>Math.sign(l)*M.get(Math.abs(l))));
  const orig=x.dimacs.trimEnd().split("\n").slice(1).map(l=>l.split(/\s+/).map(Number).slice(0,-1));let a=G.source_map.representative_ports.f,ar=pp.root[a[0]],f=pp.phase[a[0]]^a[1],mapping=[];
  for(let j=1;j<=x.nvars;j++){let [q,z]=G.source_map.representative_ports["x"+j];mapping.push([j,M.get(pp.root[q]+1),pp.phase[q]^z^f])}
  let inverse=new Map(mapping.map(([i,j,b])=>[j,[i,b]]));let C=F.map(c=>c.map(l=>{let [i,b]=inverse.get(Math.abs(l));return i*Math.sign(l)*(b?-1:1)})),K=new Set(orig.map(key)),J=new Set(C.map(key));if(ar!==pp.anchor||K.size!==J.size||[...K].some(k=>!J.has(k))||inverse.size!==V.length)throw Error("adapter");
  const baseline=experiment(F,V.length);
  const native=probe(F,V.length),cnf=probe(orig,x.nvars);
  const imp=importPeer(orig,i?baseR:baseJ,i?peerR:peerJ,e.source_cnf,i),mp=new Map(mapping.map(([i,j,b])=>[i,[j,b]]));
  const extra=[...imp.learned,...imp.binary],nativeExtra=extra.map(c=>c.map(l=>{const [j,b]=mp.get(Math.abs(l));return Math.sign(l)*j*(b?-1:1)}));
  const cooperative=probe(F,V.length,nativeExtra),cnfCoop=probe(orig,x.nvars,extra);
  const pullback=localPullback(G);
  out.push({name,instance:e.short_id,instance_id:e.instance_id,N:e.N_bits,cnf:e.source_cnf,source_pin:"registry 0c14cdc57925788cf7a451dcd5aa171dce860f2c; compiler 21b9d53fb8166c819b24e708656c742cd3c24f10; corpus e315349cd6c1fe3fa696504859f28312f6aab69a",guard_id:"EMPTY",residual_id:"ROOT",original_ids:{vertices:[0,G.network.types.length-1],ports:[0,4*G.network.types.length-1],edges:[0,G.network.edges.length-1]},projection:{carriers:pp.carriers,variables:V.length,anchor:pp.anchor,rootPorts:V.map(v=>v-1),cost:pp.cost,steps:pp.steps.length,mapHash:hash({root:pp.root,phase:pp.phase,steps:pp.steps,cond:pp.cond}),chartHash:hash(F),mapping},baseline,native,cnf,peer:{ids:imp.ids,ternary:imp.learned.length,binary:imp.binary.length,truthChecks:imp.truthChecks},cooperative,cnfCoop,pullback})
 }
 return out
}
if(typeof module!=="undefined"){module.exports=run;if(require.main===module){const fs=require("fs");console.log(JSON.stringify(run(...process.argv.slice(2).map(p=>fs.readFileSync(p,"utf8"))),null,2))}}
