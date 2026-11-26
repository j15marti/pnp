function audit(){
 let checks=0;const ok=(b,m)=>{checks++;if(!b)throw Error(m||"check "+checks)};
 const bit=i=>1n<<BigInt(i),par=x=>{let a=0;while(x){x&=x-1n;a^=1}return a},hi=x=>x.toString(2).length-1,ids=x=>{let a=[];while(x){let b=x&-x;a.push(hi(b));x^=b}return a};
 function basis(rows){let B=new Map;for(let [a,b] of rows){while(a&&B.has(hi(a))){let r=B.get(hi(a));a^=r[0];b^=r[1]}if(a)B.set(hi(a),[a,b]);else if(b)return null}return B}
 function rref(B){let A=[...B.keys()].sort((a,b)=>a-b);for(let i=0;i<A.length;i++)for(let j=i+1;j<A.length;j++){let r=B.get(A[j]),s=B.get(A[i]);if(r[0]&bit(A[i]))B.set(A[j],[r[0]^s[0],r[1]^s[1]])}return B}
 const rank=rows=>basis(rows.map(x=>[x,0])).size, sat=(R,w)=>R.every(([a,b])=>par(a&w)===b);
 function kernel(R,n){let B=rref(basis(R.map(x=>[x,0]))),D=[];for(let i=0;i<n;i++)if(!B.has(i)){let d=bit(i);for(let [j,[a]] of B)if(a&bit(i))d|=bit(j);D.push(d)}return D}
 function rows(T){let O=new Map;for(let i=0;i<T.length;i++)for(let v of T[i])O.set(v,(O.get(v)||0n)|bit(i));return O}
 function exact(T,w,boundary=false){let m=0;for(let [v,a] of rows(T)){let t=w&a;if(t&&(t&(t-1n)))return null;if(boundary&&v<4){if(t)m|=1<<v}else if(!t)return null}return m}
 function nativeWords(T,boundary=false){let out=[];for(let w=0n;w<bit(T.length);w++){let m=exact(T,w,boundary);if(m!==null)out.push([w,m])}return out}
 const ATOM=[[0,2,4],[0,2,5],[0,3,5],[1,2,4],[1,3,4],[1,3,5]],B_I=[[0,7,8],[6,2,3],[6,7,8],[1,10,11],[9,2,3],[9,10,11]],B_E=[[0,4,3],[0,4,5],[1,2,5],[1,4,5]];
 const atomWords=nativeWords(ATOM).map(x=>x[0]);ok(atomWords.length===3);
 function side(k,left,hostile){let T=(left?B_I:B_E).map(x=>x.slice()),C=new Map([[0,0],[1,0],[2,1],[3,2]]),groups=[{a:0,b:T.length,boundary:true}],pure=[],obs=[],off=[];
 for(let t of T)for(let j=0;j<3;j++)C.set(t[j],j);
 let nxt=left?12:6; // caller renames private owners on exterior before gluing
 function add(){let o=T.length;let p=nxt;nxt+=6;for(let t of ATOM){let tt=t.map(x=>x+p);T.push(tt);tt.forEach((v,j)=>C.set(v,j))}return o}
 let start=T.length;
 for(let i=0;i<4;i++)off.push(add());
 pure.push([bit(off[0]+1),0],[bit(off[3]+2),0]);
 for(let i=0;i<3;i++)pure.push([bit(off[i]+2)^bit(off[i+1]+1),1]);
 obs.push(...off.slice(0,3).map(bit));groups.push({a:start,b:T.length,core:true,off:off.slice()});
 for(let i=0;i<k;i++){let a=add(),free=!hostile&&(left?i%2===0:i%2===1);if(free)pure.push([bit(a+2),0]);obs.push(bit(a));groups.push({a,b:T.length,atom:true,free})}
 return {T,C,pure,obs,groups}
 }
 function closure(T,A){let O=[...rows(T).values()],P=new Map,rounds=0;
 function pin(i,b){if(P.has(i))return P.get(i)===b?0:-1;P.set(i,b);return 1}
 for(;;){rounds++;let change=0;for(let a of O){let ar=ids(a),one=ar.filter(i=>P.get(i)===1),live=ar.filter(i=>!P.has(i));if(one.length>1||(!one.length&&!live.length))return null;
 if(one.length||live.length===1)for(let i of live){let t=pin(i,one.length?0:1);if(t<0)return null;change+=t}}
 let B=basis(A.concat(O.map(a=>[a,1]),[...P].map(([i,b])=>[bit(i),b])));if(!B)return null;rref(B);
 for(let [i,[a,b]] of B)if(a===bit(i)){let t=pin(i,b);if(t<0)return null;change+=t}
 if(!change)return {P,rounds}
 }}
 function shifts(S,P){let R=S.pure.map(x=>x[0]);for(let i of P.keys())R.push(bit(i));
 for(let [v,a] of rows(S.T)){let ar=ids(a).filter(i=>!P.has(i));if(v>=4&&!ids(a).some(i=>P.get(i)===1)&&ar.length===2)R.push(bit(ar[0])^bit(ar[1]));else for(let i of ar)R.push(bit(i))}
 return kernel(R,S.T.length)}
 function syn(obs,w){let x=0n;for(let i=0;i<obs.length;i++)if(par(obs[i]&w))x|=bit(i);return x}
 function quotient(L,E,D,F){let B=new Map;function add(z,d){while(z&&B.has(hi(z))){let a=B.get(hi(z));z^=a[0];d^=a[1]}if(z)B.set(hi(z),[z,d])}
 for(let d of D)add(syn(L.obs,d),d);for(let d of F)add(syn(E.obs,d),d<<BigInt(L.T.length));
 let order=[...B.keys()].sort((a,b)=>b-a);
 function reduce(z){let d=0n;for(let i of order)if(z&bit(i)){let a=B.get(i);z^=a[0];d^=a[1]}return [z,d]}
 return {reduce,r:L.obs.length-B.size,dim:B.size}}
 function groupWords(S,g,P){let out=[];if(g.core){for(let a of atomWords)for(let b of atomWords)for(let c of atomWords)for(let d of atomWords){let w=[a,b,c,d].reduce((s,x,i)=>s|(x<<BigInt(g.off[i])),0n);out.push([w,0])}}
 else if(g.atom)out=atomWords.map(w=>[w<<BigInt(g.a),0]);
 else out=nativeWords(S.T.slice(g.a,g.b),true).map(([w,m])=>[w<<BigInt(g.a),m]);
 let mask=(bit(g.b)-1n)^(bit(g.a)-1n),R=S.pure.filter(([a])=>a&mask);
 ok(R.every(([a])=>(a&mask)===a),"pure ownership");
 return out.filter(([w])=>sat(R,w)&&[...P].every(([i,b])=>!(mask&bit(i))||+(!!(w&bit(i)))===b))}
 function support(S,P,Q,shift=0n){let out=new Map([["0:0",[0,0n,0n]]]),peak=1;
 for(let g of S.groups){let W=groupWords(S,g,P),V=new Map;ok(W.length>0);
 for(let [h,z,w] of out.values())for(let [v,m] of W){let s=Q.reduce(z^syn(S.obs,v))[0],t=h|m;V.set(`${t}:${s}`,[t,s,w|v])}
 out=V;peak=Math.max(peak,out.size)}
 let ret=new Map;for(let [h,z,w] of out.values()){ok(exact(S.T,w,true)===h);ok(sat(S.pure,w));ok([...P].every(([i,b])=>+(!!(w&bit(i)))===b));let z1=Q.reduce(z^shift)[0];ret.set(`${h}:${z1}`,[h,z1,w])}return {ret,peak}}
 function verify(T,A,w){ok(exact(T,w)===0,"full cover");ok(sat(A,w),"full guards")}
 let scales=[];
 function run(k,hostile=false){
 let L=side(k,true,hostile),E=side(k,false,hostile),n=L.T.length,sh=BigInt(n),m=E.T.length,all=L.T.concat(E.T.map(t=>t.map(v=>v<4?v:v+1000000)));
 ok(new Set(all.map(t=>t.join(","))).size===all.length);let cols=new Map;for(let t of all)t.forEach((v,j)=>{ok(!cols.has(v)||cols.get(v)===j);cols.set(v,j)});let counts=[0,0,0];for(let c of cols.values())counts[c]++;ok(counts.every(c=>c===counts[0]));
 let pure=L.pure.concat(E.pure.map(([a,b])=>[a<<sh,b])),rec={k,triples:n+m,rawRank:k+3};
 for(let yes of [false,true]){
  let rhs=yes?6n:7n;for(let i=3;i<k+3;i++)if(i%3===1)rhs|=bit(i);
  let cross=L.obs.map((a,i)=>[a^(E.obs[i]<<sh),+(!!(rhs&bit(i)))]),A=pure.concat(cross);
  let C=closure(all,A);ok(C!==null,"closure should not reject");
  let LP=new Map([...C.P].filter(([i])=>i<n)),EP=new Map([...C.P].filter(([i])=>i>=n).map(([i,b])=>[i-n,b]));
  let D=shifts(L,LP),F=shifts(E,EP),Q=quotient(L,E,D,F);
  let R=pure.concat([...C.P].map(([i,b])=>[bit(i),b]));ok(rank(A.concat([...C.P].map(([i,b])=>[bit(i),b])).map(x=>x[0]))-rank(R.map(x=>x[0]))===k+3);
  ok(Q.r===(hostile?k+3:3),"effective rank");ok(D.length===(hostile?0:Math.ceil(k/2))&&F.length===(hostile?0:Math.floor(k/2)));
  // On hostile examples use factor separation instead of exponential support DP.
  if(hostile){ok(Q.dim===0);for(let S of [L,E])for(let g of S.groups.filter(g=>g.atom))ok(groupWords(S,g,new Map()).length===3);rec[yes?"yes":"no"]={closurePins:C.P.size,effective:Q.r,productSupportLowerBound:`2^${k}`,decisionByCore:yes?"YES":"NO"};continue}
  let U=support(L,LP,Q),V=support(E,EP,Q,rhs),common=0,lifts=0;
  for(let [h,z,w] of U.ret.values()){let x=V.ret.get(`${15^h}:${z}`);if(!x)continue;common++;let v=x[2],delta=syn(L.obs,w)^syn(E.obs,v)^rhs,[rr,d]=Q.reduce(delta);ok(!rr);let W=(w|(v<<sh))^d;verify(all,A,W);ok([...C.P].every(([i,b])=>+(!!(W&bit(i)))===b));lifts++}
  ok(!!common===yes,"joint decision");ok(U.ret.size===12&&V.ret.size===12);ok(common===(yes?6:0));
  rec[yes?"yes":"no"]={closurePins:C.P.size,effective:Q.r,leftSwitches:D.length,rightSwitches:F.length,oneSidedEffective:k+3-rank(D.map(d=>syn(L.obs,d))),leftPatterns:U.ret.size,rightPatterns:V.ret.size,common,lifts,peak:Math.max(U.peak,V.peak)}
  // independent exhaustive exact cross support for the small source sizes
  if(k<=4){let product=(S,P)=>{let W=[[0n,0]];for(let g of S.groups){let V=groupWords(S,g,P);W=W.flatMap(([w,h])=>V.map(([v,m])=>[w|v,h|m]))}return W};
  let a=product(L,LP),b=product(E,EP),witness=0;for(let [w,h] of a)for(let [v,g] of b)if((h^g)===15&&sat(A,w|(v<<sh))){witness++;verify(all,A,w|(v<<sh))}ok(!!witness===yes);rec[yes?"yes":"no"].referenceWitnesses=witness}
 }
 return rec
 }
 for(let k of [0,2,4,8,16,32,64,128])scales.push(run(k));
 let hostile=[4,16,64].map(k=>run(k,true));
 // independent brute test of exact stabilizers and quotient (all nonempty 3-bit tables)
 const rels=[];for(let mask=1;mask<256;mask++){let W=Array.from({length:8},(_,i)=>i).filter(i=>mask>>i&1),H=W.map(x=>x^W[0]).filter(d=>W.every(x=>W.includes(x^d)));ok(H.every(a=>H.every(b=>H.includes(a^b))));rels.push({W,H})}
 let seed=261126;function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)%n}
 for(let i=0;i<1500;i++){let A=rels[rnd(255)],B=rels[rnd(255)],b=rnd(8),H=[...new Set(A.H.flatMap(a=>B.H.map(c=>a^c)))],rep=x=>Math.min(...H.map(d=>d^x));let exact=A.W.some(x=>B.W.includes(x^b)),quot=A.W.some(x=>B.W.some(y=>rep(x)===rep(y^b)));ok(exact===quot);if(quot)for(let x of A.W)for(let y of B.W)if(rep(x)===rep(y^b)){let a=A.H.find(a=>B.H.includes(a^x^y^b));ok(a!==undefined);ok(A.W.includes(x^a)&&B.W.includes(y^(a^x^y^b)))}}
 // FibonacciAi counterexample: all four length-3 clauses with negative x; x=0 always SAT, x=1 impossible.
 let formula=Array.from({length:4},(_,i)=>[[-1,0],[i&1?1:-1,1],[i&2?1:-1,2]]);
 let ev=(a)=>formula.every(c=>c.some(([s,j])=>!!(a>>j&1)===(s>0)));
 ok(Array.from({length:8},(_,i)=>i).filter(ev).join(",")==="0,2,4,6");ok(formula.every(c=>c.length===3));
 // integer recurrence with effective, input-dependent rank
 let recurrence=0;for(let c=5;c<=10;c++)for(let n=112;n<=2000;n+=17)for(let a=56;a<=n/2;a+=19)for(let r=0;r<=10;r++){let b=20+36*2**r;if(2*b>a)continue;let nn=BigInt(n),aa=BigInt(a),p=BigInt(c),q=BigInt(2**r);if(16n*q*aa**(p-1n)>nn**(p-1n))continue;ok(6n*q*aa**p+(nn-aa+BigInt(b))**p<=nn**p-1n);recurrence++}
 return {checks,scales,hostile,randomQuotientCases:1500,stabilizerTables:255,recurrence,seed:261126};
}
console.log(JSON.stringify(audit(),null,2));
