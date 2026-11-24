function run(){
  let seed=113024;const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed>>>16};const bit=()=>rand()&1;
  const pc=x=>{let n=0;while(x){x&=x-1;n++}return n};const parity=x=>pc(x)&1;
  const flip=(S,x)=>S.has(x)?S.delete(x):S.add(x);
  function add(A,B){let C=new Set(A);for(let x of B)flip(C,x);return C}
  function mul(A,B){let C=new Set();for(let x of A)for(let y of B)flip(C,x|y);return C}
  function evaluate(P,x){let v=0;for(let m of P)if((x&m)===m)v^=1;return v}
  function restrict(P,i,b){let S=new Set(),v=1<<i;for(let m of P){if(!(m&v))flip(S,m);else if(b)flip(S,m^v)}return S}
  function gauss(P,n){let R=new Set(P),k=n,f=1;while(true){let e=[...R].find(x=>pc(x)===2);if(e===undefined)break;let i=e&-e,j=e^i,A=new Set(),B=new Set(),C=new Set();for(let m of R){if(m===e)continue;if(m&i)flip(A,m^i);else if(m&j)flip(B,m^j);else flip(C,m)}R=add(C,mul(A,B));k-=2;f*=2}return [...R].some(x=>x!==0)?0:f*2**k*(R.has(0)?-1:1)}
  function count(eq,n){let total=0;for(let mask=0;mask<2**eq.length;mask++){let P=new Set();for(let i=0;i<eq.length;i++)if(mask>>i&1)P=add(P,eq[i]);total+=gauss(P,n)}return total/2**eq.length}
  function insert(B,x){while(x){let j=31-Math.clz32(x);if(B[j])x^=B[j];else{B[j]=x;return true}}return false}
  function kernel(B,d){let out=[];for(let i=0;i<d;i++)if(!B[i]){let x=1<<i;for(let j=0;j<d;j++)if(B[j]&&parity(B[j]&x))x^=1<<j;out.push(x)}return out}
  function findWitness(eq,n){let E=eq.slice(),x=0,calls=1;if(!count(E,n))return {x:null,calls};for(let i=0;i<n;i++){let A=E.map(P=>restrict(P,i,0));calls++;if(count(A,n))E=A;else{E=E.map(P=>restrict(P,i,1));x|=1<<i}}if(!eq.every(P=>!evaluate(P,x)))throw Error("invalid reconstruction");return{x,calls}}
  function feature(p,x){return p.reduce((v,P,i)=>v|(evaluate(P,x)<<i),0)}
  function basis(eq,p,n){let B=[],calls=0,probes=0,w=[];while(true){let grew=false;for(let f of kernel(B,p.length)){let P=new Set([0]);for(let i=0;i<p.length;i++)if(f>>i&1)P=add(P,p[i]);let r=findWitness([...eq,P],n);calls+=r.calls;probes++;if(r.x===null)continue;let v=feature(p,r.x);if(!insert(B,v))throw Error("no progress");w.push(r.x);grew=true;break}if(!grew)return{B,w,calls,probes}}}
  function quad(n){let P=new Set();if(bit())P.add(0);for(let i=0;i<n;i++){if(bit())P.add(1<<i);for(let j=i+1;j<n;j++)if(bit())P.add((1<<i)|(1<<j))}return P}
  const rank=B=>B.filter(Boolean).length;
  const stats={seed:113024,randomSystems:0,sat:0,unsat:0,referenceAssignments:0,dualProbes:0,fourierCalls:0,verifiedWitnesses:0,guardPinQueries:0,fano:{},rankChecks:0};
  for(let t=0;t<100;t++){let n=3+rand()%4,r=1+rand()%4,eq=Array.from({length:r},()=>quad(n)),p=[new Set([0]),...Array.from({length:n},(_,i)=>new Set([1<<i])),quad(n),quad(n)];
    // Contradictory pair has no constant equation and each individual equation is satisfiable.
    if(t%10===0){let Q=new Set([3,1]);eq=[Q,add(Q,new Set([0]))]}
    let ref=[],nr=0;for(let x=0;x<2**n;x++){stats.referenceAssignments++;if(eq.every(P=>!evaluate(P,x))){nr++;insert(ref,feature(p,x))}}
    let b=basis(eq,p,n);stats.dualProbes+=b.probes;stats.fourierCalls+=b.calls;stats.verifiedWitnesses+=b.w.length;
    let both=[...ref];for(let v of b.B)if(v)insert(both,v);if(rank(both)!==rank(ref)||rank(b.B)!==rank(ref)||count(eq,n)!==nr)throw Error("basis/count disagreement");
    stats.randomSystems++;if(nr)stats.sat++;else stats.unsat++;
    for(let a=0;a<4;a++){let E=eq.map(P=>restrict(restrict(P,0,a&1),1,a>>1));let r=findWitness(E,n);let direct=0;for(let x=0;x<2**n;x++)if((x&3)===a&&eq.every(P=>!evaluate(P,x)))direct++;if((r.x!==null)!==(direct>0))throw Error("guard error");if(r.x!==null&&!eq.every(P=>!evaluate(P,(r.x&~3)|a)))throw Error("guard lift");stats.guardPinQueries++;stats.fourierCalls+=r.calls}
  }
  const edges=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
  const polys=edges.map(([i,j,k])=>new Set([0,1<<i,1<<j,1<<k,(1<<i)|(1<<j),(1<<i)|(1<<k),(1<<j)|(1<<k)]));
  // NAE indicator is 1 when monochromatic. Verify against direct relation.
  for(let x=0;x<128;x++)for(let t=0;t<edges.length;t++){let [i,j,k]=edges[t];let sum=((x>>i)&1)+((x>>j)&1)+((x>>k)&1);if(evaluate(polys[t],x)!==+(sum===0||sum===3))throw Error("NAE encoding")}
  let cols=new Map(),next=0,B=[];for(let P of polys){let v=0;for(let m of P)if(pc(m)===2){if(!cols.has(m))cols.set(m,next++);v|=1<<cols.get(m)}insert(B,v)}stats.fano.quadraticRank=rank(B);
  stats.fano.fullCount=count(polys,7);stats.fano.edgeDeletionCounts=polys.map((_,i)=>count(polys.filter((_,j)=>i!==j),7));if(stats.fano.fullCount!==0||stats.fano.edgeDeletionCounts.some(x=>x<=0)||rank(B)!==7)throw Error("Fano control");
  return stats
}
console.log(JSON.stringify(run(),null,2));
