function experiment(){
  let seed=2010950;const rng=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
  const edge=(s,t,u,g)=>({s,t,l:0,u,g:BigInt(g)});
  const sum=(a,f)=>a.reduce((s,e)=>s+f(e),0);
  const sign=e=>e.t===1?1:-1;
  const minnet=e=>sign(e)>0?e.l:-e.u;
  const maxnet=e=>sign(e)>0?e.u:-e.l;
  const mod=x=>BigInt((x%2+2)%2);
  let counts={random:0,baseSAT:0,baseUNSAT:0,closedFixed:0,closureQueries:0,candidateChecks:0,accepted:0,declined:0,empty:0,referenceTuples:0,referenceFibers:0,verifiedFibers:0,targetSAT:0,targetUNSAT:0,targetUnknown:0,verifiedLifts:0,wrong:0,scale:[],hostile:[]};
  const assert=(p,msg)=>{if(!p)throw Error(msg)};
  function rangeK(K,b2){let A=K.filter(e=>e.s===0),B=K.filter(e=>e.s===1);
    return [Math.max(sum(B,e=>e.l),b2-sum(A,e=>e.u)),Math.min(sum(B,e=>e.u),b2-sum(A,e=>e.l))]}
  function feasible(H,K,b1,b2){if([...H,...K].some(e=>e.l>e.u))return false;let [a,b]=rangeK(K,b2);return Math.max(a,sum(H,minnet)-b1)<=Math.min(b,sum(H,maxnet)-b1)}
  function close(H,K,b1,b2,stats){
    H=H.map(e=>({...e}));K=K.map(e=>({...e}));if(!feasible(H,K,b1,b2))return null;
    for(let e of [...H,...K]){if(e.l===e.u)continue;let lo=e.l,hi=e.u,a=lo,b=hi;
      while(a<b){let mid=Math.floor((a+b)/2);e.u=mid;if(stats)counts.closureQueries++;if(feasible(H,K,b1,b2))b=mid;else a=mid+1;e.u=hi}
      let mn=a;a=mn;b=hi;e.l=mn;
      while(a<b){let mid=Math.ceil((a+b)/2);e.l=mid;if(stats)counts.closureQueries++;if(feasible(H,K,b1,b2))a=mid;else b=mid-1;e.l=mn}
      e.u=a;if(e.u===e.l&&stats)counts.closedFixed++;
    }return {H,K}
  }
  function basis(cols){let B=new Map(),chosen=[];for(let i=0;i<cols.length;i++){let x=cols[i],mask=1n<<BigInt(i);while(x){let k=x.toString(2).length-1;if(!B.has(k)){B.set(k,[x,mask]);chosen.push(i);break}let [v,m]=B.get(k);x^=v;mask^=m}}return {chosen,solve:x=>{let mask=0n;while(x){let k=x.toString(2).length-1;if(!B.has(k))return null;let [v,m]=B.get(k);x^=v;mask^=m}return mask}}}
  function allocate(lo,hi,target){let a=lo.slice(),d=target-sum(a,x=>x);assert(d>=0,"allocation below");for(let i=0;i<a.length;i++){let z=Math.min(d,hi[i]-a[i]);a[i]+=z;d-=z}assert(d===0,"allocation above");return a}
  function cert(H,K,b1,b2,base){
    let [a,b]=rangeK(K,b2);if(a>b)return null;
    let R=[],C=[];for(let i=0;i<H.length;i++){(H[i].g===base?R:C).push(i)}
    if(!R.length)return null;let Cedges=C.map(i=>H[i]),Redges=R.map(i=>H[i]);
    let B=basis(Cedges.map(e=>e.l<e.u?e.g^base:0n)),r=B.chosen.length,P=new Set(B.chosen);
    let cmin=sum(Cedges,minnet),cmax=sum(Cedges,maxnet),rmin=sum(Redges,minnet),rmax=sum(Redges,maxnet);
    let L=Math.max(cmin,b1+b-rmax),U=Math.min(cmax-r,b1+a-r-rmin);
    if(L>U)return null;
    let cb=allocate(Cedges.map(minnet),Cedges.map((e,i)=>maxnet(e)-(P.has(i)?1:0)),L).map((v,i)=>v*sign(Cedges[i]));
    let offset=mod(b1)*base;for(let j=0;j<C.length;j++)if(mod(cb[j]))offset^=Cedges[j].g^base;
    return {R,C,r,L,U,offset,B,cb,base}
  }
  function Ktag(K,y,base){let t=0n;for(let i=0;i<K.length;i++)if(mod(y[i]))t^=K[i].g^(K[i].s===1?base:0n);return t}
  function lift(H,K,b1,b2,c,y,t){let mask=c.B.solve(t^c.offset^Ktag(K,y,c.base));if(mask===null)return null;
    let x=Array(H.length).fill(0),h=b1+sum(K,(e)=>0);h=b1+y.reduce((s,v,i)=>s+(K[i].s===1?v:0),0);
    for(let j=0;j<c.C.length;j++){let i=c.C[j];x[i]=c.cb[j]+(mask>>BigInt(j)&1n?sign(H[i]):0);h-=sign(H[i])*x[i]}
    let r=c.R.map(i=>H[i]),v=allocate(r.map(minnet),r.map(maxnet),h);
    for(let j=0;j<c.R.length;j++)x[c.R[j]]=v[j]*sign(r[j]);
    assert(check(H,K,b1,b2,x,y,t),"bad lift");return x}
  function check(H,K,b1,b2,x,y,t){let net=[0,0,0],g=0n;let all=[...H,...K],v=[...x,...y];for(let i=0;i<all.length;i++){let e=all[i],z=v[i];if(z<e.l||z>e.u||!Number.isInteger(z))return false;net[e.s]-=z;net[e.t]+=z;if(mod(z))g^=e.g}return net[1]===b1&&net[2]===b2&&g===t}
  function tuples(E,fn){let x=Array(E.length).fill(0);function go(i){if(i===E.length){fn(x.slice());return}for(let j=E[i].l;j<=E[i].u;j++){x[i]=j;go(i+1)}}go(0)}
  function krows(K,b2){let Y=[];tuples(K,y=>{if(sum(y,z=>z)===b2)Y.push(y)});return Y}
  function ref(H,K,b1,b2){let out=new Map();for(let y of krows(K,b2)){let tags=new Set();tuples(H,x=>{counts.referenceTuples++;if(sum(x,(v)=>0)!==0)throw Error("unused");if(x.reduce((s,v,i)=>s+sign(H[i])*v,0)!==b1+y.reduce((s,v,i)=>s+(K[i].s===1?v:0),0))return;let tag=0n;for(let i=0;i<H.length;i++)if(mod(x[i]))tag^=H[i].g;for(let i=0;i<K.length;i++)if(mod(y[i]))tag^=K[i].g;tags.add(tag)});out.set(y.join(","),tags)}counts.referenceFibers+=out.size;return out}
  function find(H,K,b1,b2,stats=true){let best=null;for(let base of new Set(H.map(e=>e.g))){if(stats)counts.candidateChecks++;let c=cert(H,K,b1,b2,base);if(c&&(!best||c.r>best.r))best=c}return best}
  function run(H,K,b1,b2){counts.random++;let F=ref(H,K,b1,b2),all=new Set([...F.values()].flatMap(s=>[...s]));let cl=close(H,K,b1,b2,true);assert(!!cl===(all.size>0),"closure decision");if(!cl){counts.baseUNSAT++;counts.empty++;counts.targetUNSAT+=16;return}
    counts.baseSAT++;let c=find(cl.H,cl.K,b1,b2);if(!c){counts.declined++;counts.targetUnknown+=16;return}counts.accepted++;let pred=new Set();
    for(let y of krows(cl.K,b2)){let expected=F.get(y.join(","));assert(expected!==undefined,"new quotient y");counts.verifiedFibers++;for(let t=0n;t<16n;t++){let x=lift(cl.H,cl.K,b1,b2,c,y,t);assert(!!x===expected.has(t),"fiber mismatch");if(x){counts.verifiedLifts++;pred.add(t)}}}
    for(let t=0n;t<16n;t++){assert(pred.has(t)===all.has(t),"global mismatch");if(pred.has(t))counts.targetSAT++;else counts.targetUNSAT++}
  }
  for(let j=0;j<240;j++){
    let H=[],K=[],base=rng(8),nr=1+rng(3),nc=1+rng(4);
    for(let i=0;i<nr;i++){let s=rng(2);H.push(edge(s,1-s,1+rng(3),base))}
    for(let i=0;i<nc;i++){let s=rng(2);H.push(edge(s,1-s,1+rng(2),rng(8)))}
    for(let i=0;i<3;i++)K.push(edge(rng(2),2,1+rng(2),rng(8)));
    let b1=rng(12)-5,b2=rng(6);run(H,K,b1,b2)
  }
  for(let r of [2,4,8,16,32,64,128,256]){
    let H=[],K=[edge(0,2,1,0n),edge(0,2,1,1n<<BigInt(r)),edge(1,2,1,1n<<BigInt(r+1))];
    for(let i=0;i<r+1;i++)H.push(edge(0,1,1,0n));
    for(let i=0;i<r;i++)H.push(edge(0,1,1,1n<<BigInt(i)));
    let cl=close(H,K,r,1,false);assert(cl,"scale base");let c=cert(cl.H,cl.K,r,1,0n);assert(c&&c.r===r,"scale cert");let sat=0,unsat=0;
    let mask=(1n<<BigInt(r))-1n;
    for(let low of [0n,mask,mask/3n])for(let hi=0;hi<4;hi++){
      let t=low^(BigInt(hi)<<BigInt(r));let w=krows(cl.K,1).some(y=>!!lift(cl.H,cl.K,r,1,c,y,t));assert(w===(hi!==3),"scale decision");if(w)sat++;else unsat++;
    }counts.scale.push({rank:r,H_arcs:H.length,total_arcs:H.length+K.length,quotient_arcs:K.length,SAT:sat,UNSAT:unsat,all_unit:true,interval:[c.L,c.U]});
  }
  for(let tags of [[0,1,2],[0,1,1]]){let H=tags.map(g=>edge(0,1,1,g)),K=[],cl=close(H,K,1,0,false),c=cert(cl.H,cl.K,1,0,0n),F=ref(H,K,1,0);let s=[...F.get("")].map(String).sort();assert(!!c===(tags[1]===tags[2]),"hostile acceptance");counts.hostile.push({tags,support:s,certificate:!!c,missing3:!s.includes("3")})}
  return counts;
}
console.log(JSON.stringify(experiment(),null,2));
