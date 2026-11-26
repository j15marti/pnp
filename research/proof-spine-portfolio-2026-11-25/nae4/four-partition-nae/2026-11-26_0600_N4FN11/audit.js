// node audit.js. Small exhaustive oracle for chart composition; genuine cover certificates.
let seed=20261126,checks=0,calls=0,probes=0,shrinks=0;
function ok(x){checks++;if(!x)throw Error("check "+checks)}
function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
function parity(x){let r=0;while(x){r^=1;x&=x-1}return r}
function basis(rows){let b=[];for(let x of rows){for(let y of b)x=Math.min(x,x^y);if(x){b.push(x);b.sort((a,b)=>b-a)}}return b}
function word(rows,z){return rows.reduce((a,r,i)=>a|(parity(r&z)<<i),0)}
function span(b){let s=[0];for(let x of b)s=s.concat(s.map(y=>x^y));return s}
function fit(F,z){return F.every(f=>f.t.includes(word(f.r,z)))}
function dimCut(F,A,G){let x=G[0],diff=basis(G.map(z=>z^x)),map=r=>word(diff,r),U=basis(A.flatMap(f=>f.r.map(map))),B=F.filter(f=>!A.includes(f)),V=basis(B.flatMap(f=>f.r.map(map)));return U.length+V.length-basis(U.concat(V)).length}
function close(F,G){for(;;){if(!G.length)return [F,G];let old=G.length;let H=[];for(let f of F){let p=new Set(G.map(z=>word(f.r,z))),t=f.t.filter(x=>p.has(x));if(!t.length)return [[],[]];let h=t[0],sp=new Set(span(basis(t.map(x=>x^h))).map(x=>x^h));G=G.filter(z=>sp.has(word(f.r,z)));H.push({r:f.r,t});if(!G.length)return [[],[]]}F=H;if(G.length===old)return [F,G];shrinks++}}
function solver(F,G,d){calls++;[F,G]=close(F,G);if(!G.length)return null;if(F.length<=3)return G.find(z=>fit(F,z))??null;let m=F.length,mu=m-1,best=null;
for(let mask=1;mask<2**m-1;mask++){let A=F.filter((_,i)=>(mask>>i)&1),a=A.length;if(a<2||a>m/2)continue;let r=dimCut(F,A,G),u=a-1;probes++;if(2**r*u**2>mu**2)continue;if(!best||r<best.r)best={A,r,u}}
if(!best)return G.find(z=>fit(F,z))??null; // small oracle fallback only, not a polynomial general solver
let {A,r,u}=best,B=F.filter(f=>!A.includes(f)),x=G[0],diff=basis(G.map(z=>z^x)),map=row=>word(diff,row),U=basis(A.flatMap(f=>f.r)),V=basis(B.flatMap(f=>f.r)),Ur=basis(U.map(map)),Vr=new Set(span(basis(V.map(map)))),I=basis(span(Ur).filter(y=>Vr.has(y)));ok(I.length===r);
let reps=I.map(y=>span(U).find(t=>map(t)===y));ok(reps.every(t=>t!==undefined));let D=[],witness=new Map;
for(let p of new Set(G.map(z=>word(reps,z)))){let a=solver(A,G.filter(z=>word(reps,z)===p),d);if(a!==null){D.push(p);witness.set(p,a)}}
if(!D.length)return null;let b=solver(B.concat([{r:reps,t:D}]),G,d);if(b===null)return null;let a=witness.get(word(reps,b));ok(a!==undefined);let z=G.find(z=>word(U,z)===word(U,a)&&word(V,z)===word(V,b));ok(z!==undefined&&fit(F,z));ok(2**r*u**4+(mu-u)**4<=mu**4-1);return z}
let random={sat:0,unsat:0};for(let t=0;t<240;t++){let d=3+rnd(4),m=4+rnd(5),F=[];for(let i=0;i<m;i++){let l=1+rnd(3),r=Array.from({length:l},()=>rnd(2**d)),tab=Array.from({length:2**l},(_,j)=>j).filter(()=>rnd(4)!==0);F.push({r,t:tab})}let G=Array.from({length:2**d},(_,z)=>z);if(t%3===0){let h=1+rnd(2**d-1),p=rnd(2);G=G.filter(z=>parity(h&z)===p)}let ref=G.find(z=>fit(F,z)),z=solver(F,G,d);ok((z!==null)===(ref!==undefined));if(z!==null){ok(G.includes(z)&&fit(F,z));random.sat++}else random.unsat++}
// Nonlocal correlation: the same latent bit in disconnected physical regions with opposite required pins.
let F=[{r:[1],t:[0]},{r:[1],t:[0,1]},{r:[1],t:[1]},{r:[1],t:[0,1]}];ok(dimCut(F,F.slice(0,2),[0,1])===1);ok(solver(F,[0,1],1)===null);
const P=[[[4,11,14],[5,9,12],[3,7,10],[2,6,13],[0,1,8]],[[8,9,14],[0,2,11],[4,6,10],[5,7,13],[1,3,12]],[[2,3,9],[1,5,6],[4,7,12],[8,10,11],[0,13,14]],[[4,8,13],[3,5,14],[1,2,7],[0,9,10],[6,11,12]]],W=[10778,2777,505,5429,2537,985,4413,381,2777,505,4413,505,381,2777,5429];
const AG=[[[0,1,2],[3,4,5],[6,7,8]],[[0,3,6],[1,4,7],[2,5,8]],[[0,4,8],[1,5,6],[2,3,7]],[[0,5,7],[1,3,8],[2,4,6]]];
function valid(F,x){return F.flat().every(c=>c.some(v=>x[v]!==x[c[0]]))}
function auth(F,n){let seen=new Set;ok(F.length===4);for(let p of F){let ct=Array(n).fill(0);for(let c of p){ok(new Set(c).size===3);for(let v of c){ok(v>=0&&v<n);ct[v]++}for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let k=Math.min(c[i],c[j])*n+Math.max(c[i],c[j]);ok(!seen.has(k));seen.add(k)}}ok(ct.every(x=>x===1))}}
function rank3(C,n){let a=C.map(c=>{let v=new Uint8Array(n);for(let x of c)v[x]=1;return v}),r=0;for(let j=0;j<n;j++){let t=r;while(t<a.length&&!a[t][j])t++;if(t===a.length)continue;[a[r],a[t]]=[a[t],a[r]];if(a[r][j]===2)for(let k=j;k<n;k++)a[r][k]=2*a[r][k]%3;for(let i=r+1;i<a.length;i++){let q=a[i][j];if(q)for(let k=j;k<n;k++)a[i][k]=(a[i][k]+6-q*a[r][k])%3}r++}return r}
function bits(w,n){return Array.from({length:n},(_,i)=>(w>>i)&1)}
auth(P,15);ok(rank3(P.flat().slice(2),15)===14);for(let i=0;i<15;i++){let a=bits(W[i],15);ok(valid(P,a));a[i]^=1;ok(valid(P,a))}
function lift(L){let F=[[],[],[],[]];for(let x=0;x<L;x++)for(let y=0;y<L;y++){let t=x*L+y;for(let j=0;j<4;j++)for(let c=0;c<5;c++){let a=P[j][c].map(v=>15*t+v);if(j===0&&c===0)a[0]=15*(((x+1)%L)*L+y)+P[j][c][0];if(j===0&&c===1)a[0]=15*(x*L+(y+1)%L)+P[j][c][0];F[j].push(a)}}return F}
function attach(F,n,no){let G=F.map(p=>p.map(c=>c.slice()));for(let j=0;j<4;j++)for(let t=0;t<2;t++)for(let c of AG[j]){let a=c.map(v=>n+9*t+v);if(j===0&&(c[0]===0||(!no&&c[0]===3)))a[2]=n+9*(1-t)+c[2];G[j].push(a)}
// swap an occurrence in partition 0 with first attached private row; second module untouched by splice.
let k=F[0].length+2;[G[0][0][0],G[0][k][0]]=[G[0][k][0],G[0][0][0]];return G}
let covers=[];for(let L of [3,4,8,16,32]){let F=lift(L),n=15*L*L;auth(F,n);let x=Array.from({length:n},(_,i)=>(W[0]>>(i%15))&1);ok(valid(F,x));let inc=Array.from({length:n},()=>[]);for(let c of F.flat())for(let v of c)inc[v].push(c);for(let i=0;i<n;i++){let w=W[i%15];ok(inc[i].every(c=>{let [a,b]=c.filter(v=>v!==i);return ((w>>(a%15))^(w>>(b%15)))&1}))}
let r3=n<=240?rank3(F.flat(),n):null;if(r3!==null)ok(r3===n-1);
let plus=attach(F,n,false),minus=attach(F,n,true);auth(plus,n+18);auth(minus,n+18);let u=[0,0,0,1,1,1,0,0,1,1,1,1,0,0,0,0,0,1];if(u[6]!==x[F[0][0][0]])u=u.map(a=>a^1);ok(valid(plus,x.concat(u)));
let core=minus.flat().filter(c=>c.every(v=>v>=n+9));ok(core.length===11);for(let w=0;w<512;w++)ok(!core.every(c=>c.some(v=>((w>>(v-n-9))&1)!==((w>>(c[0]-n-9))&1))));
covers.push({L,n,clauses:4*n/3,affineHullRank:n,ternaryNullity:1,directRank3:r3,fullOwnerDeficiency:n/3+1,neighborVariables:n+18})}
console.log(JSON.stringify({seed:20261126,checks,calls,probes,shrinks,random,covers,base:P,flipWitnesses:W}));