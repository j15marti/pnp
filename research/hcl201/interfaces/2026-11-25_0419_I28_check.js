function run(){
let checks=0, visits=0, queries=0, pins=0, scans=0; const ok=(v)=>{checks++;if(!v)throw Error("check "+checks)},par=(x)=>{let p=0;while(x){p^=x&1;x>>>=1}return p};
function project(raw, nc, rhs){
  let ts=raw.map(t=>{let ids=[...new Set(t.islands)],map=new Map();for(let w of t.rows){let y=0;for(let k=0;k<t.islands.length;k++)y^=((w>>k)&1)<<ids.indexOf(t.islands[k]);if(!map.has(y))map.set(y,w)}return {ids,map}});
  return {ts,nc,rhs};
}
function compile(p){
  let adj=[], edges=[],nv=()=>{adj.push([]);return adj.length-1},edge=(u,v)=>{ok(u!==v);adj[u].push(v);adj[v].push(u);edges.push([u,v])};
  if(p.ts.some(t=>!t.map.size))return null;
  let ports=Array.from({length:p.nc},()=>[]),data=[],pad=[];
  for(let t of p.ts){
    let d=t.ids.length;ok(d<=2);let a=[...t.map.keys()][0], aa=a|(par(a)<<d), ps=Array.from({length:d+1},nv);
    for(let y of t.map.keys()){let z=(y|(par(y)<<d))^aa;ok(par(z)===0);if(z){let js=ps.filter((_,i)=>(z>>i)&1);ok(js.length===2);edge(...js)}}
    for(let i=0;i<d;i++)ports[t.ids[i]].push({u:ps[i],a:(a>>i)&1});
    let r=nv();edge(ps[d],r);pad.push(r);data.push({ps,a});
  }
  for(let c=0;c<p.nc;c++){
    let q=ports[c],b=p.rhs[c];if(!q.length){if(b)return null;continue}
    let pp=q.map(nv);for(let i=0;i<pp.length;i++)for(let j=0;j<i;j++)edge(pp[i],pp[j]);
    q.forEach(({u,a},i)=>{if(a===(i===0?b:0))edge(u,pp[i]);else{let h=nv();edge(u,h);edge(h,pp[i])}})
  }
  if(adj.length%2)pad.push(nv());for(let i=0;i<pad.length;i++)for(let j=0;j<i;j++)edge(pad[i],pad[j]);
  return {adj,edges,data};
}
function match(g){queries++;if(!g)return null;let n=g.adj.length,memo=new Set(),mate=Array(n).fill(-1);
  function rec(s){visits++;if(s===0n)return true;if(memo.has(s))return false;let u=-1,best=null;for(let i=0;i<n;i++)if((s>>BigInt(i))&1n){let a=g.adj[i].filter(j=>(s>>BigInt(j))&1n);if(best===null||a.length<best.length){u=i;best=a;if(!a.length)break}}for(let v of best){mate[u]=v;mate[v]=u;if(rec(s^(1n<<BigInt(u))^(1n<<BigInt(v))))return true;mate[u]=mate[v]=-1}memo.add(s);return false}
  if(!rec((1n<<BigInt(n))-1n))return null;for(let i=0;i<n;i++)ok(mate[mate[i]]===i&&g.adj[i].includes(mate[i]));return mate;
}
function solve(p){let g=compile(p),m=match(g);if(!m)return null;let out=g.data.map(({ps,a},i)=>{let y=a;for(let j=0;j<ps.length-1;j++)if(ps.includes(m[ps[j]]))y^=1<<j;ok(p.ts[i].map.has(y));return y});let v=Array(p.nc).fill(0);out.forEach((y,i)=>p.ts[i].ids.forEach((c,j)=>v[c]^=(y>>j)&1));ok(v.every((b,i)=>b===p.rhs[i]));return out}
function ref(raw,nc,rhs){let out=[],v=Array(nc).fill(0),word=[];function go(i){if(i===raw.length){if(v.every((b,j)=>b===rhs[j]))out.push(word.slice());return}let t=raw[i];for(let w of t.rows){word.push(w);t.islands.forEach((c,j)=>v[c]^=(w>>j)&1);go(i+1);t.islands.forEach((c,j)=>v[c]^=(w>>j)&1);word.pop()}}go(0);return out}
function close(raw,nc,rhs){
  // Necessary local affine/coordinate closure: empty tables and fixed incidence bits, and one-free-bit parity rows.
  raw=raw.map(t=>({islands:t.islands.slice(),rows:t.rows.slice()}));
  let changed=true;while(changed){changed=false;let inc=Array.from({length:nc},()=>[]);
    for(let i=0;i<raw.length;i++){let t=raw[i];if(!t.rows.length)return null;t.islands.forEach((c,j)=>inc[c].push([i,j]));}
    for(let c=0;c<nc;c++){scans++;let known=0,free=[];for(let [i,j] of inc[c]){let r=raw[i].rows,b=(r[0]>>j)&1;if(r.every(w=>((w>>j)&1)===b))known^=b;else free.push([i,j])}
      if(!free.length&&known!==rhs[c])return null;
      if(free.length===1){let [i,j]=free[0],r=raw[i].rows;raw[i].rows=r.filter(w=>((w>>j)&1)===(known^rhs[c]));if(raw[i].rows.length!==r.length){changed=true;pins++}}
    }
  }return raw;
}
function job(raw,nc,rhs,allRows=true){
  let expected=ref(raw,nc,rhs),closed=close(raw,nc,rhs);let p=closed&&project(closed,nc,rhs),got=p&&solve(p);ok(Boolean(got)===Boolean(expected.length));
  if(got){let lift=got.map((w,i)=>p.ts[i].map.get(w));ok(expected.some(a=>a.every((w,i)=>w===lift[i])));}
  if(allRows&&got){for(let i=0;i<closed.length;i++)for(let w of closed[i].rows){let probe=closed.map((t,j)=>({islands:t.islands,rows:i===j?[w]:t.rows}));let q=close(probe,nc,rhs);let yes=q&&solve(project(q,nc,rhs));ok(Boolean(yes)===expected.some(a=>a[i]===w));}}
  return {SAT:!!got,models:expected.length};
}
let cases=0,sat=0,unsat=0;function test(raw,nc,rhs){let a=job(raw,nc,rhs);cases++;if(a.SAT)sat++;else unsat++}
for(let mask=0;mask<16;mask++)for(let b=0;b<4;b++)test([{islands:[0,1],rows:[0,1,2,3].filter(w=>(mask>>w)&1)}],2,[b&1,b>>1]);
let seed=20261125;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>12)%n}
for(let trial=0;trial<160;trial++){let nc=1+rnd(3),raw=[];for(let i=0;i<1+rnd(4);i++){let a=rnd(nc),b=rnd(nc),k=1+rnd(3),islands=Array.from({length:k},()=>rnd(2)?a:b);let rows=Array.from({length:1<<k},(_,w)=>w).filter(()=>rnd(4)!==0);raw.push({islands,rows})}test(raw,nc,Array.from({length:nc},()=>rnd(2)))}
let peer=[];for(let m of [5,40])for(let mode of ["root","delete","flip"]){let raw=mode==="root"?[]:[{islands:[0,0,0],rows:mode==="delete"?[0,1,2,4,7]:[0,1,2,7]}];let a=job(raw,1,[mode==="root"?1:0]);ok(a.SAT===(mode!=="root"));peer.push({m,mode,boundary:mode==="root"?[]:m===5?[0,3,20]:[0,1560,38],...a})}
function exchange(R){let bad=[];for(let a of R)for(let b of R)for(let i=0;i<4;i++)if(((a^b)>>i)&1){let good=false;for(let j=0;j<4;j++)if(j!==i&&(((a^b)>>j)&1)&&R.includes(a^(1<<i)^(1<<j)))good=true;if(!good)bad.push([a,b,i])}return bad}
let barriers=[];for(let R of [[0,1,2,4,7],[0,1,2,7],[0,7]]){let L=R.map(x=>x|(par(x)<<3)),bad=exchange(L);ok(bad.length>0);barriers.push({R,L,firstFailure:bad[0]})}
return {cases,sat,unsat,peer,barriers,checks,matchingQueries:queries,recursiveMatchingNodes:visits,closureScans:scans,localPinEvents:pins,seed:20261125,limits:"Exponential small matching reference search, not blossom. BW22 immutable projected boundary charts only; upstream raw grouping, physical native and forest lifts not reexecuted. No full portfolio, formal kernel, or physical CM measurement."}
}
console.log(JSON.stringify(run(),null,2));
