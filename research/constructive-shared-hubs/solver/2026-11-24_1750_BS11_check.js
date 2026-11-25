function runBS11(){
 const stats={gaussInsert:0,imageQueries:0,closureScans:0,pins:0,projectionCalls:0,contracted:0,matchScans:0,branchNodes:0,memoHits:0,smallCountCalls:0,smallCountWords:0,sourceChecks:0,wheelLifts:0,assertions:0};
 const bit=i=>1n<<BigInt(i), par=x=>{let p=0;while(x){x&=x-1n;p^=1}return p}, val=(a,x)=>par(a[0]&x)^a[1];
 function ok(c,msg){stats.assertions++;if(!c)throw Error(msg)}
 function top(x){return x.toString(2).length-1}
 function insert(B,a,b){stats.gaussInsert++;while(a){let p=top(a),q=B.get(p);if(!q){B.set(p,[a,b]);return true}a^=q[0];b^=q[1]}return b===0||b===0n}
 function reduce(B,a,b){while(a){let q=B.get(top(a));if(!q)return null;a^=q[0];b^=q[1]}return b}
 function linear(rows,d){let B=new Map();for(let [a,b] of rows)if(!insert(B,a,b))return null;let ps=[...B.keys()].sort((a,b)=>a-b);
  function complete(x,hom){for(let p of ps){let [a,b]=B.get(p);if(par(a&x)!==(hom?0:b))x^=bit(p)}return x}
  let point=complete(0n,false),kernel=[];for(let i=0;i<d;i++)if(!B.has(i))kernel.push(complete(bit(i),true));
  for(let p of ps)for(let q of ps)if(q>p&&(B.get(q)[0]&bit(p))){let a=B.get(q),b=B.get(p);B.set(q,[a[0]^b[0],a[1]^b[1]])}
  return {point,kernel,rank:B.size,key:ps.map(p=>B.get(p).join(":")).join(";")}}
 function check(F,x){stats.sourceChecks++;return F.every(C=>C.some(a=>val(a,x)===0))}
 function guardOK(G,x){return G.every(([a,b])=>par(a&x)===b)}
 function DS(n){let p=Array.from({length:n},(_,i)=>i);return {f(i){while(p[i]!==i){p[i]=p[p[i]];i=p[i]}return i},u(a,b){a=this.f(a);b=this.f(b);if(a!==b)p[a]=b}}}
 function project(F,d,G=[],P=[]){stats.projectionCalls++;if(F.some(c=>!c.length))return null;
  let K=linear([...G.map(([a])=>[a,0]),...P.map(a=>[a,0])],d),O=F.flat(),L=O.length,owners=F.flatMap((C,i)=>C.map(()=>i));
  const image=x=>O.reduce((y,a,i)=>y|(BigInt(par(a[0]&x))<<BigInt(i)),0n);
  const word=x=>O.reduce((y,a,i)=>y|(BigInt(val(a,x))<<BigInt(i)),0n);
  let B=new Map();for(let h of K.kernel)insert(B,image(h),h);
  const lookup=y=>{stats.imageQueries++;return reduce(B,y,0n)};
  let D=DS(L),free=Array.from({length:L},(_,i)=>lookup(bit(i))!==null);
  for(let i=0;i<L;i++)for(let j=i+1;j<L;j++)if(lookup(bit(i)^bit(j))!==null)D.u(i,j);
  let groups=new Map();for(let i=0;i<L;i++){let k=D.f(i);if(!groups.has(k))groups.set(k,[]);groups.get(k).push(i)}
  let blocks=[...groups.values()], forms=blocks.map(A=>A.some(i=>free[i])?[0n,0]:A.reduce((a,i)=>[a[0]^O[i][0],a[1]^O[i][1]],[0n,0]));
  let graph=DS(blocks.length+F.length);
  for(let i=0;i<blocks.length;i++)for(let o of blocks[i])graph.u(i,blocks.length+owners[o]);
  let cs=new Map();function get(k){if(!cs.has(k))cs.set(k,{bs:[],clauses:0,edges:0});return cs.get(k)}
  for(let i=0;i<blocks.length;i++){let c=get(graph.f(i));c.bs.push(i);c.edges+=blocks[i].length}
  for(let i=0;i<F.length;i++)get(graph.f(blocks.length+i)).clauses++;
  let Q=[...cs.values()].filter(c=>c.edges===c.bs.length+c.clauses-1).map(c=>c.bs.map(i=>forms[i]));
  let slots=F.map(()=>[]),slotOwner=[];for(let i=0;i<F.length;i++)for(let j=1;j<F[i].length;j++){slots[i].push(slotOwner.length);slotOwner.push(i)}
  let adj=blocks.map(A=>[...new Set(A.flatMap(o=>slots[owners[o]]))]);
  function lift(x){let active=forms.map((a,i)=>val(a,x)?i:-1).filter(i=>i>=0),matched=Array(slotOwner.length).fill(-1);
   function aug(i,seen){for(let s of adj[i]){stats.matchScans++;if(seen.has(s))continue;seen.add(s);if(matched[s]===-1||aug(matched[s],seen)){matched[s]=i;return true}}return false}
   for(let i of active)if(!aug(i,new Set()))throw Error("projected support not liftable");
   let target=0n;for(let s=0;s<matched.length;s++)if(matched[s]>=0){let o=blocks[matched[s]].find(o=>owners[o]===slotOwner[s]);target|=bit(o)}
   let h=lookup(word(x)^target);ok(h!==null,"fiber correction");let z=x^h;
   ok(guardOK(G,z)&&P.every(a=>par(a&z)===par(a&x))&&check(F,z),"source lift");
   return z}
  return {Q,forms,blocks,lift,components:[...cs.values()].map(c=>({blocks:c.bs.length,clauses:c.clauses,edges:c.edges})),moves:L-blocks.length+(free.some(Boolean)?1:0)}}
 function solve(F,d,G=[],P=[]){let memo=new Map();
  function rec(F,G){stats.branchNodes++;let A=linear(G,d);if(!A)return null;
   while(true){let keep=[],pin=null;for(let C of F){stats.closureScans++;let bad=linear([...G,...C.map(([a,b])=>[a,1^b])],d);if(!bad)continue;
     let k=bad.rank-A.rank;if(k===0)return null;if(k===1){let [a,b]=C.find(([a])=>A.kernel.some(h=>par(a&h)));pin=[a,b];break}keep.push(C)}
    if(pin){stats.pins++;G=[...G,pin];A=linear(G,d);if(!A)return null;continue}
    F=keep;break}
   if(!F.length)return A.point;
   let key=A.key+"|"+F.map(C=>C.map(a=>a.join(":")).sort().join(",")).sort().join(";");
   if(memo.has(key)){stats.memoHits++;return memo.get(key)}
   let pr=project(F,d,G,P),res=null;
   if(pr.Q.flat().length<F.flat().length){stats.contracted++;let x=rec(pr.Q,G);res=x===null?null:pr.lift(x)}
   else { // paid small observation quotient count; decision witness only
    let O=F.flat(), B=new Map();for(let h of A.kernel){let y=O.reduce((v,[a],i)=>v|(BigInt(par(a&h))<<BigInt(i)),0n);insert(B,y,h)}
    if(B.size<=4){stats.smallCountCalls++;let hs=[...B.values()].map(a=>a[1]);for(let w=0;w<2**hs.length;w++){stats.smallCountWords++;let x=A.point;for(let i=0;i<hs.length;i++)if(w&(1<<i))x^=hs[i];if(check(F,x)&&res===null)res=x}}
    else {let [a,b]=O.find(([a])=>A.kernel.some(h=>par(a&h)));res=rec(F,[...G,[a,b]]);if(res===null)res=rec(F,[...G,[a,1^b]])}
   }
   memo.set(key,res);return res}
  let x=rec(F,G);if(x!==null)ok(guardOK(G,x)&&check(F,x),"final original verification");return x}
 let seed=20811;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
 let summary={randomFibers:0,randomSAT:0,randomUNSAT:0,randomLifts:0,randomStrictProjections:0,fano:[],wheelFibers:0,path:[],denseMoves:0,cyclic:[]};
 function brute(F,d,G=[]){for(let x=0;x<2**d;x++)if(guardOK(G,BigInt(x))&&check(F,BigInt(x)))return BigInt(x);return null}
 function audit(F,d,G,P){let pr=project(F,d,G,P),tab=new Map();function key(x){return [...P.map(a=>par(a&x)),...pr.forms.map(a=>val(a,x))].join("")}
  for(let i=0;i<2**d;i++){let x=BigInt(i);if(!guardOK(G,x))continue;let k=key(x);tab.set(k,(tab.get(k)||false)||check(F,x))}
  for(let i=0;i<2**d;i++){let x=BigInt(i);if(!guardOK(G,x))continue;let accept=check(pr.Q,x);ok(accept===tab.get(key(x)),"fiber equivalence");summary.randomFibers++;if(accept){pr.lift(x);summary.randomLifts++}}
  let x=solve(F,d,G,P),y=brute(F,d,G);ok((x===null)===(y===null),"decision agreement");if(y===null)summary.randomUNSAT++;else summary.randomSAT++;
  if(pr.Q.flat().length<F.flat().length)summary.randomStrictProjections++}
 for(let t=0;t<140;t++){let d=3+rnd(4),F=Array.from({length:2+rnd(6)},()=>Array.from({length:1+rnd(3)},()=>[BigInt(rnd(2**d)),rnd(2)])), G=[],P=[];
  if(t%3===0)G.push([BigInt(1+rnd(2**d-1)),rnd(2)]);if(t%4===0)P.push(BigInt(1+rnd(2**d-1)));audit(F,d,G,P)}
 const cnf=C=>C.map(c=>c.map(l=>[bit(Math.abs(l)-1),l>0?1:0]));
 // doubled pentagon: signs 0 and direction, legal differences exclude both; XOR around rim is zero.
 function wheel(bits){let ds=[...bits.map(b=>b?2:1),1,1],paths=new Map([[0,[]]]);for(let d of ds){let next=new Map();for(let [x,p] of paths)for(let v=0;v<4;v++)if(v!==0&&v!==d&&!next.has(x^v))next.set(x^v,[...p,v]);paths=next}
  if(!paths.has(0))return null;let p=paths.get(0),x=0,colors=[0];for(let i=0;i<4;i++){x^=p[i];colors.push(x)}
  ok(colors.every((c,i)=>{let v=c^colors[(i+1)%5];return v!==0&&v!==ds[i]}),"wheel source edges");stats.wheelLifts++;return colors}
 for(let w=0;w<8;w++){let bs=[0,1,2].map(i=>!!(w&(1<<i)));ok((wheel(bs)!==null)===bs.some(Boolean),"wheel truth");summary.wheelFibers++}
 let es=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]],base=es.flatMap(e=>[e,e.map(x=>-x)]);
 for(let j=-1;j<base.length;j++){let C=base.filter((_,i)=>i!==j),F=cnf(C),x=solve(F,7),y=brute(F,7);ok((x===null)===(y===null),"Fano");ok((x!==null)===(j!==-1),"Fano expected");
  if(x!==null)for(let c of F)ok(wheel(c.map(a=>val(a,x)===0))!==null,"Fano wheel lift");summary.fano.push({removed:j,sat:x!==null})}
 summary.denseMoves=project(cnf(base),7).moves;
 // chain of b parity blocks, b-1 binary clause owners. Endpoint singleton parity, each internal has a free private bit.
 for(let b of [4,16,64,128]){let F=[],P=Array.from({length:b},(_,i)=>bit(i)),d=2*b-2;
  for(let i=0;i<b-1;i++){let left=i===0?[bit(0),0]:[bit(b+i-1)^bit(i),0];let right=i===b-2?[bit(b-1),0]:[bit(b+i),0];F.push([left,right])}
  let pr=project(F,d,[],P);ok(pr.Q.length===1&&pr.Q[0].length===b&&pr.moves===b-2,"path projection");let bad=(1n<<BigInt(b))-1n,good=bad^1n;
  ok(!check(pr.Q,bad)&&check(pr.Q,good),"path opposite labels");pr.lift(good);
  // original protected fibers fixed by guard, solver reclosure applied.
  for(let v of [bad,good]){let G=P.map(a=>[a,par(a&v)]),x=solve(F,d,G,P);ok((x!==null)===(v===good),"path solver")}
  summary.path.push({blocks:b,sourceOccurrences:2*(b-1),projectedOccurrences:b,privateMoves:pr.moves,oppositeLabels:true})}
 // cycle of b blocks, each contributes two occurrences; every parity word extends.
 for(let b of [3,12,40]){let F=[],P=Array.from({length:b},(_,i)=>bit(i));for(let i=0;i<b;i++)F.push([[bit(b+i)^bit(i),0],[bit(b+(i+1)%b),0]]);
  let pr=project(F,2*b,[],P);ok(pr.Q.length===0,"cyclic universal");pr.lift((1n<<BigInt(b))-1n);summary.cyclic.push({blocks:b,privateMoves:pr.moves,projectedClauses:pr.Q.length})}
 return {seed:20811,summary,stats}
}
console.log(JSON.stringify(runBS11(),null,2));
