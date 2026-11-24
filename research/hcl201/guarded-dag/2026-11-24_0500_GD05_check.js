// GD05 standalone Node runner; deterministic seed and exact small binary controls.
function run(){
 let seed=0x2010500;const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n;};
 const bit=(x,i)=>(x>>>i)&1, parity=x=>{let p=0;while(x){p^=1;x&=x-1;}return p;};
 const mix=(B,m)=>B.reduce((a,v,i)=>a^(bit(m,i)?v:0),0);
 const all=n=>Array.from({length:1<<n},(_,i)=>i);
 function* low(n,k,start=0,m=0){yield m;if(k)for(let i=start;i<n;i++)yield* low(n,k-1,i+1,m|(1<<i));}
 // Linear map columns, returning a section on its image and a kernel basis.
 function map(cols,d){let rows=Array(d).fill(null),K=[];
  for(let i=0;i<cols.length;i++){let v=cols[i],a=1<<i;for(let j=d-1;j>=0;j--)if(bit(v,j)){if(rows[j]){v^=rows[j][0];a^=rows[j][1];}else{rows[j]=[v,a];break;}}if(!v)K.push(a);}
  function reduce(v){let a=0;for(let j=d-1;j>=0;j--)if(bit(v,j)&&rows[j]){v^=rows[j][0];a^=rows[j][1];}return [v,a];}
  return {reduce,K,rank:rows.filter(Boolean).length};
 }
 // Solve vector-valued affine equations f(a + B*y)=0.
 function affine(f,a,B,d){let c=f(a),L=map(B.map(v=>f(a^v)^c),d),[rem,m]=L.reduce(c);
  return rem?null:{a:a^mix(B,m),B:L.K.map(k=>mix(B,k))};
 }
 function backdoor(f,n,d){let U=Array.from({length:n},(_,i)=>1<<i),steps=0;
  while(true){let found=false;for(let k=0;k<d;k++){const polar=(u,v)=>bit(f(u)^f(v)^f(u^v)^f(0),k);
    let cols=U.map(v=>U.reduce((a,u,j)=>a|(polar(u,v)<<j),0));
    if(cols.some(Boolean)){const L=map(cols,U.length);U=L.K.map(m=>mix(U,m));steps++;found=true;break;}}
   if(!found)break;
  }
  let C=[],B=U.slice();for(let i=0;i<n;i++){let v=1<<i;if(map(B,n).reduce(v)[0]){B.push(v);C.push(v);}}
  return {U,C,steps};
 }
 const guard=(f,x)=> (parity(f.g[0]&x)^f.gc[0])|((parity(f.g[1]&x)^f.gc[1])<<1);
 function prep(I){const B=I.F.flatMap(f=>f.W),L=map(B,I.d);
  function states(x){return I.F.map(f=>f.rows[guard(f,x)]);}
  function rhs(x){return states(x).reduce((a,z)=>a^z.a,I.c);}
  function eq(x){let v=L.reduce(rhs(x))[0];states(x).forEach((z,i)=>{if(!z.ok)v|=1<<(I.d+i);});if(I.pin!==null&&parity(I.pin[0]&x)!==I.pin[1])v|=1<<(I.d+I.F.length);return v;}
  let e=I.d+I.F.length+(I.pin===null?0:1);
  // Every affine equation in the current equation span is exposed before branching.
  // For this small implementation, enumerate the degree<=2 coefficient rows,
  // row-reduce quadratic parts, and impose their kernel's affine consequences.
  let a=0,X=Array.from({length:I.n},(_,i)=>1<<i),closure=0;
  while(true){const f=y=>eq(a^mix(X,y)),qcols=[];let idx=0;
    for(let j=0;j<X.length;j++)for(let i=0;i<j;i++)qcols.push(f(0)^f(1<<i)^f(1<<j)^f((1<<i)|(1<<j)));
    const trans=Array.from({length:e},(_,i)=>qcols.reduce((m,v,j)=>m|(bit(v,i)<<j),0));
    let nulls=map(trans,qcols.length).K;
    const af=y=>nulls.reduce((m,v,j)=>m|(parity(v&f(y))<<j),0);
    let sol=affine(af,0,Array.from({length:X.length},(_,i)=>1<<i),nulls.length);
    if(!sol)return {L,empty:true,closure};
    if(sol.B.length===X.length)break;
    a^=mix(X,sol.a);X=sol.B.map(m=>mix(X,m));closure++;
  }
  const f=y=>eq(a^mix(X,y)),bd=backdoor(f,X.length,e);
  let cells=[];for(let b of all(bd.C.length)){let z=affine(f,mix(bd.C,b),bd.U,e);if(z)cells.push({a:a^mix(X,z.a),B:z.B.map(v=>mix(X,v))});}
  function lift(x,z,t){let [rem,u]=L.reduce(rhs(x));if(rem||eq(x))throw Error("bad selector");u^=mix(L.K,z);
    let p=0,pos=0,off=0;for(let i=0;i<I.F.length;i++){let F=I.F[i],R=states(x)[i],v=R.p;
      for(let j=0;j<F.W.length;j++)if(bit(u,off++))v^=R.P[j];
      if(bit(t,i))v^=R.K; p|=v<<pos;pos+=F.pdim;}
    return x|(p<<I.n);
  }
  return {L,cells,lift,b:bd.C.length,closure,empty:false};
 }
 function feature(y,n,k){let v=1n,pos=1n;for(let i=0;i<n;i++){if(bit(y,i))v|=1n<<pos;pos++;}if(k===2)for(let j=0;j<n;j++)for(let i=0;i<j;i++){if(bit(y,i)&&bit(y,j))v|=1n<<pos;pos++;}return v;}
 function basis(){let rows=new Map();function reduce(v){while(v){let j=v.toString(2).length-1;if(!rows.has(j))break;v^=rows.get(j);}return v;}return {rows,reduce,add(v){v=reduce(v);if(!v)return false;rows.set(v.toString(2).length-1,v);return true;}};}
 function reference(I){let S=new Set();for(let x of all(I.n)){if(I.pin!==null&&parity(I.pin[0]&x)!==I.pin[1])continue;
   function go(i,s,p,off){if(i===I.F.length){if(s===I.c)S.add(x|(p<<I.n));return;}let F=I.F[i],R=F.rows[guard(F,x)];if(!R.ok)return;
    for(let u of all(F.W.length))for(let t of [0,1])go(i+1,s^R.a^mix(F.W,u),p|((R.p^mix(R.P,u)^(t?R.K:0))<<off),off+F.pdim);}
   go(0,0,0,0);}return S;}
 let R={seed:"0x2010500",random:0,SAT:0,UNSAT:0,targets:0,featureChecks:0,referenceTuples:0,candidates:0,basisWitnesses:0,closureRounds:0,maxBackdoor:0,quartic:null,scaling:[],errors:0};
 function check(I,label){let S=reference(I),P=prep(I),outDim=I.n+I.F.reduce((s,f)=>s+f.pdim,0);
  R.targets++;R[S.size?"SAT":"UNSAT"]++;R.referenceTuples+=S.size;R.closureRounds+=P.closure;R.maxBackdoor=Math.max(R.maxBackdoor,P.b||0);
  if(Boolean(S.size)!==Boolean(!P.empty&&P.cells.length))throw Error("decision "+label);
  for(let k of [1,2]){let B=basis(),A=basis();for(let y of S)A.add(feature(y,outDim,k));
   if(!P.empty)for(let C of P.cells)for(let x of low(C.B.length,4*k))for(let zt of low(P.L.K.length+I.F.length,k)){
    let y=P.lift(C.a^mix(C.B,x),zt&((1<<P.L.K.length)-1),zt>>>P.L.K.length);R.candidates++;
    if(!S.has(y))throw Error("invalid lift "+label);
    if(B.add(feature(y,outDim,k)))R.basisWitnesses++;
   }
   if(A.rows.size!==B.rows.size||[...A.rows.values()].some(v=>B.reduce(v)))throw Error("feature span "+label);
   R.featureChecks++;
  }return {S,P};
 }
 for(let i=0;i<160;i++){let n=2+rand(3),d=2+rand(3),F=[];
  for(let j=0,h=1+rand(3);j<h;j++){let W=rand(4)?[1+rand((1<<d)-1)]:[],pdim=1+rand(2);
   F.push({g:[rand(1<<n),rand(1<<n)],gc:[rand(2),rand(2)],W,pdim,rows:all(2).map(()=>({ok:rand(5)!==0,a:rand(1<<d),p:rand(1<<pdim),P:W.map(()=>rand(1<<pdim)),K:rand(1<<pdim)}))});}
  let I={n,d,F,pin:rand(3)?null:[rand(1<<n),rand(2)],c:0};
  for(let c of all(d)){I.c=c;check(I,i+":"+c);}R.random++;
 }
 let I={n:4,d:1,c:0,pin:null,F:[{g:[1,2],gc:[0,0],W:[1],pdim:1,rows:all(2).map(g=>({ok:true,a:0,p:0,P:[g===3?1:0],K:0}))},{g:[4,8],gc:[0,0],W:[],pdim:1,rows:all(2).map(g=>({ok:true,a:g===3?1:0,p:0,P:[],K:0}))}]};
 let Q=check(I,"quartic");let low2=[...Q.S].filter(y=>parity(y&15)===0); // direct check below
 let le2=[...low(4,2)];if(![...Q.S].every(y=>bit(y,4)===((y&15)===15?1:0))||[...Q.S].some(y=>le2.includes(y&15)&&bit(y,4)))throw Error("quartic");
 R.quartic={tuples:Q.S.size,protectedOne:[...Q.S].filter(y=>bit(y,4)).length,weightLE2:le2.length};
 // Large analytic independent syndrome directions. For each two-bit selector x,
 // u_i=x0*x1 is forced by the target, p_i=t_i+x0*x1*u_i.
 // Thus the joint protected relation is exactly the full cube on h+2 bits.
 // Enumerate only t of Hamming weight <=2 per selector and verify all generated lifts.
 function bigFeature(y,n){let v=1n,pos=1n;for(let i=0;i<n;i++){if((y>>BigInt(i))&1n)v|=1n<<pos;pos++;}for(let j=0;j<n;j++)for(let i=0;i<j;i++){if(((y>>BigInt(i))&1n)&&((y>>BigInt(j))&1n))v|=1n<<pos;pos++;}return v;}
 for(let h of [8,16,32,64]){let B=basis(),candidates=0,H=(1n<<BigInt(h))-1n;
  for(let x=0;x<4;x++){let u=x===3?H:0n,offset=u;if((u^offset)!==0n)throw Error("target");
   function test(t){let p=t^u,y=BigInt(x)|(p<<2n);if((p^t)!==u)throw Error("lift");B.add(bigFeature(y,h+2));candidates++;}
   test(0n);for(let i=0;i<h;i++){test(1n<<BigInt(i));for(let j=0;j<i;j++)test((1n<<BigInt(i))|(1n<<BigInt(j)));}}
  let expected=1+h+2+(h+2)*(h+1)/2;if(B.rows.size!==expected)throw Error("scale");
  R.scaling.push({r:h,b:0,selectorBits:2,freeBits:h,candidates,rank:expected,fullTuples:(1n<<BigInt(h+2)).toString(),outsideImageUNSAT:true});}
 return R;
}
console.log(JSON.stringify(run(),null,2));