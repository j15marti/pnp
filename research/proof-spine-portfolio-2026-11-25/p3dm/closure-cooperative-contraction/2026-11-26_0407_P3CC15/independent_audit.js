// Node.js independent native rotation, witness, exact phase count and projection audit.
const run=()=>{
  let assertions=0; const ok=(v)=>{assertions++;if(!v)throw Error("assertion "+assertions)};
  const B=[[1,0,0],[2,0,0],[1,1,1],[2,1,1],[0,2,2],[2,0,1],[0,1,2],[1,1,2],[0,2,0],[1,2,0]], C=Array.from({length:8},(_,i)=>[i>>2,i>>1&1,i&1]);
  const RB=[[13,15,17],[9,11,16,18],[12,14,10],[10,14,9],[11,12,15,16],[13,17,18],[17,10,9,18],[14,12,11],[15,13,16],[6,3,1],[2,3,6],[1,7,4],[4,7,2],[0,5,8],[3,2,7],[4,0,8],[8,1,4],[5,0,6],[1,5,6]];
  const RC=[[6,8,9,7],[10,11,13,12],[6,7,11,10],[9,8,12,13],[8,6,10,12],[7,9,13,11],[0,2,4],[2,0,5],[3,0,4],[5,0,3],[4,2,1],[1,2,5],[1,3,4],[1,5,3]];
  const P=[[0,3,4],[1,2,4],[5,6,9],[5,7,8]], L=[[0,7],[1,6],[2,5],[3,4]];
  function phaseCount(k){let f=[1n,3n,3n,3n];for(let i=1;i<k;i++)f=f.map((_,q)=>[0,1,2,3].reduce((z,p)=>z+((p===2)===(q===3)?f[p]:0n),0n)*(q===0?1n:3n));return f.reduce((a,b)=>a+b,0n)}
  function family(k){
    const n=5*k,T=[],R=Array(33*k);for(let i=0;i<k;i++)for(let t of B)T.push(t.map(x=>5*i+x));for(let i=0;i<k;i++)for(let t of C)T.push(t.map(x=>5*i+3+x));
    function unit(r,sz,off,id){const map=(v)=>v<3*sz?Math.floor(v/sz)*n+off+v%sz:3*n+id+v-3*sz;for(let i=0;i<r.length;i++)R[map(i)]=r[i].map(map)}
    for(let i=0;i<k;i++){unit(RB,3,5*i,10*i);unit(RC,2,5*i+3,10*k+8*i)}
    function swap(a,b,c){let x=c*n+T[a][c],y=c*n+T[b][c],u=3*n+a,v=3*n+b;function rep(i,j,h){let q=R[i].indexOf(j);ok(q>=0);R[i][q]=h}rep(u,x,y);rep(x,u,v);rep(v,y,x);rep(y,v,u);[T[a][c],T[b][c]]=[T[b][c],T[a][c]]}
    for(let i=0;i<k-1;i++)swap(10*i+6,10*(i+1)+7,1);for(let i=0;i<k;i++)swap(10*i,10*k+8*i,0);
    ok(new Set(T.map(t=>t.join(","))).size===18*k);for(let u=0;u<R.length;u++){ok(new Set(R[u]).size===R[u].length);for(let v of R[u])ok(R[v].includes(u))}
    for(let j=0;j<T.length;j++)ok(T[j].every((x,c)=>R[3*n+j].includes(c*n+x)));
    let seen=new Set(),faces=0;for(let u=0;u<R.length;u++)for(let v of R[u])if(!seen.has(u+","+v)){faces++;let a=u,b=v;while(!seen.has(a+","+b)){seen.add(a+","+b);let d=R[b][(R[b].indexOf(a)+1)%R[b].length];a=b;b=d}ok(a===u&&b===v)}ok(seen.size===108*k);ok(R.length-seen.size/2+faces===2);
    let reach=new Set([0]),q=[0];while(q.length)for(let v of R[q.pop()])if(!reach.has(v)){reach.add(v);q.push(v)}ok(reach.size===R.length);
    const verify=ids=>{ok(ids.length===n&&new Set(ids).size===n);for(let c=0;c<3;c++)ok(new Set(ids.map(j=>T[j][c])).size===n);return ids};
    const lift=(F,leaf=-1,pick=1)=>verify(F.flatMap((p,i)=>P[p].map(j=>10*i+j)).concat(F.flatMap((p,i)=>L[p===0?0:(i===leaf?pick:1)].map(j=>10*k+8*i+j))));
    let W=[];for(let i=0;i<k;i++)for(let p=0;p<4;p++){let F=Array(k).fill(1);F[i]=p;for(let a=i-1;a>=0;a--)F[a]=F[a+1]===3?2:1;for(let a=i+1;a<k;a++)F[a]=F[a-1]===2?3:1;W.push(lift(F))}for(let i=0;i<k;i++)for(let p=1;p<4;p++)W.push(lift(Array(k).fill(1),i,p));
    const support=Array(T.length).fill(0);for(let ids of W)for(let j of ids)support[j]++;ok(support.every(v=>v>0&&v<W.length));
    const footprint=ids=>new Set(ids.filter(j=>j<10*k).map(j=>T[j][0]));let F0=footprint(lift(Array(k).fill(1)));for(let i=0;i<k;i++){let F=Array(k).fill(1);F[i]=0;let X=footprint(lift(F));ok([...F0].filter(x=>!X.has(x)).join(",")===String(5*i+1));ok([...X].filter(x=>!F0.has(x)).join(",")===String(5*i+3))}
    let D=new Map();for(let j=0;j<10*k;j++){let [x,y,z]=T[j],key=y+","+z;if(!D.has(key))D.set(key,new Set());D.get(key).add(x)}
    const contains=(a,b)=>[...a].every(x=>b.has(x));
    for(let i=0;i<k;i++){let a=5*i,ref=[new Set([a+2,a+3]),new Set([a+1,a+2]),new Set([a])];for(let r=0;r<3;r++){let d=D.get((a+r)+","+(a+r));ok(d.size===ref[r].size&&contains(ref[r],d))}for(let r=0;r<2;r++)ok([...D.entries()].filter(([p,d])=>contains(ref[r],d)).map(([p])=>p).join()===((a+r)+","+(a+r)));let bad=D.get((a+2)+","+a);ok(bad.size===2&&bad.has(a)&&bad.has(a+1));ok(!ref.some(d=>contains(bad,d)))}
    let off=Array(k).fill(1);off[0]=3;lift(off); // actual offdiagonal witness on first block.
    let bad=[5,7,9];for(let i=1;i<k;i++)bad.push(...P[1].map(j=>10*i+j));ok(new Set(bad.map(j=>T[j][1])).size===3*k);ok(new Set(bad.map(j=>T[j][2])).size===3*k);ok(!bad.some(j=>T[j][0]===0));
    let projectionWords=0,bruteCount=null;
    if(k<=3){
      let rows=Array.from({length:n},()=>[]);T.forEach((t,j)=>rows[t[1]].push(j));let full=0n;
      function brute(y,X,Z){if(y===n){full++;return}for(let j of rows[y]){let [x,,z]=T[j];if(!X.has(x)&&!Z.has(z)){X.add(x);Z.add(z);brute(y+1,X,Z);X.delete(x);Z.delete(z)}}}brute(0,new Set(),new Set());ok(full===phaseCount(k));bruteCount=String(full);
      let ys=Array.from({length:3*k},(_,i)=>5*Math.floor(i/3)+i%3);
      function projected(i,Z,ids){if(i===ys.length){projectionWords++;let X=new Set(ids.map(j=>T[j][0]));for(let b=0;b<k;b++)ok([5*b+1,5*b+2,5*b+3].filter(x=>X.has(x)).length<=2);return}for(let j of rows[ys[i]]){let z=T[j][2];if(!Z.has(z)){Z.add(z);ids.push(j);projected(i+1,Z,ids);ids.pop();Z.delete(z)}}}projected(0,new Set(),[]);
    }
    // Local independent audit of each diagonal/offdiagonal indexed PM after reversing Y seams.
    const main=[...B.map(t=>t.slice())];main[0][0]=3;
    let local=0;for(let a of [0,1]){const A=Array.from({length:3},(_,y)=>main.filter(t=>t[1]===y&&t[2]===(y+a)%3));for(let x of A[0])for(let y of A[1])for(let z of A[2]){local++;let S=new Set([x[0],y[0],z[0]]);ok([1,2,3].filter(v=>S.has(v)).length<=2)}}
    return {k,triples:T.length,faces,verifiedWitnesses:W.length,mainRank:3*k,log2FootprintLowerBound:k,exactCoverCount:String(phaseCount(k)),bruteCount,projectionWords,localIndexedPatterns:local};
  }
  const scales=[1,2,3,4,8,16,32,64,128].map(family);
  return {assertions,scales};
};
console.log(JSON.stringify(run(),null,2));
