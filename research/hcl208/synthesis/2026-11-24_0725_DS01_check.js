function runDS01(){
  const stats={seed:20801,systems:0,sat:0,unsat:0,referenceAssignments:0,tableEntries:0,twistedMoments:0,cycleTerms:0,noJoinMoments:0,relativeProbes:0,forcedRelative:0,forcedUnary:0,unaryProbes:0,searchChoices:0,verifiedWitnesses:0,glueChecks:0,glueWitnesses:0,hostile:null,controls:[],discrepancies:0};
  let seed=stats.seed; const rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n;};
  const assert=(x,msg)=>{if(!x)throw Error(msg)};
  const pop=x=>{let n=0;while(x){x&=x-1;n++}return n};
  const sign=x=>pop(x)%2?-1n:1n;
  const power=(a,n)=>a**BigInt(n);
  const valid=(F,x)=>F.every(c=>{const a=c.map(([v,s])=>((x>>v)&1)^s);return a.some(t=>t!==a[0])});
  function brute(n,F,B){const a=Array(1<<B.length).fill(0n);for(let x=0;x<(1<<n);x++){stats.referenceAssignments++;if(valid(F,x)){let k=0;B.forEach((v,j)=>k|=((x>>v)&1)<<j);a[k]++;}}return a}
  function backend(n,F){
    const m=F.length, edges=[],adj=Array.from({length:n+m},()=>[]);let signs=0;
    F.forEach((c,i)=>c.forEach(([v,s])=>{const e=edges.length;edges.push([v,n+i]);adj[v].push([n+i,e]);adj[n+i].push([v,e]);if(s)signs|=1<<e}));
    assert(edges.length<31&&n+m<31,"small reference backend only");
    const par=Array(n+m).fill(-2),pe=Array(n+m).fill(-1),order=[];let tree=0;
    for(let r=0;r<n+m;r++)if(par[r]===-2){par[r]=-1;const q=[r];for(let i=0;i<q.length;i++){const v=q[i];order.push(v);for(const [u,e] of adj[v])if(par[u]===-2){par[u]=v;pe[u]=e;tree|=1<<e;q.push(u)}}}
    function join(p){let a=0;for(let i=order.length-1;i>=0;i--){const v=order[i];if(((p>>v)&1)===0)continue;if(par[v]<0)return null;p^=(1<<v)|(1<<par[v]);a|=1<<pe[v]}assert(p===0,"join residual");return a}
    const cycles=[0];edges.forEach(([u,v],e)=>{if(!(tree&(1<<e))){const c=join((1<<u)^(1<<v))^(1<<e);const z=cycles.length;for(let i=0;i<z;i++)cycles.push(cycles[i]^c)}});
    const cache=new Map();
    function numerator(Y){const l=pop(Y);assert(l%2===0,"hub parity");const k=l/2;return sign(Y&signs)*(k%2?-1n:1n)*power(3n,m-k)}
    function moment(p){if(cache.has(p))return cache.get(p);const J=join(p);if(J===null){stats.noJoinMoments++;cache.set(p,0n);return 0n}stats.twistedMoments++;
      let tw=0n, direct=0n;for(const Y of cycles){tw+=numerator(Y)*power(-3n,pop(Y&J));direct+=numerator(Y^J);stats.cycleTerms++}
      const j=pop(J)/2, pref=sign(J&signs)*(j%2?-1n:1n);
      assert(tw*pref===direct*power(3n,j),"T-join twist");
      const num=tw*pref*power(2n,n),den=power(3n,j)*power(2n,2*m);
      assert(num%den===0n,"moment integrality");const val=num/den;cache.set(p,val);return val;
    }
    function table(B){const q=1<<B.length,M=[];for(let p=0;p<q;p++){let v=0;B.forEach((b,j)=>{if(p&(1<<j))v|=1<<b});M.push(moment(v))}
      const A=[];for(let a=0;a<q;a++){let s=0n;for(let p=0;p<q;p++)s+=sign(a&p)*M[p];assert(s%BigInt(q)===0n&&s>=0n,"nonnegative pin table");A.push(s/BigInt(q))}
      return {A,M};
    }
    return {table};
  }
  function pinned(n,F,P){const B=[...P.keys()].sort((a,b)=>a-b);let k=0;B.forEach((v,i)=>k|=P.get(v)<<i);return backend(n,F).table(B).A[k]}
  function merge(n,F,P,u,v,d){assert(u<v,"ordered contraction");const map=x=>x===v?u:(x>v?x-1:x);const G=F.map(c=>c.map(([x,s])=>[map(x),s^(x===v?d:0)]));const Q=new Map();for(const [x,t] of P){const y=map(x),b=t^(x===v?d:0);if(Q.has(y)&&Q.get(y)!==b)return null;Q.set(y,b)}return {n:n-1,F:G,P:Q}}
  function witness(n,F,P){if(pinned(n,F,P)===0n)return null;
    // Exact unary support probes; record all forced values without increasing the stored guard.
    const forced=new Map();for(let x=0;x<n;x++)if(!P.has(x)){const Q=new Map(P);Q.set(x,0);const a=pinned(n,F,Q);Q.set(x,1);const b=pinned(n,F,Q);stats.unaryProbes+=2;assert(a+b>0n,"nonempty unary support");if(a===0n||b===0n){forced.set(x,a===0n?1:0);stats.forcedUnary++}}
    const pairs=new Map();for(const c of F)for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let [u,v]=[c[i][0],c[j][0]].sort((a,b)=>a-b);if(u!==v)pairs.set(u+","+v,[u,v])}
    let a0=null,choice=null;
    for(const [u,v] of pairs.values()){
      const a=merge(n,F,P,u,v,0),b=merge(n,F,P,u,v,1);const ca=a?pinned(a.n,a.F,a.P):0n,cb=b?pinned(b.n,b.F,b.P):0n;stats.relativeProbes+=2;assert(ca+cb>0n,"relative support");
      if(ca===0n||cb===0n){choice={u,v,d:ca===0n?1:0,next:ca===0n?b:a};stats.forcedRelative++;break}
      if(!a0)a0={u,v,d:0,next:a};
    }
    if(!choice&&a0){choice=a0;stats.searchChoices++}
    let out;
    if(!choice){out=Array.from({length:n},(_,i)=>P.get(i)??forced.get(i)??0)}
    else{const {u,v,d,next}=choice;const w=witness(next.n,next.F,next.P);assert(w!==null,"positive contraction");out=[...w.slice(0,v),w[u]^d,...w.slice(v)]}
    const x=out.reduce((a,b,i)=>a|(b<<i),0);assert(valid(F,x),"source lift");for(const [v,b] of P)assert(out[v]===b,"pin lift");for(const [v,b] of forced)assert(out[v]===b,"forced unary lift");return out
  }
  function compare(n,F,B,label){const {A}=backend(n,F).table(B),R=brute(n,F,B);assert(A.every((v,i)=>v===R[i]),"table "+label);stats.tableEntries+=A.length;stats.systems++;const total=A.reduce((x,y)=>x+y,0n);if(total===0n)stats.unsat++;else{stats.sat++;const a=A.findIndex(v=>v>0n);const P=new Map(B.map((v,i)=>[v,(a>>i)&1]));const W=witness(n,F,P);assert(W!==null,"witness "+label);stats.verifiedWitnesses++}return total}
  function local(F,B){const V=[...new Set(F.flatMap(c=>c.map(([v])=>v)))].sort((a,b)=>a-b);const map=new Map(V.map((v,i)=>[v,i]));const G=F.map(c=>c.map(([v,s])=>[map.get(v),s]));const b=B.map(v=>map.get(v));return {V,G,b,...backend(V.length,G).table(b)}}
  function glue(n,F,k,label){const F1=F.slice(0,k),F2=F.slice(k);const v1=new Set(F1.flatMap(c=>c.map(([v])=>v))),v2=new Set(F2.flatMap(c=>c.map(([v])=>v)));const B=[...v1].filter(v=>v2.has(v)).sort((a,b)=>a-b);
    const L=local(F1,B),R=local(F2,B);const nonisolated=new Set([...v1,...v2]).size;const factor=power(2n,n-nonisolated);let total=0n,dual=0n,nonzero=0;for(let a=0;a<L.A.length;a++){total+=L.A[a]*R.A[a];const d=L.M[a]*R.M[a];dual+=d;if(d!==0n)nonzero++}
    assert(dual===total*BigInt(L.A.length),"dual glue");const reference=brute(n,F,[])[0];assert(total*factor===reference,"semantic glue "+label);stats.glueChecks++;
    if(total>0n){const a=L.A.findIndex((x,i)=>x>0n&&R.A[i]>0n);const W=Array(n).fill(0);for(const Q of [L,R]){const P=new Map(Q.b.map((v,i)=>[v,(a>>i)&1]));const w=witness(Q.V.length,Q.G,P);assert(w!==null,"region witness");Q.V.forEach((v,i)=>{W[v]=w[i]})}assert(valid(F,W.reduce((a,b,i)=>a|(b<<i),0)),"global glued lift");stats.glueWitnesses++}
    return {label,boundary:B.length,solutions:String(reference),nonzeroSignedProducts:nonzero,regionTables:[L.A.map(String),R.A.map(String)]};
  }
  const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map(c=>c.map(v=>[v,0]));
  const fc=compare(7,fano,[0,1,2,3],"Fano");assert(fc===0n,"Fano UNSAT");stats.controls.push(glue(7,fano,3,"Fano split"));
  for(let i=0;i<7;i++){const F=fano.filter((_,j)=>j!==i);assert(compare(7,F,[0,1,2],"Fano deletion")===10n,"Fano neighbor");stats.controls.push(glue(7,F,3,"Fano deletion "+i))}
  const hostile=[0,1,2,4].map(s=>[0,1,2].map(v=>[v,(s>>v)&1]));assert(compare(3,hostile,[0,1,2],"opposite support")===0n,"hostile unsat");stats.hostile=glue(3,hostile,2,"four signed NAE, disjoint feasible boundary");
  for(let t=0;t<50;t++){const n=3+rand(5),m=2+rand(4);const F=Array.from({length:m},()=>Array.from({length:3},()=>[rand(n),rand(2)]));const B=Array.from({length:Math.min(n,3)},(_,i)=>i);compare(n,F,B,"random "+t);glue(n,F,1+rand(m-1),"random split "+t)}
  return stats
}
console.log(JSON.stringify(runDS01(),null,2));
