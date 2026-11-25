function main(){
const bit=i=>1n<<BigInt(i), top=x=>x.toString(2).length-1;
function add(B,x){while(x){let k=top(x);if(B.has(k))x^=B.get(k);else{B.set(k,x);return;}}}
function has(B,x){while(x){let k=top(x);if(!B.has(k))return false;x^=B.get(k);}return true;}
function span(xs){let B=new Map();for(let x of xs)add(B,x);return B;}
function ins(T,v,h,c,rep,bases){let key=v.toString()+":"+h, a=T.get(key);if(!a){a={v,h,c:0n,rep,B:new Map()};T.set(key,a);}a.c+=c;add(a.B,a.rep^rep);for(let B of bases)for(let x of B.values())add(a.B,x);}
let stat={calls:0,nodes:0,pairs:0,overlapReject:0,cosetReject:0,peakTable:0,peakHullRank:0,assertions:0};
function check(x){stat.assertions++;if(!x)throw Error("assertion "+stat.assertions);}
function dp(n,E,t,h,pins=new Map(),tagged=true,quota=true){
 stat.calls++;const mask=bit(n)-1n, target=mask|(tagged?t<<BigInt(n):0n), m=E.length;
 const cols=E.map(e=>bit(e.u)|bit(e.v)|(tagged?e.g<<BigInt(n):0n));
 const R=span(cols).size;let width=0,localPeak=0,pairs=0;
 function rec(l,r){
  stat.nodes++;const A=span(cols.slice(l,r)), C=span(cols.slice(0,l).concat(cols.slice(r)));
  const w=A.size+C.size-R;width=Math.max(width,w);
  const T=new Map();const accept=v=>{if(has(C,target^v))return true;stat.cosetReject++;return false;};
  if(r-l===1){for(let x=0;x<=1;x++)if((!pins.has(l)||pins.get(l)===x)&&accept(x?cols[l]:0n))ins(T,x?cols[l]:0n,quota?x*E[l].h:0,1n,x?bit(l):0n,[]);}
  else if(r===l){if(accept(0n))ins(T,0n,0,1n,0n,[]);}
  else{const mid=(l+r)>>1,L=rec(l,mid),Q=rec(mid,r);for(let a of L.values())for(let b of Q.values()){
    pairs++;stat.pairs++;if((a.v&b.v&mask)!==0n){stat.overlapReject++;continue;}let v=a.v^b.v;if(!accept(v))continue;
    ins(T,v,a.h+b.h,a.c*b.c,a.rep|b.rep,[a.B,b.B]);
  }}
  localPeak=Math.max(localPeak,T.size);stat.peakTable=Math.max(stat.peakTable,T.size);for(let a of T.values())stat.peakHullRank=Math.max(stat.peakHullRank,a.B.size);
  return T;
 }
 const root=rec(0,m),a=root.get(target.toString()+":"+(quota?h:0));return {a,width,localPeak,pairs};
}
function ref(n,E,t,h,pins=new Map(),tagged=true,quota=true){
 let arr=[];function dfs(occ,g,w,x){if(occ===bit(n)-1n){if((!tagged||g===t)&&(!quota||w===h)&&[...pins].every(([i,b])=>Number((x>>BigInt(i))&1n)===b))arr.push(x);return;}
 let u=0;while(occ&bit(u))u++;E.forEach((e,i)=>{if((e.u===u||e.v===u)&&!(occ&(bit(e.u)|bit(e.v)))&&pins.get(i)!==0)dfs(occ|bit(e.u)|bit(e.v),g^e.g,w+e.h,x|bit(i));});}dfs(0n,0n,0,0n);return arr;
}
function compare(d,a){check((d.a?.c??0n)===BigInt(a.length));if(a.length){check(a.includes(d.a.rep));let B=span(a.map(x=>x^a[0]));check(B.size===d.a.B.size);check([...d.a.B.values()].every(x=>has(B,x)));}}
function pinsOf(a,m){let p=new Map();if(!a)return p;let varying=0n;for(let x of a.B.values())varying|=x;for(let i=0;i<m;i++)if(!(varying&bit(i)))p.set(i,Number((a.rep>>BigInt(i))&1n));return p;}
function witness(n,E,t,h,x,quota=true){let o=0n,g=0n,w=0;for(let i=0;i<E.length;i++)if(x&bit(i)){let e=E[i],b=bit(e.u)|bit(e.v);check(!(o&b));o|=b;g^=e.g;w+=e.h;}check(o===bit(n)-1n&&g===t&&(!quota||w===h));}
let seed=20261124;function rnd(k){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%k;}
let random={systems:0,targets:0,sat:0,unsat:0,referenceMatches:0,untaggedPins:0,taggedPins:0,closureRechecks:0};
for(let z=0;z<80;z++){let n=4+2*rnd(3),E=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(rnd(100)<40)E.push({u,v,g:BigInt(rnd(8)),h:rnd(4)});if(z%4===0)E.push({u:0,v:1,g:BigInt(rnd(8)),h:rnd(4)});
 let P=new Map();if(E.length&&z%5===0)P.set(rnd(E.length),rnd(2));let d0=dp(n,E,0n,0,P,false,false),a0=ref(n,E,0n,0,P,false,false);compare(d0,a0);random.systems++;
 let p0=pinsOf(d0.a,E.length);random.untaggedPins+=p0.size;for(let [i,b] of P)p0.set(i,b);
 let targets=[];if(a0.length){let x=a0[rnd(a0.length)],t=0n,h=0;E.forEach((e,i)=>{if(x&bit(i)){t^=e.g;h+=e.h;}});targets.push([t,h]);}
 while(targets.length<4)targets.push([BigInt(rnd(8)),rnd(3*n/2+1)]);
 for(let [t,h] of targets){let d=dp(n,E,t,h,p0),a=ref(n,E,t,h,P);compare(d,a);random.targets++;random.referenceMatches+=a.length;if(a.length){random.sat++;witness(n,E,t,h,d.a.rep);let p=pinsOf(d.a,E.length);random.taggedPins+=p.size;for(let [i,b] of p0)p.set(i,b);let dd=dp(n,E,t,h,p);compare(dd,a);random.closureRechecks++;}else random.unsat++;}
}
function chain(k){let E=[];for(let j=0;j<k;j++)for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)E.push({u:4*j+u,v:4*j+v,g:u===0?(v===1?bit(j):v===2?bit(j+1):0n):0n,h:0});return E;}
function fib(k){let a=0n,b=1n;for(let j=0;j<k;j++)[a,b]=[b,a+b];return a;}
let scaling=[];
for(let k of [4,8,16,32,64]){let E=chain(k),n=4*k,all=bit(k+1)-1n;let d0=dp(n,E,0n,0,new Map(),false,false);check(d0.a.c===3n**BigInt(k));let p=pinsOf(d0.a,E.length);check(p.size===0);
 let no=dp(n,E,all,0,p),yes=dp(n,E,all^bit(k>>1),0,p),zero=dp(n,E,0n,0,p);
 check(!no.a);check(yes.a.c===1n);check(zero.a.c===fib(k+1));witness(n,E,all^bit(k>>1),0,yes.a.rep);witness(n,E,0n,0,zero.a.rep);
 let p1=pinsOf(yes.a,E.length);check(p1.size===E.length);let again=dp(n,E,all^bit(k>>1),0,p1);check(again.a.c===1n&&again.a.rep===yes.a.rep);
 scaling.push({blocks:k,edges:E.length,globalSharedTagRank:k-1,rawCutWidth:Math.max(no.width,yes.width,zero.width),peakTable:Math.max(no.localPeak,yes.localPeak,zero.localPeak),zeroTargetCount:String(zero.a.c),zeroHullRank:zero.a.B.size,nearUnsatCount:String(yes.a.c),unsatCount:"0",untaggedHullRank:d0.a.B.size});
}
return {seed:20261124,random,scaling,stat,scope:"Raw joint-column spans; exact DP and affine hull. Random reference independent vertex recursion; scaling formula controls. No physical source compiler or branch-width optimizer."};
}
console.log(JSON.stringify(main(), null, 2));
