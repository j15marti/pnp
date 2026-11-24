'use strict';
function experiment(){
 let seed=20261124>>>0;const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n};
 const xor=(a,b)=>a^b, bit=i=>1n<<BigInt(i), str=x=>x.toString(), uniq=a=>[...new Set(a)];
 function basis(a){let b=[];for(let x of a){for(const y of b)if((x^y)<x)x^=y;if(x){b.push(x);b.sort((x,y)=>x>y?-1:1)}}return b}
 function reduce(x,b){for(const y of b)if((x^y)<x)x^=y;return x}
 function span(b){let s=[0n];for(let x of b)s=s.concat(s.map(y=>y^x));return s}
 function eq(a,b){return a.size===b.size&&[...a].every(x=>b.has(x))}
 function check(x,m){if(!x)throw Error(m)}
 function match(g,mask){let out=new Map();function rec(rem,z,sel){if(!rem){if(!out.has(z))out.set(z,sel.slice());return}let u=0;while(!(rem&bit(u)))u++;for(let i=0;i<g.e.length;i++){let [a,b,t]=g.e[i];if(a!==u&&b!==u)continue;let v=a===u?b:a;if(!(rem&bit(v)))continue;sel.push(i);rec(rem^bit(u)^bit(v),z^t,sel);sel.pop()}}rec(mask,0n,[]);return out}
 function fibers(g){let k=g.n-2,p=k%2,inside=(bit(g.n)-1n)^3n;return [0,1].map(a=>match(g,inside|(a?1n:0n)|((a^p)?2n:0n)))}
 function stabilizer(s,r){if(!s.size)return [];let a=[];for(let i=0;i<2**r;i++){let d=BigInt(i);if([...s.keys()].every(x=>s.has(x^d)))a.push(d)}return basis(a)}
 function factor(s,r){if(!s.size)return {b:[],rep:[]};let b=stabilizer(s,r),rep=uniq([...s.keys()].map(x=>reduce(x,b)));return {b,rep}}
 // Construct exact chain from two fiber factor descriptions. Each stage is u-a-b-v;
 // parallel labels are explicit alternatives. Internal joins force alternating occupancy.
 function make(f,p){let k=1+Math.max(f[0].b.length,f[1].b.length);if((k%2===0?1:0)!==p)k++;
 let n=2,e=[],st=[];for(let i=0;i<k;i++){let u=i?st[i-1].v:0,v=i===k-1?1:n++,a=n++,b=n++;let options=[0,1].map(local=>{let global=local^(i%2),q=f[global];if(!i)return q.rep;if(i<=q.b.length)return [0n,q.b[i-1]];return [0n]});
 let low=[],high=[];for(let t of options[0]){low.push(e.length);e.push([a,b,t])}for(let t of options[1]){high.push(e.length);e.push([u,a,t])}let last=e.length;e.push([b,v,0n]);st.push({u,v,a,b,low,high,last})}return {n,e,st}}
 function valid(g,sel,mask,t){let o=0n,z=0n;for(let i of sel){let [u,v,s]=g.e[i],d=bit(u)|bit(v);if(o&d)return false;o|=d;z^=s}return o===mask&&z===t}
 function glue(g,ext){let e=g.e.slice();for(let [u,v,t] of ext.e){let a=u<2?u:g.n+u-2,b=v<2?v:g.n+v-2;e.push([a,b,t])}return {n:g.n+ext.n-2,e}}
 function rndGraph(k,r){let n=k+2,e=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(rand(100)<48)e.push([u,v,BigInt(rand(2**r))]);return {n,e}}
 let out={seed:20261124,randomModules:240,fiberChecks:0,emptyFibers:0,nonzeroFiberStabilizers:0,strictFiberStabilizerDifferences:0,globalTargets:0,sat:0,unsat:0,liftChecks:0,cutChecks:0,cutStrictDrops:0,scale:[]};
 for(let j=0;j<out.randomModules;j++){let p=j%2,k=2+rand(3)*2+p,r=4,g=rndGraph(k,r),s=fibers(g),f=s.map(x=>factor(x,r));let h=make(f,p),q=fibers(h);
 for(let a=0;a<2;a++){out.fiberChecks++;if(!s[a].size)out.emptyFibers++;if(f[a].b.length)out.nonzeroFiberStabilizers++;check(eq(new Set(s[a].keys()),new Set(q[a].keys())),"fiber support");for(let t of q[a].keys()){let mask=(bit(g.n)-1n)^3n;mask|=BigInt(a)|BigInt(a^p)*2n;check(valid(g,s[a].get(t),mask,t),"original lift");out.liftChecks++}}
 if(!eq(new Set(span(f[0].b)),new Set(span(f[1].b))))out.strictFiberStabilizerDifferences++;
 let ext=rndGraph(2+p,r),G=glue(g,ext),H=glue(h,ext),ref=match(G,bit(G.n)-1n),actual=match(H,bit(H.n)-1n);check(eq(new Set(ref.keys()),new Set(actual.keys())),"exterior");for(let t=0;t<2**r;t++){out.globalTargets++;if(ref.has(BigInt(t)))out.sat++;else out.unsat++}
 }
 // Partial local translation quotient width identity, independent of graphs.
 for(let j=0;j<600;j++){let Vs=Array.from({length:5},()=>basis(Array.from({length:rand(5)},()=>BigInt(rand(64))))),Ws=Vs.map(v=>basis(Array.from({length:rand(4)},()=>{let x=0n;for(let y of v)if(rand(2))x^=y;return x}))),W=basis(Ws.flat()),A=basis(Vs.slice(0,2).flat()),B=basis(Vs.slice(2).flat());let k=A.length+B.length-basis(A.concat(B)).length,Ap=basis(A.map(x=>reduce(x,W))),Bp=basis(B.map(x=>reduce(x,W))),kp=Ap.length+Bp.length-basis(Ap.concat(Bp)).length;let inter=span(W).filter(x=>!reduce(x,A)&&!reduce(x,B));check(kp===k-basis(inter).length,"width");out.cutChecks++;if(kp<k)out.cutStrictDrops++}
 // Disjoint conditional translation directions, no common nonzero translation.
 for(let r of [4,8,16,32,64,128]){let f=[{b:Array.from({length:r},(_,i)=>bit(i)),rep:[0n]},{b:Array.from({length:r},(_,i)=>bit(i+r)),rep:[0n]}],g=make(f,0);for(let a=0;a<2;a++){let target=0n,sel=[];for(let i=0;i<g.st.length;i++){let s=g.st[i],local=a^(i%2),options=local?s.high:s.low;let pick=options.length===2?i%2:0,id=options[pick];sel.push(id);target^=g.e[id][2];if(local)sel.push(s.last)}
 let mask=((bit(g.n)-1n)^3n)|(a?3n:0n);check(valid(g,sel,mask,target),"scale lift");check((a?target&(bit(r)-1n):target>>BigInt(r))===0n,"scale wrong fiber");let bad=target^bit(a?0:r);check((a?bad&(bit(r)-1n):bad>>BigInt(r))!==0n,"bad fiber")}
 out.scale.push({rankPerFiber:r,commonRank:0,explicitSupportPerFiber:(bit(r)).toString(),stages:g.st.length,vertices:g.n,edges:g.e.length,verifiedSatWitnesses:2,analyticUnsatControls:2})}
 return out;
}
console.log(JSON.stringify(experiment(),null,2));
