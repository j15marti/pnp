
function transfer(compile,r,bl){
 const ck=(x,m)=>{if(!x)throw Error(m)},start=Date.now(),n=r.original_ids.variables[1],G=compile({nvars:n,dimacs:r.dimacs}),net=G.network,sm=G.source_map,A=native(net),P=A.map,bytes=J(net),hash=sha(bytes);
 ck(!A.conflict,"parity conflict");
 let source=r.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1)),tern=source.map(a=>{ck(a.length===2||a.length===3,"arity");let b=a.slice();while(b.length<3)b.push(b.at(-1));return b});
 ck(J(tern)===J(sm.ternary_clauses)&&sm.original_n===n&&sm.original_clause_ids.length===source.length&&sm.original_clause_ids.every((v,i)=>v===i+1),"source padding");
 let ports=new Set(),pairs=new Set(),edgeChecks=0;
 for(let [a,b,s] of net.edges){ck(Number.isInteger(a)&&Number.isInteger(b)&&a>=0&&a<P.length&&b>=0&&b<P.length&&[0,1].includes(s),"edge range");let u=Math.floor(a/4),v=Math.floor(b/4),k=Math.min(u,v)+","+Math.max(u,v);ck(u!==v&&!pairs.has(k)&&!ports.has(a)&&!ports.has(b),"simple 4 regular");pairs.add(k);ports.add(a);ports.add(b);ck(P[a][0]===P[b][0]&&(P[a][1]^P[b][1])===s,"signed quotient");edgeChecks++}
 ck(ports.size===P.length,"port coverage");
 let logical=new Map(),byRoot=new Map(),expected=new Set(["f"]);for(let i=1;i<=n;i++)expected.add("x"+i);for(let i=0;i<source.length;i++){expected.add("z"+i);expected.add("w"+i+"_0");expected.add("w"+i+"_1")}
 for(let [id,[p,s]] of Object.entries(sm.representative_ports)){ck(expected.has(id)&&Number.isInteger(p)&&p>=0&&p<P.length&&[0,1].includes(s),"rep");let [root,t]=P[p];ck(!byRoot.has(root),"shared logical root");logical.set(id,{root,phase:t^s});byRoot.set(root,id)}
 ck(logical.size===expected.size&&byRoot.size===A.roots&&P.every(([root])=>byRoot.has(root)),"all logical classes");
 let seen=new Set(),Bchecks=0,Echecks=0;const literal=l=>["x"+Math.abs(l),Number(l<0)];
 for(let [v,t] of net.types.entries()){let o=sm.vertex_provenance[v];if(t==="E"){let a=P[4*v];for(let j=1;j<4;j++){ck(J(P[4*v+j])===J(a),"E class");Echecks++}continue}
 ck(t==="B"&&o[0]==="clause","B owner");let [,parent,i,j,k]=o;ck(parent===i+1&&i>=0&&i<source.length&&[0,1].includes(j)&&[0,1].includes(k),"owner range");let tag=[i,j,k].join(",");ck(!seen.has(tag),"duplicate B");seen.add(tag);
 let [a,b,c]=tern[i],row=j===0?[literal(a),literal(b),["z"+i,0],["w"+i+"_0",0]]:[["z"+i,1],literal(c),["f",0],["w"+i+"_1",0]];
 for(let [h,[id,s]] of row.entries()){let R=logical.get(id),[root,t0]=P[4*v+h];ck(root===R.root&&t0===(R.phase^s),"B incidence");Bchecks++}}
 ck(seen.size===4*source.length,"every gadget");
 let truthChecks=0;for(let f=0;f<2;f++)for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let c=0;c<2;c++){let ok=false;for(let z=0;z<2;z++)for(let w=0;w<2;w++)for(let v=0;v<2;v++){truthChecks++;if(a+b+z+w===2&&1-z+c+f+v===2)ok=true}ck(ok===Boolean((a^f)||(b^f)||(c^f)),"local clause equivalence")}
 let witness=null;if(r.answer==="SAT"){let W=bl.witness.W,values=new Map([["f",0]]);for(let i=1;i<=n;i++)values.set("x"+i,W[i]);let trials=0;
 for(let [i,row] of tern.entries()){let [a,b,c]=row.map(l=>W[Math.abs(l)]^Number(l<0)),hit=false;for(let z=0;z<2&&!hit;z++){let w=2-a-b-z,v=2-(1-z)-c;trials++;if([0,1].includes(w)&&[0,1].includes(v)){values.set("z"+i,z);values.set("w"+i+"_0",w);values.set("w"+i+"_1",v);hit=true}}ck(hit,"SAT lift")}
 let rootVals=new Map([...logical].map(([id,a])=>[a.root,values.get(id)^a.phase])),word=P.map(([root,t])=>rootVals.get(root)^t);ck(word.every(x=>x===0||x===1),"total lift");let checks=0;for(let [a,b,s] of net.edges){ck((word[a]^word[b])===s,"native edge witness");checks++}for(let [v,t] of net.types.entries()){let a=word.slice(4*v,4*v+4);ck(t==="E"?a.every(b=>b===a[0]):a.reduce((s,b)=>s+b,0)===2,"native vertex witness");checks++}witness={packed:word.join(""),sha:sha(word.join("")+"\n"),checks,trials}}
 return {model:"STRICT-EB4-v1",short:"EB-"+r.short.split("@")[0].slice(4)+"@"+hash.slice(0,12),instance_id:"STRICT-EB4-v1:sha256:"+hash,N:bytes.length*8,guard:"EMPTY",residual:"ROOT",sourceCNF:r.instance_id,sourceN:r.N,sourceMapSHA:sha(J(sm)),vertices:net.types.length,ports:P.length,edges:net.edges.length,classes:A.roots,sourceClauses:source.length,checks:{edgeChecks,Echecks,Bchecks,truthChecks},parentProof:"CERT-v1:sha256:a0995bcce5367b97c8281201fb19532df26156b0b7ec34b8cfef960311255aa5",answer:r.answer,witness,ms:Date.now()-start}
}

// Load pinned check.js; call transfer(compile, CNF record, blind record).
