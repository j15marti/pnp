function main() {
  "use strict";
  const ctr={assertions:0,gauges:0,histograms:0,localWords:0,convolutions:0,rootPins:0,privatePins:0,creditQueries:0,referenceWords:0,externalFibers:0,momentChecks:0,lifts:0};
  const ck=(p,s)=>{ctr.assertions++;if(!p)throw Error(s)};
  const bit=i=>1n<<BigInt(i), size=n=>bit(n), has=(a,i)=>!!(a&bit(i));
  const par=a=>{let p=0;while(a){a&=a-1n;p^=1}return p};
  const sign=a=>par(a)?-1n:1n, mask=n=>size(n)-1n;
  const add=(p,w,v)=>{if(v){let a=(p.get(w)||0n)+v;if(a)p.set(w,a);else p.delete(w)}};
  const plus=(p,q,s=1n)=>{for(let [w,v] of q)add(p,w,s*v);return p};
  const mul=(p,q)=>{let a=new Map();for(let [w,v] of p)for(let [u,b] of q)add(a,w^u,v*b);return a};
  const evalP=(p,z)=>{let a=0n;for(let [w,v] of p)a+=v*sign(w&z);return a};
  const bad=(e,x,z)=>e.rows.reduce((a,[r,s,b])=>a+(par(r&x)^par(s&z)^b),0)>e.H;
  const col=(rows,j,k)=>rows.reduce((a,r,i)=>has(r[k],j)?a|bit(i):a,0n);
  function gauge(e,n,q){
    ctr.gauges++;let B=new Map(),V=[],Q=[],T=[];
    function reduce(v){let a=0n;while(v){let p=v.toString(2).length-1,b=B.get(p);if(!b)break;v^=b[0];a^=b[1]}return [v,a]}
    for(let j=0;j<n;j++){let [v,a]=reduce(col(e.rows,j,0));if(v)B.set(v.toString(2).length-1,[v,a^bit(j)])}
    for(let j=0;j<q;j++){
      let [v,a]=reduce(col(e.rows,j,1));
      if(v){let k=V.length;V.push(v);Q.push(0n);B.set(v.toString(2).length-1,[v,bit(n+k)]);a^=bit(n+k)}
      T.push(a&mask(n));for(let k=0;k<V.length;k++)if(has(a,n+k))Q[k]|=bit(j);
      let rec=0n;for(let k=0;k<n;k++)if(has(a,k))rec^=col(e.rows,k,0);for(let k=0;k<V.length;k++)if(has(a,n+k))rec^=V[k];ck(rec===col(e.rows,j,1),"gauge decomposition");
    }
    return {e,n,q,T,V,Q,t:V.length};
  }
  // Exact single-event signed weight histogram. Inactive coordinates remain
  // dummy uniform bits, so the returned numerator always has denominator 2^n.
  function hist(rows,H,n,w){
    ctr.histograms++;
    let p=Array.from({length:n},(_,i)=>i),root=i=>{while(p[i]!==i)i=p[i];return i};
    for(let [r,b] of rows){let first=-1;for(let i=0;i<n;i++)if(has(r,i)){if(first<0)first=i;else p[root(i)]=root(first)}}
    let groups=new Map();for(let i=0;i<n;i++){let k=root(i);if(!groups.has(k))groups.set(k,{ids:[],rows:[]});groups.get(k).ids.push(i)}
    let offset=0;for(let [r,b] of rows){if(!r){offset+=b;continue}let i=0;while(!has(r,i))i++;groups.get(root(i)).rows.push([r,b])}
    let A=new Map([[offset,1n]]);
    for(let {ids,rows:rr} of groups.values()){
      let L=new Map();for(let j=0;j<2**ids.length;j++){
        ctr.localWords++;let x=0n;ids.forEach((k,i)=>{if(j&2**i)x|=bit(k)});
        let wt=rr.reduce((a,[r,b])=>a+(par(r&x)^b),0);add(L,wt,sign(w&x));
      }
      let C=new Map();for(let [a,u] of A)for(let [b,v] of L){ctr.convolutions++;add(C,a+b,u*v)}A=C;
    }
    let out=0n;for(let [a,v] of A)if(a>H)out+=v;return out;
  }
  function spec(g,w,D){
    let {e,n,q,T,V,Q,t}=g, vals=[];
    for(let u=0;u<2**t;u++){
      let bvec=0n;for(let k=0;k<t;k++)if(u&2**k)bvec^=V[k];
      vals.push(hist(e.rows.map(([r,s,b],i)=>[r,b^Number(has(bvec,i))]),e.H,n,w));
    }
    let phase=0n;for(let j=0;j<q;j++)if(par(T[j]&w))phase|=bit(j);
    let P=new Map(),scale=D/size(n+t);
    for(let a=0;a<2**t;a++){
      let v=0n,key=phase;for(let u=0;u<2**t;u++)v+=vals[u]*sign(BigInt(a&u));
      for(let k=0;k<t;k++)if(a&2**k)key^=Q[k];add(P,key,v*scale);
    }
    return P;
  }
  function substitute(events,side,j,v){
    return events.map(e=>({H:e.H,rows:e.rows.map(row=>{let a=row.slice();if(has(a[side],j)){a[side]^=bit(j);a[2]^=v}return a})}));
  }
  // Restricted certified root closure: exact individual covers and one-bit
  // cover probes. No semantic complete-hull oracle.
  function closeRoot(events,n,q){
    let pins=[0n,0n],values=[0n,0n];
    for(;;){
      let gs=events.map(e=>gauge(e,n,q)),D=size(n+Math.max(0,...gs.map(g=>g.t))),forced=null;
      for(let g of gs){
        let M=spec(g,0n,D),a=M.get(0n)||0n;
        if(a===D)return {unsat:true,events,pins,values};
        if(2n*a<D)continue;
        for(let side=0;side<2&&!forced;side++)for(let j=0;j<(side?q:n);j++){
          if(has(pins[side],j))continue;
          let b=side?(M.get(bit(j))||0n):(spec(g,bit(j),D).get(0n)||0n);
          for(let v=0;v<2;v++)if(a+(v?-b:b)===D){forced=[side,j,1-v];break}
          if(forced)break;
        }
        if(forced)break;
      }
      if(!forced)return {unsat:false,events,pins,values};
      let [s,j,v]=forced;pins[s]|=bit(j);if(v)values[s]|=bit(j);events=substitute(events,s,j,v);ctr.rootPins++;
    }
  }
  function cert(events,n,q,H){
    let gs=events.map(e=>gauge(e,n,q)),t=Math.max(0,...gs.map(g=>g.t)),D=size(n+t);
    let A=gs.map(g=>new Map(H.map(w=>[w,spec(g,w,D)])));
    let P=new Map([[0n,2n*D*D]]);
    for(let a of A)plus(P,a.get(0n),-2n*D);
    let pairs=[];
    for(let i=0;i<A.length;i++)for(let j=0;j<i;j++){
      let B=new Map();plus(B,A[i].get(0n),-D);plus(B,A[j].get(0n),-D);
      for(let w of H){let h=plus(new Map(A[i].get(w)),A[j].get(w));plus(B,mul(h,h))}
      pairs.push({i,j,B,weight:B.get(0n)||0n});
    }
    pairs.sort((a,b)=>a.weight>b.weight?-1:a.weight<b.weight?1:0);
    let parent=A.map((_,i)=>i),root=i=>{while(parent[i]!==i)i=parent[i];return i},edges=[];
    for(let a of pairs)if(a.weight>0n&&root(a.i)!==root(a.j)){parent[root(a.i)]=root(a.j);edges.push(a);plus(P,a.B)}
    let lb=P.get(0n)||0n;for(let [w,v] of P)if(w)lb-=v<0n?-v:v;
    return {A,P,lb,D,t,edges,H,gs,events,n,q};
  }
  function lift(C,z,root){
    let {events,n,H,D,A,edges}=C, pin=root.pins[0],val=root.values[0],zrows=events.map(e=>({H:e.H,rows:e.rows.map(([r,s,b])=>[r,b^par(s&z)])}));
    let hh=edges.map(({i,j})=>({i,j,h:H.map(w=>[w,evalP(A[i].get(w),z)+evalP(A[j].get(w),z)]).filter(a=>a[1])}));
    const M=size(n);
    function moments(p,v){
      let cache=new Map();
      function at(i,w){
        let key=i+":"+w;if(cache.has(key))return cache.get(key);
        let e=zrows[i],a=sign(w&p&v)*hist(e.rows.map(([r,b])=>[r&~p,b^par(r&p&v)]),e.H,n,w&~p);cache.set(key,a);return a;
      }
      return at;
    }
    function credit(p,v){
      ctr.creditQueries++;let at=moments(p,v),out=2n*D*D*M;
      for(let i=0;i<events.length;i++)out-=2n*D*D*at(i,0n);
      for(let {i,j,h} of hh){
        out-=D*D*(at(i,0n)+at(j,0n));let F=new Map();
        for(let [w,a] of h){out+=2n*D*a*(at(i,w)+at(j,w));add(F,w&~p,a*sign(w&p&v))}
        for(let a of F.values())out-=a*a*M;
      }
      return out; // conditional mean in units 1/(2 D^2 M)
    }
    function close(){
      for(;;){
        let at=moments(pin,val),force=null,all=true;
        for(let i=0;i<events.length;i++){
          let a=at(i,0n);if(a===M)throw Error("positive credit hit cover");if(a)all=false;
          if(2n*a<M)continue;
          for(let j=0;j<n;j++)if(!has(pin,j)){
            let b=at(i,bit(j));for(let v=0;v<2;v++)if(a+(v?-b:b)===M){force=[j,1-v];break}if(force)break;
          }
          if(force)break;
        }
        if(!force)return all;
        let [j,v]=force;pin|=bit(j);if(v)val|=bit(j);ctr.privatePins++;
      }
    }
    ck(credit(pin,val)>0n,"positive initial guarded credit");
    for(;;){
      if(close())break;
      let j=0;while(j<n&&has(pin,j))j++;if(j===n)break;
      let p=pin|bit(j),a=credit(p,val),b=credit(p,val|bit(j));
      ck(a+b===2n*credit(pin,val),"conditional credit additivity");ck(a>0n||b>0n,"positive child");
      pin=p;if(a<=0n)val|=bit(j);
    }
    ck(events.every(e=>!bad(e,val,z)),"lift reduced");ctr.lifts++;return val;
  }
  let rng=20261124;const rnd=k=>{rng=(Math.imul(rng,1664525)+1013904223)>>>0;return rng%k};
  const features=n=>{let H=[0n];for(let i=0;i<n;i++){H.push(bit(i));for(let j=0;j<i;j++)H.push(bit(i)^bit(j))}return H};
  const results={seed:20261124,random:{systems:0,satFibers:0,unsatFibers:0,certifiedFibers:0,uniformSystems:0,rootUnsat:0,nonzeroQuotientEvents:0},scales:[],controls:[]};
  for(let k=0;k<84;k++){
    let n=3+rnd(3),q=2+rnd(3),es=[];
    for(let i=0,m=2+rnd(5);i<m;i++){
      let r=2+rnd(5),rows=[];for(let j=0;j<r;j++)rows.push([BigInt(rnd(2**n)),BigInt(rnd(2**q)),rnd(2)]);
      es.push({rows,H:rnd(r+1)});
    }
    let H=features(n),gs=es.map(e=>gauge(e,n,q)),D=size(n+Math.max(...gs.map(g=>g.t)));
    for(let g of gs){if(g.t)results.random.nonzeroQuotientEvents++;for(let w of H){let P=spec(g,w,D);for(let z=0;z<2**q;z++){let a=0n;for(let x=0;x<2**n;x++)if(bad(g.e,BigInt(x),BigInt(z)))a+=sign(w&BigInt(x));ck(evalP(P,BigInt(z))===a*(D/size(n)),"moment exact");ctr.momentChecks++}}}
    let R=closeRoot(es,n,q);results.random.systems++;if(R.unsat)results.random.rootUnsat++;
    let C=R.unsat?null:cert(R.events,n,q,H);if(C&&C.lb>0n)results.random.uniformSystems++;
    for(let z=0;z<2**q;z++){
      let legal=0;for(let x=0;x<2**n;x++){ctr.referenceWords++;if(es.every(e=>!bad(e,BigInt(x),BigInt(z))))legal++}
      ctr.externalFibers++;results.random[legal?"satFibers":"unsatFibers"]++;
      if(R.unsat||((BigInt(z)^R.values[1])&R.pins[1])){ck(!legal,"sound root closure");continue}
      let actual=evalP(C.P,BigInt(z));ck(actual>=C.lb,"uniform lower bound");
      let reducedLegal=0;for(let x=0;x<2**n;x++)if(R.events.every(e=>!bad(e,BigInt(x),BigInt(z))))reducedLegal++;
      ck(actual*size(n)<=2n*C.D*C.D*BigInt(reducedLegal),"pointwise credit bound");
      if(C.lb>0n){ck(legal>0,"no false uniform result");let x=lift(C,BigInt(z),R);ck(es.every(e=>!bad(e,x,BigInt(z))),"original witness");results.random.certifiedFibers++}
    }
  }
  // Dense translated gated majorities: each event has d independent
  // exterior phases, all private-row components singleton.
  for(let d of [3,7,15,31]){
    let n=1+5*d,q=15*d,es=[],H=[0n,1n];
    for(let i=0;i<5;i++){
      let rows=[];for(let k=0;k<d;k++)rows.push([1n,0n,1]);
      for(let j=0;j<d;j++){
        let p=1+i*d+j,w=bit(p),a=3*(p-1),s=bit(a)|bit(a+1)|bit(a+2);
        rows.push([w,s,0]);H.push(w,1n^w);
      }
      es.push({rows,H:d+(d-1)/2});
    }
    let R=closeRoot(es,n,q);ck(!R.unsat&&R.pins[0]===0n&&R.pins[1]===0n,"scale root closure");
    let C=cert(R.events,n,q,H);ck(C.t===0&&C.lb>0n&&C.P.size===1,"scale constant positive certificate");
    let D=C.D,old=2n*D*D-5n*D*D/2n; // only common constant and gate bit; pair lower 0.
    ck(old<0n,"old degree-two credit nonpositive");
    let z=mask(q);let x=lift(C,z,R);ck(es.every(e=>!bad(e,x,z)),"scale witness");
    results.scales.push({d,n,q,rawExternalRankPerEvent:d,t:C.t,features:H.length,nonzeroCreditMasks:C.P.size,edges:C.edges.length,creditNumerator:String(C.lb),creditDenominator:String(2n*D*D),creditApprox:Number(C.lb)/Number(2n*D*D),oldDegreeTwoCredit:-0.25});
  }
  // Full shifted two-bit cube, deletion neighbor and a mixed-fiber system.
  for(let mode of ["cover","deletion","mixed"]){
    let n=2,q=6,H=features(n),s0=7n,s1=56n;
    let es=Array.from({length:mode==="deletion"?3:4},(_,i)=>({H:1,rows:[[1n,s0,1^(i&1)],[2n,s1,1^((i>>1)&1)]]}));
    if(mode==="mixed")es[3].rows[0][1]=0n;
    let R=closeRoot(es,n,q);ck(!R.unsat,"cube individual closure should stagnate");let C=cert(R.events,n,q,H),sat=0,unsat=0;
    for(let z=0;z<2**q;z++){
      let legal=0;for(let x=0;x<4;x++)if(es.every(e=>!bad(e,BigInt(x),BigInt(z))))legal++;
      if(legal)sat++;else unsat++;
      if(C.lb>0n){ck(legal>0,"cube uniform");let x=lift(C,BigInt(z),R);ck(es.every(e=>!bad(e,x,BigInt(z))),"cube source witness")}
    }
    ck(mode==="cover"?unsat===64&&C.lb<=0n:mode==="deletion"?sat===64&&C.lb>0n:sat>0&&unsat>0&&C.lb<=0n,"cube controls");
    results.controls.push({mode,sat,unsat,t:C.t,uniform:C.lb>0n,creditApprox:Number(C.lb)/Number(2n*C.D*C.D)});
  }
  results.counters=ctr;return results;
}
console.log(JSON.stringify(main(),null,2));
