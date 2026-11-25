function run(){
let seed=20261124;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
const abs=x=>x<0n?-x:x,gcd=(x,y)=>{x=abs(x);y=abs(y);while(y){[x,y]=[y,x%y]}return x};
const singleton=x=>({a:x,g:0n,lo:x,hi:x});
const add=(a,b)=>({a:a.a+b.a,g:gcd(a.g,b.g),lo:a.lo+b.lo,hi:a.hi+b.hi});
const union=(a,b)=>a?({a:a.a,g:gcd(gcd(a.g,b.g),a.a-b.a),lo:a.lo<b.lo?a.lo:b.lo,hi:a.hi>b.hi?a.hi:b.hi}):b;
const ok=(a,x)=>!!a&&x>=a.lo&&x<=a.hi&&(a.g===0n?x===a.a:(x-a.a)%a.g===0n);
const put=(map,k,v)=>map.set(k,union(map.get(k),v));
let stats={cases:0,sat:0,unsat:0,assertions:0,reference:0,closureScans:0,deletions:0,coarseJoins:0,outsideJoins:0,exactJoins:0,peakKeys:0};
const assert=x=>{stats.assertions++;if(!x)throw Error("mismatch")};
function solve(blocks,target,tag){
 const opts=blocks.map(b=>b.map((o,i)=>({...o,i})));
 function build(l,r){
  const n={l,r,in:new Map(),out:new Map(),exact:new Map()};
  if(r-l===1){for(const o of opts[l])put(n.in,o.t,singleton(o.q))}
  else {const m=(l+r)>>1;n.a=build(l,m);n.b=build(m,r);
    for(const [x,u] of n.a.in)for(const [y,v] of n.b.in){stats.coarseJoins++;put(n.in,x^y,add(u,v))}}
  return n;
 }
 function outside(n){
  if(!n.a)return;
  for(const [p,e] of n.out){
   for(const [x,u] of n.a.in){const y=p^x,v=n.b.in.get(y);if(v){stats.outsideJoins++;put(n.a.out,x,add(e,v));put(n.b.out,y,add(e,u))}}
  }
  outside(n.a);outside(n.b);
 }
 function find(n){if(n.a)return find(n.a)||find(n.b);
  for(const o of opts[n.l]){stats.closureScans++;if(!ok(n.out.get(o.t),target-o.q))return [n.l,o.i]}
  return null;
 }
 let root;
 for(;;){
   if(opts.some(b=>!b.length))return {c:0n,w:null};
   root=build(0,opts.length);
   if(!ok(root.in.get(tag),target))return {c:0n,w:null};
   root.out.set(tag,singleton(0n));outside(root);
   const bad=find(root);if(!bad)break;
   stats.deletions++;opts[bad[0]]=opts[bad[0]].filter(o=>o.i!==bad[1]);
 }
 function fill(n){
  function keep(t,q,c,w){if(!ok(n.out.get(t),target-q))return;const k=t+":"+q;const old=n.exact.get(k);if(old)old.c+=c;else n.exact.set(k,{t,q,c,w})}
  if(!n.a){for(const o of opts[n.l])keep(o.t,o.q,1n,[o.i])}
  else{fill(n.a);fill(n.b);for(const a of n.a.exact.values())for(const b of n.b.exact.values()){stats.exactJoins++;keep(a.t^b.t,a.q+b.q,a.c*b.c,a.w.concat(b.w))}}
  stats.peakKeys=Math.max(stats.peakKeys,n.exact.size);
 }
 fill(root);return root.exact.get(tag+":"+target)||{c:0n,w:null};
}
function ref(b,q,t){let c=0n;function go(i,a,s){if(i===b.length){stats.reference++;if(a===q&&s===t)c++;return}for(const o of b[i])go(i+1,a+o.q,s^o.t)}go(0,0n,0);return c}
function test(b,q,t,expected){
 const a=solve(b,q,t),c=expected===undefined?ref(b,q,t):expected;assert(a.c===c);stats.cases++;if(c){stats.sat++;assert(a.w.length===b.length);let v=0n,s=0;for(let i=0;i<b.length;i++){const o=b[i][a.w[i]];v+=o.q;s^=o.t}assert(v===q&&s===t)}else stats.unsat++;
 return a.c.toString();
}
for(let i=0;i<200;i++){const b=Array.from({length:2+rnd(7)},()=>Array.from({length:2+rnd(2)},()=>({q:BigInt(rnd(31)-15),t:rnd(8)})));let q=BigInt(rnd(61)-30),t=rnd(8);if(i%2===0){q=0n;t=0;for(const x of b){const o=x[rnd(x.length)];q+=o.q;t^=o.t}}test(b,q,t)}
const random={...stats};const scaling=[];const comb=(n,k)=>{let a=1n;for(let i=1;i<=k;i++)a=a*BigInt(n-i+1)/BigInt(i);return a};
for(const n of [4,8,16,32,64]){const M=(1n<<128n)+1n;const b=Array.from({length:2*n},(_,i)=>[{q:0n,t:0},{q:M+BigInt(i>=n),t:0}]);const q=M*BigInt(n)+BigInt(n/2);const prev=stats.exactJoins;const count=test(b,q,0,comb(n,n/2)**2n);test(b,M*BigInt(n)+BigInt(n+1),0,0n);scaling.push({n,coefficient:M.toString(),target:q.toString(),count,exactJoins:stats.exactJoins-prev,peakKeysSoFar:stats.peakKeys})}
return {seed:20261124,random,total:stats,scaling};
}
console.log(JSON.stringify(run(),null,2));
