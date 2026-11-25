"use strict";
function run(){
 const stats={seed:162024,random:0,sat:0,unsat:0,targetComparisons:0,forcedPins:0,closureProbes:0,witnesses:0,packetPairs:0,assertions:0,scales:[],barrier:[]};
 let seed=stats.seed;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
 const chk=(v)=>{stats.assertions++;if(!v)throw Error("assertion "+stats.assertions)};
 const pow=e=>1n<<BigInt(e), mod=(a,m)=>(a%m+m)%m;
 const packet=(a,e,c=1n)=>({a:a.map((x,i)=>mod(BigInt(x),pow(e[i]))),e:[...e],c});
 const key=p=>p.e.join(",")+":"+p.a.join(",");
 function merge(ps){const map=new Map();for(const p of ps){let k=key(p);let q=map.get(k);map.set(k,packet(p.a,p.e,p.c+(q?q.c:0n)))}return [...map.values()].filter(p=>p.c!==0n)}
 function size(p,E){return p.e.reduce((n,e,i)=>n*pow(E[i]-e),1n)}
 function intersect(p,q){let a=[],e=[];for(let i=0;i<p.e.length;i++){let j=Math.min(p.e[i],q.e[i]);if(mod(p.a[i]-q.a[i],pow(j))!==0n)return null;let r=p.e[i]>=q.e[i]?p:q;a.push(r.a[i]);e.push(r.e[i])}return packet(a,e,p.c*q.c)}
 function restrict(f,p){return merge(f.map(q=>intersect(q,p)).filter(Boolean))}
 function conv(f,g,E){let out=[];for(const p of f)for(const q of g){stats.packetPairs++;const e=p.e.map((x,i)=>Math.min(x,q.e[i]));const k=p.e.reduce((n,x,i)=>n*pow(E[i]-Math.max(x,q.e[i])),1n);out.push(packet(p.a.map((x,i)=>x+q.a[i]),e,p.c*q.c*k))}return merge(out)}
 function val(f,x){return f.reduce((n,p)=>n+(x.every((v,i)=>mod(v-p.a[i],pow(p.e[i]))===0n)?p.c:0n),0n)}
 function mass(f,g,t,E,guard){let sum=0n;for(const p of f)for(const q of g){stats.packetPairs++;let r=intersect(p,packet(t.map((v,i)=>v-q.a[i]),q.e,q.c));if(r&&guard)r=intersect(r,guard);if(r)sum+=r.c*size(r,E)}return sum}
 const delta=(x,E)=>[packet(x,E)];
 function all(E){let a=[[]];for(const e of E){let b=[];for(const x of a)for(let y=0n;y<pow(e);y++)b.push([...x,y]);a=b}return a}
 const add=(x,y,E)=>x.map((v,i)=>mod(v+y[i],pow(E[i])));
 const sub=(x,y,E)=>x.map((v,i)=>mod(v-y[i],pow(E[i])));
 const zero=E=>E.map(()=>0n);
 function product(fs,E){return fs.reduce((a,b)=>conv(a,b,E),delta(zero(E),E))}
 function lift(f,g,t,E){let a=zero(E),e=E.map(()=>0);chk(mass(f,g,t,E)>0n);for(let i=0;i<E.length;i++)for(let j=0;j<E[i];j++){e[i]++;let p=packet(a,e);let n=mass(f,g,t,E,p);if(n===0n)a[i]+=pow(j);chk(mass(f,g,t,E,packet(a,e))>0n)}chk(val(f,a)>0n&&val(g,sub(t,a,E))>0n);return a}
 function closure(fs,t,E){let f=fs.map(a=>a.slice()),fixed=new Set();while(true){let total=val(product(f,E),t);if(total===0n)return {f,total};let changed=false;outer:for(let i=0;i<f.length;i++){let outside=product(f.filter((_,j)=>i!==j),E);for(let j=0;j<E.length;j++){let id=i+":"+j;if(fixed.has(id))continue;let e=E.map(()=>0);e[j]=1;let n=mass(f[i],outside,t,E,packet(zero(E),e));stats.closureProbes++;chk(n>=0n&&n<=total);if(n===0n||n===total){let a=zero(E);a[j]=n===0n?1n:0n;f[i]=restrict(f[i],packet(a,e));fixed.add(id);stats.forcedPins++;changed=true;break outer}}}if(!changed)return {f,total}}}
 function reference(fs,E){let X=all(E),m=new Map([[zero(E).join(","),1n]]);for(let f of fs){let q=new Map();for(let [k,c] of m){let x=k.split(",").map(BigInt);for(let y of X){let d=val(f,y);if(d){let k2=add(x,y,E).join(",");q.set(k2,(q.get(k2)||0n)+c*d)}}}m=q}return m}
 function randomLeaf(E){let e=E.map(x=>rnd(x+1)),a=E.map(x=>BigInt(rnd(2**x))),p=packet(a,e);let j=rnd(E.length),q=packet(a,e,-1n);if(q.e[j]<E[j]){q.e[j]++;q=packet(q.a,q.e,-1n)}else q.c=0n;let r=packet(E.map(x=>BigInt(rnd(2**x))),E.map(x=>rnd(x+1)),BigInt(1+rnd(3)));return merge([p,q,r])}
 for(let k=0;k<100;k++){let E=[1,1,2+(k%2)],fs=Array.from({length:3},()=>randomLeaf(E)),X=all(E);for(let f of fs)for(let x of X)chk(val(f,x)>=0n);
 let ref=reference(fs,E),F=product(fs,E);for(let x of X){chk(val(F,x)===(ref.get(x.join(","))||0n));stats.targetComparisons++}
 let t=X[rnd(X.length)],c=closure(fs,t,E),expected=ref.get(t.join(","))||0n;chk(c.total===expected);stats.random++;
 if(expected){stats.sat++;let a=lift(c.f[0],product(c.f.slice(1),E),t,E),b=lift(c.f[1],c.f[2],sub(t,a,E),E),d=sub(sub(t,a,E),b,E);chk(val(fs[0],a)>0n&&val(fs[1],b)>0n&&val(fs[2],d)>0n);chk(add(add(a,b,E),d,E).every((v,i)=>v===t[i]));stats.witnesses++}else stats.unsat++;
 }
 // Explicit incompatible integer quota neighbors, exact signed range <= 2W, modulus > 4W.
 for(const k of [8,32,64,128]){let E=[1,1,k+3],W=pow(k),fs=[ [packet([0n,0n,W],[0,0,E[2]])], [packet([0n,0n,-W],[0,0,E[2]])] ];let c=closure(fs,zero(E),E);chk(c.total===4n);let a=lift(c.f[0],c.f[1],zero(E),E);chk(a[2]===W);let bad=closure(fs,[0n,0n,1n],E);chk(bad.total===0n);
 // Abstract modular group with massive dense cosets, not a safe exact-integer interval.
 let f=[packet(zero(E),[0,0,1])],g=[packet([0n,0n,1n],[0,0,1])],h=conv(f,g,E);chk(h.length===1&&val(h,[0n,0n,1n])===pow(k+4)&&val(h,zero(E))===0n);
 stats.scales.push({quotaWeight:W.toString(),modulus:pow(E[2]).toString(),exactQuotaSatCount:c.total.toString(),exactQuotaUnsatCount:bad.total.toString(),denseModularCosetSize:size(f[0],E).toString(),denseModularOutputPackets:h.length});
 }
 for(let k=2;k<=9;k++){let E=[k],M=pow(k),half=M/2n;let f=Array.from({length:Number(half)},(_,i)=>packet([BigInt(i)],E));let active=0;for(let x=0n;x<half;x++)if(val(f,[x])!==val(f,[x+half]))active++;chk(active===Number(half));stats.barrier.push({k,antipodalDifferences:active,minimumUnsignedCosets:active})}
 return stats;
}
console.log(JSON.stringify(run(), null, 2));
