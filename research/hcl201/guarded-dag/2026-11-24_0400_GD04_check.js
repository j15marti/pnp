function runGD04(){
const parity=x=>{let p=0;while(x){p^=1;x&=x-1n}return p};
const bit=i=>1n<<BigInt(i), has=(x,b)=>(x&b)!==0n;
const norm=a=>{let s=new Set();for(let v of a)s.has(v)?s.delete(v):s.add(v);return [...s]};
const add=(a,b)=>norm([...a,...b]), mul=(a,b)=>norm(a.flatMap(x=>b.map(y=>x|y)));
const ev=(p,x)=>p.reduce((s,m)=>s^Number((m&x)===m),0);
const isquad=m=>m!==0n&&(m&(m-1n))!==0n;
const sub=(p,b,l)=>norm(p.flatMap(m=>has(m,b)?l.map(t=>(m^b)|t):[m]));
const lead=p=>p.reduce((a,b)=>isquad(a)!==isquad(b)?(isquad(a)?a:b):(a>b?a:b),0n);
function close(eq,phase){
 let subs=[];
 while(true){
  let rows=new Map();
  for(let p of eq){while(p.length){let l=lead(p);if(rows.has(l))p=add(p,rows.get(l));else{rows.set(l,p);break}}}
  if(rows.has(0n))return null;
  let lin=[...rows].find(([l])=>!isquad(l));
  if(!lin)return {eq:[...rows.values()],phase,subs};
  let [b,p]=lin,l=add(p,[b]);subs.push([b,l]);
  eq=[...rows.values()].map(e=>sub(e,b,l));phase=sub(phase,b,l);
 }
}
function gauss(p,free){
 let a=1n;
 while(free.length){
  let b=free[0];free=free.slice(1);
  let l=p.filter(m=>has(m,b)).map(m=>m^b),g=p.filter(m=>!has(m,b));
  if(l.length===1&&l[0]===0n)return 0n;
  a*=2n;
  if(!l.length){p=g;continue}
  let v=l.find(m=>m!==0n);
  if(v===undefined)throw Error("not affine");
  free=free.filter(m=>m!==v);p=sub(g,v,add(l,[v]));
 }
 if(p.some(m=>m!==0n))throw Error("free mismatch");
 return p.length?-a:a;
}
const dot=(a,b)=>parity(BigInt(a&b));
function interpolate(tab,g){
 let [a,b]=g;return norm([...(tab[0]?[0n]:[]),...((tab[1]^tab[0])?a:[]),...((tab[2]^tab[0])?b:[]),...((tab[0]^tab[1]^tab[2]^tab[3])?mul(a,b):[])]);
}
function compile(F,target){
 let {n,d,r,factors,eq=[]}=F, chars=[],maxq=0;
 let quotient=[];
 for(let j=r;j<d;j++){let p=(target>>j)&1?[0n]:[];for(let f of factors)p=add(p,interpolate(f.tab.map(t=>((t?.a??0)>>j)&1),f.g));quotient.push(p)}
 for(let lam=0;lam<2**r;lam++){
  let equations=[...eq,...quotient],phase=dot(lam,target)?[0n]:[];
  for(let f of factors){
   equations.push(interpolate(f.tab.map(t=>Number(!t||t.w.some(w=>dot(lam,w)))),f.g));
   phase=add(phase,interpolate(f.tab.map(t=>dot(lam,t?.a??0)),f.g));
  }
  let c=close(equations,phase);if(c){maxq=Math.max(maxq,c.eq.length);chars.push(c)}
 }
 let calls=0,gausses=0, maxAfter=0;
 function mass(probe=[],pins=[]){
  calls++;let z=0n;
  for(let c of chars){
   let trans=p=>c.subs.reduce((u,[b,l])=>sub(u,b,l),p);
   let cc=close([...c.eq,...pins.map(trans)],add(c.phase,trans(probe)));if(!cc)continue;
   if(cc.eq.length>c.eq.length)throw Error("q grew under affine pins");
   maxAfter=Math.max(maxAfter,cc.eq.length);
   let dead=new Set([...c.subs,...cc.subs].map(([b])=>b));
   let free=Array.from({length:n},(_,i)=>bit(i)).filter(b=>!dead.has(b)),sum=0n;
   for(let e=0;e<2**cc.eq.length;e++){
    let p=cc.phase;for(let j=0;j<cc.eq.length;j++)if(e>>j&1)p=add(p,cc.eq[j]);
    sum+=gauss(p,free);gausses++;
   }
   let den=1n<<BigInt(cc.eq.length);if(sum%den)throw Error("noninteger");z+=sum/den;
  }return z;
 }
 return {mass,maxq,stats:()=>({calls,gausses,maxAfter})};
}
function basisAdd(B,x){for(let i of [...B.keys()].sort((a,b)=>a>b?-1:1))if(has(x,i))x^=B.get(i);if(!x)return false;let p=bit(x.toString(2).length-1);B.set(p,x);return true}
function orth(B,m){let out=[];for(let i=0;i<m;i++){let b=bit(i);if(B.has(b))continue;let x=b;for(let p of [...B.keys()].sort((a,b)=>a<b?-1:1))if(parity(B.get(p)&x))x^=p;out.push(x)}return out}
function mon(n){let a=[0n];for(let i=0;i<n;i++)a.push(bit(i));for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)a.push(bit(i)|bit(j));return a}
function feat(m,x){return m.reduce((v,t,i)=>v|((t&x)===t?bit(i):0n),0n)}
function poly(m,v){return m.filter((_,i)=>has(v,bit(i)))}
function extract(F,solver){
 let m=mon(F.n),B=new Map(),I=new Map(),rounds=0,witnesses=[],total=solver.mass();
 if(!total)return {B,I,rounds,witnesses};
 while(B.size+I.size<m.length){
  let f=orth(B,m.length).find(x=>{let J=new Map(I);return basisAdd(J,x)});
  if(f===undefined)throw Error("gap");let p=poly(m,f);rounds++;
  if(solver.mass(p)===total){basisAdd(I,f);continue}
  let pins=[],x=0n;
  for(let j=0;j<F.n;j++){
   let trial=[...pins,[bit(j)]],z=solver.mass([],trial),s=solver.mass(p,trial);
   if(z!==s)pins=trial;else{pins.push([0n,bit(j)]);x|=bit(j)}
  }
  if(!ev(p,x)||!basisAdd(B,feat(m,x)))throw Error("bad witness");
  witnesses.push(x);
 }
 return {B,I,rounds,witnesses};
}
function reference(F,target){
 let R=[];
 for(let x=0n;x<bit(F.n);x++){
  if((F.eq??[]).some(p=>ev(p,x)))continue;
  let a=0,W=new Set([0]),ok=true;
  for(let f of F.factors){let t=f.tab[ev(f.g[0],x)+2*ev(f.g[1],x)];if(!t){ok=false;break}a^=t.a;for(let w of t.w)W=new Set([...W,...[...W].map(y=>y^w)])}
  if(ok&&W.has(a^target))R.push([x,BigInt(2**F.r/W.size)]);
 }return R;
}
let seed=0x2014004;function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
let stats={seed:"0x2014004",networks:0,sat:0,unsat:0,refAssignments:0,identityChecks:0,pairCells:0,featureComparisons:0,witnesses:0,rounds:0,massCalls:0,gaussCalls:0,maxq:0,nonlinearOnly:0,scaling:[]};
function assert(x){if(!x)throw Error("comparison failure")}
for(let t=0;t<70;t++){
 let n=2+rnd(4),r=rnd(3),d=r+1+rnd(2),m=mon(n),factors=[];
 const affine=()=>m.slice(0,n+1).filter(()=>rnd(2));
 for(let i=0;i<1+rnd(5);i++)factors.push({g:[affine(),affine()],tab:Array.from({length:4},()=>rnd(6)===0?null:{a:rnd(2**d),w:Array.from({length:rnd(3)},()=>rnd(2**r))})});
 let F={n,r,d,factors,eq:rnd(3)===0?[affine()]:[]},target=rnd(2**d),S=compile(F,target),R=reference(F,target),total=R.reduce((a,[x,w])=>a+w,0n);
 stats.networks++;stats.refAssignments+=2**n;stats[R.length?"sat":"unsat"]++;assert(S.mass()===total);
 for(let j=0;j<8;j++){let p=m.filter(()=>rnd(2)),a=S.mass(p),b=R.reduce((s,[x,w])=>s+(ev(p,x)?-w:w),0n);assert(a===b);stats.identityChecks++}
 let p=m.filter(()=>rnd(2)),q=m.filter(()=>rnd(2)),sp=S.mass(p),sq=S.mass(q),spq=S.mass(add(p,q));
 for(let a=0;a<2;a++)for(let b=0;b<2;b++){let v=(total+(a?-sp:sp)+(b?-sq:sq)+((a^b)?-spq:spq))/4n;assert(v===R.filter(([x])=>ev(p,x)===a&&ev(q,x)===b).reduce((s,[x,w])=>s+w,0n));stats.pairCells++}
 let E=extract(F,S),B=new Map(),A=new Map();for(let [x] of R){basisAdd(B,feat(m,x));basisAdd(A,feat(m.slice(0,n+1),x))}
 assert(E.B.size===B.size);for(let f of E.I.values())assert(R.every(([x])=>!ev(poly(m,f),x)));for(let x of E.witnesses)assert(R.some(([y])=>x===y));
 if(R.length){assert(E.I.size+B.size===m.length);assert(E.rounds===m.length);if(A.size===n+1&&B.size<m.length)stats.nonlinearOnly++}
 stats.featureComparisons++;stats.witnesses+=E.witnesses.length;stats.rounds+=E.rounds;let k=S.stats();stats.massCalls+=k.calls;stats.gaussCalls+=k.gausses;stats.maxq=Math.max(stats.maxq,S.maxq);
}
for(let n of [8,16,32,64,128]){
 let factors=[],p=[];for(let i=0;i<n;i+=2){factors.push({g:[[bit(i)],[bit(i+1)]],tab:[0,0,0,1].map(a=>({a,w:[]}))});p.push(bit(i)|bit(i+1))}
 let F={n,r:0,d:1,factors};let row={n};
 for(let c of [0,1]){let S=compile(F,c),Z=S.mass(),expected=((1n<<BigInt(n))+(c?-1n:1n)*(1n<<BigInt(n/2)))/2n;assert(Z===expected);assert(S.mass(p)===(c?-Z:Z));row["target"+c]=Z.toString();row.q=S.maxq;row["gauss"+c]=S.stats().gausses}
 // Separate UNSAT neighbor: require the opposite duplicate syndrome target.
 let G={...F,d:2,factors:factors.map(f=>({...f,tab:f.tab.map(t=>({...t,a:3*t.a}))}))},U=compile(G,1);assert(U.mass()===0n);row.unsatMass="0";stats.scaling.push(row)
}
return stats;
}
console.log(JSON.stringify(runGD04(),null,2));
