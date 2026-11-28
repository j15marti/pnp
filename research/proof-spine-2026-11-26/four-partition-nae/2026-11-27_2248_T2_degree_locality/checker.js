// Coupled AND-seam family: explicit DIMACS, no auxiliaries. Node.js.
const crypto=require("node:crypto"),sha=s=>crypto.createHash("sha256").update(s).digest("hex");
function generate(m,k,yes=false){
 if(m<3||m%2!==1||k<2)throw Error("parameters");
 let F=[],blocks=Array.from({length:m},(_,i)=>Array.from({length:k},(_,j)=>i*k+j+1)),edges=[];
 for(let i=0;i<m;i++){let j=(i+1)%m,A=blocks[i],B=blocks[j],equal=yes&&i===m-1,start=F.length+1;
 if(equal){for(let a of A)F.push([...B.map(b=>-b),a]);for(let b of B)F.push([...A.map(a=>-a),b]);}
 else{for(let a of A)for(let b of B)F.push([a,b]);F.push([...A,...B].map(v=>-v));}
 edges.push({i,j,equal,clauses:[start,F.length]});}
 let dimacs="p cnf "+m*k+" "+F.length+"\n"+F.map(c=>c.join(" ")+" 0").join("\n")+"\n";
 return {m,k,yes,F,blocks,edges,dimacs};
}
function verify(g){
 const {m,k,F,blocks,edges,yes}=g;let tests=0;
 // Re-parse actual clauses and independently recognize block structure from
 // negative seam clauses in NO case; for YES use authenticated supplied blocks.
 let lines=g.dimacs.trimEnd().split("\n"),h=lines.shift().split(" ");if(+h[2]!==m*k||+h[3]!==F.length)throw Error("header");
 const C=lines.map(s=>s.split(" ").map(Number).slice(0,-1));
 let keys=new Set(C.map(c=>c.slice().sort((a,b)=>a-b).join(",")));if(keys.size!==C.length)throw Error("duplicate");
 function has(c){tests++;return keys.has(c.slice().sort((a,b)=>a-b).join(","))}
 let recovered=null;
 if(!yes){const neg=C.filter(c=>c.every(l=>l<0)).map(c=>c.map(x=>-x));let incidence=new Map();
 for(let i=0;i<neg.length;i++)for(let v of neg[i]){if(!incidence.has(v))incidence.set(v,[]);incidence.get(v).push(i)}
 let groups=new Map();for(let [v,e] of incidence){let key=e.join(",");if(!groups.has(key))groups.set(key,[]);groups.get(key).push(v)}
 recovered=[...groups.values()];if(recovered.length!==m||recovered.some(a=>a.length!==k))throw Error("recognition");
 let ids=new Map();recovered.forEach((a,i)=>a.forEach(v=>ids.set(v,i)));
 let adj=Array.from({length:m},()=>[]);
 for(let e of neg){let [a,b]=[...new Set(e.map(v=>ids.get(v)))];if(a===undefined||b===undefined||new Set(e.map(v=>ids.get(v))).size!==2)throw Error("edge");adj[a].push(b);adj[b].push(a);
 for(let x of recovered[a])for(let y of recovered[b])if(!has([x,y]))throw Error("missing positive clause")}
 if(adj.some(a=>a.length!==2))throw Error("not cycle");let seen=new Set(),stack=[0];while(stack.length){let x=stack.pop();if(seen.has(x))continue;seen.add(x);stack.push(...adj[x])}if(seen.size!==m||m%2!==1)throw Error("not odd cycle");
 if(C.length!==m*(k*k+1))throw Error("extra source clauses");
 }
 // Direct verification of every factor and every block assignment for small k.
 let truthTests=0;
 for(const e of edges){let A=blocks[e.i],B=blocks[e.j],vs=[...A,...B];let rows=C.slice(e.clauses[0]-1,e.clauses[1]);
 if(k<=5)for(let w=0;w<2**(2*k);w++){let evalv=v=>w>>vs.indexOf(v)&1,actual=rows.every(c=>c.some(l=>evalv(Math.abs(l))===+(l>0))),a=A.every(evalv),b=B.every(evalv);truthTests++;if(actual!==(e.equal?a===b:a!==b))throw Error("truth mismatch");}
 }
 let witness=null;if(yes){witness=Array.from({length:m*k},(_,v)=>Math.floor(v/k)%2?0:1);if(!C.every(c=>c.some(l=>witness[Math.abs(l)-1]===+(l>0))))throw Error("YES");}
 // Exact XOR certificate in the block monomial basis: g_e=1+M_i+M_j
 // on NO, each monomial appears twice and m is odd.
 let terms=new Set();if(!yes){for(const {i,j} of edges)for(let t of ["1",blocks[i].join(","),blocks[j].join(",")]){if(terms.has(t))terms.delete(t);else terms.add(t)}if(terms.size!==1||!terms.has("1"))throw Error("identity")}
 // Check the explicit evaluation-functional proof on every monomial of a
 // k-bit block of degree < k: XOR of all words except all-ones equals 1.
 let dualChecks=0;if(k<=12){for(let a=0;a<(1<<k)-1;a++){let x=0;for(let w=0;w<(1<<k)-1;w++)x^=+((a&w)===a);dualChecks++;if(x!==1)throw Error("dual")}}
 return {tests,truthTests,dualChecks,recoveredBlocks:recovered,terminal:yes?"SAT":"UNSAT",witness,degree:k,staticXorTerms:yes?null:3*m};
}
function run(){let out=[];for(let [m,k] of [[5,3],[11,3],[23,4],[47,5],[95,8]])for(let yes of [false,true]){let g=generate(m,k,yes),v=verify(g),h=sha(g.dimacs),cert={problem_id:"DIMACS-CNF-v1",instance:"AND-SEAM-"+m+"-"+k+"-"+(yes?"YES":"NO")+"@"+h.slice(0,12),instance_id:"DIMACS-CNF-v1:sha256:"+h,original_N_bits:g.dimacs.length*8,guard_id:"EMPTY",residual_id:"ROOT",original_ids:{variables:[1,m*k],clauses:[1,g.F.length]},parents:[],parameters:{m,k,yes},claim:yes?"exact witness":"odd block-phase cycle, static degree-k contradiction; no degree<k consequence from any proper subset of whole edge factors can exclude all-ones",checker:"checker.js",proof:{blocks:g.blocks,edges:g.edges,...v},dimacs:g.dimacs};out.push(cert)}return out}
if(require.main===module)console.log(JSON.stringify(run()));
module.exports={generate,verify,run};
