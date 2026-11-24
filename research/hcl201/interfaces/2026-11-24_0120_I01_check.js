function runI01(){
const bit=i=>1n<<BigInt(i),all=n=>bit(n)-1n;
let seed=20261124;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
const assert=(x,m)=>{if(!x)throw Error(m)};
function basis(xs){const b=[];for(let x of xs){while(x){const i=x.toString(2).length-1;if(b[i])x^=b[i];else{b[i]=x;break}}}return b.filter(Boolean)}
function contains(b,x){for(let i=b.length-1;i>=0;i--){const y=b[i];if((x^y)<x)x^=y}return x===0n}
function hull(s){const a=s[0];return {a,b:basis(s.map(x=>x^a))}}
function sumHull(ss){let a=0n,bs=[];for(const s of ss){const h=hull(s);a^=h.a;bs.push(...h.b)}return {a,b:basis(bs)}}
function split(n,edges,h){const incidence=Array.from({length:n},()=>new Set());for(const [u,v,g,r] of edges){incidence[u].add(r);incidence[v].add(r)}
const map=Array.from({length:n},()=>new Map()),out=[];let N=n,H=h;
for(let v=0;v<n;v++){const rs=[...incidence[v]].sort((a,b)=>a-b);if(rs.length<=2){for(const r of rs)map[v].set(r,v);continue}
const cs=[v];for(let i=1;i<rs.length;i++)cs.push(N++);const t=H++;rs.forEach((r,i)=>map[v].set(r,cs[i]));
for(let i=0;i<cs.length-1;i++){const a=N++;out.push([cs[i],a,0,t],[a,cs[i+1],0,t])}}
for(const [u,v,g,r] of edges)out.push([map[u].get(r),map[v].get(r),g,r]);return {n:N,edges:out,h:H}}
function supports(n,edges,h){const inc=Array.from({length:n},()=>new Set()),rs=Array.from({length:h},()=>[]);for(const e of edges){rs[e[3]].push(e);inc[e[0]].add(e[3]);inc[e[1]].add(e[3])}
return rs.map((es,r)=>{let need=0n;for(let v=0;v<n;v++)if(inc[v].size===1&&inc[v].has(r))need|=bit(v);const s=new Set();
function go(i,o,g){if(i===es.length){if((o&need)===need)s.add(o|(BigInt(g)<<BigInt(n)));return}go(i+1,o,g);const [u,v,t]=es[i],m=bit(u)|bit(v);if(!(o&m))go(i+1,o|m,g^t)}
go(0,0n,0);return [...s]})}
function ref(n,edges){const adj=Array.from({length:n},()=>[]);for(const [u,v,g] of edges){adj[u].push([v,g]);adj[v].push([u,g])}const out=new Set();
function go(mask,g){if(!mask){out.add(g);return}let u=0;while(!(mask&bit(u)))u++;for(const [v,t] of adj[u])if(mask&bit(v))go(mask^bit(u)^bit(v),g^t)}go(all(n),0);return out}
function solve(ss,target,doClosure=true){let s=ss.map(x=>x.slice()),removed=0,passes=0,trans=0,peak=1,width=0;if(s.some(x=>!x.length))return {ok:false,removed,passes,trans,peak:0,width};
if(doClosure){let ch=true;while(ch){passes++;ch=false;const whole=sumHull(s);if(!contains(whole.b,target^whole.a))return {ok:false,removed,passes,trans,peak:0,width};
for(let i=0;i<s.length;i++){const other=sumHull(s.filter((_,j)=>i!==j));const a=s[i].filter(x=>contains(other.b,target^x^other.a));if(a.length!==s[i].length){removed+=s[i].length-a.length;s[i]=a;ch=true}if(!a.length)return {ok:false,removed,passes,trans,peak:0,width}}}}
const suff=Array.from({length:s.length+1},(_,i)=>sumHull(s.slice(i)));let dp=new Set([0n]);for(let i=0;i<s.length;i++){const pref=sumHull(s.slice(0,i+1));const oth=suff[i+1];const k=pref.b.length+oth.b.length-basis([...pref.b,...oth.b]).length;width=Math.max(width,k);const next=new Set();for(const x of dp)for(const y of s[i]){trans++;const z=x^y;if(contains(oth.b,target^z^oth.a))next.add(z)}assert(BigInt(next.size)<=bit(k),"state bound");peak=Math.max(peak,next.size);dp=next;if(!dp.size)break}return {ok:dp.has(target),removed,passes,trans,peak,width}}
function dummySupport(n,es,boundary){let D=n+boundary.length;const ee=es.map(e=>e.slice());for(let j=0;j<boundary.length;j++)ee.push([boundary[j],n+j,0,0]);if(D%2)D++;for(let i=n;i<D;i++)for(let j=i+1;j<D;j++)ee.push([i,j,0,0]);const adj=Array.from({length:D},()=>[]);ee.forEach(([u,v,g],i)=>{adj[u].push([v,g,i]);adj[v].push([u,g,i])});const out=new Set();function go(mask,o,g){if(!mask){out.add(o|(BigInt(g)<<BigInt(n)));return}let u=0;while(!(mask&bit(u)))u++;for(const [v,t,i] of adj[u])if(mask&bit(v)){const old=i<es.length;go(mask^bit(u)^bit(v),old?o|bit(u)|bit(v):o,old?g^t:g)}}go(all(D),0n,0);return out}
const stats={seed:20261124,graphs:0,targets:0,sat:0,unsat:0,wrong:0,uncorrectedFalsePositives:0,graphsWithFalsePositive:0,closureRemoved:0,closurePasses:0,transitions:0,maxLive:0,maxCutWidth:0,dummyChecks:0,gaugeChecks:0,controls:[]};
function test(n,es,h){const r=ref(n,es),t=split(n,es,h),s=supports(t.n,t.edges,t.h),raw=supports(n,es,h);let bad=false;stats.graphs++;
for(let c=0;c<8;c++){const target=all(t.n)|(BigInt(c)<<BigInt(t.n)),ans=solve(s,target),expect=r.has(c);assert(ans.ok===expect,"decision mismatch");const wrong=solve(raw,all(n)|(BigInt(c)<<BigInt(n)),false).ok&&!expect;if(wrong){stats.uncorrectedFalsePositives++;bad=true}stats.targets++;stats[expect?"sat":"unsat"]++;stats.closureRemoved+=ans.removed;stats.closurePasses+=ans.passes;stats.transitions+=ans.trans;stats.maxLive=Math.max(stats.maxLive,ans.peak);stats.maxCutWidth=Math.max(stats.maxCutWidth,ans.width)}if(bad)stats.graphsWithFalsePositive++;
if(s.every(x=>x.length)){const p=Array.from({length:t.n},()=>rnd(8)),shear=z=>{let g=0;for(let v=0;v<t.n;v++)if(z&bit(v))g^=p[v];return z^(BigInt(g)<<BigInt(t.n))};const sg=s.map(x=>x.map(shear));for(let i=0;i<=s.length;i++){const W=arr=>{const a=sumHull(arr.slice(0,i)),b=sumHull(arr.slice(i));return a.b.length+b.b.length-basis([...a.b,...b.b]).length};assert(W(s)===W(sg),"gauge rank");stats.gaugeChecks++}}
return {splitVertices:t.n,regions:t.h,syndromes:[...r].sort((a,b)=>a-b)}}
for(let d of [3,5,7,9]){const n=d+1,es=Array.from({length:d},(_,i)=>[0,i+1,0,i]);const t=split(n,es,d),s=supports(t.n,t.edges,t.h); // path enumeration for d=31 would be exponential: handled analytically below
if(d>=15)break;const a=solve(s,all(t.n)),raw=solve(supports(n,es,d),all(n),false);assert(!a.ok&&raw.ok,"star");stats.controls.push({d,splitVertices:t.n,splitUnsat:!a.ok,rawFalseSat:raw.ok,closureRemoved:a.removed,transitions:a.trans})}
for(let i=0;i<220;i++){const n=4+2*rnd(3),h=3+rnd(2),es=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(rnd(100)<40)es.push([u,v,rnd(8),rnd(h)]);if(i%3===0){for(let u=0;u<n;u+=2)if(!es.some(e=>e[0]===u&&e[1]===u+1))es.push([u,u+1,rnd(8),rnd(h)])}test(n,es,h)}
for(let i=0;i<100;i++){const n=2+rnd(5),es=[],boundary=[];for(let u=0;u<n;u++){if(rnd(2))boundary.push(u);for(let v=u+1;v<n;v++)if(rnd(2))es.push([u,v,rnd(8),0])}
let need=all(n);for(const v of boundary)need^=bit(v);const expected=new Set();function go(k,o,g){if(k===es.length){if((o&need)===need)expected.add(o|(BigInt(g)<<BigInt(n)));return}go(k+1,o,g);const [u,v,t]=es[k],m=bit(u)|bit(v);if(!(o&m))go(k+1,o|m,g^t)}go(0,0n,0);const actual=dummySupport(n,es,boundary);assert(actual.size===expected.size&&[...expected].every(x=>actual.has(x)),"completion graph");stats.dummyChecks++}
return stats
}
console.log(JSON.stringify(runI01(),null,2));
