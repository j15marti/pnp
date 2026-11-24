function run(){
const stat={seed:20809,pairs:0,phase_cancels:0,empty_restrictions:0,merges:0,peak_packets:0,closure_scans:0,pins:0,queries:0,assertions:0,reference_words:0,sat:0,unsat:0,witnesses:0,random_packet_checks:0};
let seed=stat.seed;const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
const bit=i=>1n<<BigInt(i), pivot=x=>bit(x.toString(2).length-1);
function par(x){let b=0;while(x){x&=x-1n;b^=1}return b}
const dot=(a,b)=>par(a&b),sign=b=>b?-1n:1n;
function check(b){stat.assertions++;if(!b)throw Error("assertion "+stat.assertions)}
function rr(eq){let a=[];for(let [x,b] of eq){for(const [u,v] of a)if(x&pivot(u)){x^=u;b^=v}if(!x){if(b)return null;continue}const p=pivot(x);a=a.map(([u,v])=>u&p?[u^x,v^b]:[u,v]);a.push([x,b]);a.sort((v,w)=>v[0]>w[0]?-1:1)}return a}
const span=vs=>rr(vs.map(x=>[x,0])).map(v=>v[0]);
function sol(eq,d){const r=rr(eq);if(!r)return null;let base=0n,used=0n,dirs=[];for(const [x,b] of r){used|=pivot(x);if(b)base|=pivot(x)}for(let j=0;j<d;j++){let p=bit(j);if(p&used)continue;let x=p;for(const [u] of r)if(u&p)x|=pivot(u);dirs.push(x)}return {base,dirs}}
const orth=(vs,d)=>sol(vs.map(x=>[x,0]),d).dirs;
const inter=(a,b,d)=>span(sol([...orth(a,d),...orth(b,d)].map(x=>[x,0]),d).dirs);
function packet(base,dirs,p,c){dirs=span(dirs);for(const u of dirs)if(base&pivot(u))base^=u;let q=0n;for(const u of dirs)if(dot(p,u))q|=pivot(u);c*=sign(dot(p^q,base));return {base,dirs,p:q,c}}
function restrict(a,I,d){let eq=orth(a.dirs,d).map(x=>[x,dot(x,a.base)]);eq.push(...orth(I,d).map(x=>[x,0]));let s=sol(eq,d);return s?packet(s.base,s.dirs,a.p,a.c):null}
function push(a,b,I,d){stat.pairs++;let r=rr([...a.dirs.map(x=>[x,dot(x,a.p)]),...b.dirs.map(x=>[x,dot(x,b.p)])]);if(!r){stat.phase_cancels++;return null}let p=0n;for(const [x,v] of r)if(v)p|=pivot(x);let base=a.base^b.base;let c=a.c*b.c*sign(dot(a.p,a.base)^dot(b.p,b.base)^dot(p,base))*bit(a.dirs.length+b.dirs.length-r.length);let s=restrict(packet(base,r.map(v=>v[0]),p,c),I,d);if(!s)stat.empty_restrictions++;return s}
function key(a){return [a.base,a.dirs.join(","),a.p].join("|")}
function collect(ps){let m=new Map();for(const p of ps){if(!p||!p.c)continue;let k=key(p);if(m.has(k)){stat.merges++;m.get(k).c+=p.c}else m.set(k,{...p})}let a=[...m.values()].filter(x=>x.c);stat.peak_packets=Math.max(stat.peak_packets,a.length);return a}
function val(a,x){let y=x^a.base;for(const u of a.dirs)if(y&pivot(u))y^=u;return y?0n:a.c*sign(dot(a.p,x))}
function ev(terms,x){return terms.reduce((s,a)=>s+val(a,x),0n)}
function good(C,x){return C.every(c=>c.some(l=>Boolean(x&bit(Math.abs(l)-1))===(l>0)))}
function closure(C,pins){let p=new Map(pins),cs=C.map(c=>[...new Set(c)]).filter(c=>!c.some(l=>c.includes(-l)));while(true){stat.closure_scans++;let next=[],change=false;for(const c of cs){if(c.some(l=>p.has(Math.abs(l))&&p.get(Math.abs(l))===(l>0)))continue;let a=c.filter(l=>!p.has(Math.abs(l)));if(!a.length)return null;if(a.length===1){let l=a[0];p.set(Math.abs(l),l>0);stat.pins++;change=true;break}next.push(a)}if(!change)return {clauses:[...next,...[...p].map(([i,b])=>[b?i:-i])],p};cs=cs}}
function count(d,C,pins=[]){stat.queries++;let s=closure(C,pins);if(!s)return 0n;let cs=s.clauses;if(!cs.length)return bit(d);let factors=cs.map(c=>{let W=c.map(l=>bit(Math.abs(l)-1)),a=0n;for(const l of c)if(l<0)a|=bit(-l-1);return {W:span(W),ps:[packet(0n,[],0n,bit(d)),packet(0n,W,a,-bit(d-W.length))]}});
function rec(lo,hi){let W=span(factors.slice(lo,hi).flatMap(f=>f.W));let O=span([...factors.slice(0,lo),...factors.slice(hi)].flatMap(f=>f.W));let I=inter(W,O,d);if(hi-lo===1)return collect(factors[lo].ps.map(p=>restrict(p,I,d)));let mid=(lo+hi)>>1,L=rec(lo,mid),R=rec(mid,hi),ps=[];for(const a of L)for(const b of R)ps.push(push(a,b,I,d));return collect(ps)}
let a=rec(0,factors.length),v=ev(a,0n),den=bit(d*(factors.length-1));check(v%den===0n);let z=v/den;check(z>=0n&&z<=bit(d));return z}
function solve(d,C,reference=true){let z=count(d,C);let expected=0n;if(reference){for(let x=0n;x<bit(d);x++){stat.reference_words++;if(good(C,x))expected++}check(z===expected)}stat[z?"sat":"unsat"]++;if(z){let pins=[];for(let j=1;j<=d;j++){let a=[...pins,[j,false]];if(count(d,C,a)>0n)pins=a;else pins.push([j,true]);}let x=0n;for(const [j,b] of pins)if(b)x|=bit(j-1);check(good(C,x));stat.witnesses++;}return z.toString()}
for(let t=0;t<160;t++){let d=4;let gen=()=>packet(BigInt(rand(16)),Array.from({length:rand(5)},()=>BigInt(rand(16))),BigInt(rand(16)),BigInt(rand(7)-3));let a=gen(),b=gen(),I=span(Array.from({length:rand(5)},()=>BigInt(rand(16)))),c=push(a,b,I,d),ip=packet(0n,I,0n,1n);for(let w=0n;w<16n;w++){let v=0n;if(val(ip,w))for(let u=0n;u<16n;u++)v+=val(a,u)*val(b,u^w);check(v===(c?val(c,w):0n));stat.random_packet_checks++}}
const cube=Array.from({length:8},(_,i)=>[1,2,3].map((x,j)=>i&(1<<j)?x:-x));
for(let m=0;m<256;m++)solve(3,cube.filter((_,i)=>m&(1<<i)));
const triples=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]];
const fano=triples.flatMap(t=>[t,t.map(x=>-x)]);check(solve(7,fano)==="0");for(let i=0;i<14;i++)check(solve(7,fano.filter((_,j)=>i!==j))==="5");
for(let t=0;t<40;t++){let d=5,C=[];for(let j=0;j<8;j++){let a=[];while(a.length<3){let v=1+rand(d);if(!a.some(l=>Math.abs(l)===v))a.push(rand(2)?v:-v)}C.push(a)}solve(d,C)}
let scaling=[];for(let d of [8,16,32,64]){let C=[Array.from({length:d},(_,i)=>i+1),Array.from({length:d},(_,i)=>i===0?-1:i+1)];let z=count(d,C);check(z===bit(d)-2n);scaling.push({d,count:z.toString(),leaf_spectral_support:bit(d).toString(),leaf_packets:2})}
let hostile=[];for(let k of [2,4,8]){let L=Array.from({length:k},(_,i)=>[3*i+1,3*i+2,3*i+3]),R=L.map(c=>c.map(x=>-x));let before=stat.pairs,z=count(3*k,[...L,...R]);check(z===6n**BigInt(k));let bad=stat.pairs-before;before=stat.pairs;let q=count(3*k,L.flatMap((c,i)=>[c,R[i]]));check(q===z);hostile.push({k,left_packet_keys:2**k,bad_pairs:bad,grouped_pairs:stat.pairs-before,count:z.toString()})}
return {stat,scaling,hostile}}
console.log(JSON.stringify(run(),null,2));
