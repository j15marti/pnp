function runDO03(){
  const stats={seed:20803,graphs:[],projectionChecks:0,projectedTargets:0,dpTransitions:0,affineRankChecks:0,guardRows:0,pairChecks:0,colorSearchNodes:0,neighborWitnessChecks:0,sourceLiftChecks:0,fano:[]};let rng=stats.seed;
  function rnd(){rng=(Math.imul(rng,1664525)+1013904223)>>>0;return rng}
  function ok(x,s){if(!x)throw Error(s)}
  function edges(n){let E=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)E.push([i,j]);return E}
  function myc(n,E){return [2*n+1,[...E,...E.flatMap(([u,v])=>[[u,n+v],[v,n+u]]),...Array.from({length:n},(_,i)=>[n+i,2*n])]]}
  function color(n,E){let adj=Array.from({length:n},()=>[]);for(const[u,v]of E){adj[u].push(v);adj[v].push(u)}let a=Array(n).fill(-1);
    function dfs(used,left){stats.colorSearchNodes++;if(!left)return true;let b=-1,bs=-1,bd=-1,bm=0;
      for(let i=0;i<n;i++)if(a[i]<0){let m=0;for(const j of adj[i])if(a[j]>=0)m|=1<<a[j];let s=0;for(let q=m;q;q&=q-1)s++;if(s>bs||s===bs&&adj[i].length>bd){b=i;bs=s;bd=adj[i].length;bm=m}}
      for(let c=0;c<Math.min(4,used+1);c++)if(!(bm&(1<<c))){a[b]=c;if(dfs(Math.max(used,c+1),left-1))return true;a[b]=-1}return false
    }return dfs(0,n)?a:null
  }
  function basis(vs){let B=new Map();for(let v of vs){while(v){let k=v.toString(2).length-1;if(B.has(k))v^=B.get(k);else{B.set(k,v);break}}}return B.size}
  function compile(n,E){let adj=Array.from({length:n},()=>[]);E.forEach(([u,v],i)=>{adj[u].push([v,i]);adj[v].push([u,i])});let par=Array(n).fill(-1),pe=Array(n).fill(-1),dep=Array(n).fill(0);par[0]=0;let q=[0];for(let j=0;j<q.length;j++)for(let [v,i]of adj[q[j]])if(par[v]<0){par[v]=q[j];pe[v]=i;dep[v]=dep[q[j]]+1;q.push(v)}ok(q.length===n,"connected");
    let tree=new Set(pe.filter(i=>i>=0)),C=E.map(()=>0n),b=0;
    E.forEach(([u0,v0],i)=>{if(tree.has(i))return;let u=u0,v=v0,bit=1n<<BigInt(b++);C[i]|=bit;while(u!==v){if(dep[u]>=dep[v]){C[pe[u]]|=bit;u=par[u]}else{C[pe[v]]|=bit;v=par[v]}}});
    let girth=Infinity;E.forEach(([u,v],i)=>{let d=Array(n).fill(-1),q=[u];d[u]=0;for(let j=0;j<q.length;j++)for(const[w,k]of adj[q[j]])if(k!==i&&d[w]<0){d[w]=d[q[j]]+1;q.push(w)}if(d[v]>=0)girth=Math.min(girth,d[v]+1)});
    return {C,b,girth,adj}
  }
  function syndrome(C,b,d){let z=0n;for(let i=0;i<d.length;i++){if(d[i]&1)z^=C[i];if(d[i]&2)z^=C[i]<<BigInt(b)}return z}
  function lift(n,E,C,b,d){if(syndrome(C,b,d))return null;let a=Array(n).fill(-1);a[0]=0;let q=[0];let adj=Array.from({length:n},()=>[]);E.forEach(([u,v],i)=>{adj[u].push([v,i]);adj[v].push([u,i])});for(let j=0;j<q.length;j++)for(const[v,i]of adj[q[j]]){let c=a[q[j]]^d[i];if(a[v]<0){a[v]=c;q.push(v)}else ok(a[v]===c,"bad lift")}ok(E.every(([u,v],i)=>(a[u]^a[v])===d[i]&&d[i]!==0),"lift verification");stats.sourceLiftChecks++;return a}
  function parity(a){let p=0;while(a){a&=a-1n;p^=1}return p}
  function randomBig(d){let v=0n;for(let i=0;i<d;i+=32)v|=BigInt(rnd())<<BigInt(i);return v&((1n<<BigInt(d))-1n)}
  function exactProject(C,b,pins,R){let projected=C.map(c=>{let x=0,y=0;for(let j=0;j<R.length;j++){x|=parity(R[j]&c)<<j;y|=parity(R[j]&(c<<BigInt(b)))<<j}return [x,y,x^y]});let S=new Set([0]);for(let i=0;i<C.length;i++){let T=new Set();let tags=pins.has(i)?[projected[i][pins.get(i)-1]]:projected[i];for(const x of S)for(const y of tags){T.add(x^y);stats.dpTransitions++}S=T}stats.projectionChecks++;stats.projectedTargets+=1<<R.length;return S.size}
  function analyze(name,n,E,expect,tests){let c=compile(n,E),{C,b,girth:g}=c;let a=color(n,E);ok(!!a===expect,"color label "+name);if(a){let d=E.map(([u,v])=>a[u]^a[v]);ok(d.every(Boolean)&&!syndrome(C,b,d),"color syndrome");lift(n,E,C,b,d);for(let e=0;e<E.length;e++)for(let t=1;t<=3;t++){let h=[1,2,3].find(z=>z!==d[e]);let k=[1,2,3].find(z=>z!==t);let map=[];map[0]=0;map[d[e]]=t;map[h]=k;map[d[e]^h]=t^k;let w=a.map(x=>map[x]);ok(E.every(([u,v])=>w[u]!==w[v])&&(w[E[e][0]]^w[E[e][1]])===t,"neighbor row");stats.neighborWitnessChecks++}}
    let distinct=new Set(C.map(String)).size===E.length&&C.every(Boolean);if(distinct){for(let i=0;i<C.length;i++)for(let j=i+1;j<C.length;j++){ok(C[i]!==C[j]&&C[i]&&C[j],"pair");stats.pairChecks++}}
    let maxr=0;for(let t=0;t<tests;t++){let p=t%(g-1),pins=new Map();while(pins.size<p)pins.set(rnd()%E.length,1+rnd()%3);let d=2*b,r=Math.min(d,Math.floor(Math.log2(3**(g-p)-1)));if(!r)continue;let R=[];while(R.length<r){let v=randomBig(d);if(basis([...R,v])>R.length)R.push(v)}ok(exactProject(C,b,pins,R)===(1<<r),"projection fails "+name);maxr=Math.max(maxr,r);
      let unp=C.flatMap((z,i)=>pins.has(i)?[]:[z,z<<BigInt(b)]);ok(basis(unp)===d,"affine closure");stats.affineRankChecks++;
      for(let i=0;i<C.length;i++)if(!pins.has(i)){let v=C.flatMap((z,j)=>pins.has(j)||j===i?[]:[z,z<<BigInt(b)]);ok(basis(v)===d,"row support");stats.affineRankChecks++;stats.guardRows+=3}
    }
    stats.graphs.push({name,n,m:E.length,b,girth:g,sat:expect,distinct,maxr,projectionTrials:tests});return a
  }
  let K=edges(5);analyze("K5",5,K,false,96);for(let i=0;i<K.length;i++)analyze("K5-delete-"+i,5,K.filter((_,j)=>i!==j),true,12);
  let E5=Array.from({length:5},(_,i)=>[i,(i+1)%5]);let [n1,E1]=myc(5,E5),[n2,E2]=myc(n1,E1);
  // Minimize the 5-chromatic triangle-free graph by actual edge deletion tests.
  let H=E2.slice();ok(!color(n2,H),"Mycielski root");for(let i=H.length-1;i>=0;i--){let J=H.filter((_,j)=>i!==j);if(!color(n2,J))H=J}
  let used=[...new Set(H.flat())].sort((a,b)=>a-b);H=H.map(([u,v])=>[used.indexOf(u),used.indexOf(v)]);let n=used.length;
  analyze("Mycielski-critical",n,H,false,96);for(let i=0;i<H.length;i++)analyze("Mycielski-delete-"+i,n,H.filter((_,j)=>i!==j),true,3);
  // Exact small pair-subspace control in F2^4: enumerate every line and plane.
  function fibers(A,H){let M=new Map();for(let x of A){let k=Math.min(...H.map(h=>x^h));M.set(k,(M.get(k)||0)+1)}return Math.min(...M.values())}
  let spaces=new Map();for(let x=1;x<16;x++){let h=[0,x];spaces.set(h.join(","),h);for(let y=x+1;y<16;y++){let h=[0,x,y,x^y].sort((a,b)=>a-b);spaces.set(h.join(","),h)}}
  let checks=0;for(let h of spaces.values()){ok(fibers([1,2,3],h)+fibers([4,8,12],h)<=h.length,"disjoint saturation");checks++}ok(fibers([1,2,3],[0,1,2,3])*2>4,"equal plane positive control");stats.pairSubspaceChecks=checks;
  // Fano shared benchmark: paired monotone OR / negative OR; not graph-compiled.
  let F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
  for(let del=-1;del<14;del++){let count=0;for(let x=0;x<128;x++)if(F.every((e,i)=>{let s=e.reduce((a,v)=>a+((x>>v)&1),0);return (del===2*i||s>0)&&(del===2*i+1||s<3)}))count++;ok(count===(del<0?0:5),"Fano");stats.fano.push(count)}
  stats.criticalEdges=H;stats.graphCount=stats.graphs.length;return stats
}
console.log(JSON.stringify(runDO03(), null, 2));
