function run(){
const unit=i=>1n<<BigInt(i), parity=x=>{let p=0;while(x){x&=x-1n;p^=1;}return p;}, dot=(x,y)=>parity(x&y);
function basis(rows){let p=new Map();for(let a of rows){while(a){let k=a.toString(2).length-1;if(p.has(k))a^=p.get(k);else{p.set(k,a);break;}}}return [...p.values()];}
const rank=r=>basis(r).length;
function restrict(B,f){let p=B.find(x=>dot(x,f));return p===undefined?B:B.filter(x=>x!==p).map(x=>dot(x,f)?x^p:x);}
function perp(B,n){let V=Array.from({length:n},(_,i)=>unit(i));for(let b of B)V=restrict(V,b);return V;}
function meet(A,B,n){return perp([...perp(A,n),...perp(B,n)],n);}
let checks=0;function check(x){checks++;if(!x)throw Error("assertion "+checks);}
function common(U,n){let V=Array.from({length:n},(_,i)=>unit(i)),out=[];while(V.length){let I=V,S=[];for(let X of U){let T=meet(I,X,n);if(T.length)I=T;else S.push(...X);}let v=I[0],f=perp(S,n).find(x=>dot(x,v));if(f===undefined)return null;out.push(v);V=restrict(V,f);U=U.map(X=>restrict(X,f));}return out;}
let seed=20261124;function rnd(k){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%k;}
let graphs=0,subsets=0,compatible=0,opposite=0,paddedGraphs=0;
function graph(n,E,pad){let m=n+E.length,U=Array.from({length:m},()=>[]);E.forEach(([u,v],i)=>{let a=unit(2*i),b=unit(2*i+1);U[u].push(a);U[v].push(b);U[n+i].push(a^b);});if(pad)U.forEach((X,i)=>X.push(unit(2*E.length+i)));let N=2*E.length+(pad?m:0),best=m;for(let mask=0;mask<2**m;mask++){let K=U.filter((_,i)=>!(mask&(1<<i)));let expected=E.every(([u,v],i)=>mask&((1<<u)|(1<<v)|(1<<(n+i))));let B=common(K,N);check(!!B===expected);subsets++;if(B){compatible++;best=Math.min(best,parityCount(mask));}else opposite++;}let vc=n;for(let mask=0;mask<2**n;mask++)if(E.every(([u,v])=>mask&((1<<u)|(1<<v))))vc=Math.min(vc,parityCount(mask));check(vc===best);graphs++;if(pad)paddedGraphs++;}
function parityCount(x){let c=0;while(x){x&=x-1;c++;}return c;}
for(let n of [3,4]){let P=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)P.push([i,j]);let masks=n===3?Array.from({length:8},(_,i)=>i):[1,7,11,21,42,63];for(let mask of masks){let E=P.filter((_,i)=>mask&(1<<i));graph(n,E,false);if(E.length&&Array.from({length:n},(_,i)=>E.some(e=>e.includes(i))).every(Boolean))graph(n,E,true);}}
function ok(x,F){return F.every(E=>!E.every(([a,b])=>dot(x,a)===b));}
function cons(G,n){return rank(G.map(([a,b])=>a+(b?unit(n):0n)))===rank(G.map(([a])=>a));}
let scans=0,pins=0,branches=0,sat=0,unsat=0,rootContradictions=0,witnesses=0,assignments=0;
function close(F,G,n){if(!cons(G,n))return null;while(true){let g=rank(G.map(x=>x[0])),changed=false;for(let E of F){scans++;let H=G.concat(E);if(!cons(H,n))continue;let r=rank(H.map(x=>x[0]))-g;if(r===0)return null;if(r===1){let [a,b]=E.find(([a])=>rank([...G.map(x=>x[0]),a])>g);G=G.concat([[a,1-b]]);pins++;changed=true;break;}}if(!changed)return G;}}
function solve(F,ordinary,k,n){let G=close(F,[],n);if(!G){rootContradictions++;return null;}let mask=unit(k)-1n;for(let z=0n;z<unit(k);z++){branches++;let branch=close(F,G.concat(Array.from({length:k},(_,i)=>[unit(i),dot(z,unit(i))])),n);if(!branch)continue;if(!ok(z,F.slice(ordinary)))continue;for(let q=0n;q<unit(n-k);q++){let x=(q<<BigInt(k))|z;assignments++;if(ok(x,F.slice(0,ordinary))){check(ok(x,F));check(branch.every(([a,b])=>dot(x,a)===b));return x;}}}return null;}
for(let i=0;i<180;i++){let n=3+rnd(5),k=1+rnd(Math.min(n,4)),m=1+rnd(15),F=[];for(let j=0;j<m;j++){let rows=[];for(let a=0;a<n;a++)if(rnd(5)<2)rows.push([unit(a),rnd(2)]);if(!rows.length)rows.push([unit(rnd(n)),rnd(2)]);F.push(rows);}for(let j=0;j<1+rnd(4);j++){let rows=[];for(let a=0;a<1+rnd(k);a++)rows.push([BigInt(1+rnd(2**k-1)),rnd(2)]);F.push(rows);}let expected=false;for(let x=0n;x<unit(n);x++)if(ok(x,F)){expected=true;break;}let out=solve(F,m,k,n);check((out!==null)===expected);if(out!==null){sat++;witnesses++;check(ok(out,F));}else unsat++;}
return {seed:20261124,graphs,subsets,compatible,incompatible:opposite,paddedGraphs,sat,unsat,witnesses,rootContradictions,scans,pins,branches,assignments,checks,notes:"S17 recognizer executed on all tested graph deletion sets; conditional CNF terminal used exhaustive backend, not Szeider. Local affine closure executed. No strict physical compiler or full portfolio."};
}
console.log(JSON.stringify(run(),null,2));
