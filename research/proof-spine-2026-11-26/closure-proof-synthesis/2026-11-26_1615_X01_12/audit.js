function audit(){
let checks=0,probes=0,seed=261126;const ok=(v,m)=>{checks++;if(!v)throw Error(m||`check ${checks}`)};function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)%n}
const bit=i=>1n<<BigInt(i), xor=a=>a.reduce((s,x)=>s^x,0n), key=x=>x.toString(), uniq=a=>[...new Set(a)], has=(a,v)=>a.includes(v);
function basis(vs){let b=new Map();for(let j=0;j<vs.length;j++){let v=vs[j],c=bit(j);while(v){let i=v.toString(2).length-1;if(!b.has(i)){b.set(i,[v,c]);break}let [x,y]=b.get(i);v^=x;c^=y}}return b}
function reduce(v,b){let c=0n;for(let i of [...b.keys()].sort((a,b)=>b-a)){if(v&bit(i)){let [x,y]=b.get(i);v^=x;c^=y}}return[v,c]}
function transversal(U){let I=Array(U.length).fill(0n);while(true){let b=basis(I),queue=[],parent=new Map(),end=null;
 for(let i=0;i<I.length;i++)if(!I[i]){queue.push(i);parent.set(i,null)}
 for(let j=0;j<queue.length&&!end;j++){let i=queue[j];for(let v of U[i])if(v){probes++;let [w,c]=reduce(v,b);if(w){end=[i,v];break}
 for(let k=0;k<I.length;k++)if((c&bit(k))&&!parent.has(k)){parent.set(k,[i,v]);queue.push(k)}}}
 if(!end)return I;let [i,v]=end;while(true){I[i]=v;let p=parent.get(i);if(!p)break;[i,v]=p}ok(basis(I).size===I.filter(Boolean).length,"transversal")
 }}
function periods(S){return S.map(x=>x^S[0]).filter(d=>S.every(x=>has(S,x^d)))}
function affineClose(T,t){T=T.map(S=>S.slice());let deleted=0;for(;;){let change=false;for(let i=0;i<T.length;i++){if(!T[i].length)return{T,deleted,no:true};let O=T.filter((_,j)=>j!==i);if(O.some(x=>!x.length))return{T,deleted,no:true};let base=xor(O.map(S=>S[0])),b=basis(O.flatMap(S=>S.map(x=>x^S[0])));let D=T[i].filter(x=>reduce(t^x^base,b)[0]===0n);if(D.length<T[i].length){deleted+=T[i].length-D.length;T[i]=D;change=true}}if(!change)return{T,deleted,no:false}}}
function dp(T,t,cap=256){let S=new Map([[0n,[]]]),peak=1,work=0;for(let A of T){let Q=new Map();for(let [x,rows] of S)for(let y of A){work++;if(!Q.has(x^y))Q.set(x^y,[...rows,y]);if(Q.size>cap)return{answer:"UNKNOWN",peak:Q.size,work}}S=Q;peak=Math.max(peak,S.size)}return{answer:S.has(t)?"YES":"NO",rows:S.get(t),peak,work}}
function cert(F){let U=[],W=[];for(let M of F){let lists=[...M.values()];if(!lists.length||lists.some(S=>!S.length))return null;let dif=lists.map(S=>uniq(S.flatMap(x=>S.map(y=>x^y))).filter(Boolean));U.push(dif[0].filter(v=>dif.every(D=>has(D,v))));for(let S of lists)W.push(...S.map(x=>x^S[0]))}
 let b=basis(W),I=transversal(U);if(I.filter(Boolean).length!==b.size)return null;ok(I.every(v=>reduce(v,b)[0]===0n));return{I,b,basisRank:b.size}}
function lift(F,labels,target,C){let base=[],pairs=[];for(let i=0;i<F.length;i++){let S=F[i].get(labels[i]);if(!S)return null;let d=C.I[i];let a=d?S.find(x=>has(S,x^d)):S[0];ok(a!==undefined,"pair");base.push(a);pairs.push(d)}let [rem,c]=reduce(target^xor(base),basis(pairs));if(rem)return null;let words=base.map((x,i)=>x^((c&bit(i))?pairs[i]:0n));ok(xor(words)===target&&words.every((x,i)=>has(F[i].get(labels[i]),x)));return words}
const atom=[[0,2,4],[0,2,5],[0,3,5],[1,2,4],[1,3,4],[1,3,5]];
const covers=[];for(let m=0;m<64;m++){let cnt=Array(6).fill(0);for(let j=0;j<6;j++)if(m>>j&1)for(let v of atom[j])cnt[v]++;if(cnt.every(x=>x===1))covers.push(m)}
ok(covers.length===3);ok(covers.every(m=>[0,1,2].filter(j=>m>>j&1).length===1));
function source(n,no){let triples=[],rows=[],blocks=[],m=2*n+3;function addAtom(){let o=triples.length;for(let a of atom)triples.push(a.map(v=>v+o));return o}
 for(let i=0;i<n+2;i++){let a=addAtom(),b=addAtom();blocks.push({a,b,core:i>=n})}
 for(let i=0;i<n;i++){let {a,b}=blocks[i],prev=blocks[(i+n-1)%n];rows.push({ids:[a,b+1,prev.a+1],rhs:i%2});let c=blocks[n+i%2];rows.push({ids:[b,[c.a,c.a+1,c.b][Math.floor(i/2)%3]],rhs:0})}
 for(let j=0;j<3;j++){let p=blocks.slice(n).map(c=>[c.a,c.a+1,c.b][j]);rows.push({ids:p,rhs:no?1:+(j!==2)})}
 for(let c of blocks.slice(n))rows.push({ids:[c.a+2,c.b+2],rhs:1,local:true});
 return{n,triples,rows,blocks,m}}
function getTables(F){let map=F.triples.map(()=>0n),t=0n;for(let [i,r] of F.rows.filter(r=>!r.local).entries()){if(r.rhs)t|=bit(i);for(let j of r.ids)map[j]^=bit(i)}
 let raw=[],local=[];for(let c of F.blocks){let M=new Map(),ids=[];for(let a of covers)for(let b of covers){if(c.core&&((a>>2&1)^(b>>2&1))!==1)continue;let chosen=[];for(let j=0;j<6;j++){if(a>>j&1)chosen.push(c.a+j);if(b>>j&1)chosen.push(c.b+j)}let w=xor(chosen.map(j=>map[j]));if(!M.has(w))M.set(w,chosen);ids.push({w,chosen})}raw.push(M);local.push(ids)}return{raw,local,t}}
function verify(F,chosen){let s=new Set(chosen),counts=Array(F.triples.length).fill(0);for(let id of s){for(let v of F.triples[id])counts[v]++}ok(counts.every(x=>x===1),"owners");for(let r of F.rows)ok(r.ids.reduce((a,j)=>a^+s.has(j),0)===r.rhs,"guard")}
function direct(F,G){let {n}=F,E=Array.from({length:n},(_,i)=>bit(2*i)),P=Array.from({length:n},(_,i)=>bit(2*i+1)),fm=bit(2*n)|bit(2*n+1)|bit(2*n+2);for(let [a,ra] of G.raw[n])for(let [b,rb] of G.raw[n+1]){if(((a^b^G.t)&fm)!==0n)continue;let need=a^b^G.t,words=[];for(let i=0;i<n;i++){let w=(need&E[i])|(need&P[i]);ok(G.raw[i].has(w),"direct word");words.push(...G.raw[i].get(w))}verify(F,[...words,...ra,...rb]);return"YES"}return"NO"}
function run(n,no){let F=source(n,no),G=getTables(F),T=G.raw.map(M=>[...M.keys()]),init=affineClose(T,G.t);ok(!init.no&&init.deleted===0,"affine closure");
 const A=dp(T,G.t),periodRank=basis(T.flatMap(periods)).size;ok(periodRank===0,"raw periods");
 let U=T.map(S=>S.map(x=>x^S[0]).filter(Boolean)),I=transversal(U),b=basis(I);
 // Largest saturatable subset using raw dependency closure.
 let bad=new Set();U.forEach((S,i)=>{if(S.some(x=>reduce(x,b)[0]))bad.add(i)});for(;;){let q=bad.size;U.forEach((S,i)=>{if(S.some(x=>{let c=reduce(x,b)[1];return [...bad].some(j=>c&bit(j))}))bad.add(i)});if(q===bad.size)break}
 ok(bad.size===T.length,"raw Rado stalls");const B=dp(T,G.t),C=direct(F,G);
 let P=Array.from({length:n},(_,i)=>bit(2*i+1)),Em=xor(Array.from({length:n},(_,i)=>bit(2*i))),Fm=bit(2*n)|bit(2*n+1)|bit(2*n+2),fiber=T.slice(0,n).map((S,i)=>new Map([0,1].map(p=>[p,uniq(S.filter(x=>+(!!(x&P[i]))===p).map(x=>x&Em))])));
 let H=cert(fiber);ok(H&&H.basisRank===n);ok(fiber.every(M=>M.get(0).length===4&&M.get(1).length===3));let Q=T.map(S=>uniq(S.map(x=>x&~Em))),closure1=affineClose(Q,G.t&~Em);ok(!closure1.no&&closure1.deleted===0);let per=basis(Q.slice(0,n).flatMap(periods));ok(per.size===n);let red=Q.slice(n).map(S=>uniq(S.map(x=>reduce(x,per)[0]))),target=reduce(G.t&~Em,per)[0],closure2=affineClose(red,target);ok(!closure2.no&&closure2.deleted===0);let D=dp(red,target);ok(D.answer===C&&D.answer===(no?"NO":"YES"));
 if(D.answer==="YES"){let cs=D.rows.map((v,i)=>[...G.raw[n+i].keys()].find(x=>reduce(x&~Em,per)[0]===v));let need=G.t^xor(cs),labels=P.map(x=>+(!!(need&x))),words=lift(fiber,labels,need&Em,H);ok(words);let local=words.map((x,i)=>x^(labels[i]?P[i]:0n));verify(F,[...local.flatMap((v,i)=>G.raw[i].get(v)),...cs.flatMap((v,i)=>G.raw[n+i].get(v))])}
 let enc=JSON.stringify(F),hash=2166136261;for(let c of enc)hash=Math.imul(hash^c.charCodeAt(0),16777619)>>>0;
 return{n,no,triples:F.triples.length,encodedBits:enc.length*8,fingerprint:hash.toString(16),rawRank:basis(U.flat()).size,rawPeriodRank:periodRank,rawRadoCore:T.length-bad.size,protectedRank:H.basisRank,projectedPeriodRank:per.size,A:{answer:A.answer,peak:A.peak,work:A.work},B:{answer:B.answer,peak:B.peak,work:B.work},C,D:{answer:D.answer,peak:D.peak,work:D.work},deleted:init.deleted+closure1.deleted+closure2.deleted}
}
let native=[];for(let n of [4,8,16,32,64])for(let no of [false,true])native.push(run(n,no));
let random={tested:0,admitted:0,comparisons:0};for(let z=0;z<240;z++){let n=1+rnd(4),d=1+rnd(4),F=Array.from({length:n},()=>new Map([0,1].map(p=>[p,uniq(Array.from({length:1+rnd(5)},()=>BigInt(rnd(1<<d))))]))),C=cert(F);random.tested++;if(!C)continue;random.admitted++;for(let mask=0;mask<1<<n;mask++){let lab=Array.from({length:n},(_,i)=>mask>>i&1),S=[0n];for(let i=0;i<n;i++)S=uniq(S.flatMap(x=>F[i].get(lab[i]).map(y=>x^y)));for(let t=0;t<1<<d;t++){let w=lift(F,lab,BigInt(t),C);ok(!!w===S.includes(BigInt(t)),"reference");random.comparisons++}}}
let badFiber=[new Map([[0,[0n,1n]],[1,[0n]]])];ok(!cert(badFiber));ok(badFiber[0].get(1).every(v=>v!==1n)); // pooled fiber would incorrectly admit (p=1,e=1).
return{checks,transversalProbes:probes,native,random,seed:261126,cap:256,adversarial:"native single-atom protected pin destroys pooled symmetry"}
}
console.log(JSON.stringify(audit(),null,2));
