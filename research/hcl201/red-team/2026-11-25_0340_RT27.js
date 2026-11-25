// node research/hcl201/red-team/2026-11-25_0340_RT27.js
// Immutable inputs embedded for reproducibility. Reference enumeration, not polynomial solver.
const raw={"controls":[{"n":9,"attempts":1,"initial":24,"critical":9,"maxDegree":5,"neighbors":27,"registry":[{"p":0,"t":[7,8,5],"bad":[2,5]},{"p":0,"t":[4,0,2],"bad":[7,0]},{"p":1,"t":[8,2,1],"bad":[1,6]},{"p":1,"t":[3,6,7],"bad":[5,2]},{"p":2,"t":[5,2,0],"bad":[4,3]},{"p":2,"t":[1,8,3],"bad":[3,4]},{"p":3,"t":[6,2,7],"bad":[0,7]},{"p":4,"t":[5,4,8],"bad":[2,5]},{"p":4,"t":[3,2,1],"bad":[5,2]}]},{"n":12,"attempts":1,"initial":32,"critical":9,"maxDegree":4,"neighbors":27,"registry":[{"p":1,"t":[0,7,6],"bad":[7,0]},{"p":1,"t":[8,9,11],"bad":[5,2]},{"p":2,"t":[7,5,8],"bad":[5,2]},{"p":3,"t":[11,4,9],"bad":[5,2]},{"p":4,"t":[5,7,11],"bad":[3,4]},{"p":4,"t":[2,9,6],"bad":[1,6]},{"p":5,"t":[6,7,0],"bad":[3,4]},{"p":5,"t":[2,11,4],"bad":[1,6]},{"p":6,"t":[2,4,9],"bad":[0,7]}]},{"n":15,"attempts":1,"initial":40,"critical":16,"maxDegree":6,"neighbors":48,"registry":[{"p":0,"t":[6,5,3],"bad":[2,5]},{"p":0,"t":[11,4,1],"bad":[4,3]},{"p":0,"t":[14,2,13],"bad":[5,2]},{"p":1,"t":[9,5,13],"bad":[3,4]},{"p":1,"t":[1,10,11],"bad":[0,7]},{"p":1,"t":[0,12,2],"bad":[1,6]},{"p":1,"t":[6,14,3],"bad":[4,3]},{"p":2,"t":[9,13,4],"bad":[4,3]},{"p":2,"t":[1,5,6],"bad":[7,0]},{"p":3,"t":[8,0,14],"bad":[3,4]},{"p":3,"t":[9,13,5],"bad":[4,3]},{"p":3,"t":[2,3,1],"bad":[0,7]},{"p":4,"t":[8,4,10],"bad":[6,1]},{"p":4,"t":[1,6,12],"bad":[2,5]},{"p":4,"t":[5,9,13],"bad":[2,5]},{"p":6,"t":[3,9,1],"bad":[3,4]}]}]};
const peer={"rt":[{"n":9,"models":24,"alternating":{"accepted":[["c",0],["108",0]]},"neighborAlternating":{"accepted":[["c",0],["108",0],["120",1],["180",1]]}},{"n":12,"models":64,"alternating":{"accepted":[["44",0],["c0",1],["180",0],["300",0],["a00",1]]},"neighborAlternating":{"accepted":[["44",0],["140",1],["300",0],["a00",1],["801",0],["880",0]]}},{"n":15,"models":96,"alternating":{"accepted":[["6",1],["c",1],["30",0],["48",1],["220",0],["2200",0],["41",0],["2040",0],["2800",1],["3000",0],["6000",1]]},"neighborAlternating":{"accepted":[["30",0],["60",1],["240",1],["2200",0],["2008",1]]}}]};
function run(raw,peer){
 let checks=0,visits=0,closureScans=0,forced=0;
 const ok=(x)=>{checks++;if(!x)throw Error("assertion "+checks)};
 const parity=x=>{let p=0;while(x){p^=1;x&=x-1}return p};
 const energy=(reg,x)=>{let e=0;for(const r of reg){let z=0;for(let i=0;i<3;i++)z|=((x>>r.t[i])&1)<<i;e+=r.bad.includes(z)?1:0}return 4*e};
 const neg=(reg,j=0)=>reg.map((r,i)=>({...r,bad:r.bad.map(b=>i===j?b^1:b)}));
 const list=(n,reg)=>Array.from({length:1<<n},(_,x)=>{visits++;return energy(reg,x)});
 const guard=(x,rows)=>rows.every(([m,b])=>parity(x&m)===b);
 // Reference closure over coordinates, respecting the affine guard. No oracle for global SAT.
 function close(n,reg,rows){
  let allowed=Array.from({length:1<<n},(_,x)=>x).filter(x=>guard(x,rows));
  for(;;){
   closureScans++;
   if(!allowed.length)return allowed;
   let fixed=0,word=allowed[0];for(let i=0;i<n;i++)if(allowed.every(x=>!((x^word)&(1<<i))))fixed|=1<<i;
   let add=[];
   for(const r of reg){
    let good=[];
    for(let z=0;z<8;z++)if(!r.bad.includes(z)&&r.t.every((v,i)=>!(fixed&(1<<v))||((z>>i)&1)===((word>>v)&1)))good.push(z);
    if(!good.length)return [];
    for(let i=0;i<3;i++)if(!(fixed&(1<<r.t[i]))&&good.every(z=>((z^good[0])&(1<<i))===0))add.push([1<<r.t[i],(good[0]>>i)&1]);
   }
   if(!add.length)return allowed;
   forced+=add.length;allowed=allowed.filter(x=>guard(x,add));
  }
 }
 function spectrum(E,allowed,d,n){
  const vals=new Set(),abs=[],p=d&-d;
  let min=Infinity;for(const x of allowed){if(x&p)continue;const a=E[x],b=E[x^d];const B=(a-b)/2;ok(Number.isInteger(B));vals.add(Math.abs(B));abs.push(Math.abs(B));min=Math.min(min,a,b);ok((a+b)/2-Math.abs(B)===Math.min(a,b))}
  return {magnitudes:vals.size,min,abs};
 }
 function fwht(a){a=a.slice();for(let h=1;h<a.length;h*=2)for(let i=0;i<a.length;i+=2*h)for(let j=i;j<i+h;j++){let u=a[j],v=a[j+h];a[j]=u+v;a[j+h]=u-v}return a}
 const dense=[];
 for(const k of [3,4]){
  const n=(1<<k)-1,reg=[];
  for(let a=1;a<=n;a++)for(let b=a+1;b<=n;b++){let c=a^b;if(c>b)reg.push({t:[a-1,b-1,c-1],bad:[0,7]})}
  const base=reg.filter(r=>r.t.every(v=>v<7));ok(base.length===7);
  const flipped=neg(base);
  const witness=Array.from({length:128},(_,x)=>x).find(x=>energy(flipped,x)===0);
  ok(witness!==undefined&&energy(base,witness)===4);
  const root=reg.map(r=>{
    if(r.t.every(v=>v<7))return r;
    return energy([r],witness)?{...r,bad:[1,6]}:r;
  });
  const neighbor=neg(root,root.findIndex(r=>r.t.join(",")===base[0].t.join(",")));
  ok(energy(neighbor,witness)===0);
  let pairs=new Set();for(const r of reg)for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let id=r.t[i]+":"+r.t[j];ok(!pairs.has(id));pairs.add(id)}ok(pairs.size===n*(n-1)/2);
  const dirs=n===7?Array.from({length:(1<<(n-1))-1},(_,i)=>i+1):[...new Set([...Array.from({length:n-1},(_,i)=>1<<i),...Array.from({length:n-2},(_,i)=>(1<<(i+2))-1).filter(d=>d<(1<<(n-1))),0x1555,0x2aaa])];
  for(const [label,R] of [["unsigned",reg],["root",root],["neighbor",neighbor]]){
   const A=close(n,R,[]),E=list(n,R);ok(A.length===1<<n);
   const models=E.filter(e=>e===0).length;
   ok(label==="neighbor"?models>0:models===0);
   let minMagnitude=Infinity,minSupport=Infinity,maxMagnitude=0;
   for(const d of dirs){
    const t=spectrum(E,A,d,n),p=Array.from({length:n},(_,i)=>i).filter(i=>d&(1<<i)).length,q=Math.max(p,n-p);
    const lower=Math.ceil((Math.ceil(q/2)+1)/2);
    ok(t.magnitudes>=lower);
    minMagnitude=Math.min(minMagnitude,t.magnitudes);maxMagnitude=Math.max(maxMagnitude,t.magnitudes);
    const support=fwht(t.abs).filter(v=>v!==0).length;minSupport=Math.min(minSupport,support);
    if(label==="unsigned")ok(support>=2**(q-1));
   }
   dense.push({n,owners:R.length,label,models,witness:label==="neighbor"?witness:null,dirs:dirs.length,minMagnitude,maxMagnitude,minAbsWalshSupport:minSupport});
  }
 }
 const shared=[];
 for(const c of raw.controls){
  const p=peer.rt.find(x=>x.n===c.n);
  for(const [label,R,rows0] of [["root",c.registry,p.alternating.accepted],["neighbor",neg(c.registry),p.neighborAlternating.accepted]]){
   const E=list(c.n,R),models=E.filter(x=>x===0).length;
   ok(models===(label==="root"?0:p.models));
   for(let x=0;x<E.length;x++)if(!E[x])ok(guard(x,rows0.map(([m,b])=>[parseInt(m,16),b])));
   let A=close(c.n,R,[]),rows=[];
   const jobs=[];
   for(const phase of ["raw","peer-cuts"]){
    if(phase==="peer-cuts"){for(const [m,b] of rows0){rows.push([parseInt(m,16),b]);A=close(c.n,R,rows)}}
    let min=Infinity;for(const x of A)min=Math.min(min,E[x]);ok((min===0)===(models>0));
    let dirs=0,eligible4=0,least=null;
    if(A.length){ // closure may pin extra coordinates: use directions preserving actual reference chart
     const present=new Set(A),first=A[0],basis=[];
     for(const x of A){let d=x^first;if(!d)continue;let r=d;for(const b of basis)r=Math.min(r,r^b);if(!r)continue;basis.push(r);basis.sort((a,b)=>b-a);if(!A.every(y=>present.has(y^d)))continue;let s=spectrum(E,A,d,c.n);dirs++;eligible4+=s.magnitudes<=4?1:0;least=least===null?s.magnitudes:Math.min(least,s.magnitudes);ok(s.min===min)}
    }
    jobs.push({phase,remaining:A.length,min:Number.isFinite(min)?min:null,dirs,eligible4,least});
   }
   shared.push({n:c.n,label,models,jobs});
  }
 }
 return {checks,visits,closureScans,forced,dense,shared};
}
console.log(JSON.stringify(run(raw,peer),null,2));
