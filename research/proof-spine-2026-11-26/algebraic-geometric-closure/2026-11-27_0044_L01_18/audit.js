function check(x,m="assertion"){if(!x)throw Error(m)}

function fano(b){const L=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];return {m:7*b,T:Array.from({length:b},(_,j)=>L.map(t=>t.map(x=>x+7*j))).flat()}}

function make({m,T}){
  const leaves=Array.from({length:m},()=>[]),groups=T.map((t,j)=>t.map((e,k)=>{const id=m+3*j+k;leaves[e].push(id);return id}));
  const word=leaves.flatMap((L,e)=>[e,...L,e,...L.slice().reverse()]),s=word.length;
  const pos=Array.from({length:m+3*T.length},()=>[]);word.forEach((v,i)=>pos[v].push(i));check(pos.every(p=>p.length===2));
  const C=Array.from({length:s},(_,i)=>(i+1)%s),p=C.slice(),g=Array.from({length:s},(_,i)=>i),h=g.slice(),owner=g.map(()=>-1),partner=g.slice();
  for(let e=0;e<m;e++){const [a,b]=pos[e];[p[a],p[b]]=[p[b],p[a]]}
  groups.forEach((L,j)=>{const E=L.flatMap(l=>pos[l]);for(const l of L){const [a,b]=pos[l];partner[a]=b;partner[b]=a}E.forEach((i,k)=>{g[i]=E[(k+1)%E.length];owner[i]=j});for(const i of E)h[i]=partner[g[i]]});
  const n=3*s,E=[],rows=[];
  for(let i=0;i<s;i++){let u=s+2*i,v=u+1;E.push([i,u],[u,v],[v,p[i]]);if(owner[i]>=0)E.push([g[i],v],[v,u],[u,p[h[i]]]);rows.push({i,u,v})}
  const adj=Array.from({length:n},()=>[]);for(const [a,b] of E)adj[a].push(b);check(adj.every(L=>new Set(L).size===L.length));
  const tables=rows.map(({i,u,v})=>{let out=[];for(const [a,b] of [[u,v],[v,u]])if(adj[a].includes(b))for(let x=0;x<s;x++)if(adj[x].includes(a))for(let y of adj[b])if(y<s)out.push({x,y,path:[a,b]});return out});
  for(let i=0;i<s;i++){check(tables[i].length===(owner[i]<0?1:2));check(tables[i].some(t=>t.x===i&&t.y===p[i]));if(owner[i]>=0)check(tables[i].some(t=>t.x===g[i]&&t.y===p[h[i]]))}
  // recover group equality from incoming occupancy on the g permutation; groups are six positions.
  const seen=new Set(),acquired=[];for(let i=0;i<s;i++)if(owner[i]>=0&&!seen.has(i)){let j=i,L=[];do{seen.add(j);L.push(j);j=g[j]}while(j!==i);check(L.length===6&&L.every(x=>owner[x]===owner[i]));acquired.push(L)}
  check(acquired.length===T.length);
  return {m,T,s,n,E,adj,tables,word,pos,groups,p,g,h,owner,partner,acquired};
}

function cycles(P){let count=0,seen=new Set();for(let i=0;i<P.length;i++)if(!seen.has(i)){count++;let j=i;while(!seen.has(j)){seen.add(j);j=P[j]}check(j===i)}return count}

function lift(G,x){
  const P=Array(G.n).fill(-1),compressed=Array(G.s).fill(-1);
  for(let i=0;i<G.s;i++){const active=G.owner[i]>=0&&x[G.owner[i]],a=active?G.g[i]:i,b=active?G.p[G.h[i]]:G.p[i],t=G.tables[i].find(t=>t.x===a&&t.y===b);check(t&&P[a]===-1);const [u,v]=t.path;P[a]=u;P[u]=v;P[v]=b;compressed[a]=b}
  check(new Set(P).size===G.n&&P.every((v,i)=>G.adj[i].includes(v)));check(compressed.every((v,i)=>v===G.p[G.owner[i]>=0&&x[G.owner[i]]?G.partner[i]:i]));
  return {P,compressed}
}

function defect(G,x){let d=Array(G.m).fill(0);G.T.forEach((t,j)=>{if(x[j])for(let e of t)d[e]++});return {d,loss:d.reduce((a,b)=>a+Math.abs(b-1),0)}}

function rank(A){A=A.map(r=>r.slice());let r=0;for(let j=0;j<(A[0]?.length||0)&&r<A.length;j++){let k=r;while(k<A.length&&!A[k][j])k++;if(k===A.length)continue;[A[r],A[k]]=[A[k],A[r]];for(let i=r+1;i<A.length;i++)if(A[i][j])for(let l=j;l<A[i].length;l++)A[i][l]^=A[r][l];r++}return r}

function interlace(G,x){const ids=[...Array.from({length:G.m},(_,i)=>i),...G.groups.flatMap((L,i)=>x[i]?L:[])];const A=ids.map(i=>ids.map(j=>{if(i===j)return 0;let [a,b]=G.pos[i],[c,d]=G.pos[j];return Number((a<c&&c<b)!==(a<d&&d<b))}));return ids.length-rank(A)}

function stronglyConnected(G,E){let A=Array.from({length:G.n},()=>[]),B=A.map(()=>[]);for(const [a,b] of E){A[a].push(b);B[b].push(a)}return [A,B].every(L=>{let seen=new Set([0]),q=[0];while(q.length)for(const j of L[q.pop()])if(!seen.has(j)){seen.add(j);q.push(j)}return seen.size===G.n})}

function local(){
 const G=make(fano(1)),hist={},oddWeights={},oddMasks=[],all=[];
 for(let b=0;b<128;b++){const x=Array.from({length:7},(_,i)=>(b>>i)&1),d=defect(G,x),L=lift(G,x),c=cycles(L.P);check(c===cycles(L.compressed)&&c===1+d.loss&&c===1+interlace(G,x));hist[c]=(hist[c]||0)+1;if(d.d.every(a=>a%2===1)){let w=x.reduce((a,b)=>a+b,0);oddWeights[w]=(oddWeights[w]||0)+1;oddMasks.push(b)}all.push({mask:b,cycles:c,defect:d.loss,occupancy:d.d})}
 check(Math.min(...Object.keys(hist).map(Number))===3);check(oddMasks.length===8&&oddWeights[3]===7&&oddWeights[7]===1);
 for(let i=0;i<7;i++)check(oddMasks.some(b=>b>>i&1)&&oddMasks.some(b=>!(b>>i&1)));
 const mat=Array.from({length:7},(_,e)=>G.T.map(t=>Number(t.includes(e))));check(rank(mat)===4);
 // minimal actual YES falsifier, one triple selected covers all three elements
 const Y=make({m:3,T:[[0,1,2]]});check(cycles(lift(Y,[1]).P)===1&&interlace(Y,[1])===0&&cycles(lift(Y,[0]).P)>1);
 return {hist,oddWeights,oddMasks,all,rank:4,control:"one triple: selection 1 yields actual native single cycle"}
}

function run(){
 const base=local(),scale=[];
 for(const b of [3,6,12,24,48]){
  const G=make(fano(b)),t=G.T.length,seen=new Set();let tests=0;
  const add=x=>{check(x.reduce((a,b)=>a+b,0)%2===G.m%2);const L=lift(G,x),D=defect(G,x);check(cycles(L.P)===1+D.loss);for(let i=0;i<G.n;i++)seen.add(i+","+L.P[i]);tests++};
  // target parity witnesses cover every arc: start from all ones; toggle each bit together with a distinct bit
  const x=Array(t).fill(1);add(x);for(let i=0;i<t;i++){const y=x.slice();y[i]=0;y[(i+1)%t]=0;add(y)}
  check(G.E.every(([a,c])=>seen.has(a+","+c)));check(stronglyConnected(G,G.E));
  // factor recovered from actual incidence of element rows and phase columns
  const by=Array.from({length:G.m},()=>[]);G.T.forEach((L,i)=>L.forEach(e=>by[e].push(i)));let S=new Set(),components=[];
  for(let i=0;i<t;i++)if(!S.has(i)){let q=[i],L=[];S.add(i);while(q.length){const j=q.pop();L.push(j);for(let e of G.T[j])for(let k of by[e])if(!S.has(k)){S.add(k);q.push(k)}}components.push(L)}
  check(components.length===b&&components.every(L=>L.length===7));let min=0,terms=0,dim=0;
  for(const L of components){const E=[...new Set(L.flatMap(j=>G.T[j]))],M=E.map(e=>L.map(j=>Number(G.T[j].includes(e))));let r=rank(M),best=Infinity,count=0; // enumerate local affine candidates by basis via direct 128-word reference, charge all probes
   for(let k=0;k<(1<<L.length);k++){terms++;let y=L.map((_,i)=>(k>>i)&1);if(M.every(row=>row.reduce((a,v,i)=>a^(v&y[i]),0)===1)){count++;best=Math.min(best,y.reduce((a,v)=>a+v,0))}}
   check(count===2**(L.length-r)&&best===3);min+=best;dim+=L.length-r;
  }
  check(min>G.m/3&&G.m%3===0);
  scale.push({blocks:b,n:G.n,s:G.s,arcs:G.E.length,inputBits:G.n*(G.n-1),phase:t,parityCompatible:(2n**BigInt(t-1)).toString(),oddOccupancy:(2n**BigInt(dim)).toString(),oddMinWeight:min,requiredWeight:G.m/3,components:components.length,chargedLocalWords:terms,allArcsTargetSupported:true,stronglyConnected:true,nativeWitnessProbes:tests,minCycles:1+2*b});
 }
 return {base,scale,execution:"serial, fixed local cap 128; no general delta parity, exact-cover solver or Lean build"};
}
console.log(JSON.stringify(run(),null,2));
