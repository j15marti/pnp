"use strict";
const results = (function main(){
 const stats={checks:0,gauss:0,closureSweeps:0,forcedPins:0,edgeScans:0,signatures:0,transitions:0,dominance:0,referenceWords:0,peakMasks:0,peakLayerCandidates:0};
 function ok(b,ctx){stats.checks++;if(!b)throw Error("assert "+stats.checks+" "+JSON.stringify(ctx))}
 function parity(x){x>>>=0;x^=x>>>16;x^=x>>>8;x^=x>>>4;return (0x6996>>>(x&15))&1}
 function gauss(eq){stats.gauss++;let p=new Map();for(let [x,b] of eq){while(x){let j=31-Math.clz32(x);if(p.has(j)){let [a,c]=p.get(j);x^=a;b^=c}else{p.set(j,[x,b]);break}}if(!x&&b)return null}return p}
 function reduce(x,b,p){for(let j of [...p.keys()].sort((a,b)=>b-a))if(x&(1<<j)){let [a,c]=p.get(j);x^=a;b^=c}return [x,b]}
 function lift(eq){let p=gauss(eq);if(!p)return null;let z=0;for(let j of [...p.keys()].sort((a,b)=>a-b)){let [a,c]=p.get(j);if(parity(a&z)!==c)z|=1<<j}return z}
 function basis(rows){return [...gauss(rows.map(x=>[x,0])).values()].map(x=>x[0])}
 function inter(A,B){let bp=gauss(B.map(x=>[x,0])),p=new Map(),out=[];for(let a of A){let [x]=reduce(a,0,bp),v=a;while(x){let j=31-Math.clz32(x);if(p.has(j)){let [y,w]=p.get(j);x^=y;v^=w}else{p.set(j,[x,v]);break}}if(!x)out.push(v)}return basis(out)}
 const bit=i=>1n<<BigInt(i);
 function step(S,E,enabled){let R=0n;for(let e of E){stats.edgeScans++;if((S&bit(e[0]))&&enabled(e))R|=bit(e[1])}return R}
 function reach(G,pred){let S=1n;for(let E of G.layers)S=step(S,E,pred);return !!(S&1n)}
 function actual(G,z){return reach(G,e=>e[2].every(([x,b])=>parity(x&z)===b))}
 function close(G,pins){pins=pins.slice();while(true){stats.closureSweeps++;let p=gauss(pins);if(!p)return {label:"EMPTY",pins};let kind=new Map(),opt=[];for(let E of G.layers)for(let e of E){let a=gauss(pins.concat(e[2]));let k=a===null?-1:a.size-p.size;kind.set(e,k);if(k===1)opt.push(e)}
 if(reach(G,e=>kind.get(e)===0))return {label:"UNSAT",pins};
 if(!reach(G,e=>kind.get(e)>=0))return {label:"SAT",pins,z:lift(pins)};
 let changed=false;for(let e of opt){if(reach(G,f=>kind.get(f)===0||f===e)){let a=e[2].find(([x,b])=>reduce(x,b,p)[0]!==0);pins.push([a[0],a[1]^1]);stats.forcedPins++;changed=true;break}}if(!changed)return {label:"OPEN",pins}}
 }
 function sig(rows,z){let x=0;rows.forEach((a,i)=>x|=parity(a&z)<<i);return x}
 function run(G,guard=[],cap=4096){let c=close(G,guard);if(c.label!=="OPEN")return {...c,peak:0,k:0,r:0};let p=gauss(c.pins);
 let layers=G.layers.map(E=>E.map(([u,v,g])=>[u,v,g.map(([x,b])=>reduce(x,b,p))]));
 let W=layers.map(E=>basis(E.flatMap(e=>e[2].map(x=>x[0])))),L=W.length,A=[[]],B=Array(L+1);B[L]=[];for(let i=0;i<L;i++)A.push(basis(A[i].concat(W[i])));for(let i=L-1;i>=0;i--)B[i]=basis(B[i+1].concat(W[i]));let I=A.map((a,i)=>inter(a,B[i]));
 let k=Math.max(...I.map(a=>a.length)),r=0,peak=1;let front=new Map([[0,[{mask:1n,eq:[]}]]]);
 for(let i=0;i<L;i++){let Q=basis(W[i].concat(I[i],I[i+1]));r=Math.max(r,Q.length);if(Q.length>18)return {label:"UNKNOWN",peak,k,r};let groups=new Map();for(let s=0;s<2**Q.length;s++){let eq=Q.map((a,j)=>[a,(s>>>j)&1]),z=lift(eq),a=sig(I[i],z),b=sig(I[i+1],z);stats.signatures++;if(!groups.has(a))groups.set(a,[]);groups.get(a).push({z,b,eq})}
 let next=new Map(),raw=0;for(let [a,arr] of front)for(let old of arr)for(let v of groups.get(a)||[]){stats.transitions++;raw++;let mask=step(old.mask,layers[i],e=>e[2].every(([x,b])=>parity(x&v.z)===b));let list=next.get(v.b)||[];let dominated=false;for(let item of list){stats.dominance++;if((item.mask&mask)===item.mask){dominated=true;break}}if(dominated)continue;let remain=list.filter(item=>{stats.dominance++;return (mask&item.mask)!==mask});remain.push({mask,eq:old.eq.concat(v.eq)});next.set(v.b,remain)}
 stats.peakLayerCandidates=Math.max(stats.peakLayerCandidates,raw);let count=[...next.values()].reduce((a,b)=>a+b.length,0);peak=Math.max(peak,count);stats.peakMasks=Math.max(stats.peakMasks,count);if(count>cap)return {label:"UNKNOWN",peak,k,r};front=next;
 }
 let win=(front.get(0)||[]).find(x=>!(x.mask&1n));if(!win)return {label:"UNSAT",peak,k,r};let z=lift(c.pins.concat(win.eq));ok(z!==null&&!actual(G,z)&&guard.every(([a,b])=>parity(a&z)===b),{phase:"lift",G,guard,z});return {label:"SAT",z,peak,k,r}}
 function cnf(n,C){let layers=[C.map((_,j)=>[0,j,[]])];for(let i=0;i<n;i++){let E=[];for(let j=0;j<C.length;j++){let a=C[j].filter(x=>Math.abs(x)===i+1).map(x=>[1<<i,x>0?0:1]);E.push([j,j,a])}layers.push(E)}layers.push(C.map((_,j)=>[j,0,[]]));return {n,layers}}
 function paired(k,neighbor){let layers=[Array.from({length:4*k},(_,j)=>[0,j,[]])];for(let i=0;i<2*k;i++)layers.push(Array.from({length:4*k},(_,j)=>[j,j,Math.floor(j/4)===Math.floor(i/2)?[[1<<i,(j>>(i%2))&1]]:[]]));layers.push(Array.from({length:4*k},(_,j)=>[j,0,neighbor?[[1<<(2*k),1]]:[]]));return {n:2*k+1,layers}}
 const results={families:{},scales:[],stats};function check(name,G,guard=[],expected=null,cap=4096){let count=0;if(expected===null){for(let z=0;z<2**G.n;z++){stats.referenceWords++;if(guard.every(([a,b])=>parity(a&z)===b)&&!actual(G,z))count++}expected=count?"SAT":"UNSAT"}let a=run(G,guard,cap);ok(a.label===expected,{name,G,guard,a,expected,count});if(a.label==="SAT")ok(!actual(G,a.z)&&guard.every(([x,b])=>parity(x&a.z)===b),{name,phase:"witness"});let f=results.families[name]??={SAT:0,UNSAT:0,UNKNOWN:0,EMPTY:0};f[a.label]++;return {...a,count}}
 let cube=Array.from({length:8},(_,j)=>Array.from({length:3},(_,i)=>((j>>i)&1?1:-1)*(i+1)));for(let s=0;s<256;s++)check("cube",cnf(3,cube.filter((_,i)=>(s>>i)&1)));
 let lines=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]],C=lines.flatMap(x=>[x,x.map(y=>-y)]);let root=check("Fano",cnf(7,C));ok(root.count===0,{root});for(let i=0;i<C.length;i++)ok(check("Fano",cnf(7,C.filter((_,j)=>i!==j))).count===5,{i});
 let seed=2011600;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}
 for(let j=0;j<100;j++){let n=5,L=4,layers=[];for(let i=0;i<L;i++){let E=[];for(let u=0;u<(i?3:1);u++)for(let v=0;v<(i===L-1?1:3);v++)if(rand(4)!==0){let g=Array.from({length:rand(3)},()=>[1+rand(31),rand(2)]);E.push([u,v,g])}layers.push(E)}let G={n,layers};check("affine",G);check("affineGuard",G,[[1+rand(31),rand(2)]])}
 for(let k of [1,2,3,4,5]){let a=check("scaling",paired(k,false),[],"UNSAT"),b=check("scaling",paired(k,true),[],"SAT");ok(a.peak===4**k&&b.peak===4**k&&a.k===0&&a.r===1,{k,a,b});results.scales.push({k,root:a.label,neighbor:b.label,peak:a.peak,interface:a.k,localRank:a.r})}
 check("cap",paired(4,false),[],"UNKNOWN",64);
 return results
})();
console.log(JSON.stringify(results,null,2));
