function BD07(){
 const S={rref:0,xor:0,projections:0,closureScans:0,forced:0,eventDrops:0,edges:0,merges:0,cancellations:0,queries:0,queryTerms:0,reference:0,assertions:0,lifts:0};
 const check=(v,m)=>{S.assertions++;if(!v)throw Error(m)};
 const bit=i=>1n<<BigInt(i+1),eq=(i,b)=>bit(i)|BigInt(b);
 const pivot=x=>x.toString(2).length-1;
 function rr(rows){S.rref++;let a=[];for(let x of rows){for(let y of a)if(x&(1n<<BigInt(pivot(y)))){x^=y;S.xor++}if(x===1n)return null;if(!x)continue;let p=1n<<BigInt(pivot(x));a=a.map(y=>{if(y&p){S.xor++;return y^x}return y});a.push(x);a.sort((x,y)=>pivot(y)-pivot(x));}return a}
 const hom=a=>a.map(x=>x&~1n);
 const key=a=>a.map(x=>x.toString(16)).join(",");
 function proj(H,U){S.projections++;let b=new Map(),out=[];for(let x of H){let v=x&~1n;for(let y of U)if(v&(1n<<BigInt(pivot(y)))){v^=y;S.xor++}while(v){let p=pivot(v),t=b.get(p);if(!t){b.set(p,[v,x]);break}v^=t[0];x^=t[1];S.xor+=2}if(!v)out.push(x)}return rr(out)}
 function close(G,E){G=rr(G);if(G===null)return null;E=E.slice();while(true){S.closureScans++;let seen=new Set(),change=false;for(let j=0;j<E.length;j++){let J=rr([...G,...E[j]]);if(J===null){E.splice(j,1);S.eventDrops++;change=true;break}let d=J.length-G.length;if(!d)return null;if(d===1){let a=E[j].find(x=>{let B=rr([...G,x]);return B&&B.length>G.length});check(a!==undefined,"unit");G=rr([...G,a^1n]);E.splice(j,1);S.forced++;change=true;break}let k=key(J);if(seen.has(k)){E.splice(j,1);S.eventDrops++;change=true;break}seen.add(k)}if(!change)return [G,E]}}
 function conditional(M,P){S.queries++;let n=0n;for(let [H,w] of M.values()){S.queryTerms++;let J=rr([...H,...P]);if(J){let q=1n<<BigInt(J.length-H.length);check(w%q===0n,"conditional division");n+=w/q}}return n}
 function solve(n,G,E,lift=true){let C=close(G,E);if(!C)return {count:0n,peak:0,states:0};let [A,F]=C,m=F.length,U=Array(m+1);U[m]=[];for(let i=m-1;i>=0;i--)U[i]=rr([...U[i+1],...hom(F[i])]);let H=proj(A,U[0]),M=new Map([[key(H),[H,1n<<BigInt(n-A.length)]]]),tables=[M],peak=1,states=1;
 function add(D,H,w){S.edges++;let k=key(H),old=D.get(k);if(old){S.merges++;w+=old[1]}if(w===0n){S.cancellations++;D.delete(k)}else D.set(k,[H,w])}
 for(let i=0;i<m;i++){let D=new Map();for(let [H,w] of M.values()){add(D,proj(H,U[i+1]),w);let J=rr([...H,...F[i]]);if(J){let q=1n<<BigInt(J.length-H.length);check(w%q===0n,"transition division");add(D,proj(J,U[i+1]),-w/q)}else S.edges++}M=D;tables.push(M);peak=Math.max(peak,M.size);states+=M.size}
 let count=M.get("")?.[1]??0n;check(count>=0n,"negative count");if(!lift||!count)return {count,peak,states};
 let P=[],audit=A.slice();
 for(let i=m-1;i>=0;i--){
  const good=Q=>conditional(tables[i],Q)-conditional(tables[i],[...Q,...F[i]]);
  check(good(P)>0n,"reverse invariant");
  for(let a of U[i]){let J=rr([...P,a]);if(J===null||J.length===P.length)continue;let c=good(J);P=c>0n?J:rr([...P,a^1n]);check(P!==null&&good(P)>0n,"reverse choice");let certified=close([...audit,...P],F);check(certified!==null,"closure after pin");audit=certified[0]}
 }
 let J=rr([...audit,...P]);check(J!==null,"lift consistent");let w=0n;for(let x of J)if(x&1n)w|=1n<<BigInt(pivot(x)-1);
 const hit=(Q)=>Q.every(x=>{let v=(x>>1n)&w,p=0n;while(v){v&=v-1n;p^=1n}return p===(x&1n)});
 check(hit(G)&&E.every(Q=>!hit(Q)),"source witness");S.lifts++;return {count,peak,states,w}
 }
 function brute(n,G,E){let c=0n;const hit=(Q,w)=>Q.every(x=>{let v=(x>>1n)&w,p=0n;while(v){v&=v-1n;p^=1n}return p===(x&1n)});for(let w=0n;w<(1n<<BigInt(n));w++){S.reference++;if(hit(G,w)&&E.every(Q=>!hit(Q,w)))c++}return c}
 const cube=Array.from({length:8},(_,j)=>[0,1,2].map(i=>eq(i,(j>>i)&1)));
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].flatMap(e=>[0,1].map(b=>e.map(i=>eq(i,b))));
 let groups={cube:[0,0],fano:[0,0],random:[0,0]},scale=[],order=[];
 function test(name,n,G,E){let a=solve(n,G,E),b=brute(n,G,E);check(a.count===b,"count "+name);groups[name][b>0n?0:1]++;return a}
 for(let j=0;j<256;j++)test("cube",3,[],cube.filter((_,i)=>j&(1<<i)));
 for(let j=-1;j<14;j++)test("fano",7,[],fano.filter((_,i)=>i!==j));
 let seed=20261124;const rnd=k=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%k};
 for(let t=0;t<100;t++){let n=3+rnd(5),G=Array.from({length:rnd(3)},()=>BigInt(1+rnd((1<<n)-1))*2n+BigInt(rnd(2))),E=Array.from({length:2+rnd(9)},()=>Array.from({length:1+rnd(4)},()=>BigInt(1+rnd((1<<n)-1))*2n+BigInt(rnd(2))));test("random",n,G,E)}
 for(let h of [4,8,16,32]){let m=h,n=h+m,common=Array.from({length:h},(_,i)=>eq(i,0)),E=Array.from({length:m},(_,i)=>[...common,eq(h+i,0)]);let a=solve(n,[],E);check(a.count===((1n<<BigInt(h))-1n)*(1n<<BigInt(m))+1n,"scale");check(a.peak<=2,"scale peak");let b=solve(n+3,[],[...E,...cube.map(Q=>Q.map(x=>((x>>1n)<<BigInt(n+1))|(x&1n)))]);check(b.count===0n,"scale UNSAT");scale.push({h,m,count:String(a.count),peak:a.peak,states:a.states,unsatPeak:b.peak,unsatStates:b.states})}
 for(let m of [2,4,6,8]){let A=[],B=[];for(let i=0;i<m;i++){A.push([eq(i,0),eq(m+i,0)]);B.push([eq(i,1),eq(2*m+i,0)])}let a=solve(3*m,[],[...A,...B],false),b=solve(3*m,[],A.flatMap((e,i)=>[e,B[i]]),false);check(a.count===4n**BigInt(m)&&b.count===a.count,"order count");check(a.peak===2**m&&b.peak<=2,"order peak");order.push({m,badPeak:a.peak,goodPeak:b.peak,badStates:a.states,goodStates:b.states})}
 return {groups,scale,order,ledger:S}
}
console.log(JSON.stringify(BD07(),null,2));
