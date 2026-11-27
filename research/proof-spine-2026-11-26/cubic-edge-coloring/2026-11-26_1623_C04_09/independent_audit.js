/* C04-09 independent executable six-port neighbor and tariff audit. Node.js */
function audit(){
 const assert=(b)=>{if(!b)throw Error("assertion")};
 const norm=w=>{const m=new Map();return w.map(x=>{if(!m.has(x))m.set(x,m.size+1);return m.get(x)}).join("")};
 const words=new Set();for(let x=0;x<729;x++){let y=x,w=[];for(let i=0;i<6;i++){w.push(y%3+1);y=Math.floor(y/3)}if([1,2,3].every(c=>w.filter(z=>z===c).length%2===0))words.add(norm(w))}
 const T=[...words].sort();assert(T.length===31);
 const path=[[0,1],[1,2],[2,3]], p=[0,0,1,2,3,3],q=[0,0,2,1,3,3];
 const F=[[24,25],[24,29],[25,26],[25,30],[26,31],[27,29],[27,30],[28,30],[28,31],[29,31],[0,26],[12,24]],t=[27,0,28,0,12,12];
 function support(E,P){const e=[...E,...P.map((v,i)=>[v,-i-1])],used=new Map(),w=[];let s=0,visits=0;
 function dfs(i){visits++;if(i===e.length){s|=1<<T.indexOf(norm(w.slice(-6)));return}const[u,v]=e[i],a=used.get(u)||0,b=used.get(v)||0;for(let c=1;c<=3;c++){let z=1<<c;if((a|b)&z)continue;used.set(u,a|z);used.set(v,b|z);w.push(c);dfs(i+1);w.pop();used.set(u,a);used.set(v,b)}}
 dfs(0);return {s,visits}}
 function pairings(a){if(!a.length)return [[]];const out=[];for(let i=1;i<a.length;i++)for(const p of pairings(a.filter((_,j)=>j!==0&&j!==i)))out.push([[a[0],a[i]],...p]);return out}
 const wires=pairings([0,1,2,3,4,5]).map(p=>T.reduce((s,w,i)=>p.every(([a,b])=>w[a]===w[b])?s|(1<<i):s,0));
 const sig=s=>wires.reduce((v,x,i)=>s&x?v|(1<<i):v,0);
 const A=support(path,p),B=support(path,q),C=support(F,t);assert(A.s===31660032&&B.s===509614080&&C.s===1635975168);assert(sig(A.s)===sig(B.s));assert(Boolean(A.s&C.s)!==Boolean(B.s&C.s));
 const f=F.map(([a,b])=>[a+100,b+100]),ports=t.map(v=>v+100);
 function check(E){const a=new Map();E.forEach(([u,v],i)=>{for(const [x,y] of [[u,v],[v,u]]){if(!a.has(x))a.set(x,[]);a.get(x).push([y,i])}});assert([...a.values()].every(z=>z.length===3));let nodes=0;const M=new Set();
 function dfs(free){nodes++;if(!free.size){const seen=new Set();for(const u of a.keys())if(!seen.has(u)){const Q=[u];seen.add(u);for(const v of Q)for(const[w,i]of a.get(v))if(!M.has(i)&&!seen.has(w)){seen.add(w);Q.push(w)}if(Q.length%2)return false}return true}const v=[...free].sort((x,y)=>a.get(x).filter(([w])=>free.has(w)).length-a.get(y).filter(([w])=>free.has(w)).length)[0];for(const [w,i]of a.get(v))if(free.has(w)){const g=new Set(free);g.delete(v);g.delete(w);M.add(i);if(dfs(g))return true;M.delete(i)}return false}return {yes:dfs(new Set(a.keys())),nodes}}
 const joined=[p,q].map(v=>check([...path,...f,...v.map((u,i)=>[u,ports[i]])]));assert(joined[0].yes&&!joined[1].yes);
 const Q=2n**31n-1n,c=80n;assert(3n*Q*3n**(c-1n)<4n**(c-1n));
 let tariff=0;for(let L=1;L<=12;L++)for(let n=4*L;n<=100;n+=2)for(let s=2*L;s<=n/2;s++){assert(Q*BigInt(s+L)**c+BigInt(n-s+L)**c<BigInt(n)**c);tariff++}
 return {types:T.length,supports:[A,B,C],wire_signature:sig(A.s),joined,tariff_checks:tariff,exponent:Number(c)};
}
console.log(JSON.stringify(audit(),null,2));
