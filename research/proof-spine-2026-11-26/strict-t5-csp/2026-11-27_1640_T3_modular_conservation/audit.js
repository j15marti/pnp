function audit(src){
 const H=Function(src.hybrid.split('if(typeof require==="function"')[0]+";return {sha,norm,closure,affine,unique,lift,gadgetAudit}")(),C=Function(src.compiler.slice(src.compiler.indexOf("function compile("),src.compiler.indexOf("function auditLocal("))+";return compile")(),assert=(x,m)=>{if(!x)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const verify=Function(src.checker.slice(0,src.checker.lastIndexOf("\nif(typeof require"))+";return verify")(),s={...src},details=[];
 for(let key of ["joint","random"]){let P=JSON.parse(src[key]),m=JSON.parse(P.map),F=JSON.parse(P.chart).F;let a={...P,privateTrace:m.privateTrace,dpTrace:m.dpTrace,gauge:m.gauge,chart_id:"RESIDUAL-v1:sha256:"+H.sha(P.chart),guards:P.guards.guards,guardVariables:P.guards.v,arms:P.pairedCertificates,guardInfo:[]};
  for(let [i,g] of a.guards.entries()){let q=P.guardInfo[i],b=JSON.stringify({gaugePort:m.gauge-1,relativePortBits:g.map(([v,b])=>[v-1,b]).sort((a,b)=>a[0]-b[0])})+"\n";assert(b===q.bytes&&q.id==="GUARD-v1:sha256:"+H.sha(JSON.stringify(["PNP-GUARD-v1",P.instance_id,q.schema,H.sha(b)])+"\n")&&q.residual_id==="RESIDUAL-v1:sha256:"+H.sha(JSON.stringify(["PNP-RESIDUAL-v1",P.instance_id,q.id,"T3-CNF-chart-v1",H.sha(P.chart),H.sha(P.map)])+"\n"),"canonical IDs");
   let legacy=JSON.stringify({schema:"T3-relative-carrier-v1",gaugePort:m.gauge-1,relativePortBits:g.map(([v,b])=>[v-1,b]).sort((a,b)=>a[0]-b[0])})+"\n";a.guardInfo.push({guardBytes:legacy,guard_id:"GUARD-v1:sha256:"+H.sha(legacy)})
  }
  s[key]=JSON.stringify(a)+"\n";
  let nodes=0,reads=0;
  function up(F,g){let p=new Map(g);for(;;){let change=false;for(let c of F){let u=[],hit=false;for(let l of c){reads++;let v=Math.abs(l);if(!p.has(v))u.push(l);else if(p.get(v)===+(l>0)){hit=true;break}}if(hit)continue;if(!u.length)return {p,conflict:true};if(u.length===1){p.set(Math.abs(u[0]),+(u[0]>0));change=true}}if(!change)return {p,conflict:false}}}
  function walk(F,t,g){nodes++;let q=up(F,g);if(q.conflict){assert(t===0,"leaf");return}assert(Array.isArray(t)&&t.length===3&&!q.p.has(t[0])&&F.some(c=>c.some(l=>Math.abs(l)===t[0])),"branch");walk(F,t[1],[...q.p,[t[0],0]]);walk(F,t[2],[...q.p,[t[0],1]])}
  for(let [i,t] of P.fused.entries()){let q=up(F,a.guards[i]);if(q.conflict){assert(t.via==="UP","early");continue}let D=H.unique(F.filter(c=>!c.some(l=>q.p.get(Math.abs(l))===+(l>0))).map(c=>c.filter(l=>!q.p.has(Math.abs(l)))));assert(eq(D,t.D)&&t.trace.every(z=>z.a.proofs.length===0&&eq(z.D,D)),"no field imports");walk(D,t.tree,[])}
  details.push({key,originalCertSha:H.sha(src[key]),canonicalGuards:5,fusionNodes:nodes,fusionReads:reads})
 }
 let replay=verify(s);
 const lines=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]],cases=[];
 for(let q of [1,2,4,8,16,32]){let rows=[];for(let [i,line] of lines.entries())for(let j=0;j<q;j++)rows.push(line.map((v,k)=>(v-1)*q+(j+(i+1)*k)%q+1));let n=7*q,deg=Array(n).fill(0);for(let r of rows)for(let v of r)deg[v-1]++;assert(deg.every(x=>x===3)&&rows.length%3!==0,"sum");
  let parityChecks=0;for(let g=0;g<8;g++){let val=v=>{let z=g&(Math.floor((v-1)/q)+1),p=0;while(z){p^=1;z&=z-1}return 1^p};for(let r of rows){assert((val(r[0])^val(r[1])^val(r[2]))===1,"parity");parityChecks++}}
  let F=H.unique(rows.flatMap(c=>[c,...c.flatMap((a,i)=>c.slice(i+1).map(b=>[-a,-b]))])),dimacs=`p cnf ${n} ${F.length}\n`+F.map(c=>c.join(" ")+" 0\n").join(""),G=C({nvars:n,dimacs}),raw=JSON.stringify(G.network)+"\n",S=H.norm(G.network),m={n:0,cap:2e6},p=new Map(),cl=H.closure(S.factors,p,m),ge=H.affine(S),L=H.lift(F),bits="1".repeat(L.n)+"0",gamma=(L.m+1).toString(2);bits+="0".repeat(gamma.length-1)+gamma;let width=Math.ceil(Math.log2(L.n+1));for(let c of L.R)for(let v of c)bits+=v.toString(2).padStart(width,"0");assert(bits.length===L.N,"T5");let packed="";for(let i=0;i<bits.length;i+=8)packed+=String.fromCharCode(parseInt(bits.slice(i,i+8).padEnd(8,"0"),2));
  let valid=null;if(q===1){valid=0;for(let w=0;w<128;w++)if(F.every(c=>c.some(l=>((w>>(Math.abs(l)-1))&1)===+(l>0))))valid++;assert(valid===0,"reference")}
  cases.push({q,n,rows:rows.length,clauses:F.length,dimacs,cnfSha:H.sha(dimacs),cnfN:dimacs.length*8,nativeSha:H.sha(raw),nativeN:raw.length*8,nativeVertices:G.network.types.length,nativeEdges:G.network.edges.length,initialNative:{status:cl?"UNKNOWN":"UNSAT",pins:p.size,checks:m.n,affine:ge},T5:{n:L.n,m:L.m,N:L.N,bytes:packed.length,sha:H.sha(packed)},parityChecks,mod3Rhs:rows.length%3,valid})
 }
 return {replay,details,cases,gadget:H.gadgetAudit()}
}
if(typeof require==='function'){const fs=require('fs');const keys=['compiler','corpus','registry','hybrid','joint','random','checker'];const src=Object.fromEntries(keys.map((k,i)=>[k,fs.readFileSync(process.argv[i+2],'utf8')]));console.log(JSON.stringify(audit(src),null,2));}
