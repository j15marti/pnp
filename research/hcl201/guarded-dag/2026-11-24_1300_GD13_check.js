"use strict";
function experiment(){
 const L={calls:0,gaussInserts:0,xors:0,closureSweeps:0,forced:0,edgeTests:0,leafWords:0,joinPairs:0,rejectedPairs:0,mergedStates:0,peakTable:0,peakRetainedEntries:0,referenceWords:0,assertions:0};
 const hi=x=>x.toString(2).length-1, bit=i=>1n<<BigInt(i);
 function parity(x){let p=0;while(x){p^=1;x&=x-1n}return p}
 function add(B,a,c=0){L.gaussInserts++;while(a){let i=hi(a),v=B.get(i);if(!v){B.set(i,[a,c]);return true}a^=v[0];c^=v[1];L.xors++}return c===0}
 function reduce(B,a,c=0){for(const i of [...B.keys()].sort((a,b)=>b-a))if(a&bit(i)){const v=B.get(i);a^=v[0];c^=v[1];L.xors++}return [a,c]}
 function basis(rows){let B=new Map();for(const a of rows)add(B,a);return [...B.values()].map(v=>v[0])}
 function intersection(A,B){let D=new Map(),out=[];function push(a,t){while(a){let i=hi(a),v=D.get(i);if(!v){D.set(i,[a,t]);return}a^=v[0];t^=v[1];L.xors++}if(t)out.push(t)}for(let a of B)push(a,0n);for(let a of A)push(a,a);return basis(out)}
 function value(B,a){let [r,c]=reduce(B,a);if(r)throw Error("unobserved interface");return c}
 function witness(B){let x=0n;for(const i of [...B.keys()].sort((a,b)=>a-b)){const [a,c]=B.get(i);if((parity(a&x)^c))x|=bit(i)}return x}
 const e=(u,v,g=[])=>({u,v,g});
 function reaches(E,s,t){let S=new Set([s]);for(let change=true;change;){change=false;for(let a of E)if(S.has(a.u)&&!S.has(a.v)){S.add(a.v);change=true}}return S.has(t)}
 function reachset(E,s,rev=false){let S=new Set([s]);for(let change=true;change;){change=false;for(let a of E){let u=rev?a.v:a.u,v=rev?a.u:a.v;if(S.has(u)&&!S.has(v)){S.add(v);change=true}}}return S}
 function valid(E,x,s,t){return !reaches(E.filter(a=>a.g.every(([m,c])=>parity(m&x)===c)),s,t)}
 function ok(x,msg){L.assertions++;if(!x)throw Error(msg)}
 function solve(n,E,s,t,pins=[],want=null,terminals=[s,t]){
  L.calls++;let G=new Map(), stats={maxB:0,maxR:0,maxD:0,peak:0,joins:0,forced:0,retained:0};const nonreach=want===null;
  for(let [a,c] of pins)if(!add(G,a,c))return {count:0n,x:null,stats};
  let F;
  while(true){L.closureSweeps++;F=[];for(let a of E){let B=new Map(),yes=true;for(let [m,c] of a.g){L.edgeTests++;let [v,b]=reduce(G,m,c);if(!add(B,v,b)){yes=false;break}}if(yes)F.push(e(a.u,a.v,[...B.values()]))}
   if(!nonreach)break;
   let U=F.filter(a=>a.g.length===0);
   if(reaches(U,s,t))return {count:0n,x:null,stats};
   if(!reaches(F,s,t)){let x=witness(G);ok(valid(E,x,s,t),"early witness");return {count:1n<<BigInt(n-G.size),x,stats}}
   let A=reachset(U,s),B=reachset(U,t,true),q=F.find(a=>a.g.length===1&&A.has(a.u)&&B.has(a.v));
   if(!q)break;let [m,c]=q.g[0];ok(add(G,m,c^1),"forced");L.forced++;stats.forced++;
  }
  const all=F.map(a=>a.g.map(v=>v[0]));
  const ends=F.map(a=>[a.u,a.v]);
  function closure(V,arcs){let M=V.map((u,i)=>V.map((v,j)=>i===j));let idx=new Map(V.map((u,i)=>[u,i]));for(let [u,v] of arcs)M[idx.get(u)][idx.get(v)]=true;
   for(let k=0;k<V.length;k++)for(let i=0;i<V.length;i++)if(M[i][k])for(let j=0;j<V.length;j++)if(M[k][j])M[i][j]=true;
   let out=[];for(let i=0;i<V.length;i++)for(let j=0;j<V.length;j++)if(i!==j&&M[i][j])out.push([V[i],V[j]]);return out}
  function canon(arcs){return arcs.map(a=>a.join(",")).join(";")}
  function node(lo,hi){
   let U=basis(all.slice(lo,hi).flat()),O=basis([...all.slice(0,lo),...all.slice(hi)].flat()),I=intersection(U,O);
   let outside=new Set([...ends.slice(0,lo),...ends.slice(hi)].flat()),inside=new Set(ends.slice(lo,hi).flat());
   let V=[...new Set([...terminals,...[...inside].filter(x=>outside.has(x))])].sort((a,b)=>a-b);
   stats.maxB=Math.max(stats.maxB,V.length);stats.maxR=Math.max(stats.maxR,I.length);
   let T=new Map();
   function emit(W,arcs,count){let J=I.map(a=>value(W,a)).join("");let key=J+"|"+canon(arcs);let old=T.get(key);if(old){old.count+=count;L.mergedStates++}else T.set(key,{W,arcs,count})}
   if(hi-lo<=1){
    stats.maxD=Math.max(stats.maxD,U.length);let a=F[lo];if(!a){emit(new Map(),[],1n)}
    else for(let z=0n;z<(1n<<BigInt(U.length));z++){L.leafWords++;let W=new Map();for(let i=0;i<U.length;i++)add(W,U[i],Number((z>>BigInt(i))&1n));
      let enabled=a.g.every(([m,c])=>value(W,m)===c);let arcs=enabled&&V.includes(a.u)&&V.includes(a.v)&&a.u!==a.v?[[a.u,a.v]]:[];
      emit(W,arcs,1n)}
   }else{
    let mid=(lo+hi)>>1,A=node(lo,mid),B=node(mid,hi);
    let J=intersection(A.U,B.U);let Q=[...new Set([...A.V,...B.V])].sort((a,b)=>a-b);
    for(let a of A.T.values())for(let b of B.T.values()){
     L.joinPairs++;stats.joins++;if(J.some(m=>value(a.W,m)!==value(b.W,m))){L.rejectedPairs++;continue}
     let W=new Map(a.W);for(let [m,c] of b.W.values())ok(add(W,m,c),"join witness incompatibility");
     let arcs=closure(Q,[...a.arcs,...b.arcs]).filter(([u,v])=>V.includes(u)&&V.includes(v));emit(W,arcs,a.count*b.count);
    }
   }
   stats.peak=Math.max(stats.peak,T.size);L.peakTable=Math.max(L.peakTable,T.size);stats.retained+=T.size;
   return {U,I,V,T}
  }
  let R=node(0,F.length);L.peakRetainedEntries=Math.max(L.peakRetainedEntries,stats.retained);let count=0n,x=null;
  for(let a of R.T.values())if(nonreach?!a.arcs.some(([u,v])=>u===s&&v===t):want(a.arcs)){
   count+=a.count;if(x===null){let W=new Map(G);for(let [m,c] of a.W.values())ok(add(W,m,c),"root lift");x=witness(W)}
  }
  count<<=BigInt(n-G.size-R.U.length);
  if(x!==null){ok(pins.every(([m,c])=>parity(m&x)===c),"pins");if(nonreach)ok(valid(E,x,s,t),"source lift")}
  return {count,x,stats}
 }
 function brute(n,E,s,t,pins=[]){let c=0n;for(let x=0n;x<(1n<<BigInt(n));x++){L.referenceWords++;if(pins.every(([m,b])=>parity(m&x)===b)&&valid(E,x,s,t))c++}return c}
 let state=20261124;const rnd=k=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state%k};
 const random={sat:0,unsat:0};for(let q=0;q<100;q++){let n=5,v=5,E=[];for(let j=0;j<8;j++){let g=[];for(let k=0;k<1+rnd(3);k++)g.push([BigInt(1+rnd(31)),rnd(2)]);E.push(e(rnd(v),rnd(v),g))}let pins=q%3===0?[[BigInt(1+rnd(31)),rnd(2)]]:[];let a=solve(n,E,0,v-1,pins),b=brute(n,E,0,v-1,pins);ok(a.count===b,"random");random[b?"sat":"unsat"]++}
 function clauseEdge(vars,word){return e(0,1,vars.map((v,j)=>[bit(v),(word>>j)&1]))}
 let cube={sat:0,unsat:0};for(let mask=0;mask<256;mask++){let E=[];for(let j=0;j<8;j++)if(mask&(1<<j))E.push(clauseEdge([0,1,2],j));let a=solve(3,E,0,1);ok(a.count===brute(3,E,0,1),"cube");cube[a.count?"sat":"unsat"]++}
 let triples=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],F=triples.flatMap(v=>[clauseEdge(v,0),clauseEdge(v,7)]);
 let fano=[];for(let i=-1;i<F.length;i++){let E=F.filter((_,j)=>j!==i);let a=solve(7,E,0,1);ok(a.count===brute(7,E,0,1)&&a.count===(i<0?0n:5n),"Fano");fano.push(String(a.count))}
 let scales=[];for(let k of [4,16,64,128])for(let sat of [false,true]){let E=[];for(let i=0;i<k;i++){E.push(e(i,i+1,[[bit(i),1]]));E.push(e(i,i+1,[[bit(i),sat&&i===Math.floor(k/2)?1:0]]));E.push(e(i+1,i,[[bit(i)^(i+1<k?bit(i+1):0n),1]]))}
  let a=solve(k,E,0,k);ok(a.count===(sat?1n<<BigInt(k-1):0n),"scale");scales.push({k,sat,count:String(a.count),...a.stats,minFeedbackLowerBound:Math.floor((k+1)/2)})}
 // Two predicates, common dense observation; same or opposite literal.
 let identity=[];for(let equal of [true,false]){let E=[e(0,1,[[7n,1]]),e(2,3,[[7n,equal?1:0]])];let a=solve(3,E,0,1,[],arcs=>arcs.some(([u,v])=>u===0&&v===1)!==arcs.some(([u,v])=>u===2&&v===3),[0,1,2,3]);ok(a.count===(equal?0n:8n),"identity");identity.push({equal,disagreements:String(a.count)})}
 // A true forced-path deduction and a parity-inconsistent guard.
 let forced=solve(3,[e(0,2),e(2,1,[[3n,1]])],0,1);ok(forced.count===4n&&forced.stats.forced===1,"forced closure");
 let empty=solve(3,[e(0,1)],0,1,[[3n,0],[3n,1]]);ok(empty.count===0n,"inconsistent");
 return {seed:20261124,random,cube,fano,scales,identity,forced:{count:String(forced.count),stats:forced.stats},ledger:L};
}
console.log(JSON.stringify(experiment(),null,2));
