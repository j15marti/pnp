function main(){
  let seed=20261124; const rand=n=>{seed=(Math.imul(1664525,seed)+1013904223)>>>0;return seed%n};
  const P=998244353n, mod=x=>(x%P+P)%P;
  function pow(x,n){let y=1n;while(n){if(n&1n)y=y*x%P;x=x*x%P;n>>=1n}return y}
  let stats={joins:0,convolutions:0,butterflies:0,quotient_candidates:0,compatible_fibers:0,table_cells:0,reference_tuples:0,closure_queries:0,forced_deletions:0,witnesses:0,SAT:0,UNSAT:0,checks:0};
  const check=(b)=>{stats.checks++;if(!b)throw Error("mismatch")};
  function fft(a,inv){let n=a.length;for(let i=1,j=0;i<n;i++){let b=n>>1;while(j&b){j^=b;b>>=1}j^=b;if(i<j)[a[i],a[j]]=[a[j],a[i]]}for(let l=2;l<=n;l*=2){let w=pow(3n,(P-1n)/BigInt(l));if(inv)w=pow(w,P-2n);for(let i=0;i<n;i+=l){let t=1n;for(let j=0;j<l/2;j++){let u=a[i+j],v=a[i+j+l/2]*t%P;a[i+j]=mod(u+v);a[i+j+l/2]=mod(u-v);t=t*w%P;stats.butterflies++}}}if(inv){let q=pow(BigInt(n),P-2n);for(let i=0;i<n;i++)a[i]=a[i]*q%P}}
  const tuples=ds=>ds.reduce((a,d)=>a.flatMap(x=>Array.from({length:d},(_,i)=>[...x,i])),[[]]);
  const idx=(x,ds)=>x.reduce((s,v,i)=>s*ds[i]+v,0);
  function conv(f,g,ds){stats.convolutions++;stats.table_cells+=f.length*3;let a=f.slice(),b=g.slice();function transform(v,inv){let stride=v.length;for(let d of ds){stride/=d;for(let base=0;base<v.length;base+=d*stride)for(let j=0;j<stride;j++){let line=Array.from({length:d},(_,i)=>v[base+j+i*stride]);fft(line,inv);line.forEach((x,i)=>v[base+j+i*stride]=x)}}}transform(a,false);transform(b,false);a=a.map((x,i)=>x*b[i]%P);transform(a,true);return a}
  const span=gs=>{let s=new Set([0]);for(let g of gs)for(let x of [...s])s.add(x^g);return [...s].sort((a,b)=>a-b)};
  const key=(s,q)=>[s,...q].join(",");
  function join(sp,mask,rows,ms){
    stats.joins++;
    let [A,B,C]=sp,D=A.filter(x=>B.includes(x)&&C.includes(x)),basis=[],v=[0];
    for(let x of D)if(!v.includes(x)){basis.push(x);v=v.concat(v.map(y=>y^x))}
    const rep=x=>Math.min(...D.map(y=>x^y)),ar=[...new Set(A.map(rep))],br=[...new Set(B.map(rep))],cr=new Set(C.map(rep));
    let common=[],pair=[];for(let i=0;i<ms.length;i++){let k=mask[i];if(k===7)common.push(i);else if(k===3||k===5||k===6)pair.push(i)}
    const ds=[...basis.map(()=>2),...common.map(i=>ms[i])],ct=tuples(ds),pt=tuples(pair.map(i=>ms[i]));
    const sd=x=>basis.reduce((s,b,i)=>x[i]?s^b:s,0);
    const maps=rows.map(rr=>{let m=new Map;for(let [s,q,w] of rr){let k=key(s,q.map((x,i)=>(x%ms[i]+ms[i])%ms[i]));m.set(k,(m.get(k)||0n)+BigInt(w))}return m});
    let out=new Map;
    for(let a of ar)for(let b of br){stats.quotient_candidates++;if(!cr.has(a^b))continue;for(let pp of pt){stats.compatible_fibers++;
      let qa=ms.map(()=>0),qb=qa.slice(),qc=qa.slice();
      pair.forEach((i,j)=>{let x=pp[j],k=mask[i];if(k&1)qa[i]=x;if(k===3)qb[i]=(ms[i]-x)%ms[i];else if(k===6)qb[i]=x;if(k&4)qc[i]=x});
      const fill=(m,r,q)=>ct.map(x=>{let p=q.slice();common.forEach((i,j)=>p[i]=x[basis.length+j]);return m.get(key(r^sd(x),p))||0n});
      const f=fill(maps[0],a,qa),g=fill(maps[1],b,qb);if(!f.some(x=>x)||!g.some(x=>x))continue;
      const h=conv(f,g,ds);h.forEach((x,j)=>{if(!x)return;let z=ct[j],p=qc.slice();common.forEach((i,k)=>p[i]=z[basis.length+k]);let k=key(a^b^sd(z),p);out.set(k,(out.get(k)||0n)+x)})
    }}
    return out;
  }
  function exact(sp,mask,rows,ms){let h=join(sp,mask,rows,ms),n=0n;for(let [s,q,w] of rows[2]){let p=q.map((x,i)=>(-x%ms[i]+ms[i])%ms[i]);n+=(h.get(key(s,p))||0n)*BigInt(w)}return n}
  function reference(rows){let n=0n;for(let a of rows[0])for(let b of rows[1])for(let c of rows[2]){stats.reference_tuples++;if((a[0]^b[0]^c[0])===0&&a[1].every((v,i)=>v+b[1][i]+c[1][i]===0))n+=BigInt(a[2]*b[2]*c[2])}return n}
  let cases=[];
  for(let t=0;t<48;t++){let sp=Array.from({length:3},()=>span(Array.from({length:1+rand(3)},()=>rand(8)))),mask=[1+rand(7),1+rand(7)],ms=[8,8],rows=sp.map((s,i)=>Array.from({length:3+rand(3)},()=>[s[rand(s.length)],mask.map(m=>m&(1<<i)?rand(3)-1:0),1+rand(3)]));
    // Guaranteed paired labels in addition to unrestricted random cases.
    if(t%4===0){for(let rr of rows)rr.push([0,[0,0],1])}
    if(t%4===1){mask[0]=1;rows[0]=rows[0].map(([s,q,w])=>[s,[1,q[1]],w]);for(let i=1;i<3;i++)rows[i]=rows[i].map(([s,q,w])=>[s,[0,q[1]],w])}
    let n=exact(sp,mask,rows,ms);check(n===reference(rows));let init=n;stats[n?"SAT":"UNSAT"]++;
    // Explicit leaf-row support closure: restart immediately after a deletion.
    if(n){let changed=true;while(changed){changed=false;outer:for(let i=0;i<3;i++)for(let j=0;j<rows[i].length;j++){let rr=rows.map(x=>x.slice());rr[i]=[rr[i][j]];stats.closure_queries++;let k=exact(sp,mask,rr,ms);check(k===reference(rr));if(!k){rows[i].splice(j,1);stats.forced_deletions++;check(exact(sp,mask,rows,ms)===n);changed=true;break outer}}}
      // Guarded witness choices, followed by renewed closure in each restricted context.
      for(let i=0;i<3;i++){let rr=rows.map(x=>x.slice());rr[i]=[rr[i][0]];check(exact(sp,mask,rr,ms)>0n);rows=rr;let again=true;while(again){again=false;outer2:for(let k=0;k<3;k++)for(let j=0;j<rows[k].length;j++){let r=rows.map(x=>x.slice());r[k]=[r[k][j]];stats.closure_queries++;let q=exact(sp,mask,r,ms);check(q===reference(r));if(!q){rows[k].splice(j,1);stats.forced_deletions++;again=true;break outer2}}}}
      check(reference(rows)>0n);stats.witnesses++;
    }
    cases.push({id:t,count:String(init)});
  }
  let scaling=[];
  for(let r=1;r<=7;r++){let s=span(Array.from({length:r},(_,i)=>1<<i)),ms=[8],mask=[7],rr=s.flatMap(x=>Array.from({length:3},(_,q)=>[x,[q-1],1])),c=[[0,[0],1]],rows=[rr,rr,c],sp=[s,s,s];let old={...stats},n=exact(sp,mask,rows,ms);check(n===reference(rows));scaling.push({rank:r,common_domain:s.length*8,naive_dense_pairs:(s.length*8)**2,butterflies:stats.butterflies-old.butterflies,convolutions:stats.convolutions-old.convolutions,count:String(n)})}
  // Marginals pass, joint target fails. Safe mod and sign controls.
  let hostile=[[[0,[0],1],[1,[1],1]],[[0,[0],1]],[[1,[0],1]]];check(exact([[0,1],[0],[0,1]],[1],hostile,[8])===0n);check(reference(hostile)===0n);
  let signed=conv([1n,mod(-2n),3n,0n],[mod(-1n),2n,0n,1n],[2,2]);let fs=[1n,-2n,3n,0n],gs=[-1n,2n,0n,1n];for(let i=0;i<4;i++)check(signed[i]===mod(fs.reduce((a,v,j)=>a+v*gs[i^j],0n)));
  return {seed:20261124,stats,cases,scaling,notes:"Fixed prime exact for this suite by counts < prime; small enumerated span/coset reference front end, not general Gaussian kernel discovery or arbitrary precision FFT. No strict-source compilation or full peer closure. Row supports use full joint terminal; no root pins exported."};
}
console.log(JSON.stringify(main(),null,2));
