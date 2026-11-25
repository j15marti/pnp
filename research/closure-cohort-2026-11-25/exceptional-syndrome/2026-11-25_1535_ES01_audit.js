// ES01 deterministic exact audit. Run: node this_file.js
function audit(){
  const B=i=>1n<<BigInt(i), mask=n=>B(n)-1n, hi=x=>x.toString(2).length-1;
  const xor=a=>a.reduce((s,x)=>s^x,0n);
  function parity(x){let p=0;while(x){x&=x-1n;p^=1}return p}
  let checks=0;
  function ok(q,m){checks++;if(!q)throw Error(m)}
  function add(b,x){while(x){let j=hi(x);if(b.has(j))x^=b.get(j);else{b.set(j,x);return true}}return false}
  function basis(rows){let b=new Map(),out=[];for(let x of rows)if(add(b,x))out.push(x);return out}
  function coords(rows,target,projection){let b=new Map();for(let i=0;i<rows.length;i++){let x=rows[i]&projection,t=B(i);while(x){let j=hi(x);if(b.has(j)){let [u,v]=b.get(j);x^=u;t^=v}else{b.set(j,[x,t]);break}}}let x=target&projection,t=0n;while(x){let z=b.get(hi(x));if(!z)return null;x^=z[0];t^=z[1]}return t}
  function combine(rows,c){let x=0n;for(let j=0;j<rows.length;j++)if(c&B(j))x^=rows[j];return x}
  function complete(M){let n=M.length,C=Array(n).fill(0n),inc=0;for(let i=n-1;i>=0;i--){let later=C.slice(i+1),prefix=mask(i),r=M[i]&prefix,c=coords(later,r,prefix);if(c===null){C[i]=r;inc++}else C[i]=combine(later,c)}let R=basis(C),U=C.map(x=>coords(R,x,mask(n))),T=M.map((x,i)=>x^C[i]);ok(R.length===inc,"completion rank");for(let i=0;i<n;i++){ok((T[i]&mask(i))===0n,"triangular");ok(combine(R,U[i])===C[i],"factor")}return {T,R,U,C,k:R.length}}
  function forced(M){let z=0n;for(;;){let old=z;for(let i=0;i<M.length;i++)if(!(z&B(i))&&(M[i]&~z)===B(i))z|=B(i);if(z===old)return z}}
  const valid=(M,p)=>M.every((r,i)=>!(p&B(i))||parity(r&p)===0);
  function testGuard(p,G){return G.every(([r,v])=>parity(r&p)===v)}
  function monomials(n,d){let map=new Map(),idx=0;function visit(s,i,j){map.set(s,B(idx++));if(j)for(let h=i;h<n;h++)visit(s|B(h),h+1,j-1)}visit(0n,0,d);return map}
  function lift(p,d,mon){let bits=[];for(let x=p;x;x&=x-1n)bits.push(x&-x);let out=0n;function visit(s,i,j){out|=mon.get(s);if(j)for(let h=i;h<bits.length;h++)visit(s|bits[h],h+1,j-1)}visit(0n,0,d);return out}
  let totalModes=0,totalTransitions=0,peakBasis=0,peakD=0,forcedBits=0;
  function solve(M,G,F=complete(M)){
    let n=M.length,k=F.k,d=Math.min(n,k+G.length),mon=monomials(n,d),z=forced(M);
    peakD=Math.max(peakD,mon.size);for(let x=z;x;x&=x-1n)forcedBits++;
    for(let c=0n;c<B(k);c++){
      totalModes++;let rep=[0n];
      for(let i=n-1;i>=0;i--){
        let next=[],bas=new Map();for(let p of rep){let opts=[p];if(!(z&B(i))&&((Number(!!(F.T[i]&B(i)))^parity(F.T[i]&p)^parity(F.U[i]&c))===0))opts.push(p|B(i));for(let q of opts){totalTransitions++;if(add(bas,lift(q,d,mon)))next.push(q)}}
        rep=next;peakBasis=Math.max(peakBasis,rep.length);
      }
      for(let p of rep){let a=0n;for(let j=0;j<k;j++)if(parity(F.R[j]&p))a|=B(j);if(a===c&&testGuard(p,G)){ok(valid(M,p),"lift soundness");ok((p&z)===0n,"forced zero");return p}}
    }return null
  }
  function brute(M,G){for(let p=0n;p<B(M.length);p++)if(valid(M,p)&&testGuard(p,G))return p;return null}
  let completionCases=0,completionAlternatives=0;
  for(let n=1;n<=4;n++){let low=[],free=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++)(j<i?low:free).push([i,j]);for(let a=0;a<(1<<low.length);a++){let M=Array(n).fill(0n);low.forEach(([i,j],h)=>{if(a>>h&1)M[i]|=B(j)});let k=complete(M).k,best=n;for(let f=0;f<(1<<free.length);f++){let C=M.slice();free.forEach(([i,j],h)=>{if(f>>h&1)C[i]|=B(j)});best=Math.min(best,basis(C).length);completionAlternatives++}ok(k===best,"optimal completion");completionCases++}}
  let seed=20261125;function rnd(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed}
  function randrow(n){let a=0n;for(let i=0;i<n;i++)if(rnd()>>>31)a|=B(i);return a}
  let randomCases=0,randomSat=0,randomUnsat=0,jointCases=0,jointSat=0,jointUnsat=0;
  for(let r=0;r<180;r++){let n=3+r%7,k=r%3,R=Array.from({length:k},()=>randrow(n)),U=Array.from({length:n},()=>randrow(k)),T=Array.from({length:n},(_,i)=>randrow(n)&~mask(i)),M=T.map((x,i)=>x^combine(R,U[i])),b=randrow(n)||1n,F=complete(M);
    ok(F.k<=k,"completion above supplied rank");let G=[[b,1]],p=solve(M,G,F),q=brute(M,G);ok((p===null)===(q===null),"random decision");randomCases++;if(p===null)randomUnsat++;else randomSat++;
    if(r<90){let G2=[[b,1],[randrow(n),r%2]],s=solve(M,G2,F),t=brute(M,G2);ok((s===null)===(t===null),"joint guards");jointCases++;if(s===null)jointUnsat++;else jointSat++}
  }
  function strong(M){let n=M.length;for(let i=0;i<n;i++){let r=B(i);for(let j=0;j<n;j++){let s=r;for(let k=0;k<n;k++)if(r&B(k))s|=M[k];if(s===r)break;r=s}if(r!==mask(n))return false}return true}
  function symSCC(M){let n=M.length,reach=M.map((r,i)=>r|B(i));for(let k=0;k<n;k++)for(let i=0;i<n;i++)if(reach[i]&B(k))reach[i]|=reach[k];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)if((reach[i]&B(j))&&(reach[j]&B(i))&&(!!(M[i]&B(j))!==!!(M[j]&B(i))))return false;return true}
  function altern(M){let n=M.length;return M.map((r,i)=>{let s=r;for(let j=0;j<n;j++)if(M[j]&B(i))s^=B(j);return s})}
  let large=[];
  for(let n of [8,16,32,64,96]){let M=Array.from({length:n},(_,i)=>mask(n)&~mask(i));M[0]^=B(n-1);M[n-1]|=1n;let F=complete(M);
    ok(strong(M)&&!symSCC(M)&&F.k===1,"dense feedback family");
    let b0=1n|B(n-1),b1=mask(n),p0=solve(M,[[b0,1]],F),p1=solve(M,[[b1,1]],F);
    ok(p0===null&&p1!==null,"dense family labels");ok(basis(altern(M)).length===n,"alternating rank");let checksSmall=0;
    if(n<=16)for(let p=0n;p<B(n);p++){let want=p===0n||((p&b0)===b0&&(()=>{let t=p^b0;return t!==0n&&(t&(t-1n))===0n})());ok(valid(M,p)===want,"dense family exact support");checksSmall++}
    large.push({n,completionRank:F.k,alternatingRank:n,unsatDemand:b0.toString(),satDemand:b1.toString(),witness:p1.toString(),exhaustiveSupportChecks:checksSmall});
  }
  function strict(P){let m=P.length;for(let j=1n;j<B(m);j++){let vs=[];for(let i=0;i<m;i++)if(j&B(i))vs.push(P[i][0],P[i][1]);let c=0;for(let x=j;x;x&=x-1n)c++;ok(basis(vs).length>=c+1,"strict plane ranks")}ok(basis(P.flat()).length===m+1,"full dual rank")}
  function sums(P){let s=new Set([0n]);for(let plane of P){let t=new Set();for(let a of s)for(let v of plane)t.add(a^v);s=t}return s}
  function trans(P,fn,e=[],i=0){if(i===P.length){if(basis(e).length===e.length)fn(e);return}for(let a of P[i])trans(P,fn,e.concat(a),i+1)}
  function mkchart(e,f,t){let n=e.length,w=t^xor(f);if(coords(e,w,mask(n+1))!==null)return null;let M=Array.from({length:n},(_,i)=>B(i)),b=0n;for(let j=0;j<n;j++){let a=coords(e.concat(w),f[j],mask(n+1));ok(a!==null,"chart basis");for(let i=0;i<n;i++)if(a&B(i))M[i]^=B(j);if(a&B(n))b|=B(j)}return {M,b,e,f,w}}
  function liftPlane(P,ch,p,t){let y=ch.e.map((e,i)=>p&B(i)?e:ch.f[i]^(parity(ch.M[i]&p)?e:0n));ok(y.every((v,i)=>P[i].includes(v))&&xor(y)===t,"source plane lift")}
  function solvePlane(P,t){let e;trans(P,v=>{if(!e)e=v});ok(!!e,"transversal exists");let f=P.map((p,i)=>p.find(v=>v!==e[i])),n=e.length,c=coords(e,t^xor(f),mask(n+1));if(c!==null){let y=f.map((v,i)=>v^(c&B(i)?e[i]:0n));ok(xor(y)===t&&y.every((v,i)=>P[i].includes(v)),"direct hyperplane lift");return true}let ch=mkchart(e,f,t),p=solve(ch.M,[[ch.b,1]]);if(p===null)return false;liftPlane(P,ch,p,t);return true}
  let atom=[[15,32,47],[13,17,28],[14,36,42],[11,53,62],[10,39,45]].map(x=>x.map(BigInt));strict(atom);let sa=sums(atom);ok(sa.size===63&&!sa.has(29n),"atom missing syndrome");let transCount=0,chartCount=0,symmetricCharts=0,minK=6,best=null;
  trans(atom,e=>{transCount++;let f0=atom.map((p,i)=>p.find(v=>v!==e[i]));for(let q=0n;q<B(5);q++){let f=f0.map((v,i)=>v^(q&B(i)?e[i]:0n)),ch=mkchart(e,f,29n);ok(ch!==null,"missing candidate outside");chartCount++;if(symSCC(ch.M))symmetricCharts++;let F=complete(ch.M);if(F.k<minK){minK=F.k;best={ch,F}}}});
  ok(transCount===174&&chartCount===5568&&symmetricCharts===0,"atom chart reproduction");ok(solve(best.ch.M,[[best.ch.b,1]],best.F)===null,"atom terminal no");
  let atomSyndromes=0;for(let t=0n;t<64n;t++){ok(solvePlane(atom,t)===sa.has(t),"atom syndrome");atomSyndromes++}
  let groups=[[[0,1],[2,3]],[[0,2],[1,4]],[[0,3],[2,4]],[[0,4],[1,3]],[[1,2],[3,4]]],E=groups.flat(),L=E.map(([u,v])=>(u?B(u-1):0n)^(v?B(v-1):0n)),dep=[];
  for(let p=0n;p<B(10);p++)if(combine(L,p)===0n)dep.push(p);
  let D=basis(dep);ok(D.length===6,"K5 dependency rank");let H=L.map((_,j)=>D.reduce((a,r,i)=>a|(r&B(j)?B(i):0n),0n)),P=groups.map((_,i)=>[H[2*i],H[2*i+1],H[2*i]^H[2*i+1]]);strict(P);let S=sums(P),k5Syndromes=0;
  ok(S.size===63&&!S.has(0n),"K5 missing zero");
  for(let t=0n;t<64n;t++){ok(solvePlane(P,t)===S.has(t),"K5 syndrome");k5Syndromes++}
  let k5Labels=[];for(let signs of [0n,...Array.from({length:10},(_,i)=>B(i)),mask(10)]){let source=false;for(let p=0n;p<B(4);p++)if(groups.every((_,i)=>[0,1].some(j=>parity(L[2*i+j]&p)!==Number(!!(signs&B(2*i+j)))))){source=true;break}let t=combine(H,signs);ok(source===S.has(t),"K5 primal lift label");k5Labels.push({forbidden:signs.toString(),sat:source})}
  return {seed:20261125,assertions:checks,completionCases,completionAlternatives,randomCases,randomSat,randomUnsat,jointCases,jointSat,jointUnsat,totalModes,totalTransitions,peakBasis,peakD,forcedBits,large,atom:{missing:29,transCount,chartCount,symmetricCharts,minK,chart:{M:best.ch.M.map(String),b:String(best.ch.b),e:best.ch.e.map(String),f:best.ch.f.map(String),w:String(best.ch.w)},atomSyndromes},k5:{k5Syndromes,labels:k5Labels}}
}
console.log(JSON.stringify(audit(),null,2));
