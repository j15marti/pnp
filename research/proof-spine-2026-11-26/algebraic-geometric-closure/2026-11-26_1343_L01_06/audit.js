const audit = function(){
 const out={smallGraphs:0,treeCompiles:0,coefficientChecks:0,rankChecks:0,rootClosureChecks:0,completeCutChecks:0,constructiveWitnessChecks:0,crossChecks:0,largeWitnessChecks:0,neighbors:0,failures:0,fields:[2,3,101],mode:"sequential reference enumeration, not hypothetical D"};
 const ck=(x,msg)=>{if(!x)throw Error(msg)};
 const seq=n=>Array.from({length:n},(_,i)=>i);
 const perms=a=>a.length===0?[[]]:a.flatMap((x,i)=>perms(a.filter((_,j)=>j!==i)).map(t=>[x,...t]));
 const cycle=w=>{let n=w.length;if(new Set(w).size!==n)return false;let seen=new Set(),i=0;while(!seen.has(i)){seen.add(i);i=w[i]}return i===0&&seen.size===n};
 const words=(n,k)=>k===0?[[]]:words(n,k-1).flatMap(a=>seq(n).map(j=>[...a,j]));
 const key=(a)=>a.join(",");
 const proj=(w,S)=>S.map(i=>w[i]);
 const mod=(x,p)=>(x%p+p)%p;
 const inv=(x,p)=>{for(let i=1;i<p;i++)if(mod(i*x,p)===1)return i;throw Error("zero pivot")};
 function eliminate(rows,p){let b=[],piv=[];for(let a of rows){let v=a.slice();for(let i=0;i<b.length;i++){let c=v[piv[i]];v=v.map((x,j)=>mod(x-c*b[i][j],p))}let j=v.findIndex(x=>x!==0);if(j>=0){let c=inv(v[j],p);b.push(v.map(x=>mod(x*c,p)));piv.push(j)}}return b.length}
 function coordinates(row,basis,p){let v=row.slice(),coeff=Array(basis.length).fill(0);for(let i=0;i<basis.length;i++){let c=v[basis[i].pivot];v=v.map((x,j)=>mod(x-c*basis[i].vec[j],p));coeff=coeff.map((x,j)=>mod(x+c*(basis[i].repr[j]||0),p))}return {v,coeff}}
 function tree(S,style){if(S.length===1)return {S};let i=style===0?Math.floor(S.length/2):1;return {S,L:tree(S.slice(0,i),style),R:tree(S.slice(i),style)}}
 function compile(node,n,W,p){
   let S=node.S,T=seq(n).filter(i=>!S.includes(i));
   let suffix=[...new Map(W.map(w=>[key(proj(w,T)),proj(w,T)])).values()];
   let full=new Set(W.map(key));
   const row=a=>suffix.map(z=>{let w=Array(n);S.forEach((i,j)=>w[i]=a[j]);T.forEach((i,j)=>w[i]=z[j]);return +full.has(key(w))});
   let L,R,candidates;
   if(node.L){L=compile(node.L,n,W,p);R=compile(node.R,n,W,p);candidates=L.B.flatMap(a=>R.B.map(b=>[...a,...b]))}else candidates=seq(n).map(x=>[x]);
   let B=[],basis=[];
   for(let a of candidates){let {v,coeff}=coordinates(row(a),basis,p),j=v.findIndex(x=>x!==0);if(j>=0){let c=inv(v[j],p);B.push(a);basis.push({pivot:j,vec:v.map(x=>mod(x*c,p)),repr:[...coeff.map(x=>mod(-x*c,p)),c]})}}
   let distinct=[...new Map(W.map(w=>[key(proj(w,S)),proj(w,S)])).values()];
   ck(eliminate(distinct.map(row),p)===B.length,"rank");out.rankChecks++;
   const maps=candidates.map(a=>{let {v,coeff}=coordinates(row(a),basis,p);ck(v.every(x=>!x),"span");return coeff});
   function state(w){if(!L)return maps[w[S[0]]]||[];let l=L.state(w),r=R.state(w),s=Array(B.length).fill(0);for(let i=0;i<l.length;i++)for(let j=0;j<r.length;j++){let c=mod(l[i]*r[j],p);for(let k=0;k<s.length;k++)s[k]=mod(s[k]+c*maps[i*r.length+j][k],p)}return s}
   return {B,state}
 }
 function runGraph(n,E){let W=perms(seq(n)).filter(w=>cycle(w)&&w.every((j,i)=>E.has(i*n+j)));let full=new Set(W.map(key));out.smallGraphs++;
 for(let i=0;i<n;i++)for(let j=0;j<n;j++){let supported=W.some(w=>w[i]===j),forced=W.length>0&&W.every(w=>w[i]===j);ck(!supported||E.has(i*n+j),"support");ck(!forced||supported,"forced");out.rootClosureChecks++}
 for(let p of out.fields)for(let style of [0,1]){let order=style===0?seq(n):seq(n).reverse();let C=compile(tree(order,style),n,W,p);out.treeCompiles++;for(let w of words(n,n)){let s=C.state(w);ck((s[0]||0)===+full.has(key(w)),"coefficient");out.coefficientChecks++}}
 }
 for(let n of [2,3,4]){let ed=seq(n*n).filter(x=>Math.floor(x/n)!==x%n),limit=n<4?2**ed.length:36;for(let m=0;m<limit;m++){let mask=n<4?m:m===0?0:m===1?2**ed.length-1:((m*2654435761)>>>0)%(2**ed.length);runGraph(n,new Set(ed.filter((_,j)=>(mask>>j)&1)))}}
 function make(n,S,T){let A=S.filter(x=>!T.includes(x)),B=T.filter(x=>!S.includes(x)),I=S.filter(x=>T.includes(x)),J=seq(n).filter(x=>!S.includes(x)&&!T.includes(x));ck(A.length===B.length&&A.length>0,"sets");let path=[];for(let i=0;i<A.length;i++){path.push(A[i]);if(i===0)path.push(...I);path.push(B[i]);if(i===0)path.push(...J)}let w=Array(n);path.forEach((x,i)=>w[x]=path[(i+1)%n]);return w}
 function sets(n,k){let a=[];for(let m=0;m<2**n;m++){let S=seq(n).filter(i=>(m>>i)&1);if(S.length===k)a.push(S)}return a}
 for(let n=2;n<=7;n++){for(let k=1;k<n;k++){let all=sets(n,k);for(let S of all){let W=all.filter(T=>key(T)!==key(S)).map(T=>({T,w:make(n,S,T)}));out.completeCutChecks++;for(let {T,w} of W){ck(cycle(w)&&key(proj(w,S).sort((a,b)=>a-b))===key(T),"image");out.constructiveWitnessChecks++}if(n<=6)for(let a of W)for(let b of W){let w=seq(n).map(i=>S.includes(i)?a.w[i]:b.w[i]);ck(cycle(w)===(key(a.T)===key(b.T)),"minor");out.crossChecks++}}}}
 for(let n of [16,32,64,128,256]){let k=Math.floor(n/3),S=seq(k),T=seq(k).map(i=>i+1),U=seq(k).map(i=>i+2);for(let target of [T,U]){let w=make(n,S,target);ck(cycle(w)&&key(proj(w,S).sort((a,b)=>a-b))===key(target),"large lift");out.largeWitnessChecks++;let E=new Set(w.map((j,i)=>i*n+j));E.delete(w[0]);ck(!seq(n).some(j=>E.has(j)),"NO empty row");out.neighbors++}let a=make(n,S,T),b=make(n,S,U),w=seq(n).map(i=>S.includes(i)?a[i]:b[i]);ck(!cycle(w),"large offdiagonal");out.crossChecks++}
 return out
};
console.log(JSON.stringify(audit(),null,2));
