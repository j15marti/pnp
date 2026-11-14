"use strict";
// Reproducer for TMR-1/007 graph/component parity criterion. Node.js 22+, no packages.
// This is a finite GF(2) verification, NOT a Turing machine simulation.
function edges(name) {
 let E=[],add=(a,b)=>E.push([Math.min(a,b),Math.max(a,b)]);
 if(name[0]==="K"){let n=+name.slice(1);for(let a=0;a<n;a++)for(let b=a+1;b<n;b++)add(a,b)}
 else if(name==="prism"){for(let [a,b] of [[0,1],[1,2],[2,0],[3,4],[4,5],[5,3],[0,3],[1,4],[2,5]])add(a,b)}
 else if(name==="cube"){for(let a=0;a<8;a++)for(let k of [1,2,4])if(a<(a^k))add(a,a^k)}
 else if(name==="bowtie"){for(let vv of [[0,1,2,3],[0,4,5,6]])for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)add(vv[a],vv[b])}
 else throw Error(name);
 return [...new Map(E.map(e=>[e.join(":"),e])).values()].sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
}
function graph(E) {let N=1+Math.max(...E.flat()),adj=Array.from({length:N},()=>[]);for(let [u,v] of E){adj[u].push(v);adj[v].push(u)}for(let a of adj)a.sort((x,y)=>x-y);return adj}
function components(adj,v) {let unseen=new Set(adj.map((_,i)=>i).filter(i=>i!==v)),cs=[];while(unseen.size){let s=[unseen.values().next().value],c=[];unseen.delete(s[0]);while(s.length){let u=s.pop();c.push(u);for(let w of adj[u])if(unseen.delete(w))s.push(w)}cs.push(c)}return cs}
function build(E,adj,b) {
 let vars=new Map(),id=s=>{if(!vars.has(s))vars.set(s,vars.size);return vars.get(s)};
 for(let [a,c] of E)id("e:"+a+":"+c);
 let gates=[];
 for(let v=0;v<adj.length;v++){
  let ee=adj[v].map(u=>id("e:"+Math.min(u,v)+":"+Math.max(u,v))),d=ee.length;
  if(d<3)throw Error("min-degree");
  let aux=Array.from({length:d-3},(_,i)=>id("a:"+v+":"+i)),local=[];
  if(d===3)local.push([ee,b[v]]);
  else {local.push([[ee[0],ee[1],aux[0]],0]);
    for(let j=1;j<d-3;j++)local.push([[aux[j-1],ee[j+1],aux[j]],0]);
    local.push([[aux.at(-1),ee.at(-2),ee.at(-1)],b[v]])}
  local.forEach(([ids,c],p)=>gates.push({v,p,ids,c}));
 }
 return {n:vars.size,vars,gates};
}
function solve(n,rows) {
 let P=new Map(),limit=(1n<<BigInt(n))-1n;
 for(let [ids,rhs] of rows){let x=0n,z=rhs;
  for(let j of ids)x^=1n<<BigInt(j);
  while(x){let p=x.toString(2).length-1;
   if(P.has(p)){let [a,b]=P.get(p);x^=a;z^=b}
   else{P.set(p,[x,z]);break}}
  if(!x&&z)return null;
 }
 let value=0n;
 for(let p of [...P.keys()].sort((a,b)=>a-b)){
  let [bits,z]=P.get(p),t=(bits&limit&~(1n<<BigInt(p)))&value;
  while(t){z^=1;t&=t-1n}
  if(z)value|=1n<<BigInt(p);
 }
 for(let [ids,rhs] of rows){let z=0;for(let j of ids)z^=Number((value>>BigInt(j))&1n);if(z!==rhs)throw Error("GF mismatch")}
 return value;
}
function wrong(z){let out=[];for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let c=0;c<2;c++)if((a^b^c)!==z)out.push([a,b,c]);return out}
function full(gates,q,t){let R=gates.map((g,i)=>[g.ids,g.c^(i===q?1:0)]);if(q>=0)gates[q].ids.forEach((x,k)=>R.push([[x],t[k]]));return R}
function condition(E,adj,b,X,q,t) {
 let v=X.gates[q].v,inc=adj[v].map(u=>X.vars.get("e:"+Math.min(u,v)+":"+Math.max(u,v))),comps=components(adj,v);
 for(let mask=0;mask<(1<<inc.length);mask++){
  let fixed=new Map(inc.map((id,i)=>[id,(mask>>i)&1])),ok=true;
  for(let comp of comps){let a=0,z=0;
   for(let u of comp){a^=b[u];if(adj[u].includes(v))z^=fixed.get(X.vars.get("e:"+Math.min(u,v)+":"+Math.max(u,v)))}
   if(a!==z){ok=false;break}}
  if(!ok)continue;
  let R=X.gates.map((g,i)=>[g,i]).filter(([g])=>g.v===v).map(([g,i])=>[g.ids,g.c^(i===q?1:0)]);
  for(let [id,bit] of fixed)R.push([[id],bit]);
  X.gates[q].ids.forEach((id,i)=>R.push([[id],t[i]]));
  if(solve(X.n,R)!==null)return true;
 }
 return false;
}
function audit(){
 let cases=[],total={cases:0,original_unsat:0,original_sat:0,deletion_sat:0,deletion_unsat:0,criterion_agrees:0,deletion_unique_witness:0,polarity_flip_witness_checks:0,negative_articulation_cases:0,assertions:0};
 for(let name of ["K4","K5","K6","prism","cube","bowtie"]){
  let E=edges(name),adj=graph(E);
  for(let pos of [0,adj.length-1]){
   let b=adj.map((_,v)=>+(v===pos)),X=build(E,adj,b);
   if(X.n!==3*(E.length-adj.length)||X.gates.length!==2*(E.length-adj.length))throw Error("formula sizes");
   if(solve(X.n,full(X.gates,-1,[]))!==null)throw Error("odd charge SAT");
   total.original_unsat++;
   let a={graph:name,odd_charge_position:pos,vertices:adj.length,edges:E.length,variables:X.n,clauses:4*X.gates.length,deletion_sat:0,deletion_unsat:0,articulation:adj.some((_,v)=>components(adj,v).length>1)};
   for(let q=0;q<X.gates.length;q++)for(let t of wrong(X.gates[q].c)){
    let w=solve(X.n,full(X.gates,q,t)),c=condition(E,adj,b,X,q,t);
    total.criterion_agrees++;total.assertions++;
    if((w!==null)!==c)throw Error("criterion");
    if(w===null){a.deletion_unsat++;total.deletion_unsat++;if(a.articulation)total.negative_articulation_cases++}
    else{
     a.deletion_sat++;total.deletion_sat++;
     let bad=0;
     for(let j=0;j<X.gates.length;j++)for(let z of wrong(X.gates[j].c)){
      let falseClause=X.gates[j].ids.every((id,k)=>Number((w>>BigInt(id))&1n)===z[k]);
      if(falseClause){bad++;if(j!==q||z.join("")!==t.join(""))throw Error("another false clause")}
     }
     if(bad!==1)throw Error("bad witness");
     total.deletion_unique_witness++;total.assertions++;
     for(let i=0;i<3;i++){let mut=t.map((z,k)=>z^(k===i?1:0));
      if(!X.gates[q].ids.some((id,k)=>Number((w>>BigInt(id))&1n)!==mut[k]))throw Error("sign-flip witness");
      total.polarity_flip_witness_checks++;total.assertions++}
    }
   }
   if(!a.articulation&&a.deletion_unsat)throw Error("biconnected bad");
   if(name==="bowtie"&&pos===0){
    let q=X.gates.findIndex(g=>g.v===0&&g.p===1),t=[1,0,0];
    if(solve(X.n,full(X.gates,q,t))!==null)throw Error("bowtie should remain unsat");
    a.specific_falsifier={v:0,gate:1,forbidden_tuple:t,deletion_remains_unsat:true,left_boundary_xor_required:0,left_boundary_xor_forced:1,right_boundary_xor_required:0,right_boundary_xor_forced:1};
   }
   cases.push(a);total.cases++;
  }
  let zero=adj.map(()=>0),Y=build(E,adj,zero),s=solve(Y.n,full(Y.gates,-1,[]));
  if(s===null)throw Error("even charge UNSAT");
  for(let g of Y.gates)for(let t of wrong(g.c))if(g.ids.every((id,k)=>Number((s>>BigInt(id))&1n)===t[k]))throw Error("even bad");
  total.original_sat++;total.assertions++;
 }
 return {status:"COMPUTATIONAL",method:"Independent V8 GF(2) implementation checks exact connected-graph component parity criterion",seed:null,totals:total,cases};
}
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(audit(),null,2));
if(typeof module!=="undefined")module.exports={audit};
