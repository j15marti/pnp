function audit(){
"use strict";
let seed=20261125>>>0;const rnd=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
let checks=0;function ck(x,msg){checks++;if(!x)throw Error(msg)}
const bit=i=>1n<<BigInt(i);function par(x){let v=0;while(x){x&=x-1n;v^=1}return v}
const ids=n=>Array.from({length:n},(_,i)=>i);
function rows(A,d){return A.map((r,i)=>r.reduce((m,x,j)=>x?m|bit(j):m,0n)|(d[i]?bit(i):0n))}
function valid(M,p,h=0){return M.every((r,i)=>!(p&bit(i))||par(r&p)===h)}
function sig(cols,p){let g=0;cols.forEach((c,i)=>{if(p&bit(i))g^=c});return g}
function closure(M,cols,q,target){
 const n=M.length,B=Array(n).fill(null);let contradiction=false,adds=0;
 function red(x,c){for(let i=n-1;i>=0;i--)if((x&bit(i))&&B[i]){x^=B[i][0];c^=B[i][1]}return [x,c]}
 function add(x,c){[x,c]=red(x,c);if(!x){if(c)contradiction=true;return false}let i=x.toString(2).length-1;B[i]=[x,c];adds++;return true}
 for(let j=0;j<q;j++)add(cols.reduce((r,c,i)=>c&(1<<j)?r|bit(i):r,0n),(target>>j)&1);
 let change=true;while(change&&!contradiction){change=false;for(let i=0;i<n;i++){let [a,c]=red(bit(i),0),[b,e]=red(M[i],0);if(!a&&!c||!b&&!e)continue;if(!a&&c)change=add(b,e)||change;else if(!b&&e)change=add(a,c)||change;else if(a===b&&c===e)change=add(a,c)||change;if(contradiction)break}}
 return {contradiction,adds,pins:ids(n).map(i=>{const [a,c]=red(bit(i),0);return a?-1:c})};
}
function decompose(A){
 let tested=0,width=0;
 function rec(V){
  if(V.length===1)return {v:V[0],rep:V[0]};
  let mod=null;
  outer:for(let i=0;i<V.length;i++)for(let j=i+1;j<V.length;j++){
   tested++;let u=V[i],S=[u,V[j]],seen=new Set(S);
   for(let k=1;k<S.length&&S.length<V.length;k++){
    let v=S[k];for(const x of V)if(!seen.has(x)&&(A[x][u]!==A[x][v]||A[u][x]!==A[v][x])){seen.add(x);S.push(x)}
   }
   if(S.length<V.length){mod=S;break outer}
  }
  if(!mod){width=Math.max(width,V.length);return {children:V.map(v=>({v,rep:v})),Q:V.map(u=>V.map(v=>A[u][v])),rep:V[0]}}
  const S=new Set(mod),r=mod[0],inside=rec(mod),outside=rec(V.filter(v=>!S.has(v)||v===r));
  function replace(t){if(t.v!==undefined)return t.v===r?inside:t;return {...t,children:t.children.map(replace)}}
  return replace(outside)
 }
 let tree=rec(ids(A.length));return {tree,width,tested}
}
function verifyTree(A,t){
 if(t.v!==undefined)return [t.v];
 const S=t.children.map(c=>verifyTree(A,c));for(let i=0;i<S.length;i++)for(let j=0;j<S.length;j++)if(i!==j)for(const u of S[i])for(const v of S[j])ck(A[u][v]===t.Q[i][j],"bad module quotient");
 return S.flat()
}
function tables(t,d,cols,q,pins,stats){
 const size=1<<q;
 if(t.v!==undefined){const i=t.v;return [0,1].map(h=>{let m=new Map();for(let x=0;x<2;x++)if((pins[i]===-1||pins[i]===x)&&(!x||d[i]===h))m.set(x*size+(x?cols[i]:0),x?bit(i):0n);return m})}
 const kids=t.children.map(c=>tables(c,d,cols,q,pins,stats)),k=kids.length;
 if(k>20)throw Error("cap");
 const out=[new Map(),new Map()];
 for(let h=0;h<2;h++)for(let s=0;s<(1<<k);s++){stats.modes++;let dp=new Map([[0,0n]]);for(let i=0;i<k&&dp.size;i++){
  let h2=h;for(let j=0;j<k;j++)if(t.Q[i][j]&&(s&(1<<j)))h2^=1;
  const si=(s>>i)&1, next=new Map();
  for(const [key,p] of kids[i][h2])if(Math.floor(key/size)===si)for(const [g,w] of dp){stats.joins++;next.set(g^(key%size),w|p)}
  dp=next
 }let ps=par(BigInt(s));for(const [g,w]of dp)out[h].set(ps*size+g,w)}
 return out;
}
function solve(A,d,cols,q,target,cap=12){const M=rows(A,d),c=closure(M,cols,q,target);if(c.contradiction)return {label:"NO",closure:true};const dec=decompose(A);if(dec.width>cap)return {label:"UNKNOWN",width:dec.width};const stats={modes:0,joins:0};const T=tables(dec.tree,d,cols,q,c.pins,stats)[0],size=1<<q;for(let s=0;s<2;s++)if(T.has(s*size+target)){const p=T.get(s*size+target);ck(valid(M,p)&&sig(cols,p)===target,"bad lift");return {label:"YES",p,width:dec.width,...stats}}return {label:"NO",width:dec.width,...stats}}
function cycle(n){return ids(n).map(i=>ids(n).map(j=>+((i+1)%n===j)))}
function subst(Q,As){const lab=As.flatMap((A,i)=>ids(A.length).map(j=>[i,j]));return lab.map(([i,u])=>lab.map(([j,v])=>i===j?As[i][u][v]:Q[i][j]))}
function randomA(n){return ids(n).map(i=>ids(n).map(j=>i===j?0:+(rnd()<.5)))}
function randTree(n){if(n<=2||rnd()<.25)return randomA(n);const a=1+Math.floor(rnd()*(n-1));return subst(randomA(2),[randTree(a),randTree(n-a)])}
let small={roots:0,tableComparisons:0,witnessChecks:0,guardDecisions:0,yes:0,no:0,closureDeductions:0};
for(let z=0;z<240;z++){
 const n=2+Math.floor(rnd()*9),A=z%2?randTree(n):randomA(n),d=ids(n).map(()=>+(rnd()<.5)),q=1+Math.floor(rnd()*3),cols=ids(n).map(()=>Math.floor(rnd()*(1<<q))),M=rows(A,d),dec=decompose(A),stats={modes:0,joins:0};
 ck(new Set(verifyTree(A,dec.tree)).size===n,"bad leaves");const T=tables(dec.tree,d,cols,q,ids(n).map(()=>-1),stats),ref=[new Set(),new Set()];
 for(let p=0;p<(1<<n);p++)for(let h=0;h<2;h++)if(valid(M,BigInt(p),h))ref[h].add(par(BigInt(p))*(1<<q)+sig(cols,BigInt(p)));
 for(let h=0;h<2;h++)for(let k=0;k<(2<<q);k++){small.tableComparisons++;ck(T[h].has(k)===ref[h].has(k),"table mismatch");if(T[h].has(k)){const p=T[h].get(k);small.witnessChecks++;ck(valid(M,p,h)&&par(p)*(1<<q)+sig(cols,p)===k,"table lift")}}
 for(let t=0;t<(1<<q);t++){const want=ref[0].has(t)||ref[0].has((1<<q)+t),c=closure(M,cols,q,t),ans=solve(A,d,cols,q,t);small.guardDecisions++;small.closureDeductions+=c.adds;ck(ans.label===(want?"YES":"NO"),"guard mismatch");small[want?"yes":"no"]++}
 small.roots++
}
function atom(){const U=[[15,32,47],[13,17,28],[14,36,42],[11,53,62],[10,39,45]];let sums=new Set([0]);for(const g of U)sums=new Set([...sums].flatMap(s=>g.map(x=>x^s)));ck(sums.size===63&&!sums.has(29),"atom");
 let E=null,map=null;for(let z=0;z<243&&!E;z++){let t=z,es=U.map(g=>{let e=g[t%3];t=Math.floor(t/3);return e}),m=new Map();for(let s=0;s<32;s++){let v=0;for(let i=0;i<5;i++)if(s&(1<<i))v^=es[i];m.set(v,s)}if(m.size===32){E=es;map=m}}
 let w=ids(64).find(x=>!map.has(x));for(const [v,s]of [...map])map.set(v^w,s|32);
 const f=U.map((g,i)=>g.find(x=>x!==E[i]));const base=f.reduce((x,y)=>x^y,0);let count=0,yes=0,no=0,widths=new Set();
 for(let t=0;t<64;t++){let c=map.get(t^base);if(!(c&32)){ck(sums.has(t),"hyperplane");yes++;continue}let ff=f.map((x,i)=>c&(1<<i)?x^E[i]:x);let C=ff.map(x=>map.get(x)),A=ids(5).map(i=>ids(5).map(j=>i===j?0:(C[j]>>i)&1)),d=ids(5).map(i=>1^((C[i]>>i)&1)),b=C.map(x=>x>>5),res=solve(A,d,b,1,1);ck(res.label===(sums.has(t)?"YES":"NO"),"atom chart");widths.add(res.width??0);count++;if(sums.has(t))yes++;else no++}
 return {missing:29,allSyndromes:64,repairChartChecks:count,yes,no,widths:[...widths]}
}
let family=[],A=cycle(4);for(let level=1;level<=4;level++){const n=A.length,d=ids(n).map(()=>1),b=d.slice(),dec=decompose(A);ck(dec.width<=4,"lex width");ck(new Set(verifyTree(A,dec.tree)).size===n,"lex tree");const no=solve(A,d,b,1,1,4);d[0]=0;const yes=solve(A,d,b,1,1,4);ck(no.label==="NO"&&yes.label==="YES","lex neighbor");for(let s=0;s<n;s+=4){const r=s,c=s+1,j=s+2;ck((A[r][j]^A[c][j])===1,"rank diagonal");for(let t=0;t<n;t+=4)if(t!==s)ck((A[r][t+2]^A[c][t+2])===0,"rank offdiag")}
 family.push({level,n,width:dec.width,pairClosureTests:dec.tested,completionRankLower:n/4,no:no.label,yes:yes.label,noModes:no.modes,yesModes:yes.modes});if(level<4)A=subst(cycle(4),[A,A,A,A])
}
let barriers=[];for(const n of [12,31,48]){let A=cycle(n),dec=decompose(A);ck(dec.width===n,"cycle prime");let res=solve(A,ids(n).map(()=>1),ids(n).map(()=>1),1,1,8);ck(res.label==="UNKNOWN","cap");barriers.push({kind:"directed cycle",n,width:dec.width,capped:res.label,cycleTerminal:n%2?"YES":"NO"})}
for(const n of [16,32]){let A=cycle(n),perm=ids(n);for(let i=n-1;i>0;i--){let j=Math.floor(rnd()*(i+1));[perm[i],perm[j]]=[perm[j],perm[i]]}for(let i=0;i<n;i++)A[perm[i]][perm[(i+1)%n]]=1;let dec=decompose(A);barriers.push({kind:"union of two directed cycles (no expansion certificate)",n,width:dec.width,capped:solve(A,ids(n).map(()=>1),ids(n).map(()=>1),1,1,8).label})}
return {seedInitial:20261125,checks,small,atom:atom(),family,barriers,checksAfterAtom:checks};
}
console.log(JSON.stringify(audit(), null, 2));
