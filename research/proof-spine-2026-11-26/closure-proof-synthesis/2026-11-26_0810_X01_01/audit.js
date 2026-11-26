"use strict";
function audit(){
  const check=(p,msg)=>{if(!p)throw Error(msg);checks++};let checks=0,seed=261126;
  const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n};
  const pop=x=>{let s=0;while(x){x&=x-1;s++}return s};
  const perms=n=>{let a=[];function rec(p){if(p.length===n)a.push(p);else for(let i=0;i<n;i++)if(!p.includes(i))rec([...p,i])}rec([]);return a};
  let arithmetic=[];
  for(let n=2;n<=4;n++){
    const ps=perms(n), masks=ps.map(p=>p.reduce((a,j,i)=>a|(1<<(i*n+j)),0)), cycles=ps.filter(p=>{let v=0,t=0;do{v=p[v];t++}while(v!==0);return t===n}).map(p=>p.reduce((a,j,i)=>a|(1<<(i*n+j)),0));
    const counts={n,graphs:0,coefficients:0,perfect:0,hamiltonian:0};
    for(let s=0;s<(1<<(n*n));s++){
      const w=pop(s);if(w>n)continue;counts.graphs++;
      const f=t=>masks.some(p=>(p&t)===p)?1:0, h=t=>cycles.some(p=>(p&t)===p)?1:0, e=t=>cycles.includes(t)?1:0;
      const coeff=fn=>{let z=0,t=s;while(true){z+=((w-pop(t))&1?-1:1)*fn(t);if(!t)break;t=(t-1)&s}return z};
      const c1=coeff(f),c2=coeff(h),c3=coeff(e);
      check(c1===+masks.includes(s),"per coefficient");check(c2===+cycles.includes(s),"hc coefficient");check(c3===c2,"exact-HC coefficient");counts.coefficients+=3;
      counts.perfect+=c1;counts.hamiltonian+=c2;
    }
    check(counts.perfect===ps.length,"perm total");check(counts.hamiltonian===cycles.length,"hc total");arithmetic.push(counts);
  }
  let interpolation=0;const mod=x=>((x%5)+5)%5;const pow=(x,e)=>{let z=1;while(e--)z=mod(z*x);return z};
  for(let q=0;q<200;q++){
    let d=5,b=1+rnd(3),terms=[];
    for(let j=0;j<16;j++)terms.push([rnd(5),Array.from({length:d},(_,i)=>rnd(i<b?5:2))]);
    const raw=(x,reduce=false)=>mod(terms.reduce((acc,[c,e])=>acc+c*e.reduce((v,a,i)=>mod(v*pow(x[i],reduce&&a>0?1:a)),1),0));
    for(let t=0;t<16;t++){
      const x=Array.from({length:d},()=>rnd(5));let z=0;
      for(let y=0;y<(1<<b);y++){const u=x.slice();let c=1;for(let i=0;i<b;i++){u[i]=(y>>i)&1;c=mod(c*(u[i]?x[i]:1-x[i]))}z=mod(z+c*raw(u))}
      check(z===raw(x,true),"interpolation");interpolation++;
    }
  }
  // Exact explicit four-port grid. N,E,S,W bits, all boundary pins absorbed in local tables.
  const bit=(w,i)=>(w>>i)&1;
  const table=pred=>Array.from({length:16},(_,w)=>w).filter(w=>pred(...[0,1,2,3].map(i=>bit(w,i))));
  function compile(n,clauses){
    const m=clauses.length,k=Math.max(3,n+2,m+2),r=n,c=m, G=[];
    for(let i=0;i<k;i++)for(let j=0;j<k;j++){
      let t;
      if(i<n&&j<m)t=table((N,E,S,W)=>E===W&&S===(N||+clauses[j].some(l=>Math.abs(l)===i+1&&((l>0)===!!W)))&&(i!==0||N===0));
      else if(i<n&&j===m)t=table((N,E,S,W)=>N===0&&E===0&&S===0);
      else if(i===r&&j<m)t=table((N,E,S,W)=>E===W&&S===(N||W));
      else if(i>r&&j<m)t=table((N,E,S,W)=>E===0&&W===0&&S===N&&(i!==k-1||S===1));
      else if(i===r&&j===c)t=table((N,E,S,W)=>N===0&&W===E&&(W===1||S===0));
      else if(i===r&&j===c+1)t=table((N,E,S,W)=>N===0&&E===0&&S===W);
      else if(i===r+1&&j===c+1)t=table((N,E,S,W)=>S===0&&E===0&&W===N);
      else if(i===r+1&&j===c)t=table((N,E,S,W)=>W===0&&S===0&&(E===1||N===1));
      else t=[0];
      G.push(t);
    }
    return {k,r,c,G,A:r*k+c,B:(r+1)*k+c};
  }
  function relaxed(o){let G=o.G.map(a=>a.slice());for(const [v,p] of [[o.A,2],[o.B,0]])G[v]=Array.from(new Set(G[v].flatMap(w=>[w,w^(1<<p)]))).sort((a,b)=>a-b);return {...o,G}}
  function dp(o,guard){
    const {k,r,G}=o;let states=new Set([0]);
    for(let v=0;v<G.length;v++){
      const i=Math.floor(v/k),j=v%k,newset=new Set();
      for(const st of states)for(const w of G[v]){
        if(bit(w,0)!==((st>>j)&1))continue;
        if(j&&bit(w,3)!==((st>>k)&1))continue;
        if(j===0&&i===r&&guard!==null&&bit(w,3)!==guard)continue;
        if(j===k-1&&bit(w,1)!==0)continue;
        let ns=(st&~(1<<j)&~(1<<k))|(bit(w,2)<<j)|(bit(w,1)<<k);
        newset.add(ns);
      }
      states=newset;if(!states.size)return false;
    }
    return !!states.size;
  }
  function sat(n,cls){for(let a=0;a<(1<<n);a++)if(cls.every(c=>c.some(l=>!!((a>>(Math.abs(l)-1))&1)===(l>0))))return true;return false}
  function verify(o,words){
    const {k,G}=o;if(words.length!==G.length)return false;
    for(let v=0;v<G.length;v++){let i=Math.floor(v/k),j=v%k,w=words[v];if(!G[v].includes(w))return false;if(i&&bit(words[v-k],2)!==bit(w,0))return false;if(j&&bit(words[v-1],1)!==bit(w,3))return false}return true;
  }
  function explicit(o,n,cls,a,e,x){
    const {k,r,c}=o,w=Array(k*k).fill(0),mk=(N,E,S,W)=>N+2*E+4*S+8*W;
    for(let j=0;j<cls.length;j++){
      let acc=0;for(let i=0;i<n;i++){let y=(a>>i)&1,next=acc||+cls[j].some(l=>Math.abs(l)===i+1&&((l>0)===!!y));w[i*k+j]=mk(acc,y,next,y);acc=next}
      w[r*k+j]=mk(acc,e,acc||e,e);acc=acc||e;
      for(let i=r+1;i<k;i++)w[i*k+j]=mk(acc,0,acc,0);
    }
    for(let i=0;i<n;i++)w[i*k+c]=mk(0,0,0,(a>>i)&1);
    w[o.A]=mk(0,e,x,e);w[o.A+1]=mk(0,0,e,e);w[o.B+1]=mk(e,0,0,e);w[o.B]=mk(x,e,0,0);
    return w;
  }
  let reductions={cases:0,sat:0,unsat:0,explicitLifts:0,dpCalls:0,largest:0};
  for(let q=0;q<240;q++){
    let n=1+rnd(4),m=1+rnd(5),cls=Array.from({length:m},()=>Array.from({length:rnd(4)},()=> (rnd(2)?1:-1)*(1+rnd(n))));
    if(q%3===0)cls=[...cls,[1],[-1]];
    if(q%3===1)cls=cls.map(c=>c.length?c:[1]).map(c=>c.map(Math.abs));
    const yes=sat(n,cls),o=compile(n,cls),p=relaxed(o);reductions.cases++;reductions[yes?"sat":"unsat"]++;reductions.largest=Math.max(reductions.largest,o.k);
    check(dp(o,1),"F known SAT");check(!dp(o,0),"F e0");check(dp(p,1),"G known SAT");check(dp(p,0)===yes,"G e0 iff SAT");reductions.dpCalls+=4;
    for(let a=0;a<(1<<n);a++)for(let e=0;e<=1;e++)for(let x=0;x<=1;x++){
      const w=explicit(o,n,cls,a,e,x),valid=e===1||cls.every(c=>c.some(l=>!!((a>>(Math.abs(l)-1))&1)===(l>0)));
      check(verify(p,w)===valid,"G lift");check(verify(o,w)===(e===1),"F lift");reductions.explicitLifts++;
    }
  }
  // Actual unsmooth block-NNF on singleton 2x2 tables; enumerate true unfolded traces.
  const gates=[];const leaf=(v,p,b)=>{gates.push({v,p,b,sc:1<<v});return gates.length-1};
  const bin=(op,a,b)=>{gates.push({op,a,b,sc:gates[a].sc|gates[b].sc});return gates.length-1};
  const and=(a,b)=>bin("and",a,b),or=(a,b)=>bin("or",a,b);
  const eq=(v,p,w,q)=>or(and(leaf(v,p,0),leaf(w,q,0)),and(leaf(v,p,1),leaf(w,q,1)));
  const es=[[0,1,1,3],[0,2,2,0],[1,2,3,0],[2,1,3,3]];
  let base=es.map(e=>eq(...e)).reduce(and);
  const taut=v=>or(leaf(v,0,0),leaf(v,0,1));
  const g=or(and(taut(0),taut(1)),and(taut(0),taut(2)));
  const root=and(g,base),groups=new Map();
  const tr=(id,w)=>{let a=gates[id];if(!a.op)return (bit(w[a.v],a.p)===a.b)?[{id,sc:a.sc,ch:[]}]:[];let l=tr(a.a,w),r=tr(a.b,w);if(a.op==="or")return [...l,...r].map(c=>({id,sc:c.sc,ch:[c]}));return l.flatMap(x=>r.map(y=>({id,sc:x.sc|y.sc,ch:[x,y]})))};
  const source=w=>es.every(([v,p,j,q])=>bit(w[v],p)===bit(w[j],q));
  const domains=Array.from({length:4},(_,v)=>Array.from({length:16},(_,x)=>x).filter(w=>{let i=v>>1,j=v&1;return (i||!bit(w,0))&&(j||!bit(w,3))&&(i===0||!bit(w,2))&&(j===0||!bit(w,1))}));
  let traceStats={inputs:0,yes:0,traces:0,balanced:0,groups:0,multiScopeGroups:0,rectangleChecks:0};
  const zkey=(w,J)=>w.map((x,i)=>J>>i&1?x:"-").join(",");
  function visit(t,context,w){
    if(pop(t.sc)===2){let J=gates[t.id].sc&context;check((gates[t.id].sc&~t.sc&~J)===0,"missing scope not in J");let key=[t.id,J,zkey(w,J)].join("|");if(!groups.has(key))groups.set(key,{S:t.sc,scopes:new Set(),words:new Map()});let a=groups.get(key);a.scopes.add(t.sc);a.words.set(w.join(","),w);traceStats.balanced++}
    t.ch.forEach((c,i)=>visit(c,context|t.ch.filter((_,j)=>i!==j).reduce((s,x)=>s|x.sc,0),w));
  }
  for(const a of domains[0])for(const b of domains[1])for(const c of domains[2])for(const d of domains[3]){
    let w=[a,b,c,d],ts=tr(root,w);traceStats.inputs++;check(!!ts.length===source(w),"NNF source");
    if(ts.length)traceStats.yes++;
    for(const t of ts){check(t.sc===15,"read saturation");traceStats.traces++;visit(t,0,w)}
  }
  traceStats.groups=groups.size;
  for(const a of groups.values()){
    if(a.scopes.size>1)traceStats.multiScopeGroups++;
    for(const x of a.words.values())for(const y of a.words.values()){
      let z=x.map((v,i)=>a.S>>i&1?v:y[i]);check(source(z),"group splice");traceStats.rectangleChecks++;
    }
  }
  check(traceStats.multiScopeGroups>0,"no unsmooth groups");
  return {checks,arithmetic,interpolation,reductions,traceStats,seedFinal:seed};
}
console.log(JSON.stringify(audit(), null, 2));
