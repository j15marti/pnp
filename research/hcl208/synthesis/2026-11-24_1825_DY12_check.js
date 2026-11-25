function run(){
let seed=2081226, stats={assertions:0,gauss:0,countQueries:0,leafKeys:0,joinPairs:0,peakTable:0,closureScans:0,pins:0,rankChecks:0,referenceWords:0};
const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
const ok=(v,s)=>{stats.assertions++;if(!v)throw Error(s)};
function parity(x){let p=0;while(x){p^=1;x&=x-1}return p}
function sys(d,eq){stats.gauss++;let B=Array(d).fill(null),r=0;for(let [v,b] of eq){for(let j=d-1;j>=0;j--)if((v>>>j)&1){if(B[j]){v^=B[j][0];b^=B[j][1]}else{B[j]=[v,b];r++;v=0;b=0;break}}if(b)return null}
let x=0;for(let j=0;j<d;j++)if(B[j]&&(parity(B[j][0]&x)^B[j][1]))x|=1<<j;
let K=[];for(let k=0;k<d;k++)if(!B[k]){let z=1<<k;for(let j=0;j<d;j++)if(B[j]&&parity(B[j][0]&z))z|=1<<j;K.push(z)}return {r,x,K,B:B.filter(Boolean).map(a=>a[0])}}
const basis=(d,V)=>sys(d,V.map(v=>[v,0])).B;
const perp=(d,V)=>sys(d,V.map(v=>[v,0])).K;
const inter=(d,A,B)=>perp(d,[...perp(d,A),...perp(d,B)]);
const rank=(d,V)=>basis(d,V).length;
const val=(V,x)=>V.reduce((a,v,i)=>a|(parity(v&x)<<i),0);
const eqv=(V,k)=>V.map((v,i)=>[v,(k>>>i)&1]);
const rows=f=>f.flatMap(t=>t.e.map(e=>e[0]));
const evalf=(f,x)=>f.reduce((s,t)=>s+(t.e.every(([a,b])=>parity(a&x)===b)?t.c:0),0);
function count(d,f,G){stats.countQueries++;let z=0n;for(const t of f){let s=sys(d,[...G,...t.e]);if(s)z+=BigInt(t.c)*(1n<<BigInt(d-s.r))}return z}
function witness(d,f,G){if(count(d,f,G)<=0n)return null;let g=G.slice();for(let i=0;i<d;i++){let e=[1<<i,0];if(count(d,f,[...g,e])===0n)e[1]=1;g.push(e)}return sys(d,g).x}
function closure(d,F,G){G=G.slice();for(;;){stats.closureScans++;let gs=sys(d,G);if(!gs)return null;let changed=false;for(const f of F){let a=witness(d,f,G);if(a===null)return null;let D=[];for(;;){let extra=null;for(const u of perp(d,D)){let b=parity(a&u);if(count(d,f,[...G,[u,b^1]])>0n){extra=witness(d,f,[...G,[u,b^1]])^a;break}
if(rank(d,[...gs.B,u])>gs.r){G.push([u,b]);stats.pins++;changed=true;break}}
if(changed||extra===null)break;D=basis(d,[...D,extra])}
if(changed)break}if(!changed)return G}}
function tree(ids){if(ids.length===1)return ids[0];let m=Math.floor(ids.length/2);return [tree(ids.slice(0,m)),tree(ids.slice(m))]}
function leaves(t){return typeof t==="number"?[t]:[...leaves(t[0]),...leaves(t[1])]}
function solve(d,F,T){let Vs=F.map(f=>basis(d,rows(f))),all=basis(d,Vs.flat()),w=0,maxLocal=Math.max(...Vs.map(v=>v.length));
function rec(t){let ids=leaves(t),set=new Set(ids),V=basis(d,ids.flatMap(i=>Vs[i])),O=basis(d,Vs.filter((_,i)=>!set.has(i)).flat()),W=inter(d,V,O);w=Math.max(w,W.length);let M=new Map();
if(typeof t==="number"){for(let k=0;k<(1<<W.length);k++){stats.leafKeys++;let g=eqv(W,k),z=count(d,F[t],g);ok(z>=0n,"Boolean leaf");if(z>0n){let a=witness(d,F[t],g);ok(a!==null,"leaf witness");M.set(k,{z:z/(1n<<BigInt(d-V.length)),a})}}}else{let L=rec(t[0]),R=rec(t[1]);let I=inter(d,L.V,R.V);
for(const l of L.M.values())for(const r of R.M.values()){stats.joinPairs++;if(val(I,l.a)!==val(I,r.a))continue;let s=sys(d,[...eqv(L.V,val(L.V,l.a)),...eqv(R.V,val(R.V,r.a))]);ok(!!s,"glue");let k=val(W,s.x),z=l.z*r.z,old=M.get(k);if(old)old.z+=z;else M.set(k,{z,a:s.x})}}
stats.peakTable=Math.max(stats.peakTable,M.size);return {V,W,M}}
let r=rec(T),a=r.M.get(0);return {z:(a?.z??0n)*(1n<<BigInt(d-all.length)),a:a?.a??null,w,maxLocal}}
function reduce(d,F,G){let g=sys(d,G);if(!g)return null;let q=g.K.length;const map=u=>g.K.reduce((s,k,j)=>s|(parity(u&k)<<j),0);let FF=F.map(f=>f.map(t=>({c:t.c,e:t.e.map(([u,b])=>[map(u),b^parity(u&g.x)])})));return {d:q,F:FF,lift:y=>g.K.reduce((x,k,i)=>((y>>>i)&1)?x^k:x,g.x),map}}
const pred=e=>[{c:1,e:[]},{c:-1,e}];
const positive=e=>[{c:1,e}];
const triple=(a,b,c)=>pred([[(1<<a)^(1<<b),0],[(1<<a)^(1<<c),0]]);
let cases=[];
function test(name,d,F,G=[],T=tree(F.map((_,i)=>i)),brute=true){let originalG=G.slice(),gg=closure(d,F,G),z=0n,w=null,a=null,maxLocal=null; if(gg!==null){let q=reduce(d,F,gg),out=solve(q.d,q.F,T);z=out.z;w=out.w;maxLocal=out.maxLocal;if(z>0n){a=q.lift(out.a);ok(originalG.every(([u,b])=>parity(u&a)===b)&&F.every(f=>evalf(f,a)===1),"source lift")}
// Every owner-local deduction is local modulo the input guard. Check all cuts on the actual tree.
let before=reduce(d,F,originalG);if(before){let B=before.F.map(f=>basis(before.d,rows(f))),A=q.F.map(f=>basis(q.d,rows(f)));function ck(t){let s=new Set(leaves(t));let cut=(k,V)=>inter(k,V.filter((_,i)=>s.has(i)).flat(),V.filter((_,i)=>!s.has(i)).flat()).length;ok(cut(q.d,A)<=cut(before.d,B),"local closure increased width");stats.rankChecks++;if(typeof t!=="number"){ck(t[0]);ck(t[1])}}ck(T)}}
if(brute){let ref=0n;for(let x=0;x<(1<<d);x++){stats.referenceWords++;if(originalG.every(([u,b])=>parity(u&x)===b)&&F.every(f=>evalf(f,x)===1))ref++}ok(ref===z,"global count "+name)}cases.push({name,d,z:String(z),w,maxLocal,a})}
let fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
let F=fano.map(t=>triple(...t));test("Fano",7,F);
for(let i=0;i<7;i++)for(let b=0;b<2;b++){let FF=F.slice();FF[i]=pred(fano[i].map(v=>[1<<v,b]));test("Fano single clause "+i+"/"+b,7,FF)}
for(let k=0;k<72;k++){let d=4+rnd(4),m=2+rnd(7),F=[];for(let i=0;i<m;i++){let e=[];for(let j=0;j<1+rnd(4);j++)e.push([1+rnd((1<<d)-1),rnd(2)]);F.push(pred(e))}let G=k%3===0?[[1+rnd((1<<d)-1),rnd(2)]]:[];test("random "+k,d,F,G)}
// Three pairwise disjoint line spaces with a global dependency: non-coordinate chart.
test("three line SAT",2,[positive([[1,0]]),positive([[2,0]]),positive([[3,0]])]);
test("three line UNSAT",2,[positive([[1,0]]),positive([[2,0]]),positive([[3,1]])]);
// High local rank, small cut: two coaffine factors observe private bits plus common x.
for(let d of [8,12,16]){let h=d/2;let A=Array.from({length:h},(_,j)=>[1<<j,0]),B=[[1,0],...Array.from({length:d-h},(_,j)=>[1<<(h+j),0])];test("high local rank "+d,d,[pred(A),pred(B)]);test("opposed shared pins "+d,d,[pred(A),pred(B),positive([[1,0]]),positive([[1,1]])]);}
// Exact quotient identity under arbitrary H, plus monotonicity for locally generated H.
let increase=0;
for(let i=0;i<300;i++){let d=3+rnd(5),rv=()=>Array.from({length:rnd(d+1)},()=>rnd(1<<d)),A=rv(),B=rv(),H=rv();let W=inter(d,A,B),ab=basis(d,[...A,...B]);let q=perp(d,H),map=u=>val(q,u),wq=inter(q.length,A.map(map),B.map(map)).length;let a=inter(d,H,A).length,b=inter(d,H,B).length,c=inter(d,H,ab).length,hw=inter(d,H,W).length;ok(wq===W.length+c-a-b,"quotient formula");stats.rankChecks++;if(wq>W.length)increase++;let local=[...A.filter(()=>rnd(2)),...B.filter(()=>rnd(2))],lq=perp(d,local),lm=u=>val(lq,u);ok(inter(lq.length,A.map(lm),B.map(lm)).length<=W.length,"local rank monotonic");stats.rankChecks++}
let result={seed:2081226,stats,arbitraryGuardWidthIncrease:increase,cases,sat:cases.filter(c=>c.z!=="0").length,unsat:cases.filter(c=>c.z==="0").length};return result
}
console.log(JSON.stringify(run(),null,2));
