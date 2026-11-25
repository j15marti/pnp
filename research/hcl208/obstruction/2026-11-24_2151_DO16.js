function run(){
const stats={controls:0,sat:0,unsat:0,baseWords:0,baseNear:0,cnfNear:0,naeNear:0,sourceLifts:0,assertions:0,maxOwners:0,closureScans:0};
function ck(v){stats.assertions++;if(!v)throw Error("assertion "+stats.assertions);}
function val(l,w){return l>0?w[l]:1-w[-l]}
function bad(C,w,nae=false){let t=C.map(l=>val(l,w));return nae?t.every(x=>x===t[0]):!t.some(Boolean)}
function checkNear(F,w,i,nae=false){ck(F.every((C,j)=>bad(C,w,nae)===(j===i)))}
function base(F,n){
 let m=F.length,N=n+m,C=[],W=[];
 function emit(c,w){C.push(c);W.push(w)}
 function w0(){return Array(N+1).fill(0)}
 let s=i=>n+i+1, others=i=>Array.from({length:m},(_,j)=>j).filter(j=>j!==i).map(s);
 for(let i=0;i<m;i++){
  let w=w0();w[s(i)]=1;for(let l of F[i])w[Math.abs(l)]=+(l<0);
  emit([...F[i],...others(i)],w);
  for(let a=0;a<F[i].length;a++){
   w=w0();w[s(i)]=1;for(let b=0;b<a;b++)w[Math.abs(F[i][b])]=+(F[i][b]<0);w[Math.abs(F[i][a])]=+(F[i][a]>0);
   emit([-s(i),...others(i),...F[i].slice(0,a),-F[i][a]],w);
  }
 }
 for(let i=0;i<m;i++)for(let j=i+1;j<m;j++){let w=w0();w[s(i)]=w[s(j)]=1;emit([-s(i),-s(j)],w)}
 return {C,W,N};
}
function split(B){
 let N=B.N,C=[],groups=[];
 for(let L of B.C){
  let G=[],aux=[];
  if(L.length<=3){for(let k=L.length;k<3;k++)aux.push(++N);
   for(let mask=0;mask<2**aux.length;mask++)G.push([...L,...aux.map((v,j)=>mask>>j&1?-v:v)]);
  }else{for(let k=0;k<L.length-3;k++)aux.push(++N);
   G.push([L[0],L[1],aux[0]]);
   for(let k=1;k<aux.length;k++)G.push([-aux[k-1],L[k+1],aux[k]]);
   G.push([-aux.at(-1),...L.slice(-2)]);
  }
  groups.push({start:C.length,G,aux,L});C.push(...G);
 }
 function lift(w,target=-1,sub=-1){
  let u=Array(N+1).fill(0);w.forEach((b,i)=>u[i]=b);
  for(let [i,g] of groups.entries()){
   if(g.L.length<=3){if(i===target)g.aux.forEach((v,j)=>u[v]=sub>>j&1);}
   else g.aux.forEach((v,j)=>u[v]=i===target?+(j<sub):+g.L.slice(0,j+2).every(l=>!val(l,w)));
  }return u;
 }
 return {N,C,groups,lift};
}
function naeify(D){
 let r=D.N+1,N=r,C=[];
 for(let L of D.C){let z=++N;C.push([L[0],L[1],z],[-z,L[2],r])}
 function lift(w,target=-1,side=-1){
  let u=Array(N+1).fill(0);w.forEach((b,i)=>u[i]=b);
  for(let i=0;i<D.C.length;i++){let z=r+i+1;if(i===target){u[z]=side===0?0:1;continue}
   let found=false;for(let b=0;b<2;b++){u[z]=b;if(!bad(C[2*i],u,true)&&!bad(C[2*i+1],u,true)){found=true;break}}ck(found)
  }return u;
 }return {N,C,lift};
}
function words(n){return Array.from({length:2**n},(_,a)=>[0,...Array.from({length:n},(_,i)=>a>>i&1)])}
function control(F,n){
 let B=base(F,n),D=split(B),E=naeify(D);
 stats.controls++;let models=words(n).filter(w=>F.every(c=>!bad(c,w)));
 stats[models.length?"sat":"unsat"]++;
 if(B.N<=12)for(let w of words(B.N)){stats.baseWords++;ck(B.C.every(c=>!bad(c,w))===(w.slice(n+1).every(x=>!x)&&F.every(c=>!bad(c,w))))}
 for(let [i,w] of B.W.entries()){
  checkNear(B.C,w,i);stats.baseNear++;
  for(let [j] of D.groups[i].G.entries()){
   let ix=D.groups[i].start+j,u=D.lift(w,i,j);checkNear(D.C,u,ix);stats.cnfNear++;
   for(let side=0;side<2;side++){let v=E.lift(u,ix,side);checkNear(E.C,v,2*ix+side,true);stats.naeNear++}
  }
 }
 for(let w of models){let b=[...w,...Array(F.length).fill(0)],u=D.lift(b),v=E.lift(u);ck(E.C.every(c=>!bad(c,v,true)));stats.sourceLifts++}
 // Certified singleton hull check: each signed NAE triple has six allowed words, spanning F2^3.
 for(let C of E.C){ck(new Set(C.map(Math.abs)).size===3);let rows=words(3).filter(w=>!bad(C.map((l,i)=>l>0?i+1:-i-1),w,true));ck(rows.length===6);for(let mask=1;mask<8;mask++){let p=rows.map(w=>w.slice(1).reduce((s,b,i)=>s^(b*(mask>>i&1)),0));ck(p.includes(0)&&p.includes(1))}stats.closureScans++}
 stats.maxOwners=Math.max(stats.maxOwners,E.C.length);
}
control([[1],[-1]],1);control([[1,2],[-1,2]],2);control([[]],0);control([[1]],1);
let fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]];
let ff=fano.flatMap(c=>[c,c.map(l=>-l)]);control(ff,7);for(let i=0;i<3;i++)control(ff.filter((_,j)=>j!==i),7);
let seed=20261124;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
for(let i=0;i<24;i++){let n=3+rnd(2),m=1+rnd(5),F=[];for(let j=0;j<m;j++){let q=Array.from({length:n},(_,a)=>a+1);let c=[];for(let a=0;a<1+rnd(3)&&q.length;a++){let l=q.splice(rnd(q.length),1)[0];c.push(rnd(2)?l:-l)}F.push(c)}control(F,n)}
return stats;
}
console.log(JSON.stringify(run(),null,2));
