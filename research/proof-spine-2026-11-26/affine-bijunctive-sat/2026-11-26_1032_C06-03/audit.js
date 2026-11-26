function audit(){
  const parity=x=>{let b=0;while(x){b^=1;x&=x-1n}return b};
  const pivot=x=>x.toString(2).length-1;
  let checks=0, pairTests=0, maxStates=0;
  function assert(v,msg){checks++;if(!v)throw Error(msg)}
  function linear(eqs){
    let m=new Map();
    for(let [v,b] of eqs){while(v){let p=pivot(v);if(!m.has(p)){m.set(p,[v,b]);break}let [w,c]=m.get(p);v^=w;b^=c}if(!v&&b)return null}
    return m;
  }
  function ev(m,v){let b=0;while(v){let a=m.get(pivot(v));if(!a)return null;v^=a[0];b^=a[1]}return b}
  function basis(vs){return [...linear(vs.map(v=>[v,0])).values()].map(x=>x[0])}
  function intersect(A,B){
    let m=new Map(),out=[];
    for(let [v,t] of [...A.map(v=>[v,v]),...B.map(v=>[v,0n])]){
      while(v){let p=pivot(v);if(!m.has(p)){m.set(p,[v,t]);break}let [w,u]=m.get(p);v^=w;t^=u}
      if(!v&&t)out.push(t)
    }
    return basis(out);
  }
  function key(B,m){let k=0n;for(let i=0;i<B.length;i++){let v=ev(m,B[i]);assert(v!==null,"boundary not determined");if(v)k|=1n<<BigInt(i)}return k}
  function eqs(B,k){return B.map((v,i)=>[v,Number((k>>BigInt(i))&1n)])}
  function witness(m,q){let x=0n;for(let j=0;j<q;j++){let a=m.get(j);if(a&&(a[1]^parity(a[0]&x)))x|=1n<<BigInt(j)}return x}
  let seed=6112603;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
  function shuffle(a){for(let j=a.length-1;j>0;j--){let i=rnd(j+1);[a[i],a[j]]=[a[j],a[i]]}return a}
  function solve(q,F,random=false,verifyTables=false){
    const tokens=[];F=F.map((f,i)=>{let ids=f.v.map(v=>{tokens.push(v);return tokens.length-1});if(f.v.length===2){ids.push(tokens.length);tokens.push(f.v[0]^f.v[1])}return {...f,i,ids}});
    if(!tokens.length)return {sat:true,x:0n,width:0,nodes:0,states:0};
    const nodes=[];function tree(ids){let n={ids:new Set(ids),fac:[],B:[],tab:new Map()};nodes.push(n);if(ids.length===1)n.leaf=ids[0];else{let h=Math.floor(ids.length/2);n.l=tree(ids.slice(0,h));n.r=tree(ids.slice(h))}n.V=basis(ids.map(i=>tokens[i]));n.B=intersect(n.V,basis(tokens.filter((_,i)=>!n.ids.has(i))));return n}
    let ids=tokens.map((_,i)=>i);if(random)shuffle(ids);let root=tree(ids);
    for(let f of F){let n;if(f.ids.length===1)n=nodes.find(n=>n.leaf===f.ids[0]);else n=nodes.find(n=>n.l&&f.ids.filter(i=>n.ids.has(i)).length===2&&f.ids.some(i=>n.l.ids.has(i))&&f.ids.some(i=>n.r.ids.has(i)));assert(!!n,"unique median missing");n.fac.push(f)}
    function good(f,m){let k=0;for(let j=0;j<f.v.length;j++){let v=ev(m,f.v[j]);assert(v!==null,"median vector not in boundary span");k|=v<<j}return (f.allow>>k)&1}
    let width=0,states=0;
    function visit(n){
      width=Math.max(width,n.B.length);n.desc=[...n.fac];
      if(n.leaf!==undefined){let v=tokens[n.leaf];for(let b=0;b<2;b++){let m=linear([[v,b]]);if(m&&n.fac.every(f=>good(f,m)))n.tab.set(key(n.B,m),[[v,b]])}}
      else{visit(n.l);visit(n.r);n.desc.push(...n.l.desc,...n.r.desc);
        for(let [a,wa] of n.l.tab)for(let [b,wb] of n.r.tab){
          pairTests++;
          let m=linear([...eqs(n.l.B,a),...eqs(n.r.B,b)]);
          if(m&&n.fac.every(f=>good(f,m))){let k=key(n.B,m);if(!n.tab.has(k)){let w=[...wa,...wb];assert(linear(w)!==null,"full witnesses fail glue");n.tab.set(k,w)}}
        }
      }
      states+=n.tab.size;maxStates=Math.max(maxStates,n.tab.size);
      if(verifyTables){let want=new Set();for(let x=0n;x<(1n<<BigInt(q));x++){if(n.desc.every(f=>{let k=f.v.reduce((s,v,j)=>s|(parity(v&x)<<j),0);return (f.allow>>k)&1})){let k=n.B.reduce((s,v,j)=>s|(BigInt(parity(v&x))<<BigInt(j)),0n);want.add(k)}}assert(want.size===n.tab.size&&[...want].every(k=>n.tab.has(k)),"table support mismatch")}
    }
    visit(root);let sat=root.tab.size>0,x=0n;if(sat){x=witness(linear(root.tab.get(0n)),q);assert(F.every(f=>(f.allow>>f.v.reduce((s,v,j)=>s|(parity(v&x)<<j),0))&1),"witness rejected")}
    return {sat,x,width,nodes:nodes.length,states};
  }
  function param(n,rows){let m=linear(rows);if(!m)return null;let q=0,v=[],c=[];for(let j=0;j<n;j++){let a=m.get(j);if(!a){v[j]=1n<<BigInt(q++);c[j]=0}else{v[j]=0n;c[j]=a[1];for(let k=0;k<j;k++)if((a[0]>>BigInt(k))&1n){v[j]^=v[k];c[j]^=c[k]}}}return {q,v,c,rank:m.size}}
  function native(sizes,pins=[]){
    let C=[],n=0;for(let s of sizes){for(let i=0;i<s;i++)C.push([n+(i+s-1)%s,n+i,n+(i+1)%s]);n+=s}
    let pos=0;for(let k=0;k<sizes.length-1;k++){let next=pos+sizes[k];[C[pos+3][1],C[next][1]]=[C[next][1],C[pos+3][1]];pos=next}
    assert(C.every(c=>new Set(c).size===3),"repeated variable");
    let deg=Array(n).fill(0);C.flat().forEach(i=>deg[i]++);assert(deg.every(d=>d===3),"not cubic");
    const bit=i=>1n<<BigInt(i), rows=C.map(c=>[c.reduce((s,i)=>s^bit(i),0n),1]);pins.forEach(([i,b])=>rows.push([bit(i),b]));
    let raw=param(n,rows);if(!raw)return {sat:false,rank:null,q:null,width:0,states:0,n};
    let P,F,rounds=0;
    for(;;){
      P=param(n,rows);if(!P)return {sat:false,rank:raw.rank,q:raw.q,width:0,states:0,n,rounds};
      F=[];let add=[];
      for(let [i,j,k] of C){let vv=basis([P.v[i],P.v[j]]);let allow=0;
        for(let a=0;a<(1<<vv.length);a++){let m=linear(eqs(vv,BigInt(a)));let x=P.c[i]^ev(m,P.v[i]),y=P.c[j]^ev(m,P.v[j]);if(!(x&&y))allow|=1<<a}
        if(!allow)return {sat:false,rank:raw.rank,q:raw.q,width:0,states:0,n,rounds};
        if(allow===(1<<(1<<vv.length))-1)continue;
        if(vv.length===1){let l=P.v[i]?i:j;add.push([bit(l),P.c[l]^(allow===2?1:0)])}
        else F.push({v:vv,allow})
      }
      if(!add.length)break;rows.push(...add);rounds++;assert(rounds<=n,"closure nonprogress");
    }
    let out=solve(P.q,F,false,P.q<=7);
    if(out.sat){let x=P.v.map((v,i)=>parity(v&out.x)^P.c[i]);assert(C.every(c=>c.reduce((s,i)=>s+x[i],0)===1)&&pins.every(([i,b])=>x[i]===b),"native witness invalid")}
    if(n<=18){let ref=false;for(let x=0;x<2**n;x++){if(C.every(c=>c.reduce((s,i)=>s+((x>>i)&1),0)===1)&&pins.every(([i,b])=>((x>>i)&1)===b)){ref=true;break}}assert(ref===out.sat,"native decision mismatch")}
    return {sat:out.sat,rank:raw.rank,q:raw.q,residualQ:P.q,width:out.width,states:out.states,n,rounds};
  }
  let randomCases=0,yes=0,no=0;
  for(let t=0;t<160;t++){
    let q=2+rnd(6),F=[];for(let j=0;j<2+rnd(8);j++){let a=BigInt(1+rnd((1<<q)-1));if(rnd(4)===0)F.push({v:[a],allow:1+rnd(3)});else{let b;do{b=BigInt(1+rnd((1<<q)-1))}while(a===b);F.push({v:[a,b],allow:1+rnd(15)})}}
    let out=solve(q,F,true,true);randomCases++;out.sat?yes++:no++;
  }
  let nativeCases=[];for(let blocks of [1,2,3,4,8,16,32,64]){let s=Array(blocks).fill(6);nativeCases.push({blocks,guard:"none",...native(s)});nativeCases.push({blocks,guard:"x0=1",...native(s,[[0,1]])});nativeCases.push({blocks,guard:"x0=x1=1",...native(s,[[0,1],[1,1]])})}
  for(let s of [[4],[8],[10],[6,8],[4,8],[8,10]])nativeCases.push({sizes:s,guard:"none",...native(s)});
  // A genuinely nonaffine rank-two support must not be replaced by its hull.
  let f=[{v:[1n,2n],allow:7},{v:[1n],allow:2},{v:[2n],allow:2}];assert(!solve(2,f,true,true).sat,"hull false positive");
  // Basis change on shared forms: dense vector coordinates can still have width one.
  let dense=[];for(let i=1;i<24;i++)dense.push({v:[(1n<<BigInt(i+1))-1n,(1n<<BigInt(i))-1n],allow:7});let d=solve(24,dense,false,false);assert(d.sat,"dense chain false negative");
  return {seed:6112603,randomCases,yes,no,checks,pairTests,maxStates,nativeCases,denseControl:{width:d.width,states:d.states,sat:d.sat},notes:"Random tables checked at every node by exhaustive global phase enumeration; connected native prism chains use explicit consecutive clause-factor order, not Oum-Seymour implementation. No independent review."}
}
console.log(JSON.stringify(audit(),null,2));
