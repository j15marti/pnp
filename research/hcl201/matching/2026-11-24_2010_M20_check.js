"use strict";
function main(){
const Z=0n,O=1n; let seed=20261124; const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n};
const stats={assertions:0,lpSolves:0,pivots:0,closurePasses:0,removedTransitions:0,small:[],scale:[]};
function ok(x){stats.assertions++;if(!x)throw Error("assertion "+stats.assertions)}
const abs=x=>x<0n?-x:x;function gcd(a,b){a=abs(a);b=abs(b);while(b){[a,b]=[b,a%b]}return a||1n}
function f(a,b=1n){if(!a)return [0n,1n];if(b<0n){a=-a;b=-b}const g=gcd(a,b);return [a/g,b/g]}
const add=(a,b)=>f(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),neg=a=>[-a[0],a[1]],sub=(a,b)=>add(a,neg(b)),mul=(a,b)=>f(a[0]*b[0],a[1]*b[1]),div=(a,b)=>f(a[0]*b[1],a[1]*b[0]),cmp=(a,b)=>a[0]*b[1]-b[0]*a[1];
function LP(A,b){
 const n=A[0].length,m=A.length;let B=A.map((r,i)=>n+i),T=A.map((r,i)=>[...r.map(x=>f(b[i]<0n?-x:x)),...Array.from({length:m},(_,j)=>f(i===j?O:Z)),f(abs(b[i]))]);const end=n+m;
 function pivot(i,j){const d=T[i][j];T[i]=T[i].map(x=>div(x,d));for(let k=0;k<T.length;k++)if(k!==i&&T[k][j][0]){const z=T[k][j];T[k]=T[k].map((x,l)=>sub(x,mul(z,T[i][l])))}B[i]=j;stats.pivots++}
 function solve(c,limit){stats.lpSolves++;let steps=0;for(;;){if(++steps>10000)throw Error("pivot cap");const r=Array.from({length:limit},(_,j)=>T.reduce((v,row,i)=>sub(v,mul(c[B[i]],row[j])),c[j]));let j=r.findIndex(x=>x[0]>0n);if(j<0){const x=Array.from({length:end},()=>f(Z));B.forEach((v,i)=>x[v]=T[i][end]);return {x,v:x.reduce((s,y,i)=>add(s,mul(y,c[i])),f(Z))}}let i=-1,ratio;for(let k=0;k<T.length;k++)if(T[k][j][0]>0n){let t=div(T[k][end],T[k][j]);if(i<0||cmp(t,ratio)<0n||(cmp(t,ratio)===0n&&B[k]<B[i])){i=k;ratio=t}}if(i<0)throw Error("unbounded");pivot(i,j)}}
 const first=solve(Array.from({length:end},(_,j)=>f(j<n?Z:-O)),end);if(first.v[0]<0n)return null;ok(first.v[0]===0n);
 for(let i=T.length-1;i>=0;i--)if(B[i]>=n){ok(T[i][end][0]===0n);let j=T[i].slice(0,n).findIndex(x=>x[0]!==0n);if(j>=0)pivot(i,j);else{T.splice(i,1);B.splice(i,1)}}
 return c=>{const r=solve([...c.map(f0=>f(f0)),...Array.from({length:m},()=>f(Z))],n);ok(r.x.slice(0,n).every(x=>x[0]>=0n));for(let i=0;i<A.length;i++)ok(cmp(A[i].reduce((s,a,j)=>add(s,mul(f(a),r.x[j])),f(Z)),f(b[i]))===0n);return r}
}
const plus=(a,b)=>[a[0]+b[0],a[1]+b[1]],minus=(a,b)=>[a[0]-b[0],a[1]-b[1]],dot=(a,b)=>a[0]*b[0]+a[1]*b[1],cross=(a,b)=>a[0]*b[1]-a[1]*b[0],eq=(a,b)=>a[0]===b[0]&&a[1]===b[1];
function basis(xs){const b=[];for(let x of xs){for(const y of b)if((x^y)<x)x^=y;if(x){b.push(x);b.sort((a,b)=>a>b?-1:a<b?1:0)}}return b}
function inspan(x,b){for(const y of b)if((x^y)<x)x^=y;return !x}
function cbasis(xs){const b=[];for(const x of xs)if((x[0]||x[1])&&(!b.length||(b.length===1&&cross(x,b[0])!==0n)))b.push(x);return b}
function build(blocks,target,untag=false){
 const states=[],tr=[];function state(key){let s={id:states.length,key,ts:[]};states.push(s);return s}
 function trans(s,ch,c,word){let t={id:tr.length,s,ch,c,word};tr.push(t);s.ts.push(t);return t}
 function tree(l,r){const map=new Map();const get=k=>{if(!map.has(k))map.set(k,state(k));return map.get(k)};
 if(r-l===1){blocks[l].forEach((a,j)=>trans(get(untag?0:a[0]),[],a[1],1n<<BigInt(3*l+j)));return map}
 const m=(l+r)>>1,A=tree(l,m),B=tree(m,r);for(const a of A.values())for(const b of B.values())trans(get(a.key^b.key),[a,b],[Z,Z],Z);return map}
 const root=tree(0,blocks.length).get(target);return {states,tr,root}
}
function hull(g,allow=null,dir=null){
 stats.closurePasses++;const h=new Map(),chosen=new Set();for(const s of g.states){let p=null;for(const t of s.ts){if(allow&&!allow.has(t.id))continue;const kids=t.ch.map(x=>h.get(x.id));if(kids.some(x=>!x))continue;
 let q={count:1n,r:t.word,b:[],cost:t.c,cb:[],val:dir?dot(t.c,dir):Z};
 for(const k of kids){q.count*=k.count;q.r^=k.r;q.b=basis([...q.b,...k.b]);q.cost=plus(q.cost,k.cost);q.cb=cbasis([...q.cb,...k.cb]);q.val+=k.val}
 if(!p||dir&&q.val>p.val){p=q;p.t=[t]}else if(!dir||q.val===p.val){p.count+=q.count;p.b=basis([...p.b,...q.b,p.r^q.r]);p.cb=cbasis([...p.cb,...q.cb,minus(q.cost,p.cost)]);p.t.push(t)}
 }if(p)h.set(s.id,p)}
 const root=g.root&&h.get(g.root.id);if(root){const seen=new Set();function walk(s){if(seen.has(s.id))return;seen.add(s.id);for(const t of h.get(s.id).t){chosen.add(t.id);t.ch.forEach(walk)}}walk(g.root)}return {root,chosen}
}
function reference(g){
 if(!g.root)return [];const memo=new Map();function rec(s){if(memo.has(s.id))return memo.get(s.id);const out=[];for(const t of s.ts){if(!t.ch.length)out.push({c:t.c,r:t.word,ids:[t.id]});else for(const a of rec(t.ch[0]))for(const b of rec(t.ch[1]))out.push({c:plus(a.c,b.c),r:a.r^b.r,ids:[...a.ids,...b.ids,t.id]})}memo.set(s.id,out);return out}return rec(g.root)
}
// Independent planar convex hull reference, only small two-dimensional audits.
function face(ref,Q){const pts=[...new Map(ref.map(a=>[a.c.join(","),a.c])).values()].sort((a,b)=>a[0]<b[0]?-1:a[0]>b[0]?1:a[1]<b[1]?-1:a[1]>b[1]?1:0);
 if(!pts.length)return null;if(pts.length===1)return eq(pts[0],Q)?ref:null;
 const turn=(a,b,c)=>cross(minus(b,a),minus(c,a));function chain(a){const h=[];for(const p of a){while(h.length>=2&&turn(h[h.length-2],h[h.length-1],p)<=0n)h.pop();h.push(p)}return h}
 const h=[...chain(pts).slice(0,-1),...chain([...pts].reverse()).slice(0,-1)];if(h.length===2){const [a,b]=h;if(turn(a,b,Q)!==0n||dot(minus(Q,a),minus(Q,b))>0n)return null;return eq(Q,a)||eq(Q,b)?ref.filter(x=>eq(x.c,Q)):ref}
 let out=ref;for(let i=0;i<h.length;i++){const a=h[i],b=h[(i+1)%h.length],s=turn(a,b,Q);if(s<0n)return null;if(!s)out=out.filter(x=>turn(a,b,x.c)===0n)}return out
}
function sameHull(h,ref){ok(h.count===BigInt(ref.length));const b=basis(ref.map(x=>x.r^ref[0].r));ok(h.b.length===b.length&&h.b.every(x=>inspan(x,b))&&inspan(h.r^ref[0].r,b));ok(ref.some(x=>x.r===h.r))}
function run(blocks,tag,Q,name){
 const u=build(blocks,0,true);hull(u);const g=build(blocks,tag),pre=hull(g),ref=reference(g),actual=ref.filter(x=>eq(x.c,Q)),expected=face(ref,Q);
 let answer="UNSAT",dim=null,removed=0;
 if(pre.root){sameHull(pre.root,ref);const ts=g.tr.filter(t=>pre.chosen.has(t.id)),states=g.states.filter(s=>ts.some(t=>t.s===s));
 const A=states.map(s=>ts.map(t=>BigInt((t.s===s?1:0)-t.ch.filter(k=>k===s).length))),b=states.map(s=>s===g.root?O:Z);
 for(let j=0;j<2;j++){A.push(ts.map(t=>t.c[j]));b.push(Q[j])}const lp=LP(A,b);
 ok(!!lp===!!expected);
 if(lp){let keep=new Set();for(let j=0;j<ts.length;j++){const r=lp(ts.map((_,i)=>i===j?O:Z));if(r.v[0]>0n)keep.add(ts[j].id)}
 const want=new Set(expected.flatMap(x=>x.ids));ok(keep.size===want.size&&[...keep].every(x=>want.has(x)));removed=ts.length-keep.size;stats.removedTransitions+=removed;
 const post=hull(g,keep);sameHull(post.root,expected);dim=post.root.cb.length;ok(actual.every(x=>x.ids.every(i=>keep.has(i))));
 if(dim===0){ok(eq(post.root.cost,Q));answer="SAT";sameHull(post.root,actual)}
 else {answer="UNKNOWN";if(actual.length&&eq(post.root.cost,Q))answer="SAT"}
 const re=hull(g,post.chosen);sameHull(re.root,expected);
 }
 }else ok(!expected&&!actual.length);
 if(answer==="SAT")ok(actual.length>0);if(answer==="UNSAT")ok(!actual.length);stats.small.push({name,actual:actual.length,coarse:ref.length,face:expected?.length??0,dim,removed,answer})
}
const B=(x,y,z=0)=>[z,[BigInt(x),BigInt(y)]];
run([[B(0,4),B(4,0),B(3,3)]],0,[3n,3n],"oblique vertex");
run([[B(0,4),B(4,0),B(3,3)]],0,[4n,3n],"oblique outside");
run([[B(0,4),B(4,0),B(3,3)]],0,[2n,2n],"face hole");
run([[B(0,4),B(4,0),B(3,3)],[B(0,0),B(0,0)]],0,[3n,3n],"vertex multiple witnesses");
for(let i=0;i<32;i++){const blocks=Array.from({length:2+rnd(3)},()=>Array.from({length:2+rnd(2)},()=>B(rnd(7)-3,rnd(7)-3,rnd(4))));let tag=rnd(4),Q=[BigInt(rnd(13)-6),BigInt(rnd(13)-6)];if(i%2===0){tag=0;Q=[Z,Z];for(const block of blocks){const o=block[rnd(block.length)];tag^=o[0];Q=plus(Q,o[1])}}run(blocks,tag,Q,"seeded-"+i)}
for(const k of [8,16,32,64]){const blocks=[],L=1n<<BigInt(8*k);let s=Z;for(let i=0;i<k;i++){const a=L+BigInt(i);s+=a;blocks.push([B(0n,4n*a),B(4n*a,0n),B(3n*a,3n*a)])}for(let i=0;i<k;i++)blocks.push([B(0,0),B(0,0)]);const g=build(blocks,0),pre=hull(g),best=hull(g,null,[O,O]),Q=[3n*s,3n*s];ok(best.root.val===dot(Q,[O,O]));ok(best.root.val<dot(plus(Q,[O,Z]),[O,O]));const h=hull(g,best.chosen);ok(h.root.cb.length===0&&eq(h.root.cost,Q)&&h.root.count===O<<BigInt(k)&&h.root.b.length===k);ok(pre.root.count===6n**BigInt(k));stats.scale.push({k,weightBits:L.toString(2).length,quotaDefect:s.toString(),count:h.root.count.toString(),rank:h.root.b.length,removed:pre.chosen.size-best.chosen.size,neighbor:"UNSAT",method:"supplied integer direction; exact max-plus DP"})}
return stats
}
console.log(JSON.stringify(main(),null,2));
