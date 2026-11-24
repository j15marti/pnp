function DR06(){
 const pop=x=>{let c=0;while(x){x&=x-1;c++}return c};
 const par=x=>pop(x)%2;
 const eq=(i,b)=>[1<<i,b];
 const metrics={rankCalls:0,rankXors:0,closureScans:0,forcedPins:0,edgeAttempts:0,referenceWords:0,checks:0,adapterChecks:0};
 const check=(x)=>{metrics.checks++;if(!x)throw Error("assertion "+metrics.checks)};
 function count(n,rows){metrics.rankCalls++;const B={};let r=0;for(let [a,b] of rows){while(a){const k=31-Math.clz32(a);if(!(k in B)){B[k]=[a,b];r++;break}a^=B[k][0];b^=B[k][1];metrics.rankXors++}if(!a&&b)return 0}return 2**(n-r)}
 function words(n,G){return Array.from({length:2**n},(_,x)=>x).filter(x=>G.every(([a,b])=>par(a&x)===b))}
 function bad(E,x){return E.every(([a,b])=>par(a&x)===b)}
 function legal(n,Es,G){const W=words(n,G);metrics.referenceWords+=W.length;return W.filter(x=>!Es.some(e=>bad(e,x)))}
 function closure(n,Es,G){G=G.slice();for(;;){metrics.closureScans++;const M=count(n,G);if(!M||Es.some(e=>count(n,G.concat(e))===M))return null;let changed=false;for(let i=0;i<n;i++){let fail=[0,1].map(b=>{let H=G.concat([eq(i,b)]),v=count(n,H);return !v||Es.some(e=>count(n,H.concat(e))===v)});if(fail.every(Boolean))return null;if(fail.some(Boolean)){const b=fail[0]?1:0;if(count(n,G.concat([eq(i,b)]))<M){G.push(eq(i,b));metrics.forcedPins++;changed=true;break}}}if(!changed)return G}}
 function forest(M,C,P){let p=C.map((_,i)=>i);function rt(i){while(p[i]!==i)i=p[i];return i}let E=[];for(let i=0;i<C.length;i++)for(let j=0;j<i;j++){E.push([P(i,j),i,j]);metrics.edgeAttempts++}E.sort((a,b)=>b[0]-a[0]||a[1]-b[1]||a[2]-b[2]);let sum=0,T=[];for(let [w,i,j] of E){let a=rt(i),b=rt(j);if(a!==b){p[a]=b;sum+=w;T.push([i,j])}}return {numerator:M*(M-C.reduce((a,b)=>a+b,0))+sum,denominator:M,tree:T}}
 function exact(n,Es,G,T=null){let M=count(n,G);if(!M)return {numerator:0,denominator:1,tree:[]};let C=Es.map(e=>count(n,G.concat(e)));let P=(i,j)=>M*count(n,G.concat(Es[i],Es[j]));if(!T)return forest(M,C,P);return {numerator:M*(M-C.reduce((a,b)=>a+b,0))+T.reduce((s,[i,j])=>s+P(i,j),0),denominator:M,tree:T}}
 function approx(n,Es,W){let M=W.length,d=Math.log2(M),A=Es.map(e=>W.map(x=>+bad(e,x))),C=A.map(a=>a.reduce((s,x)=>s+x,0));let D=A.map(a=>Array.from({length:d},(_,i)=>{let up=true,down=true;for(let z=0;z<M;z++)if(!(z&(1<<i))){let x=a[z],y=a[z|(1<<i)];if(x>y)up=false;if(x<y)down=false}return up&&down?0:up?1:down?-1:2}));let P=(i,j)=>D[i].every((a,k)=>{let b=D[j][k];return !a||!b||(a===b&&a!==2)})?C[i]*C[j]:M*Math.max(0,C[i]+C[j]-M);return {...forest(M,C,P),marginals:C}}
 function chart(n,a,b,p){let free=Array.from({length:n},(_,i)=>i).filter(i=>i!==p);return Array.from({length:2**(n-1)},(_,z)=>{let x=free.reduce((s,i,j)=>s|(((z>>j)&1)<<i),0);return x|((par(x&a)^b)<<p)})}
 const val=x=>x.numerator/x.denominator;
 function hull(W,n){if(!W.length)return -1;let basis={};for(let x of W){x^=W[0];while(x){let k=31-Math.clz32(x);if(basis[k])x^=basis[k];else{basis[k]=x;break}}}return Object.keys(basis).length}
 function cube(terms){return terms.map(([i,b])=>eq(i,b))}
 const n=6,terms=[[[0,1],[1,0],[5,0]],[[0,0],[3,1],[4,0]],[[2,1],[3,0],[5,0]],[[3,0],[4,0],[5,0]],[[1,1],[4,0],[5,1]],[[3,0],[4,1]],[[0,0],[4,1]]],Es=terms.map(cube),a=22;
 for(let x=0;x<64;x++)for(let e of Es){let wt=2*e.reduce((s,[a,b])=>s+(par(a&x)===b),0),H=2*e.length-2,W=4*e.length;check(bad(e,x)===(wt>H||wt>W-H));metrics.adapterChecks++}
 const G=closure(n,Es,[]);check(G!==null&&G.length===0);const A=approx(n,Es,words(n,G)),X=exact(n,Es,G),L=legal(n,Es,G);check(val(A)===2&&L.length===14&&hull(L,n)===n);const result={root:{approx:val(A),exact:val(X),models:L.length,hull:hull(L,n),marginals:A.marginals,approxTree:A.tree,exactTree:X.tree},guard: a,children:[]};
 for(let b=0;b<2;b++){const H=closure(n,Es,[[a,b]]);check(H!==null&&H.length===1);let Lb=legal(n,Es,H),xe=exact(n,Es,H),xf=exact(n,Es,H,X.tree),pivots=[];for(let p=0;p<n;p++)if(a&(1<<p)){let w=chart(n,a,b,p),ap=approx(n,Es,w);check(val(ap)<=0);pivots.push({p,credit:val(ap),marginals:ap.marginals,tree:ap.tree})}check(Lb.length===7&&hull(Lb,n)===n-1);result.children.push({b,models:Lb.length,hull:hull(Lb,n),exactOptimized:val(xe),exactFixed:val(xf),pivots})}
 check(result.children.reduce((s,x)=>s+x.exactFixed,0)===val(X));check(result.children.some(x=>x.exactFixed>0));
 function lift(n,E,G,T){let H=G;for(let i=0;i<n;i++){H=closure(n,E,H);check(H!==null);let parent=val(exact(n,E,H,T));check(parent>0);let children=[0,1].map(b=>H.concat([eq(i,b)]));let vals=children.map(h=>val(exact(n,E,h,T)));check(vals[0]+vals[1]===parent);let b=vals[0]>0?0:1;H=children[b]}let W=legal(n,E,H);check(W.length===1);return W[0]}
 result.witness=lift(n,Es,[[a,result.children.find(c=>c.exactFixed>0).b]],X.tree);
 let controls={sat:0,unsat:0,positive:0,unknown:0,witnesses:0,affineSplits:0};
 function control(n,E){let L=legal(n,E,[]),H=closure(n,E,[]);if(L.length)controls.sat++;else controls.unsat++;if(H===null){check(!L.length);return}let Z=exact(n,E,H);check(val(Z)<=L.length);if(val(Z)>0){check(L.length>0);lift(n,E,H,Z.tree);controls.witnesses++;controls.positive++}else controls.unknown++;
 for(let a=1;a<2**n;a++){let sum=0;for(let b=0;b<2;b++){let K=H.concat([[a,b]]),c=exact(n,E,K,Z.tree),l=legal(n,E,K);check(val(c)<=l.length);sum+=val(c)}check(sum===val(Z));controls.affineSplits++}}
 const all=Array.from({length:8},(_,x)=>cube(Array.from({length:3},(_,i)=>[i,(x>>i)&1])));
 for(let m=0;m<256;m++)control(3,all.filter((_,i)=>m&(1<<i)));
 const lines=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],F=lines.flatMap(l=>[0,1].map(b=>cube(l.map(i=>[i,b]))));control(7,F);for(let i=0;i<F.length;i++)control(7,F.filter((_,j)=>i!==j));
 // Exact axis-aligned subcube partition cardinality controls. Enumerate free-coordinate sets and verify every cube inside each guard pins all active columns.
 let partition=[];for(let n=2;n<=7;n++){let a=(1<<n)-1,G=[[a,0]],W=words(n,G);let maxFree=0;for(let x of W)for(let free=0;free<2**n;free++){let C=Array.from({length:2**n},(_,y)=>y).filter(y=>(y&~free)===(x&~free));if(C.every(y=>par(a&y)===0))maxFree=Math.max(maxFree,pop(free))}check(maxFree===0);partition.push({n,guardWords:W.length,minimumSubcubes:W.length})}
 return {result,controls,partition,metrics};
}
console.log(JSON.stringify(DR06(),null,2));
