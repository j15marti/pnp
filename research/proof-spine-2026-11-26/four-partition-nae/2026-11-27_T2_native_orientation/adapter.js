// Map-assisted checker; run node adapter.js benchmarks.json JOINT_certificate.json RANDOM_certificate.json
const fs=require('node:fs');
function compile(instance){
 const lines=instance.dimacs.trimEnd().split("\n"),h=lines.shift().split(" ").map((s,i)=>i>=2?Number(s):s);
 if(h[0]!=="p"||h[1]!=="cnf"||h[2]!==instance.nvars||h[3]!==lines.length)throw Error("header");
 const n=instance.nvars,F=[],parents=[];let next=n;
 const add=(a,id)=>{F.push(a);parents.push(id)};
 lines.forEach((line,i)=>{const a=line.split(/\s+/).map(Number);if(a.pop()!==0||a.some(l=>!Number.isInteger(l)||!l||Math.abs(l)>n))throw Error("bad clause");const id=i+1;if(a.length===0){let v=++next;add([v,v,v],id);add([-v,-v,-v],id)}else if(a.length<=3){while(a.length<3)a.push(a[a.length-1]);add(a,id)}else{let prev=++next;add([a[0],a[1],prev],id);for(let j=2;j<a.length-2;j++){let t=++next;add([-prev,a[j],t],id);prev=t}add([-prev,a[a.length-2],a[a.length-1]],id)}});
 const types=[],used=[],edges=[],groups=new Map(),reps={},owners=[];
 const V=(t,owner)=>{types.push(t);used.push(0);owners.push(owner);return types.length-1};
 const P=v=>{if(used[v]>=4)throw Error("port overflow");return 4*v+used[v]++};
 const E=(a,b,s=0)=>edges.push([a,b,s]);
 const wire=(a,b,s)=>{const v=Array.from({length:5},()=>V("E",["wire",a,b]));for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)if(i!==0||j!==1)E(P(v[i]),P(v[j]));E(a,P(v[0]),s);E(b,P(v[1]),0)};
 const occ=(id,s,p)=>{if(!groups.has(id))groups.set(id,[]);groups.get(id).push([p,s])};
 F.forEach(([a,b,c],i)=>{const L=x=>["x"+Math.abs(x),Number(x<0)],z="z"+i,T=[[L(a),L(b),[z,0]],[[z,1],L(c),["f",0]]];for(let j=0;j<2;j++)for(let k=0;k<2;k++){let v=V("B",["clause",parents[i],i,j,k]);for(const [id,s] of T[j])occ(id,s,P(v));occ("w"+i+"_"+j,0,P(v))}});
 for(const [id,O] of groups){if(O.length%2||O.length<2)throw Error("occurrence parity");reps[id]=O[0];if(O.length===2){wire(O[0][0],O[1][0],O[0][1]^O[1][1]);continue}const a=Array.from({length:(O.length-2)/2},()=>V("E",["carrier",id]));for(let i=1;i<a.length;i++)wire(P(a[i-1]),P(a[i]),0);let k=0;for(const v of a)while(used[v]<4){const [p,s]=O[k++];wire(P(v),p,s)}if(k!==O.length)throw Error("fanout")}
 const seen=new Set(),ports=new Set();for(const [a,b,s] of edges){let u=Math.floor(a/4),v=Math.floor(b/4),key=Math.min(u,v)+":"+Math.max(u,v);if(u===v||seen.has(key)||ports.has(a)||ports.has(b)||![0,1].includes(s))throw Error("not simple signed 4-regular");seen.add(key);ports.add(a);ports.add(b)}
 if(used.some(x=>x!==4)||ports.size!==4*types.length)throw Error("degree");
 const network={format:"STRICT-EB4-v1",types,edges};
 return {network,source_map:{original_n:n,ternary_clauses:F,original_clause_ids:parents,representative_ports:reps,vertex_provenance:owners}};
}

function adapt(G,cert,dimacs){
 const {network:net,source_map:map}=G,n=4*net.types.length,adj=Array.from({length:n},()=>[]);
 function link(a,b,s){adj[a].push([b,s]);adj[b].push([a,s])}
 for(const [a,b,s] of net.edges)link(a,b,s);net.types.forEach((t,i)=>{if(t==="E")for(let j=1;j<4;j++)link(4*i,4*i+j,0)});
 let root=new Int32Array(n).fill(-1),par=new Uint8Array(n),arcs=0;for(let i=0;i<n;i++)if(root[i]<0){let q=[i];root[i]=i;for(let j=0;j<q.length;j++)for(const [v,s] of adj[q[j]]){arcs++;let b=par[q[j]]^s;if(root[v]<0){root[v]=i;par[v]=b;q.push(v)}else if(par[v]!==b)throw Error("signed contradiction")}}
 let rep={};for(const [name,[p,s]] of Object.entries(map.representative_ports))rep[name]=[root[p]+1,par[p]^s];
 let [anchor,anchorSign]=rep.f;if(anchor!==cert.data.gauge_port+1)throw Error("anchor");
 let found=new Set(),portWords=0,vertexChecks=0,sourceFactors=0;
 for(const f of cert.data.final){let ownerIds=f.ids.map(i=>{let o=map.vertex_provenance[i];vertexChecks++;if(net.types[i]!=="B"||o[0]!=="clause")throw Error("B ID");return o[2]});let j=ownerIds[0];if(f.ids.length!==4||ownerIds.some(i=>i!==j)||found.has(j))throw Error("factor provenance");found.add(j);let ls=map.ternary_clauses[j],expected=[...new Set([anchor,...ls.map(l=>rep["x"+Math.abs(l)][0])])].sort((a,b)=>a-b);if(JSON.stringify(expected)!==JSON.stringify(f.v))throw Error("scope");for(let w=0;w<2**f.v.length;w++){portWords++;let a=((w>>f.v.indexOf(anchor))&1)^anchorSign;let sat=ls.some(l=>{let [r,s]=rep["x"+Math.abs(l)];return (((w>>f.v.indexOf(r))&1)^s^a^Number(l<0))===1});if(sat!==f.ok.includes(w))throw Error("factor truth")}sourceFactors++}
 if(found.size!==map.ternary_clauses.length)throw Error("missing");
 let F=dimacs.trimEnd().split("\n").slice(1).map(l=>l.split(/\s+/).map(Number).slice(0,-1)),groups=F.map(()=>[]);map.ternary_clauses.forEach((cl,i)=>groups[map.original_clause_ids[i]-1].push(cl));let splitTrials=0,sourceWords=0,auxSeen=new Set();
 for(let i=0;i<F.length;i++){let vs=[...new Set(F[i].map(Math.abs))],aux=[...new Set(groups[i].flat().map(Math.abs))].filter(v=>!vs.includes(v));for(let a of aux){if(a<=map.original_n||auxSeen.has(a))throw Error("not private");auxSeen.add(a)}for(let w=0;w<2**vs.length;w++){sourceWords++;let val=l=>((w>>vs.indexOf(Math.abs(l)))&1)^Number(l<0);let want=F[i].some(l=>val(l)),hit=false;for(let z=0;z<2**aux.length;z++){splitTrials++;let sat=groups[i].every(cl=>cl.some(l=>vs.includes(Math.abs(l))?val(l):((z>>aux.indexOf(Math.abs(l)))&1)^Number(l<0)));if(sat)hit=true}if(want!==hit)throw Error("split equivalence")}}
 return {arcs,anchor_port:anchor-1,anchorSign,sourceFactors,vertexChecks,portWords,sourceWords,splitTrials,privateAux:auxSeen.size,originalSourceClauses:F.length,sourceRepresentativeCount:Object.keys(rep).filter(k=>/^x/.test(k)).length,originalVariableMap:Object.fromEntries(Object.entries(rep).filter(([k])=>/^x/.test(k)))};
}
const corpus=JSON.parse(fs.readFileSync(process.argv[2]));for(let i=0;i<2;i++){const x=corpus.instances.find(x=>x.id===['JOINT-24','RANDOM-3CNF-40'][i]),c=JSON.parse(fs.readFileSync(process.argv[3+i]));console.log(JSON.stringify(adapt(compile(x),c,x.dimacs)));}
