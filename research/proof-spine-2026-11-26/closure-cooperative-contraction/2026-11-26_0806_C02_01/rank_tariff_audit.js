// Standalone Node.js. Independently reconstructs FP20 guarded cubic ring, exact GF2 seam DP, parity reference and source witness lift.
const run=()=>{
let checks=0;const ok=(p,msg="check")=>{checks++;if(!p)throw Error(msg+" "+checks)};
const xorBasis=vs=>{let b=new Map();for(let v of vs){while(v){let k=v.toString(2).length-1;if(b.has(k))v^=b.get(k);else{b.set(k,v);break}}}return b};
const member=(v,b)=>{while(v){let k=v.toString(2).length-1;if(!b.has(k))return false;v^=b.get(k)}return true};
function fixture(h,d){
let n=2*h*d+2,s=n-2,t=n-1,E=[],inc=Array.from({length:n},()=>[]),a=[],b=[],phase=[];
const v=(i,j)=>2*d*i+j;
function edge(u,w,aa,bb,p=-1){let e=E.length;E.push([u,w]);inc[u].push(e);inc[w].push(e);a.push(aa);b.push(bb);phase.push(p)}
for(let i=0;i<h;i++)for(let j=0;j<2*d;j++)edge(v(i,j),v(i,(j+1)%(2*d)),1,+(j%2===0),i);
for(let i=0;i<h;i++)for(let j=0;j<d;j++){let u=v(i,d+j),w=v((i+1)%h,j);if(i===h-1&&j<2){edge(u,(u%2===0?s:t),0,1);edge(w,(w%2===0?s:t),0,1)}else edge(u,w,0,1)}
edge(s,t,0,0);
ok(E.length===3*n/2);ok(inc.every(q=>q.length===3));ok(new Set(E.map(([u,v])=>[Math.min(u,v),Math.max(u,v)].join(","))).size===E.length);
for(let q of inc){ok(q.reduce((z,e)=>z^a[e],0)===0);ok(q.reduce((z,e)=>z^b[e],0)===0)}
ok(E.filter((_,e)=>!(a[e]||b[e])).length===1);
const side=Array(n).fill(-1);side[0]=0;let todo=[0];for(let u of todo)for(let e of inc[u]){let w=E[e][0]^E[e][1]^u;if(side[w]<0){side[w]=1-side[u];todo.push(w)}else ok(side[u]!==side[w])}ok(todo.length===n);
return {n,E,inc,a,b,phase,h,d};
}
function guards(h,mode,dense){
let rows=[],rhs=[];for(let i=0;i<h;i+=2){rows.push((1n<<BigInt(i))|(1n<<BigInt(i+1)));rhs.push(0)}
let global=0n;for(let i=0;i<h;i+=2)global|=1n<<BigInt(i);rows.push(global);rhs.push(1);
if(mode==="pin") {rows.push(1n);rhs.push(1)}
if(mode==="NO"){rows.push(global);rhs.push(0)}
const orig=rows.slice(),origR=rhs.slice();
if(dense){let r=rows.length;for(let i=0;i<r;i++)for(let j=0;j<r;j++)if(i!==j&&((i*37+j*13+7)%5)<3){rows[i]^=rows[j];rhs[i]^=rhs[j]}}
let cols=Array.from({length:h},(_,i)=>rows.reduce((v,r,j)=>v|(((r>>BigInt(i))&1n)<<BigInt(j)),0n));let target=rhs.reduce((v,x,j)=>v|(BigInt(x)<<BigInt(j)),0n);
return {rows,rhs,orig,origR,cols,target};
}
function verifyGuard(x,g){let mask=x.reduce((v,z,i)=>v|(BigInt(z)<<BigInt(i)),0n);function parity(v){let p=0;while(v){v&=v-1n;p^=1}return p}return g.rows.every((r,j)=>parity(r&mask)===g.rhs[j])&&g.orig.every((r,j)=>parity(r&mask)===g.origR[j])}
function lift(F,x){let {E,inc,b,phase,n}=F;let bb=b.map((v,e)=>phase[e]<0?v:v^x[phase[e]]);ok(inc.every(q=>q.reduce((s,e)=>s+bb[e],0)===2));let c=bb.map(v=>v?0:2);
for(let e=0;e<E.length;e++)if(c[e]===0){let start=E[e][0],u=start,j=e,cl=1;do{ok(c[j]===0);c[j]=cl;let w=E[j][0]^E[j][1]^u;let next=inc[w].find(k=>bb[k]&&k!==j);u=w;j=next;cl=4-cl}while(u!==start);ok(j===e&&cl===1)}
ok(inc.every(q=>new Set(q.map(e=>c[e])).size===3));ok(c.every((v,e)=>(v&1)===bb[e]));return c}
function phaseDP(g,cost,domains){
let n=cost.length,stats={nodes:0,attempts:0,entries:0,maxEntries:0,maxLambda:0,rankQueries:0};
function rec(lo,hi){
let L=g.cols.slice(lo,hi),R=g.cols.filter((_,i)=>i<lo||i>=hi),u=xorBasis(L),v=xorBasis(R),all=xorBasis(L.concat(R));stats.rankQueries+=3;stats.nodes++;let lam=u.size+v.size-all.size;stats.maxLambda=Math.max(stats.maxLambda,lam);let M=new Map();
function put(s,c,x,count){stats.attempts++;if(!member(g.target^s,v))return;let old=M.get(s);if(!old)M.set(s,{c,x,count});else{old.count+=count;if(c<old.c){old.c=c;old.x=x}}}
if(hi-lo===1){for(let b of domains[lo])put(b?g.cols[lo]:0n,cost[lo][b],String(b),1n)}
else {let mid=(lo+hi)>>1,A=rec(lo,mid),B=rec(mid,hi);for(let [s,p] of A)for(let [t,q] of B)put(s^t,p.c+q.c,p.x+q.x,p.count*q.count)}
ok(BigInt(M.size)<=1n<<BigInt(lam),"rank bound");stats.entries+=M.size;stats.maxEntries=Math.max(stats.maxEntries,M.size);return M
}
let M=rec(0,n),r=M.get(g.target);return {result:r,stats};
}
function reference(h,mode,cost){if(mode==="NO")return null;let M=new Map([[0,{cost:0,x:"",count:1n}]]);for(let i=0;i<h;i+=2){let B=new Map();for(let [p,r] of M)for(let b of (mode==="pin"&&i===0?[1]:[0,1])){let q=p^b,v=r.cost+cost[i][b]+cost[i+1][b],o=B.get(q);if(!o)B.set(q,{cost:v,x:r.x+String(b).repeat(2),count:r.count});else{o.count+=r.count;if(v<o.cost){o.cost=v;o.x=r.x+String(b).repeat(2)}}}M=B}return M.get(1)??null}
function closure(g){if(!member(g.target,xorBasis(g.cols)))return null;let domains=[];for(let i=0;i<g.cols.length;i++){let B=xorBasis(g.cols.filter((_,j)=>i!==j));domains.push([0,1].filter(b=>member(g.target^(b?g.cols[i]:0n),B)));ok(domains[i].length>0)}return domains}
let scale=[];for(let [h,d] of [[4,3],[6,5],[8,9],[12,11],[20,19],[32,31],[64,3],[128,3],[256,3]]){
let F=fixture(h,d),cost=Array.from({length:h},(_,i)=>[(i*19+3)%17,(i*23+5)%19]);
for(let mode of ["base","pin","NO"]){let base=guards(h,mode,false),dense=guards(h,mode,true),D=closure(dense),ref=reference(h,mode,cost);
if(!D){ok(!ref);continue}
let a=phaseDP(base,cost,D),b=phaseDP(dense,cost,D);
ok(a.result&&b.result&&ref);ok(a.result.c===ref.cost&&b.result.c===ref.cost);ok(a.result.count===ref.count&&b.result.count===ref.count);ok(a.stats.maxLambda===b.stats.maxLambda);ok(a.stats.entries===b.stats.entries);for(let r of [a.result,b.result]){let x=Array.from(r.x,Number);ok(verifyGuard(x,dense));lift(F,x)}
if(h<=12){let count=0n,min=Infinity;for(let w=0;w<2**h;w++){let x=Array.from({length:h},(_,i)=>(w>>i)&1);if(verifyGuard(x,dense)){count++;let v=x.reduce((z,b,i)=>z+cost[i][b],0);min=Math.min(min,v)}}ok(count===b.result.count&&min===b.result.c)}
scale.push({h,d,vertices:F.n,mode,rank:xorBasis(dense.cols).size,forced:D.filter(x=>x.length===1).length,phaseWords:b.result.count.toString(),cost:b.result.c,...b.stats,naiveFullGuardLeaves:(1n<<BigInt(h/2-(mode==="pin"?2:1))).toString()});
}}
/* independent adversary: at each nonfinal pair both choices have an extension under total parity; memo full pin vectors retains distinct histories. */
let branch=[];for(let q of [4,8,12,16,32,64,128]){let n=q*2;let g=guards(n,"base",false);let leaves=1n<<BigInt(q-1);if(q<=16){let C=0n;for(let w=0;w<2**(q-1);w++){let x=[],p=1;for(let i=0;i<q-1;i++){let b=(w>>i)&1;x.push(b,b);p^=b}x.push(p,p);ok(verifyGuard(x,g));C++}ok(C===leaves)}branch.push({phases:n,localKernelBits:1,distinctFullHistoryLeaves:leaves.toString(),exactCompressedKeysPerSeam:2})}
return {checks,scale,branch,negativeGuardCharts:9,sourceWitnessLifts:36}
};
console.log(JSON.stringify(run(),null,2));
