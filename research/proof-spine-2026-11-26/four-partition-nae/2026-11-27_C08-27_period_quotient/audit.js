function audit(){
const cap=200000, stats={checks:0,cutChecks:0,randomChecks:0}, cases=[];
function ck(b,m){stats.checks++;if(!b)throw Error(m)}
const range=n=>Array.from({length:n},(_,i)=>i), uniq=a=>[...new Set(a)];
function basis(xs){let p=new Map();for(let x of xs){while(x){let k=x.toString(2).length-1;if(!p.has(k)){p.set(k,x);break}x^=p.get(k)}}let arr=[...p].sort((a,b)=>b[0]-a[0]);return {rank:p.size,red(x){for(let [k,y] of arr)if((x>>BigInt(k))&1n)x^=y;return x}}}
function period(A){let s=new Set(A),a=A[0];return A.map(x=>x^a).filter(w=>A.every(x=>s.has(x^w)))}
function close(A,h){let rounds=0,drop=0;while(true){let W=basis(A.flatMap(period));if(!W.rank)return {A,h,rounds,drop};A=A.map(a=>uniq(a.map(x=>W.red(x))));h=W.red(h);rounds++;drop+=W.rank}}
function sum(A){let s=[0n];for(let a of A)s=uniq(s.flatMap(x=>a.map(y=>x^y)));return s}
let seed=20261127;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}
for(let j=0;j<250;j++){let A=range(2+rnd(4)).map(()=>uniq(range(1+rnd(9)).map(()=>BigInt(rnd(32)))));let s=new Set(sum(A));for(let h=0;h<32;h++){let q=close(A,BigInt(h));ck(s.has(BigInt(h))===sum(q.A).includes(q.h),"period closure mismatch");stats.randomChecks++}}
let iter=close([[0n,1n,2n],[0n,1n]],3n);ck(iter.rounds===2&&iter.drop===2,"iterative period");
let anti=[[1n,2n,3n],[0n]];ck(!sum(anti).includes(0n)&&basis(anti[0].map(x=>x^1n)).rank===2,"hull false");
const ag=[...range(3).map(r=>range(3).map(c=>3*r+c)),...range(3).map(c=>range(3).map(r=>3*r+c)),...range(3).map(k=>range(3).map(r=>3*r+(r+k)%3)),...range(3).map(k=>range(3).map(r=>3*r+(k-r+3)%3))];
function make(L){let rows=range(L).flatMap(j=>ag.map((r,i)=>({id:12*j+i,p:Math.floor(i/3),v:r.map(v=>9*j+v)})));
for(let j=0;j<L-1;j++){let a=rows[12*j+1],b=rows[12*(j+1)+0];[a.v[0],b.v[0]]=[b.v[0],a.v[0]]}
let pairs=new Set();for(let r of rows){ck(new Set(r.v).size===3,"triple");for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let k=[r.v[i],r.v[j]].sort((a,b)=>a-b).join();ck(!pairs.has(k),"linear");pairs.add(k)}}
for(let p=0;p<4;p++){let vs=rows.filter(r=>r.p===p).flatMap(r=>r.v);ck(vs.length===9*L&&new Set(vs).size===9*L,"partition")}
let core=rows.filter(r=>r.v.every(v=>v<9));ck(core.length>=11,"retained AG9 core");
for(let w=0;w<512;w++)ck(!core.every(r=>{let a=r.v.map(v=>(w>>v)&1);return a.some(x=>x!==a[0])}),"core no");
return rows}
function comps(rows){let parent=new Map();function root(v){if(!parent.has(v))parent.set(v,v);while(parent.get(v)!==v)v=parent.get(v);return v}for(let r of rows){let a=root(r.v[0]);for(let v of r.v.slice(1)){let b=root(v);if(a!==b)parent.set(b,a)}}return {count:new Set([...parent.keys()].map(root)).size,vs:new Set(parent.keys())}}
function encode(rows){let occ=new Map();rows.forEach((r,i)=>r.v.forEach((v,j)=>{if(!occ.has(v))occ.set(v,[]);occ.get(v).push([i,j])}));let C=rows.map(()=>[0n,0n,0n]),r=0;
for(let a of occ.values()){for(let j=1;j<a.length;j++){let q=1n<<BigInt(r++);C[a[0][0]][a[0][1]]^=q;C[a[j][0]][a[j][1]]^=q}}
let A=C.map(c=>range(6).map(w=>w+1).map(w=>c.reduce((s,x,j)=>s^(((w>>j)&1)?x:0n),0n)));let W=basis(A.flatMap(period));let G=C.map(c=>c.map(x=>W.red(x)));let B=A.map(a=>uniq(a.map(x=>W.red(x))));ck(B.every(a=>a.length===3),"NAE three phases");return {C,A,G,B,r,W}}
function measure(rows,E,P){let ps=new Set(P),Q=range(rows.length).filter(i=>!ps.has(i)),a=comps(P.map(i=>rows[i])),b=comps(Q.map(i=>rows[i])),c=comps(rows);let split=[...a.vs].filter(v=>b.vs.has(v)).length;
function lambda(C){return basis(P.flatMap(i=>C[i])).rank+basis(Q.flatMap(i=>C[i])).rank-basis(C.flat()).rank}
let raw=lambda(E.C),quot=lambda(E.G),seam=split-a.count-b.count+c.count;ck(raw===split&&quot===seam&&quot<=raw,"cycle rank formula");stats.cutChecks++;return [raw,quot]}
function dp(A,C,order){let s=[0n],peak=1,work=0;let suffix=order.map((_,i)=>basis(order.slice(i+1).flatMap(j=>C[j])));
for(let i=0;i<order.length;i++){let out=new Set();for(let x of s)for(let a of A[order[i]]){if(++work>cap)return {status:"UNKNOWN",work:cap,peak};let y=x^a;if(suffix[i].red(y)===0n)out.add(y)}s=[...out];peak=Math.max(peak,s.length);if(!s.length)return {status:"UNSAT",work,peak,emptyAt:i+1}}
return {status:s.includes(0n)?"SAT":"UNSAT",work,peak}}
for(let L of [1,2,4,8,16]){let rows=make(L),E=encode(rows);ck(E.W.rank===rows.length-1,"connected phase rank");
let order=range(rows.length),part=order.slice().sort((a,b)=>rows[a].p-rows[b].p||a-b);
let w=[0,0],p=[0,0];for(let i=0;i<=order.length;i++){let t=measure(rows,E,order.slice(0,i)),u=measure(rows,E,part.slice(0,i));w=w.map((x,j)=>Math.max(x,t[j]));p=p.map((x,j)=>Math.max(x,u[j]))}
if(L===1)for(let mask=0;mask<4096;mask++)measure(rows,E,order.filter(i=>(mask>>i)&1));
let raw=dp(E.A,E.C,order),quot=dp(E.B,E.G,order);ck(raw.status==="UNSAT"&&quot.status==="UNSAT","DP expected no");
cases.push({L,variables:9*L,owners:rows.length,source:rows,encodedJSONBytes:JSON.stringify(rows).length,rawRank:E.r,periodRank:E.W.rank,quotientRank:E.r-E.W.rank,groupedWidths:w,partitionWidths:p,raw,quot})}
return {cap,stats,cases,controls:{iterativeRounds:iter.rounds,iterativeRankDrop:iter.drop,affineHullFalse:true},seed:20261127}
}
console.log(JSON.stringify(audit(),null,2));
