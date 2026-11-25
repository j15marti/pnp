function run(){
const stats={rankTests:0,assertions:0,labelings:0,closureScans:0,pins:0,branches:0,leaves:0,gaussianCalls:0,referenceWords:0,witnesses:0};const check=(a)=>{stats.assertions++;if(!a)throw Error("assertion "+stats.assertions)};
const parity=x=>{let p=0;while(x){p^=1;x&=x-1}return p};
function basis(rows){stats.rankTests++;const b=[];for(let x of rows){while(x){let k=31-Math.clz32(x);if(b[k])x^=b[k];else{b[k]=x;break}}}return b.filter(Boolean)}
const rank=r=>basis(r).length;
const diff=(u,v)=>(1<<u)^(1<<v);
const row=(n,d,l)=>(l&1?d:0)^(l&2?d<<n:0);
function checkLabels(n,edges,labels){
 const ds=edges.map(([u,v])=>diff(u,v)); const r=rank(ds);
 const rs=labels.map((l,i)=>row(n,ds[i],l));const R=rank(rs);
 const A=[1,2,3].map(l=>basis(ds.filter((_,i)=>labels[i]===l)));
 let common=0;for(let x=0;x<1<<n;x++)if(A.every(b=>rank([...b,x])===b.length))common++;
 check(R===A.reduce((s,b)=>s+b.length,0)-Math.log2(common));check(R>=r);
 // For every subset forming a simple cycle, test monochromatic property.
 let mono=true;for(let mask=1;mask<1<<edges.length;mask++){let deg=Array(n).fill(0),sub=[],colors=new Set();for(let i=0;i<edges.length;i++)if(mask>>i&1){const [u,v]=edges[i];deg[u]++;deg[v]++;sub.push(ds[i]);colors.add(labels[i])}if(sub.length>=3&&deg.every(d=>d===0||d===2)&&rank(sub)===sub.length-1&&colors.size>1)mono=false}
 check((R===r)===mono);stats.labelings++;
}
const k4=[];for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)k4.push([u,v]);
for(let w=0;w<4096;w++){let es=[],ls=[];for(let i=0;i<6;i++){const l=w>>(2*i)&3;if(l){es.push(k4[i]);ls.push(l)}}checkLabels(4,es,ls)}
// Augmented Gaussian consistency, with rhs in bit n.
function gauss(n,eq){stats.gaussianCalls++;let b=Array(n).fill(0),mask=(1<<n)-1;for(let [a,t] of eq){let x=a|(t<<n);while(x&mask){let k=31-Math.clz32(x&mask);if(b[k])x^=b[k];else{b[k]=x;break}}if(!(x&mask)&&x>>n)return null}let r=b.filter(Boolean).length,x=0;for(let k=0;k<n;k++)if(b[k]&&parity((b[k]&mask)&x)!==(b[k]>>n))x|=1<<k;return {r,x}}
function valid(x,fs){return fs.every(([a,b,s,t])=>parity(a&x)!==s||parity(b&x)!==t)}
function solve(n,fs,guards){
 function close(eq){eq=eq.slice();for(;;){let g=gauss(n,eq);if(!g)return null;let changed=false,done=true;for(let [a,b,s,t] of fs){stats.closureScans++;let possible=[],good=[];for(let i=0;i<4;i++){let p=i&1,q=i>>1;if(gauss(n,[...eq,[a,p],[b,q]])){possible.push(i);if(p!==s||q!==t)good.push(i)}}if(!good.length)return null;if(good.length<possible.length)done=false;for(let l=1;l<=3;l++){const t0=parity(l&good[0]);if(good.every(i=>parity(l&i)===t0)&&possible.some(i=>parity(l&i)!==t0)){eq.push([(l&1?a:0)^(l&2?b:0),t0]);stats.pins++;changed=true;break}}if(changed)break}if(!changed)return {eq,g,done}}}
 function rec(eq){const c=close(eq);if(!c)return 0;if(c.done){stats.leaves++;check(valid(c.g.x,fs));stats.witnesses++;return 2**(n-c.g.r)}
 // closure at stagnation already performed; retain actual affine guard
 const a=guards.find(a=>gauss(n,[...c.eq,[a,0]])&&gauss(n,[...c.eq,[a,1]]));check(a!==undefined);stats.branches++;return rec([...c.eq,[a,0]])+rec([...c.eq,[a,1]])}
 const count=rec([]);let ref=0;for(let x=0;x<1<<n;x++){stats.referenceWords++;ref+=valid(x,fs)}check(count===ref);return count
}
const k5=[];for(let u=0;u<5;u++)for(let v=u+1;v<5;v++)k5.push([u,v]);
const gf=(edges,signs)=>edges.map(([u,v],i)=>[diff(u,v),diff(u,v)<<5,signs[i]&1,signs[i]>>1]);
let graphControls=[];graphControls.push(solve(10,gf(k5,Array(10).fill(0)),[diff(0,1),diff(0,2),diff(0,3),diff(0,4)]));
for(let j=0;j<10;j++){graphControls.push(solve(10,gf(k5.filter((_,i)=>i!==j),Array(9).fill(0)),[2^1,4^1,8^1,16^1]));graphControls.push(solve(10,gf(k5,Array.from({length:10},(_,i)=>i===j?1:0)),[3,5,9,17]))}
const triples=[];for(let a=1;a<=7;a++)for(let b=a+1;b<=7;b++){let c=a^b;if(c>b)triples.push([a-1,b-1,c-1])}
const opts=triples.map(([a,b,c])=>[diff(a,b),diff(a,c),diff(b,c)]);
let min=99,chosen=[],hist={};for(let w=0;w<3**7;w++){let a=w,rows=[];for(let i=0;i<7;i++){rows.push(opts[i][a%3]);a=Math.floor(a/3)}let r=rank(rows);hist[r]=(hist[r]||0)+1;if(r<min){min=r;chosen=basis(rows)}}
check(min===4);
const fano=triples.map(([a,b,c])=>[diff(a,b),diff(a,c),0,0]);
const fanoControls=[solve(7,fano,chosen)];for(let i=0;i<7;i++)fanoControls.push(solve(7,fano.filter((_,j)=>j!==i),chosen));
return {stats,graphControls,fanoControls,fanoMinRank:min,fanoRankHistogram:hist,chosenFanoRows:chosen};
}
console.log(JSON.stringify(run(),null,2));
