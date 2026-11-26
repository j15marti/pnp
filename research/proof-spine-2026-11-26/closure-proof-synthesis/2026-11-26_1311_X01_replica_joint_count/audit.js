function replicaAudit() {
  const A2=[[1,1],[1,1]], A3=[[1,1,1],[1,0,1],[1,1,0]], R=[0,2,1];
  let checks=0,matchCalls=0,sccCalls=0,seed=13112026;
  const ok=(x,m)=>{checks++;if(!x)throw Error(m||"assertion "+checks)};
  function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
  function match(b,pin) {
    matchCalls++;const n=b.A.length,adj=b.A.map((a,i)=>a.flatMap((v,j)=>v&&b.P.every(p=>p.row!==i||!pin.has(p.g)||((+(j===0))^p.s)===pin.get(p.g))?[j]:[]));
    let m=Array(n).fill(-1);
    function aug(i,seen){for(let j of adj[i])if(!seen[j]){seen[j]=1;if(m[j]<0||aug(m[j],seen)){m[j]=i;return true}}return false}
    for(let i=0;i<n;i++)if(!aug(i,Array(n).fill(0)))return null;
    let ans=[];m.forEach((i,j)=>ans[i]=j);return ans
  }
  const bit=(M,p)=>(+(M[p.row]===0))^p.s;
  function mk(h){return {h,B:Array.from({length:h},(_,g)=>({A:A2,P:[{g,row:0,s:0}]}))}}
  function add(I,gs,ss){I.B.push({A:A3,P:gs.map((g,j)=>({g,row:R[j],s:ss[j]||0}))})}
  function family(h,yes){const I=mk(h);for(let a=0;a<h;a++)for(let b=a+1;b<h;b++)add(I,[a,b],[0,0]);add(I,[0,1,2],[0,0,0]);add(I,[3,4,5],[yes?1:0,0,0]);return I}
  function closure(I){let f=new Map();for(;;){let change=false;for(let b of I.B){if(!match(b,f))return null;for(let g of new Set(b.P.map(p=>p.g)))if(!f.has(g)){
    let d=[];for(let x=0;x<2;x++){let p=new Map(f);p.set(g,x);if(match(b,p))d.push(x)}
    if(!d.length)return null;if(d.length===1){f.set(g,d[0]);change=true}
  }}if(!change)return f}}
  function feedback(I,f){const n=I.B.length,par=Array.from({length:n+I.h},(_,i)=>i),K=new Set();function root(i){while(par[i]!==i){par[i]=par[par[i]];i=par[i]}return i}for(let i=0;i<n;i++)for(let p of I.B[i].P)if(!f.has(p.g)){let a=root(i),b=root(n+p.g);if(a===b)K.add(p.g);else par[a]=b}return [...K].sort((a,b)=>a-b)}
  function shadow(I,f){const C=new Map();function put(c){let a=c.slice().sort((x,y)=>x[0]-y[0]||x[1]-y[1]);C.set(JSON.stringify(a),a)}
    for(let b of I.B){const gs=[...new Set(b.P.map(p=>p.g))];for(let g of gs)for(let x=0;x<2;x++){let p=new Map(f);if(p.has(g)&&p.get(g)!==x){put([[g,x^1]]);continue}p.set(g,x);if(!match(b,p))put([[g,x^1]])}
      for(let i=0;i<gs.length;i++)for(let j=i+1;j<gs.length;j++)for(let x=0;x<2;x++)for(let y=0;y<2;y++){let a=gs[i],c=gs[j],p=new Map(f);if((p.has(a)&&p.get(a)!==x)||(p.has(c)&&p.get(c)!==y))continue;p.set(a,x);p.set(c,y);if(!match(b,p))put([[a,x^1],[c,y^1]])}}
    for(let [g,x] of f)put([[g,x]]);return [...C.values()]
  }
  function sat2(h,C,pin){sccCalls++;let A=Array.from({length:2*h},()=>[]),B=A.map(()=>[]);function edge(x,y){A[x].push(y);B[y].push(x)}
    function clause(a,b){let u=2*a[0]+a[1],v=2*b[0]+b[1];edge(u^1,v);edge(v^1,u)}
    for(let c of C)clause(c[0],c[1]||c[0]);for(let [g,x] of pin)clause([g,x],[g,x]);let seen=Array(2*h).fill(false),order=[];function dfs(u){seen[u]=true;for(let v of A[u])if(!seen[v])dfs(v);order.push(u)}for(let i=0;i<2*h;i++)if(!seen[i])dfs(i);
    let comp=Array(2*h).fill(-1);function rev(u,k){comp[u]=k;for(let v of B[u])if(comp[v]===-1)rev(v,k)}let k=0;for(let i=order.length-1;i>=0;i--)if(comp[order[i]]<0)rev(order[i],k++);
    for(let i=0;i<h;i++)if(comp[2*i]===comp[2*i+1])return false;return true
  }
  function forest(I,f,K){let n=I.B.length,cut=new Set(K),A=Array.from({length:n+I.h},()=>[]);for(let i=0;i<n;i++)for(let p of I.B[i].P)if(!f.has(p.g)&&!cut.has(p.g)){A[i].push(n+p.g);A[n+p.g].push(i)}
    let seen=new Set();function go(u,pa){ok(!seen.has(u),"not forest");seen.add(u);return {u,ch:A[u].filter(v=>v!==pa).map(v=>go(v,u))}}let trees=[];for(let i=0;i<n;i++)if(!seen.has(i))trees.push(go(i,-1));return trees
  }
  function solveTree(I,T,fix){let n=I.B.length,M=Array(n),vals=new Map(fix);
    function tab(t,p){let ch=t.ch.map(c=>tab(c,t.u)),out=new Map();
      if(t.u>=n){for(let x of [0,1])if(ch.every(c=>c.out.has(x)))out.set(x,{})}
      else for(let x of p<0?[-1]:[0,1]){if(ch.some(c=>!c.out.size))continue;let f=new Map(fix);if(p>=0)f.set(p-n,x);for(let c of ch)if(c.out.size===1)f.set(c.u-n,[...c.out.keys()][0]);let m=match(I.B[t.u],f);if(m){let vv=ch.map(c=>bit(m,I.B[t.u].P.find(p=>p.g===c.u-n)));ok(vv.every((v,i)=>ch[i].out.has(v)),"child compatibility");out.set(x,{m,vv})}}
      return {u:t.u,ch,out}
    }
    function lift(t,x){let q=t.out.get(x);ok(q);if(t.u>=n){vals.set(t.u-n,x);for(let c of t.ch)lift(c,x)}else{M[t.u]=q.m;t.ch.forEach((c,i)=>lift(c,q.vv[i]))}}
    for(let t of T){let root=tab(t,-1);if(!root.out.has(-1))return null;lift(root,-1)}
    for(let i=0;i<n;i++){ok(M[i].every((j,r)=>I.B[i].A[r][j]),"original matching");for(let p of I.B[i].P)ok(bit(M[i],p)===vals.get(p.g),"original physical guard")}
    return {M,vals}
  }
  function run(I,cap,useShadow){const startM=matchCalls,startS=sccCalls,F=closure(I);if(!F)return {answer:"NO",closure:true,states:0,matchCalls:matchCalls-startM,sccCalls:sccCalls-startS};
    const K=feedback(I,F),T=forest(I,F,K),C=useShadow?shadow(I,F):[],P=new Map(F);let count=0,overflow=false,witness=null,accepted=0;
    function visit(i){if(overflow)return;if(i===K.length){if(count===cap){overflow=true;return}count++;let w=solveTree(I,T,P);if(w){accepted++;if(!witness)witness=w}return}
      for(let x of [0,1]){P.set(K[i],x);
        // Raw representative projection: each class owns a private free 2x2 block.
        let admitted=useShadow?sat2(I.h,C,P):!!match(I.B[K[i]],P);
        if(admitted)visit(i+1);P.delete(K[i]);if(overflow)break}
    }
    if(!useShadow||sat2(I.h,C,P))visit(0);
    return {answer:witness?"YES":overflow?"UNKNOWN":"NO",states:count,overflow,accepted,feedback:K.length,pins:F.size,clauses:C.length,matchCalls:matchCalls-startM,sccCalls:sccCalls-startS,witness}
  }
  function verifyGrid(I,w,scan){let off=0,sel=[],inv=[],meta=[];for(let i=0;i<I.B.length;i++){let b=I.B[i],m=w.M[i],n=b.A.length;ok(new Set(m).size===n);for(let r=0;r<n;r++){ok(b.A[r][m[r]]);sel.push(off+m[r]);meta.push([i,off,r,n])}off+=n}sel.forEach((j,i)=>inv[j]=i);ok(new Set(sel).size===off);
    if(scan)for(let i=0;i<off;i++)for(let j=0;j<off;j++){let [b,o,r,n]=meta[i],available=j>=o&&j<o+n&&I.B[b].A[r][j-o],N=+(inv[j]<i),E=+(sel[i]<=j),S=+(inv[j]<=i),W=+(sel[i]<j);ok((E===W&&S===N)||(available&&N===0&&E===1&&S===1&&W===0),"cell")}
    for(let i=0;i<I.B.length;i++)for(let p of I.B[i].P)ok(bit(w.M[i],p)===w.vals.get(p.g),"guard");
    return off
  }
  function reference(I){for(let w=0;w<(1<<I.h);w++){let p=new Map(Array.from({length:I.h},(_,i)=>[i,w>>i&1]));if(I.B.every(b=>match(b,p)))return true}return false}
  let random={yes:0,no:0},scales=[];
  for(let i=0;i<120;i++){let h=3+rnd(5),I=mk(h),r=2+rnd(9);for(let j=0;j<r;j++){let gs=[],d=2+rnd(2);while(gs.length<d){let g=rnd(h);if(!gs.includes(g))gs.push(g)}add(I,gs,gs.map(()=>rnd(2)))}let want=reference(I),z=run(I,2**h,true);ok(z.answer===(want?"YES":"NO"));random[want?"yes":"no"]++;if(want)verifyGrid(I,z.witness,true)}
  for(let h of [8,12,16,24,32,48,64]){
    let U=family(h,false),Y=family(h,true),raw=run(U,h+1,false),a=run(U,h+1,true),b=run(Y,h+1,true);
    ok(raw.answer==="UNKNOWN"&&raw.overflow,"raw cap");ok(a.answer==="NO"&&!a.overflow&&a.states===a.feedback+1,"all shadow candidates");
    ok(b.answer==="YES"&&!b.overflow&&b.states<=b.feedback+1);ok(a.pins===0&&b.pins===0,"local closure stagnation");
    let zero=new Map(Array.from({length:h},(_,i)=>[i,0]));let C=shadow(U,new Map());ok(sat2(h,C,zero));ok(!U.B.every(b=>match(b,zero)));
    let side=verifyGrid(Y,b.witness,h<=16);ok(side===2*h+3*(h*(h-1)/2+2));
    let slim=(r)=>{let {witness,...s}=r;return s};
    scales.push({guardClasses:h,gridSide:side,cells:side*side,fullCellScan:h<=16,raw:slim(raw),jointNO:slim(a),jointYES:slim(b),binaryHullNO:"SAT relaxation, not original witness"})
  }
  let parity=[];for(let h of [4,8,12,16]){let visits=0,leaves=0;function p(i){visits++;if(i===h){leaves++;return}if(i+1<h){p(i+1);p(i+1)}}p(0);ok(visits===2**h-1&&leaves===0);parity.push({h,separatePrefixNodes:visits,jointModels:0})}
  return {checks,matchCalls,sccCalls,random,scales,parity,seed:13112026}
}
console.log(JSON.stringify(replicaAudit(),null,2));
