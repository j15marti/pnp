function run(){
  let assertions=0;const check=(x)=>{assertions++;if(!x)throw Error("assertion "+assertions)};
  const plane=()=>({n:9,P:[...Array.from({length:3},(_,s)=>Array.from({length:3},(_,b)=>Array.from({length:3},(_,i)=>3*i+(s*i+b)%3))),Array.from({length:3},(_,i)=>[3*i,3*i+1,3*i+2])]});
  function ring(q){let L=12*q,P=[[],[],[],[]];for(let i=0;i<L;i++)for(let j=0;j<3;j++)P[(i+j)%3].push([3*i+j,3*((i+1)%L)+j,3*((i+1)%L)+(j+1)%3]);for(let b=0;b<q;b++)for(let j=0;j<3;j++){let t=b===0&&j===0?[[0,4,8],[1,3,6],[2,9,11],[5,7,10]]:j===2?[[0,2,5],[1,3,10],[4,7,9],[6,8,11]]:[[0,2,5],[1,3,8],[4,7,10],[6,9,11]];for(let row of t)P[3].push(row.map(i=>3*(12*b+i)+j))}let x=Array.from({length:3*L},(_,v)=>Math.floor(v/3)%2),y=x.slice();y[0]^=1;let z=x.map((a,v)=>a^+(v%3===Math.floor(v/3)%3));return{n:3*L,P,x,y,z}}
  const legal=(a,C)=>C.every(c=>{let k=c.reduce((s,v)=>s+a[v],0);return k===1||k===2});
  function colors(n,A,B){let right=Array(n);B.forEach((c,j)=>c.forEach(v=>right[v]=j));let unused=new Set(Array.from({length:n},(_,i)=>i)),color=Array(n).fill(-1);for(let k=0;k<3;k++){let match=Array(B.length).fill(-1);function aug(i,seen){for(let v of A[i])if(unused.has(v)&&!seen.has(right[v])){let j=right[v];seen.add(j);if(match[j]<0||aug(match[j],seen)){match[j]=i;return true}}return false}for(let i=0;i<A.length;i++)check(aug(i,new Set()));for(let j=0;j<B.length;j++){let v=A[match[j]].find(v=>unused.has(v)&&right[v]===j);check(v!==undefined);color[v]=k;unused.delete(v)}}check(!unused.size);return color}
  let rows=[],latticePairs=0,fractionalChecks=0,guardScans=0;
  for(let [name,F] of [["affine-plane",plane()],...([1,2,4,8].map(q=>["BS15-q"+q,ring(q)]))]){
    let {n,P}=F;let seen=new Set();for(let part of P){check(part.flat().length===n&&new Set(part.flat()).size===n);for(let c of part)for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let key=[c[i],c[j]].sort((a,b)=>a-b).join(",");check(!seen.has(key));seen.add(key)}}
    let exact=null,one=null;if(n===9){let X=[],Y=[];exact=0;for(let k=0;k<1<<n;k++){let a=Array.from({length:n},(_,i)=>(k>>i)&1);if(legal(a,P[0].concat(P[1])))X.push(a);if(legal(a,P[2].concat(P[3])))Y.push(a);if(legal(a,P.flat()))exact++}outer:for(let a of X)for(let b of Y)if(a.slice(1).every((v,i)=>v===b[i+1])&&a[0]!==b[0]){one=[a,b];break outer}check(exact===0&&one!==null)}else{check(legal(F.x,P[0].concat(P[1]))&&legal(F.y,P[2].concat(P[3]))&&legal(F.z,P.flat()));one=[F.x,F.y]}
    let pairCount=0,sampleCount=0;
    for(let pairing of [[[0,1],[2,3]],[[0,2],[1,3]],[[0,3],[1,2]]])for(let side of pairing){
      let A=P[side[0]],B=P[side[1]],C=A.concat(B),col=colors(n,A,B);
      for(let pin of [-1,0,1]){
        guardScans++;let a0=Array.from({length:n},(_,i)=>i===0&&pin>=0?pin:pin===0?12:pin===1?8:10); // seed uses actual numerator below
        if(pin>=0)a0[0]=20*pin;
        check(P.flat().every(c=>{let s=c.reduce((v,i)=>v+a0[i],0);return s>20&&s<40}));
        let words=[];
        for(let f=0;f<n;f++){if(pin>=0&&f===0)continue;let k=[0,1,2].find(k=>k!==col[f]&&(pin<0||k!==col[0]));let u=col.map(c=>+(c===k)),v=u.slice();v[f]=1;if(pin===1){u=u.map(x=>1-x);v=v.map(x=>1-x)}check(legal(u,C)&&legal(v,C));check(pin<0||u[0]===pin&&v[0]===pin);check(u.every((x,i)=>i===f?x!==v[i]:x===v[i]));latticePairs++;pairCount++;words.push(u,v)}
        if(n===9){words=[];for(let k=0;k<1<<n;k++){let a=Array.from({length:n},(_,i)=>(k>>i)&1);if((pin<0||a[0]===pin)&&legal(a,C))words.push(a)}}
        for(let a of words){let b=a0.map((v,i)=>v-a[i]);check(b.every(v=>v>=0&&v<=19));check(C.every(c=>{let s=c.reduce((v,i)=>v+b[i],0);return s>=19&&s<=38}));check(pin<0||b[0]===19*pin);check(b.every((v,i)=>v+a[i]===a0[i]));fractionalChecks++;sampleCount++}
      }
    }
    rows.push({name,n,exactJointCount:exact,knownSAT:exact===null,oneMismatch:one[0].filter((x,i)=>x!==one[1][i]).length,latticePairs:pairCount,fractionalWitnessChecks:sampleCount});
  }
  return {assertions,latticePairs,fractionalChecks,guardScans,rows,scope:"Exact integer numerator checks and matching decomposition; no LP backend, full repair search, or semantic closure."};
}
console.log(JSON.stringify(run(),null,2));
