// Independent finite checks, not asymptotic proof. Node.js.
const audit = ()=> {
  let seed=2611261202, checks=0, systems=0, fibers=0, syndromeClasses=0, screened=0;
  const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n;};
  const dot=(a,b)=>{let x=a&b,r=0;while(x){r^=1;x&=x-1;}return r;};
  const range=n=>Array.from({length:n},(_,i)=>i);
  const eq=(rows,x)=>rows.every(([a,b])=>dot(a,x)===b);
  const rank=rows=>{const piv={};for(let a of rows){while(a){let j=31-Math.clz32(a);if(piv[j]===undefined){piv[j]=a;break;}a^=piv[j];}}return Object.keys(piv).length;};
  const assert=b=>{checks++;if(!b)throw Error("check "+checks);};
  const count=(E,k)=>range(1<<k).filter(x=>E.some(e=>eq(e,x))).length;
  const ie=(E,k)=>{let a=0;for(let m=1;m<(1<<E.length);m++){let R=E.flatMap((e,i)=>m>>i&1?e:[]),n=range(1<<k).filter(x=>eq(R,x)).length,odd=dot(m,m);a+=odd?n:-n;}return a;};
  for(let h=0;h<160;h++){
    let k=1+rnd(5), l=1+rnd(3), q=1+rnd(5), M=(1<<k)-1;
    let E=range(q).map(()=>range(1+rnd(5)).map(()=>[1+rnd((1<<(k+l))-1),rnd(2)]));
    // Discard events not depending on private coordinates. They remain exterior constraints.
    E=E.filter(e=>e.some(([a])=>a&M));q=E.length;if(!q)continue;
    let ranks=E.map(e=>rank(e.map(([a])=>a&M)));
    for(let y=0;y<(1<<l);y++){
      let F=E.map(e=>e.map(([a,b])=>[a&M,b^dot(a>>k,y)]));
      let S=F.filter((e,i)=>ranks[i]<=q-1),c=count(F,k);
      assert((c===(1<<k))===(count(S,k)===(1<<k)));
      assert(c===ie(F,k));fibers++;screened+=F.length-S.length;
      if(c===(1<<k)){
        let G=F.map((e,i)=>i);
        for(let i=0;i<q;i++)if(G.includes(i)&&count(G.filter(j=>j!==i).map(j=>F[j]),k)===(1<<k))G=G.filter(j=>j!==i);
        for(let i of G)assert(ranks[i]<=G.length-1);
      }
    }
    // Independent syndrome test: enumerate every RHS and group by explicit
    // translation orbits, NOT a Gaussian nullspace implementation.
    const A=E.map(e=>e.map(([a])=>a&M));
    let m=A.reduce((a,b)=>a+b.length,0);if(m>9)continue;
    let flat=A.flat(),translation=range(1<<k).map(x=>flat.reduce((v,a,i)=>v|(dot(a,x)<<i),0)),D=new Map;
    for(let b=0;b<(1<<m);b++){
      let key=Math.min(...translation.map(t=>t^b)),idx=0;
      let F=A.map(e=>e.map(a=>[a,(b>>idx++)&1]));
      let c=count(F,k);if(D.has(key))assert(D.get(key)===c);else D.set(key,c);
    }
    assert(D.size===(1<<(m-rank(flat))));syndromeClasses+=D.size;systems++;
  }
  // Tight minimal covers: x1=0, x1=1,x2=0, ..., all x=1.
  for(let q=2;q<=8;q++){
    let k=q-1,E=range(q).map(i=>range(Math.min(i+1,k)).map(j=>[1<<j,j===i?0:1]));
    assert(count(E,k)===(1<<k));
    for(let i=0;i<q;i++)assert(count(E.filter((e,j)=>i!==j),k)<(1<<k));
    assert(rank(E[q-1].map(([a])=>a))===q-1);
  }
  // Native guarded exact-one controls, preserving original ID order across inflation.
  const base="000 002 010 011 021 022 100 101 111 201 202 221 110".split(" ").map(s=>s.split("").map(Number));
  let T=base,n=3, native=[];
  function nativeSolve(T,n,pins){
    const rows=range(3*n).map(()=>[]),tr=T.map(t=>t.map((x,c)=>c*n+x));
    tr.forEach((rs,i)=>rs.forEach(r=>rows[r].push(i)));
    let calls=0,witness=null,forbid=new Set(pins.filter(p=>p[1]===0).map(p=>p[0]));
    function search(covered,sel){
      calls++;if(covered.size===3*n){witness=sel;return true;}
      let best=null;for(let r=0;r<3*n;r++)if(!covered.has(r)){let L=rows[r].filter(i=>!forbid.has(i)&&tr[i].every(v=>!covered.has(v)));if(best===null||L.length<best.length)best=L;}
      for(let i of best)if(search(new Set([...covered,...tr[i]]),[...sel,i]))return true;return false;
    }
    let ok=search(new Set,[]);if(ok){assert(witness.every(i=>!forbid.has(i)));for(let r of rows)assert(r.filter(i=>witness.includes(i)).length===1);}
    return {ok,calls,witness};
  }
  let leaf=12;
  for(let depth=0;depth<=2;depth++){
    let yes=nativeSolve(T,n,[]),no=nativeSolve(T,n,[[leaf,0]]),del=nativeSolve(T.filter((_,i)=>i!==leaf),n,[]);
    assert(yes.ok&&!no.ok&&!del.ok);native.push({depth,triples:T.length,leaf,yes,no,delete:del});
    let old=T;T=old.flatMap(([a,b,c],i)=>{let z=n+i;return [[z,z,z],[a,z,z],[z,b,c]]});n+=old.length;leaf=leaf*3+1;
  }
  return {seed:2611261202,checks,systems,fibers,syndromeClasses,screened,native};
};
console.log(JSON.stringify(audit(),null,2));
