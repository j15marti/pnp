// Dense high-rank and deletion controls; node dense-controls.js cycle.js check-lower.js compile.js
function tests(engine,independent,checkLower,compile,sha){
 const enc=x=>JSON.stringify(x)+"\n",v=x=>BigInt("0x"+x),records=[];
 function generate(q,yes,ablate=false){let n=2*q,rows=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>({j,v:(i%2===0&&j===i+1?1n<<BigInt(i/2):0n).toString(16)})).filter(e=>!ablate||i!==0||e.j!==1));return {format:"MATCH-SYNDROME-v1",dimension:q+1,rows,target:(yes?(1n<<BigInt(q))-1n:1n<<BigInt(q)).toString(16)}}
 function run(name,F){let bytes=enc(F),id=sha(bytes),R=engine(F,"lex"),I=independent(F,R),L=checkLower(F,R),S=engine(F,"spectral"),J=independent(F,S),K=checkLower(F,S);let x={name,short_id:name+"@"+id.slice(0,12),problem_id:"MATCH-SYNDROME-v1",instance_id:"MATCH-SYNDROME-v1:sha256:"+id,N_bits:bytes.length*8,source:F,guard_id:"EMPTY",residual_id:"ROOT",original_ids:{rows:[0,F.rows.length-1],resources:[0,F.rows.length-1],records:"row-local zero based"},parents:[],lex:R,spectral:S,independent:I,lower:L,spectralCheck:J,spectralLower:K};records.push({certificate_id:"CERT-v1:sha256:"+sha(enc(x)),record:x});return x}
 for(const q of [2,4,8,16])for(const yes of [true,false])run("DENSE-INDEPENDENT-"+q+"-"+(yes?"YES":"NO"),generate(q,yes));
 const ablation=run("DENSE-INDEPENDENT-8-EDGE-REMOVED",generate(8,true,true));if(ablation.lex.status!=="NO_AFFINE")throw Error("ablation");
 // For a small recognized source, build an exact CNF using one variable per matching edge and explicit syndrome parity clauses.
 function encode(F,R){const n=F.rows.length,es=[],C=[],rows=[],cols=Array.from({length:n},()=>[]);for(let i=0;i<n;i++){let A=[];for(let e of F.rows[i]){let k=es.length+1;es.push({i,j:e.j,v:e.v,k});A.push(k);cols[e.j].push(k)}rows.push(A)}
  function exactly(A){C.push(A.slice());for(let i=0;i<A.length;i++)for(let j=i+1;j<A.length;j++)C.push([-A[i],-A[j]])}rows.forEach(exactly);cols.forEach(exactly);
  const target=v(F.target);for(let b=0;b<F.dimension;b++){let A=es.filter(e=>v(e.v)&(1n<<BigInt(b))).map(e=>e.k),want=Number((target>>BigInt(b))&1n);if(A.length>8)throw Error("control width");for(let m=0;m<2**A.length;m++){let p=0;for(let k=0;k<A.length;k++)p^=(m>>k)&1;if(p!==want)C.push(A.map((a,k)=>(m>>k)&1?-a:a))}}
  const dimacs="p cnf "+es.length+" "+C.length+"\n"+C.map(c=>c.join(" ")+(c.length?" ":"")+"0\n").join(""),G=compile({nvars:es.length,dimacs}),src=enc(G.network),map=enc(G.source_map);
  let meta={native_id:"STRICT-EB4-v1:sha256:"+sha(src),native_N:src.length*8,cnf_id:"DIMACS-CNF-v1:sha256:"+sha(dimacs),cnf_N:dimacs.length*8,map_sha:sha(map),original_ids:{vertices:[0,G.network.types.length-1],ports:[0,4*G.network.types.length-1],edges:[0,G.network.edges.length-1],clauses:[1,C.length],variables:[1,es.length]},dimacs};
  if(!R.witness)return meta;
  let A=new Map(es.map(e=>[e.k,Number(R.witness.some(z=>z.i===e.i&&z.j===e.j&&z.v===e.v))])),lit=l=>A.get(Math.abs(l))^Number(l<0);
  if(!C.every(c=>c.some(l=>lit(l))))throw Error("source CNF witness");
  let next=es.length;for(const c of C)if(c.length>3){let p=++next;A.set(p,Number(!lit(c[0])&&!lit(c[1])));for(let j=2;j<c.length-2;j++){let t=++next;A.set(t,Number(A.get(p)&&!lit(c[j])));p=t}}
  const groups=new Map([...A].map(([i,b])=>["x"+i,b]));groups.set("f",0);
  G.source_map.ternary_clauses.forEach(([a,b,c],i)=>{let aa=lit(a),bb=lit(b),cc=lit(c),z=[0,1].find(z=>[aa+bb+z,1-z+cc].every(s=>s===1||s===2));if(z===undefined)throw Error("NAE lift");groups.set("z"+i,z);groups.set("w"+i+"_0",2-aa-bb-z);groups.set("w"+i+"_1",2-(1-z)-cc)});
  const nport=4*G.network.types.length,adj=Array.from({length:nport},()=>[]),bits=new Int8Array(nport).fill(-1);
  function add(a,b,s){adj[a].push([b,s]);adj[b].push([a,s])}
  for(const [a,b,s] of G.network.edges)add(a,b,s);G.network.types.forEach((t,i)=>{if(t==="E")for(let j=1;j<4;j++)add(4*i,4*i+j,0)});
  const Q=[];for(const [id,[p,s]] of Object.entries(G.source_map.representative_ports)){const b=groups.get(id)^s;if(bits[p]>=0&&bits[p]!==b)throw Error("seed");if(bits[p]<0){bits[p]=b;Q.push(p)}}
  let arcs=0;for(const p of Q)for(const [r,s] of adj[p]){arcs++;let b=bits[p]^s;if(bits[r]<0){bits[r]=b;Q.push(r)}else if(bits[r]!==b)throw Error("signed transport")}
  if(Q.length!==nport)throw Error("unassigned");let checks=0;for(const [a,b,s] of G.network.edges){checks++;if((bits[a]^bits[b])!==s)throw Error("edge")}for(let i=0;i<G.network.types.length;i++){checks++;let t=G.network.types[i],z=Array.from({length:4},(_,j)=>bits[4*i+j]);if(t==="E"?!z.every(x=>x===z[0]):z.reduce((a,b)=>a+b,0)!==2)throw Error("vertex")}
  return {...meta,nativeWitness:Array.from(bits).join(""),checks,arcs,sourceClauseChecks:C.length};
 }
 const base=records[0].record,ctrl=records[1].record;return {records,nativeControls:[{parent:records[0].certificate_id,source:base.instance_id,...encode(base.source,base.lex)},{parent:records[1].certificate_id,source:ctrl.instance_id,...encode(ctrl.source,ctrl.lex)}]};
}
const fs=require('node:fs'),crypto=require('node:crypto');const [c,l,cp]=process.argv.slice(2).map(p=>fs.readFileSync(p,'utf8'));const {engine,independent}=new Function(c.slice(0,c.indexOf("const fs=require('node:fs'),crypto"))+';return {engine,independent}')();const checkLower=new Function(l.slice(0,l.indexOf('const fs=require'))+';return checkLower')();const compile=new Function(cp.slice(cp.indexOf('function compile'),cp.indexOf('function auditLocal'))+';return compile')();const sha=s=>crypto.createHash('sha256').update(s).digest('hex');console.log(JSON.stringify(tests(engine,independent,checkLower,compile,sha)));
