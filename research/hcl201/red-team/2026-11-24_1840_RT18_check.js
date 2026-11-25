function run(){
  const stats={assertions:0,gaussian:0,closureScans:0,closureRows:0,edgeJobs:0,convolutionJobs:0,peakSyndromes:0,randomSAT:0,randomUNSAT:0,bruteWords:0,rectangleTests:0,scaling:[]};
  const ck=(v,m)=>{stats.assertions++;if(!v)throw Error(m)};
  let rng=0x53a9d213; const rand=n=>{rng^=rng<<13;rng^=rng>>>17;rng^=rng<<5;return (rng>>>0)%n};
  const bit=i=>1n<<BigInt(i), dot=(a,b)=>{let x=a&b,r=0;while(x){r^=1;x&=x-1n}return r};
  const bits=x=>{let a=[];while(x){let b=x&-x;a.push(b);x^=b}return a};
  const basis=vs=>{let m=new Map();for(let v of vs){while(v){let p=v&-v;if(m.has(p))v^=m.get(p);else{m.set(p,v);break}}}return [...m.values()]};
  const inspan=(v,B)=>basis([...B,v]).length===B.length;
  const union=(A,B)=>!A?B:!B?A:{a:A.a,B:basis([...A.B,...B.B,A.a^B.a])};
  const sum=(A,B)=>!A||!B?null:{a:A.a^B.a,B:basis([...A.B,...B.B])};
  const solve=(rows,mask)=>{stats.gaussian++;let piv=new Map();for(let [v,b] of rows){if(v&~mask)throw Error("out of scope");while(v){let p=v&-v;if(piv.has(p)){let [w,c]=piv.get(p);v^=w;b^=c}else{piv.set(p,[v,b]);break}}if(!v&&b)return null}
    const P=[...piv.keys()].sort((a,b)=>a>b?-1:a<b?1:0);
    let a=0n;for(let p of P){let [v,b]=piv.get(p);if(dot(v,a)!==b)a^=p}
    let B=[];for(let f of bits(mask)){if(piv.has(f))continue;let z=f;for(let p of P)if(dot(piv.get(p)[0],z))z^=p;B.push(z)}
    return {a,B};
  };
  const maskOf=I=>I.reduce((m,b)=>m|b,0n);
  const maskRows=(p,inc)=>{let rows=[];for(let e of inc)rows.push(...p.mar[e]);for(let h=0;h<p.k;h++)rows.push([inc.reduce((v,e)=>v^p.H[e][h],0n),(p.b>>h)&1]);if(p.priv&&!p.free)rows.push([p.priv^p.shift,p.off]);return rows};
  const checkPacket=(p,inc,w)=>maskRows(p,inc).every(([v,b])=>dot(v,w)===b);
  function makeTree(par,r,privateBits=true){
    const n=par.length,inc=Array.from({length:n},()=>[]),edges=[],ps=[];let d=0;
    for(let j=1;j<n;j++){let e=j-1,I=[];for(let z=0;z<r[e];z++)I.push(bit(d++));edges.push({i:par[j],j,mask:maskOf(I),I});inc[par[j]].push(e);inc[j].push(e)}
    for(let j=0;j<n;j++)ps.push(privateBits?bit(d++):0n);
    return {n,par,inc,edges,ps,d,mask:(1n<<BigInt(d))-1n,packets:Array.from({length:n},()=>[])};
  }
  const packet=(T,i,k=0)=>({k,b:0,mar:Object.fromEntries(T.inc[i].map(e=>[e,[]])),H:Object.fromEntries(T.inc[i].map(e=>[e,Array(k).fill(0n)])),priv:T.ps[i],free:true,shift:0n,off:0});
  const localWord=(T,i,w)=>T.packets[i].some(p=>checkPacket(p,T.inc[i],w));
  const legal=(T,w)=>T.packets.every((_,i)=>localWord(T,i,w));
  function closure(T){
    let G=[],B=[];for(;;){let changed=false;for(let i=0;i<T.n;i++){stats.closureScans++;let P=null;for(let p of T.packets[i])P=union(P,solve([...G,...maskRows(p,T.inc[i])],T.mask));if(!P)return {unsat:true,rows:G.length};
      const ann=solve(P.B.map(v=>[v,0]),T.mask).B;
      for(let v of ann)if(!inspan(v,B)){B=basis([...B,v]);G.push([v,dot(v,P.a)]);stats.closureRows++;changed=true;break}
      if(changed)break;
    }if(!changed)return {unsat:false,rows:G.length};}
  }
  function terminal(T){
    // Supplied marginal/coupling/section adapter, checked for exact projected marginal ranks on small random inputs below.
    const M=Array.from({length:T.n},()=>[]);
    const loc=(p,a)=>({a:p.priv&&!p.free&&p.off?p.priv:0n,B:p.priv&&p.free?[p.priv]:[]});
    const synRows=(p,e,s)=>p.H[e].map((v,h)=>[v,(s>>h)&1]);
    const edgePayload=(e,p,q,s,t)=>{stats.edgeJobs++;const E=T.edges[e],A=solve([...p.mar[e],...q.mar[e],...synRows(p,e,s),...synRows(q,e,t)],E.mask);if(!A)return null;
      const f=w=>w^(p.priv&&!p.free&&dot(p.shift,w)?p.priv:0n)^(q.priv&&!q.free&&dot(q.shift,w)?q.priv:0n);
      return {a:f(A.a),B:basis(A.B.map(f))};
    };
    for(let i=T.n-1;i>=0;i--){
      const children=T.inc[i].filter(e=>T.edges[e].i===i);
      for(let p of T.packets[i]){
        let D=new Map([[0,loc(p)]]),size=2**p.k;
        for(let e of children){let j=T.edges[e].j,Q=new Map();
          for(let s=0;s<size;s++)for(let l=0;l<T.packets[j].length;l++){let q=T.packets[j][l];for(let [t,A] of M[j][l]){
            let X=sum(A,edgePayload(e,p,q,s,t));if(X)Q.set(s,union(Q.get(s),X));
          }}
          let next=new Map();for(let [a,A] of D)for(let [b,B] of Q){stats.convolutionJobs++;next.set(a^b,union(next.get(a^b),sum(A,B)))}
          D=next;stats.peakSyndromes=Math.max(stats.peakSyndromes,D.size);
        }
        let out=new Map();if(i===0){if(D.has(p.b))out.set(0,D.get(p.b))}else{for(let [a,A] of D)out.set(a^p.b,A)}M[i].push(out);
      }
    }
    return M[0].reduce((A,B)=>union(A,B.get(0)),null);
  }
  function brute(T){let H=null,count=0;for(let w=0n;w<=T.mask;w++){stats.bruteWords++;if(legal(T,w)){count++;H=union(H,{a:w,B:[]})}}return {H,count}}
  function compare(T,doClosure=true){
    let C=doClosure?closure(T):null,A=terminal(T),B=brute(T);
    ck(!!A===!!B.H,"label");if(C?.unsat)ck(!A,"closure sound");
    if(A){ck(legal(T,A.a),"anchor");ck(A.B.length===B.H.B.length,"hull rank");ck(inspan(A.a^B.H.a,B.H.B),"anchor coset");for(let v of A.B)ck(inspan(v,B.H.B),"hull basis")}
    return {sat:!!A,rank:A?.B.length??null,count:B.count,closure:C};
  }
  // Independently generate small affine packets, then certify exact marginals / residual rank
  // by deriving the projection rank and declining overdescribed random packets for the rank audit.
  function packetAudit(T,i,p){
    let scope=maskOf(T.inc[i].map(e=>T.edges[e].mask))|p.priv;
    let A=solve(maskRows(p,T.inc[i]),scope);if(!A)return false;
    let total=0,edgeMask=scope&~p.priv;
    for(let e of T.inc[i]){let em=T.edges[e].mask,M=solve(p.mar[e],em);let B=basis(A.B.map(v=>v&em));if(!M||B.length!==M.B.length||!inspan((A.a^M.a)&em,M.B))return false;total+=B.length}
    return total-basis(A.B.map(v=>v&edgeMask)).length===p.k;
  }
  for(let it=0;it<80;it++){
    let n=2+rand(4),par=[-1];for(let i=1;i<n;i++)par.push(rand(i));let T=makeTree(par,Array(n-1).fill(2));
    for(let i=0;i<n;i++){
      let count=1+rand(3);
      for(let l=0;l<count;l++){
        let p=packet(T,i,T.inc[i].length>=2?rand(2):0);p.b=rand(2**p.k);p.free=!!rand(2);p.off=rand(2);
        for(let e of T.inc[i]){let E=T.edges[e],m=E.I[rand(2)];if(rand(3)===0)p.mar[e].push([m,rand(2)]);if(p.k)p.H[e][0]=E.I[0];if(rand(2))p.shift^=E.I[rand(2)]}
        if(!packetAudit(T,i,p)){p=packet(T,i,0);p.free=false;p.off=rand(2);for(let e of T.inc[i]){let E=T.edges[e];if(rand(2))p.mar[e].push([E.I[rand(2)],rand(2)]);if(rand(2))p.shift^=E.I[rand(2)]}}
        ck(packetAudit(T,i,p),"adapter audit");T.packets[i].push(p);
      }
    }
    let a=compare(T);if(a.sat)stats.randomSAT++;else stats.randomUNSAT++;
  }
  // Verify exact positive rectangle cover formula on small full-marginal affine relations.
  for(let it=0;it<100;it++){
    let l=2+rand(4),k=1+rand(2),H=Array.from({length:l},()=>[rand(2**k),rand(2**k)]),b=rand(2**k);
    let feasible=new Set(),counts=new Map(),marg=Array.from({length:l},()=>new Set());
    for(let w=0;w<4**l;w++){let x=w,vals=[],syn=0;for(let j=0;j<l;j++){let y=x&3;x>>=2;let s=(y&1?H[j][0]:0)^(y&2?H[j][1]:0);vals.push(s);syn^=s}if(syn===b){let key=vals.join(",");feasible.add(key);counts.set(key,(counts.get(key)||0)+1);for(let j=0;j<l;j++)marg[j].add(vals[j])}}
    if(!feasible.size)continue;
    let prod=1;for(let j=0;j<l;j++)prod*=marg[j].size;
    let all=new Set([0]);for(let s of marg){let next=new Set();for(let x of all)for(let y of s)next.add(x^y);all=next}
    ck(feasible.size===prod/all.size,"syndrome tuple count");
    // A rectangle cannot contain two distinct tuples: replacing a single differing block violates the target.
    let list=[...feasible].map(s=>s.split(",").map(Number));for(let j=1;j<list.length;j++){let a=list[0],c=list[j],h=a.findIndex((v,i)=>v!==c[i]);ck(h>=0&&(a.reduce((x,y)=>x^y,0)^a[h]^c[h])!==b,"rectangle firewall")}
    stats.rectangleTests++;
  }
  // Nonlinear branch gadget: s=0 or (s=1 and y=11); leaf y != 11.
  // Global support has all s=0 and arbitrary legal y, but every owner-local hull
  // is full apart from the center parity, so local affine closure stalls.
  function family(n,b){
    let par=[-1];for(let i=0;i<n;i++)par.push(0);for(let i=0;i<n;i++)par.push(i+1);
    let T=makeTree(par,[...Array(n).fill(1),...Array(n).fill(2)],false),p=packet(T,0,1);p.b=b;
    for(let e of T.inc[0])p.H[e][0]=T.edges[e].I[0];T.packets[0].push(p);
    for(let i=1;i<=n;i++){let a=i-1,e=n+i-1,s=T.edges[a].I[0],y=T.edges[e].I;
      let P=packet(T,i),Q=packet(T,i);P.mar[a].push([s,0]);Q.mar[a].push([s,1]);Q.mar[e].push([y[0],1],[y[1],1]);T.packets[i].push(P,Q);
      let U=packet(T,n+i),V=packet(T,n+i);U.mar[e].push([y[0],0]);V.mar[e].push([y[1],0]);T.packets[n+i].push(U,V);
    }return T;
  }
  for(let n of [2,3,4,8,16,64,128])for(let b of [0,1]){
    let T=family(n,b),C=n<=16?closure(T):null,old=stats.edgeJobs,A=terminal(T);ck(!!A===(b===0),"family label");if(C)ck(!C.unsat&&C.rows===1,"stagnant closure");
    if(A){ck(legal(T,A.a),"family witness");ck(A.B.length===2*n,"family hull rank")}
    if(n<=4){let B=brute(T);ck(B.count===(b?0:3**n),"family independent count");ck(!!B.H===!!A,"family independent label")}
    stats.scaling.push({n,b,rank:A?.B.length??null,closure:C,edgeJobs:stats.edgeJobs-old,flatPositiveLabels:(1n<<BigInt(n-1)).toString()});
  }
  return stats;
}
console.log(JSON.stringify(run(),null,2));
