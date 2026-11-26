function sccAudit(){
 const stats={cases:0,assertions:0,solverCalls:0,transitions:0,flexiblePairs:0,unsat:0};
 const check=b=>{if(!b)throw Error("SCC assertion");stats.assertions++};
 function solve(n,clauses){stats.solverCalls++;let adj=Array.from({length:2*n},()=>[]),rev=adj.map(()=>[]);for(let [a,b] of clauses){adj[a^1].push(b);adj[b^1].push(a);rev[b].push(a^1);rev[a].push(b^1)}let seen=adj.map(()=>false),order=[];function dfs(v){if(seen[v])return;seen[v]=true;for(let w of adj[v])dfs(w);order.push(v)}for(let i=0;i<2*n;i++)dfs(i);let c=adj.map(()=>-1),q=0;function walk(v){if(c[v]>=0)return;c[v]=q;for(let w of rev[v])walk(w)}for(let v of order.reverse())if(c[v]<0){walk(v);q++}for(let i=0;i<n;i++)if(c[2*i]===c[2*i+1])return null;let x=Array.from({length:n},(_,i)=>+(c[2*i]>c[2*i+1]));return {x,c,adj,q}}
 const ok=(cs,x)=>cs.every(([a,b])=>[a,b].some(l=>x[l>>1]===1-(l&1)));
 const syn=(x,w)=>x.reduce((a,b,i)=>a^(b?w[i]:0),0);
 const span=vs=>{let S=new Set([0]);for(let v of vs)S=new Set([...S].flatMap(s=>[s,s^v]));return S};
 function terminal(n,cs,w){let sol=solve(n,cs);if(!sol)return null;let {x,c,adj,q}=sol;check(ok(cs,x));let groups=Array.from({length:q},()=>[]);for(let l=0;l<2*n;l++)groups[c[l]].push(l);let seen=new Set(),dirs=[],paths=[];
 for(let i=0;i<n;i++){let j=c[2*i];if(seen.has(j))continue;let h=c[2*i+1];seen.add(j);seen.add(h);let flip=2*i+x[i];let alt=solve(n,[...cs,[flip,flip]]);if(!alt)continue;stats.flexiblePairs++;let t=x.slice(),target=alt.x,delta=groups[j].reduce((s,l)=>s^w[l>>1],0);dirs.push(delta);
 // move along SCC flips from original witness to alternative
 let path=[t.slice()],seenDelta=false;while(t.some((b,k)=>b!==target[k])){
  let C=groups.find(g=>g.every(l=>target[l>>1]===1-(l&1)&&t[l>>1]!==1-(l&1))&&g.every(l=>adj[l].every(v=>c[v]===c[l]||t[v>>1]===1-(v&1))));
  check(!!C);let before=syn(t,w);for(let l of C)t[l>>1]=1-(l&1);check(ok(cs,t));let d=before^syn(t,w);if(c[C[0]]===j||c[C[0]]===h){check(d===delta);seenDelta=true}path.push(t.slice());stats.transitions++;
 }check(seenDelta);paths.push(path);}
 return {base:syn(x,w),hull:span(dirs),witnesses:paths.flat().concat([x])}}
 let seed=6112608;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 for(let q=0;q<600;q++){let n=2+rnd(7),cs=Array.from({length:rnd(3*n+1)},()=>[rnd(2*n),rnd(2*n)]),w=Array.from({length:n},()=>rnd(16));let actual=new Set(),valid=[];for(let t=0;t<1<<n;t++){let x=Array.from({length:n},(_,i)=>(t>>i)&1);if(ok(cs,x)){actual.add(syn(x,w));valid.push(x)}}let got=terminal(n,cs,w);stats.cases++;check(Boolean(got)===Boolean(actual.size));if(!got){stats.unsat++;continue}let exp=span([...actual].map(v=>v^got.base));check(exp.size===got.hull.size&&[...exp].every(v=>got.hull.has(v)));for(let j=0;j<4;j++){let a=new Set([...actual].map(v=>(v>>j)&1)),b=new Set(got.witnesses.map(x=>(syn(x,w)>>j)&1));check(a.size===b.size&&[...a].every(v=>b.has(v)))}}
 return stats;
}
console.log(JSON.stringify(sccAudit(),null,2));
