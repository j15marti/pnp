function run(rt,da){
 const cap=512,K=4;let checks=0,products=0,probes=0,declines=0,scans=0,largest=0;
 const assert=x=>{checks++;if(!x)throw Error("assertion "+checks)};
 const parity=x=>{let p=0;while(x){p^=1;x&=x-1}return p}, hi=x=>31-Math.clz32(x);
 const abs=x=>x<0n?-x:x,gcd=(a,b)=>{a=abs(a);b=abs(b);while(b)[a,b]=[b,a%b];return a},lcm=(a,b)=>a/gcd(a,b)*b;
 function frac(n,d=1n){if(!d)throw Error("zero denominator");if(d<0n){n=-n;d=-d}let g=gcd(n,d);return [n/g,d/g]}
 const plus=(a,b)=>frac(a[0]*b[1]+b[0]*a[1],a[1]*b[1]),neg=a=>[-a[0],a[1]],times=(a,b)=>frac(a[0]*b[0],a[1]*b[1]),div=(a,b)=>frac(a[0]*b[1],a[1]*b[0]);
 function gauss(A,b){let k=b.length;A=A.map((r,i)=>[...r.map(v=>frac(v)),frac(b[i])]);for(let j=0;j<k;j++){let p=j;while(p<k&&!A[p][j][0])p++;if(p===k)return null;[A[p],A[j]]=[A[j],A[p]];let z=A[j][j];for(let h=j;h<=k;h++)A[j][h]=div(A[j][h],z);for(let i=0;i<k;i++)if(i!==j&&A[i][j][0]){let q=A[i][j];for(let h=j;h<=k;h++)A[i][h]=plus(A[i][h],neg(times(q,A[j][h])))}}return A.map(r=>r[k])}
 function add(M,m,a){let b=(M.get(m)||0n)+a;if(b)M.set(m,b);else M.delete(m)}
 function mul(A,B){let C=new Map();for(const [m,a] of A)for(const [n,b] of B){products++;add(C,m^n,a*b);if(C.size>cap)return null}largest=Math.max(largest,C.size);return C}
 function dot(A,B){let v=0n;for(const [m,a] of A)v+=a*(B.get(m)||0n);return v}
 function evalE(M,x){let v=0n;for(const [m,a] of M)v+=parity(m&x)?-a:a;return v}
 function polyEval(co,x){let v=frac(0n);for(let i=co.length-1;i>=0;i--)v=plus(times(v,frac(x)),co[i]);return v}
 function norm(M,scale){let g=scale;for(let v of M.values())g=gcd(g,v);if(g>1n){for(let [m,v] of M)M.set(m,v/g);scale/=g}return {M,scale}}
 function affineAbs(B,scale,bound){
   probes++; if(!B.size)return {M:new Map(),den:1n,r:0};
   // X=(2B)^2. Since original energy is integer in [0,bound], |2B|/scale is an integer in [0,bound].
   const W=new Map([...B].map(([m,a])=>[m,2n*a]));const X=mul(W,W);if(!X){declines++;return null}
   let P=[new Map([[0,1n]])],mom=[1n];
   for(let r=1;r<=K;r++){
     let next=mul(P[r-1],X);if(!next){declines++;return null}P.push(next);
     mom[2*r-1]=dot(P[r-1],P[r]);mom[2*r]=dot(P[r],P[r]);
     let c=gauss(Array.from({length:r},(_,i)=>Array.from({length:r},(_,j)=>mom[i+j])),Array.from({length:r},(_,i)=>-mom[i+r]));if(!c){declines++;return null}
     c.push(frac(1n));let norm2=frac(0n);for(let i=0;i<=r;i++)for(let j=0;j<=r;j++)norm2=plus(norm2,times(times(c[i],c[j]),frac(mom[i+j])));assert(norm2[0]>=0n);if(norm2[0])continue;
     let roots=[],target=[];for(let j=0;j<=bound;j++){let t=BigInt(j)*scale;if(!polyEval(c,t*t)[0]){roots.push(t*t);target.push(t)}}
     assert(roots.length===r);
     let a=gauss(roots.map(x=>Array.from({length:r},(_,i)=>x**BigInt(i))),target);assert(a!==null);
     let den=a.reduce((s,q)=>lcm(s,q[1]),1n),M=new Map();for(let i=0;i<r;i++)for(let [m,v] of P[i]){add(M,m,v*a[i][0]*(den/a[i][1]));if(M.size>cap){declines++;return null}}
     // exact sparse identity verification, using nonnegative norm already checked for annihilator
     return {M,den,r,roots:target.map(t=>Number(t/scale))};
   }
   declines++;return null;
 }
 function eliminate(M,scale,q,bound){
   let p=1<<hi(q),A=new Map(),B=new Map();for(let [m,a] of M)add(parity(m&q)?B:A,m&~p,a);if(!B.size)return null;
   let h=affineAbs(B,scale,bound);if(!h)return null;
   let D=new Map();for(let [m,a] of A)add(D,m,2n*a*h.den);for(let [m,a] of h.M)add(D,m,-a);if(D.size>cap){declines++;return null}
   return {...norm(D,2n*scale*h.den),q,p,B,r:h.r,fanout:B.size,roots:h.roots};
 }
 function sys(rows){let B=new Map();for(let [m,b] of rows){while(m){let p=hi(m);if(!B.has(p)){B.set(p,[m,b]);break}let [a,c]=B.get(p);m^=a;b^=c}if(!m&&b)return null}let x=0;for(let p of [...B.keys()].sort((a,b)=>a-b)){let [m,b]=B.get(p);if(parity(m&x)!==b)x^=1<<p}return x}
 function solve(M,n,bound,first=null){
   let initial=M,scale=1n,log=[],word=null,mode="OPEN",minimum=null;
   for(let stage=0;stage<=n;stage++){
     let terms=[...M].filter(([m])=>m),off=(M.get(0)||0n)-terms.reduce((s,[,a])=>s+abs(a),0n);
     if(!terms.length){minimum=Number((M.get(0)||0n)/scale);word=0;mode=minimum===0?"SAT":"UNSAT";break}
     if(off>0n){mode="UNSAT";break}
     if(off===0n){word=sys(terms.map(([m,a])=>[m,+(a>0n)]));mode=word===null?"UNSAT":"SAT";if(word!==null)minimum=0;break}
     let best=null;for(let i=0;i<n;i++){let q=1<<i;if(first!==null&&stage===0&&q!==first)continue;if(!terms.some(([m])=>m&q))continue;let e=eliminate(M,scale,q,bound);if(e&&(!best||e.M.size<best.M.size))best=e}
     if(!best)break;
     let e=best;
     // For larger cubes deterministic sampled local identities; small ones exhaustive.
     let lim=n<=9?1<<n:128;
     for(let i=0;i<lim;i++){let x=(n<=9?i:Math.imul(i+1,2654435761)&((1<<n)-1))&~e.p;let a=evalE(M,x),b=evalE(M,x^e.q);assert(evalE(e.M,x)*scale===(a<b?a:b)*e.scale)}
     M=e.M;scale=e.scale;log.push(e);
   }
   if(word!==null){for(let i=log.length-1;i>=0;i--){let e=log[i];assert(!(word&e.p));if(evalE(e.B,word)>0n)word^=e.q}assert(evalE(initial,word)===BigInt(minimum))}
   return {mode,minimum,word,steps:log.length,fanout:Math.max(0,...log.map(e=>e.fanout)),magnitudes:log.map(e=>e.r),peak:Math.max(initial.size,...log.map(e=>e.M.size)),moves:log.map(e=>({q:e.q,fanout:e.fanout,magnitudes:e.roots,terms:e.M.size}))};
 }
 function test(n,reg,cuts){
   let basis=new Map(),contradiction=false,derived=0;
   function put(m,b){while(m){let p=hi(m);if(!basis.has(p)){basis.set(p,[m,b]);return 1}let [u,v]=basis.get(p);m^=u;b^=v}return b?-1:0}
   function reduce(m,b=0){for(let p of [...basis.keys()].sort((a,b)=>b-a))if(m>>p&1){let [u,v]=basis.get(p);m^=u;b^=v}return [m,b]}
   function form(o){let [a,b,c]=o.t,v=o.bad[0];return [[(1<<a)^(1<<b),(v^(v>>1))&1],[(1<<a)^(1<<c),(v^(v>>2))&1]].map(([m,b])=>reduce(m,b))}
   function close(){let change;do{change=false;scans++;for(let o of reg){let [[a,b],[c,d]]=form(o);if((!a&&b)||(!c&&d)||(a===c&&b!==d))continue;if(!a&&!c){contradiction=true;return}if(!a||!c||a===c){let s=put(a||c,(a?b:d)^1);if(s<0){contradiction=true;return}if(s){derived++;change=true;break}}}}while(change)}
   close();for(let [m,b] of cuts){if(contradiction)break;let s=put(parseInt(m,16),b);if(s<0){contradiction=true;break}close()}if(!contradiction)close();
   let count=0,ref=Infinity,M=new Map();for(let o of reg){let [[a,b],[c,d]]=form(o);add(M,0,1n);add(M,a,b?-1n:1n);add(M,c,d?-1n:1n);add(M,a^c,b^d?-1n:1n)}
   function violations(x){return reg.reduce((s,o)=>s+ +o.bad.includes(o.t.reduce((v,t,i)=>v|((x>>t&1)<<i),0)),0)}
   for(let x=0;x<1<<n;x++){let v=violations(x);if(!v){count++;assert(cuts.every(([m,b])=>parity(x&parseInt(m,16))===b));assert(!contradiction&&[...basis.values()].every(([m,b])=>parity(x&m)===b))}if(!contradiction&&[...basis.values()].every(([m,b])=>parity(x&m)===b)){ref=Math.min(ref,4*v);if(n<=9||x%127===0)assert(evalE(M,x)===BigInt(4*v))}}
   if(contradiction){assert(count===0);return {mode:"UNSAT",reason:"local-closure",count,derived}}
   let z=solve(M,n,4*reg.length);if(z.mode!=="OPEN"){assert((z.mode==="SAT")===(count>0));if(z.minimum!==null)assert(z.minimum===ref);if(z.word!==null){let x=z.word;for(let p of [...basis.keys()].sort((a,b)=>a-b)){let [m,b]=basis.get(p);if(parity(x&m)!==b)x^=1<<p}assert(4*violations(x)===z.minimum);assert([...basis.values()].every(([m,b])=>parity(x&m)===b));z.sourceWord=x}}
   return {count,derived,reference:ref,...z};
 }
 let out=[];for(let i=0;i<rt.controls.length;i++){let {n,registry:r}=rt.controls[i],d=da.rt[i],neighbor=r.map((o,j)=>j?o:{...o,bad:o.bad.map(x=>x^1)});out.push({n,root:test(n,r,[]),combined:test(n,r,d.alternating.accepted),neighbor:test(n,neighbor,[]),neighborCombined:test(n,neighbor,d.neighborAlternating.accepted)})}
 let fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map(t=>({t,bad:[0,7]}));let f=[test(7,fano,[])];for(let i=0;i<7;i++)for(let j=0;j<3;j++)f.push(test(7,fano.map((o,k)=>k===i?{...o,bad:o.bad.map(v=>v^(1<<j))}:o),[]));
 let addr=[];for(let k=1;k<=4;k++){let s=1<<k,z=1<<(k+s),n=k+s+1;for(let bad=0;bad<2;bad++){let M=new Map([[0,BigInt(s+bad)]]);for(let a=0;a<s;a++)for(let b=0;b<s;b++)add(M,z|(1<<(k+a))|b,parity(a&b)?-1n:1n);let h=eliminate(M,1n,z,2*s+bad);assert(h!==null&&h.M.size===(bad?1:0)&&evalE(h.M,0)===BigInt(bad)*h.scale);addr.push({k,s,fanout:s*s,rankDifference:s-1+k,mode:bad?"UNSAT":"SAT",magnitudes:h.roots,outputTerms:h.M.size});}}
 return {cap,K,checks,products,probes,declines,scans,largest,out,fano:f,addr};
}
if(require.main===module){const fs=require('fs');console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2])),JSON.parse(fs.readFileSync(process.argv[3]))),null,2))}
