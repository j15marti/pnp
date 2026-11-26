function run(){
let assertions=0; const check=(x)=>{assertions++;if(!x)throw Error("assertion "+assertions)};const perms=(a)=>a.length?a.flatMap((x,i)=>perms(a.filter((_,j)=>i!==j)).map(p=>[x,...p])):[[]];
const cycle=p=>{let i=0,k=0;do{i=p[i];k++}while(i!==0&&k<=p.length);return k===p.length};
const graph=(n,M)=>{let v=n*(n+1),adj=Array.from({length:v},()=>[]),c=(j,i)=>n+j*n+i;for(let j=0;j<n;j++)for(let i=0;i<n;i++){adj[c(j,i)].push(c(j,(i+1)%n));adj[c(j,(i+n-1)%n)].push((i+1)%n);if(M[i][j])adj[i].push(c(j,i))}return adj};
const tour=(n,p)=>{let out=[];for(let i=0;i<n;i++){out.push(i);for(let k=0;k<n;k++)out.push(n+p[i]*n+(i+k)%n)}return out};
const valid=(a,p)=>p.length===a.length&&new Set(p).size===a.length&&p.every((x,i)=>a[x].includes(p[(i+1)%p.length]));
function countNative(adj){let ct=0;function dfs(path,seen){if(path.length===adj.length){if(adj[path[path.length-1]].includes(0))ct++;return}for(const x of adj[path[path.length-1]])if(!seen.has(x)){seen.add(x);path.push(x);dfs(path,seen);path.pop();seen.delete(x)}}dfs([0],new Set([0]));return ct}
let oracleCalls=0,merges=0,graphCases=0,pmCases=0,weightedChecks=0,forcedChecks=0;
function compile(n,ps){
 const suf=(a)=>ps.filter(p=>a.every((x,i)=>p[i]===x)).map(p=>p.slice(a.length).join(",")).sort().join("|");
 // Empty suffix is special: use count or explicit JSON representation.
 const lang=a=>{oracleCalls++;return JSON.stringify(ps.filter(p=>a.every((x,i)=>p[i]===x)).map(p=>p.slice(a.length).join(",")).sort())};
 if(!ps.length)return {levels:[],root:-1};
 let levels=[[{a:[],sig:lang([]),arcs:[]}]];
 for(let i=0;i<n;i++){let next=[];for(const node of levels[i]){const completions=ps.filter(p=>node.a.every((x,j)=>p[j]===x));for(let j=i;j<n;j++)for(let c=0;c<n;c++){const have=completions.some(p=>p[j]===c),all=completions.every(p=>p[j]===c);check(!all||have);forcedChecks++}for(let j=0;j<n;j++){let a=[...node.a,j],sig=lang(a);if(sig==="[]")continue;let k=next.findIndex(x=>x.sig===sig);if(k<0){k=next.length;next.push({a,sig,arcs:[]})}else merges++;node.arcs.push([j,k])}}levels.push(next)}
 return {levels,root:0}
}
function test(n,ps){
 let D=compile(n,ps);if(!ps.length){check(D.root===-1);return}
 // Independently reconstruct every root path, compare exact monomial IDs.
 let paths=[{a:[],k:0}];for(let i=0;i<n;i++)paths=paths.flatMap(({a,k})=>D.levels[i][k].arcs.map(([j,z])=>({a:[...a,j],k:z})));check(JSON.stringify(paths.map(x=>x.a.join(",")).sort())===JSON.stringify(ps.map(x=>x.join(",")).sort()));
 for(const p of [2,3,101]){const K=3*n,mod=x=>((x%p)+p)%p;let values=D.levels[n].map(()=>Array.from({length:K+1},(_,i)=>i===0?1:0));for(let i=n-1;i>=0;i--){values=D.levels[i].map(node=>{let a=Array(K+1).fill(0);for(const [j,k] of node.arcs){let w=(i+2*j)%4,x=(3*i+5*j+1)%p;for(let d=w;d<=K;d++)a[d]=mod(a[d]+x*values[k][d-w])}return a})}
 let ref=Array(K+1).fill(0);for(const a of ps){let w=a.reduce((s,j,i)=>s+(i+2*j)%4,0),x=a.reduce((s,j,i)=>mod(s*(3*i+5*j+1)),1);ref[w]=mod(ref[w]+x)}check(JSON.stringify(ref)===JSON.stringify(values[0]));weightedChecks++}
}
for(const n of [3,4]){const ps=perms(Array.from({length:n},(_,i)=>i)).filter(cycle),es=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(i!==j)es.push([i,j]);for(let m=0;m<2**es.length;m++){let a=Array.from({length:n},()=>Array(n).fill(false));es.forEach(([i,j],k)=>a[i][j]=!!(m>>k&1));test(n,ps.filter(p=>p.every((j,i)=>a[i][j])));graphCases++}}
for(const n of [2,3]){const all=perms(Array.from({length:n},(_,i)=>i));for(let m=0;m<2**(n*n);m++){let M=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>!!(m>>(i*n+j)&1)));let ps=all.filter(p=>p.every((j,i)=>M[i][j]));test(n,ps);let a=graph(n,M);check(countNative(a)===ps.length);for(let p of ps)check(valid(a,tour(n,p)));pmCases++}}
const binom=(n,k)=>{let v=1n;for(let i=1;i<=k;i++)v=v*BigInt(n-i+1)/BigInt(i);return v};let adaptive=[];for(const n of [4,6,8,10,12,16]){let k=n/2,sets=new Set(),a=graph(n,Array.from({length:n},()=>Array(n).fill(1)));let seen=0;for(let mask=0;mask<2**n;mask++){let S=Array.from({length:n},(_,i)=>i).filter(i=>mask>>i&1);if(S.length!==k)continue;let rows=Array.from({length:n},(_,i)=>i),p=Array(n).fill(-1),cols=[...S,...Array.from({length:n},(_,i)=>i).filter(i=>!(mask>>i&1))],prefix=[];for(let t=0;t<n;t++){let r=rows.splice((prefix.reduce((s,j)=>s+j,0)+t)%rows.length,1)[0];p[r]=cols[t];prefix.push(cols[t]);if(t===k-1)sets.add(prefix.slice().sort((x,y)=>x-y).join(","))}check(valid(a,tour(n,p)));seen++}check(BigInt(sets.size)===binom(n,k));adaptive.push({n,v:n*(n+1),midWidth:sets.size,lifts:seen})}
let pairs=[];for(let n of [4,8,16,32,64]){let M=Array.from({length:n},(_,i)=>Array.from({length:n},(_,j)=>i===j||(i<n-1&&i%2===0&&j===i+1)||(i<n-1&&i%2===1&&j===i-1))); // remove offdiag at final row and column, force final identity
for(let i=0;i<n-1;i++)M[i][n-1]=0;for(let j=0;j<n-1;j++)M[n-1][j]=0;
let p=Array.from({length:n},(_,i)=>i);check(valid(graph(n,M),tour(n,p)));M[n-1][n-1]=0;let a=graph(n,M);check(a[n-1].length===0);pairs.push({n,v:a.length,oneDeletionNo:true})}
return {assertions,graphCases,pmCases,weightedChecks,forcedChecks,oracleCalls,merges,adaptive,pairs,limits:"Reference suffix lists from exhaustive normalized permutation enumeration; not a general HC decider or NP reduction implementation. Weighted evaluations only, exact path identities checked. Adaptive test one row policy; all-policy proof symbolic. Large NO via empty row."}
}
console.log(JSON.stringify(run(),null,2));
