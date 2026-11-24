// Node.js, no dependencies. Reproduce: node <file>
function run(){
 let seed=0x201303, rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296},rng=n=>Math.floor(rand()*n);
 const range=n=>Array.from({length:n},(_,i)=>i), bit=i=>1n<<BigInt(i), xor=a=>a.reduce((x,y)=>x^y,0n);
 const assert=(x,m)=>{if(!x)throw Error(m)};
 let scans=0, augment=0;
 // Left items in given order; each insertion augments if possible, never unmatches an earlier item.
 function match(items,adj,n){let own=Array(n).fill(-1),failed=[];
  for(let x of items){let seen=new Set(),dfs=a=>{for(let y of adj[a]){scans++;if(seen.has(y))continue;seen.add(y);if(own[y]<0||dfs(own[y])){own[y]=a;return true}}return false};
   if(dfs(x))augment++;else failed.push(x)}
  return {own,failed,rank:own.filter(x=>x>=0).length}}
 function make(n,k,full=false){let m=n+k,A=range(m).map(i=>range(m).map(j=>i>=k||full||j===n+i||rand()<0.48));
  const randtag=()=>xor(range(n).filter(()=>rand()<.5).map(bit));
  let p=range(m).map(randtag),q=range(m).map(randtag);
  let g=A.map((row,i)=>row.map((v,j)=>v?(p[i]^q[j]^(i<k&&j<n?bit(j):0n)):null));
  return {n,k,m,A,g}}
 // supplied partition/dictionary, discover vertex gauge, check every edge and dummy saturation
 function certify(G){let {n,k,m,A,g}=G;
  if(A.slice(k).some(row=>row.some(x=>!x)))return null;
  let dummy=range(m).map(j=>range(k).filter(i=>A[i][j]));
  if(match(range(m-n).map(j=>n+j),dummy,k).rank!==k)return null;
  let p=Array(2*m).fill(null),neighbors=range(2*m).map(()=>[]);
  for(let i=0;i<m;i++)for(let j=0;j<m;j++)if(A[i][j]){
   let h=g[i][j]^(i<k&&j<n?bit(j):0n);neighbors[i].push([m+j,h]);neighbors[m+j].push([i,h])}
  for(let i=0;i<2*m;i++)if(p[i]===null){p[i]=0n;let stack=[i];while(stack.length){let v=stack.pop();for(let [u,h] of neighbors[v]){let t=p[v]^h;if(p[u]===null){p[u]=t;stack.push(u)}else if(p[u]!==t)return null}}}
  return {offset:xor(p),adj:range(m).map(j=>range(k).filter(i=>A[i][j]))}}
 function lift(G,C,J){let {n,k,m,A,g}=G;
  let R=match([...J,...range(m-n).map(j=>n+j)],C.adj,k);
  assert(R.rank===k&&!R.failed.some(j=>j<n),"local extension");
  let cols=new Set(R.own),unused=range(m).filter(j=>!cols.has(j));
  let perm=R.own.concat(unused);
  assert(perm.length===m&&new Set(perm).size===m&&perm.every((j,i)=>A[i][j]),"source PM");
  assert(xor(perm.map((j,i)=>g[i][j]))===(C.offset^xor(J.map(bit))),"source label");
  return xor(perm.map((j,i)=>g[i][j]))}
 function reference(G){let out=new Set(),count=0;let {m,A,g}=G;
  function dfs(i,used,s){if(i===m){out.add(s);count++;return}for(let j=0;j<m;j++)if(A[i][j]&&!(used&(1<<j)))dfs(i+1,used|(1<<j),s^g[i][j])}dfs(0,0,0n);
  return {out,count}}
 function decide(Gs,Cs,target){let n=Gs[0].n,offset=xor(Cs.map(c=>c.offset)),z=target^offset,T=range(n).filter(j=>(z&bit(j))!==0n);
  if(z>>BigInt(n))return {sat:false,affine:true};
  let slots=Gs.flatMap((g,i)=>range(g.k).map(j=>[i,j]));
  let adj=range(n).map(j=>range(slots.length).filter(s=>{let [i,a]=slots[s];return Gs[i].A[a][j]}));
  // complete affine hull in coordinate dictionary: every nonloop singleton attainable
  if(T.some(j=>!adj[j].length))return {sat:false,affine:true};
  let R=match(T,adj,slots.length);
  if(R.rank!==T.length){let X=new Set(R.failed),Y=new Set(),todo=[...X];
   while(todo.length){let j=todo.pop();for(let s of adj[j])if(!Y.has(s)){Y.add(s);let w=R.own[s];assert(w>=0,"augmenting path remains");if(!X.has(w)){X.add(w);todo.push(w)}}}
   assert(Y.size<X.size,"Hall deficiency");return {sat:false,hall:[X.size,Y.size]}}
  let J=Gs.map(()=>[]);R.own.forEach((j,s)=>{if(j>=0)J[slots[s][0]].push(j)});
  assert(xor(Gs.map((g,i)=>lift(g,Cs[i],J[i])))===target,"global source lift");return {sat:true}}
 let stats={seed:"0x201303",networks:120,factors:0,reference_matchings:0,local_support_checks:0,targets:0,sat:0,unsat:0,hall:0,affine_reject:0,source_lifts:0,scaling:[],bad_controls:{}};
 for(let t=0;t<stats.networks;t++){let n=2+rng(3),Gs=range(2+rng(2)).map(()=>make(n,1+rng(3))),Cs=Gs.map(certify);assert(Cs.every(Boolean),"certification");
  let support=new Set([0n]);
  for(let i=0;i<Gs.length;i++){let g=Gs[i],c=Cs[i],r=reference(g);stats.factors++;stats.reference_matchings+=r.count;
   for(let z=0;z<1<<n;z++){let J=range(n).filter(j=>z&(1<<j));let feasible=match(J,c.adj,g.k).rank===J.length;assert(feasible===r.out.has(c.offset^BigInt(z)),"local support");stats.local_support_checks++}
   support=new Set([...support].flatMap(x=>[...r.out].map(y=>x^y)))}
  for(let z=0;z<1<<n;z++){let target=BigInt(z),r=decide(Gs,Cs,target);assert(r.sat===support.has(target),"global support");stats.targets++;
   if(r.sat){stats.sat++;stats.source_lifts+=Gs.length}else {stats.unsat++;if(r.hall)stats.hall++;if(r.affine)stats.affine_reject++}}}
 for(let n of [9,17,33,65,129]){let k=(n-1)/2,Gs=[make(n,k,true),make(n,k,true)],Cs=Gs.map(certify),offset=xor(Cs.map(c=>c.offset)),all=bit(n)-1n;assert(Cs.every(Boolean),"scale cert");
  let a=decide(Gs,Cs,offset^all),b=decide(Gs,Cs,offset^(all^1n));assert(!a.sat&&b.sat,"scale");
  stats.scaling.push({n,active_slots:2*k,vertices:4*(n+k),edges:2*(n+k)**2,full_target:a,one_bit_deleted:b});}
 // necessity counterexamples in the actual graph, with zero gauge
 let bad={n:1,k:1,m:2,A:[[true,false],[true,true]],g:[[1n,null],[0n,0n]]};
 assert(!certify(bad)&&reference(bad).out.has(1n)&&!reference(bad).out.has(0n),"dummy counterexample");stats.bad_controls.dummy_rank="rejected; only nonempty selection attainable";
 bad={n:1,k:1,m:2,A:[[true,true],[true,false]],g:[[1n,0n],[0n,null]]};
 assert(!certify(bad)&&reference(bad).out.has(0n)&&!reference(bad).out.has(1n),"slack counterexample");stats.bad_controls.slack="rejected; selectable element cannot be completed";
 stats.edge_scans=scans;stats.successful_augmentations=augment;stats.disagreements=0;return stats
}
console.log(JSON.stringify(run(),null,2));
