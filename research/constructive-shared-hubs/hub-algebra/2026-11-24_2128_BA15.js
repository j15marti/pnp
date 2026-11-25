"use strict";
function BA15(){
  const parity=x=>{let p=0;while(x){x&=x-1;p^=1}return p};
  const rank=xs=>{const b=new Map();for(let x of xs){while(x){const p=31-Math.clz32(x);if(b.has(p))x^=b.get(p);else{b.set(p,x);break}}}return b.size};
  const A={assertions:0,closure_scans:0,forced:0,deleted:0,reference_words:0,polar_subsets:0,guard_subset_tests:0};
  function check(x){A.assertions++;if(!x)throw Error("assertion "+A.assertions)}
  function chart(n,G){
    const b=new Map();
    for(let [x,v] of G){while(x){let p=31-Math.clz32(x);if(b.has(p)){const [y,w]=b.get(p);x^=y;v^=w}else{b.set(p,[x,v]);break}}if(!x&&v)return null}
    const free=Array.from({length:n},(_,i)=>i).filter(i=>!b.has(i));
    function lift(y,hom=false){let x=0;for(let i=0;i<free.length;i++)if(y>>i&1)x|=1<<free[i];for(let i=0;i<n;i++)if(b.has(i)){const [r,v]=b.get(i);if(parity(r&x)^(hom?0:v))x|=1<<i}return x}
    return {free,lift};
  }
  const violation=(p,x)=>Number(p.every(([a,b])=>parity(a&x)===b));
  function poly(p,C){
    const d=C.free.length,q0=violation(p,C.lift(0)),L=Array.from({length:d},(_,i)=>violation(p,C.lift(1<<i))^q0);
    let low=BigInt(q0);for(let i=0;i<d;i++)if(L[i])low|=1n<<BigInt(i+1);
    let hi=0n,j=0n;for(let i=0;i<d;i++)for(let k=i+1;k<d;k++,j++)if(violation(p,C.lift((1<<i)|(1<<k)))^q0^L[i]^L[k])hi|=1n<<j;
    return [hi,low];
  }
  function closure(n,Ps,G0=[]){
    let P=Ps.slice(),G=G0.slice(),f=0,del=0;
    outer:while(true){
      A.closure_scans++;const C=chart(n,G);if(!C)return {unsat:true,G,P,f,del};
      const pol=P.map(p=>poly(p,C));
      function force(l){let a=0;for(let i=0;i<C.free.length;i++)if((l>>BigInt(i+1))&1n)a|=1<<C.free[i];if(!a)return false;G.push([a,Number(l&1n)]);f++;A.forced++;return true}
      // Singleton affine reductions first, including inactive packets.
      for(let i=0;i<P.length;i++)if(!pol[i][0]){let l=pol[i][1];if(l===1n)return {unsat:true,G,P,f,del};if(l){check(force(l));continue outer}P.splice(i,1);del++;A.deleted++;continue outer}
      const piv=new Map();
      for(let i=0;i<P.length;i++){
        let [h,l]=pol[i];while(h){const b=h&-h;if(!piv.has(b)){piv.set(b,[h,l]);break}const [H,L]=piv.get(b);h^=H;l^=L}
        if(!h){if(l===1n)return {unsat:true,G,P,f,del};if(l){check(force(l));continue outer}P.splice(i,1);del++;A.deleted++;continue outer}
      }
      return {unsat:false,G,P,f,del};
    }
  }
  const valid=(P,G,x)=>G.every(([a,b])=>parity(a&x)===b)&&P.every(p=>!violation(p,x));
  function control(name,n,P,G=[]){
    const R=closure(n,P,G);let count=0;
    for(let x=0;x<(1<<n);x++){A.reference_words++;const v=valid(P,G,x);count+=Number(v);check(v===(!R.unsat&&valid(R.P,R.G,x)))}
    return {name,count,forced:R.f,deleted:R.del,closure_reject:R.unsat};
  }
  const nae=([a,b,c],s=0)=>[[(1<<a)^(1<<b),s&1],[(1<<a)^(1<<c),(s>>1)&1]];
  const E=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
  const F=E.map(e=>nae(e));const controls=[];
  controls.push(control("Fano",7,F));
  for(let j=0;j<7;j++)for(let s=1;s<4;s++){const P=F.slice();P[j]=nae(E[j],s);controls.push(control("Fano sign "+j+"/"+s,7,P))}
  // Single-budget: keep only one monochromatic word in one owner. Reference only.
  const budgets=[];for(let j=0;j<7;j++)for(let b=0;b<2;b++){const P=F.slice();P[j]=E[j].map(i=>[1<<i,b]);let count=0;for(let x=0;x<128;x++){A.reference_words++;count+=Number(valid(P,[],x))}check(count===5);budgets.push(count)}
  const p1=[[[1,1],[2,1]],[[1,1],[4,1]],[[1,1],[6,0]]];
  controls.push(control("nonlocal forced a=0",3,p1));
  const p2=p1.slice();p2[2]=[[1,1],[6,1]];controls.push(control("redundancy neighbor",3,p2));
  controls.push(control("opposite forced a=1",5,[...p1,[[1,0],[8,1]],[[1,0],[16,1]],[[1,0],[24,0]]]));
  for(let a=1;a<128;a++)for(let b=0;b<2;b++)controls.push(control("Fano guard "+a+"/"+b,7,F,[[a,b]]));
  let seed=241124;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
  for(let i=0;i<100;i++){const P=[];for(let j=0;j<8;j++){let a=1+rnd(31),b=1+rnd(31);if(a===b)b=(b%31)+1;P.push([[a,rnd(2)],[b,rnd(2)]])}controls.push(control("random "+i,5,P))}
  const geometries=[{name:"Fano",n:7,E,D:3,g:3}];
  for(let m=4;m<=6;m++){geometries.push({name:"loose cycle "+m,n:2*m,E:Array.from({length:m},(_,i)=>[i,(i+1)%m,m+i]),D:2,g:m})}
  geometries.push({name:"loose path",n:11,E:Array.from({length:5},(_,i)=>[i,i+1,6+i]),D:2,g:1000});
  for(const z of geometries){const P=z.E.map(e=>nae(e)),M=1<<P.length;for(let mask=1;mask<M;mask++){
    let J=z.E.filter((_,i)=>mask>>i&1),rows=Array(z.n).fill(0);
    for(const e of J)for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){rows[e[i]]^=1<<e[j];rows[e[j]]^=1<<e[i]}
    const r=rank(rows);A.polar_subsets++;check(r>0);check(6*J.length<=r*(2*z.D)**2);if(J.length<z.g)check(r===2*J.length);
    for(let k=1;k<=2;k++)for(let t=0;t<6;t++){let G=[];while(G.length<k){const a=1+rnd((1<<z.n)-1);if(rank([...G.map(x=>x[0]),a])>G.length)G.push([a,rnd(2)])}
      const C=chart(z.n,G);let h=0n;for(let i=0;i<P.length;i++)if(mask>>i&1)h^=poly(P[i],C)[0];A.guard_subset_tests++;
      if(!h){check(r<=2*k);check(3*J.length<=4*z.D*z.D*k);if(z.g>4*z.D*z.D*k/3)check(J.length<=k)}
    }
  }}
  check(controls[0].count===0);check(controls.slice(1,22).every(x=>x.count===10));check(controls[22].forced===1&&controls[22].count===4);check(controls[23].deleted>=1&&controls[23].count===5);check(controls[24].closure_reject&&controls[24].count===0);
  return {ledger:A,controls:controls.length,sat:controls.filter(x=>x.count>0).length,unsat:controls.filter(x=>x.count===0).length,budget_reference:budgets,examples:controls.slice(0,25),guard_summary:{max_forced:Math.max(...controls.slice(25,279).map(x=>x.forced)),max_deleted:Math.max(...controls.slice(25,279).map(x=>x.deleted)),rejected:controls.slice(25,279).filter(x=>x.closure_reject).length},seed:241124};
}
console.log(JSON.stringify(BA15(),null,2));
