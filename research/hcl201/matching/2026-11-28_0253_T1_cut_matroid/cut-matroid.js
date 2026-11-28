
const assert=(x,m)=>{if(!x)throw Error(m)};
function flow(H,q,D=[],force=-1){
 const d=H.length,s=d+q,t=s+1,n=t+1,B=d+q+1,A=Array.from({length:n},()=>[]),arcs=[];let scans=0;
 const del=new Set(D);
 function add(u,v,c){let a={v,c,rev:A[v].length},b={v:u,c:0,rev:A[u].length};A[u].push(a);A[v].push(b);arcs.push([u,v,c,a])}
 for(let i=0;i<d;i++){add(s,i,i===force?B:1);for(let j of H[i])add(i,d+j,B)}
 for(let j=0;j<q;j++)add(d+j,t,del.has(j)?0:1);
 let val=0,S;
 while(true){let prev=Array(n).fill(null),Q=[s];prev[s]=[-1,-1];for(let l=0;l<Q.length;l++){let u=Q[l];for(let a=0;a<A[u].length;a++){scans++;let e=A[u][a];if(e.c>0&&prev[e.v]===null){prev[e.v]=[u,a];Q.push(e.v)}}}if(!prev[t]){S=Q;break}let b=B;for(let v=t;v!==s;){let [u,a]=prev[v];b=Math.min(b,A[u][a].c);v=u}for(let v=t;v!==s;){let [u,a]=prev[v],e=A[u][a];e.c-=b;A[v][e.rev].c+=b;v=u}val+=b}
 const cut=new Set(S),balances=Array(n).fill(0),certificate=arcs.map(([u,v,c,a])=>[u,v,c,c-a.c]);let cap=0;
 for(let [u,v,c,f] of certificate){assert(f>=0&&f<=c,"capacity");balances[u]-=f;balances[v]+=f;if(cut.has(u)&&!cut.has(v))cap+=c}
 assert(cap===val&&balances[s]===-val&&balances[t]===val&&balances.every((x,i)=>i===s||i===t||x===0),"dual");
 let L=S.filter(i=>i<d),N=sort(L.flatMap(i=>H[i])).filter(j=>!del.has(j));if(force>=0){assert(L.includes(force),"forced");assert(val===d-L.length+N.length,"Hall cut")}
 return {val,scans,cut:S,L,N,arcs:certificate}
}
function robust(H,q){let C=H.map((_,i)=>flow(H,q,[],i)),m=Math.min(...C.map(c=>c.val-H.length));return {surplus:m,robust:m===q-H.length,scans:C.reduce((s,c)=>s+c.scans,0),C}}
function bruteSurplus(H){let m=Infinity;for(let w=1;w<2**H.length;w++){let S=H.filter((_,i)=>(w>>i)&1);m=Math.min(m,sort(S.flat()).length-S.length)}return m}
function indep(H,q,D){return flow(H,q,D).val===H.length}
function recognize(H,q){let k=q-H.length,calls=0,scans=0,cert=[];function test(D){let f=flow(H,q,D);calls++;scans+=f.scans;cert.push({D,val:f.val,cut:f.cut,arcs:f.arcs});return f.val===H.length}
 if(!test([]))return {status:"BASE-NO",calls,scans,cert};
 let loops=[],V=[];for(let j=0;j<q;j++)(test([j])?V:loops).push(j);
 let P=new Map(V.map(v=>[v,v]));function find(v){while(P.get(v)!==v)v=P.get(v);return v}
 let dep=[];for(let a=0;a<V.length;a++)for(let b=a+1;b<V.length;b++)if(!test([V[a],V[b]])){dep.push([V[a],V[b]]);P.set(find(V[a]),find(V[b]))}
 let C=new Map();for(let v of V){let r=find(v);if(!C.has(r))C.set(r,[]);C.get(r).push(v)}let classes=[...C.values()];let depSet=new Set(dep.map(x=>x.join(",")));assert(classes.every(c=>c.every((v,i)=>c.slice(i+1).every(w=>depSet.has([v,w].join(","))))),"parallel");
 return {status:classes.length===k?"EXACT-PAIR-QUOTIENT":"HIGHER-ORDER-NEEDED",k,loops,classes,calls,scans,cert}
}
function approximate(R,D){let s=new Set(D);return !R.loops.some(v=>s.has(v))&&D.length<=R.k&&R.classes.every(c=>c.filter(v=>s.has(v)).length<=1)}
function exhaustive(H,q){let r=recognize(H,q),g=robust(H,q),bad=[];assert(g.surplus===bruteSurplus(H),"surplus");if(r.status!=="BASE-NO"){for(let w=0;w<2**q;w++){let D=Array.from({length:q},(_,j)=>j).filter(j=>(w>>j)&1),exact=indep(H,q,D),rel=approximate(r,D);assert(!exact||rel,"invalid relaxation");if(rel&&!exact)bad.push(D);if(r.status==="EXACT-PAIR-QUOTIENT")assert(rel===exact,"bad quotient");if(g.robust)assert(exact===(D.length<=r.k),"robust failure")}}return {r,g,bad}}
const sat=(l,w)=>((w>>(Math.abs(l)-1))&1)===Number(l>0);
function blocked(P,w){return P.map((a,i)=>a.every(l=>sat(l,w))?i:-1).filter(i=>i>=0)}
function pairPacket(words,n){let m=[];for(let i=0;i<n;i++)for(let j=i;j<n;j++){let v=[0,0,0,0];for(let w of words)v[((w>>i)&1)+2*((w>>j)&1)]++;m.push([i,j,v,words.length])}return m}
function parityRegion(par){let H=[],P=[];for(let w=0;w<8;w++)if((Number(Boolean(w&1))+Number(Boolean(w&2))+Number(Boolean(w&4)))%2!==par){let ls=[1,2,3].map((x,i)=>((w>>i)&1)?x:-x);H.push([P.length,P.length+1]);P.push(ls.slice(0,2),ls.slice(2))}return {H,P,q:P.length}}
function parityTest(){let L=parityRegion(0),R=parityRegion(1),Y=parityRegion(0),runs=[];for(let w=0;w<8;w++){let row={w};for(let [name,G] of [["L",L],["R",R],["Y",Y]]){let D=blocked(G.P,w),f=flow(G.H,G.q,D);row[name]={D,feasible:f.val===G.H.length,proof:f}}runs.push(row)}let A=runs.filter(x=>x.L.feasible).map(x=>x.w),B=runs.filter(x=>x.R.feasible).map(x=>x.w),C=runs.filter(x=>x.Y.feasible).map(x=>x.w);let a=pairPacket(A,3),b=pairPacket(B,3);assert(J(a)===J(b)&&A.every(x=>!B.includes(x))&&J(A)===J(C),"pair gap");return {L,R,Y,runs,A,B,C,pair:a,LP:"exact regional support distributions with denominator4, identical all unary and pair projections"}
}
function test(){let counts={graphs:0,baseNO:0,exact:0,high:0,robust:0,falseAccept:0},examples=[];function go(H,q){let x=exhaustive(H,q);counts.graphs++;if(x.r.status==="BASE-NO")counts.baseNO++;else if(x.r.status==="EXACT-PAIR-QUOTIENT")counts.exact++;else counts.high++;counts.robust+=Number(x.g.robust);counts.falseAccept+=x.bad.length}
 for(let w=0;w<256;w++)go(Array.from({length:2},(_,i)=>Array.from({length:4},(_,j)=>j).filter(j=>(w>>(4*i+j))&1)),4);
 let seed=9317;for(let i=0;i<100;i++){let H=Array.from({length:3},()=>Array.from({length:5},(_,j)=>j).filter(()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>29)>=3}));go(H,5)}
 let H=[[0,1],[2,3]],q=4,P=[[1,2],[1,3],[2,-3],[-1,3]],r=recognize(H,q),g=robust(H,q),rows=[];for(let w=0;w<8;w++){let D=blocked(P,w),f=flow(H,q,D);assert(approximate(r,D)===(f.val===H.length),"overlap");rows.push({w,D,match:f.val,flow:f})}let high=exhaustive([[0,1,2],[3,4]],5);
 let grow=[];for(let d of [4,8,16,32]){let H=Array.from({length:d},(_,i)=>[2*i,2*i+1]),q=2*d,r=recognize(H,q);assert(r.status==="EXACT-PAIR-QUOTIENT"&&r.classes.length===d,"growing");let A=Array.from({length:d},(_,i)=>2*i),B=A.slice(1).concat([0,1]);B=B.slice(0,d-2).concat([0,1]);assert(indep(H,q,A)&&!indep(H,q,B),"controls");grow.push({d,q,slack:d,classes:r.classes.length,calls:r.calls,scans:r.scans,yes:A,no:B})}
 return {counts,overlap:{H,q,P,r,g,rows},higher:{H:[[0,1,2],[3,4]],q:5,r:high.r,g:high.g,bad:high.bad},parity:parityTest(),grow}
}

// Load after pinned T1 check.js; call test().
