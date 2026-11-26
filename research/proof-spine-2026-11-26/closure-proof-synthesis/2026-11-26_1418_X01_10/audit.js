function audit(){
let checks=0;const ok=(v,m)=>{checks++;if(!v)throw Error(m||"check "+checks)};let seed=20261126;function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)%n}
const bit=i=>1n<<BigInt(i), hi=x=>x.toString(2).length-1, par=x=>{let a=0;while(x){x&=x-1n;a^=1}return a};
function add(B,z,p=0n){while(z){let j=hi(z);if(!B.has(j)){B.set(j,[z,p]);return true}let [v,w]=B.get(j);z^=v;p^=w}return false}
function red(B,z){let p=0n;for(let j of [...B.keys()].sort((a,b)=>b-a))if(z&bit(j)){let [v,w]=B.get(j);z^=v;p^=w}return [z,p]}
function image(M,w){let x=0n;for(let i=0;i<M.length;i++)if(par(M[i]&w))x|=bit(i);return x}
function stab(R){let a=R[0],S=new Set(R),D=[];for(let b of R){let d=a^b;if(d&&R.every(x=>S.has(x^d)))D.push(d)}return D}
function close(G,target){let rounds=0,deleted=0;let R=G.map(g=>g.slice());for(;;){rounds++;let changed=false;for(let j=0;j<R.length;j++){let B=new Map(),offset=target;for(let i=0;i<R.length;i++)if(i!==j){let a=R[i][0].z;offset^=a;for(let x of R[i])add(B,x.z^a)}let S=R[j].filter(x=>red(B,x.z^offset)[0]===0n);if(!S.length)return {R:null,rounds,deleted};if(S.length!==R[j].length){deleted+=R[j].length-S.length;R[j]=S;changed=true}}if(!changed)return{R,rounds,deleted}}}
function solve(G,target,cap,mode){let B=new Map(),vectors=[],trials=0,peak=1;
 for(let i=0;i<G.length;i++){let g=G[i],R=[...new Set(g.map(x=>x.z))];if(mode==="projected"){for(let d of stab(R)){let k=vectors.length;if(add(B,d,bit(k)))vectors.push([i,d])}}else if(mode==="raw"){let W=[...new Set(g.map(x=>x.w))];for(let d of stab(W)){let j=g.find(x=>x.w===(g[0].w^d));let delta=j.z^g[0].z;if(g.every(x=>g.some(y=>y.w===(x.w^d)&&y.z===(x.z^delta)))){let k=vectors.length;if(add(B,delta,bit(k)))vectors.push([i,delta])}}}}
 let L=new Map([[0n,[]]]);
 for(let i=0;i<G.length;i++){let Q=new Map(),unique=new Map();for(let x of G[i])unique.set(red(B,x.z)[0],x);
 for(let [z,path] of L)for(let [u,x] of unique){trials++;let v=z^u;if(!Q.has(v)){Q.set(v,path.concat([x]));if(Q.size>cap)return {answer:"UNKNOWN",rank:B.size,trials,peak:Math.max(peak,Q.size)}}}
 L=Q;peak=Math.max(peak,L.size)}
 let p=L.get(red(B,target)[0]);if(!p)return{answer:"NO",rank:B.size,trials,peak};
 let delta=p.reduce((z,x)=>z^x.z,target),[r,coeff]=red(B,delta);ok(r===0n);
 let changes=G.map(()=>0n);vectors.forEach(([i,d],j)=>{if(coeff&bit(j))changes[i]^=d});
 let w=p.map((x,i)=>G[i].find(y=>y.z===(x.z^changes[i])));ok(w.every(Boolean));ok(w.reduce((z,x)=>z^x.z,0n)===target);return{answer:"YES",rank:B.size,trials,peak,w}
}
const ATOM=[[0,2,4],[0,2,5],[0,3,5],[1,2,4],[1,3,4],[1,3,5]],BI=[[0,7,8],[6,2,3],[6,7,8],[1,10,11],[9,2,3],[9,10,11]],BE=[[0,4,3],[0,4,5],[1,2,5],[1,4,5]];
function own(T,w,shared){let C=new Map();for(let i=0;i<T.length;i++)for(let v of T[i])C.set(v,(C.get(v)||0)+Number(!!(w&bit(i))));for(let [v,c] of C)if(shared.has(v)?c>1:c!==1)return false;return true}
function words(T,shared=new Set()){let R=[];for(let w=0n;w<bit(T.length);w++)if(own(T,w,shared))R.push(w);return R}
let atomW=words(ATOM);ok(atomW.length===3);ok(stab(atomW).length===0);
function build(k,yes){let T=[],groups=[],guards=[],owners=new Map(),next=20,core=[],side=[];const shared=new Set([0,1,2,3]);
 function block(raw,W,base=false){let offset=T.length,map=new Map();for(let t of raw){let row=t.map((v,j)=>{if(base&&v<4)return v;if(!map.has(v))map.set(v,next++);return map.get(v)});row.forEach((v,j)=>{ok(!owners.has(v)||owners.get(v)===j);owners.set(v,j)});T.push(row)}let g={offset,len:raw.length,W:W.map(w=>w<<BigInt(offset))};groups.push(g);return offset}
 function atom(){return block(ATOM,atomW)}
 function coreBlock(){let off=T.length,raw=[];for(let j=0;j<4;j++)raw.push(...ATOM.map(t=>t.map(v=>v+6*j)));let W=[];for(let a of atomW)for(let b of atomW)for(let c of atomW)for(let d of atomW){let w=a|(b<<6n)|(c<<12n)|(d<<18n);
 if((w&bit(1))||(w&bit(20)))continue;let good=true;for(let j=0;j<3;j++)if(par(w&(bit(6*j+2)^bit(6*(j+1)+1)))!==1)good=false;if(good){ok(own(raw,w,new Set()));W.push(w)}}ok(W.length===4);
 block(raw,W);guards.push([bit(off+1),0],[bit(off+20),0]);for(let j=0;j<3;j++)guards.push([bit(off+6*j+2)^bit(off+6*(j+1)+1),1]);return [off,off+6,off+12]}
 block(BI,words(BI,shared),true);block(BE,words(BE,shared),true);
 for(let t=0;t<2;t++){let C=coreBlock(),A=[],P=[];core.push(C);for(let i=0;i<k;i++){A.push(atom());P.push(atom());guards.push([bit(P[i])^bit(A[i])^bit(i?P[i-1]:C[0]),0])}side.push({A,P})}
 for(let j=0;j<3;j++)guards.push([bit(core[0][j])^bit(core[1][j]),(yes?6:7)>>j&1]);
 for(let i=0;i<k;i++)guards.push([bit(side[0].A[i])^bit(side[1].A[i]),i%3===1?1:0]);
 let M=[],rhs=0n;
 for(let v of shared){let r=0n;T.forEach((t,i)=>{if(t.includes(v))r|=bit(i)});M.push(r);rhs|=bit(M.length-1)}
 // Core internal guards already exact in group tables; remove these rows only after checking all rows of that group.
 for(let [r,b] of guards){let incident=groups.filter(g=>g.W.some(w=>par(w&r))||((bit(g.len)-1n)<<BigInt(g.offset))&r);if(incident.length===1&&incident[0].W.every(w=>par(w&r)===b))continue;M.push(r);if(b)rhs|=bit(M.length-1)}
 let G=groups.map(g=>g.W.map(w=>({w,z:image(M,w)})));let sizes=[0,0,0];for(let c of owners.values())sizes[c]++;ok(sizes.every(v=>v===sizes[0]));ok(new Set(T.map(t=>t.join(","))).size===T.length);
 const serial=JSON.stringify({T,guards:guards.map(([a,b])=>[a.toString(16),b])});let hash=2166136261;for(let i=0;i<serial.length;i++)hash=Math.imul(hash^serial.charCodeAt(i),16777619)>>>0;
 return {T,groups,G,guards,M,rhs,core,side,N:serial.length*8,hash:hash.toString(16)}
}
function verify(I,w){ok(own(I.T,w,new Set()),"native exact cover");ok(I.guards.every(([r,b])=>par(r&w)===b),"native guard")}
function reference(I){let [L,E]=I.core;for(let x of I.groups[2].W){for(let y of I.groups[3+2*I.side[0].A.length].W){if(!L.every((p,j)=>par((x|y)&(bit(p)^bit(E[j])))===Number(!!(I.rhs&bit(4+2*I.side[0].A.length+j)))))continue;return true}}return false}
function independentCore(I,yes){let l=I.groups[2],e=I.groups[3+2*I.side[0].A.length],cross=I.guards.slice(-(I.side[0].A.length+3),-I.side[0].A.length||undefined);let found=false;for(let x of l.W)for(let y of e.W)if(cross.every(([r,b])=>par(r&(x|y))===b))found=true;ok(found===yes);return found}
let cases=[];for(let k of [1,2,4,8,16,32,64])for(let yes of [false,true]){let I=build(k,yes),cl=close(I.G,I.rhs);ok(cl.R!==null);ok(cl.deleted===0);let A=solve(cl.R,I.rhs,256,"none"),B=solve(cl.R,I.rhs,256,"raw"),C=independentCore(I,yes),D=solve(cl.R,I.rhs,256,"projected");
 ok(B.rank===0);ok(D.rank===3*k);ok(D.answer===(yes?"YES":"NO"));if(A.answer!=="UNKNOWN")ok(A.answer===D.answer);if(B.answer!=="UNKNOWN")ok(B.answer===D.answer);if(D.w)verify(I,D.w.reduce((w,x)=>w|x.w,0n));let after=close(cl.R,I.rhs);ok(after.deleted===0);
 cases.push({k,yes,triples:I.T.length,encodedBits:I.N,fingerprint:I.hash,rawRows:I.M.length,removedRank:D.rank,residualRows:I.M.length-D.rank,closureDeleted:cl.deleted,A:{answer:A.answer,peak:A.peak,trials:A.trials},B:{answer:B.answer,rank:B.rank,peak:B.peak,trials:B.trials},C:{answer:C?"YES":"NO",method:"independent 16 core pairs + symbolic chain extension"},D:{answer:D.answer,rank:D.rank,peak:D.peak,trials:D.trials}})}
let random={yes:0,no:0};for(let t=0;t<400;t++){let g=2+rnd(4),r=1+rnd(6),G=[];for(let i=0;i<g;i++){let n=1+rnd(5),R=[];for(let j=0;j<n;j++)R.push({w:BigInt(j),z:BigInt(rnd(2**r))});G.push(R)}let target=BigInt(rnd(2**r));let ref=false;function go(i,z){if(i===G.length){if(z===target)ref=true;return}for(let x of G[i])go(i+1,z^x.z)}go(0,0n);let q=solve(G,target,256,"projected");ok(q.answer===(ref?"YES":"NO"));random[ref?"yes":"no"]++}
return{checks,seed,cases,random,limits:"Interleaved sequential copies; known verified partition, no blind chart search; no full grid or general recursive solver. A/B cap 256 syndrome states, D same cap. C direct core independent proof also solves all family."}
}
console.log(JSON.stringify(audit(),null,2));
