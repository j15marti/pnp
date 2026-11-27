// Deterministic strict E4/B4 adapter, based on RT01 (7dd71185a1093e0066993a6c88d52bd233815319).
// node compile.js benchmarks.json INSTANCE output-prefix
// Writes network JSON (canonical ASCII + LF, input N), separate source map and printed summary.
// node compile.js --audit : replay local finite equivalence checks.
const fs=require("node:fs");
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
function auditLocal(){
 let clauses=0,truthChecks=0;
 // RT01 NAE4 -> two NAE3 -> balance: exhaustive relative literal values and both anchors.
 for(let f=0;f<2;f++)for(let word=0;word<8;word++){
  const [a,b,c]=[0,1,2].map(i=>((word>>i)&1)^f);let lifts=0;
  for(let z=0;z<2;z++)for(let d=0;d<2;d++)for(let e=0;e<2;e++){truthChecks++;if(a+b+z+d===2&&(1-z)+c+f+e===2)lifts++}
  if(Boolean(lifts)!==Boolean(word))throw Error("local clause equivalence");clauses++;
 }
 // Test the exact long clause transformation for lengths 0..7, exhaustive source/auxiliary words.
 let splitChecks=0;
 for(let n=0;n<=7;n++){const dimacs=`p cnf ${n} 1\n${Array.from({length:n},(_,i)=>i+1).join(" ")}${n?" ":""}0\n`;const G=compile({nvars:n,dimacs});const F=G.source_map.ternary_clauses;const v=Math.max(n,...F.flat().map(Math.abs));for(let x=0;x<2**n;x++){let hit=false;for(let y=0;y<2**(v-n);y++){let bits=x+y*2**n;splitChecks++;if(F.every(c=>c.some(l=>Boolean((bits>>(Math.abs(l)-1))&1)===(l>0))))hit=true}if(hit!==Boolean(x))throw Error("split equivalence")}}
 return {clauses,truthChecks,splitChecks};
}
function fnv(s){let h=2166136261;for(let i=0;i<s.length;i++)h=Math.imul(h^s.charCodeAt(i),16777619)>>>0;return h.toString(16).padStart(8,"0")}
if(process.argv[2]==="--audit"){console.log(JSON.stringify(auditLocal(),null,2));}
else {const b=JSON.parse(fs.readFileSync(process.argv[2],"utf8"));const x=b.instances.find(z=>z.id===process.argv[3]);if(!x)throw Error("instance not found");const G=compile(x),s=JSON.stringify(G.network)+"\n";fs.writeFileSync(process.argv[4]+".eb.json",s);fs.writeFileSync(process.argv[4]+".map.json",JSON.stringify(G.source_map)+"\n");console.log(JSON.stringify({id:x.id,vertices:G.network.types.length,edges:G.network.edges.length,N_bits:s.length*8,fnv1a32:fnv(s)}));}
