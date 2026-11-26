function boundaryAudit(){
 let seed=6112604,checks=0;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
 function rank(V){let m=new Map();for(let v of V){while(v){let p=v.toString(2).length-1;if(!m.has(p)){m.set(p,v);break}v^=m.get(p)}}return m.size}
 function check(n,C,L){const E=i=>1n<<BigInt(i),R=C.map(c=>c.reduce((s,i)=>s^E(i),0n)),r=rank(R);let A=new Set(),B=new Set();C.forEach((c,j)=>c.forEach(i=>(L.has(j)?A:B).add(i)));let S=[...A].filter(i=>B.has(i)),U=[...new Set([...A,...B])];const q=s=>rank([...R,...[...s].map(E)])-r;let w=q(A)+q(B)-q(U),bs=q(S);checks++;if(w!==bs)throw Error("boundary identity");return {boundary:S.length,rank:bs,rawRank:r,free:n-r}}
 let random=0;for(let t=0;t<500;t++){let n=4+rnd(17),m=3+rnd(30),C=[];for(let j=0;j<m;j++){let s=new Set();while(s.size<3)s.add(rnd(n));C.push([...s])}let L=new Set(C.map((_,j)=>j).filter(()=>rnd(11)<5));check(n,C,L);random++}
 let native=[];for(let b of [2,4,8,16,32,64]){let C=[];for(let k=0;k<b;k++)for(let i=0;i<6;i++)C.push([6*k+(i+5)%6,6*k+i,6*k+(i+1)%6]);for(let k=0;k<b-1;k++){let a=6*k+3,c=6*(k+1);[C[a][1],C[c][1]]=[C[c][1],C[a][1]]}
 let L=new Set(C.map((_,j)=>j).filter(j=>Math.floor(j/6)%2===0));let v=check(6*b,C,L);checks++;if(v.boundary!==2*(b-1)||v.rank!==1||v.rawRank!==5*b-1||v.free!==b+1)throw Error("native rank formula");native.push({blocks:b,variables:6*b,...v})}
 return {seed:6112604,checks,randomClausePartitions:random,nativeAlternatingBlockCuts:native}
}
console.log(JSON.stringify(boundaryAudit(),null,2));
