const fs=require('fs');
function controls(inputs){
 const [co,base]=inputs,A=(x,m)=>{if(!x)throw Error(m)};
 const compile=new Function(co.slice(co.indexOf("function compile("),co.indexOf("function auditLocal"))+";return compile;")();
 const {sha,normalize,independentNormalize,eliminate,verifyTrace,gauge}=new Function(base.slice(0,base.indexOf("function runCase"))+";return {sha,normalize,independentNormalize,eliminate,verifyTrace,gauge};")();
 function pin(F,v){return F.map(f=>{let i=f.vs.indexOf(v);if(i<0)return f;return {...f,vs:f.vs.filter(x=>x!==v),ok:f.ok.filter(w=>!(w>>i&1)).map(w=>(w&((1<<i)-1))|((w>>(i+1))<<i))}})}
 let out=[];
 for(let [alias,nvars,dimacs,expected] of [["T2-lift-signed-SAT",3,"p cnf 3 1\n1 -2 3 0\n",true],["T2-lift-unit-UNSAT",1,"p cnf 1 2\n1 0\n-1 0\n",false]]){
  let g=compile({nvars,dimacs}),G=g.network,native=JSON.stringify(G)+"\n",N=normalize(G),I=independentNormalize(G);A(JSON.stringify(N.fs)===JSON.stringify(I.fs),"quotient");let v=gauge(N.fs),F=pin(N.fs,v),E=eliminate(F,false),B=verifyTrace(pin(I.fs,v),E.trace);let vars=[...new Set(B.fs.flatMap(f=>f.vs))];A(vars.length<20,"control too large");
  let a=null;const fits=(f,M)=>f.ok.includes(f.vs.reduce((s,v,i)=>s|((M.get(v)||0)<<i),0));
  for(let w=0;w<2**vars.length;w++){let M=new Map(vars.map((v,i)=>[v,w>>i&1]));if(B.fs.every(f=>fits(f,M))){a=M;break}}
  A(Boolean(a)===expected,"control label");let physical=null;
  if(a){let hist=new Map(F.map(f=>[f.id,f]));for(let t of E.trace)hist.set(t.out,{id:t.out,vs:t.vs,ok:t.ok});a.set(v,0);
   for(let t of [...E.trace].reverse()){for(let u of t.vs)if(!a.has(u))a.set(u,0);let ok=false;for(let bit=0;bit<2;bit++){a.set(t.v,bit);if(t.in.every(i=>fits(hist.get(i),a))){ok=true;break}}A(ok,"reverse projection")}
   A(N.fs.every(f=>fits(f,a)),"root factors");let m=4*G.types.length,adj=Array.from({length:m},()=>[]);const link=(x,y,s)=>{adj[x].push([y,s]);adj[y].push([x,s])};for(let [x,y,s]of G.edges)link(x,y,s);for(let i=0;i<G.types.length;i++)if(G.types[i]==="E")for(let j=1;j<4;j++)link(4*i,4*i+j,0);
   let bits=Array(m).fill(-1);for(let i=0;i<m;i++)if(bits[i]<0){bits[i]=a.get(i+1)||0;let q=[i];for(let j=0;j<q.length;j++)for(let [y,s]of adj[q[j]]){let b=bits[q[j]]^s;if(bits[y]<0){bits[y]=b;q.push(y)}else A(bits[y]===b,"edge parity")}}
   for(let [x,y,s] of G.edges)A((bits[x]^bits[y])===s,"physical edge");for(let i=0;i<G.types.length;i++){let z=bits.slice(4*i,4*i+4);A(G.types[i]==="E"?z.every(b=>b===z[0]):z.reduce((a,b)=>a+b,0)===2,"physical vertex")}
   let reps=g.source_map.representative_ports, f=reps.f,anchor=bits[f[0]]^f[1],word=Array.from({length:nvars},(_,i)=>{let [p,s]=reps["x"+(i+1)];return bits[p]^s^anchor});let clauses=dimacs.trimEnd().split("\n").slice(1).map(s=>s.split(/\s+/).map(Number).slice(0,-1));A(clauses.every(c=>c.some(l=>word[Math.abs(l)-1]===+(l>0))),"CNF projection");physical={word,vertices:G.types.length,edges:G.edges.length,portBits:bits.join("")}
  }
  out.push({alias,problem_id:"STRICT-EB4-v1",instance_id:"STRICT-EB4-v1:sha256:"+sha(native),original_N_bits:native.length*8,cnf_id:"DIMACS-CNF-v1:sha256:"+sha(dimacs),cnf_N_bits:dimacs.length*8,source_map_sha256:sha(JSON.stringify(g.source_map)+"\n"),dimacs,source_pin:"21b9d53fb8166c819b24e708656c742cd3c24f10",guard_id:"EMPTY",residual_id:"ROOT",original_ids:{vertices:[0,G.types.length-1],ports:[0,4*G.types.length-1],edges:[0,G.edges.length-1]},projectionCount:E.trace.length,finalVars:vars.length,expected,status:a?"SAT":"UNSAT",physical,parents:[]})
 }
 return out
}
console.log(JSON.stringify(controls(process.argv.slice(2).map(p=>fs.readFileSync(p,'utf8'))),null,2));
