// TMR5 PERMFRONT27, independent finite verifier. Hosted V8 source, 2026-11-14 PST.
(() => {
  const check=(b,s)=>{if(!b)throw Error(s)};
  function swap(j,n){const x=(j&1)^((j>>(n-1))&1);return j^(x*(1|(1<<(n-1))))}
  function frontier(p,c){const j=p.findIndex(i=>i>=c);check(j>=0 && j<=c,"frontier");return [j,c-j]}
  function verify(p,c,enumerate){
    const [j,b]=frontier(p,c);
    if(enumerate){
      const kept=new Set(p.slice(0,j)),free=[];
      for(let i=0;i<c;i++)if(!kept.has(i))free.push(i);
      check(free.length===b,"free count");
      const suffixes=new Set();
      for(let mask=0;mask<2**b;mask++){
        const x=Array(p.length).fill(0);
        free.forEach((i,z)=>{x[i]=(mask>>z)&1});
        const y=p.map(i=>x[i]);
        check(y.slice(0,j).every(v=>v===0),"prefix fixed");
        suffixes.add(y.slice(j).join(""));
      }
      check(suffixes.size===2**b,"injective suffix");
    }
    return [j,b]
  }
  const out={name:"TMR5-PERMFRONT27",status:"COMPUTATIONAL",permutations:0,cuts:0,independent_future_suffixes:0,swap:[],mcsp:[],failures:0};
  function* permute(a,k=0){
    if(k===a.length){yield a.slice();return}
    for(let i=k;i<a.length;i++){
      [a[k],a[i]]=[a[i],a[k]];
      yield* permute(a,k+1);
      [a[k],a[i]]=[a[i],a[k]];
    }
  }
  for(let N=2;N<=6;N++)
    for(const p of permute(Array.from({length:N},(_,i)=>i))){
      out.permutations++;
      for(let c=1;c<N;c++){
        const [j,b]=verify(p,c,true);
        out.cuts++;
        out.independent_future_suffixes+=2**b;
      }
    }
  function gates(w,mask){
    const a=new Set();
    for(let i=0;i<w.length;i++){
      a.add((~w[i])&mask);
      for(let z=i;z<w.length;z++){a.add(w[i]&w[z]);a.add(w[i]|w[z])}
    }
    return a
  }
  for(let n=2;n<=6;n++){
    const N=2**n,p=Array.from({length:N},(_,j)=>swap(j,n));
    check(new Set(p).size===N && p.every((v,j)=>p[v]===j),"involution");
    const B=Array.from({length:N-1},(_,i)=>frontier(p,i+1)[1]);
    const [j,b]=verify(p,N/2,n<=5);
    check(j===1 && b===N/2-1 && Math.max(...B)===b,"swap peak");
    out.swap.push({n,N,cut:N/2,first_future:j,independent_bits:b,peak:Math.max(...B),enumerated:n<=5});
  }
  for(let n=2;n<=4;n++){
    const N=2**n, mask=(2**N)-1,variables=[];
    for(let z=0;z<n;z++){
      let v=0;for(let j=0;j<N;j++)if((j>>z)&1)v|=1<<j;
      variables.push(v)
    }
    const wires=[0,mask,...variables];
    const y0=new Set(wires), first=gates(wires,mask), y1=new Set([...y0,...first]),y2=new Set(y1);
    for(const a of first)for(const b of gates([...wires,a],mask))y2.add(b);
    const classes=[y0,y1,y2];let checks=0;
    for(let x=0;x<2**N;x++){
      let y=0;for(let j=0;j<N;j++)y|=((x>>swap(j,n))&1)<<j;
      for(const C of classes){check(C.has(x)===C.has(y),"label invariance");checks++}
    }
    out.mcsp.push({n,N,yes_sizes:classes.map(c=>c.size),all_label_checks:checks})
  }
  return out
})()
