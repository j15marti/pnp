const fs=require('node:fs');
const run=function run(native){
 const {sha}=new Function(native+";return {sha};")(),A=(t,m)=>{if(!t)throw Error(m)},enc=x=>JSON.stringify(x)+"\n",sort=C=>C.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b),key=C=>sort(C).join(","),comp=C=>C.map(l=>-l),choose=(a,k)=>{let out=[];function go(i,s){if(!k||s.length===k){out.push(s);return}for(let j=i;j<=a.length-(k-s.length);j++)go(j+1,[...s,a[j]])}go(0,[]);return out};
 // Each block has at most two shared variables; size 5 only at ends, size 7 elsewhere.
 // Phase graph cycle on a permutation avoiding overlap edges.
 function generate(n,yes,seed){
  let blocks=[],id=0;for(let i=0;i<n;i++){let size=i===0||i===n-1?5:7,vs=[];if(i)vs.push(blocks[i-1].at(-1));while(vs.length<size)vs.push(++id);blocks.push(vs)}
  let st=seed>>>0;const rnd=()=>{st=(Math.imul(st,1664525)+1013904223)>>>0;return st};let perm=Array.from({length:id},(_,i)=>i+1);for(let i=id-1;i>0;i--){let j=rnd()%(i+1);[perm[i],perm[j]]=[perm[j],perm[i]]}
  blocks=blocks.map(B=>B.map(v=>(rnd()&1?1:-1)*perm[v-1]));
  // n odd, stepping by 2 gives a cycle, including wrap nonadjacent endpoints.
  let phase=[];for(let i=0;i<n;i++){let a=1+(2*i%n),b=1+(2*(i+1)%n),s=Number(!yes&&i===n-1);A(Math.abs(a-b)>1,"overlap in phase clause");phase.push([a,s?b:-b],[-a,s?-b:b])}
  let C=[];for(let c of phase){let packets=c.map(l=>choose(l>0?blocks[l-1]:comp(blocks[-l-1]),(blocks[Math.abs(l)-1].length+1)/2));for(let a of packets[0])for(let b of packets[1])C.push(sort([...a,...b]))}
  A(new Set(C.map(key)).size===C.length,"duplicate source");let dimacs="p cnf "+id+" "+C.length+"\n"+C.map(c=>c.join(" ")+" 0").join("\n")+"\n";return {dimacs,nvars:id,C,truth:{blocks,phase}};
 }
 function recognize(C,n){
  let m={deletions:0,keyLiterals:0,collisionPairs:0,cliqueEdges:0,intersectionTests:0,rowChecks:0,quotaChecks:0,phaseTests:0,witnessLiteralTests:0},index=new Map(),adj=new Map(),lits=[...new Set(C.flat())];
  function add(a,b){if(a===b)return;if(!adj.has(a))adj.set(a,new Set());if(!adj.has(b))adj.set(b,new Set());adj.get(a).add(b);adj.get(b).add(a)}
  // Exact deletion keys, no hash equality shortcut.
  for(let c of C)for(let i=0;i<c.length;i++){m.deletions++;let k=c.filter((_,j)=>i!==j).join(",");m.keyLiterals+=c.length-1;if(!index.has(k))index.set(k,new Set());index.get(k).add(c[i])}
  for(let S of index.values()){let a=[...S];for(let i=0;i<a.length;i++)for(let j=0;j<i;j++){m.collisionPairs++;add(a[i],a[j])}}
  let candidates=new Map();for(let [a,S] of adj)for(let b of S)if(a<b){m.cliqueEdges++;let T=[a,b];for(let x of S){m.intersectionTests++;if(adj.get(b).has(x))T.push(x)}let U=sort(T),k=key(U);if(candidates.has(k))continue;
    // All recovered signed sets must be cliques, odd cardinality, complement present later.
    if(U.length<5||U.length>7||U.length%2===0||new Set(U.map(Math.abs)).size!==U.length)return {decision:"UNKNOWN",reason:"clique shape",m};
    for(let i=0;i<U.length;i++)for(let j=0;j<i;j++){m.intersectionTests++;if(!adj.get(U[i]).has(U[j]))return {decision:"UNKNOWN",reason:"nonclique",m}}
    candidates.set(k,U)
  }
  let B=[];for(let U of candidates.values()){if(!candidates.has(key(comp(U))))return {decision:"UNKNOWN",reason:"missing complement",m};if(U[0]>0)B.push(U)}
  B.sort((a,b)=>a[0]-b[0]||key(a).localeCompare(key(b)));
  let owners=Array.from({length:n+1},()=>[]);B.forEach((U,i)=>U.forEach(l=>owners[Math.abs(l)].push(i)));
  if(owners.slice(1).some(o=>!o.length))return {decision:"UNKNOWN",reason:"uncovered variable",m};
  const priv=B.map(U=>U.filter(l=>owners[Math.abs(l)].length===1)),shared=B.map((U,i)=>U.length-priv[i].length);
  // Stronger than independent-lift condition: two private bits in each threshold quota.
  if(B.some((U,i)=>shared[i]>(U.length-3)/2))return {decision:"UNKNOWN",reason:"private quota",m};
  let phase=new Map(),rowSet=new Set();for(let c of C){m.rowChecks++;let rowkey=key(c);if(rowSet.has(rowkey))return {decision:"UNKNOWN",reason:"duplicate rows",m};rowSet.add(rowkey);
   let P=new Set();for(let l of c){let o=owners[Math.abs(l)];if(o.length===1)P.add(o[0])}
   let used=new Set(),q=[],multiplicity=1;
   for(let i of [...P].sort((a,b)=>a-b)){let U=B[i],M=new Map(U.map(l=>[Math.abs(l),l])),D=c.filter(l=>M.has(Math.abs(l))),k=(U.length+1)/2;m.quotaChecks+=D.length;
    if(D.length!==k||D.some(l=>used.has(Math.abs(l))))return {decision:"UNKNOWN",reason:"overlap or quota",m};
    let s=D[0]===M.get(Math.abs(D[0]))?1:-1;if(D.some(l=>l!==s*M.get(Math.abs(l))))return {decision:"UNKNOWN",reason:"mixed orientation",m};
    D.forEach(l=>used.add(Math.abs(l)));q.push(s*(i+1));multiplicity*=choose(U,k).length;
   }
   if(used.size!==c.length||!q.length)return {decision:"UNKNOWN",reason:"unassigned source literal",m};
   // Require underlying supports of blocks in each phase clause disjoint (not merely chosen literals).
   let s=new Set();for(let l of q)for(let z of B[Math.abs(l)-1]){if(s.has(Math.abs(z)))return {decision:"UNKNOWN",reason:"overlap inside phase clause",m};s.add(Math.abs(z))}
   let k=key(q);if(!phase.has(k))phase.set(k,{clause:sort(q),count:0,multiplicity});let f=phase.get(k);f.count++;if(f.multiplicity!==multiplicity)return {decision:"UNKNOWN",reason:"multiplicity",m};
  }
  if([...phase.values()].some(x=>x.count!==x.multiplicity))return {decision:"UNKNOWN",reason:"incomplete expansion",m};
  let F=[...phase.values()].map(x=>x.clause);
  // Phase solver: exact 2-SAT via reachability, no use of source label or block ordering.
  if(F.some(c=>c.length!==2))return {decision:"UNKNOWN",reason:"nonbinary phase",m};
  let nn=B.length,L=Array.from({length:2*nn},(_,i)=>i),ix=l=>2*(Math.abs(l)-1)+(l<0?1:0),G=L.map(()=>[]),R=L.map(()=>[]);
  for(let [a,b] of F)for(let [u,v] of [[ix(-a),ix(b)],[ix(-b),ix(a)]]){G[u].push(v);R[v].push(u)}
  let seen=new Set(),order=[];function dfs(v){seen.add(v);for(let w of G[v]){m.phaseTests++;if(!seen.has(w))dfs(w)}order.push(v)}for(let i of L)if(!seen.has(i))dfs(i);
  let cc=Array(2*nn).fill(-1),k=0;function back(v){cc[v]=k;for(let w of R[v]){m.phaseTests++;if(cc[w]===-1)back(w)}}for(let v of order.reverse())if(cc[v]===-1){back(v);k++}
  let bad=L.find(i=>cc[i]===cc[i^1]);
  let paths=null,witness=null,phaseWitness=null;
  function path(a,b){let q=[a],P=new Map([[a,-1]]);for(let h=0;h<q.length;h++){let u=q[h];if(u===b)break;for(let v of G[u]){m.phaseTests++;if(!P.has(v)){P.set(v,u);q.push(v)}}}A(P.has(b),"scc path");let p=[b];while(p.at(-1)!==a)p.push(P.get(p.at(-1)));return p.reverse()}
  if(bad!==undefined){paths=[path(bad,bad^1),path(bad^1,bad)]}
  else {phaseWitness=B.map((_,i)=>Number(cc[2*i]>cc[2*i+1]));A(F.every(c=>c.some(l=>phaseWitness[Math.abs(l)-1]===+(l>0))),"phase witness");
    witness=Array(n+1).fill(0);for(let i=0;i<B.length;i++)for(let l of priv[i])witness[Math.abs(l)]=phaseWitness[i]^Number(l<0);
    A(B.every((U,i)=>+(U.filter(l=>witness[Math.abs(l)]===+(l>0)).length>U.length/2)===phaseWitness[i]),"lift majority");
    A(C.every(c=>c.some(l=>{m.witnessLiteralTests++;return witness[Math.abs(l)]===+(l>0)})),"source witness");
  }
  return {decision:bad===undefined?"YES":"NO",blocks:B,phase:F,privateCounts:priv.map(x=>x.length),shared,paths,witness,phaseWitness,m,indexKeys:index.size,phaseCounts:[...phase.values()]};
 }
 function audit(C,n,r){
  const B=r.blocks,F=r.phase,owners=Array.from({length:n+1},()=>0);B.forEach(U=>U.forEach(l=>owners[Math.abs(l)]++));A(B.every(U=>U.filter(l=>owners[Math.abs(l)]===1).length>U.length/2),"lift capacity");
  let got=new Set(),tests=0;
  for(let c of F){let lists=c.map(l=>{let U=B[Math.abs(l)-1];return choose(l>0?U:comp(U),(U.length+1)/2)});
   function go(i,acc){if(i===lists.length){tests++;let k=key(acc);A(!got.has(k),"audit overlap");got.add(k);return}for(let d of lists[i])go(i+1,[...acc,...d])}go(0,[])
  }
  A(got.size===C.length&&C.every(c=>got.has(key(c))),"expansion equality");
  let pathTests=0,witnessTests=0;
  if(r.decision==="YES"){A(r.witness&&C.every(c=>c.some(l=>{witnessTests++;return r.witness[Math.abs(l)]===+(l>0)})),"independent witness")}
  else {let lit=i=>(i&1?-1:1)*(1+(i>>1));A(r.paths[0][0]===r.paths[1].at(-1)&&r.paths[1][0]===r.paths[0].at(-1)&&(r.paths[0][0]^1)===r.paths[1][0],"contradictory paths");let D=new Set(F.map(key));for(let p of r.paths)for(let i=1;i<p.length;i++){pathTests++;A(D.has(key([-lit(p[i-1]),lit(p[i])])),"invalid implication")}}
  return {expansionRows:tests,pathTests,witnessTests};
 }
 let out=[];
 for(let n of [5,7,11])for(let yes of [false,true]){let g=generate(n,yes,31991+n);let r=recognize(g.C,g.nvars);A(r.decision===(yes?"YES":"NO"),"recognition");let a=audit(g.C,g.nvars,r);A(new Set(r.blocks.map(U=>key(U.map(Math.abs)))).size===n,"block count");
  let hash=sha(g.dimacs),id=`OVERLAP-SIGNED-MAJ-${n}-${yes?"YES":"NO"}@${hash.slice(0,12)}`;
  out.push({problem_id:"DIMACS-CNF-v1",instance:id,instance_id:"DIMACS-CNF-v1:sha256:"+hash,original_N_bits:g.dimacs.length*8,original_ids:{variables:[1,g.nvars],clauses:[1,g.C.length]},guard_id:"EMPTY",residual_id:"ROOT",recipe:{n,yes,seed:31991+n},physical:g.nvars,clauses:g.C.length,decision:r.decision,recognition:r,audit:a})
 }
 return out;
};
console.log(JSON.stringify(run(fs.readFileSync(process.argv[2],'utf8')),null,2));
