// Node.js, deterministic seed; no dependencies.
function experiment(){
let seed=91273,checks=0;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n};
const xor=a=>a.reduce((x,y)=>x^y,0n),uniq=a=>[...new Set(a)],assert=x=>{checks++;if(!x)throw Error("check "+checks)};
function basis(a){let b=[];for(let x of a){for(const y of b)if((x^y)<x)x^=y;if(x){b.push(x);b.sort((x,y)=>x>y?-1:x<y?1:0)}}return b}
const red=(x,b)=>{for(const y of b)if((x^y)<x)x^=y;return x};
const dirs=f=>f.rows.map(x=>x^f.rows[0]),span=fs=>basis(fs.flatMap(dirs));
function exact(fs,t){let s=new Map([[0n,[]]]);for(const f of fs){let q=new Map;for(const [a,w] of s)for(const b of f.rows)if(!q.has(a^b))q.set(a^b,[...w,b]);s=q}return s.get(t)??null}
function* combos(n,k,s=0,p=[]){if(!k){yield p;return}for(let i=s;i<=n-k;i++)yield* combos(n,k-1,i+1,[...p,i])}
function solve(src,t){
 let fs=src.map((rows,id)=>({id,rows:uniq(rows)})),orig=t,log=[],stats={closures:0,deletions:0,probes:0,ternary:0,pair:0,affine:0,archiveRows:0};
 function close(){while(true){stats.closures++;if(fs.some(f=>!f.rows.length))return false;if(!fs.length)return t===0n;
 let change=false;for(let i=0;i<fs.length&&!change;i++){let others=fs.filter((_,j)=>i!==j),a=xor(others.map(f=>f.rows[0])),b=span(others);for(let j=0;j<fs[i].rows.length;j++)if(red(t^a^fs[i].rows[j],b)!==0n){fs[i].rows.splice(j,1);stats.deletions++;change=true;break}}if(!change)return true}}
 for(;;){
 if(!close())return {label:"UNSAT",stats};if(!fs.length)break;
 let ids=null,kind="";
 for(let i=0;i<fs.length;i++)if(fs[i].rows.length===2**span([fs[i]]).length){ids=[i];kind="affine";break}
 if(!ids)for(let k=2;k<=3&&!ids;k++)for(const I of combos(fs.length,k)){stats.probes++;let G=I.map(i=>fs[i]),D=span(G).length;if(G.some(f=>f.rows.length!==3))continue;let s=G.reduce((a,f,i)=>a+2**(-(2+span(G.filter((_,j)=>j!==i)).length-D)),0);if(s<1){ids=I;kind=k===2?"pair":"ternary";break}}
 if(!ids)return {label:"UNKNOWN",stats};
 let group=ids.map(i=>fs[i]),rest=fs.filter((_,i)=>!ids.includes(i)),b=span(group),a=xor(group.map(f=>f.rows[0]));stats[kind]++;stats.archiveRows+=fs.reduce((a,f)=>a+f.rows.length,0);log.push({group,rest,t});
 t=red(t^a,b);fs=rest.map(f=>({id:f.id,rows:uniq(f.rows.map(x=>red(x,b)))}));
 }
 let w=new Map;for(let i=log.length-1;i>=0;i--){const {group,rest,t}=log[i],b=span(group);for(const f of rest){let y=w.get(f.id),x=f.rows.find(x=>red(x,b)===y);assert(x!==undefined);w.set(f.id,x)}let z=exact(group,t^xor(rest.map(f=>w.get(f.id))));assert(z!==null);group.forEach((f,j)=>w.set(f.id,z[j]))}
 let witness=src.map((_,i)=>w.get(i));assert(xor(witness)===orig&&witness.every((x,i)=>src[i].includes(x)));return {label:"SAT",stats};
}
let out={random:{SAT:0,UNSAT:0,UNKNOWN:0,referenceSAT:0,referenceUNSAT:0,ternary:0,deletions:0},circuits:[],scaling:[],graphs:[]};
for(let j=0;j<100;j++){let d=3+rnd(4),n=1+rnd(6),lim=2**d,fs=[];for(let i=0;i<n;i++){let a=BigInt(1+rnd(lim-1)),b=BigInt(1+rnd(lim-1));if(a===b)b=a===1n?2n:1n;let z=BigInt(rnd(lim));fs.push([z^a,z^b,z^a^b])}for(let k=0;k<3;k++){let t=BigInt(rnd(lim)),ref=exact(fs.map(rows=>({rows})),t),g=solve(fs,t);out.random[g.label]++;out.random[ref?"referenceSAT":"referenceUNSAT"]++;out.random.ternary+=g.stats.ternary;out.random.deletions+=g.stats.deletions;if(g.label!=="UNKNOWN")assert((g.label==="SAT")===(ref!==null))}}
const tag=(c,j)=>BigInt(c)<<(2n*BigInt(j)),vals=[1,2,3];
for(let k of [3,4]){let f=Array.from({length:k-1},(_,j)=>vals.map(c=>tag(c,j)));f.push(vals.map(c=>xor(Array.from({length:k-1},(_,j)=>tag(c,j)))));let r={k,targets:0,missing:0,SAT:0,UNSAT:0,UNKNOWN:0};for(let t=0;t<4**(k-1);t++){let ref=exact(f.map(rows=>({rows})),BigInt(t)),g=solve(f,BigInt(t));r.targets++;if(!ref)r.missing++;r[g.label]++;if(k===3)assert(g.label==="SAT"&&g.stats.ternary===1);if(g.label!=="UNKNOWN")assert((g.label==="SAT")===(ref!==null))}out.circuits.push(r)}
for(let k of [4,8,16]){let fs=[];for(let j=0;j<k;j++){let a=0,b=j+1;fs.push(vals.map(c=>tag(c,a)),vals.map(c=>tag(c,b)),vals.map(c=>tag(c,a)^tag(c,b)))}let t=xor(Array.from({length:k+1},(_,j)=>tag(j%4,j))),y=solve(fs,t),n=solve(fs,t^tag(1,k+1));assert(y.label==="SAT"&&n.label==="UNSAT");out.scaling.push({blocks:k,factors:fs.length,rank:2*(k+1),sat:y.label,unsat:n.label,...y.stats})}
function compile(n,edges){let p=Array.from({length:n},(_,i)=>i),find=x=>p[x]===x?x:find(p[x]),adj=Array.from({length:n},()=>[]),ch=[];edges.forEach(([u,v],i)=>{let a=find(u),b=find(v);if(a!==b){p[a]=b;adj[u].push([v,i]);adj[v].push([u,i])}else ch.push(i)});let col=edges.map(()=>0n);ch.forEach((i,j)=>{let [u,v]=edges[i],bit=1n<<BigInt(j);function dfs(x,prev){if(x===v)return true;for(let [y,e] of adj[x])if(y!==prev&&dfs(y,x)){col[e]^=bit;return true}return false}assert(dfs(u,-1));col[i]^=bit});return edges.map((e,i)=>[0,1,2,3].filter(c=>c!==e[2]).map(c=>((c&1)?col[i]:0n)^((c&2)?col[i]<<BigInt(ch.length):0n)))}
function color(n,es){let a=Array(n);function rec(i){if(i===n)return true;for(let c=0;c<4;c++){a[i]=c;if(es.every(([u,v,s])=>Math.max(u,v)>i||(a[u]^a[v])!==s)&&rec(i+1))return true}return false}return rec(0)}
for(let n of [5,6])for(let s of [0,1]){let es=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)es.push([u,v,s]);let f=compile(n,es),g=solve(f,0n),r=color(n,es);assert(g.label==="UNKNOWN"&&r===!!s);out.graphs.push({n,sign:s,reference:r?"SAT":"UNSAT",fusion:g.label,...g.stats})}
out.assertions=checks;return out;
}
console.log(JSON.stringify(experiment(),null,2));
