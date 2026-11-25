// BH11 checker, Node.js >=18
function main(){
const S={checks:0,closureScans:0,merges:0,matchingScans:0,matchedCalls:0,cycleScans:0,cycleCaps:0,truthWords:0,portQueries:0,cutTrials:0,projections:0,sourceChecks:0,rootCalls:0,peakRegion:0};
const ck=(p,m)=>{S.checks++;if(!p)throw Error(m)};
const vars=F=>[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b);
const sg=l=>+(l<0), val=(l,w)=>(w.get(Math.abs(l))??0)^sg(l);
const legal=(F,w)=>F.every(e=>{S.sourceChecks++;return e.some(l=>val(l,w)!==val(e[0],w))});
const parity=(a,b,p)=>[a,p?b:-b];
const close=F=>{
 let E=F.map(e=>e.slice()),rec=[];
 while(true){
  let out=[],pair=null;
  for(let e of E){S.closureScans++;let q=[...new Set(e)];if(q.some(l=>q.includes(-l)))continue;if(q.length<2)return null;
   if(q.length===2&&!pair)pair=q;else out.push(q);
  }
  if(!pair)return {E:out,rec};
  let [a,b]=pair, u=Math.abs(a),v=Math.abs(b),p=1^sg(a)^sg(b);
  if(u>v)[u,v]=[v,u];
  rec.push([v,u,p]);S.merges++;
  E=out.map(e=>e.map(l=>Math.abs(l)===v?((sg(l)^p)?-u:u):l));
 }
};
const back=(w,rec)=>{for(let j=rec.length-1;j>=0;j--){let [v,u,p]=rec[j];w.set(v,(w.get(u)??0)^p)}return w};
const brute=(F,V)=>{for(let t=0;t<2**V.length;t++){S.truthWords++;let w=new Map(V.map((v,i)=>[v,(t>>i)&1]));if(legal(F,w))return w}return null};
const match=(E)=>{
 let M=new Map();
 const aug=(i,seen)=>{for(let l of E[i]){S.matchingScans++;let v=Math.abs(l);if(seen.has(v))continue;seen.add(v);if(!M.has(v)||aug(M.get(v),seen)){M.set(v,i);return true}}return false};
 for(let i=0;i<E.length;i++)if(!aug(i,new Set()))return null;
 return M;
};
// Exact on completed calls. Capped simple-cycle DFS, NOT polynomial RST backend.
const graphSolve=(E,V)=>{
 S.matchedCalls++;let M=match(E);if(!M)return undefined;
 let A=new Map(V.map(v=>[v,[]])),R=new Map(V.map(v=>[v,[]]));
 for(let [v,i] of M){let pivot=E[i].find(l=>Math.abs(l)===v);for(let l of E[i])if(Math.abs(l)!==v){let u=Math.abs(l),p=1^sg(l)^sg(pivot);A.get(v).push([u,p]);R.get(u).push([v,p])}}
 let seen=new Set(),order=[];
 const dfs=v=>{seen.add(v);for(let [u] of A.get(v))if(!seen.has(u))dfs(u);order.push(v)};
 for(let v of V)if(!seen.has(v))dfs(v);
 let comp=new Map(),C=[];
 const rev=(v,k)=>{comp.set(v,k);C[k].push(v);for(let [u] of R.get(v))if(!comp.has(u))rev(u,k)};
 for(let v of order.reverse())if(!comp.has(v)){C.push([]);rev(v,C.length-1)}
 let w=new Map(),budget=200000;
 for(let i=0;i<C.length;i++){
  if(C[i].some(v=>A.get(v).some(([u])=>comp.get(u)!==i)))continue;
  let free=C[i].find(v=>!M.has(v));if(free!==undefined){w.set(free,0);continue}
  let cycle=null,abort=false;
  for(let start of C[i]){
   let vis=new Set([start]),path=[];
   const search=(v,p)=>{for(let [u,q] of A.get(v)){S.cycleScans++;if(--budget<0){abort=true;return false}if(comp.get(u)!==i)continue;
    if(u===start){if((p^q)===0){cycle=[...path,[v,u,q]];return true}continue}
    if(vis.has(u)||u<start)continue;vis.add(u);path.push([v,u,q]);if(search(u,p^q))return true;path.pop();vis.delete(u);if(abort)return false}
    return false};
   if(search(start,0)||abort)break;
  }
  if(abort){S.cycleCaps++;return undefined}if(!cycle)return null;
  w.set(cycle[0][0],0);for(let [v,u,p] of cycle)w.set(u,w.get(v)^p);
 }
 let Q=[...w.keys()];for(let k=0;k<Q.length;k++){let v=Q[k];for(let [u,p] of R.get(v))if(!w.has(u)){w.set(u,w.get(v)^p);Q.push(u)}}
 ck(V.every(v=>w.has(v))&&legal(E,w),"graph lift");return w;
};
const query=(F,extra=[],cap=9)=>{
 let all=[...F,...extra],V=vars(all),c=close(all);if(!c)return null;
 let w=graphSolve(c.E,vars(c.E));if(w===undefined&&V.length<=cap)w=brute(all,V);
 else if(w instanceof Map){back(w,c.rec);for(let v of V)if(!w.has(v))w.set(v,0)}
 if(w instanceof Map)ck(legal(all,w),"query source");return w;
};
const two=(F,a,b,cap=9)=>{let W=[];for(let p=0;p<2;p++){S.portQueries++;let w=query(F,[parity(a,b,p)],cap);if(w===undefined)return undefined;W.push(w)}return W};
const three=(F,P,cap=9)=>{
 let pairs=[[0,1],[0,2],[1,2]],T=pairs.map(([i,j])=>two(F,P[i],P[j],cap));
 if(T.some(t=>t===undefined))return undefined;
 let candidates=[0,1,2,3].filter(k=>{let b=[0,k&1,k>>1];return pairs.every(([i,j],h)=>T[h][b[i]^b[j]]!==null)});
 let W=Array(4).fill(null);
 if(candidates.length<=2){
  for(let k of candidates){let b=[0,k&1,k>>1];let h=pairs.findIndex(([i,j])=>candidates.every(l=>l===k||(([0,l&1,l>>1][i]^[0,l&1,l>>1][j])!==(b[i]^b[j]))));
   ck(h>=0,"separating parity");let [i,j]=pairs[h];W[k]=T[h][b[i]^b[j]];
  }
 }else for(let k of candidates){S.portQueries++;let w=query(F,[parity(P[0],P[1],k&1),parity(P[0],P[2],k>>1)],cap);if(w===undefined)return undefined;W[k]=w}
 for(let k=0;k<4;k++)if(W[k])ck(((W[k].get(P[0])^W[k].get(P[1]))===(k&1))&&((W[k].get(P[0])^W[k].get(P[2]))===(k>>1))&&legal(F,W[k]),"three lift");
 return W;
};
const peel=(F)=>{
 let E=F.map(e=>e.slice()),rec=[],total=0;
 for(;;){
  let c=close(E);if(!c)return {label:"UNSAT",projections:total};
  E=c.E;for(let r of c.rec)rec.push({merge:r});
  S.rootCalls++;
  let root=query(E,[],9);
  if(root!==undefined){
   if(root===null)return {label:"UNSAT",projections:total};
   for(let j=rec.length-1;j>=0;j--){let t=rec[j];if(t.merge)back(root,[t.merge]);else{
     let p=(root.get(t.a)??0)^(root.get(t.b)??0),w=t.W[p];ck(w!==null,"retained parity");
     let flip=(root.get(t.a)??0)^(w.get(t.a)??0);
     for(let v of t.C)root.set(v,(w.get(v)??0)^flip);
     root.set(t.a,root.get(t.a)??0);root.set(t.b,root.get(t.b)??0);
   }}
   ck(legal(F,root),"peel lift");return {label:"SAT",w:root,projections:total}
  }
  let V=vars(E),A=new Map(V.map(v=>[v,new Set()]));
  for(let e of E)for(let l of e)for(let k of e)if(Math.abs(l)!==Math.abs(k))A.get(Math.abs(l)).add(Math.abs(k));
  let pairs=new Map();
  const add=(a,b)=>{if(a>b)[a,b]=[b,a];pairs.set(a+","+b,[a,b])};
  for(let v of V){let ns=[...A.get(v)];for(let i=0;i<ns.length;i++)for(let j=i+1;j<ns.length;j++)add(ns[i],ns[j])}
  for(let i=0;i<V.length;i++)for(let j=i+1;j<V.length;j++)add(V[i],V[j]);
  let chosen=null;
  outer:for(let [a,b] of pairs.values()){
   S.cutTrials++;let seen=new Set([a,b]),comps=[];
   for(let v of V)if(!seen.has(v)){let Q=[v];seen.add(v);for(let i=0;i<Q.length;i++)for(let u of A.get(Q[i]))if(!seen.has(u)){seen.add(u);Q.push(u)}comps.push(Q)}
   if(comps.length<2)continue;
   comps.sort((x,y)=>x.length-y.length);
   for(let C of comps){
    if(!C.some(v=>A.get(v).has(a))||!C.some(v=>A.get(v).has(b)))continue;
    let cs=new Set(C),inside=E.filter(e=>e.some(l=>cs.has(Math.abs(l))));
    S.peakRegion=Math.max(S.peakRegion,C.length);
    let W=two(inside,a,b);if(W===undefined)continue;if(W.every(w=>w===null))return {label:"UNSAT",projections:total};
    chosen={a,b,C,W,cs};break outer;
   }
  }
  if(!chosen)return {label:"UNKNOWN",projections:total};
  let {a,b,C,W,cs}=chosen;E=E.filter(e=>!e.some(l=>cs.has(Math.abs(l))));
  if(W[0]===null||W[1]===null)E.push(parity(a,b,W[0]===null?1:0));
  rec.push({a,b,C,W});S.projections++;total++;
 }
};
const Fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]];
const fresh=(obj)=>++obj.n;
const wire=(a,b,obj)=>{let p=fresh(obj),v=[a,b,p,...Array.from({length:4},()=>fresh(obj))];return Fano.slice(1).map(e=>e.map(x=>v[x-1]))};
const chain=(k)=>{let obj={n:2},a=1,E=[];for(let i=0;i<k;i++){let b=i===k-1?2:fresh(obj);E.push(...wire(a,b,obj));a=b}return E};
const twoChains=(k)=>{let obj={n:3},E=[];for(let last of [2,3]){let a=1;for(let i=0;i<k;i++){let b=i===k-1?last:fresh(obj);E.push(...wire(a,b,obj));a=b}}return {E,root:[...E,[1,2,3]],n:obj.n}};
const dense=(a,b,p,q,r)=>[a,b].flatMap(v=>[[v,p,q],[v,p,r],[v,q,r]]);
const graft=(stretch)=>{let E=Fano.map(e=>e.slice());E[0][0]=8;let D=dense(1,8,9,10,11),obj={n:11};if(!stretch)return [...E,...D];
 for(let e of D){let t=[];for(let v of e){let u=fresh(obj);t.push(u);E.push(...wire(v,u,obj))}E.push(t)}return E};
let seed=20811;const rng=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/2**32};
const relabel=F=>{let V=vars(F),P=V.slice();for(let i=P.length-1;i>0;i--){let j=Math.floor(rng()*(i+1));[P[i],P[j]]=[P[j],P[i]]}let M=new Map(V.map((v,i)=>[v,P[i]]));return F.map(e=>e.map(l=>sg(l)?-M.get(-l):M.get(l)))};
const rows=[],neighbors=[];
const control=(name,F,expected,indices)=>{
 F=relabel(F);let ans=peel(F);ck(ans.label===expected,name+" root "+ans.label);rows.push({name,n:vars(F).length,m:F.length,root:ans.label,projections:ans.projections});
 let stats={name,ownerSAT:0,maxProjections:0};
 for(let i of indices){let E=F.filter((_,j)=>j!==i),r=peel(E);ck(r.label==="SAT",name+" deleted "+i+" "+r.label);stats.maxProjections=Math.max(stats.maxProjections,r.projections);
  for(let b=0;b<2;b++){let w=new Map(r.w);let e=F[i];if(e.every(l=>val(l,w)===b))for(let v of vars(F))w.set(v,(w.get(v)??0)^1);
   ck(legal(E,w)&&!e.every(l=>val(l,w)===b),"one-sided orientation");stats.ownerSAT++}
 }neighbors.push(stats);
};
control("Fano",Fano,"UNSAT",[0,1,2,3,4,5,6]);
const c4=twoChains(4);control("DO02 49",c4.root,"UNSAT",c4.root.map((_,i)=>i));
const D=graft(false);control("DO11 dense graft",D,"UNSAT",D.map((_,i)=>i));
const D2=graft(true);control("DO11 stretched dense graft",D2,"UNSAT",[0,1,6,7,12,30,60,90,120]);
const boundary=[];
for(let k of [1,2,4,8,16,32]){
 let F=chain(k),W=two(F,1,2,0);boundary.push({kind:"two",k,n:vars(F).length,m:F.length,support:W?.map(Boolean)??"UNKNOWN"});if(W)ck(W[0]&&W[1]===null,"wire chain");
 let G=twoChains(k);let T=three(G.E,[1,2,3],0);boundary.push({kind:"three",k,n:G.n,m:G.E.length,support:T?.map(Boolean)??"UNKNOWN"});if(T)ck(T[0]&&T.slice(1).every(w=>w===null),"three wire");
}
let random={two:0,three:0,unknown:0,exact:0};
for(let i=0;i<120;i++){
 let n=3+Math.floor(rng()*5),F=[];
 for(let j=0,m=1+Math.floor(rng()*11);j<m;j++){let e=[];while(e.length<3){let v=1+Math.floor(rng()*n);if(!e.some(l=>Math.abs(l)===v))e.push(rng()<.5?v:-v)}F.push(e)}
 let t=two(F,1,2),u=three(F,[1,2,3]);let R=[0,0,0,0];for(let w=0;w<2**n;w++){let a=new Map(Array.from({length:n},(_,j)=>[j+1,(w>>j)&1]));if(legal(F,a))R[(a.get(1)^a.get(2))+2*(a.get(1)^a.get(3))]=1}
 ck(t!==undefined&&u!==undefined,"small query complete");for(let k=0;k<4;k++)ck(!!u[k]===!!R[k],"three reference");
 for(let p=0;p<2;p++)ck(!!t[p]===!!(R[p]||R[p+2]),"two reference");random.two++;random.three++;random.exact++;
}
const X=[[1,2,3]], Y=[[1,2,3],[1,2,-3]];
const R=three(X,[1,2,3]),Q=three(Y,[1,2,3]);
ck(R.map(Boolean).join(",")==="false,true,true,true","three nonaffine");
ck(Q.map(Boolean).join(",")==="false,true,false,true","two support");
return {seed:20811,rows,neighbors,boundary,random,ledger:S};
}
console.log(JSON.stringify(main(),null,2));
