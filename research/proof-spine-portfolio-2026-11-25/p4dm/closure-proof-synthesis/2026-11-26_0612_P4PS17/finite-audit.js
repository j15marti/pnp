/* Independent finite verifier. Run: node finite-audit.js */
function audit(){
 const words=d=>Array.from({length:2**d},(_,i)=>Array.from({length:d},(_,j)=>(i>>j)&1));
 const key=w=>w.join("");
 const signwords=d=>words(d).map(w=>w.map(b=>2*b-1));
 const dot=(a,b)=>a.reduce((z,x,i)=>z+x*b[i],0);
 function good(R,s){
   const d=s.length;if(!d)return R.length>0;
   if(new Set(R.map(w=>dot(w,s))).size!==1)return false;
   const O=R.map(w=>Array.from({length:d},(_,j)=>dot(w.slice(0,j),s.slice(0,j))));
   const S=new Set(O.map(w=>w.join(",")));
   for(const a of O)for(const b of O)for(let k=-2*d;k<=2*d;k++){
     const z=a.map((v,i)=>Math.min(v,b[i]+k));
     if(!S.has(z.map(v=>v-z[0]).join(",")))return false;
   }
   return true;
 }
 function check(b,m){if(!b)throw Error(m)}
 let tables=0,signCases=0,admitted=0,pins=0,cloneCases=0;
 const counts=[];
 for(let d=1;d<=4;d++){
   let t=0;
   for(let p=0;p<2;p++){
     const W=words(d).filter(w=>w.reduce((a,b)=>a+b,0)%2===p);
     for(let m=1;m<2**W.length;m++){
       const R=W.filter((_,i)=>(m>>i)&1),S=signwords(d).filter(s=>good(R,s)),K=new Set(S.map(key));
       tables++;t++;admitted+=S.length;
       const projections=[];
       for(let i=0;i<d;i++)for(let j=i;j<d;j++)projections.push([i,j,new Set(S.map(s=>`${s[i]},${s[j]}`))]);
       for(const s of signwords(d)){
         signCases++;
         check(K.has(key(s))===projections.every(([i,j,P])=>P.has(`${s[i]},${s[j]}`)),"binary sign compilation");
       }
       for(const s of S)for(let i=0;i<d;i++)for(let b=0;b<2;b++){
         const H=R.filter(w=>w[i]===b);
         if(H.length){pins++;check(good(H,s),"pin preservation");}
       }
     }
   }
   counts.push(t);
 }
 for(let a=0;a<2;a++)for(let b=0;b<2;b++){
   const bad=[0,1].map(z=>Number(!a&&!z)+Number(z&&!b));
   check(Math.min(...bad)===Number(!a&&!b),"occurrence clone");
   cloneCases++;
 }
 let state=26112617;
 const rnd=n=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state%n;};
 let networkCases=0,yes=0,no=0,maxT=0,maxQ=0,solutions=0;
 for(let trial=0;trial<100;trial++){
   const d=4,n=3+trial%2,m=2*n;
   const E=Array.from({length:m},(_,e)=>[e%n,(e%n+1)%n]);
   const F=Array.from({length:n},(_,v)=>{
     const es=E.map((uv,e)=>uv.includes(v)?e:-1).filter(e=>e>=0);
     const W=words(d).filter(w=>w.reduce((a,b)=>a+b,0)%2===rnd(2));
     // The parity is sampled once for this table, not once per word.
     const parity=rnd(2),P=words(d).filter(w=>w.reduce((a,b)=>a+b,0)%2===parity);
     const R=P.filter(()=>rnd(3)!==0);
     if(!R.length)R.push(P[0]);
     const S=signwords(d).filter(s=>good(R,s));
     const forb=[];
     if(!S.length)forb.push([0,0,-1,-1],[0,0,1,1]);
     else for(let i=0;i<d;i++)for(let j=i;j<d;j++)for(const a of [-1,1])for(const b of [-1,1]){
       if(i===j&&a!==b)continue;
       if(!S.some(s=>s[i]===a&&s[j]===b))forb.push([i,j,a,b]);
     }
     return {es,R,S,forb};
   });
   let t=Infinity,q=Infinity,choice=null;
   for(const x of signwords(m)){
     const costs=F.map((f,v)=>{const s=f.es.map(e=>x[e]*(E[e][0]===v?1:-1));return f.forb.filter(([i,j,a,b])=>s[i]===a&&s[j]===b).length});
     const b=costs.filter(c=>c>0).length,a=costs.reduce((z,c)=>z+c,0);
     t=Math.min(t,b);
     if(a<q){q=a;choice=x;}
   }
   check(t<=q&&q<=32*t,"factor/clause bound");
   maxT=Math.max(t,maxT);maxQ=Math.max(q,maxQ);
   const B=F.map((f,v)=>({f,v,s:f.es.map(e=>choice[e]*(E[e][0]===v?1:-1))})).filter(({f,s})=>!f.S.some(a=>key(a)===key(s)));
   check(B.length<=q,"repair owners");
   let goodCount=0;
   for(const w of words(m)){
     if(!F.every(f=>f.R.some(a=>key(a)===key(f.es.map(e=>w[e])))))continue;
     goodCount++;
     const fixed=new Set(B.flatMap(({f})=>f.es));
     for(let v=0;v<n;v++){
       const f=F[v],s=f.es.map(e=>choice[e]*(E[e][0]===v?1:-1));
       const R=f.R.filter(a=>f.es.every((e,i)=>!fixed.has(e)||a[i]===w[e]));
       check(good(R,s),"actual solution survives fixed orientation");
     }
   }
   solutions+=goodCount;networkCases++;if(goodCount)yes++;else no++;
 }
 return {tables,counts,signCases,admitted,pins,cloneCases,networkCases,yes,no,maxT,maxQ,solutions,scope:"Finite local sign/pin theorem and abstract cycle controls; not a second planar height solver or FPT implementation."};
}
console.log(JSON.stringify(audit(),null,2));
