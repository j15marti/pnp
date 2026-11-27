function audit(){
  const R={random:0,rootComparisons:0,conditionalComparisons:0,hcMasks:0,matchingMasks:0,neighbors:0,lifts:0,controls:[],failures:0}; 
  function check(t){if(!t){R.failures++;throw Error("assertion failed");}}
  const bits=m=>{const r=[];for(let i=0;m;i++,m>>>=1)if(m&1)r.push(1<<i);return r};
  const subs=m=>{const r=[];for(let a=m;;a=(a-1)&m){r.push(a);if(!a)break;}return r};
  function builder(){let c=[];const add=(op,a,b)=>{c.push({op,a,b});return c.length-1}; const fold=(op,ls)=>ls.reduce((a,b)=>add(op,a,b),add(op==="and"?"1":"0"));return {c,add,fold}}
  function compile(c,root,m){
    let P=[],M=[],S=[],K=[],B=c.map(()=>0),reachable=c.map(()=>false);
    function visit(g){if(reachable[g])return;reachable[g]=true;const {op,a,b}=c[g];if(op==="and"||op==="or"){visit(a);visit(b);}}visit(root);
    for(let g=0;g<c.length;g++){const {op,a,b}=c[g];P[g]=op==="p"?1<<a:0;M[g]=op==="n"?1<<a:0;K[g]=0;
      if(op==="and"||op==="or"){P[g]=P[a]|P[b];M[g]=M[a]|M[b];if(op==="and")K[g]=(P[a]&M[b])|(M[a]&P[b]);} S[g]=P[g]|M[g];}
    for(let g=root;g>=0;g--)if(reachable[g]){const {op,a,b}=c[g];if(op==="and"||op==="or")for(const h of [a,b]) B[h]|=(B[g]|K[g])&S[h];}
    const out=builder(),T=[];const zero=out.add("0"),one=out.add("1"),X=Array.from({length:m},(_,i)=>out.add("p",i));
    function gate(op,a,b){if(op==="and"){if(a===zero||b===zero)return zero;if(a===one)return b;if(b===one)return a;}else{if(a===one||b===one)return one;if(a===zero)return b;if(b===zero)return a;}if(a===b)return a;return out.add(op,a,b)}
    function aggregate(h,scope){let map=new Map();for(const [alpha,f] of T[h]){let k=alpha&scope;map.set(k,gate("or",map.get(k)??zero,f));}return map;}
    let tariff=0;
    for(let g=0;g<=root;g++)if(reachable[g]){const {op,a,b}=c[g], E=B[g]|K[g];tariff+=subs(E).length;let table=new Map();T[g]=table;
      if(op==="and"||op==="or"){
        const U=aggregate(a,E&S[a]),V=aggregate(b,E&S[b]);for(const eta of subs(E)){let alpha=eta&B[g];let f=U.get(eta&S[a])??zero,h=V.get(eta&S[b])??zero;let z=gate(op,f,h);table.set(alpha,gate("or",table.get(alpha)??zero,z));}
      }else for(const alpha of subs(B[g])){let z=op==="1"?one:op==="0"?zero:op==="p"?((B[g]&(1<<a))&&!(alpha&(1<<a))?zero:X[a]):alpha&(1<<a)?zero:one;table.set(alpha,z);}
      // Parent pins outside chosen OR child must remain affordable.
      for(const [alpha,f] of table){let z=f;for(const bit of bits(alpha)) z=gate("and",z,X[Math.log2(bit)]);table.set(alpha,z);}
    }
    return {c:out.c,root:T[root].get(0),T,B,K,S,tariff,width:Math.max(...B.map(z=>bits(z).length))};
  }
  function truth(c,m){const n=1<<m,all=(1n<<BigInt(n))-1n,X=[];for(let i=0;i<m;i++){let a=0n;for(let x=0;x<n;x++)if(x&(1<<i))a|=1n<<BigInt(x);X.push(a);}
    let z=[];for(const {op,a,b} of c)z.push(op==="0"?0n:op==="1"?all:op==="p"?X[a]:op==="n"?all^X[a]:op==="and"?z[a]&z[b]:z[a]|z[b]);return z;}
  const at=(z,x)=>Boolean((z>>BigInt(x))&1n);
  function test(c,root,m,kind,detail=false){const C=compile(c,root,m),orig=truth(c,m),out=truth(C.c,m);let n=1<<m;
    for(let x=0;x<n;x++){let expected=subs(x).some(y=>at(orig[root],y));check(at(out[C.root],x)===expected);R.rootComparisons++;if(kind==="HC")R.hcMasks++;if(kind==="PM")R.matchingMasks++;}
    if(detail)for(let g=0;g<C.T.length;g++)if(C.T[g])for(const [alpha,id] of C.T[g])for(let x=0;x<n;x++){const expected=subs(x&C.S[g]).some(y=>(y&C.B[g])===alpha&&at(orig[g],y));check(at(out[id],x)===expected);R.conditionalComparisons++;}
    return {C,orig,out};
  }
  function perms(a){if(!a.length)return [[]];return a.flatMap((x,i)=>perms(a.filter((_,j)=>i!==j)).map(p=>[x,...p]));}
  function HC(n,exact,guard){const {c,add,fold}=builder(),edges=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(i!==j)edges.push([i,j]);let P=edges.map((_,i)=>add("p",i)),M=edges.map((_,i)=>add("n",i));
    const tours=perms(Array.from({length:n-1},(_,i)=>i+1)).map(p=>[0,...p]).map(p=>p.reduce((m,i,k)=>m|(1<<edges.findIndex(([a,b])=>a===i&&b===p[(k+1)%n])),0));
    let f=fold("or",tours.map(t=>fold("and",P.filter((_,i)=>t&(1<<i)).concat(exact?M.filter((_,i)=>!(t&(1<<i))):[]))));
    if(guard)f=add("or",f,add("and",P[0],M[0]));
    return {c,f,m:edges.length,tours};
  }
  for(let n=2;n<=4;n++){const {c,f,m,tours}=HC(n,true,true),{C,out}=test(c,f,m,"HC",n<=3);for(let x=0;x<1<<m;x++){const exp=tours.some(t=>(t&x)===t);check(at(out[C.root],x)===exp);if(exp){let y=x;for(const bit of bits(x))if(at(out[C.root],y^bit))y^=bit;check(tours.includes(y));R.lifts++;}}
    for(const t of tours){check(at(out[C.root],t));for(const bit of bits(t)){check(!at(out[C.root],t^bit));R.neighbors++;}}
    R.controls.push({kind:"HC",n,source:c.length,compiled:C.c.length,width:C.width,tariff:C.tariff});
  }
  // Compact exact verifier: row and column one-hot, directed reachability from 0.
  for(let n=2;n<=3;n++){const {c,add,fold}=builder(),edge=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++)if(i!==j)edge.push([i,j]);const P=edge.map((_,i)=>add("p",i)),M=edge.map((_,i)=>add("n",i));let constraints=[];
    for(let col=0;col<2;col++)for(let i=0;i<n;i++){let es=edge.map((_,j)=>j).filter(j=>edge[j][col]===i);constraints.push(fold("or",es.map(j=>P[j])));for(let j=0;j<es.length;j++)for(let k=j+1;k<es.length;k++)constraints.push(add("or",M[es[j]],M[es[k]]));}
    let reach=Array.from({length:n},(_,i)=>add(i===0?"1":"0"));for(let k=0;k<n-1;k++)reach=reach.map((old,j)=>fold("or",[old,...edge.map(([a,b],i)=>b===j?add("and",reach[a],P[i]):null).filter(x=>x!==null)]));const f=fold("and",[...constraints,...reach]);const {C,out}=test(c,f,edge.length,"HC",true);const tours=HC(n,true,false).tours;for(let x=0;x<1<<edge.length;x++)check(at(out[C.root],x)===tours.some(t=>(t&x)===t));R.controls.push({kind:"compact HC verifier",n,source:c.length,compiled:C.c.length,width:C.width,tariff:C.tariff});
  }
  for(let n=2;n<=3;n++){const {c,add,fold}=builder(),P=Array.from({length:n*n},(_,i)=>add("p",i)),M=P.map((_,i)=>add("n",i));let ts=perms(Array.from({length:n},(_,i)=>i)).map(p=>p.reduce((x,j,i)=>x|(1<<(i*n+j)),0));let f=fold("or",ts.map(t=>fold("and",P.filter((_,i)=>t&(1<<i)).concat(M.filter((_,i)=>!(t&(1<<i)))))));const {C,out}=test(c,f,n*n,"PM",n===2);
    function augment(x){let mate=Array(n).fill(-1);function go(i,seen){for(let j=0;j<n;j++)if((x&(1<<(i*n+j)))&&!seen[j]){seen[j]=true;if(mate[j]<0||go(mate[j],seen)){mate[j]=i;return true;}}return false;}return Array.from({length:n},(_,i)=>i).every(i=>go(i,Array(n).fill(false)));}
    for(let x=0;x<1<<(n*n);x++)check(at(out[C.root],x)===augment(x));R.controls.push({kind:"PM",n,width:C.width,tariff:C.tariff});
  }
  let seed=20261126;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n;}
  for(let trial=0;trial<120;trial++){const m=5,{c,add}=builder();for(let i=0;i<m;i++){add("p",i);add("n",i);}for(let i=0;i<24;i++)add(rand(2)?"and":"or",rand(c.length),rand(c.length));test(c,c.length-1,m,"random",true);R.random++;}
  // Opposite-polarity conflict is necessary. Same-polarity repeated sub-DAGs do not contribute.
  {const {c,add}=builder(),p=add("p",0),n=add("n",0),f=add("and",p,n);const {C,out}=test(c,f,1,"conflict",true);check(!at(out[C.root],1));R.controls.push({kind:"x AND not x",width:C.width});}
  {const {c,add,fold}=builder(),p=Array.from({length:12},(_,i)=>add("p",i));let f=fold("and",p.map((x,i)=>add("or",x,p[(i+1)%p.length])));const {C}=test(c,f,12,"positive");check(C.width===0);R.controls.push({kind:"positive overlapping CNF",width:C.width,tariff:C.tariff});}
  {const {c,add,fold}=builder(),p=[0,1,2].map(i=>add("p",i)),q=[0,1,2].map(i=>add("n",i));const f=fold("or",[1,2,4,7].map(t=>fold("and",p.map((x,i)=>(t>>i)&1?x:q[i]))));const {C,out}=test(c,f,3,"odd parity",true);for(let x=0;x<8;x++)check(at(out[C.root],x)===(x!==0));R.controls.push({kind:"odd parity",width:C.width});}
  return R;
}
console.log(JSON.stringify(audit(),null,2));
