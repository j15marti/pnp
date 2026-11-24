function gridRT03(){
const assert=(p,m)=>{if(!p)throw Error(m)};
const rank=vs=>{const b=new Map();for(let x of vs){while(x){let k=x.toString(2).length-1;if(b.has(k))x^=b.get(k);else{b.set(k,x);break}}}return b.size};
let seed=20261124;const rnd=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0};
let out={seed:20261124,graphs:0,cut_checks:0,exact_rank_comparisons:0,rows:[],mismatches:0};
for(const s of [3,4,6,8,12,16,32]){
let p=s*s,base=[];for(let i=0;i<s;i++)for(let j=0;j<s;j++){let v=i*s+j;if(i+1<s)base.push([v,v+s]);if(j+1<s)base.push([v,v+1])}let grid=base.slice();base.push([0,2*s+2]);let n=2*p+1,E=[];const add=(u,v)=>E.push([Math.min(u,v),Math.max(u,v)]);
for(let [u,v] of base){add(u,v);add(u,p+v);add(v,p+u)}for(let i=0;i<p;i++)add(p+i,2*p);
assert(E.length===7*p-6*s+3,"size");let F=E.filter(([u,v])=>!(u===p&&v===2*p));let w=Array(n);for(let i=0;i<p;i++)w[i]=i===0?3:1+((Math.floor(i/s)+i%s)%2);for(let i=0;i<p;i++)w[p+i]=w[i];w[2*p]=3;assert(F.every(([u,v])=>w[u]!==w[v]),"SAT neighbor");
let row={s,n,m:E.length,binary_rank:E.length,dictionary_nullity:2*n,quadratic_rank:E.length,analytic_width_lower:s/8,min_observed_width:Infinity,min_observed_grid_cross:Infinity};
for(let H of [E,F]){out.graphs++;let m=H.length,A=Array.from({length:n},()=>new Set());for(let [u,v] of H){A[u].add(v);A[v].add(u)}assert(A.every(a=>a.size>=2),"degree");for(let [u,v] of H)assert(![...A[u]].some(z=>A[v].has(z)),"triangle");let G=Array(n).fill(0n);if(s<=6)H.forEach(([u,v],i)=>{G[u]|=1n<<BigInt(i);G[v]|=1n<<BigInt(i)});
for(let t=0;t<20;t++){let perm=Array.from({length:n+m},(_,i)=>i);for(let i=perm.length-1;i>0;i--){let j=rnd()%(i+1);[perm[i],perm[j]]=[perm[j],perm[i]]}let left=Array(n+m).fill(false),seen=0;for(let i of perm){left[i]=true;if(i<p&&++seen===Math.floor(p/2))break}
let LA=[],LB=[],cross=0,C=new Set();H.forEach(([u,v],i)=>{if(left[n+i])LA.push([u,v]);else LB.push([u,v]);if(u<p&&v<p&&!(u===0&&v===2*s+2)&&left[u]!==left[v]){cross++;let a=left[u]?u:v,b=left[u]?v:u;C.add(left[n+i]?b:a)}});
function comp(edges,side){let par=Array.from({length:n},(_,i)=>i);function f(a){while(par[a]!==a){par[a]=par[par[a]];a=par[a]}return a}for(let [u,v] of edges)par[f(u)]=f(v);let roots=new Set(),bad=new Set();for(let u=0;u<n;u++){let a=f(u);roots.add(a);if(left[u]!==side)bad.add(a)}return roots.size-bad.size}
let width=2*(n-comp(LB,true)-comp(LA,false));assert(cross>=s/4&&C.size*4>=cross&&width>=2*C.size,"width lower");
if(s<=6){let L=[],R=[];for(let i=0;i<n+m;i++){let x=i<n?G[i]:1n<<BigInt(i-n);(left[i]?L:R).push(x)}assert(width===2*(rank(L)+rank(R)-m),"rank formula");out.exact_rank_comparisons++}
row.min_observed_width=Math.min(row.min_observed_width,width);row.min_observed_grid_cross=Math.min(row.min_observed_grid_cross,cross);out.cut_checks++;
}}out.rows.push(row)
}
return out
}
console.log(JSON.stringify(gridRT03(),null,2));
