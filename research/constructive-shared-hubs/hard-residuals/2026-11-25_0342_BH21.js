// Reproduce with node checker.js RT26_results.json MS28_results.json
const fs=require('fs');
function run(rt,ms){
 let checks=0, dpTransitions=0, referenceWords=0, scans=0, joins=0, packChecks=0;
 function ck(x){checks++;if(!x)throw Error("assertion "+checks)}
 function par(x){let a=0;while(x){a^=1;x&=x-1}return a}
 function energy(n,reg){let C=reg.length,J=Array.from({length:n},()=>Array(n).fill(0));for(let {t,bad} of reg)for(let a=0;a<3;a++)for(let b=a+1;b<3;b++){let u=t[a],v=t[b],j=((bad[0]>>a^bad[0]>>b)&1)?-1:1;J[u][v]+=j;J[v][u]+=j}return {C,J}}
 function val(E,s){let e=E.C;for(let i=0;i<s.length;i++)for(let j=i+1;j<s.length;j++)e+=E.J[i][j]*s[i]*s[j];return e}
 function src(reg,s){let c=0;for(let {t,bad} of reg){let z=t.reduce((a,v,i)=>a+((s[v]<0?1:0)<<i),0);if(bad.includes(z))c++}return 4*c}
 function ref(n,reg){let best=Infinity,count=0;for(let w=0;w<2**n;w++){referenceWords++;let e=src(reg,Array.from({length:n},(_,i)=>w>>i&1?-1:1));if(e<best){best=e;count=1}else if(e===best)count++}return {best,count}}
 function quotient(n,reg,cut=[]){
  let p=Array.from({length:n},(_,i)=>i),d=Array(n).fill(0);
  function f(i){if(p[i]===i)return [i,0];let [r,b]=f(p[i]);return [r,b^d[i]]}
  function join(u,v,b){let [r,x]=f(u),[s,y]=f(v);if(r===s)return (x^y)===b?0:-1;p[r]=s;d[r]=x^y^b;joins++;return 1}
  for(let [mask,b] of cut){let a=[];for(let i=0;i<n;i++)if(mask>>i&1)a.push(i);ck(a.length===2);if(join(a[0],a[1],b)<0)return null}
  while(true){let changed=false;for(let {t,bad} of reg){scans++;let q=t.map(f),rs=[...new Set(q.map(x=>x[0]))];let legal=[];for(let w=0;w<2**rs.length;w++){let v=q.reduce((a,[r,b],i)=>a+(((w>>rs.indexOf(r)&1)^b)<<i),0);if(!bad.includes(v))legal.push(w)}if(!legal.length)return null;for(let i=0;i<rs.length;i++)for(let j=i+1;j<rs.length;j++){let vals=new Set(legal.map(w=>(w>>i^w>>j)&1));if(vals.size===1){let z=join(rs[i],rs[j],[...vals][0]);if(z<0)return null;if(z>0)changed=true}}if(changed)break}if(!changed)break}
  let roots=[...new Set(p.map((_,i)=>f(i)[0]))], map=p.map((_,i)=>{let [r,b]=f(i);return [roots.indexOf(r),b?-1:1]});
  let old=energy(n,reg),C=old.C,J=Array.from({length:roots.length},()=>Array(roots.length).fill(0));
  for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){let [a,x]=map[i],[b,y]=map[j],k=old.J[i][j]*x*y;if(a===b)C+=k;else {J[a][b]+=k;J[b][a]+=k}}
  return {C,J,map,lift:s=>map.map(([i,b])=>s[i]*b)}
 }
 function solve(E,cap=8){
  let n=E.J.length;
  for(let beta of [0,1,-1]){
   let visited=new Set(),groups=[];
   for(let i=0;i<n;i++)if(!visited.has(i)){let g=[i];visited.add(i);for(let a=0;a<g.length;a++)for(let j=0;j<n;j++)if(j!==g[a]&&!visited.has(j)&&E.J[g[a]][j]!==beta){visited.add(j);g.push(j)}groups.push(g)}
   let rows=[],ok=true;
   for(let g of groups){let j0=g.length>1?E.J[g[0]][g[1]]-beta:0,uniform=g.every((u,i)=>g.slice(i+1).every(v=>E.J[u][v]-beta===j0));let R=new Map();
    if(uniform){for(let k=0;k<=g.length;k++){let t=g.length-2*k;R.set(t,{cost:j0*(t*t-g.length)/2,s:g.map((_,i)=>i<k?-1:1)})}}
    else if(g.length<=cap){for(let w=0;w<2**g.length;w++){let s=g.map((_,i)=>w>>i&1?-1:1),t=s.reduce((a,b)=>a+b,0),cost=0;for(let i=0;i<g.length;i++)for(let j=i+1;j<g.length;j++)cost+=(E.J[g[i]][g[j]]-beta)*s[i]*s[j];if(!R.has(t)||cost<R.get(t).cost)R.set(t,{cost,s})}}
    else{ok=false;break}rows.push(R)
   }
   if(!ok)continue;
   let D=new Map([[0,{cost:0,parts:[]}]]);
   for(let R of rows){let F=new Map();for(let [a,v] of D)for(let [b,w] of R){dpTransitions++;let cost=v.cost+w.cost,t=a+b;if(!F.has(t)||cost<F.get(t).cost)F.set(t,{cost,parts:[...v.parts,w.s]})}D=F}
   let best=Infinity,s=null;for(let [t,v] of D){let e=E.C+v.cost+beta*(t*t-n)/2;if(e<best){best=e;s=Array(n);groups.forEach((g,i)=>g.forEach((u,j)=>s[u]=v.parts[i][j]))}}ck(val(E,s)===best);return {best,s,beta,groups:groups.map(g=>g.length)}
  }return null
 }
 function replayPack(E,c){
  let w=new Map(), pref=new Map(),B=E.C,load=new Map();for(let i=0;i<E.J.length;i++)for(let j=i+1;j<E.J.length;j++)if(E.J[i][j]){let m=(1<<i)|(1<<j),v=E.J[i][j];w.set(m,2*Math.abs(v));pref.set(m,v>0?1:0);B-=Math.abs(v)}
  ck(B===c.B);let total=0;for(let [str,a] of c.pack){let m=str.split(" ").map(x=>parseInt(x,16));ck(m.every(x=>w.has(x))&&new Set(m).size===m.length);ck(m.reduce((a,b)=>a^b,0)===0&&m.reduce((a,b)=>a^pref.get(b),0)===1&&a>=0);total+=a;for(let x of m)load.set(x,(load.get(x)||0)+a);packChecks++}
  for(let [m,v] of w)ck((load.get(m)||0)<=v*c.denom);
  let lower=B*c.denom+total;ck(lower===c.lowerNumerator);let cuts=[];if(lower===0)for(let [m,v] of w)if((load.get(m)||0)<v*c.denom)cuts.push([m,pref.get(m)]);
  return {lower,denom:c.denom,cuts}
 }
 let rtout=[];
 for(let {n,registry} of rt.controls)for(let neighbor of [false,true]){
  let reg=registry.map((e,i)=>({...e,bad:e.bad.map(x=>x^(neighbor&&i===0?1:0))}));let r=ref(n,reg),E=energy(n,reg),raw=quotient(n,reg),a=raw?solve(raw):{best:4},cert=ms.out.find(x=>x.n===n&&x.neighbor===neighbor&&x.mode==="raw"),pack=replayPack(E,cert),b=null;
  if(pack.lower>0){ck(r.best>0);b={status:"UNSAT-packed"}}
  else if(pack.lower===0){let Q=quotient(n,reg,pack.cuts);if(!Q){ck(r.best>0);b={status:"UNSAT-closure"}}else {let z=solve(Q);if(z){let s=Q.lift(z.s);ck(src(reg,s)===z.best);ck(z.best===r.best);b={status:z.best===0?"SAT":"UNSAT",best:z.best,dimension:Q.J.length,beta:z.beta,groups:z.groups,witness:s.map(v=>v===-1?1:0).join("")}}else b={status:"DECLINE",dimension:Q.J.length}}}
  if(a){ck((a.best===0)===(r.best===0));if(a.s)ck(src(reg,raw.lift(a.s))===a.best)}
  rtout.push({n,neighbor,reference:r,raw:a?{best:a.best,beta:a.beta,groups:a.groups}:null,packing:pack,combined:b})
 }
 let steiner=[];
 for(let d of [3,4,5,6,7])for(let signed of [false,true]){
  let n=2**d-1,reg=[];for(let x=1;x<=n;x++)for(let y=x+1;y<=n;y++){let z=x^y;if(z<=y)continue;let t=[x-1,y-1,z-1],bad=0;if(signed){let top=t.map(v=>Math.floor(Math.log2(v+1)));let i=top.findIndex((a,i)=>top.filter(b=>a===b).length===1);ck(i>=0);bad=1<<i}reg.push({t,bad:[bad,7^bad]})}
  let E=energy(n,reg),Q=quotient(n,reg),z=solve(Q);ck(z!==null);ck(src(reg,Q.lift(z.s))===z.best);ck(signed?z.best===0:z.best>0);if(d<=4)ck(ref(n,reg).best===z.best);
  let minSpectrum=null;
  if(d===3){minSpectrum=Infinity;for(let q=1;q<2**(n-1);q++){let mags=new Set();for(let x=0;x<2**(n-1);x++){let s=Array.from({length:n},(_,i)=>x>>i&1?-1:1),t=s.map((v,i)=>q>>i&1?-v:v);mags.add(Math.abs(val(E,s)-val(E,t)))}minSpectrum=Math.min(minSpectrum,mags.size);ck(mags.size>=Math.ceil((Math.ceil(Math.max(par(0),Array.from({length:n},(_,i)=>q>>i&1).filter(Boolean).length)/1))/100))}}
  steiner.push({d,n,owners:reg.length,signed,best:z.best,beta:z.beta,groups:z.groups,minSpectrum})
 }
 return {checks,dpTransitions,referenceWords,scans,joins,packChecks,rtout,steiner}
}
console.log(JSON.stringify(run(...process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,'utf8')))),null,2));
