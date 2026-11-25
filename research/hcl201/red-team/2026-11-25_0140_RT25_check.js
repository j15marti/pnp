function checkRT25(source){
 const bit=(w,i)=>(w>>i)&1, assert=(x,msg)=>{if(!x)throw Error(msg);count.assertions++}, count={assertions:0,pinJobs:0,closureSweeps:0,forced:0,localVectors:0,pairBalanceChecks:0,referenceWords:0};
 const rows=o=>Array.from({length:8},(_,w)=>w).filter(w=>w!==o.s&&w!==(o.s^7));
 function cert(O,n,pins){
  count.pinJobs++;let fixed=Array(n).fill(-1);
  for(const [i,w] of pins)for(let j=0;j<3;j++){let v=O[i].t[j],b=bit(w,j);if(fixed[v]>=0&&fixed[v]!==b)return null;fixed[v]=b}
  let live,changed=true;
  while(changed){count.closureSweeps++;changed=false;live=O.map(o=>rows(o).filter(w=>o.t.every((v,j)=>fixed[v]<0||fixed[v]===bit(w,j))));
   if(live.some(a=>!a.length))return null;
   O.forEach((o,i)=>o.t.forEach((v,j)=>{if(fixed[v]<0&&live[i].every(w=>bit(w,j)===bit(live[i][0],j))){fixed[v]=bit(live[i][0],j);changed=true;count.forced++}}));
  }
  let g=Array.from({length:n},()=>[]);
  O.forEach(o=>{let f=o.t.map((v,j)=>[v,j]).filter(([v])=>fixed[v]<0);if(f.length===2){let j=o.t.findIndex(v=>fixed[v]>=0),sg=(fixed[o.t[j]]^bit(o.s,j))? -1:1;let [a,b]=f;let aa=bit(o.s,a[1])?-1:1,bb=bit(o.s,b[1])?-1:1;g[a[0]].push([b[0],sg,aa,bb]);g[b[0]].push([a[0],sg,bb,aa])}});
  let d=Array(n).fill(null);
  for(let v=0;v<n;v++)if(fixed[v]<0&&d[v]===null){d[v]=0;let q=[v];for(let h=0;h<q.length;h++){let u=q[h];for(const [w,s,a,b] of g[u]){if(d[w]===null){d[w]=s*b*(Math.abs(d[u])+1);q.push(w)}assert(s*(a*d[u]+b*d[w])>0,"bias inequality")}}}
  function weights(o,i,D,m,positive){
   let f=o.t.map((v,j)=>j).filter(j=>fixed[o.t[j]]<0),k=f.length, R=live[i], W=Array(8).fill(0);
   let target=f.map(j=>bit(o.s,j)?D-m[o.t[j]]:m[o.t[j]]);
   const put=(z,v)=>{let w=o.t.reduce((w,x,j)=>w|((fixed[x]<0?0:fixed[x])<<j),0);for(let h=0;h<k;h++)w|=((bit(z,h)^bit(o.s,f[h]))<<f[h]);assert(R.includes(w),"illegal mass support");W[w]+=v};
   if(k===0)W[R[0]]=D;
   else if(k===1){put(0,D-target[0]);put(1,target[0])}
   else if(k===2){let j=o.t.findIndex(v=>fixed[v]>=0);if((fixed[o.t[j]]^bit(o.s,j))===0){put(3,target[0]+target[1]-D);put(1,D-target[1]);put(2,D-target[0])}else{put(0,D-target[0]-target[1]);put(1,target[0]);put(2,target[1])}}
   else {let base=positive?D/6:0;for(let z=1;z<7;z++)put(z,base);let rem=D-6*base,dx=target[0]-3*base,dy=target[1]-3*base,dz=target[2]-3*base, u=dx+dy+dz-rem;put(3,u);put(1,dx-u);put(2,dy-u);put(4,dz)}
   assert(W.reduce((a,b)=>a+b,0)===D,"mass sum");
   for(let j=0;j<3;j++)assert(W.reduce((a,v,w)=>a+v*bit(w,j),0)===m[o.t[j]],"moment");
   assert(W.every((v,w)=>Number.isInteger(v)&&(!v||R.includes(w))&&(!positive||!R.includes(w)||v>0)),"support");
   count.localVectors++;return W;
  }
  let D=600, frac=fixed.map((x,v)=>x<0?D/2+d[v]:D*x),inte=fixed.map(x=>Math.max(0,x));
  let P=O.map((o,i)=>weights(o,i,D,frac,true)),Z=O.map((o,i)=>weights(o,i,1,inte,false));
  for(let i=0;i<O.length;i++)for(let j=i+1;j<O.length;j++){let common=O[i].t.filter(v=>O[j].t.includes(v));assert(common.length<=1,"linearity");for(let v of common)for(let [A,B] of [[P[i],P[j]],[Z[i],Z[j]]]){let moment=(w,k)=>w.reduce((a,z,r)=>a+z*bit(r,k),0);assert(moment(A,O[i].t.indexOf(v))===moment(B,O[j].t.indexOf(v)),"pair balance");count.pairBalanceChecks++}}
  return true;
 }
 function exhaustive(O,n){let z=0;for(let w=0;w<2**n;w++){count.referenceWords++;if(O.every(o=>rows(o).includes(o.t.reduce((a,v,j)=>a|(bit(w,v)<<j),0))))z++}return z}
 const controls=[];
 for(let L of [7,8,9])for(let pattern of [0,1]){let O=Array.from({length:L},(_,i)=>({t:[i,(i+1)%L,L+i],s:pattern?((i*5+3)%8):0}));let start=count.pinJobs;assert(cert(O,2*L,[]),"root");for(let i=0;i<L;i++)for(let a of rows(O[i])){assert(cert(O,2*L,[[i,a]]),"single");for(let j=i+1;j<L;j++)for(let b of rows(O[j])){if(O[i].t.every((v,k)=>!O[j].t.includes(v)||bit(a,k)===bit(b,O[j].t.indexOf(v))))assert(cert(O,2*L,[[i,a],[j,b]]),"pair")}}controls.push({L,pattern,jobs:count.pinJobs-start,models:L===7?exhaustive(O,2*L):null})}
 const F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map(t=>({t,s:0}));const fano=[exhaustive(F,7),exhaustive(F.slice(1),7)];assert(fano[0]===0&&fano[1]>0,"Fano labels");
 const witness=13308834;const sourceChecks=source.O.map(o=>o.t.reduce((a,v,j)=>a|(bit(witness,v)<<j),0));assert(sourceChecks.every((w,i)=>!source.O[i].bad.includes(w)),"BW17 source witness");
 let triangles=0;for(let i=0;i<source.O.length;i++)for(let j=i+1;j<source.O.length;j++)for(let k=j+1;k<source.O.length;k++){let a=source.O[i].t.filter(v=>source.O[j].t.includes(v)),b=source.O[j].t.filter(v=>source.O[k].t.includes(v)),c=source.O[k].t.filter(v=>source.O[i].t.includes(v));if(a.some(x=>b.some(y=>c.some(z=>new Set([x,y,z]).size===3))))triangles++}
 assert(triangles>0,"BW17 high girth test should decline");
 return {controls,fano,source:{witness,owners:source.O.length,sourceChecks,bergeTriangles:triangles,rawHighGirthEligibility:false},count};
}
if(typeof require!=='undefined'&&require.main===module){console.log(JSON.stringify(checkRT25(JSON.parse(require('fs').readFileSync(process.argv[2],'utf8'))),null,2));}
