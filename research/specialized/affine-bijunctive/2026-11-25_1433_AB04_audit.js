'use strict';
function audit(){
const cnt={rootJobs:0,sat:0,unsat:0,guardJobs:0,greedyCertificates:0,optimalChecks:0,discoveryNodes:0,cells:0,closureRounds:0,probeCalls:0,forced:0,verifiedWords:0,basisChecks:0,compilerChecks:0};
const bit=i=>1n<<BigInt(i), parity=x=>{let p=0;while(x){p^=1;x&=x-1n;}return p}, ev=(f,x)=>parity(f&((x<<1n)|1n));
const reduce=(x,B)=>{for(const b of B)if(x&bit(b.toString(2).length-1))x^=b;return x};
function basis(xs){let B=[];for(let x of xs){x=reduce(x,B);if(x){B.push(x);B.sort((a,b)=>a>b?-1:a<b?1:0);}}return B}
function add(B,x){return basis([...B,x])}
function good(P,x,R=[]){return R.every(f=>!ev(f,x))&&P.every(([f,g])=>!(ev(f,x)&&ev(g,x)))}
function quadratic(f,g,n){let q=0n,l=(f&1n)&(g&1n);for(let i=1;i<=n;i++){let a=!!(f&bit(i)),b=!!(g&bit(i));if((a&&!!(g&1n))^(b&&!!(f&1n))^(a&&b))l|=bit(i);for(let j=i+1;j<=n;j++)if((a&&!!(g&bit(j)))^(b&&!!(f&bit(j))))q|=bit(i*n+j);}return [q,l]}
function norm(P,R,n){let B=basis(R);while(true){cnt.closureRounds++;if(B.includes(1n))return null;const Q=P.map(([f,g])=>[reduce(f,B),reduce(g,B)]);let piv=new Map(),pending=[];for(let [f,g] of Q){let [q,l]=quadratic(f,g,n);while(q){let h=q.toString(2).length-1;if(!piv.has(h)){piv.set(h,[q,l]);break}let [u,v]=piv.get(h);q^=u;l^=v;}if(!q&&l)pending.push(l)}let C=basis([...B,...pending]);if(C.length===B.length)return {B,Q};B=C;}}
function closure(P,R,n){let C=norm(P,R,n);while(C){let advanced=false;for(let i=1;i<=n;i++){let f=reduce(bit(i),C.B);if(f<=1n)continue;cnt.probeCalls+=2;let a=norm(P,[...C.B,bit(i)],n),b=norm(P,[...C.B,bit(i)^1n],n);if(!a&&!b)return null;if(!a||!b){cnt.forced++;C=b??a;advanced=true;break}}if(!advanced)return C}return null}
function planes(Q){return Q.map(([f,g])=>[f>>1n,g>>1n]).filter(([a,b])=>a&&b&&a!==b)}
function uncovered(P,B){return P.find(([a,b])=>reduce(a,B)&&reduce(b,B)&&reduce(a^b,B))}
function greedy(P){let B=[],pack=[];for(let p;p=uncovered(P,B);){pack.push(p);B=basis([...B,...p]);}if(B.length!==2*pack.length||uncovered(P,B))throw Error("bad packing");cnt.greedyCertificates++;return {B,lower:pack.length}}
function find(P,k,B=[]){cnt.discoveryNodes++;let p=uncovered(P,B);if(!p)return B;if(B.length===k)return null;let [a,b]=p;for(let h of [a,b,a^b]){let S=find(P,k,add(B,h));if(S)return S}return null}
function sample(B,n,free=0n){let x=free;for(const b of [...B].reverse()){let i=b.toString(2).length-1;if(i===0)throw Error("inconsistent");if(ev(b,x))x^=bit(i-1);}return x}
function solve(P,R,n,cap=n){let C=closure(P,R,n);if(!C)return {words:[],k:null,lower:null,greedy:null};let ps=planes(C.Q),g=greedy(ps);let H=null;for(let k=g.lower;k<=Math.min(cap,g.B.length);k++){H=find(ps,k);if(H)break;}if(!H)return {unknown:true,lower:g.lower};let words=[];for(let z=0;z<2**H.length;z++){cnt.cells++;let guards=H.map((h,i)=>(h<<1n)^BigInt((z>>i)&1));let L=closure(P,[...C.B,...guards],n);if(!L)continue;if(planes(L.Q).length)throw Error("nonlinear leaf");let fixed=new Set(L.B.map(b=>b.toString(2).length-2));let base=sample(L.B,n);let ws=[base];for(let i=0;i<n;i++)if(!fixed.has(i))ws.push(sample(L.B,n,bit(i)));for(let x of ws){if(!good(P,x,[...R,...guards]))throw Error("invalid witness");cnt.verifiedWords++;words.push(x)}}return {words,k:H.length,lower:g.lower,greedy:g.B.length,ps}}
let seed=20261125;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)}
function allWords(P,R,n){let w=[];for(let x=0;x<2**n;x++)if(good(P,BigInt(x),R))w.push(BigInt(x));return w}
function rankWords(w){return basis(w.map(x=>(x<<1n)|1n)).length}
function spaces(n){let S=new Map([["0",[0n]]]);let frontier=[[0n]];for(let i=0;i<n;i++){let nxt=[];for(let V of frontier)for(let a=1n;a<bit(n);a++){if(V.includes(a))continue;let W=[...V,...V.map(x=>x^a)].sort((a,b)=>a<b?-1:a>b?1:0);let key=W.join(",");if(!S.has(key)){S.set(key,W);nxt.push(W)}}frontier=nxt;}return [...S.values()].sort((a,b)=>a.length-b.length)}
const S=spaces(4);let cases=[];
function check(P,R,n,guard=false){let ref=allWords(P,R,n),out=solve(P,R,n);if(out.unknown||!!ref.length!==!!out.words.length||rankWords(ref)!==rankWords(out.words))throw Error("decision/span");cnt.basisChecks++;if(guard)cnt.guardJobs++;else {cnt.rootJobs++;cnt[ref.length?"sat":"unsat"]++}if(out.k!==null&&n===4){let opt=S.find(V=>out.ps.every(([a,b])=>V.includes(a)||V.includes(b)||V.includes(a^b)));if(Math.log2(opt.length)!==out.k||out.lower>out.k||out.greedy>2*out.k)throw Error("optimal/approx");cnt.optimalChecks++;}return {sat:!!ref.length,k:out.k}}
for(let t=0;t<160;t++){let n=4+rnd(3),P=Array.from({length:1+rnd(13)},()=>[BigInt(rnd(2**(n+1))),BigInt(rnd(2**(n+1)))]);let R=Array.from({length:rnd(3)},()=>BigInt(rnd(2**(n+1))));let res=check(P,R,n);for(let i=1;i<=n;i++)for(let v=0;v<2;v++)check(P,[...R,bit(i)^BigInt(v)],n,true);cases.push({n,m:P.length,...res})}
let large=[];
for(let n of [8,16,32]){let h=(bit(n+1)-2n),P=Array.from({length:n-1},(_,i)=>[h,bit(i+1)]);let out=solve(P,[],n,1);if(out.unknown||out.k!==1||rankWords(out.words)!==n+1)throw Error("dense star "+n+" "+out.k+" "+rankWords(out.words));let neg=solve(P,[h^1n,bit(n)],n,1);if(neg.words.length)throw Error("star UNSAT");large.push({n,k:out.k,greedy:out.greedy,actualAffineRank:rankWords(out.words),unsatNeighbor:!neg.words.length});}
for(let signs=0;signs<8;signs++)for(let x=0;x<8;x++){let L=x^signs,models=0;for(let s=0;s<8;s++){let ok=parity(BigInt(s))===1&&(s&~L)===0; if(ok)models++;cnt.compilerChecks++;}if(!!L!==!!models)throw Error("compiler");}
return {seed:20261125,counts:cnt,large,small:cases,referenceSubspaces:S.length}
}
console.log(JSON.stringify(audit(),null,2));
