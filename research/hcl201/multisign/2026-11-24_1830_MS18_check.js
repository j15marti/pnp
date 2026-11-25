"use strict";
function experiment(){
const R={seed:20261124,random:0,sat:0,unsat:0,checks:0,joins:0,gauss:0,closureRows:0,closureUnsat:0,scaling:[],barriers:[]};let seed=R.seed;
function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}
function ck(b){R.checks++;if(!b)throw Error("assert "+R.checks)}
const bit=i=>1n<<BigInt(i), parity=x=>{let p=0;while(x){x&=x-1n;p^=1}return p};
function bits(m){let a=[];while(m){let b=m&-m;a.push(b);m^=b}return a}
function solve(eq,mask){R.gauss++;let p=new Map();for(let [a,b] of eq){if(a&~mask)throw Error("mask");while(a){let k=a&-a;if(!p.has(k)){p.set(k,[a,b]);break}let [c,d]=p.get(k);a^=c;b^=d}if(!a&&b)return null}
let keys=[...p.keys()].sort((a,b)=>a>b?-1:a<b?1:0);function back(x,hom){for(let k of keys){let [a,b]=p.get(k);if(parity(a&x)!==(hom?0:b))x^=k}return x}
return {a:back(0n,false),d:bits(mask).filter(k=>!p.has(k)).map(k=>back(k,true))}}
function basis(ds){let p=new Map();for(let x of ds){while(x){let k=x&-x;if(!p.has(k)){p.set(k,x);break}x^=p.get(k)}}return [...p.values()]}
function proj(s,m){return s?{a:s.a&m,d:basis(s.d.map(x=>x&m))}:null}
function union(a,b){if(!a)return b;if(!b)return a;return {a:a.a,d:basis([...a.d,...b.d,a.a^b.a])}}
function add(a,b){return a&&b?{a:a.a^b.a,d:basis([...a.d,...b.d])}:null}
function equations(s,m){return solve(s.d.map(x=>[x,0]),m).d.map(x=>[x,parity(x&s.a)])}
function contains(s,x){return s&&basis([...s.d,s.a^x]).length===s.d.length}
function same(a,b){return (!a&&!b)||(a&&b&&a.d.length===b.d.length&&contains(a,b.a)&&b.d.every(v=>contains(a,b.a^v)))}
function pins(m,x){return bits(m).map(b=>[b,parity(b&x)])}
function make(widths,pwidths,edges){let n=0;function mask(k){let m=0n;for(let j=0;j<k;j++)m|=bit(n++);return m}
let E=edges.map(([i,j],e)=>({i,j,m:mask(widths[e])}));let V=pwidths.map(k=>({p:mask(k),es:[],terms:[]}));E.forEach((e,k)=>{V[e.i].es.push(k);V[e.j].es.push(k)});for(let v of V){v.em=v.es.reduce((m,e)=>m|E[e].m,0n);v.m=v.p|v.em}return {E,V,n,mask:(1n<<BigInt(n))-1n}}
function packet(g,i,eq){let v=g.V[i],s=solve(eq,v.m);if(!s)return null;let marg={};let d=0;for(let e of v.es){marg[e]=proj(s,g.E[e].m);d+=marg[e].d.length}if(proj(s,v.em).d.length!==d)throw Error("noncartesian");let ker=solve([...eq.map(([a])=>[a,0]),...pins(v.em,0n)],v.m);
return {eq,s,marg,v,base:{a:s.a&v.p,d:ker.d.map(x=>x&v.p)}}}
function lift(t,e,y,g){let v=t.v,m=g.E[e].m,x=(t.s.a&~m)|y;let s=solve([...t.eq,...pins(v.em,x)],v.m);if(!s)throw Error("lift");return (s.a^t.s.a)&v.p}
function contribution(t,s,e,g){R.joins++;let m=g.E[e].m,h=solve([...equations(t.marg[e],m),...equations(s.marg[e],m)],m);if(!h)return null;function F(y){return y^lift(t,e,y,g)^lift(s,e,y,g)}
let a=F(h.a);return {a,d:basis(h.d.map(v=>F(h.a^v)^a))}}
function dp(g){let T=g.V.map((v,i)=>v.terms.map(eq=>packet(g,i,eq)).filter(Boolean));function visit(i,par){let v=g.V[i],out=T[i].map(t=>t.base);for(let e of v.es){let f=g.E[e],j=f.i===i?f.j:f.i;if(j===par)continue;let sub=visit(j,i);out=out.map((a,k)=>{if(!a)return null;let u=null;for(let l=0;l<T[j].length;l++)if(sub[l])u=union(u,add(sub[l],contribution(T[i][k],T[j][l],e,g)));return add(a,u)})}return out}
return visit(0,-1).reduce(union,null)}
function legal(g,x){return g.V.every(v=>v.terms.some(eq=>eq.every(([a,b])=>parity(a&x)===b)))}
function closure(g){let eq=[];while(true){let changed=false;for(let v of g.V){let h=null;for(let t of v.terms)h=union(h,solve([...eq,...t],g.mask));if(!h){R.closureUnsat++;return null}let old=solve(eq,g.mask);for(let row of equations(h,g.mask)){let s=solve([...eq,row],g.mask);if(!s)throw Error("closure");if(s.d.length<old.d.length){eq.push(row);R.closureRows++;changed=true;break}}if(changed)break}if(!changed)return eq}}
function ref(g){let h=null,c=0;for(let x=0n;x<=g.mask;x++)if(legal(g,x)){c++;h=union(h,{a:x,d:[]})}return {h,c}}
function check(g,brute){let cl=closure(g),s=dp(g);if(!cl)ck(!s);if(s){ck(legal(g,s.a));if(cl)ck(cl.every(([a,b])=>parity(a&s.a)===b&&s.d.every(v=>!parity(a&v))))}
if(brute){let r=ref(g);ck(same(s,r.h));return !!s}return s}
for(let z=0;z<100;z++){let n=2+rand(3),edges=Array.from({length:n-1},(_,j)=>[rand(j+1),j+1]);let g=make(edges.map(()=>1+rand(2)),Array(n).fill(1),edges);for(let v of g.V){for(let t=0,L=1+rand(4);t<L;t++){let eq=[];for(let e of v.es){let m=g.E[e].m;if(rand(3))eq.push([bits(m)[rand(bits(m).length)],rand(2)])}if(rand(3))eq.push([v.p|(v.em&&rand(2)?v.em:0n),rand(2)]);v.terms.push(eq);if(rand(5)===0)v.terms.push(eq)}}let sat=check(g,true);R.random++;R[sat?"sat":"unsat"]++}
function color(g,e,c){return bits(g.E[e].m).slice(0,2).map((b,i)=>[b,(c>>i)&1])}
for(let w of [2,8,32,64])for(let sat of [false,true]){let g=make([w,w],[1,1,1],[[0,1],[1,2]]);let [a,b,c]=g.V;
for(let v of [a,c])for(let k=0;k<3;k++)v.terms.push([...color(g,v.es[0],k),[v.p|v.em,0]]);
for(let i=0;i<4;i++)for(let j=0;j<4;j++)if(i===3||j===3||(sat&&i===1&&j===2))b.terms.push([...color(g,0,i),...color(g,1,j),[b.p|b.em,0]]);
b.terms.push(b.terms[0]);let before=R.joins;let s=check(g,w===2?false:false);ck(!!s===sat);if(s)ck(s.d.length===2*w-4);if(w===2)ck(same(s,ref(g).h));R.scaling.push({edgeRank:w,sat,hullRank:s?s.d.length:null,pairJobs:R.joins-before})}
let g=make([1,1],[0,0,0],[[0,1],[1,2]]);g.V[0].terms=[[[g.E[0].m,0]]];g.V[1].terms=[[[g.E[0].m|g.E[1].m,0]]];g.V[2].terms=[[[g.E[1].m,1]]];let declined=false;try{dp(g)}catch(e){declined=e.message==="noncartesian"}ck(declined);ck(!ref(g).h);R.barriers.push("noncartesian equality center: rejected adapter, exhaustive UNSAT");
return R
}
console.log(JSON.stringify(experiment(),null,2));
