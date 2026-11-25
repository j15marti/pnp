// Node.js >=18. Exact signed NAE3 / OR3 integer field DAG. Run: node thisfile.js
console.log(JSON.stringify((function(){
const L={checks:0,closureScans:0,pins:0,transitions:0,merges:0,fieldCoordinates:0,referenceWords:0,verified:0};
function ck(x){L.checks++;if(!x)throw Error("assertion "+L.checks)}
const bit=(w,i)=>Number((w>>BigInt(i))&1n);
const val=(l,w)=>bit(w,Math.abs(l)-1)^(l<0?1:0);
function valid(c,w){let a=c.l.map(l=>val(l,w));return c.t==="N"?a.some(x=>x!==a[0]):a.some(x=>x===1)}
function solve(n,F,pins=[],order=Array.from({length:n},(_,i)=>i),cap=100000){
 let p=Array(n).fill(-1);for(const [v,b] of pins){if(p[v]>=0&&p[v]!==b)return {count:"0",peak:0};p[v]=b}
 // Complete singleton-owner affine closure for distinct strict NAE3 and OR3 under coordinate pins.
 outer:while(true){L.closureScans++;for(const c of F){let rows=[];for(let u=0;u<8;u++){let a=c.l.map((l,j)=>((u>>j)&1)^(l<0?1:0));if(c.l.some((l,j)=>p[Math.abs(l)-1]>=0&&p[Math.abs(l)-1]!==((u>>j)&1)))continue;if(c.t==="N"?a.every(x=>x===a[0]):!a.some(Boolean))continue;rows.push(u)}
 if(!rows.length)return {count:"0",peak:0};
 for(let j=0;j<3;j++){let v=Math.abs(c.l[j])-1,b=(rows[0]>>j)&1;if(p[v]<0&&rows.every(u=>((u>>j)&1)===b)){p[v]=b;L.pins++;continue outer}}
 }break}
 const pos=Array(n);order.forEach((v,i)=>pos[v]=i);const J=Array.from({length:n},()=>Array(n).fill(0));let M=0,O=[];
 for(const c of F){if(c.t==="O"){O.push(c);continue}M++;for(let j=0;j<3;j++)for(let k=j+1;k<3;k++){let a=pos[Math.abs(c.l[j])-1],b=pos[Math.abs(c.l[k])-1],s=(c.l[j]<0)===(c.l[k]<0)?1:-1;J[a][b]+=s;J[b][a]+=s}}
 const inc=Array.from({length:n},()=>[]);let init=(1n<<BigInt(O.length))-1n;
 O.forEach((c,j)=>{let end=Math.max(...c.l.map(l=>pos[Math.abs(l)-1]));c.l.forEach(l=>inc[pos[Math.abs(l)-1]].push([1n<<BigInt(j),l>0?1:0,end]))});
 let T=new Map([["",{f:Array(n).fill(0),g:init,e:0,count:1n,w:0n}]]),peak=1,raw=0,layers=[1];
 for(let i=0;i<n;i++){let U=new Map();for(let a=0;a<=i;a++)if(J[a].slice(i+1).some(Boolean))raw=Math.max(raw,0);raw=Math.max(raw,J.slice(0,i+1).filter(row=>row.slice(i+1).some(Boolean)).length);
 for(const z of T.values())for(let b=0;b<2;b++){if(p[order[i]]>=0&&p[order[i]]!==b)continue;L.transitions++;let g=z.g,good=true;for(const [mask,t,end] of inc[i]){if(b===t)g&=~mask;if(end===i&&(g&mask)!==0n){good=false;break}}if(!good)continue;
 let s=2*b-1,e=z.e+s*z.f[0],f=z.f.slice(1).map((v,j)=>v+s*J[i][i+j+1]);L.fieldCoordinates+=f.length;
 let key=g.toString()+":"+f.join(","),old=U.get(key),w=z.w|(BigInt(b)<<BigInt(order[i]));if(!old||e<old.e)U.set(key,{f,g,e,count:z.count,w});else if(e===old.e)old.count+=z.count;if(old)L.merges++;
 if(U.size>cap)return {unknown:true,peak:U.size,raw};
 }T=U;peak=Math.max(peak,T.size);layers.push(T.size);if(!T.size)break}
 let best=[...T.values()][0];if(!best)return {count:"0",peak,raw,layers};ck(best.f.length===0&&best.g===0n);ck((M+best.e)>=0&&(M+best.e)%4===0);
 let cnt=M+best.e===0?best.count:0n;if(cnt){ck(F.every(c=>valid(c,best.w)));ck(pins.every(([v,b])=>bit(best.w,v)===b));L.verified++}
 return {count:cnt.toString(),minimumViolations:(M+best.e)/4,peak,raw,layers}
}
function ref(n,F,pins=[]){let cnt=0;for(let w=0n;w<(1n<<BigInt(n));w++){L.referenceWords++;if(pins.every(([i,b])=>bit(w,i)===b)&&F.every(c=>valid(c,w)))cnt++}return String(cnt)}
const N=l=>({t:"N",l}),O=l=>({t:"O",l});const fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]].map(N);
let stats={sat:0,unsat:0},fanoResults=[],random={sat:0,unsat:0},scaling=[],hostile=[];
function test(n,F,pins=[],order){const s=solve(n,F,pins,order);ck(!s.unknown);ck(s.count===ref(n,F,pins));stats[s.count==="0"?"unsat":"sat"]++;return s}
fanoResults.push({type:"root",...test(7,fano)});
for(let i=0;i<7;i++){for(let s of [-1,1]){let F=fano.map((c,j)=>i===j?O(c.l.map(x=>s*x)):c),a=test(7,F);ck(a.count==="5");fanoResults.push({type:"budget",i,s,...a})}
for(let j=0;j<3;j++){let F=fano.map((c,k)=>i===k?N(c.l.map((x,h)=>j===h?-x:x)):c),a=test(7,F);ck(a.count==="10");fanoResults.push({type:"sign",i,j,...a})}}
let seed=2081440;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
for(let t=0;t<120;t++){let n=5+rnd(5),F=[];for(let i=0,m=4+rnd(15);i<m;i++){let a=new Set();while(a.size<3)a.add(1+rnd(n));let l=[...a].map(x=>rnd(4)<2?-x:x);F.push(rnd(5)===0?O(l):N(l))}let p=t%3===0?[[rnd(n),rnd(2)]]:[],a=test(n,F,p);random[a.count==="0"?"unsat":"sat"]++}
 // Dense tripartite modules, all share one actual hub; add Fano root or one-budget neighbor on same hub.
for(const [k,d] of [[2,4],[4,8],[6,12]])for(const sat of [true,false]){
 let F=fano.map((c,j)=>sat&&j===0?O(c.l):c),n=7;
 for(let j=0;j<k;j++){let A=Array.from({length:d},()=>++n),B=Array.from({length:d},()=>++n),C=[1,...Array.from({length:d-1},()=>++n)];for(const a of A)for(const b of B)for(const c of C)F.push(N([a,b,c]))}
 let a=solve(n,F);ck(!a.unknown);ck((a.count!=="0")===sat);scaling.push({k,d,n,m:F.length,sat,count:a.count,peak:a.peak,raw:a.raw})
}
 // Actual-key explosion under a deliberately grouped order, repaired by interleaving.
for(const k of [2,4,8,10]){let F=Array.from({length:k},(_,i)=>N([i+1,k+2*i+1,k+2*i+2])),ord=F.flatMap(c=>c.l.map(l=>l-1)),a=solve(3*k,F),b=solve(3*k,F,[],ord);ck(a.count===String(6n**BigInt(k)));ck(a.count===b.count);ck(a.layers[k]===2**k);hostile.push({k,grouped:a.peak,interleaved:b.peak,central:a.layers[k]})}
 // Closure contradiction and forced-coordinate controls.
ck(test(3,[N([1,2,3])],[[0,0],[1,0]]).count==="1");
ck(test(3,[N([1,2,3])],[[0,0],[1,0],[2,0]]).count==="0");
return {seed:2081440,referenceCases:stats,random,fano:fanoResults,scaling,hostile,ledger:L}
})(),null,2));
