function checkDO11(){
 const stats={assertions:0,smallWords:0,edgeChecks:0,matchingScans:0,closureScans:0,localHullWords:0};
 const assert=(p,m)=>{stats.assertions++;if(!p)throw Error(m)};
 const bit=(x,i)=>x[i];
 const mono=(x,e)=>e.every(v=>bit(x,v)===bit(x,e[0]));
 const valid=(x,E,skip=-1)=>{for(let i=0;i<E.length;i++){stats.edgeChecks++;if(i!==skip&&mono(x,E[i]))return false}return true};
 const words=n=>Array.from({length:2**n},(_,w)=>Array.from({length:n},(_,j)=>(w>>j)&1));
 const find=(n,E,pred,skip=-1)=>{for(const x of words(n)){stats.smallWords++;if(pred(x)&&valid(x,E,skip))return x}return null};
 const F={n:7,E:[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]]};
 const K5={n:5,E:[]};for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)for(let k=j+1;k<5;k++)K5.E.push([i,j,k]);
 function critical(G){assert(!find(G.n,G.E,()=>true),"root not UNSAT");return {...G,del:G.E.map((e,i)=>{let x=find(G.n,G.E,()=>true,i);assert(x&&mono(x,e),"not critical");return x})}}
 const f=critical(F),k5=critical(K5);
 function gadget(n,E){let legal=words(n).filter(x=>{stats.smallWords++;return valid(x,E)});assert(legal.length>0&&legal.every(x=>x[0]===x[1]),"not equality");let good=[0,1].map(b=>legal.find(x=>x[0]===b));assert(good.every(Boolean),"missing equal orientation");let bad=E.map((e,i)=>[0,1].map(b=>{let x=find(n,E,x=>x[0]===b&&x[1]!==b,i);assert(x&&mono(x,e),"missing deletion lift");return x}));return {n,E,good,bad,legal:legal.length}}
 const K=gadget(7,F.E.slice(1)); // ports 0,1; point 2 is private
 const D=gadget(5,[[0,2,3],[0,2,4],[0,3,4],[1,2,3],[1,2,4],[1,3,4]]);
 function expand(G,K,which){
   let n=G.n,E=G.E.map(e=>e.slice()),rec=[];
   for(const [i,j] of which){let a=G.E[i][j],b=n++;let map=[a,b];for(let t=2;t<K.n;t++)map.push(n++);E[i][j]=b;let start=E.length;for(const e of K.E)E.push(e.map(v=>map[v]));rec.push({i,j,a,b,map,start})}
   function lift(x,broken=null,local=-1){let y=Array(n).fill(0);x.forEach((b,i)=>y[i]=b);for(const R of rec){let z=R===broken?K.bad[local][x[R.a]]:K.good[x[R.a]];z.forEach((b,j)=>y[R.map[j]]=b)}return y}
   const locate=i=>rec.find(R=>i>=R.start&&i<R.start+K.E.length);
   function deleted(i,baseDel){if(i<G.E.length)return lift(baseDel[i]);const R=locate(i);assert(R,"missing origin");return lift(baseDel[R.i],R,i-R.start)}
   return {n,E,rec,lift,deleted}
 }
 const all=G=>G.E.flatMap((e,i)=>e.map((_,j)=>[i,j]));
 const ex=expand(D,K,all(D));
 const DK={n:ex.n,E:ex.E,good:D.good.map(x=>ex.lift(x)),bad:ex.E.map((e,i)=>[0,1].map(b=>ex.deleted(i,D.bad.map(q=>q[b]))))};
 for(const x of DK.good)assert(valid(x,DK.E)&&x[0]===x[1],"stretched good");
 for(let i=0;i<DK.E.length;i++)for(let b=0;b<2;b++){let x=DK.bad[i][b];assert(valid(x,DK.E,i)&&mono(x,DK.E[i])&&x[0]===b&&x[1]!==b,"stretched deletion")}
 function match(n,E,avoid=new Set()){let M=Array(n).fill(-1);function aug(i,seen){for(const v of E[i]){stats.matchingScans++;if(avoid.has(v)||seen.has(v))continue;seen.add(v);if(M[v]===-1||aug(M[v],seen)){M[v]=i;return true}}return false}let t=0;for(let i=0;i<E.length;i++)if(aug(i,new Set()))t++;return {t,M}}
 // Full affine hull on each individual scoped factor: enumerate legal local words.
 function rank(a){let B={};for(let x of a){while(x){let j=31-Math.clz32(x);if(B[j])x^=B[j];else{B[j]=x;break}}}return Object.keys(B).length}
 for(const ar of [3,4]){let L=[];for(let w=0;w<2**ar;w++){stats.localHullWords++;if(w!==0&&w!==2**ar-1)L.push(w)}assert(rank(L.map(x=>x^L[0]))===ar,"local affine hull")}
 function closure(G){for(const e of G.E){stats.closureScans++;assert(new Set(e).size===e.length&&e.length>=3&&e.length<=4,"not in stagnant closure domain")}}
 function testCritical(name,G,del,enumerate=false){closure(G);let rt=G.E.length-match(G.n,G.E).t;let min=Infinity,max=-Infinity,relax=0;for(let i=0;i<G.E.length;i++){let x=del(i);assert(valid(x,G.E,i)&&mono(x,G.E[i]),"critical witness "+name);for(let b=0;b<2;b++){let y=x[ G.E[i][0] ]===b?x:x.map(v=>v^1);assert(valid(y,G.E,i)&&G.E[i].every(v=>y[v]===b),"relaxed witness");relax++}let E=G.E.map((e,j)=>i===j?[...e,G.n]:e);closure({E});let d=E.length-match(G.n+1,E).t;min=Math.min(min,d);max=Math.max(max,d)}if(enumerate)assert(!find(G.n,G.E,()=>true),"enumeration root");return {name,n:G.n,m:G.E.length,excess:G.E.length-G.n,rootHallDeficit:rt,neighborMinHallDeficit:min,neighborMaxHallDeficit:max,verifiedOneBudgetWitnesses:relax,rootEvidence:enumerate?"enumerated":"exact compiler theorem"}}
 const out=[];
 out.push(testCritical("Fano",f,i=>f.del[i],true));
 out.push(testCritical("K5 triples",k5,i=>k5.del[i],true));
 for(const [name,G,W,which,brute] of [["Fano dense graft",f,D,[[0,0]],true],["Fano stretched dense graft",f,DK,[[0,0]],false],["K5 all Fano wires",k5,K,all(k5),false]]){let A=expand(G,W,which);let R=testCritical(name,A,i=>A.deleted(i,G.del),brute);out.push(R)}
 // Audit free-port theorem independently on all subsets of the four 3-edges on four vars.
 const T=[[0,1,2],[0,1,3],[0,2,3],[1,2,3]];
 let freeChecks=0,freeInstances=0;
 for(let mask=0;mask<16;mask++){let E=T.filter((e,i)=>(mask>>i)&1);let S=words(4).filter(x=>{stats.smallWords++;return valid(x,E)});if(!S.length)continue;for(let q=0;q<16;q++){let P=[0,1,2,3].filter(i=>(q>>i)&1);if(match(4,E,new Set(P)).t!==E.length)continue;freeInstances++;let projections=new Set(S.map(x=>P.map(i=>x[i]).join("")));assert(projections.size===2**P.length,"unmatched port projection");freeChecks+=2**P.length}}
 return {stats,gadgets:[{name:"Fano wire",n:K.n,m:K.E.length,models:K.legal},{name:"dense wire",n:D.n,m:D.E.length,models:D.legal},{name:"stretched dense wire",n:DK.n,m:DK.E.length}],controls:out,freeInstances,freeChecks};
}
console.log(JSON.stringify(checkDO11(),null,2));
