function run(){
let seed=11241140;const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n};
let R={seed:11241140,instances:0,positive:0,zero:0,sourceWords:0,rawWords:0,basisWitnesses:0,cutsetWords:0,closureScans:0,localTableRows:0,forestProducts:0,clauseDeletions:0,splitControls:0,maxLocal:0,maxJoint:0,maxBeta:0,scale:[]};
function ck(b){if(!b)throw Error("assertion")}
function source(F){let V=[...new Set(F.flat().map(Math.abs))];let count=0;for(let x=0;x<2**V.length;x++){R.sourceWords++;if(F.every(C=>C.some(l=>((x>>V.indexOf(Math.abs(l)))&1)===(l>0?1:0))))count++}return count}
function compile(F){
 let next=Math.max(0,...F.flat().map(Math.abs)), occ=new Map(), G=F.map(C=>C.slice());
 for(let i=0;i<G.length;i++)for(let j=0;j<G[i].length;j++){let v=Math.abs(G[i][j]);if(!occ.has(v))occ.set(v,[]);occ.get(v).push([i,j])}
 for(const [v,a] of occ)if(a.length>3){R.splitControls++;let vs=a.map(()=>++next);a.forEach(([i,j],k)=>G[i][j]=Math.sign(G[i][j])*vs[k]);vs.forEach((u,k)=>G.push([-u,vs[(k+1)%vs.length]]))}
 let groups=[[],[]], copies=new Map(), n=0;
 function add(side,vars,rows,max){groups[side].push({vars,rows,max})}
 for(const C of G){let ids=C.map(l=>{let i=n++,v=Math.abs(l);if(!copies.has(v))copies.set(v,[]);copies.get(v).push(i);return i});let rows=[];
  for(let mask=1;mask<2**C.length;mask++){let a=[],b=0;for(let j=0;j<C.length;j++)if(mask>>j&1){a.push(ids[j]);b^=+(C[j]<0)}rows.push([a,b],[a,b])}
  add(0,ids,rows,2**C.length)
 }
 for(const a of copies.values()){let rows=[];for(let j=1;j<a.length;j++)rows.push([[a[0],a[j]],1],[[a[0],a[j]],1]);add(1,a,rows,2*(a.length-1))}
 for(let s=0;s<2;s++)for(let k=0;k<2;k++){let i=n++;add(s,[i],[[[i],0],[[i],0]],2);add(1-s,[i],[],0)}
 let H=groups.map(g=>g.reduce((a,b)=>a+b.max,0)-2);
 let K=groups.map(g=>g.reduce((a,b)=>a+b.rows.length,0));
 ck(H.every((h,s)=>h>=0&&h<=K[s])); 
 return {groups,n,H,K}
}
function score(g,get){let s=0;for(const [a,b] of g.rows){let y=b;for(const i of a)y^=get(i);s+=y}return s}
function bad(P,s,get){let w=P.groups[s].reduce((a,g)=>a+score(g,get),0);return w>P.H[s]||w>2*P.K[s]-P.H[s]}
function count(P){
 const nodes=P.groups.flat(), a=P.groups[0].length, edges=Array.from({length:P.n},()=>[]);
 nodes.forEach((g,i)=>g.vars.forEach(v=>edges[v].push(i)));ck(edges.every(e=>e.length===2&&e[0]<a&&e[1]>=a));
 const parent=nodes.map((_,i)=>i);function find(i){while(parent[i]!==i)i=parent[i];return i}
 let adj=nodes.map(()=>[]),cut=[],size=nodes.map(()=>0);
 edges.forEach(([u,v],i)=>{let x=find(u),y=find(v);if(x===y)cut.push(i);else{parent[x]=y;adj[u].push([v,i]);adj[v].push([u,i])}});
 nodes.forEach((g,i)=>size[find(i)]+=g.vars.length);R.maxJoint=Math.max(R.maxJoint,...size.map(s=>s/2));R.maxBeta=Math.max(R.maxBeta,cut.length);ck(cut.length<22);
 let tables=nodes.map(g=>{R.maxLocal=Math.max(R.maxLocal,g.vars.length);let t=[];for(let j=0;j<2**g.vars.length;j++){R.localTableRows++;if(score(g,v=>(j>>g.vars.indexOf(v))&1)===g.max)t.push(g.vars.map((_,k)=>(j>>k)&1))}return t});
 function close(pin){let changed=true;while(changed){changed=false;for(let i=0;i<nodes.length;i++){R.closureScans++;let vs=nodes[i].vars,t=tables[i].filter(w=>vs.every((v,j)=>pin[v]===-1||pin[v]===w[j]));if(!t.length)return false;for(let j=0;j<vs.length;j++)if(pin[vs[j]]===-1&&t.every(w=>w[j]===t[0][j])){pin[vs[j]]=t[0][j];changed=true;break}if(changed)break}}return true}
 let root=Array(P.n).fill(-1);if(!close(root))return {value:0n,beta:cut.length};let active=cut.filter(v=>root[v]===-1);
 let total=0n;
 for(let z=0;z<2**active.length;z++){R.cutsetWords++;let pin=root.slice();active.forEach((v,j)=>pin[v]=z>>j&1);if(!close(pin))continue;
  let seen=new Set();function dfs(i,p){seen.add(i);let kids=adj[i].filter(([j])=>j!==p).map(([j,e])=>[e,dfs(j,i)]), pe=p<0?-1:adj[i].find(([j])=>j===p)[1],out=[0n,0n],vs=nodes[i].vars;
   for(const w of tables[i]){if(!vs.every((v,j)=>pin[v]===-1||pin[v]===w[j]))continue;let c=1n;for(const [e,t] of kids){R.forestProducts++;c*=t[w[vs.indexOf(e)]]}out[pe<0?0:w[vs.indexOf(pe)]]+=c}return out}
  let prod=1n;for(let i=0;i<nodes.length;i++)if(!seen.has(i))prod*=dfs(i,-1)[0];total+=prod
 }return {value:total,beta:cut.length}
}
function test(F,raw=true){let ref=source(F),P=compile(F);R.instances++;R[ref?"positive":"zero"]++;
 // Exact full affine hull of the LEGAL base, certified by zero and every unit vector.
 for(let v=-1;v<P.n;v++){let get=i=>+(i===v);ck(!bad(P,0,get)&&!bad(P,1,get));R.basisWitnesses++}
 let a=count(P);ck(a.value===BigInt(ref));
 if(raw&&P.n<=18){let both=0;for(let x=0;x<2**P.n;x++){R.rawWords++;let get=i=>(x>>i)&1;if(bad(P,0,get)&&bad(P,1,get))both++}ck(both===ref)}
 return {bits:P.n,beta:a.beta,count:ref}
}
for(let j=0;j<48;j++){let F=[];for(let k=0;k<3;k++){let v=[1,2,3,4];let l=[];for(let t=0;t<1+rand(3);t++){if(!v.length)break;let a=v.splice(rand(v.length),1)[0];l.push(rand(2)?a:-a)}F.push(l)}test(F)}
// Cycle-copy forced equivalence for a variable with >3 occurrences.
test([[1,2],[-1,3],[1,-2],[-1,-3],[1,4]],false);
for(let n=2;n<=9;n++){let F=[[1],...Array.from({length:n-1},(_,i)=>[-(i+1),i+2]),[-n]];let a=test(F);ck(a.count===0);for(let i=0;i<F.length;i++){let b=test(F.filter((_,j)=>i!==j));ck(b.count===1);R.clauseDeletions++}R.scale.push({n,...a,neighbors:F.length})}
// Reproduce MS11 exact five-event example by independent bit enumeration.
let counts=[],sets=[],feasible=[];function par(x){let a=0;while(x){a^=1;x&=x-1}return a}
for(let z=0;z<2;z++){let E=[[[4,0],[5,1]],[[5,1],[7,1^z]],[[6,0],[7,0]],[[6,z],[7,0]],[[6,1],[7,1^z]]];let s=E.map(e=>Array.from({length:8},(_,x)=>x).filter(x=>e.every(([m,b])=>par(x&m)===b)));sets.push(s.map(v=>v.reduce((a,x)=>a+(1<<x),0)));let sum=s.reduce((a,v)=>a+v.length,0);for(let i=1;i<s.length;i++)sum-=s[i].filter(x=>s[i-1].includes(x)).length;counts.push(sum);for(let x=0;x<8;x++)if(!s.some(v=>v.includes(x)))feasible.push(8*z+x)}
ck(counts.join()==="7,6"&&feasible.join()==="5,7,10,12,15");R.MS11={sets,treeNumerators:counts,feasible};
return R
}
console.log(JSON.stringify(run(),null,2));
