function runGD02(){
  const bit=i=>1n<<BigInt(i);
  const parity=x=>{let p=0;while(x){p^=1;x&=x-1n}return p};
  const pivot=x=>x.toString(2).length-1;
  function reduce(x,B){while(x){let p=pivot(x);if(!B.has(p))break;x^=B.get(p)}return x}
  function insert(x,B){x=reduce(x,B);if(!x)return false;B.set(pivot(x),x);return true}
  function rowReduce(x,B){for(const p of [...B.keys()].sort((a,b)=>b-a))if(x&bit(p))x^=B.get(p);return x}
  function basis(xs){const B=new Map();for(const x of xs)insert(x,B);return B}
  function addTagged(x,t,B){while(x){const p=pivot(x);if(!B.has(p)){B.set(p,[x,t]);return [true,t]}const [y,u]=B.get(p);x^=y;t^=u}return [false,t]}
  function obs(x,rows){let a=0;rows.forEach((r,i)=>a|=parity(x&r)<<i);return a}
  function evalF(x,f){return f.ok[obs(x,f.rows)]}
  function closure(d,F,initial=[]){const eq=new Map();let contradiction=false,added=0,passes=0;
    function add(r,b,B){let x=r,y=b;while(x){let p=pivot(x);if(!B.has(p)){B.set(p,[x,y]);return 1}const [a,c]=B.get(p);x^=a;y^=c}return y?-1:0}
    for(const [r,b] of initial)if(add(r,b,eq)<0)contradiction=true;
    let change=true;while(change&&!contradiction){change=false;passes++;
      for(const f of F){const q=f.rows.length,allowed=[];
        for(let a=0;a<(1<<q);a++){if(!f.ok[a])continue;const E=new Map(eq);let ok=true;for(let j=0;j<q;j++)if(add(f.rows[j],(a>>j)&1,E)<0){ok=false;break}if(ok)allowed.push(a)}
        if(!allowed.length){contradiction=true;break}
        for(let u=1;u<(1<<q);u++){const b=parity(BigInt(u&allowed[0]));if(!allowed.every(a=>parity(BigInt(u&a))===b))continue;let r=0n;for(let j=0;j<q;j++)if(u&(1<<j))r^=f.rows[j];const z=add(r,b,eq);if(z<0){contradiction=true;break}if(z){added++;change=true}}
        if(contradiction)break;
      }
    }return {contradiction,added,passes,eq:[...eq.values()]}
  }
  function features(r,k){const out=[0n];function rec(start,left,v){if(!left){out.push(v);return}for(let i=start;i<=r-left;i++)rec(i+1,left-1,v|bit(i))}for(let j=1;j<=Math.min(k,r);j++)rec(0,j,0n);return out}
  function feature(x,mon){let z=0n;for(let i=0;i<mon.length;i++)if((x&mon[i])===mon[i])z|=bit(i);return z}
  function boundary(prefix,suffix){const Q=basis(suffix),R=new Map(),out=[];for(let j=0;j<prefix.length;j++){const [ind,t]=addTagged(rowReduce(prefix[j],Q),bit(j),R);if(!ind)out.push(t)}return out}
  function dp(d,input,k){
    const F=input.map(f=>({rows:f.rows.slice(),ok:f.ok.slice()})),G=new Map(),P=[],stages=[];
    function compile(f){const before=P.length,rows=[];for(const r of f.rows){const [ind,t]=addTagged(r,bit(P.length),G);if(ind){P.push(r);rows.push(bit(P.length-1))}else rows.push(t^bit(P.length))}stages.push({before,after:P.length,rows,ok:f.ok,original:f.rows});}
    F.forEach(compile);for(let j=0;j<d;j++){let x=bit(j);const tmp=new Map(G);if(addTagged(x,bit(P.length),tmp)[0])compile({rows:[x],ok:[true,true]})}
    if(P.length!==d)throw Error("basis completion failed");
    const boundaries=stages.map((s,i)=>boundary(P.slice(0,s.after),stages.slice(i+1).flatMap(t=>t.original)));
    let states=new Map([[0n,{points:[0n],B:new Map([[0,1n]])}]]),peak=1,peakPoints=1,trans=0,updates=0,width=0;
    function key(x,B){let v=0n;B.forEach((r,j)=>{if(parity(x&r))v|=bit(j)});return v}
    for(let i=0;i<stages.length;i++){
      const s=stages[i],B=boundaries[i],next=new Map(),mon=features(s.after,k);width=Math.max(width,B.length);
      for(const cell of states.values())for(let a=0;a<2**(s.after-s.before);a++){
        trans++;const extension=BigInt(a)<<BigInt(s.before),first=cell.points[0]|extension;
        if(!s.ok[obs(first,s.rows)])continue;
        const t=key(first,B);let c=next.get(t);if(!c){c={points:[],B:new Map()};next.set(t,c)}
        for(const p of cell.points){const z=p|extension;if(key(z,B)!==t||!s.ok[obs(z,s.rows)])throw Error("boundary mismatch");updates++;if(insert(feature(z,mon),c.B))c.points.push(z)}
      }
      states=next;peak=Math.max(peak,states.size);peakPoints=Math.max(peakPoints,[...states.values()].reduce((s,c)=>s+c.points.length,0));
    }
    function lift(y){const E=new Map();for(let j=0;j<d;j++){let x=P[j],b=parity(y&bit(j));while(x){const p=pivot(x);if(!E.has(p)){E.set(p,[x,b]);break}const [r,c]=E.get(p);x^=r;b^=c}}
      let z=0n;for(const p of [...E.keys()].sort((a,b)=>a-b)){const [r,b]=E.get(p);if(parity(z&r)!==b)z|=bit(p)}return z}
    const pts=[...states.values()].flatMap(c=>c.points).map(lift);for(const x of pts)if(!input.every(f=>evalF(x,f)))throw Error("invalid reconstructed witness");
    return {pts,width,peak,peakPoints,trans,updates,rank:pts.length};
  }
  let seed=20261124;const rand=n=>{seed=(Math.imul(1664525,seed)+1013904223)>>>0;return (seed>>>8)%n};
  const forbid=(rows,a)=>({rows,ok:Array.from({length:2**rows.length},(_,j)=>j!==a)});
  const eqF=(r,b)=>({rows:[r],ok:[b===0,b===1]});
  let agg={randomCases:0,sat:0,unsat:0,referenceAssignments:0,closureRejected:0,closureEquations:0,affineChecks:0,quadraticChecks:0,cubicChecks:0,strictQuadraticGain:0,strictCubicGain:0,witnesses:0,disagreements:0};
  function check(d,F){
    const ref=[];for(let x=0;x<2**d;x++){agg.referenceAssignments++;if(F.every(f=>evalF(BigInt(x),f)))ref.push(BigInt(x))}
    const c=closure(d,F);agg.closureEquations+=c.added;if(c.contradiction){agg.closureRejected++;if(ref.length)throw Error("closure false UNSAT")}
    if(ref.length)agg.sat++;else agg.unsat++;
    let ranks=[];
    for(const k of [1,2,3]){
      const res=dp(d,F,k),mon=features(d,k),refB=basis(ref.map(x=>feature(x,mon))),gotB=basis(res.pts.map(x=>feature(x,mon)));
      if(refB.size!==gotB.size||ref.some(x=>rowReduce(feature(x,mon),gotB)!==0n))throw Error("hull mismatch");
      agg[["","affineChecks","quadraticChecks","cubicChecks"][k]]++;agg.witnesses+=res.pts.length;ranks.push(refB.size);
      if(k===1&&ref.length){const a=res.pts[0],L=basis(res.pts.map(x=>x^a)),derived=[];for(let u=1;u<2**d;u++){const r=BigInt(u);if([...L.values()].every(v=>!parity(v&r)))derived.push([r,parity(a&r)])}const post=closure(d,F,derived);if(post.contradiction)throw Error("post closure");for(const [r,b] of post.eq)if(ref.some(x=>parity(x&r)!==b))throw Error("post forcing wrong")}
    }
    if(ref.length&&ranks[0]===d+1&&ranks[1]<features(d,2).length)agg.strictQuadraticGain++;
    if(ref.length&&ranks[1]===features(d,2).length&&ranks[2]<features(d,3).length)agg.strictCubicGain++;
  }
  for(let t=0;t<260;t++){const d=3+rand(5),m=1+rand(12),F=[];for(let j=0;j<m;j++){const q=1+rand(3),rows=[];for(let a=0;a<q;a++)rows.push(BigInt(rand(2**d)));F.push(forbid(rows,rand(2**q)))}check(d,F);agg.randomCases++}
  const controls=[];for(const d of [3,4,5,6]){const F=[forbid(Array.from({length:d},(_,j)=>bit(j)),0)];const ranks=[1,2,3].map(k=>dp(d,F,k).rank);controls.push({d,case:"OR",ranks,featureCounts:[1,2,3].map(k=>features(d,k).length)});check(d,F)}
  // Dense invertible linear transform of a chain of overlapping OR clauses.
  const scale=[];for(const d of [8,16,32,64,128]){
    const R=Array.from({length:d},(_,j)=>bit(j));for(let t=0;t<3*d;t++){const a=rand(d),b=rand(d);if(a!==b)R[a]^=R[b]}
    const F=[];for(let j=0;j<d-1;j++)F.push(forbid([R[j],R[j+1]],1)); // monotone chain (forbids 10)
    const cases=[["SAT",F],["UNSAT",[eqF(R[0],1),...F,eqF(R[d-1],0)]]];
    for(const [label,G] of cases){const c=closure(d,G),r=dp(d,G,1);if((r.rank>0)!==(label==="SAT"))throw Error("scale decision");scale.push({d,label,width:r.width,rank:r.rank,peakStates:r.peak,peakWitnesses:r.peakPoints,transitions:r.trans,featureInsertions:r.updates,closureRejected:c.contradiction})}
  }
  return {seed:20261124,...agg,controls,scale,note:"Small exact affine and degree-2/3 monomial span comparisons; closure baseline independently verified; DP also run on closure-rejected controls as an audit, not a solver requirement. Scaling degree 1 only. No strict wheel compiler, matching oracle, decomposition discovery or physical CM benchmark."};
}
console.log(JSON.stringify(runGD02(),null,2));
