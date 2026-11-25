function main(){
const stats={assertions:0,random:0,controls:0,sat:0,unsat:0,coarseJoins:0,residualJoins:0,pruned:0,peakCoarse:0,peakResidual:0,closurePins:0,closureRuns:0,scaling:[]};
function check(x){stats.assertions++;if(!x)throw Error("assertion "+stats.assertions)}
function ins(B,x){while(x){let i=x.toString(2).length-1;if(B.has(i))x^=B.get(i);else{B.set(i,x);return}}}
function basis(xs){let b=new Map();for(let x of xs)ins(b,x);return b}
function member(B,x){while(x){let i=x.toString(2).length-1;if(!B.has(i))return false;x^=B.get(i)}return true}
function hull(xs){if(!xs.length)return null;return {r:xs[0],b:basis(xs.map(x=>x^xs[0])),c:BigInt(xs.length)}}
function merge(a,b){if(!a)return {r:b.r,b:new Map(b.b),c:b.c};ins(a.b,a.r^b.r);for(let x of b.b.values())ins(a.b,x);a.c+=b.c;return a}
function prod(a,b){return {r:a.r^b.r,b:basis([...a.b.values(),...b.b.values()]),c:a.c*b.c}}
function equal(a,b){return !a&&!b||!!a&&!!b&&a.c===b.c&&a.b.size===b.b.size&&member(a.b,a.r^b.r)&&[...b.b.values()].every(x=>member(a.b,x))}
function pins(h,m){let p=new Map();if(h)for(let i=0;i<m;i++){let z=1n<<BigInt(i);if([...h.b.values()].every(x=>!(x&z)))p.set(i,!!(h.r&z))}return p}
function tree(m){function rec(l,r){if(r-l===1)return {l,r};let s=(l+r)>>1;return {l,r,a:rec(l,s),b:rec(s,r)}}return rec(0,m)}
function build(n,E,t,tag,pin,k){
let mask=(1n<<BigInt(n))-1n, target=mask|(tag?t<<BigInt(n):0n), A=E.map(e=>(1n<<BigInt(e.u))|(1n<<BigInt(e.v))|(tag?e.g<<BigInt(n):0n));let w=0;
function go(T){let B=basis(A.filter((_,i)=>i<T.l||i>=T.r)),C=basis(A.slice(T.l,T.r));w=Math.max(w,B.size+C.size-basis([...B.values(),...C.values()]).size);
let M=new Map();function add(v,h,lo,hi){if(!member(B,target^v))return;let old=M.get(v);if(!old){M.set(v,{h,lo:lo.slice(),hi:hi.slice()});return}old.h=merge(old.h,h);for(let j=0;j<k;j++){if(lo[j]<old.lo[j])old.lo[j]=lo[j];if(hi[j]>old.hi[j])old.hi[j]=hi[j]}}
if(!T.a){let i=T.l;for(let b of [false,true])if(!pin.has(i)||pin.get(i)===b){let z=b?E[i].w.slice(0,k):Array(k).fill(0n);add(b?A[i]:0n,{r:b?1n<<BigInt(i):0n,b:new Map(),c:1n},z,z)}}else{go(T.a);go(T.b);for(let [v,x] of T.a.M)for(let [u,y] of T.b.M){stats.coarseJoins++;if(v&u&mask)continue;add(v^u,prod(x.h,y.h),x.lo.map((z,j)=>z+y.lo[j]),x.hi.map((z,j)=>z+y.hi[j]))}}
T.M=M;stats.peakCoarse=Math.max(stats.peakCoarse,M.size)}
let T=tree(E.length);go(T);return {T,target,mask,A,w,root:T.M.get(target)}
}
function solve(n,E,t,Q,pin=new Map(),cap=10000n){
let m=E.length,k=Q.length;
let U=build(n,E,0n,false,pin,0);stats.closureRuns++;if(!U.root)return {h:null,stage:"untagged"};let p=pins(U.root.h,m);stats.closurePins+=p.size;
let C=build(n,E,t,true,p,k);stats.closureRuns++;if(!C.root)return {h:null,stage:"syndrome",w:C.w};let pp=pins(C.root.h,m);stats.closurePins+=pp.size;
let signs=[],D=[];for(let j=0;j<k;j++){let a=Q[j]-C.root.lo[j],b=C.root.hi[j]-Q[j];if(a<0n||b<0n)return {h:null,stage:"range",w:C.w};signs.push(a<=b?1n:-1n);D.push(a<=b?a:b)}
let B=D.reduce((a,b)=>a*(b+1n),1n);if(B>cap)return {h:null,stage:"decline",w:C.w};
let anchor=(x,j)=>signs[j]===1n?x.lo[j]:-x.hi[j];let peak=0;
function go(T){let R=new Map();function add(v,d,h){for(let j=0;j<k;j++){check(d[j]>=0n);if(d[j]>D[j]){stats.pruned++;return}}let key=v.toString()+":"+d.join(",");let old=R.get(key);if(old)old.h=merge(old.h,h);else R.set(key,{v,d,h})}
if(!T.a){let i=T.l;for(let b of [false,true])if(!pp.has(i)||pp.get(i)===b){let v=b?C.A[i]:0n,x=T.M.get(v);if(!x)continue;add(v,Q.map((_,j)=>(b?signs[j]*E[i].w[j]:0n)-anchor(x,j)),{r:b?1n<<BigInt(i):0n,b:new Map(),c:1n})}}
else{go(T.a);go(T.b);for(let x of T.a.R.values())for(let y of T.b.R.values()){stats.residualJoins++;if(x.v&y.v&C.mask)continue;let v=x.v^y.v,z=T.M.get(v);if(!z)continue;let d=Q.map((_,j)=>x.d[j]+y.d[j]+anchor(T.a.M.get(x.v),j)+anchor(T.b.M.get(y.v),j)-anchor(z,j));add(v,d,prod(x.h,y.h))}}
T.R=R;peak=Math.max(peak,R.size);stats.peakResidual=Math.max(stats.peakResidual,R.size)}
go(C.T);let h=C.T.R.get(C.target.toString()+":"+D.join(","))?.h??null;stats.closureRuns++;if(h)stats.closurePins+=pins(h,m).size;
return {h,stage:"deficit",w:C.w,peak,B,D}
}
function ref(n,E,t,Q,pin){let out=[];function rec(used,r,g,w){if(used===(1n<<BigInt(n))-1n){if(g===t&&w.every((v,j)=>v===Q[j])&&[...pin].every(([i,b])=>!!(r&(1n<<BigInt(i)))===b))out.push(r);return}
let u=0;while(used&(1n<<BigInt(u)))u++;E.forEach((e,i)=>{if(e.u!==u&&e.v!==u)return;let b=(1n<<BigInt(e.u))|(1n<<BigInt(e.v));if(used&b)return;rec(used|b,r|(1n<<BigInt(i)),g^e.g,w.map((v,j)=>v+e.w[j]))})}rec(0n,0n,0n,Q.map(()=>0n));return hull(out)}
function verify(n,E,t,Q,r,p){let d=Array(n).fill(0),g=0n,w=Q.map(()=>0n);E.forEach((e,i)=>{if(r&(1n<<BigInt(i))){d[e.u]++;d[e.v]++;g^=e.g;w=w.map((x,j)=>x+e.w[j])}});check(d.every(x=>x===1)&&g===t&&w.every((x,j)=>x===Q[j])&&[...p].every(([i,b])=>!!(r&(1n<<BigInt(i)))===b))}
let seed=20261124;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
function test(n,E,t,Q,p=new Map()){let x=solve(n,E,t,Q,p),y=ref(n,E,t,Q,p);check(x.stage!=="decline");check(equal(x.h,y));if(x.h){stats.sat++;verify(n,E,t,Q,x.h.r,p);let closure=pins(x.h,E.length);let z=solve(n,E,t,Q,closure);check(equal(x.h,z.h))}else stats.unsat++;return x}
for(let k=0;k<100;k++){let n=4+2*rand(2),E=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)if(rand(5)<3||i%2===0&&j===i+1)E.push({u:i,v:j,g:BigInt(rand(4)),w:[BigInt(rand(7)-3),BigInt(rand(7)-3)]});let p=new Map();if(k%4===0)p.set(rand(E.length),!!rand(2));let t=BigInt(rand(4)),Q=[BigInt(rand(9)-4),BigInt(rand(9)-4)];if(k%2===0){t=0n;Q=[0n,0n];for(let i=0;i<n;i+=2){let e=E.find(e=>e.u===i&&e.v===i+1);t^=e.g;Q=Q.map((x,j)=>x+e.w[j])}}test(n,E,t,Q,p);stats.random++}
let E0=[];for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)E0.push({u:i,v:j,g:0n,w:i===0?[[0n,1n],[1n,0n],[2n,2n]][j-1]:[0n,0n]});
let bad=test(4,E0,0n,[0n,0n]);check(bad.stage==="deficit"&&bad.B===1n&&!bad.h);test(4,E0,0n,[0n,1n]);stats.controls+=2;
for(let k of [4,8,16,32,64]){let E=[],L=1n<<BigInt(8*k);for(let b=0;b<k;b++)for(let i=0;i<4;i++)for(let j=i+1;j<4;j++){let w=Array(k+1).fill(0n),g=0n;if(i===0){if(j===2)g=1n<<BigInt(b);if(j===3){g=1n<<BigInt(b+1);w[0]=b<2?2n:L;}w[b+1]=L+(j===3&&b>=2?L:0n)}E.push({u:4*b+i,v:4*b+j,g,w})}
let Q=Array(k+1).fill(L);Q[0]=2n;let yes=solve(4*k,E,0n,Q);check(yes.h&&yes.h.c===2n);verify(4*k,E,0n,Q,yes.h.r,new Map());Q[0]=1n;let no=solve(4*k,E,0n,Q);check(!no.h&&no.stage==="deficit");stats.scaling.push({blocks:k,quotaRows:k+1,weightBits:8*k+1,width:yes.w,satCount:yes.h.c.toString(),satDeficit:yes.D.reduce((a,b)=>a+b,0n).toString(),satStateFactor:yes.B.toString(),satPeak:yes.peak,unsatPeak:no.peak});stats.controls+=2;stats.sat++;stats.unsat++}
return stats;
}
console.log(JSON.stringify(main(),null,2));
