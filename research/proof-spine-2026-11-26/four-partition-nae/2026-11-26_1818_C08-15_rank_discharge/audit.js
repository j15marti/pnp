// node audit.js -- C08-15 deterministic interleaved audit
function audit(){
let seed=20261126,checks=0,miCalls=0,aug=0,exchange=0,localNodes=0,kernelMasks=0;
const ok=(v,m)=>{checks++;if(!v)throw Error(m||"check "+checks)};
function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)%n}
const bit=(w,i)=>Number((w>>BigInt(i))&1n), eb=i=>1n<<BigInt(i);
function parity(w){let x=0;while(w){w&=w-1n;x^=1}return x}
const countBits=w=>{let n=0;while(w){w&=w-1n;n++}return n};
const nae=(c,x)=>x[c[0]]!==x[c[1]]||x[c[0]]!==x[c[2]],valid=(C,x)=>C.every(c=>nae(c,x)),defects=(C,x)=>C.reduce((s,c)=>s+!nae(c,x),0);
const pairs=c=>[[c[0],c[1]],[c[0],c[2]],[c[1],c[2]]];
const AG=[[[0,1,2],[3,4,5],[6,7,8]],[[0,3,6],[1,4,7],[2,5,8]],[[0,4,8],[1,5,6],[2,3,7]],[[0,5,7],[1,3,8],[2,4,6]]];
const P=[[[4,11,14],[5,9,12],[3,7,10],[2,6,13],[0,1,8]],[[8,9,14],[0,2,11],[4,6,10],[5,7,13],[1,3,12]],[[2,3,9],[1,5,6],[4,7,12],[8,10,11],[0,13,14]],[[4,8,13],[3,5,14],[1,2,7],[0,9,10],[6,11,12]]];
function dsu(n){let p=Array.from({length:n},(_,i)=>i);function f(x){while(p[x]!==x){p[x]=p[p[x]];x=p[x]}return x}return{f,add(a,b){a=f(a);b=f(b);if(a===b)return false;p[a]=b;return true}}}
function auth(F,n){ok(F.length===4);let seen=new Set,D=dsu(n);for(let part of F){let d=Array(n).fill(0);for(let c of part){ok(c.length===3&&new Set(c).size===3);for(let v of c){ok(v>=0&&v<n);d[v]++}for(let [a,b] of pairs(c)){let key=Math.min(a,b)*n+Math.max(a,b);ok(!seen.has(key));seen.add(key);D.add(a,b)}}ok(d.every(x=>x===1))}ok(Array.from({length:n},(_,i)=>D.f(i)).every(v=>v===D.f(0)))}
function gf4(k){let F=[[],[],[],[]],mul=[0,2,3,1];for(let t=0;t<k;t++)for(let s=0;s<4;s++)for(let i=0;i<4;i++){let v=12*t;F[s].push([v+i,v+4+(i^s),v+8+(i^mul[s])])}return F}
function ring(no){let F=[[],[],[],[]];for(let t=0;t<2;t++)for(let s=0;s<4;s++)for(let i=0;i<3;i++){let c=AG[s][i].map(v=>v+9*t);if(s===0&&(i===0||(!no&&i===1)))c[2]=AG[0][i][2]+9*(1-t);F[s].push(c)}return F}
function attached(k,no){let F=ring(no),G=gf4(k);for(let s=0;s<4;s++)F[s].push(...G[s].map(c=>c.map(v=>v+18)));let owners=[F[0][2],...Array.from({length:k},(_,i)=>F[0][6+4*i])],old=owners.map(c=>c[2]);owners.forEach((c,i)=>c[2]=old[(i+1)%old.length]);return F}
function cyclic(p){return Array.from({length:4},(_,s)=>Array.from({length:p},(_,i)=>[i,p+(i+s)%p,2*p+(i+3*s)%p]))}
function torus(k){let F=[[],[],[],[]];for(let t=0;t<k;t++)for(let j=0;j<4;j++)for(let i=0;i<5;i++){let c=P[j][i].map(v=>v+15*t);if(j===0&&i<2)c[0]=15*((t+1)%k)+P[0][i][0];F[j].push(c)}return F}
function basis(n){let piv=Array(n).fill(null),rank=0;
function red(r,b=0){for(let i=n-1;i>=0;i--)if(piv[i]&&(r&eb(i))){r^=piv[i][0];b^=piv[i][1]}return[r,b]}
function add(r,b=0){[r,b]=red(r,b);if(!r)return b?-1:0;let p=r.toString(2).length-1;piv[p]=[r,b];rank++;return 1}
function solve(w=0n,hom=false){for(let i=0;i<n;i++)if(piv[i]){let b=(hom?0:piv[i][1])^parity(piv[i][0]&w);if(b)w^=eb(i)}return w}
function ker(){let K=[];for(let i=0;i<n;i++)if(!piv[i])K.push(solve(eb(i),true));return K}
return{red,add,solve,ker,get rank(){return rank}}}
function mi(E,n){miCalls++;let I=new Set;
for(;;){let T=[...I],byOwner=new Map(T.map(e=>[E[e].o,e])),piv=Array(n).fill(null);
function red(v,t){for(let i=n-1;i>=0;i--)if(piv[i]&&(v&eb(i))){v^=piv[i][0];t^=piv[i][1]}return[v,t]}
T.forEach((e,i)=>{let[v,t]=red(E[e].r,eb(i));ok(v!==0n);piv[v.toString(2).length-1]=[v,t]});
let outside=E.map((_,i)=>i).filter(i=>!I.has(i)),info=new Map,q=[],prev=new Map,pos=new Map(T.map((e,i)=>[e,i]));
for(let e of outside){let [v,t]=red(E[e].r,0n);info.set(e,[v,t]);if(v){q.push(e);prev.set(e,-1)}}
let end=-1;for(let i=0;i<q.length&&end<0;i++){let e=q[i];if(!I.has(e)){let f=byOwner.get(E[e].o);if(f===undefined){end=e;break}if(!prev.has(f)){prev.set(f,e);q.push(f)}}else{for(let f of outside){exchange++;let [v,t]=info.get(f);if(!prev.has(f)&&(v!==0n||(t&eb(pos.get(e))))){prev.set(f,e);q.push(f)}}}}
if(end<0)return T.map(e=>E[e]);
for(let e=end;e>=0;e=prev.get(e)){if(I.has(e))I.delete(e);else I.add(e)}aug++;ok(I.size===T.length+1);
}}
function guard(C,n,rows){let H=basis(n);for(let [a,b] of rows)ok(H.add(a,b)>=0);let q=H.rank,forced=[],zero=[],E=[];
C.forEach((c,o)=>{let p=pairs(c).map(([u,v])=>{let a=eb(u)^eb(v),[r,b]=H.red(a);return {o,a,r,b,u,v}});if(p.some(e=>e.r===0n&&e.b===1))forced.push(o);else{if(p.every(e=>e.r===0n))zero.push(o);for(let e of p)if(e.r)E.push(e)}});
let R=mi(E,n),G=basis(n);rows.forEach(([a,b])=>ok(G.add(a,b)>=0));for(let e of R)ok(G.add(e.a,1)===1);let w=G.solve(),x=Array.from({length:n},(_,i)=>bit(w,i));ok(rows.every(([a,b])=>parity(a&w)===b));ok(forced.every(i=>nae(C[i],x))&&R.every(e=>nae(C[e.o],x)));ok(new Set(R.map(e=>e.o)).size===R.length);
ok(forced.length*7<=16*q&&R.length<=n-1-q);let D=C.length-forced.length-R.length;ok(7*D>=7*(C.length-n+1)-9*q);return{q,f:forced.length,r:R.length,D,forced,zero,x,actual:C.length-defects(C,x)}}
let guardStats={cases:0,positiveCertificates:0,actualBetter:0,profiles:0,sharp:0};
for(let [F,n] of [[AG,9],[gf4(1),12],[cyclic(5),15]]){auth(F,n);let C=F.flat(),m=C.length,words=[];for(let w=0;w<2**n;w+=2){let W=BigInt(w),x=Array.from({length:n},(_,i)=>bit(W,i)),mask=C.reduce((a,c,i)=>nae(c,x)?a|(1<<i):a,0);words.push({W,mask,score:m-defects(C,x)})}
for(let j=0;j<30;j++){let q=j%(n),H=basis(n),rows=[],w=BigInt(2*rnd(2**(n-1)));while(H.rank<q){let a=0n;if(j%2===0){let u=rnd(n),v=rnd(n);a=eb(u)^eb(v)}else{for(let i=1;i<n;i++)if(rnd(2))a^=eb(i)^1n}let b=parity(a&w);if(H.add(a,b)===1)rows.push([a,b])}
let z=guard(C,n,rows),mask=(1<<m)-1,un=0,opt=-1,profiles=0;for(let p of words)if(rows.every(([a,b])=>parity(a&p.W)===b)){mask&=p.mask;un|=p.mask;opt=Math.max(opt,p.score);profiles++}
ok(profiles>0&&profiles===2**(n-1-q));ok(z.f===countBits(BigInt(mask))&&z.zero.length===m-countBits(BigInt(un)));ok(z.actual<=opt&&z.actual>=z.f+z.r);ok(z.q===q);if(!q)ok(z.r===n-1);guardStats.cases++;guardStats.profiles+=profiles;guardStats.positiveCertificates+=z.D===0;guardStats.actualBetter+=z.actual>z.f+z.r;guardStats.sharp+=z.q>0&&7*z.f===16*z.q;
}}
let G=gf4(1).flat(),sharpRows=Array.from({length:7},(_,i)=>[eb(0)^eb(i+1),i+1>=4?1:0]),sharp=guard(G,12,sharpRows);ok(sharp.q===7&&sharp.f===16&&sharp.D===0);
function region(C,n,S){let A=new Set(S),adj=new Map(S.map(v=>[v,[]])),touch=[];for(let i=0;i<C.length;i++){let t=C[i].filter(v=>A.has(v));if(!t.length)continue;if(t.length!==2)return null;adj.get(t[0]).push(t[1]);adj.get(t[1]).push(t[0]);touch.push(i)}if(!touch.length)return null;let col=new Map;for(let v of S)if(!col.has(v)){col.set(v,0);let q=[v];for(let i=0;i<q.length;i++)for(let u of adj.get(q[i])){if(!col.has(u)){col.set(u,1^col.get(q[i]));q.push(u)}else if(col.get(u)===col.get(q[i]))return null}}return{S:[...S],col,touch}}
function local(C,n,L){let inc=Array.from({length:n},()=>[]);C.forEach((c,i)=>c.forEach(v=>inc[v].push(i)));
function dfs(S){localNodes++;let touched=new Set,one=null;for(let v of S)for(let i of inc[v])touched.add(i);for(let i of touched){let a=C[i].filter(v=>S.has(v));if(a.length===3)return null;if(a.length===1&&!one)one=C[i].filter(v=>!S.has(v))}
if(!one)return region(C,n,[...S]);if(S.size>=L)return null;for(let v of one){S.add(v);let r=dfs(S);S.delete(v);if(r)return r}return null}
for(let v=0;v<n;v++)if(inc[v].length){let r=dfs(new Set([v]));if(r)return r}return null}
function kernel(C,n,cap=12){let B=basis(n);for(let c of C)B.add(c.reduce((s,v)=>s^eb(v),0n));let K=B.ker(),dim=K.length;if(dim>cap)return{dim,status:"UNKNOWN",r:null};for(let i=1;i<2**dim;i++){kernelMasks++;let w=0n;for(let j=0;j<dim;j++)if((i>>j)&1)w^=K[j];let S=Array.from({length:n},(_,j)=>j).filter(j=>bit(w,j)),D=dsu(n);for(let c of C){let t=c.filter(v=>bit(w,v));ok(t.length===0||t.length===2);if(t.length)D.add(...t)}let M=new Map;for(let v of S){let a=D.f(v);if(!M.has(a))M.set(a,[]);M.get(a).push(v)}for(let a of M.values()){let r=region(C,n,a);if(r)return{dim,status:"FOUND",r}}}return{dim,status:"NONE",r:null}}
function exact(C,n,x){let active=[...new Set(C.flat())],D=dsu(n);for(let c of C)D.add(c[0],c[1]),D.add(c[0],c[2]);let comps=new Map;for(let v of active){let a=D.f(v);if(!comps.has(a))comps.set(a,[]);comps.get(a).push(v)}let max=0,trials=0;for(let V of comps.values()){max=Math.max(max,V.length);if(V.length>20)return{status:"UNKNOWN",max,trials};let id=new Map(V.map((v,i)=>[v,i])),L=C.filter(c=>id.has(c[0])).map(c=>c.map(v=>id.get(v))),found=false;for(let w=0;w<2**V.length;w+=2){trials++;if(L.every(c=>((w>>c[0])&1)!==((w>>c[1])&1)||((w>>c[0])&1)!==((w>>c[2])&1))){V.forEach((v,i)=>x[v]=(w>>i)&1);found=true;break}}if(!found)return{status:"UNSAT",max,trials}}ok(valid(C,x));return{status:"SAT",max,trials,x}}
function peel(C,n,x){let F=C.slice(),regions=[],before=defects(C,x),last=before,steps=0;for(;;){let r=local(F,n,8);if(!r)break;let old=C.map(c=>nae(c,x)),d0=last;for(let v of r.S)x[v]=r.col.get(v);ok(C.every((c,i)=>!old[i]||nae(c,x)));ok(r.touch.every(i=>nae(F[i],x)));last=defects(C,x);ok(last<=d0);let ids=new Set(r.touch);regions.push({size:r.S.length,owners:r.touch.length,gain:d0-last});F=F.filter((_,i)=>!ids.has(i));steps++}let z=exact(F,n,x);if(z.status==="SAT")ok(valid(C,z.x));return{steps,regions,before,after:last,remaining:F.length,status:z.status,max:z.max,trials:z.trials}}
let attachedResults=[];for(let k of [1,2,4,8,16,32,64])for(let no of [false,true]){let F=attached(k,no),n=18+12*k,C=F.flat();auth(F,n);let x=Array(n).fill(0);for(let v=0;v<18;v++){let b=Math.floor(v/9),i=v%9;x[v]=i<3?b%2:i<6?1^(b%2):+(i===8)}x[26]=1;let Pcopy=x.slice();if(no){let c=C.filter(c=>c.every(v=>v>=9&&v<18));ok(c.length===11);ok(exact(c,n,x.slice()).status==="UNSAT")}else{let y=x.slice();for(let t=0;t<k;t++)for(let j=4;j<8;j++)y[18+12*t+j]=1;ok(valid(C,y))}
let A=local(C,n,8),B=kernel(C,n),q=peel(C,n,Pcopy);ok(A!==null&&q.status===(no?"UNSAT":"SAT"));attachedResults.push({k,n,label:no?"UNSAT":"SAT",localFirst:A.S.length,kernelDim:B.dim,kernelStatus:B.status,regions:q.steps,removed:C.length-q.remaining,before:q.before,after:q.after,remaining:q.remaining,exactMax:q.max,exactTrials:q.trials})}
let cyclicResults=[];for(let p of [5,7,13,31,127]){let n=3*p,F=cyclic(p),C=F.flat();auth(F,n);let A=local(C,n,8),B=kernel(C,n);ok(A===null&&B.dim===2&&B.status==="FOUND"&&B.r.S.length===2*p&&B.r.touch.length===C.length);let x=Array(n).fill(0);for(let v of B.r.S)x[v]=B.r.col.get(v);ok(valid(C,x));cyclicResults.push({n,local:"NONE",dim:B.dim,support:B.r.S.length,owners:B.r.touch.length,status:"SAT"})}
function safe(F,n){let D=dsu(n);for(let c of F.slice(1).flat()){D.add(c[0],c[1]);D.add(c[0],c[2])}let groups=new Map;for(let v=0;v<n;v++){let a=D.f(v);if(!groups.has(a))groups.set(a,[]);groups.get(a).push(v)}let x=Array(n),trials=0;for(let V of groups.values()){ok(V.length<=15);let id=new Map(V.map((v,i)=>[v,i])),inside=F.flat().filter(c=>c.every(v=>id.has(v))).map(c=>c.map(v=>id.get(v))),P=F[0].map(c=>c.filter(v=>id.has(v))).filter(c=>c.length===2).map(c=>c.map(v=>id.get(v)));let found=false;for(let w=0;w<2**V.length;w++){trials++;if(inside.every(c=>((w>>c[0])&1)!==((w>>c[1])&1)||((w>>c[0])&1)!==((w>>c[2])&1))&&P.every(c=>((w>>c[0])&1)!==((w>>c[1])&1))){V.forEach((v,i)=>x[v]=(w>>i)&1);found=true;break}}ok(found)}ok(valid(F.flat(),x));return{blocks:groups.size,trials}}
let torusResults=[];let pRank=basis(15);P.flat().slice(2).forEach(c=>pRank.add(c.reduce((a,v)=>a^eb(v),0n)));ok(pRank.rank===15);
for(let k of [2,4,8,16,32]){let n=15*k,F=torus(k),C=F.flat();auth(F,n);let A=local(C,n,8),B=kernel(C,n),S=safe(F,n);ok(A===null&&B.dim===0&&B.status==="NONE");torusResults.push({n,kernelDim:B.dim,local:"NONE",geometricBlocks:S.blocks,geometricTrials:S.trials,status:"SAT"})}
return{seed:20261126,checks,miCalls,aug,exchange,localNodes,kernelMasks,guardStats,sharp:{q:sharp.q,f:sharp.f,r:sharp.r,D:sharp.D},attachedResults,cyclicResults,torusResults,pRank:pRank.rank}
}
console.log(JSON.stringify(audit(),null,2));
