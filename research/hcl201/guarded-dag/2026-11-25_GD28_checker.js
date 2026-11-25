const fs=require('fs');
function experiment(data){
let seed=20261125, checks=0; const rng=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n;};
const assert=x=>{checks++;if(!x)throw Error("assertion "+checks)};
function parity(x){let b=0;while(x){b^=1;x&=x-1}return b}
function basis(xs){let p=new Map;for(let x of xs){while(x){let k=31-Math.clz32(x);if(p.has(k))x^=p.get(k);else{p.set(k,x);break}}}return [...p.values()]}
function inter(U,V){let p=new Map, out=[];for(let v of basis(V))p.set(31-Math.clz32(v),[v,0]);for(let a of basis(U)){let v=a,t=a;while(v){let k=31-Math.clz32(v);if(p.has(k)){let [b,c]=p.get(k);v^=b;t^=c}else{p.set(k,[v,t]);break}}if(!v&&t)out.push(t)}return basis(out)}
function solve(eq){let p=new Map;for(let [v,b] of eq){while(v){let k=31-Math.clz32(v);if(p.has(k)){let [a,c]=p.get(k);v^=a;b^=c}else{p.set(k,[v,b]);break}}if(!v&&b)return null}let x=0;for(let k of [...p.keys()].sort((a,b)=>a-b)){let [v,b]=p.get(k);if(parity(v&x)!==b)x|=1<<k}return x}
const leaf=(rows,neg=false)=>({rows,neg});
const join=(a,b,op="and")=>({a,b,op});
function tree(L,op="and"){if(L.length===1)return L[0];let m=L.length>>1;return join(tree(L.slice(0,m),op),tree(L.slice(m),op),op)}
function val(t,x){if(t.rows){let p=t.rows.every(([v,b])=>parity(x&v)===b);return +(t.neg?!p:p)}return t.op==="and"?val(t.a,x)&val(t.b,x):val(t.a,x)|val(t.b,x)}
function dp(t,cap=12){let width=0,states=0,pairs=0,systems=0;function acquire(v){v.span=v.rows?basis(v.rows.map(e=>e[0])):basis([...acquire(v.a),...acquire(v.b)]);return v.span}
acquire(t);
function rec(v,out){let B=inter(v.span,out);width=Math.max(width,B.length);if(B.length>cap)throw Error("cap");let A=new Map;
function put(k,z,eq){let id=2*k+z;if(!A.has(id)){A.set(id,eq);states++}}
if(v.rows){for(let k=0;k<1<<B.length;k++){let eq=B.map((b,j)=>[b,(k>>j)&1]);let e=[...eq,...v.rows];systems++;if(solve(e)!==null)put(k,+!v.neg,e);for(let [a,b] of v.rows){let e=[...eq,[a,b^1]];systems++;if(solve(e)!==null){put(k,+v.neg,e);break}}}}else{let L=rec(v.a,basis([...out,...v.b.span])),R=rec(v.b,basis([...out,...v.a.span]));for(let [i,l] of L)for(let [j,r] of R){pairs++;let e=[...l,...r];systems++;let x=solve(e);if(x===null)continue;let k=B.reduce((s,b,h)=>s|(parity(b&x)<<h),0);let z=v.op==="and"?(i&1)&(j&1):(i&1)|(j&1);put(k,z,e)}}
return A}
let a=rec(t,[]);return {width,states,pairs,systems,yes:a.has(1),no:a.has(0),witness:a.has(1)?solve(a.get(1)):null,counter:a.has(0)?solve(a.get(0)):null}}
function control(t,n){let r=dp(t),yes=0,no=0;for(let x=0;x<1<<n;x++){if(val(t,x))yes++;else no++}assert(r.yes===(yes>0));assert(r.no===(no>0));if(r.yes)assert(val(t,r.witness)===1);if(r.no)assert(val(t,r.counter)===0);return {...r,yesCount:yes,noCount:no}}
let shared={};for(let k of ["raw","wide"]){let p=data[k].gauge.packets;shared[k]=control(tree(p.map(r=>leaf(r,true))),data[k].gauge.exterior.length);shared[k].exterior=data[k].gauge.exterior;shared[k].packets=p}
let random={sat:0,unsat:0,tautology:0,maxWidth:0,pairs:0};for(let i=0;i<150;i++){let n=7,ls=Array.from({length:2+rng(8)},()=>leaf(Array.from({length:1+rng(4)},()=>[1+rng(127),rng(2)]),!!rng(2)));let t=ls.shift();for(let l of ls)t=join(t,l,rng(2)?"and":"or");let a=control(t,n);random[a.yes?"sat":"unsat"]++;random.tautology+=+!a.no;random.maxWidth=Math.max(random.maxWidth,a.width);random.pairs+=a.pairs}
let independent=[];for(let k of [1,2,4,8]){let L=[];for(let i=0;i<k;i++){let a=1<<(2*i),b=1<<(2*i+1);L.push(join(leaf([[a,0],[b,0]]),leaf([[a,1],[b,1]]),"or"))}independent.push({k,...control(tree(L),2*k)})}
let opposite=control(join(leaf([[3,0]]),leaf([[3,1]])),2);
return {checks,shared,random,independent,opposite,scope:"BS20 learned exterior exclusions only; uncovered words not certified source models. No full source replay or full closure. Small masks and exhaustive reference only."}
}
const data=JSON.parse(fs.readFileSync(process.argv[2],'utf8')); console.log(JSON.stringify(experiment(data),null,2));
