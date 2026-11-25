/* GD19 standalone checker, Node.js. No dependencies. */
function run(){
 const L={gauss:0,xor:0,transitions:0,positive:0,merges:0,implicationTests:0,closureCalls:0,referenceWords:0,assertions:0,unitScans:0,unitPins:0};
 function ok(b,msg){L.assertions++;if(!b)throw Error(msg)}
 const bit=i=>1n<<BigInt(i), top=x=>x.toString(2).length-1;
 function parity(x){let p=0;while(x){x&=x-1n;p^=1}return p}
 function basis(rows){const M=new Map;for(let v of rows){while(v){let k=top(v);if(!M.has(k)){M.set(k,v);break}v^=M.get(k);L.xor++}}return [...M.values()]}
 function inter(A,B){const M=new Map, out=[];function ins(v,t){while(v){let k=top(v);if(!M.has(k)){M.set(k,[v,t]);return}let [a,b]=M.get(k);v^=a;t^=b;L.xor++}if(t)out.push(t)}for(let a of A)ins(a,0n);for(let b of B)ins(b,b);return basis(out)}
 function solve(E){L.gauss++;const M=new Map;for(let [v,b] of E){while(v){let k=top(v);if(!M.has(k)){M.set(k,[v,b]);break}let [a,c]=M.get(k);v^=a;b^=c;L.xor++}if(!v&&b)return null}let x=0n;for(let k of [...M.keys()].sort((a,b)=>a-b)){let [v,b]=M.get(k);if(parity(v&x)!==b)x|=bit(k)}return {rank:M.size,x}}
 function eq(B,x){return B.map(r=>[r,parity(r&x)])}
 function label(B,x){let z=0n;B.forEach((r,j)=>{if(parity(r&x))z|=bit(j)});return z}
 function fromLabel(B,z){return B.map((r,j)=>[r,Number((z>>BigInt(j))&1n)])}
 const mask=vs=>vs.reduce((a,v)=>a|bit(v),0n);
 function evalDAG(G,x){let R=mask(G.sources);for(const [u,v,E] of G.edges){if((R&bit(u))&&E.every(([r,b])=>parity(r&x)===b))R|=bit(v)}return Number(label(G.sinks.map(bit),R))}
 function terminal(G,compress=true){
  const {d,V,edges,sources,sinks}=G,m=edges.length, src=mask(sources),fixed=src|mask(sinks);
  for(let i=0;i<m;i++)ok(edges[i][0]<edges[i][1]&&(!i||edges[i-1][0]<=edges[i][0]),"topological order");
  const U=edges.map(e=>basis(e[2].map(q=>q[0]))),P=[[]],S=Array(m+1),past=[0n],future=Array(m+1);
  S[m]=[];future[m]=0n;
  for(let i=0;i<m;i++){P.push(basis([...P[i],...U[i]]));past.push(past[i]|bit(edges[i][0])|bit(edges[i][1]))}
  for(let i=m-1;i>=0;i--){S[i]=basis([...S[i+1],...U[i]]);future[i]=future[i+1]|bit(edges[i][0])|bit(edges[i][1])}
  const W=P.map((p,i)=>inter(p,S[i])),live=P.map((_,i)=>(past[i]&future[i])|fixed);
  let maxw=Math.max(...W.map(w=>w.length)),maxp=0;
  for(let a of live){let z=a,p=0;while(z){z&=z-1n;p++}maxp=Math.max(maxp,p)}
  const caches=Array.from({length:m+1},()=>new Map);
  function closure(i,lam,R){L.closureCalls++;if(!compress)return R&live[i];let tab=caches[i].get(lam);
   if(!tab){const H=fromLabel(W[i],lam),desc=Array.from({length:V},(_,v)=>bit(v));
    for(let j=m-1;j>=i;j--){let [u,v,E]=edges[j],yes=true;for(let [r,b] of E){L.implicationTests++;if(solve([...H,[r,b^1]])!==null){yes=false;break}}if(yes)desc[u]|=desc[v]}
    tab=desc;caches[i].set(lam,tab)}
   let z=R,out=0n;while(z){let v=top(z);z^=bit(v);out|=tab[v]}return out&live[i]
  }
  let T=new Map([["0:"+closure(0,0n,src),{lam:0n,R:closure(0,0n,src),count:1n,x:0n}]]);
  let peak=T.size;
  for(let i=0;i<m;i++){
   const next=new Map, [u,v,E]=edges[i],dimB=basis([...W[i],...U[i]]).length,tc=new Map;
   for(let a of T.values()){
    let tr=tc.get(a.lam);
    if(!tr){tr=[];let h0=fromLabel(W[i],a.lam);
     for(let eta=0n;eta<(1n<<BigInt(W[i+1].length));eta++){L.transitions++;let H=[...h0,...fromLabel(W[i+1],eta)],all=solve(H);if(!all)continue;let yes=solve([...H,...E]);let total=1n<<BigInt(dimB-all.rank),c1=yes?1n<<BigInt(dimB-yes.rank):0n;ok(c1<=total,"nonnegative weight");
      for(let [truth,c] of [[0,total-c1],[1,c1]])if(c){tr.push({eta,H,truth,c});L.positive++}
     }tc.set(a.lam,tr)}
    for(let t of tr){let R=a.R;if(t.truth&&(R&bit(u)))R|=bit(v);R=closure(i+1,t.eta,R);let k=t.eta+":"+R,old=next.get(k),mass=a.count*t.c;
     if(old){old.count+=mass;L.merges++;continue}
     const Q=[...eq(P[i],a.x),...t.H];let s=t.truth?solve([...Q,...E]):null;
     if(!t.truth)for(let [r,b] of E){s=solve([...Q,[r,b^1]]);if(s)break}
     ok(!!s,"actual witness lift");next.set(k,{lam:t.eta,R,count:mass,x:s.x})
    }
   }T=next;peak=Math.max(peak,T.size)
  }
  const hist=Array(1<<sinks.length).fill(0n), witnesses={};let factor=1n<<BigInt(d-P[m].length);
  for(let a of T.values()){let j=Number(label(sinks.map(bit),a.R));hist[j]+=a.count*factor;ok(evalDAG(G,a.x)===j,"actual sink witness");witnesses[j]=a.x}
  ok(hist.reduce((a,b)=>a+b,0n)===(1n<<BigInt(d)),"mass conservation");
  return {hist,peak,maxw,maxp,witnesses}
 }
 function reference(G){let h=Array(1<<G.sinks.length).fill(0n);for(let x=0n;x<(1n<<BigInt(G.d));x++){h[evalDAG(G,x)]++;L.referenceWords++}return h}
 function check(G){let a=terminal(G),b=terminal(G,false),r=reference(G);ok(a.hist.every((x,i)=>x===r[i]&&x===b.hist[i]),"count mismatch");return a}
 function unitClose(C){let pins=new Map,changed=true;while(changed){changed=false;L.unitScans++;for(let c of C){if(c.some(([v,b])=>pins.has(v)&&pins.get(v)===b))continue;let u=c.filter(([v])=>!pins.has(v));if(!u.length)return {conflict:true,pins};if(u.length===1){pins.set(...u[0]);L.unitPins++;changed=true}}}return {conflict:false,pins}}
 function cnf(d,C){let u=unitClose(C);ok(!u.conflict&&u.pins.size===0,"benchmark is closure-stable");return {d,V:2,sources:[0],sinks:[1],edges:C.map(c=>[0,1,c.map(([v,b])=>[bit(v),b^1])])}}
 const triples=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 const C=triples.flatMap(t=>[t.map(v=>[v,0]),t.map(v=>[v,1])]);
 let fano=[];for(let j=-1;j<C.length;j++){let G=cnf(7,C.filter((_,i)=>i!==j)),a=check(G);ok(a.hist[0]===BigInt(j<0?0:5),"Fano count");fano.push(Number(a.hist[0]))}
 let flips=[];for(let i=0;i<7;i++)for(let j=0;j<3;j++){let D=C.map(c=>c.map(q=>[...q]));for(let p of [2*i,2*i+1])D[p][j][1]^=1;let a=check(cnf(7,D));ok(a.hist[0]===10n,"Fano flip");flips.push(Number(a.hist[0]))}
 let unit=unitClose([[[0,1]],[[0,0],[1,1]],[[1,0],[2,1]]]);ok(unit.pins.size===3&&!unit.conflict,"unit closure cascade");
 let unitBad=unitClose([[[0,1]],[[0,0]]]);ok(unitBad.conflict,"unit contradiction");
 let seed=20261124;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
 let random=0,identity=0,nonidentity=0;for(let z=0;z<48;z++){let d=5,V=7,E=[];for(let u=0;u<V-2;u++)for(let v=u+1;v<V;v++)if(rand(3)!==0){let G=[];for(let j=0,k=rand(4);j<k;j++)G.push([BigInt(rand(1<<d)),rand(2)]);E.push([u,v,G])}let G={d,V,sources:[0],sinks:[V-2,V-1],edges:E},a=check(G);random++;if(a.hist[1]+a.hist[2]===0n)identity++;else nonidentity++}
 function probe(G,r,b){return {...G,V:G.V+2,sources:[...G.sources,G.V],sinks:[...G.sinks,G.V+1],edges:[...G.edges,[G.V,G.V+1,[[r,b]]]]}}
 let neigh=cnf(7,C.slice(1)),forced=[];for(let r=1n;r<128n;r++){let a=terminal(probe(neigh,r,1));ok(a.hist[0]+a.hist[2]===5n,"probe total");if(a.hist[0]===0n||a.hist[2]===0n)forced.push([r,a.hist[0]===0n?1:0])}
 let rr=basis(forced.map(x=>x[0])).length;ok(rr===3,"Fano neighbor forced rank");
 for(let x=0n;x<128n;x++)if(evalDAG(neigh,x)===0)ok(forced.every(([r,b])=>parity(r&x)===b),"forced audit");
 let scale=[];for(let n of [8,16,32,64])for(let root of [true,false]){let E=[[0,1,[[1n,1]]],[0,1,[[1n,root?0:1]]]];for(let i=1;i<n;i++)E.push([0,i+1,[[bit(i),1]]]);for(let i=1;i<=n;i++)E.push([i,i+1,[]]);let G={d:n,V:n+2,sources:[0],sinks:[n+1],edges:E},a=terminal(G);ok(a.hist[0]===(root?0n:1n),"chain safe count");scale.push({n,root,safe:String(a.hist[0]),peak:a.peak,w:a.maxw,p:a.maxp,rawCentral:String(1n<<BigInt(n-(root?1:0)))})}
 let hostile=[];for(let n of [4,6,8]){let E=[];for(let i=0;i<n;i++)E.push([0,i+1,[[bit(i),1]]]);for(let i=0;i<n;i++)E.push([i+1,n+1,[[bit(n+i),1]]]);let G={d:2*n,V:n+2,sources:[0],sinks:[n+1],edges:E},a=terminal(G);ok(a.hist[0]===3n**BigInt(n),"hostile safe count");ok(a.peak>=2**n,"hostile exponential central");hostile.push({n,peak:a.peak,w:a.maxw,safe:String(a.hist[0])})}
 return {fano,flips,random,identity,nonidentity,forcedRows:forced.length,forcedRank:rr,scale,hostile,ledger:L};
}
console.log(JSON.stringify(run(),null,2));
