function run(){
let seed=20261124,checks=0;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}, ok=(b)=>{checks++;if(!b)throw Error("assertion "+checks)};
const top=x=>31-Math.clz32(x), bas=xs=>{let p=[];for(let x of xs){while(x){let k=top(x);if(p[k])x^=p[k];else{p[k]=x;break}}}return p.filter(Boolean).reverse()}, rem=(x,b)=>{for(const v of b)if(x&(1<<top(v)))x^=v;return x}, span=b=>{let a=[0];for(const x of b)a=a.concat(a.map(y=>y^x));return a};
function deps(cols){let p=[],out=[];for(let [x,t] of cols){while(x){let k=top(x);if(p[k]){x^=p[k][0];t^=p[k][1]}else{p[k]=[x,t];break}}if(!x)out.push(t)}return bas(out)}
const inter=(a,b)=>deps([...a.map(x=>[x,x]),...b.map(x=>[x,0])]), add=(m,k,v)=>m.set(k,(m.get(k)||0n)+v), parity=x=>{let p=0;while(x){x&=x-1;p^=1}return p};
let stats={joins:0,quotientGroups:0,butterflies:0,leafTransitions:0,localProbes:0,localPins:0,fullHullQueries:0};
function fw(a){for(let h=1;h<a.length;h*=2)for(let i=0;i<a.length;i+=2*h)for(let j=i;j<i+h;j++){let x=a[j],y=a[j+h];a[j]=x+y;a[j+h]=x-y;stats.butterflies++}}
function join(f,g,A,B,C,q, audit=false){
 const D=inter(inter(A,B),C),d=D.length,L=2**d,mask=(1<<q)-1;
 const R=deps([...A.map(x=>[x,x]),...B.map(x=>[x,x<<q]),...C.map(x=>[x,0])]),t=R.length;
 const Q=bas(R.map(v=>rem(v&mask,D)|(rem(v>>>q,D)<<q)));ok(Q.length===t-2*d);
 const values=span(D), partition=m=>{let out=new Map();for(const [x,v] of m){let r=rem(x,D),a=out.get(r);if(!a){a=Array(L).fill(0n);out.set(r,a)}let u=x^r,i=0;for(let j=0;j<d;j++)if(u&(1<<top(D[j]))){u^=D[j];i|=1<<j}ok(u===0);a[i]+=v}return out};
 const F=partition(f),G=partition(g);for(const a of F.values())fw(a);for(const a of G.values())fw(a);
 let out=new Map();stats.joins++;
 for(const v of span(Q)){stats.quotientGroups++;let x=v&mask,y=v>>>q,a=F.get(x),b=G.get(y);if(!a||!b)continue;let c=a.map((z,i)=>z*b[i]);fw(c);for(let i=0;i<L;i++){ok(c[i]%BigInt(L)===0n);let z=c[i]/BigInt(L);if(z)add(out,x^y^values[i],z)}}
 if(audit){let ref=new Map();for(const [x,a] of f)for(const [y,b] of g)if(!rem(x^y,C))add(ref,x^y,a*b);for(const k of new Set([...ref.keys(),...out.keys()]))ok((ref.get(k)||0n)===(out.get(k)||0n))}
 return {out,t,d,w:[inter(A,bas([...B,...C])).length,inter(B,bas([...A,...C])).length,inter(C,bas([...A,...B])).length]};
}
const colors=mask=>[0,1,2,3].filter(x=>mask&(1<<x)), xorMask=(a,b)=>{let z=0;for(let x of colors(a))for(let y of colors(b))z|=1<<(x^y);return z};
function prepare(leaves){let offset=0;for(const l of leaves){l.off=offset;offset+=2*l.steps.length;l.B=bas(l.steps.flatMap(s=>s.cols))}for(const l of leaves)l.out=bas(leaves.filter(x=>x!==l).flatMap(x=>x.B));return offset}
function leaf(l,pins,chi){let dp=new Map([[1,1n]]);for(let i=0;i<l.steps.length;i++){let s=l.steps[i],next=new Map(),suffix=bas([...l.out,...l.steps.slice(i+1).flatMap(x=>x.cols)]);for(const [key,c] of dp)for(let y=0;y<4;y++){stats.leafTransitions++;let pos=l.off+2*i;if(pins.some(([j,b])=>j>=pos&&j<pos+2&&((y>>(j-pos))&1)!==b))continue;let D=15^(s.fixed|(1<<(y^s.shift)));if(!D)continue;let p=(key>>>4)^((y&1)?s.cols[0]:0)^((y&2)?s.cols[1]:0);if(rem(p,suffix))continue;let R=l.cycle?xorMask(key&15,D):1;if(l.cycle&&i===l.steps.length-1&&!(R&1))continue;let sign=parity(y&((chi>>>pos)&3))?-1n:1n;add(next,(p<<4)|R,c*sign)}dp=next}let out=new Map();for(const [k,v] of dp)if(v)add(out,k>>>4,v);return out}
function solve(L,q,pins=[],chi=0,audit=false){let f=leaf(L[0],pins,chi),g=leaf(L[1],pins,chi),h=leaf(L[2],pins,chi);
 let j=join(f,g,L[0].B,L[1].B,L[2].B,q,audit),k=join(j.out,h,bas([...L[0].B,...L[1].B]),L[2].B,[],q,audit);return {count:k.out.get(0)||0n,j}}
function close(L,m,pins=[]){pins=pins.slice();for(;;){let changed=false;for(let l of L){let s=leaf(l,pins,0);if(![...s.values()].some(x=>x>0n))return {pins,unsat:true};for(let j=l.off;j<l.off+2*l.steps.length;j++){if(pins.some(x=>x[0]===j))continue;let b=[0,1].map(v=>{stats.localProbes++;return [...leaf(l,[...pins,[j,v]],0).values()].some(x=>x>0n)});if(!b[0]&&!b[1])return {pins,unsat:true};if(!b[0]||!b[1]){pins.push([j,b[1]?1:0]);stats.localPins++;changed=true;break}}if(changed)break}if(!changed)return {pins,unsat:false}}}
function valid(l,x){let D=l.steps.map((s,i)=>colors(15^(s.fixed|(1<<(((x>>>(l.off+2*i))&3)^s.shift)))));if(D.some(a=>!a.length))return false;if(!l.cycle)return true;function rec(i,z){return i===D.length?z===0:D[i].some(y=>rec(i+1,z^y))}return rec(0,0)}
function ref(L,m,pins=[]){let words=[];for(let x=0;x<2**m;x++){if(pins.some(([j,b])=>((x>>>j)&1)!==b))continue;let p=0;for(const l of L)for(let i=0;i<l.steps.length;i++)for(let b=0;b<2;b++)if(x&(1<<(l.off+2*i+b)))p^=l.steps[i].cols[b];if(!p&&L.every(l=>valid(l,x)))words.push(x)}return words}
function witness(L,q,m,pins,chi=0,want=0){let P=pins.slice();for(let j=0;j<m;j++){if(P.some(x=>x[0]===j))continue;let T=[...P,[j,0]],C=solve(L,q,T).count,M=chi?solve(L,q,T,chi).count:C;let n=chi?(C+(want?-M:M))/2n:C;P.push([j,n>0n?0:1])}return P.reduce((x,[j,b])=>x|(b<<j),0)}
let cases=0,sat=0,unsat=0,moments=0,witnesses=0,hulls=0;
for(let z=0;z<80;z++){
 let q=1+rnd(5),L=Array.from({length:3},()=>({cycle:!!rnd(2),steps:Array.from({length:1+rnd(2)},()=>({fixed:rnd(16),shift:rnd(4),cols:[rnd(1<<q),rnd(1<<q)]}))}));let m=prepare(L),W=ref(L,m),cl=close(L,m);cases++;if(W.length)sat++;else unsat++;ok(!cl.unsat||!W.length);ok(W.every(x=>cl.pins.every(([j,b])=>((x>>>j)&1)===b)));
 if(cl.unsat)continue;let C=solve(L,q,cl.pins,0,true).count;ok(C===BigInt(W.length));for(let i=0;i<8;i++){let a=rnd(1<<m);ok(solve(L,q,cl.pins,a,true).count===W.reduce((s,x)=>s+(parity(x&a)?-1n:1n),0n));moments++}
 if(W.length){let x=witness(L,q,m,cl.pins);ok(W.includes(x));witnesses++;
 // All annihilator queries are basis-restricted; use nullspace generators of H.
 let H=[],done=false;while(!done){done=true;let piv=bas(H);let ann=deps(Array.from({length:m},(_,i)=>[piv.reduce((a,v,j)=>a|(((v>>>i)&1)<<j),0),1<<i]));for(let a of ann){stats.fullHullQueries++;let M=solve(L,q,cl.pins,a).count;if(M!== (parity(x&a)?-C:C)){let y=witness(L,q,m,cl.pins,a,1^parity(x&a));ok(W.includes(y));ok(rem(x^y,piv)!==0);H.push(x^y);done=false;break}}}let actual=bas(W.map(y=>y^x));ok(bas(H).length===actual.length&&actual.every(v=>!rem(v,bas(H))));hulls++}
}
// Pure join controls with arbitrary signed tables, including mixed pairwise and triple overlap.
for(let z=0;z<120;z++){let q=1+rnd(7),S=Array.from({length:3},()=>bas(Array.from({length:1+rnd(q)},()=>rnd(1<<q)))),[A,B,C]=S;let make=(a,b,c)=>new Map(span(inter(a,bas([...b,...c]))).map(x=>[x,BigInt(rnd(9)-4)]));let j=join(make(A,B,C),make(B,A,C),A,B,C,q,true);ok(2*(j.t-j.d)<=j.w.reduce((s,x)=>s+x,0))}
let scale=[];for(let q of [2,4,6,8,10,12]){
 let A=Array.from({length:q},(_,i)=>1<<i).reverse(),L=Array.from({length:3},()=>({cycle:false,steps:Array.from({length:q/2},(_,i)=>({fixed:0,shift:0,cols:[1<<(2*i),1<<(2*i+1)]}))}));prepare(L);
 // Analytic closure: each leaf admits all words; every global bit has both supports.
 // q<=12, only unsigned chi=0 on scales (word offsets exceed 31).
 let old=stats.butterflies,j=solve(L,q);ok(j.count===1n<<BigInt(2*q));ok(j.j.d===q&&j.j.t===2*q);let work=stats.butterflies-old;
 let f=new Map([[0,1n]]),g=new Map([[0,1n]]),h=new Map([[1,1n]]);let bad=join(f,g,A,A,A,q).out;ok((join(bad,h,A,A,[],q).out.get(0)||0n)===0n);
 scale.push({q,count:j.count.toString(),pairCandidates:2**(2*q),commonFiberSize:2**q,butterflies:work});
}
return {seed:20261124,cases,sat,unsat,moments,witnesses,hulls,signedJoinControls:120,scale,stats,checks};
}
console.log(JSON.stringify(run(),null,2));
